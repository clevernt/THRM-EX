unskilled_operators = [
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


def filter_and_translate(operators_list, operator_names):
    operators_list_en = []
    for operator in operators_list:
        if operator in unskilled_operators:
            operators_list_en.append(operator_names[operator])
        else:
            skill = f"S{operator[-1]}" if operator[-1].isnumeric() else None
            name_cn = operator.rstrip(skill)
            name_en = operator_names.get(name_cn)
            operators_list_en.append(
                f"{name_en} {skill}" if skill is not None else f"{name_en}"
            )
    return operators_list_en
