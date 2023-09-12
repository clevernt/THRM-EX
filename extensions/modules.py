import lightbulb
import hikari
import json

from difflib import get_close_matches
from typing import Sequence, Union

bot = lightbulb.BotApp
plugin = lightbulb.Plugin('modules')

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
            if operator == operator_name.title():
                operator_id = _id
    avatar_url = f"https://raw.githubusercontent.com/Aceship/Arknight-Images/main/avatars/{operator_id}.png"
    return avatar_url

@plugin.command
@lightbulb.option(
    'operator', 
    'Operator', 
    required=True, 
    autocomplete=True
)
@lightbulb.command(
    'module', 
    "Get details about an operator's module", 
    auto_defer=True
)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def module(ctx):
    requested_operator = ctx.options.operator.strip()
    if requested_operator.lower() not in operators_with_modules:
        await ctx.respond(
            hikari.Embed(
                description=f"{requested_operator} is either an invalid operator or does not have a module yet"
                )
            )
    avatar_url = get_operator_avatar(requested_operator)
    embeds = []
    for i in data:
        operator = i["operator"]
        if requested_operator.lower() == operator.lower():
            module_branch = i["module_branch"]
            stage_1_trait_upgrade = i["stage_1_trait_upgrade"]
            base_talent = i["base_talent"]
            stage_2_talent_upgrade = i["stage_2_talent_upgrade"]
            stage_3_talent_upgrade = i["stage_3_talent_upgrade"]
            total_stat_buffs = i["total_stat_buffs"]
            embed = hikari.Embed(title=operator)
            embed.add_field("Module Branch", module_branch)
            embed.add_field("Stage 1 | Trait Upgrade", stage_1_trait_upgrade)
            if base_talent != "N/A":
                embed.add_field("Base Talent", base_talent)
                embed.add_field("Stage 2 | Talent Upgrade", stage_2_talent_upgrade)
                embed.add_field("Stage 3 | Talent Upgrade", stage_3_talent_upgrade)
            else:
                embed.add_field("Stage 2 | New Talent", stage_2_talent_upgrade)
                embed.add_field("Stage 3 | Talent Upgrade", stage_3_talent_upgrade)
            embed.add_field("Total Stat Buffs", total_stat_buffs)
            embed.add_field("Modules Sheet", "https://bit.ly/AKModules")
            embed.set_thumbnail(avatar_url)
            if module_branch == "SPC-X":
                embed.add_field("Increased Attack Range:", "See below")
                embed.set_image("https://i.imgur.com/aQUIiMu.png")
            if module_branch == "RIN-X":
                embed.add_field("Increased Attack Range:", "See below")
                embed.set_image("https://i.imgur.com/x8bMsT8.png")
            if operator == "Tomimi":
                embed.add_field("Slightly Reduced Attack Range:", "See below")
                embed.set_image("https://i.imgur.com/dx7Qy8b.png")
            embeds.append(embed)
    await ctx.respond(embeds=embeds)


@module.autocomplete("operator")
async def module_autocomplete(
    opt: hikari.AutocompleteInteractionOption, inter: hikari.AutocompleteInteraction
) -> Union[str, Sequence[str], hikari.CommandChoice, Sequence[hikari.CommandChoice]]:
    user_input = opt.value    
    close_matches = get_close_matches(user_input, operators_with_modules, cutoff=0.3)
    return close_matches

def load(bot):
    bot.add_plugin(plugin)
