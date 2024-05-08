from typing import Union, Sequence

import requests
import hikari
import lightbulb

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
stage_types = {"challenge": "Challenge Mode", "normal": "Normal Mode"}


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
    print(stage)
    stage_name = next(
        (
            value["name"]
            for value in stage_table.values()
            if value["code"].lower() == stage.lower()
        ),
        None,
    )
    print(stage_name)
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
    clears = response.json()

    embeds = []
    embed = None
    per_page = 4
    clear_count = 0
    for clear in clears:
        operation_type = clear["operationType"]
        categories_cn = clear["category"]
        categories_en = [categories.get(category) for category in categories_cn]

        if (category.title() in categories_en) and (mode in (operation_type, None)):
            stage_code = clear["operation"]
            clear_link = clear["url"]
            operator_count = len(clear["team"])
            operators_list = clear["team"]
            operators_list_en = filter_and_translate(
                operators_list, operators_chinese_names
            )

            if clear_count % per_page == 0:
                embed = hikari.Embed(
                    title=f"{stage_code} {category.title()} Clears",
                    description=f"[Arkrec Page](https://en.arkrec.com/operation/{stage_code}+{stage_name})",
                    color=EMBED_COLOR,
                )
                embeds.append(embed)

            embed.add_field(
                name=f"{stage_types.get(operation_type)} | {operator_count} Operators",
                value=f"{', '.join(operators_list_en)}\n[Video Link]({clear_link})\n",
            )

            clear_count += 1

            if clear_count % per_page == 0:
                embed = None

    if embed is not None:
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
