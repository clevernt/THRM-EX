from typing import Union, Sequence
from typing import Optional
from difflib import get_close_matches
from requests_html import HTMLSession
import re
import lightbulb
import hikari
import requests
import json

session = HTMLSession()
plugin = lightbulb.Plugin('arkrec')

STAGE_TABLE_PATH = "./data/stage_table.json"
OPS_NAMES_PATH = "./data/ops_names.json"
CATEGORIES_PATH = "./data/categories.json"


def load_json(file_path):
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)


def create_embed(title, fields, thumbnail_url=None):
    embed = hikari.Embed(title=title)
    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)
    if thumbnail_url:
        embed.set_image(url=thumbnail_url)
    return embed


def find_image_url(urls):
    for url in urls:
        if re.match(r'(?:([^:/?#]+):)?(?://([^/?#]*))?([^?#]*\.(?:jpg|gif|png))(?:\?([^#]*))?(?:#(.*))?', url):
            if "800px" in url:
                return url
    return None


@plugin.command
@lightbulb.option('category', 'Category', required=True, autocomplete=True)
@lightbulb.option('mode', "Mode", choices=["Normal Mode", "Challenge Mode"], required=False, default=None)
@lightbulb.option('stage', 'Stage Name', required=True)
@lightbulb.command('arkrec', 'finds clears from arkrec', auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def arkrec(ctx):
    stages_data = load_json(STAGE_TABLE_PATH)
    ops_data = load_json(OPS_NAMES_PATH)
    categories_data = load_json(CATEGORIES_PATH)

    arkrec_url = "https://arkrec.com/api/records"
    stage = ctx.options.stage.strip()
    category = ctx.options.category.strip()
    mode = ctx.options.mode.strip() if ctx.options.mode else None

    stage_value = stages_data["stages"].get(stage.lower())
    if not stage_value:
        await ctx.respond(f"{ctx.author.mention} Are you sure that's a valid stage?")
        return

    stage_name = stage_value["name"]
    operation_type = stage_value.get("operationType")

    payload = {
        "operation": stage.upper(),
        "cn_name": stage_name
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    response = requests.request(
        "POST", arkrec_url, json=payload, headers=headers)
    data = response.json()

    categories_en = [value.lower()
                     for value in categories_data["Categories"].values()]

    found_clear = False
    for clear_data in data:
        try:
            operation_type = clear_data["operationType"]
        except KeyError:
            operation_type = None
            if mode == "challenge":
                await ctx.respond(f"{ctx.author.mention} This stage does not have CM.")
                break

        if (category in categories_en) and (operation_type == mode or not mode):
            found_clear = True
            stage = clear_data["operation"]
            clear_link = clear_data["url"]
            ops_count = len(clear_data["team"])
            ops = clear_data["team"]
            raider = clear_data["raider"]
            date = clear_data["date_published"][:10]
            ops_en_ver = []

            for op in ops:
                if op in ops_data["Operators"]:
                    ops_en_ver.append(ops_data["Operators"][op])
                elif op in ["Lancet-2", "Castle-3", "THRM-EX"]:
                    ops_en_ver.append(op)
                elif op == "正义骑士号":
                    ops_en_ver.append("Justice Knight")
                else:
                    skill = op[-1]
                    cn_name = op.rstrip(skill)
                    if cn_name in ops_data["Operators"]:
                        ops_en_ver.append(
                            f"{ops_data['Operators'][cn_name]} S{skill}")

            sep = ", "

            adverse_stages = {"10-7", "10-11", "10-15", "10-17",
                              "11-3", "11-8", "11-12", "11-15",
                              "11-20", "12-7", "12-13", "12-19", "12-20"}

            if stage in adverse_stages:
                stage_url = f"https://prts.wiki/w/文件:磨难{stage.upper()}_{stage_name}_地图.png" if operation_type == "challenge" else f"https://prts.wiki/w/文件:{stage.upper()}_{stage_name}_地图.png"
            else:
                stage_url = f"https://prts.wiki/w/文件:{stage.upper()}_{stage_name}_地图.png"

            resp = session.get(stage_url)
            urls = resp.html.absolute_links
            stage_thumbnail_url = find_image_url(urls)

            cm_field = "✅" if operation_type == "challenge" else "❌"

            fields = [
                ("Stage", stage, True),
                ("CM", cm_field, True),
                ("Player", raider, True),
                ("Category(s)", sep.join(map(str, categories_en)), True),
                ("Operator Count", ops_count, True),
                ("Squad", sep.join(map(str, ops_en_ver)), True),
                ("Date", date, True),
                ("Link", clear_link, True)
            ]

            embed = create_embed("Clear Found", fields, stage_thumbnail_url)
            await ctx.respond(embed=embed)
            break

    if not found_clear:
        await ctx.respond(f"{ctx.author.mention} Couldn't find a clear", flags=hikari.MessageFlag.EPHEMERAL)


@arkrec.autocomplete("category")
async def arkrec_autocomplete(
    opt: hikari.AutocompleteInteractionOption, inter: hikari.AutocompleteInteraction
) -> Union[str, Sequence[str], hikari.CommandChoice, Sequence[hikari.CommandChoice]]:
    user_input = opt.value
    categories_data = load_json(CATEGORIES_PATH)
    categories_en = [value.lower()
                     for value in categories_data["Categories"].values()]
    close_matches = get_close_matches(user_input, categories_en, cutoff=0.1)
    return close_matches


@plugin.command
@lightbulb.command('categories', 'Lists all arkrec categories')
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def categories(ctx):
    categories_data = load_json(CATEGORIES_PATH)
    categories = categories_data["Categories"]

    embed = hikari.Embed()
    embed.add_field("Categories:", "\n".join(
        [f"• {v}" for v in categories.values()]))
    await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)


def load(bot):
    bot.add_plugin(plugin)
