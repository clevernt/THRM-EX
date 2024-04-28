import re
from typing import Union
import requests

API_URL = "https://awedtan.ca/api/enemy"
EMBED_COLORS = {"NORMAL": "#62759d", "ELITE": "#c58b3a", "BOSS": "#ce3131"}
REGEX_PATTERN = re.compile(r"<[^>]+>")


def get_enemy_data(enemy: str) -> dict:
    resp = requests.get(f"{API_URL}/{enemy.lower()}", timeout=10)
    if resp.status_code != 200:
        return None

    return resp.json()["value"]


def get_enemy_abilities(enemy_data: dict) -> list:
    abilities_list = [
        (
            f"**{re.sub(REGEX_PATTERN, '', ability['text'])}**"
            if ability["textFormat"] == "TITLE"
            else f"• {re.sub(REGEX_PATTERN, '', ability['text'])}"
        )
        for ability in enemy_data["excel"]["abilityList"]
    ]
    return "\n".join(abilities_list)


def get_enemy_code(enemy_data: dict) -> Union[str, int]:
    return enemy_data["excel"]["enemyIndex"]


def get_enemy_levels(enemy_data: dict) -> list:
    stats_list = []
    for level in enemy_data["levels"]["Value"]:
        stats = {
            "level": level["level"],
            "hp": level["enemyData"]["attributes"]["maxHp"]["m_value"],
            "atk": level["enemyData"]["attributes"]["atk"]["m_value"],
            "def": level["enemyData"]["attributes"]["def"]["m_value"],
            "res": level["enemyData"]["attributes"]["magicResistance"]["m_value"],
            "attackInterval": level["enemyData"]["attributes"]["baseAttackTime"][
                "m_value"
            ],
            "weight": level["enemyData"]["attributes"]["massLevel"]["m_value"],
        }
        stats_list.append(stats)
    return stats_list


def get_prts_link(enemy_id):
    enemy_cn_name = None
    resp = requests.get(
        "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/levels/enemydata/enemy_database.json"
    )
    data = resp.json()
    for enemy in data["enemies"]:
        if enemy["Value"][0]["enemyData"]["prefabKey"]["m_value"] == enemy_id:
            enemy_cn_name = enemy["Value"][0]["enemyData"]["name"]["m_value"]
            break

    return f"https://prts.wiki/w/{enemy_cn_name}"


def get_immunities(enemy_data: dict) -> list:
    immune_effects = [
        key[: -len("Immune")].title()
        for key, value in enemy_data["levels"]["Value"][0]["enemyData"][
            "attributes"
        ].items()
        if value.get("m_defined", False) and key.endswith("Immune")
    ]
    return immune_effects or "None"


def add_embed_fields(embed, idx, level, enemy_immunities):
    fields = [
        ("Level", level["level"]),
        ("HP", level["hp"]),
        ("ATK", level["atk"]),
        ("DEF", level["def"]),
        ("RES", level["res"]),
        ("Attack Interval", level["attackInterval"]),
        ("Weight", level["weight"]),
        ("Immunities", ", ".join(enemy_immunities)),
    ]

    for name, value in fields:
        if idx and not value:
            continue
        embed.add_field(name, value, inline=name not in ["Level", "Immunities"])
