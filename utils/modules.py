import json
import requests

from utils.data import GITHUB_REPO

range_mods = {
    "SPC-X": "https://uwu.so/neuvium/new5soyo92",
    "RIN-X": "https://uwu.so/neuvium/nesDf7uFTC",
}

operators_with_modules = {}
with open("./data/operators.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    for operator_key, operator_data in data.items():
        if operator_data.get("modules", {}):
            operators_with_modules[operator_data["name_en"].lower()] = operator_data[
                "name_en"
            ]


def get_modules(operator_name):
    modules_list = []
    with open("./data/operators.json", encoding="utf-8") as f:
        modules_data = json.load(f)
        for _, operator_data in modules_data.items():
            if operator_data["name_en"].lower() == operator_name.lower():
                modules_list.extend(operator_data.get("modules"))
    return modules_list


def get_branch_trait(branch_code, operator_name):
    with open("./data/branches.json") as f:
        branches_data = json.load(f)
        branch_data = branches_data.get(branch_code.upper(), {})
        if isinstance(branch_data, dict):
            return branch_data[operator_name]
        else:
            return branch_data


def get_branch_icon(branch_code):
    # for some reason TRP-D is the only capitalized one in the repo
    if branch_code != "TRP-D":
        branch_code = branch_code.lower()
    return f"{GITHUB_REPO}/equipt/{branch_code}.png"


def get_release_event(branch_code):
    with open("./data/release_events.json") as f:
        data = json.load(f)
        return next(
            (event for event, modules in data.items() if branch_code in modules), None
        )


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
        and module.get("typeIcon").lower() == branch_code.lower()
        for stage in module.get("itemCost", {}).values()
        for item in stage
        if isinstance(item, dict)
        and item.get("type", "") == "MATERIAL"
        and not item.get("id", "").startswith("mod")
    ]
    return materials
