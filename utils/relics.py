import requests

rogue_mapping = {
    "rogue_1": "IS2: Phantom & Crimson Solitaire",
    "rogue_2": "IS3: Mizuki & Caerula Arbor",
    "rogue_3": "IS4: Expeditioner's Jǫklumarkar",
}

relics_data = requests.get("https://raw.githubusercontent.com/ArknightsAssets/ArknightsGamedata/master/en/gamedata/excel/roguelike_topic_table.json").json()


def get_relic_details(relic: str) -> dict:
    matching_relics = []
    for rogue_key, rogue_name in rogue_mapping.items():
        items = relics_data.get("details", {}).get(rogue_key, {}).get("items", {})
        for _, relic_details in items.items():
            if relic_details.get("name").lower() == relic.lower():
                matching_relics.append(
                    {
                        "rogue": rogue_name,
                        "iconId": relic_details.get("iconId"),
                        "name": relic_details.get("name"),
                        "description": relic_details.get("description"),
                        "usage": relic_details.get("usage"),
                        "unlockCond": relic_details.get("unlockCondDesc"),
                    }
                )
    return matching_relics


def get_relic_icon(relic_id: str) -> str:
    return f"https://raw.githubusercontent.com/Awedtan/HellaAssets/main/rogueitems/{relic_id}.png"
