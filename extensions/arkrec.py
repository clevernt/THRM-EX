from typing import Union
from typing import Sequence
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
@lightbulb.option('challenge_mode', 'Challenge Mode', choices="True, False", required=True)
@lightbulb.option('category', 'Category', required=True, autocomplete=True)
@lightbulb.option('stage', 'Stage Name', required=True)
@lightbulb.command('arkrec', 'finds clears from arkrec', auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def arkrec(ctx):
    arkrec_url = "https://arkrec.com/api/records"
    stage = ctx.options.stage.strip()
    categoryy = ctx.options.category.strip()
    challenge_mode = ctx.options.challenge_mode
    with open("./data/stage_table.json", encoding="utf-8") as f:
        stagesdata = json.load(f)
        stages = stagesdata["stages"]
        for i in stages.items():
            if i[1]["code"].lower() == stage.lower():
                stage_name = i[1]["name"]
    try:
        payload = {
            "operation": stage.upper(),
            "cn_name": stage_name
        }
    except UnboundLocalError:
        await ctx.respond(f"{ctx.author.mention} Are you sure that is a stage?")
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    response = requests.request("POST", arkrec_url, json=payload, headers=headers)
    data = response.json()
    stage_url = f"https://prts.wiki/w/文件:{stage.upper()}_{stage_name}_地图.png"
    resp = session.get(stage_url)
    urls = resp.html.absolute_links
    for url in urls:
        if re.match(r'(?:([^:/?#]+):)?(?://([^/?#]*))?([^?#]*\.(?:jpg|gif|png))(?:\?([^#]*))?(?:#(.*))?', url):
            if "800px" in url:
                stage_thumbnail_url = url
        else:
            pass
    with open("./data/ops_names.json", encoding="utf-8") as c:
        opsdata = json.load(c)
        Ops = opsdata["Operators"]

    with open("./data/categories.json", encoding="utf-8") as g:
        categoriesdata = json.load(g)
        Categories = categoriesdata["Categories"]

    clear_found = []
    for i in data: 
        category = i["category"]
        categories_en = []
        for x in category:
            for key, value in Categories.items():
                if key == x:
                    en_name = value
                    categories_en.append(en_name)
        if categoryy.title() in categories_en:
            stage = i["operation"]
            clear_link = i["url"]
            ops_count = len(i["team"])
            ops = i["team"]
            raider = i["raider"]
            ops_en_ver = []
            for i in ops:
                skill = i[-1]
                cn_name = i.rstrip(i[-1])
                for key, value in Ops.items():
                    if value == cn_name:
                        en_name = key
                        ops_en_ver.append(f"{en_name} S{skill}")
            sep = ", "
            # await ctx.respond(f"Stage: {stage}, Category(s): {sep.join(map(str, categories_en))}, Lowest ops: {ops_count}, Squad: {sep.join(map(str, ops_en_ver))} Link: {clear_link}")
            embed = hikari.Embed(title="Clear Found")
            embed.add_field("Stage", stage, inline=True)
            embed.add_field("Player", raider, inline=True)
            embed.add_field("Category(s)", sep.join(map(str, categories_en)), inline=True)
            embed.add_field("OP Count", ops_count, inline=True)
            embed.add_field("Squad", sep.join(map(str, ops_en_ver)), inline=True)
            embed.add_field("Link", clear_link, inline=True)
            embed.set_image(stage_thumbnail_url)
            if challenge_mode != None:
                try: 
                    operationType = i["operationType"]
                except KeyError:
                    await ctx.respond("This stage does not have challenge mode.")
                else:
                    if challenge_mode == "True" and operationType == "challenge":
                        embed.add_field("Challenge Mode?", "✔", inline=True)
                        await ctx.respond(embed)
                        break
                    elif challenge_mode == "False" and operationType == "normal":
                        embed.add_field("Challenge Mode?", "❌", inline=True)                        
                        await ctx.respond(embed)
                        break
            else:
                await ctx.respond(embed)
                break
        else:
            clear_found.append(False)
    if True not in clear_found:
        await ctx.respond(f"{ctx.author.mention} Couldn't find a clear.")

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
@lightbulb.implements(lightbulb.SlashCommand)
async def categories(ctx):
    embed = hikari.Embed()
    embed.add_field("Categories:", "Regular Squad\n No Ling S3\n E2 Lv1\n E1 Max Lv\n E1 Lv1\n E0 Max Level\n E0 Lv1\n Five Star Only\n E2 Lv1 Five Star Only\n Four Star Only\n E1 Max Level Four Star Only\n E1 Lv1 Four Star Only\n Three Star Only\n Two Star Only\n Vanguard Only\n Guard Only\n Sniper Only\n Defender Only\n Medic Only\n Supporter Only\n Caster Only\n Specialist Only\n Low Step\n 1P Relay\n 1 Tile Only\n Welfare Only\n No Normal Attack Operators\n Abyssal Hunters Only\n Liberi Only\n Vulpo Only\n Enmity Only\n Karlan Commercial Only\n Male Only\n Supporters Without Summoners\n Knights Only\n Feline Only\n Bears Only")
    await ctx.respond(embed)


def load(bot):
    bot.add_plugin(plugin)
