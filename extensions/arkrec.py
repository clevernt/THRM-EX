from typing import Union
from typing import Sequence
import aiohttp
from bs4 import BeautifulSoup
from thefuzz import fuzz
from thefuzz import process
import lightbulb
import hikari
import requests
import json
from difflib import get_close_matches
from requests_html import HTMLSession
import re

session = HTMLSession()
plugin = lightbulb.Plugin('arkrec')

@plugin.command
@lightbulb.option('category', 'Category', required=True, autocomplete=True)
@lightbulb.option('mode', "Mode", choices=["Normal Mode", "Challenge Mode"], required=False, default=None)
@lightbulb.option('stage', 'Stage Name', required=True)
@lightbulb.command('arkrec', 'finds clears from arkrec', auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def arkrec(ctx):
    arkrec_url = "https://arkrec.com/api/records"
    stage = ctx.options.stage.strip()
    categoryy = ctx.options.category.strip()
    if ctx.options.mode:
        mode = ctx.options.mode.strip()
        if mode == "Normal Mode":
            mode = "normal"
        elif mode == "Challenge Mode":
            mode = "challenge"
        else:
            mode = None
    else:
        mode = None
    def get_stage_name(stage_code: str) -> str:
        with open("./data/stage_table.json", encoding="utf-8") as f:
            stagesdata = json.load(f)
            stages = stagesdata["stages"]
            for key, stage_value in stages.items():
                if stage_value["code"].lower() == stage_code.lower():
                    return stage_value["name"]
        return None
    stage_name = get_stage_name(stage)
    if stage_name is None:
        await ctx.respond("Stage not found")
        return
    try:
        payload = {
            "operation": stage.upper(),
            "cn_name": stage_name
        }
    except UnboundLocalError:
        await ctx.respond("Stage not found")
        return
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    async with aiohttp.CLientSession() as session:
        async with session.post(arkrec_url, json=payload, headers=headers) as response:
            data = await response.json()

    def load_json_file(filename: str) -> dict:
        with open(filename, encoding="utf-8") as f:
            return json.load(f)
    operators = load_json_file("./data/ops_names.json")["Operators"]
    categories = load_json_file("./data/categories.json")["Categories"]

    clear_found = []
    for i in data:
        try:
            operationType = i["operationType"]
        except KeyError:
            operationType = None
            if mode == "challenge":
                await ctx.respond("This stage does not have CM")
                break
        else:
            pass
        category = i["category"]
        categories_en = []
        for x in category:
            for key, value in categories.items():
                if key == x:
                    en_name = value
                    categories_en.append(en_name)
        if (categoryy.title() in categories_en) and (operationType == mode or mode == None):
            clear_found.append(True)
            stage = i["operation"]
            clear_link = i["url"]
            ops_count = len(i["team"])
            ops = i["team"]
            raider = i["raider"]
            date = i["date_published"][:10]
            ops_en_ver = []
            for i in ops:
                if i in ["黑角", "夜刀", "巡林者", "杜林"]:
                    for key, value in operators.items():
                        if value == i:
                            en_name = key
                            ops_en_ver.append(f"{en_name}")
                elif i in ["Lancet-2", "Castle-3", "THRM-EX"]:
                    ops_en_ver.append(i)
                elif i == "正义骑士号":
                    ops_en_ver.append("Justice Knight")
                else:
                    skill = i[-1]
                    cn_name = i.rstrip(i[-1])
                    for key, value in operators.items():
                        if value == cn_name:
                            en_name = key
                            ops_en_ver.append(f"{en_name} S{skill}")
            sep = ", "
            embed = hikari.Embed(title="Clear Found")
            embed.add_field("Stage", stage, inline=True)
            adverse_stages = {"10-7", "10-11", "10-15", "10-17",
                            "11-3", "11-8", "11-12", "11-15",
                            "11-20", "12-7", "12-13", "12-19", "12-20"}

            if stage in adverse_stages:
                if operationType == "challenge":
                    stage_url = f"https://prts.wiki/w/文件:磨难{stage.upper()}_{stage_name}_地图.png"
                else:
                    stage_url = f"https://prts.wiki/w/文件:{stage.upper()}_{stage_name}_地图.png"
            else:
                stage_url = f"https://prts.wiki/w/文件:{stage.upper()}_{stage_name}_地图.png"

            stage_thumbnail_url = None
            found_thumbnail_url = False
            async with session.get(stage_url) as stage_resp:
                stage_html = await stage_resp.text()
                stage_soup = BeautifulSoup(stage_html, 'html.parser')
                urls = stage_soup.find_all('a')
                for url in urls:
                    url = url.get('href')
                    if url and re.match(
                            r'(?:([^:/?#]+):)?(?://([^/?#]*))?([^?#]*\.(?:jpg|gif|png))(?:\?([^#]*))?(?:#(.*))?'
                            , url):
                        if "800px" in url:
                            stage_thumbnail_url = url
                            found_thumbnail_url = True
                            break
                if not found_thumbnail_url:
                    stage_thumbnail_url = None
            if operationType == "challenge":
                embed.add_field("CM", "✅", inline=True)
            elif operationType == "normal":
                embed.add_field("CM", "❌", inline=True)
            else:
                pass
            embed.add_field("Player", raider, inline=True)
            embed.add_field("Category(s)", sep.join(map(str, categories_en)), inline=True)
            embed.add_field("Operator Count", ops_count, inline=True)
            embed.add_field("Squad", sep.join(map(str, ops_en_ver)), inline=True)
            embed.add_field("Date", date, inline=True)
            embed.add_field("Link", clear_link, inline=True)
            embed.set_image(stage_thumbnail_url)
            await ctx.respond(embed)
            break
        else:
            clear_found.append(False)
    if True not in clear_found:
        await ctx.respond("Couldn't find a clear", flags=hikari.MessageFlag.EPHEMERAL)

@arkrec.autocomplete("category")
async def arkrec_autocomplete(
    opt: hikari.AutocompleteInteractionOption, inter: hikari.AutocompleteInteraction
    ) -> Union[str, Sequence[str], hikari.CommandChoice, Sequence[hikari.CommandChoice]]:
    user_input = opt.value
    with open("./data/categories.json", encoding="utf-8") as g:
        categoriesdata = json.load(g)
        Categories = categoriesdata["Categories"]  
        categories_en = []
        for _, value in Categories.items():
            en_name = value.lower()
            categories_en.append(en_name)
    close_matches = get_close_matches(user_input, categories_en, cutoff=0.1)
    return close_matches

@plugin.command
@lightbulb.command('categories', 'Lists all arkrec categories')
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def categories(ctx):
    with open("./data/categories.json", encoding="utf-8") as f:
        categoriesdata = json.load(f)
        categories = categoriesdata["Categories"]

    embed = hikari.Embed()
    embed.add_field("Categories:", "\n".join([f"• {v}" for v in categories.values()]))
    await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)


def load(bot):
    bot.add_plugin(plugin)
