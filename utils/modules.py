import requests
import json

from utils import GITHUB_REPO

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
    # for some reason TRP-D is the only capitalized one in the repo
    if branch_code != "TRP-D":
        branch_code = branch_code.lower()
    return f"{GITHUB_REPO}/equipt/{branch_code}.png"


def get_mats(operator_id, branch_code):
    uniequip_table = requests.get(
        "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/uniequip_table.json"
    ).json()

    with open("./data/materials.json") as f:
        materials_data = json.load(f)

    materials = [
        (
            f"{item['count']}x <:{materials_data[item['id']]['id']}:{materials_data[item['id']]['emojiId']}>"
        )
        for module in uniequip_table.get("equipDict", {}).values()
        if isinstance(module, dict)
        and module.get("charId") == operator_id
        and module.get("typeIcon") == branch_code.lower()
        for stage in module.get("itemCost", {}).values()
        for item in stage
        if isinstance(item, dict)
        and item.get("type", "") == "MATERIAL"
        and not item.get("id", "").startswith("mod")
    ]

    return materials
