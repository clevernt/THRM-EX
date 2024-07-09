import json

EMBED_COLOR = 16448250
ARKREC_URL = "https://en.arkrec.com/api/records"
GITHUB_REPO = "https://raw.githubusercontent.com/fexli/ArknightsResource/main/"

with open("./data/operators.json", encoding="utf-8") as f:
    operators = json.load(f)

with open("./data/categories.json", encoding="utf-8") as f:
    categories = json.load(f)
    categories_en = [value.lower() for value in categories.values()]

with open("./data/terms.json", encoding="utf-8") as f:
    terms_dict = json.load(f)


def get_operator_id(operator_name):
    for operator_key, operator_data in operators.items():
        if operator_data["nameEn"].lower() == operator_name.lower():
            return operator_key
