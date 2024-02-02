import requests
import json

from bs4 import BeautifulSoup


def get_avatar(operator):

    with open("./data/operators.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for operator_name, operator_data in data.items():
            if operator_name.lower() == operator.lower():
                chinese_name = operator_data["name"]

    link = f"https://prts.wiki/w/文件:头像_{chinese_name}.png"
    response = requests.get(link)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")

        img_link = soup.select_one(".fullImageLink a")["href"]

        return f"https://prts.wiki{img_link}"

    else:
        return None
