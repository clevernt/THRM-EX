import requests
import re
import hikari

professions = {
    "SNIPER": "Sniper",
    "PIONEER": "Vanguard",
    "WARRIOR": "Guard",
    "CASTER": "Caster",
    "SUPPORT": "Supporter",
    "MEDIC": "Medic",
    "TANK": "Defender",
    "SPECIAL": "Specialist",
}

sp_types = {
    "INCREASE_WITH_TIME": "Natural Recovery",
    "INCREASE_WHEN_ATTACK": "Offensive Recovery",
    "INCREASE_WHEN_TAKEN_DAMAGE": "Defensive Recovery",
}

colors = {
    "TIER_6": 16628340,
    "TIER_5": 16638022,
    "TIER_4": 10859772,
    "TIER_3": 8246268,
    "TIER_2": 12513892,
    "TIER_1": 13948120,
}

# Only ones that are actually different, others can just be .title()'d
sub_professions = {
    "bearer": "Flagbearer",
    "artsfghter": "Arts Fighter",
    "sword": "Swordmaster",
    "musha": "Soloblade",
    "fearless": "Dreadnought",
    "librator": "Liberator",
    "unyield": "Juggernaut",
    "artsprotector": "Arts Protector",
    "fastshot": "Marksman",
    "closerange": "Heavyshooter",
    "aoesniper": "Artilleryman",
    "longrange": "Deadeye",
    "reaperrange": "Spreadshooter",
    "siegesniper": "Besieger",
    "bombarder": "Flinger",
    "corecaster": "Core Caster",
    "splashcaster": "Splash Caster",
    "funnel": "Mech-accord Caster",
    "phalanx": "Phalanx Caster",
    "mystic": "Mystic Caster",
    "chain": "Chain Caster",
    "blastcaster": "Blast Caster",
    "physician": "Medic",
    "ringhealer": "Multitarget Medic",
    "healer": "Therapist",
    "wandermedic": "Wandering Medic",
    "slower": "Decel Binder",
    "craftsman": "Artificer",
    "blessing": "Abjurer",
    "underminer": "Hexer",
    "pusher": "Push Stroker",
    "stalker": "Ambusher",
    "traper": "Trapmaster",
    "incantationmedic": "Incantation Medic",
    "shotprotector": "Sentinel Iron Guard",
    "chainhealer": "Chain Healer",
    "primcaster": "Primal Caster",
}


def format_value(value, format_str):
    if format_str == "0%":
        return f"{value * 100:.0f}%"
    elif format_str == "0":
        return f"{value:.1f}"
    else:
        return f"{value}"


def fetch_operator_data(operator_name):
    response = requests.get(
        f"https://awedtan.ca/api/operator/{operator_name.strip().lower()}"
    )
    response.raise_for_status()
    return response.json()


def parse_skill_description(skill_desc, blackboard):
    for item in blackboard:
        placeholder = r"\{" + re.escape(item["key"]) + r"(:\d+%|\d+)?\}"
        match = re.search(placeholder, skill_desc)
        format_str = ("0%" if "%" in match.group(0) else "0") if match else "0"
        value_str = format_value(item["value"], format_str)
        skill_desc = re.sub(placeholder, value_str, skill_desc)
    return re.sub(r"<[@\$]ba\.[^>]+>|</>", "", skill_desc)


def create_embed(api_resp):
    op_id = api_resp["canon"]
    op_data = api_resp["value"]

    name = op_data["data"]["name"]
    trait = op_data["data"]["description"]
    rarity = op_data["data"]["rarity"]
    profession = op_data["data"]["profession"]
    sub_profession = op_data["data"]["subProfessionId"]
    description = op_data["data"]["itemDesc"]

    talent_names = [
        talent["candidates"][-1]["name"] for talent in op_data["data"]["talents"]
    ]
    talent_descs = [
        talent["candidates"][-1]["description"] for talent in op_data["data"]["talents"]
    ]
    talents = list(zip(talent_names, talent_descs))

    skills = []
    for skill in op_data["skills"]:
        last_level = skill["levels"][-1]
        skill_name = last_level["name"]
        skill_desc = parse_skill_description(
            last_level["description"], last_level["blackboard"]
        )
        skills.append(
            {
                "name": skill_name,
                "description": skill_desc,
                "skillType": last_level["skillType"].title(),
                "spType": sp_types.get(last_level["spData"]["spType"]),
                "spCost": last_level["spData"]["spCost"],
                "initSp": last_level["spData"]["initSp"],
            }
        )

    em = hikari.Embed(
        title=f"{rarity[-1]}-Star {professions.get(profession)} // {sub_professions.get(sub_profession, sub_profession.title())}",
        description=f"{re.sub(r'<[@\$]ba\.[^>]+>|</>', '', trait)}\n__Values Shown At Max Potential & Skill Level__",
        color=colors.get(rarity),
    )
    em.set_author(
        name=name,
        icon=f"https://raw.githubusercontent.com/akgcc/arkdata/main/assets/torappu/dynamicassets/arts/charavatars/{op_id}.png",
    )
    em.set_thumbnail(
        f"https://raw.githubusercontent.com/fexli/ArknightsResource/main/charpor/{op_id}_1.png"
    )
    em.set_footer(description)

    for talent_name, talent_desc in talents:
        em.add_field(
            name=talent_name,
            value=re.sub(r"<[@\$]ba\.[^>]+>|</>", "", talent_desc),
            inline=True,
        )

    for skill in skills:
        em.add_field(
            name=skill.get("name"),
            value=f"**{skill.get('skillType')} | {skill.get('spType')} | Cost: {skill.get('spCost')} | Initial: {skill.get('initSp')}**\n{skill.get('description')}",
        )

    return em
