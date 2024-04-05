import json

EMBED_COLOR = 16448250
ARKREC_URL = "https://arkrec.com/api/records"
mode_mapping = {"Normal Mode": "normal", "Challenge Mode": "challenge"}

with open("./data/stage_table.json", encoding="utf-8") as f:
    stage_table = json.load(f)["stages"]

with open("./data/operators.json", encoding="utf-8") as f:
    data = json.load(f)
    operator_names = {data[key]["name"]: key for key in data}

with open("./data/categories.json", encoding="utf-8") as f:
    categories = json.load(f)
    categories_en = [value.lower() for value in categories.values()]