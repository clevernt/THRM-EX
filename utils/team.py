from utils.data import operators

bad_operators = [
    "Friston-3",
    "U-Official",
    "THRM-EX",
    "泰拉大陆调查团",
    "Lancet-2",
    "Castle-3",
    "正义骑士号",
    "夜刀",
    "巡林者",
    "黑角",
    "杜林",
    "12F",
]


def translate_operators(team):
    translated_team = []

    for operator in team:
        operator_name = None
        skill = ""

        if operator in bad_operators:
            operator_name = next(
                (op["name_en"] for op in operators.values() if op["name_cn"] == operator),
                None,
            )
        else:
            operator_name = next(
                (
                    op["name_en"]
                    for op in operators.values()
                    if op["name_cn"] == operator.rstrip("123")
                ),
                None,
            )
            if operator[-1].isdigit():
                skill = f" S{operator[-1]}"

        translated_name = f"{operator_name}{skill}" if skill else operator_name
        translated_team.append(translated_name)

    return translated_team
