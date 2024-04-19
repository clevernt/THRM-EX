import asyncio
import aiohttp


async def fetch_json(session, url):
    async with session.get(url) as response:
        return await response.json()


async def fetch_enemy_data(session, enemy_id, enemy_level):
    url = f"https://hellabotapi.cyclic.app/enemy/{enemy_id}"
    data = await fetch_json(session, url)
    level_stats = next(
        level["enemyData"]["attributes"]
        for level in data["value"]["levels"]["Value"]
        if level.get("level") == enemy_level
    )
    enemy_data = {
        "name": data["value"]["excel"]["name"],
        "status": data["value"]["excel"]["enemyLevel"],
        "level": enemy_level,
        "stats": {
            "ATK": level_stats["atk"]["m_value"],
            "DEF": level_stats["def"]["m_value"],
            "RES": level_stats["magicResistance"]["m_value"],
        },
    }
    return enemy_data


async def get_enemies(stage, mode):
    stage_mode = "toughstage" if mode.lower() == "challenge" else "stage"

    connector = aiohttp.TCPConnector(limit=30)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(
            f"https://hellabotapi.cyclic.app/{stage_mode}/{stage}?include=levels.enemyDbRefs"
        ) as response:
            if response.status == 200:
                data = await response.json()
            else:
                return None

        enemy_data = {
            (enemy["id"], enemy["level"])
            for enemy in data["value"][0]["levels"]["enemyDbRefs"]
        }

        tasks = [
            fetch_enemy_data(session, enemy_id, enemy_level)
            for enemy_id, enemy_level in enemy_data
        ]
        enemy_names = await asyncio.gather(*tasks)
        return sorted(enemy_names, key=lambda x: x["name"])
