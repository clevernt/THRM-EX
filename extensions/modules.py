import lightbulb
import hikari
import json

from difflib import get_close_matches
from typing import Sequence, Union
from lightbulb.utils import pag, nav

bot = lightbulb.BotApp
plugin = lightbulb.Plugin("modules")

operators_with_modules = set()
with open("./data/modules.json", "r") as f:
    data = json.load(f)
    for module in data:
        operator_name = module["operator"].lower()
        operators_with_modules.add(operator_name)


def get_operator_avatar(operator_name):
    with open("./data/operator_ids.json", "r") as f:
        data = json.load(f)
        for operator, _id in data.items():
            if operator.lower() == operator_name.lower():
                operator_id = _id

    avatar_url = f"https://raw.githubusercontent.com/Aceship/Arknight-Images/main/avatars/{operator_id}.png"
    return avatar_url

def get_modules(operator_name):
    modules_list = []
    with open("./data/modules.json") as f:
        modules = json.load(f)
        for module in modules:
            if module["operator"].lower() == operator.lower():
                modules_list.append(module)

    return modules_list   

@plugin.command
@lightbulb.option("operator", "Operator", required=True, autocomplete=True)
@lightbulb.command("module", "Get details about an operator's module", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def module(ctx):
    paginator = pag.EmbedPaginator()
    requested_operator = ctx.options.operator.strip()
    if requested_operator.lower() not in operators_with_modules:
        await ctx.respond(
            hikari.Embed(
                description=f"`{requested_operator}` is either an invalid operator or does not have a module yet"
            )
        )
    avatar_url = get_operator_avatar(requested_operator)
    modules_list = get_modules(requested_operator)
    for module in modules_list:
        embed = hikari.Embed(title=module["operator"])
        embed.add_field("Module Branch", module["module_branch"])
        embed.add_field("Stage 1 | Trait Upgrade", module["stage_1_trait_upgrade"])
        if base_talent != "N/A":
            embed.add_field("Base Talent", module["base_talent"])
            embed.add_field("Stage 2 | Talent Upgrade", module["stage_2_talent_upgrade"])
            embed.add_field("Stage 3 | Talent Upgrade", module["stage_3_talent_upgrade"])
        else:
            embed.add_field("Stage 2 | New Talent", module["stage_2_talent_upgrade"])
            embed.add_field("Stage 3 | Talent Upgrade", module["stage_3_talent_upgrade"])
        embed.add_field("Total Stat Buffs", module["total_stat_buffs"])
        embed.add_field("Modules Sheet", "https://bit.ly/AKModules")
        embed.set_thumbnail(avatar_url)
        if module_branch == "SPC-X":
            embed.add_field("Increased Attack Range:", "\u200b")
            embed.set_image("https://i.postimg.cc/w75TMGX9/SPC-X.png")
        if module_branch == "RIN-X":
            embed.add_field("Increased Attack Range:", "\u200b")
            embed.set_image("https://i.postimg.cc/crGLsS8D/RIN-X.png")
        if operator == "Tomimi":
            embed.add_field("Slightly Reduced Attack Range:", "\u200b")
            embed.set_image("https://i.postimg.cc/TKR2DJ0g/Tomimi.png")
        embeds.append(embed)
        paginator.add_line(embed)
    navigator = nav.ButtonNavigator(embeds)
    await navigator.run(ctx)
    


@module.autocomplete("operator")
async def module_autocomplete(
    opt: hikari.AutocompleteInteractionOption, inter: hikari.AutocompleteInteraction
) -> Union[str, Sequence[str], hikari.CommandChoice, Sequence[hikari.CommandChoice]]:
    user_input = opt.value
    close_matches = get_close_matches(user_input, operators_with_modules, cutoff=0.3)
    return close_matches


def load(bot):
    bot.add_plugin(plugin)
