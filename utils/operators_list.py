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


def filter_and_translate(operators_list, operators_chinese_names):
    return [
        (
            operators_chinese_names[operator]
            if operator in unskilled_operators
            else (
                f"{operators_chinese_names[operator.rstrip(operator[-1])]} S{operator[-1]}"
                if operator[-1].isdigit()
                else operators_chinese_names.get(operator)
            )
        )
        for operator in operators_list
    ]
