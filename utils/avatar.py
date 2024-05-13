from utils.data import GITHUB_REPO, operators


def get_avatar(operator):
    for operator_name, operator_data in operators.items():
        if operator_name.lower() == operator.lower():
            operator_id = operator_data["id"]

    if operator_id == "char_172_svrash":
        return f"{GITHUB_REPO}/avatar/ASSISTANT/{operator_id}.png"

    return f"{GITHUB_REPO}/avatar/ASSISTANT/{operator_id}_2.png"
