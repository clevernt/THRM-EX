import requests
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


def get_mats(operator_id, branch_code):
    uniequip_table = requests.get(
        "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/uniequip_table.json"
    ).json()
    item_name_to_id = requests.get(
        "https://raw.githubusercontent.com/neeia/ak-roster/main/src/data/item-name-to-id.json"
    ).json()

    id_to_name_dict = {v: k for k, v in item_name_to_id.items()}

    materials = [
        (id_to_name_dict.get(item["id"], "Unknown"), item["count"])
        for module in uniequip_table.get("equipDict", {}).values()
        if module.get("charId") == operator_id
        and module.get("typeIcon") == branch_code.lower()
        for stage in module.get("itemCost", {}).values()
        for item in stage
        if item.get("type", "") == "MATERIAL"
        and not item.get("id", "").startswith("mod")
    ]

    return materials
