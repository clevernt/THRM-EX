import lightbulb
import hikari
import requests
import pytz

from typing import Union
from typing import Sequence
from lightbulb.utils import nav
from dateutil import parser

from utils import *

plugin = lightbulb.Plugin("arkrec")


@plugin.command
@lightbulb.option("category", "Category", required=True, autocomplete=True)
@lightbulb.option(
    "mode",
    "Mode",
    choices=["Normal Mode", "Challenge Mode"],
    required=False,
    default=None,
)
@lightbulb.option("stage", "Stage Name", required=True)
@lightbulb.command("arkrec", "Finds clears from arkrec", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def arkrec(ctx):
    requested_stage = ctx.options["stage"]
    requested_category = ctx.options["category"]
    mode = mode_mapping.get(ctx.options["mode"], None)

    stage_name = None
    for _, value in stage_table.items():
        if value["code"].lower() == requested_stage.lower():
            stage_name = value["name"]
            break

    if stage_name is not None:
        payload = {"operation": requested_stage.upper(), "cn_name": stage_name}
    else:
        await ctx.respond(
            hikari.Embed(
                description=f"Stage `{requested_stage}` was not found",
                color=EMBED_COLOR,
            )
        )
        return

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
    }

    try:
        response = requests.request(
            "POST", ARKREC_URL, json=payload, headers=headers, timeout=30
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        await ctx.respond(
            hikari.Embed(description=f"Request error: {e}", color=EMBED_COLOR)
        )
        return

    data = response.json()
    clear_found = []
    embeds = []

    for i in data:
        operation_type = i["operationType"]
        categories_cn = i["category"]
        categories_en = [categories.get(category) for category in categories_cn]

        if (requested_category.title() in categories_en) and (
            mode in (operation_type, None)
        ):
            clear_found.append(True)
            raider_image = i["raiderImage"]
            stage_code = i["operation"]
            clear_link = i["url"]
            operator_count = len(i["team"])
            operators_list = i["team"]
            raider = i["raider"]
            date_published = i["date_published"]
            stage_page = f"https://en.arkrec.com/operation/{stage_code}+{stage_name}"
            parsed_timestamp = parser.isoparse(date_published).astimezone(pytz.UTC)
            operators_list_en = filter_and_translate(operators_list, operator_names)
            sep = ", "
            embed = hikari.Embed(
                title=f"{stage_code} | {'Challenge Mode' if operation_type == 'challenge' else 'Normal Mode'}",
                description=sep.join(map(str, categories_en)),
                timestamp=parsed_timestamp,
                url=stage_page,
                color=EMBED_COLOR,
            )
            embed.set_author(name=raider, icon=raider_image)
            embed.add_field(
                f"Squad - {operator_count} Operators",
                sep.join(map(str, operators_list_en)),
                inline=True,
            )
            embed.add_field("Clear Link", clear_link)
            embeds.append(embed)

        else:
            clear_found.append(False)

    if True not in clear_found:
        await ctx.respond(
            hikari.Embed(
                description=f"No clears found matching the following parameters:\nStage: `{requested_stage} {mode if mode else ''}`\nCategory: `{requested_category}`",
                color=EMBED_COLOR,
            )
        )
        return

    if len(embeds) > 0:
        navigator = nav.ButtonNavigator(embeds)
        await navigator.run(ctx)


@arkrec.autocomplete("category")
async def arkrec_autocomplete(
    opt: hikari.AutocompleteInteractionOption, inter: hikari.AutocompleteInteraction
) -> Union[str, Sequence[hikari.CommandChoice]]:
    user_input = opt.value.lower()
    matching_categories = [
        category for category in categories_en if user_input in category.lower()
    ]
    matching_categories = matching_categories[:25]
    return [
        hikari.CommandChoice(name=category.title(), value=category.title())
        for category in matching_categories
    ]


def load(bot):
    bot.add_plugin(plugin)
