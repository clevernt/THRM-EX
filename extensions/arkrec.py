import lightbulb
import hikari
import requests
import json
import re

from typing import Union
from typing import Sequence
from difflib import get_close_matches
from requests_html import HTMLSession

session = HTMLSession()
plugin = lightbulb.Plugin("arkrec")

ARKREC_URL = "https://arkrec.com/api/records"

mode_mapping = {"Normal Mode": "normal", "Challenge Mode": "challenge"}
adverse_stages = {
    "10-7",
    "10-11",
    "10-15",
    "10-17",
    "11-3",
    "11-8",
    "11-12",
    "11-15",
    "11-20",
    "12-7",
    "12-13",
    "12-19",
    "12-20",
}
skilless_operators = [
    "Friston-3",
    "U-Official",
    "THRM-EX",
    "泰拉大陆调查团",
    "Lancet-2",
    "Castle-3",
    "正义骑士号",
]

with open("./data/stage_table.json", encoding="utf-8") as f:
    stage_table = json.load(f)["stages"]
with open("./data/operator_names.json", encoding="utf-8") as f:
    operator_names = json.load(f)
with open("./data/categories.json", encoding="utf-8") as f:
    categories = json.load(f)


def filter_and_translate(operators_list, operator_names):
    operators_list_en = []
    for operator in operators_list:
        if operator in skilless_operators:
            operators_list_en.append(operator_names[operator])
        else:
            skill = operator[-1]
            name_cn = operator.rstrip(skill)
            name_en = operator_names[name_cn]
            operators_list_en.append(f"{name_en} S{skill}")
    return operators_list_en


@plugin.command
@lightbulb.option(
    "category", 
    "Category",
    required=True, 
    autocomplete=True
)
@lightbulb.option(
    "mode",
    "Mode",
    choices=["Normal Mode", "Challenge Mode"],
    required=False,
    default=None,
)
@lightbulb.option(
    "stage", 
    "Stage Name", 
    required=True
)
@lightbulb.command(
    "arkrec", 
    "finds clears from arkrec", 
    auto_defer=True
)
@lightbulb.implements(lightbulb.SlashCommand)
async def arkrec(ctx):
    requested_stage = ctx.options.stage.strip()
    requested_category = ctx.options.category.strip()
    if ctx.options.mode.strip() is not None:
        mode_mapping.get(mode)
    else:
        mode = None

    for _, value in stage_table.items():
        if value["code"].lower() == requested_stage.lower():
            stage_name = value["name"]
            break

    if stage_name is not None:
        payload = {"operation": requested_stage.upper(), "cn_name": stage_name}
    else:
        await ctx.respond(
            hikari.Embed(description=f"Stage `{requested_stage}` was not found")
        )

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
    }

    try:
        response = requests.request("POST", ARKREC_URL, json=payload, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        await ctx.respond(hikari.Embed(description=f"Request error: {e}"))
        return  
    data = response.json()
    clear_found = []
    for i in data:
        try:
            operationType = i["operationType"]
        except KeyError:
            operationType = None
            if mode == "challenge":
                await ctx.respond(
                    hikari.Embed(
                        description=f"`{requested_stage}` does not have Challenge Mode"
                    )
                )
                break
        else:
            pass

        categories_cn = i["category"]
        categories_en = [categories.get(category) for category in categories_cn]

        if (
            requested_category.title() in categories_en
            and operationType == mode
            or mode == None
        ):
            clear_found.append(True)
            stage_code = i["operation"]
            clear_link = i["url"]
            operator_count = len(i["team"])
            operators_list = i["team"]
            raider = i["raider"]
            date_published = i["date_published"][:10]
            operators_list_en = filter_and_translate(operators_list, operator_names)

            sep = ", "
            embed = hikari.Embed(title="Clear Found")
            embed.add_field("Stage", stage_code, inline=True)


            if operationType == "challenge":
                embed.add_field("CM", "✅", inline=True)
            elif operationType == "normal":
                embed.add_field("CM", "❌", inline=True)
            else:
                pass

            embed.add_field("Player", raider, inline=True)
            embed.add_field(
                "Category(s)", sep.join(map(str, categories_en)), inline=True
            )
            embed.add_field("Operator Count", operator_count, inline=True)
            embed.add_field("Squad", sep.join(map(str, operators_list_en)), inline=True)
            embed.add_field("Date Published", date_published, inline=True)
            embed.add_field("Link", clear_link, inline=True)
            await ctx.respond(embed)
            break
        else:
            clear_found.append(False)
    if True not in clear_found:
        await ctx.respond(
            hikari.Embed(
                description=f"No clear found matching the following input:\nStage: `{requested_stage}\nCategory: `{requested_category}`"
            )
        )


@arkrec.autocomplete("category")
async def arkrec_autocomplete(
    opt: hikari.AutocompleteInteractionOption, inter: hikari.AutocompleteInteraction
) -> Union[str, Sequence[str], hikari.CommandChoice, Sequence[hikari.CommandChoice]]:
    user_input = opt.value
    categories_en = []
    for _, value in categories.items():
        en_name = value.lower()
        categories_en.append(en_name)
    close_matches = get_close_matches(user_input, categories_en, cutoff=0.1)
    return close_matches

def load(bot):
    bot.add_plugin(plugin)
