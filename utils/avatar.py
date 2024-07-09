from utils.data import GITHUB_REPO, get_operator_id


def get_avatar(operator):
    operator_id = get_operator_id(operator)

    if operator_id in ["char_172_svrash", "char_4087_ines", "char_423_blemsh"]:
        return f"{GITHUB_REPO}/avatar/ASSISTANT/{operator_id}.png"
    else:
        return f"{GITHUB_REPO}/avatar/ASSISTANT/{operator_id}_2.png"
