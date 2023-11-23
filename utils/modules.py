import json

range_mods = {
    "SPC-X": "https://uwu.so/neuvium/new5soyo92",
    "RIN-X": "https://uwu.so/neuvium/nesDf7uFTC",
}

operators_with_modules = {}
with open("./data/modules.json", "r") as f:
    data = json.load(f)
    for operator in data:
        operators_with_modules[operator.lower()] = operator


def get_modules(operator_name):
    modules_list = []
    with open("./data/modules.json") as f:
        modules_data = json.load(f)
        for operator, modules in modules_data.items():
            if operator.lower() == operator_name.lower():
                modules_list.extend(modules)
    return modules_list


def get_branch_trait(branch_code):
    with open("./data/branches.json") as f:
        branches_data = json.load(f)

        return branches_data[branch_code.upper()]


def get_branch_icon(branch_code):
    branch_icon_url = f"https://raw.githubusercontent.com/Aceship/Arknight-Images/main/equip/type/{branch_code}.png"

    return branch_icon_url


def get_operator_avatar(operator):
    with open("./data/operators.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for operator_name, operator_data in data.items():
            if operator_name.lower() == operator.lower():
                operator_id = operator_data["id"]

    avatar_url = f"https://raw.githubusercontent.com/Aceship/Arknight-Images/main/avatars/{operator_id}.png"
    return avatar_url
