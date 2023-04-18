from difflib import get_close_matches
from typing import Sequence, Union

import lightbulb
import hikari
import json

bot = lightbulb.BotApp 
plugin = lightbulb.Plugin('modules')

async def paginate_embeds(ctx, embeds):
    """
    Paginates a list of embeds in a Discord channel.
    """

    page = 0
    total_pages = len(embeds)
    reaction_emojis = {"⬅️", "➡️"}

    def check(reaction, user):
        return user != bot.user and str(reaction.emoji) in reaction_emojis

    while True:
        current_embed = embeds[page]
        current_embed.set_footer(text=f"Page {page + 1}/{total_pages}")

        message = await ctx.respond(embed=current_embed)

        for emoji in reaction_emojis:
            await message.add_reaction(emoji)

        try:
            reaction, user = await bot.wait_for(
                "reaction_add", timeout=60.0, check=check)

            if str(reaction.emoji) == "⬅️":
                page -= 1
                if page < 0:
                    page = total_pages - 1

            if str(reaction.emoji) == "➡️":
                page += 1
                if page > total_pages - 1:
                    page = 0

            await message.remove_reaction(reaction, user)

        except TimeoutError:
            await message.clear_reactions()
            break

@plugin.command
@lightbulb.option('operator', 'Operator', required=True, autocomplete=True)
@lightbulb.command('module', "Get details about an operator's module", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand, lightbulb.PrefixCommand)
async def module(ctx):
    operator = ctx.options.operator.strip()
    with open("./data/modules.json", "r") as f:
        ops_with_modules = []
        operators_list = []
        data = json.load(f)
        for i in data:
            op_name = i["operator"]
            ops_with_modules.append(op_name.lower())
    with open("./data/operator_name_to_id.json", "r") as c:
        ops_id_data = json.load(c)
        for key, _ in ops_id_data.items():
            operators_list.append(key.lower())
        if operator.lower() not in ops_with_modules:
            if operator.lower() in operators_list:
                await ctx.respond(f"{operator.title()} does not have a module *yet*", flags=hikari.MessageFlag.EPHEMERAL)
            else:
                await ctx.respond(f"{operator.title()} is not an operator", flags=hikari.MessageFlag.EPHEMERAL) 
        embeds = []           
        for i in data:
            name = i["operator"]
            for key, value in ops_id_data.items():
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
                    embed.add_field("Base Talent", base_talent)
                    embed.add_field("Stage 2 | Talent Upgrade", stage_2_talent_upgrade)
                    embed.add_field("Stage 3 | Talent Upgrade", stage_3_talent_upgrade)
                elif base_talent == "N/A":
                    embed.add_field("Stage 2 | New Talent", stage_2_talent_upgrade)
                    embed.add_field("Stage 3 | Talent Upgrade", stage_3_talent_upgrade)
                embed.add_field("Total Stat Buffs", total_stat_buffs)
                embed.add_field("Modules Sheet", "https://bit.ly/AKModules")
                embed.set_footer("DM CleverShadow#5250 for any errors.")
                embed.set_thumbnail(operator_icon)
                if module_branch == "SPC-X":
                    embed.add_field("Increased Attack Range:", "See below")
                    embed.set_image("https://i.imgur.com/aQUIiMu.png")
                if module_branch == "RIN-X": 
                    embed.add_field("Increased Attack Range:", "See below")
                    embed.set_image("https://i.imgur.com/x8bMsT8.png")
                if name == "Tomimi":
                    embed.add_field("Slightly Reduced Attack Range:", "See below")
                    embed.set_image("https://i.imgur.com/dx7Qy8b.png")
                embeds.append(embed)
    await paginate_embeds(ctx, embeds)

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