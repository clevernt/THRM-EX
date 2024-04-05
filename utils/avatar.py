import json

url = "https://raw.githubusercontent.com/yuanyan3060/ArknightsGameResource/main/avatar"


def get_avatar(operator):
    with open("./data/operators.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for operator_name, operator_data in data.items():
            if operator_name.lower() == operator.lower():
                operator_id = operator_data["id"]

    return f"{url}/{operator_id}_2.png"
