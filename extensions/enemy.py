import hikari
import lightbulb
import json
import re

from typing import Union, Sequence

plugin = lightbulb.Plugin("enemy")

with open("./data/enemy_database.json", encoding="utf-8") as f:
    enemy_db = json.load(f)

enemy_colors = {"NORMAL": "#62759d", "ELITE": "#c58b3a", "BOSS": "#ce3131"}
regex_pattern = re.compile(r"<(\$[a-z]+\.[a-z]+\.[a-z]+)>(.*?)</>")


def get_prts_link(enemy_id):
    enemy_cn_name = None
    with open("./data/enemy_database_cn.json", encoding="utf-8") as cn_db:
        enemy_db_cn = json.load(cn_db)
        for enemy in enemy_db_cn["enemies"]:
            if enemy["Value"][0]["enemyData"]["prefabKey"]["m_value"] == enemy_id:
                enemy_cn_name = enemy["Value"][0]["enemyData"]["name"]["m_value"]
                break

    return f"https://prts.wiki/w/{enemy_cn_name}"


def get_abilities(enemy_id):
    with open("./data/enemy_handbook_table.json", encoding="utf-8") as handbook:
        handbook_data = json.load(handbook)
        for _, enemy in handbook_data["enemyData"].items():
            if enemy["enemyId"] == enemy_id:
                ability_list = [ability["text"] for ability in enemy["abilityList"]]
                ability_list = [
                    regex_pattern.sub(r"**\2**", ability_text)
                    for ability_text in ability_list
                ]
                return ability_list

    return []


def get_enemy_code(enemy_id):
    with open("./data/enemy_handbook_table.json", encoding="utf-8") as handbook:
        handbook_data = json.load(handbook)
        for _, enemy in handbook_data["enemyData"].items():
            if enemy["enemyId"] == enemy_id:
                return enemy["enemyIndex"]


def find_enemy(ctx, enemy_db):
    enemy_levels = []

    for enemy_entry in enemy_db["enemies"]:
        for level_data in enemy_entry["Value"]:
            stored_name = level_data["enemyData"]["name"]["m_value"]
            if stored_name and isinstance(stored_name, str):
                stored_name = stored_name.lower().replace(",", "").strip()
                input_name = ctx.options.enemy.lower().replace(",", "").strip()
                if stored_name == input_name:
                    enemy_levels.extend(enemy_entry["Value"])
                    break

    return enemy_levels


def process_basic_info(enemy):
    name = enemy["enemyData"]["name"]["m_value"]
    enemy_id = enemy["enemyData"]["prefabKey"]["m_value"]
    level = enemy["enemyData"]["levelType"]["m_value"]

    basic_info = {
        "name": name,
        "id": enemy_id,
        "level": level,
    }

    return basic_info


def process_immunities(enemy):
    immunities = {
        "stunImmune": enemy["enemyData"]["attributes"]["stunImmune"]["m_value"],
        "silenceImmune": enemy["enemyData"]["attributes"]["silenceImmune"]["m_value"],
        "sleepImmune": enemy["enemyData"]["attributes"]["sleepImmune"]["m_value"],
        "frozenImmune": enemy["enemyData"]["attributes"]["frozenImmune"]["m_value"],
        "levitateImmune": enemy["enemyData"]["attributes"]["levitateImmune"]["m_value"],
    }

    active_immunities = [
        key[:-6].capitalize() for key, value in immunities.items() if value
    ]
    if active_immunities:
        return ", ".join(active_immunities)
    else:
        return "None"


def process_enemy_data(enemy):
    enemy_lvl = enemy["level"]
    enemy_hp = enemy["enemyData"]["attributes"]["maxHp"]["m_value"]
    enemy_atk = enemy["enemyData"]["attributes"]["atk"]["m_value"]
    enemy_def = enemy["enemyData"]["attributes"]["def"]["m_value"]
    enemy_res = enemy["enemyData"]["attributes"]["magicResistance"]["m_value"]
    enemy_atk_intrvl = enemy["enemyData"]["attributes"]["baseAttackTime"]["m_value"]
    enemy_weight = enemy["enemyData"]["attributes"]["massLevel"]["m_value"]

    enemy_data = {
        "lvl": enemy_lvl,
        "hp": enemy_hp,
        "atk": enemy_atk,
        "def": enemy_def,
        "res": round(enemy_res),
        "atkIntrvl": enemy_atk_intrvl,
        "weight": enemy_weight,
    }

    return enemy_data


@plugin.command
@lightbulb.option("enemy", "Enemy's name", required=True, autocomplete=True)
@lightbulb.command("enemy", "Get an enemy's details")
@lightbulb.implements(lightbulb.SlashCommand)
async def enemy(ctx):
    enemy_levels = find_enemy(ctx, enemy_db)

    if not enemy_levels:
        await ctx.respond(
            hikari.Embed(
                title="Enemy not found!",
                description=f"Enemy `{ctx.options.enemy}` was not found, try waiting for auto-complete!",
            )
        )

    basic_info = process_basic_info(enemy_levels[0])

    abilities = get_abilities(basic_info["id"])
    formatted_abilities = "\n".join([f"• {ability}" for ability in abilities])

    embeds = []
    added_fields = set()

    for index, level in enumerate(enemy_levels):
        enemy_data = process_enemy_data(level)
        immunities = process_immunities(level)

        embed = hikari.Embed(
            title=(basic_info["name"] if index == 0 else ""),
            description=(formatted_abilities if index == 0 else ""),
            color=(enemy_colors.get(basic_info["level"])),
            url=get_prts_link(basic_info["id"]) if index == 0 else "",
        )

        embed.set_thumbnail(
            f"https://raw.githubusercontent.com/Aceship/Arknight-Images/main/enemy/{basic_info['id']}.png"
        )

        if index == 0:
            embed.set_author(name=get_enemy_code(basic_info["id"]))

        embed.add_field("Level", enemy_data["lvl"])
        if enemy_data["hp"] != 0 or "HP" not in added_fields:
            embed.add_field("HP", enemy_data["hp"], inline=True)
            added_fields.add("HP")

        if enemy_data["atk"] != 0 or "ATK" not in added_fields:
            embed.add_field("ATK", enemy_data["atk"], inline=True)
            added_fields.add("ATK")

        if enemy_data["def"] != 0 or "DEF" not in added_fields:
            embed.add_field("DEF", enemy_data["def"], inline=True)
            added_fields.add("DEF")

        if enemy_data["res"] != 0 or "RES" not in added_fields:
            embed.add_field("RES", enemy_data["res"], inline=True)
            added_fields.add("RES")

        if enemy_data["atkIntrvl"] != 0 or "Attack Interval" not in added_fields:
            embed.add_field(
                "Attack Interval", f'{enemy_data["atkIntrvl"]}s', inline=True
            )
            added_fields.add("Attack Interval")

        if enemy_data["weight"] != 0 or "Weight" not in added_fields:
            embed.add_field("Weight", enemy_data["weight"], inline=True)
            added_fields.add("Weight")

        if immunities != "None" or "Immunities" not in added_fields:
            embed.add_field("Immunities", immunities)
            added_fields.add("Immunities")

        embeds.append(embed)

    if embeds:
        await ctx.respond(embeds=embeds)


@enemy.autocomplete("enemy")
async def enemy_autocomplete(
    opt: hikari.AutocompleteInteractionOption, inter: hikari.AutocompleteInteraction
) -> Union[str, Sequence[hikari.CommandChoice]]:
    user_input = opt.value.lower().strip()  # Trim whitespaces and convert to lowercase

    matching_enemies = [
        enemy_data["enemyData"]["name"]["m_value"].lower().strip()
        for enemy_entry in enemy_db["enemies"]
        for enemy_data in enemy_entry["Value"]
        if enemy_data["enemyData"]["name"]["m_value"] is not None
    ]

    matching_enemies = [enemy for enemy in matching_enemies if user_input in enemy]
    matching_enemies = matching_enemies[:25]

    return [
        hikari.CommandChoice(name=enemy.title(), value=enemy.title())
        for enemy in matching_enemies
    ]


def load(bot):
    bot.add_plugin(plugin)
