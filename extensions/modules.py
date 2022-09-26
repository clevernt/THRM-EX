from difflib import get_close_matches
from typing import Sequence, Union
from lightbulb.utils.pag import EmbedPaginator
import lightbulb
import hikari
import json

plugin = lightbulb.Plugin('modules')

@plugin.command
@lightbulb.option('operator', 'Operator', required=True, autocomplete=True)
@lightbulb.command('module', "Get details about an operator's module")
@lightbulb.implements(lightbulb.SlashCommand)
async def module(ctx):
    await ctx.respond(hikari.ResponseType.DEFERRED_MESSAGE_CREATE)
    operator = ctx.options.operator.strip()
    with open("./data/modules.json", "r") as f:
        ops_with_modules = []
        data = json.load(f)
        for i in data:
            op_name = i["operator"]
            ops_with_modules.append(op_name.lower())
        if operator.lower() not in ops_with_modules:
            await ctx.respond(hikari.Embed(title="Operator doesn't have a module"))
        for i in data:
            name = i["operator"]
            with open("./data/operator_name_to_id.json", "r") as c:
                    data = json.load(c)
                    for key, value in data.items():
                        if key == name:
                            operator_code = value 
                            operator_icon = f"https://raw.githubusercontent.com/Aceship/Arknight-Images/main/avatars/{operator_code}.png"
            if name.lower() == operator.lower():       
                module_branch = i["module_branch"]
                stage_1_trait_upgrade = i["stage_1_trait_upgrade"]
                base_talent = i["base_talent"]
                stage_2_talent_upgrade = i["stage_2_talent_upgrade"]
                stage_3_talent_upgrade = i["stage_3_talent_upgrade"]
                total_stat_buffs = i["total_stat_buffs"]
                embed = hikari.Embed(title=name)
                embed.add_field("Module Branch", module_branch)
                embed.add_field("Stage 1 | Trait Upgrade", stage_1_trait_upgrade)
                if base_talent != "N/A":
                    embed.add_field("Base Talent (Talent Upgrade Pot included if applicable)", base_talent)
                    embed.add_field("Stage 2 | Talent Upgrade (Talent Upgrade Pot not included)", stage_2_talent_upgrade)
                    embed.add_field("Stage 3 | Talent Upgrade (Talent Upgrade Pot not included)", stage_3_talent_upgrade)
                elif base_talent == "N/A":
                    embed.add_field("Stage 2 | New Talent", stage_2_talent_upgrade)
                    embed.add_field("Stage 3 | Talent Upgrade", stage_3_talent_upgrade)
                embed.add_field("Total Stat Buffs", total_stat_buffs)
                embed.add_field("Modules Sheet", "https://bit.ly/AKModules")
                embed.set_footer("Copypasting from Modules Sheet by CleverShadow#5250")
                embed.set_thumbnail(operator_icon)
                if module_branch == "SPC-X":
                    embed.add_field("Increased Attack Range:", "See below")
                    embed.set_image("https://i.imgur.com/aQUIiMu.png")
                if module_branch == "RIN-X": 
                    embed.add_field("Increased Attack Range:", "See below")
                    embed.set_image("https://i.imgur.com/x8bMsT8.png")
                await ctx.respond(embed)
               
@module.autocomplete("operator")
async def module_autocomplete(
    opt: hikari.AutocompleteInteractionOption, inter: hikari.AutocompleteInteraction
    ) -> Union[str, Sequence[str], hikari.CommandChoice, Sequence[hikari.CommandChoice]]:
    user_input = opt.value
    operators_list = []
    with open("./data/operator_name_to_id.json", "r") as d:
        ops = json.load(d)
        for key, _ in ops.items():
            operator_name = key
            operators_list.append(operator_name.lower())
    close_matches = get_close_matches(user_input, operators_list, cutoff=0.3)
    return close_matches

def load(bot):
    bot.add_plugin(plugin)