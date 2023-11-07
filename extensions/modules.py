import lightbulb
import hikari
import json

from difflib import get_close_matches
from typing import Sequence, Union
from lightbulb.utils import pag, nav

bot = lightbulb.BotApp
plugin = lightbulb.Plugin("modules")

range_mods = {
    "SPC-X": "https://uwu.so/neuvium/new5soyo92",
    "RIN-X": "https://uwu.so/neuvium/nesDf7uFTC"
}

operators_with_modules = set()
with open("./data/modules.json", "r") as f:
    data = json.load(f)
    for operator in data:
        operators_with_modules.add(operator.lower())

def get_modules(operator_name):
    modules_list = []
    with open("./data/modules.json") as f:
        modules_data = json.load(f)
        for operator, modules in modules_data.items():
            if operator.lower() == operator_name.lower():
                modules_list.extend(modules)
    return modules_list   

def get_branch_trait(branch_code):
    with open("./data/branches.json") as f:
        branches_data = json.load(f)

        return branches_data[branch_code.upper()]

def get_branch_icon(branch_code):
    branch_icon_url = f"https://raw.githubusercontent.com/Aceship/Arknight-Images/main/equip/type/{branch_code}.png"

    return branch_icon_url

def get_operator_avatar(operator):
    with open("./data/operators.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for operator_name, operator_data in data.items():
            if operator_name.lower() == operator.lower():
                operator_id = operator_data["id"]
        
    avatar_url = f"https://raw.githubusercontent.com/Aceship/Arknight-Images/main/avatars/{operator_id}.png"
    return avatar_url

@plugin.command
@lightbulb.option("operator", "Operator", required=True, autocomplete=True)
@lightbulb.command("module", "Get details about an operator's module", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
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
    embeds = []
    for module in modules_list:
        trait_upgrade = get_branch_trait(module["module_branch"])

        embed = hikari.Embed(title=requested_operator.title(), description=trait_upgrade, color=16448250)
        embed.set_author(name=module["module_branch"], icon=f"https://raw.githubusercontent.com/Aceship/Arknight-Images/main/equip/type/{module['module_branch'].lower()}.png")

        if module["base_talent"] != "N/A":
            embed.add_field("Base Talent", module["base_talent"])
            embed.add_field("Stage 2 - Talent Upgrade", module["stage_2_talent_upgrade"])
            embed.add_field("Stage 3 - Talent Upgrade", module["stage_3_talent_upgrade"])
        else:
            embed.add_field("Stage 2 - New Talent", module["stage_2_talent_upgrade"])
            embed.add_field("Stage 3 - Talent Upgrade", module["stage_3_talent_upgrade"])

        embed.set_thumbnail(avatar_url)

        if module["module_branch"] in range_mods:
            embed.add_field(module["total_stat_buffs"], "New Attack Range:")
            embed.set_image(range_mods[module["module_branch"]])
        elif requested_operator.lower() == "tomimi":
            embed.add_field(module["total_stat_buffs"], "New Attack Range:")
            embed.set_image("https://uwu.so/neuvium/neyKuxn8jH")
        else:
            embed.add_field(module["total_stat_buffs"], "\u200b")

        embed.set_footer("DM @neuvium for any errors/feedback")
        embeds.append(embed)

        paginator.add_line(embed)
    navigator = nav.ButtonNavigator(embeds)
    await navigator.run(ctx)
    


@module.autocomplete("operator")
async def module_autocomplete(
    opt: hikari.AutocompleteInteractionOption, inter: hikari.AutocompleteInteraction
) -> Union[str, Sequence[hikari.CommandChoice]]:
    user_input = opt.value.lower()
    matching_operators = [operator for operator in operators_with_modules if user_input in operator.lower()]
    matching_operators = matching_operators[:25]
    return [hikari.CommandChoice(name=operator, value=operator) for operator in matching_operators]

def load(bot):
    bot.add_plugin(plugin)
