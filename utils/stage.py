import asyncio
import aiohttp

from aiohttp import ContentTypeError


async def fetch_json(session, url):
    async with session.get(url) as response:
        return await response.json()


async def fetch_enemy_data(session, enemy_id, enemy_level):
    url = f"https://awedtan.ca/api/enemy/{enemy_id}"
    try:
        data = await fetch_json(session, url)
    except ContentTypeError:
        return None
    return parse_enemy_data(data, enemy_level)


def parse_enemy_data(data, enemy_level):
    for level in data["value"]["levels"]["Value"]:
        if level.get("level") == enemy_level:
            level_stats = level["enemyData"]["attributes"]
            break
    else:
        return None

    return {
        "name": data["value"]["excel"]["name"],
        "status": data["value"]["excel"]["enemyLevel"],
        "level": enemy_level,
        "stats": {
            "ATK": level_stats["atk"]["m_value"],
            "DEF": level_stats["def"]["m_value"],
            "RES": level_stats["magicResistance"]["m_value"],
        },
    }


async def fetch_enemies_data(session, stage, mode):
    stage_mode = "toughstage" if mode.lower() == "challenge" else "stage"
    url = f"https://awedtan.ca/api/{stage_mode}/{stage}?include=levels.enemyDbRefs"

    async with session.get(url) as response:
        if response.status != 200:
            return None
        data = await response.json()

    enemy_data = [
        (enemy["id"], enemy["level"])
        for enemy in data["value"][0]["levels"]["enemyDbRefs"]
    ]
    tasks = [
        fetch_enemy_data(session, enemy_id, enemy_level)
        for enemy_id, enemy_level in enemy_data
    ]
    return await asyncio.gather(*tasks)


async def get_enemies(stage, mode):
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(limit=100)
    ) as session:
        enemies = await fetch_enemies_data(session, stage, mode)
        return sorted(
            [enemy for enemy in enemies if enemy is not None], key=lambda x: x["name"]
        )
