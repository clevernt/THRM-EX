import json
from utils import GITHUB_REPO


def get_avatar(operator):
    with open("./data/operators.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for operator_name, operator_data in data.items():
            if operator_name.lower() == operator.lower():
                operator_id = operator_data["id"]

    if operator_id == "char_172_svrash":
        return f"{GITHUB_REPO}/avatar/ASSISTANT/{operator_id}.png"

    return f"{GITHUB_REPO}/avatar/ASSISTANT/{operator_id}_2.png"
