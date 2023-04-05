import time

import requests
from bs4 import BeautifulSoup
import lxml
import json


def read_url(url: str, delay: int = 0):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    time.sleep(delay)
    return response


def save_html_file(file_name, response, counter=0):
    with open(f"data/{file_name}_{counter}.html", "w", encoding="utf-8") as f:
        f.write(response.text)


def read_html_file(file_name: str) -> bytes:
    with open(f"data/{file_name}.html", encoding="utf-8") as f:
        src = f.read()
    return src


def read_json_file(file_name: str) -> dict:
    with open(f"json/{file_name}.json", encoding="utf-8") as f:
        data = json.load(f)
    return data


def save_to_json(data: dict, file_name: str):
    with open(f"json/{file_name}.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def scrap_links(source: bytes):
    data_dict = {}
    soup = BeautifulSoup(source, "lxml")

    for link_tag in soup.findAll("a", {"class": "cs-goods-title"}):
        data_dict[link_tag.text] = "https://arttidesign.com.ua" + link_tag.get("href")

    return data_dict


if __name__ == "__main__":
    # save all html files from category
    # for i in range(1, 6):
    #     url = read_url(f"https://arttidesign.com.ua/ua/g86105736-vertikalnye-dizajnerskie-radiatory/page_{i}")
    #     if url.status_code == 200:
    #         save_html_file("index", url, i)
    #     else:
    #         print(f"404 - {i}")
    #         break

    # scrap all product names and links from html files and save result to json
    # links_data_dict = {}
    # for i in range(1, 6):
    #     try:
    #         file = read_html_file(f"index_{i}")
    #         links_data_dict.update(scrap_links(file))
    #     except FileNotFoundError:
    #         print("File not found")
    #         break
    #
    # save_to_json(data=links_data_dict, file_name="links_data")

    # save html product pages
    i = 0
    for item in read_json_file("links_data").values():
        link = read_url(url=item, delay=0.5)

        if link.status_code == 200:
            save_html_file("product", link, i)
            print(link.status_code)
        else:
            print(link.status_code)
            continue

        i += 1

    # scrap product data

