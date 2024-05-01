from typing import Union, Sequence

import requests
import pytz
import hikari
import lightbulb

from dateutil import parser
from lightbulb.utils import nav
from utils.data import (
    EMBED_COLOR,
    ARKREC_URL,
    categories,
    operators_chinese_names,
    categories_en,
)
from utils.operators_list import filter_and_translate

plugin = lightbulb.Plugin("arkrec")

stage_table = requests.get(
    "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/stage_table.json"
).json()["stages"]


@plugin.command()
@lightbulb.option("category", "Category", required=True, autocomplete=True)
@lightbulb.option(
    "mode",
    "Mode",
    choices=["normal", "challenge"],
    required=False,
    default=None,
)
@lightbulb.option("stage", "Stage Name", required=True)
@lightbulb.command("arkrec", "Finds clears from arkrec", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def arkrec(ctx):
    category = ctx.options.category
    stage = ctx.options.stage
    mode = ctx.options.mode

    stage_name = next(
        (
            value["name"]
            for value in stage_table.values()
            if value["code"].lower() == stage.lower()
        ),
        None,
    )

    if not stage_name:
        return await ctx.respond(
            hikari.Embed(description=f"Stage {stage} not found.", color=EMBED_COLOR)
        )

    payload = {"operation": stage.upper(), "cn_name": stage_name}
    headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}

    try:
        response = requests.post(ARKREC_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        return await ctx.respond(
            hikari.Embed(description=f"Request error: ```{e}```", color=EMBED_COLOR)
        )

    data = response.json()
    embeds = []

    for i in data:
        operation_type = i["operationType"]
        categories_cn = i["category"]
        categories_en = [categories.get(category) for category in categories_cn]

        if (category.title() in categories_en) and (mode in (operation_type, None)):
            raider_image = i["raiderImage"]
            stage_code = i["operation"]
            clear_link = i["url"]
            operator_count = len(i["team"])
            operators_list = i["team"]
            raider = i["raider"]
            date_published = parser.isoparse(i["date_published"]).astimezone(pytz.UTC)
            operators_list_en = filter_and_translate(
                operators_list, operators_chinese_names
            )
            embed = hikari.Embed(
                title=f"{stage_code} | {'Challenge Mode' if operation_type == 'challenge' else 'Normal Mode'}",
                description=", ".join(map(str, categories_en)),
                timestamp=date_published,
                url=f"https://en.arkrec.com/operation/{stage_code}+{stage_name}",
                color=EMBED_COLOR,
            )
            embed.set_author(name=raider, icon=raider_image)
            embed.add_field(
                f"Squad - {operator_count} Operators",
                ", ".join(map(str, operators_list_en)),
                inline=True,
            )
            embed.add_field("Clear Link", clear_link)
            embeds.append(embed)

    if not embeds:
        return await ctx.respond(
            hikari.Embed(
                description=f"No clears found matching the parameters:\nStage: `{stage} {mode if mode else ''}`\nCategory: `{category}`",
                color=EMBED_COLOR,
            )
        )

    navigator = nav.ButtonNavigator(embeds)
    await navigator.run(ctx)


@arkrec.autocomplete("category")
async def arkrec_autocomplete(
    opt: hikari.AutocompleteInteractionOption, inter: hikari.AutocompleteInteraction
) -> Union[str, Sequence[hikari.CommandChoice]]:
    user_input = opt.value.lower()
    matching_categories = [
        category for category in categories_en if user_input in category.lower()
    ][:25]
    return [
        hikari.CommandChoice(name=category.title(), value=category.title())
        for category in matching_categories
    ]


def load(bot):
    bot.add_plugin(plugin)
