import hikari
import lightbulb
import json
bot = lightbulb.BotApp
plugin = lightbulb.Plugin('modulesbeta')

with open("operator_data.json", "r", encoding="utf-8") as f:
    operator_data = json.load(f)

OPERATORS = {operator["operator"].lower(
): operator for operator in operator_data}


def create_embed(module_data):
    embed = hikari.Embed(title="Module Data", color=0x00ff00)
    embed.add_field("Module Branch", module_data["module_branch"], inline=True)
    embed.add_field("Stage 1 Trait Upgrade",
                    module_data["stage_1_trait_upgrade"], inline=True)
    embed.add_field("Base Talent", module_data["base_talent"], inline=True)
    embed.add_field("Stage 2 Talent Upgrade",
                    module_data["stage_2_talent_upgrade"], inline=True)
    embed.add_field("Stage 3 Talent Upgrade",
                    module_data["stage_3_talent_upgrade"], inline=True)
    embed.add_field("Total Stat Buffs",
                    module_data["total_stat_buffs"], inline=True)
    return embed


@plugin.command
@lightbulb.option('operator', 'Operator', required=True, autocomplete=True)
@lightbulb.command('modulebeta', "Get details about an operator's module", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def modulebeta(ctx):
    operator_name = ctx.options.operator.strip()
    if operator_name not in OPERATORS:
        await ctx.respond("Operator not found.")
        return
    operator_data = OPERATORS[operator_name]
    module_names = [module_data["module_branch"]
                    for module_data in operator_data]
    module_options = [hikari.SelectOption(
        module_name, module_name) for module_name in module_names]
    components = [hikari.SelectMenu(
        "module_select", "Select the module to display", options=module_options)]
    message = await ctx.respond(components=components)
    interaction = await message.wait_for(hikari.SelectOptionInteraction)
    module_data = [module for module in operator_data if module["module_branch"]
                   == interaction.selected_option.value][0]
    module_embed = create_embed(module_data)
    await interaction.edit_initial_response(embed=module_embed)


def load(bot):
    bot.add_plugin(plugin)
