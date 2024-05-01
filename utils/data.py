import json

EMBED_COLOR = 16448250
ARKREC_URL = "https://arkrec.com/api/records"
GITHUB_REPO = "https://raw.githubusercontent.com/fexli/ArknightsResource/main/"

with open("./data/operators.json", encoding="utf-8") as f:
    operators = json.load(f)
    operators_chinese_names = {operators[key]["name"]: key for key in operators}

with open("./data/categories.json", encoding="utf-8") as f:
    categories = json.load(f)
    categories_en = [value.lower() for value in categories.values()]
