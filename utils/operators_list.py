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
    return [
        (
            operator_names[operator]
            if operator in unskilled_operators
            else (
                f"{operator_names[operator.rstrip(operator[-1])]} S{operator[-1]}"
                if operator[-1].isdigit()
                else operator_names.get(operator)
            )
        )
        for operator in operators_list
    ]
