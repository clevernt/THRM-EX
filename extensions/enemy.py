import hikari
import lightbulb
import requests

from typing import Union, Sequence
from utils.data import GITHUB_REPO
from utils.enemy import *

plugin = lightbulb.Plugin("enemy")

enemy_list = requests.get(
    "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData_YoStar/main/en_US/gamedata/excel/enemy_handbook_table.json"
).json()


@plugin.command
@lightbulb.option("enemy", "Enemy's name", required=True, autocomplete=True)
@lightbulb.command("enemy", "Get an enemy's details", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def enemy(ctx):
    enemy_data = get_enemy_data(ctx.options.enemy)
    if not enemy_data:
        await ctx.respond(
            hikari.Embed(
                title="Enemy not found!",
                description=f"Enemy `{ctx.options.enemy}` was not found, try waiting for auto-complete!",
            )
        )
        return

    enemy_levels = get_enemy_levels(enemy_data)
    enemy_abilities = get_enemy_abilities(enemy_data)
    enemy_immunities = get_immunities(enemy_data)
    prts_link = get_prts_link(enemy_data["excel"]["enemyId"])
    enemy_code = get_enemy_code(enemy_data)

    embeds_list = []
    for idx, level in enumerate(enemy_levels):
        embed = hikari.Embed(
            title=enemy_data["excel"]["name"] if not idx else None,
            description=enemy_abilities if not idx else None,
            url=prts_link if not idx else None,
        )

        embed.set_author(name=enemy_code)
        embed.set_thumbnail(f"{GITHUB_REPO}/enemy/{enemy_data["excel"]["enemyId"]}.png")

        add_embed_fields(embed, idx, level, enemy_immunities)

        embeds_list.append(embed)

    await ctx.respond(embeds=embeds_list)


@enemy.autocomplete("enemy")
async def enemy_autocomplete(
    opt: hikari.AutocompleteInteractionOption, inter: hikari.AutocompleteInteraction
) -> Union[str, Sequence[hikari.CommandChoice]]:
    user_input = opt.value.lower().strip()
    matching_enemies = [
        enemy_list["enemyData"][key]["name"]
        for key in enemy_list["enemyData"]
        if user_input in enemy_list["enemyData"][key]["name"].lower().strip()
    ][:25]

    return [hikari.CommandChoice(name=enemy, value=enemy) for enemy in matching_enemies]


def load(bot):
    bot.add_plugin(plugin)
