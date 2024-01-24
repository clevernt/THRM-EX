import json

files_to_sort = ["./data/branches.json", "./data/modules.json", "./data/operators.json"]


def sort(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    sorted_data = {key: data[key] for key in sorted(data.keys())}

    with open(file, "w", encoding="utf-8") as sorted_f:
        json.dump(sorted_data, sorted_f, indent=2, ensure_ascii=False)


for file in files_to_sort:
    sort(file)
