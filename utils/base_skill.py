import hikari
import requests
import re

REGEX_PATTERN = re.compile(r"<\$cc[^>]*>|<@cc[^>]*>|<\/>")


# Should really be in another file (maybe data.py)
def get_operator_data(operator: str):
    response = requests.get(
        f"https://awedtan.ca/api/operator/{operator.lower()}?include=bases"
    )
    if response.status_code == 200:
        return response.json()
    return None


def extract_base_skills(operator_data):
    bases = operator_data.get("value", {}).get("bases", [])
    base_skills = []
    for base_skill in bases:
        skill_icon = base_skill.get("skill", {}).get("skillIcon", {})
        color = base_skill.get("skill", {}).get("buffColor", {})
        req_elite = base_skill.get("condition", {}).get("cond", {}).get("phase")
        req_level = base_skill.get("condition", {}).get("cond", {}).get("level")
        name = base_skill.get("skill", {}).get("buffName")
        room_type = base_skill.get("skill", {}).get("roomType")
        description = base_skill.get("skill", {}).get("description")
        base_skills.append(
            {
                "skillIcon": skill_icon,
                "color": color,
                "reqElite": req_elite,
                "reqLevel": req_level,
                "name": name,
                "roomType": room_type,
                "description": f"{re.sub(REGEX_PATTERN, "**", description)}",
                "terms": re.findall(r"<\$cc[^>]*>", description),
            }
        )
    return base_skills


def create_embeds(operator, base_skills):
    embeds = []
    for idx, base_skill in enumerate(base_skills):
        embed = hikari.Embed(
            title=(operator.title() if not idx else base_skill["name"]),
            description=(
                f"**E{base_skill['reqElite'][-1]} Lv{base_skill['reqLevel']}**\n{base_skill['description']}"
                if idx
                else None
            ),
            color=base_skill["color"],
        )
        embed.set_thumbnail(
            f"https://raw.githubusercontent.com/KrisTheNewest/MayerBotPics/master/riic/{base_skill['skillIcon']}.webp"
        )

        if not idx:
            embed.add_field(
                f"{base_skill['name']}",
                f"**E{base_skill['reqElite'][-1]} Lv{base_skill['reqLevel']}**\n{base_skill['description']}",
            )

        if terms := base_skill["terms"]:
            for term in terms:
                dictionary = requests.get(
                    f"https://awedtan.ca/api/define/{term[2:-1]}"
                ).json()
                term_name = dictionary["value"].get("termName")
                term_description = dictionary["value"].get("description")
                embed.add_field(term_name, term_description)

        embeds.append(embed)
    return embeds
