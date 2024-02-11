import lightbulb
import hikari

from typing import Sequence, Union
from lightbulb.utils import pag, nav

from utils import *

bot = lightbulb.BotApp
plugin = lightbulb.Plugin("modules")


@plugin.command
@lightbulb.option("operator", "Operator", required=True, autocomplete=True)
@lightbulb.command("module", "Get details about an operator's module", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def module(ctx):
    paginator = pag.EmbedPaginator()
    requested_operator = ctx.options.operator.strip().lower()
    if requested_operator not in operators_with_modules:
        await ctx.respond(
            hikari.Embed(
                description=f"`{requested_operator}` is either an invalid operator or does not have a module yet"
            ),
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return
    avatar_url = get_avatar(requested_operator)
    modules_list = get_modules(requested_operator)
    embeds = []
    for module in modules_list:
        trait_upgrade = get_branch_trait(module["module_branch"])

        embed = hikari.Embed(
            title=operators_with_modules[requested_operator],
            description=trait_upgrade,
            color=EMBED_COLOR,
        )
        embed.set_author(
            name=module["module_branch"],
            icon=f"https://raw.githubusercontent.com/Aceship/Arknight-Images/main/equip/type/{module['module_branch'].lower()}.png",
        )

        if module["base_talent"] != "N/A":
            embed.add_field("Base Talent", module["base_talent"])
            embed.add_field(
                "Stage 2 - Talent Upgrade", module["stage_2_talent_upgrade"]
            )
            embed.add_field(
                "Stage 3 - Talent Upgrade", module["stage_3_talent_upgrade"]
            )
        else:
            embed.add_field("Stage 2 - New Talent", module["stage_2_talent_upgrade"])
            embed.add_field(
                "Stage 3 - Talent Upgrade", module["stage_3_talent_upgrade"]
            )

        embed.set_thumbnail(avatar_url)

        if module["module_branch"] in range_mods:
            embed.add_field(module["total_stat_buffs"], "New Attack Range:")
            embed.set_image(range_mods[module["module_branch"]])
        elif requested_operator.lower() == "tomimi":
            embed.add_field(module["total_stat_buffs"], "New Attack Range:")
            embed.set_image("https://uwu.so/neuvium/neyKuxn8jH")
        else:
            embed.add_field(module["total_stat_buffs"], "\u200b")

        embed.set_footer("DM @clevernt for any errors/feedback")
        embeds.append(embed)

        paginator.add_line(embed)
    navigator = nav.ButtonNavigator(embeds)
    await navigator.run(ctx)


@module.autocomplete("operator")
async def module_autocomplete(
    opt: hikari.AutocompleteInteractionOption, inter: hikari.AutocompleteInteraction
) -> Union[str, Sequence[hikari.CommandChoice]]:
    user_input = opt.value.lower()
    matching_operators = [
        operator
        for operator in operators_with_modules
        if user_input in operator.lower()
    ]
    matching_operators = matching_operators[:25]
    return [
        hikari.CommandChoice(name=operator, value=operator)
        for operator in matching_operators
    ]


def load(bot):
    bot.add_plugin(plugin)
