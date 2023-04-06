"""Main file to scrap data from arttidesign.com.ua."""

import time

import requests
from bs4 import BeautifulSoup
import lxml
import json


def read_url(url: str, delay: int = 0):
    """Read url and return response. Delay is in seconds."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    time.sleep(delay)
    return response


def save_html_file(file_name, response, counter=0) -> None:
    """Save html file to data folder."""
    with open(f"data/{file_name}_{counter}.html", "w", encoding="utf-8") as f:
        f.write(response.text)


def read_html_file(file_name: str) -> str:
    """Read html file from data folder."""
    with open(f"data/{file_name}.html", "r", encoding="utf-8") as f:
        src = f.read()
    return src


def read_json_file(file_name: str) -> dict:
    """Read json file from json folder."""
    with open(f"json/{file_name}.json", encoding="utf-8") as f:
        data = json.load(f)
    return data


def save_to_json(data, file_name: str):
    """Save data to json file."""
    with open(f"json/{file_name}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def scrap_links(source: bytes):
    """Scrap product links from html file."""
    data_dict = {}
    soup = BeautifulSoup(source, "lxml")

    for link_tag in soup.findAll("a", {"class": "cs-goods-title"}):
        data_dict[link_tag.text] = "https://arttidesign.com.ua" + link_tag.get("href")

    return data_dict


def scrap_product_data(source) -> dict:
    """Scrap product data from html file."""
    soup = BeautifulSoup(source, "lxml")

    main_content = soup.find("div", {"class": "cs-page__main-content"})
    product_name = main_content.find(
        "span", {"class": "cs-title__product"}
    ).text.strip()
    product_price = main_content.find(
        "span", {"data-qaid": "product_price"}
    ).text.strip()
    product_image = (
        main_content.find("div", {"class": "cs-image-holder__image-link"})
        .find("img")
        .get("src")
    )
    product_sku_stock = main_content.find(
        "ul", {"class": "b-product-data"}
    ).findChildren("li", recursive=False)
    product_stock = product_sku_stock[0].text.strip()
    product_sku = product_sku_stock[1].text.strip().replace("Код: ", "")
    product_description = main_content.find("div", {"class": "b-user-content"}).get_text()
    product_table = main_content.find("table", {"class": "b-product-info"}).findAll(
        "tr"
    )

    product_table_dict = {}
    for item in product_table:
        td = item.findAll("td")
        try:
            title = td[0].text.strip()
            data = td[1].text.strip()
            product_table_dict[title] = data
        except IndexError:
            continue

    product_dict = {
        "name": product_name,
        "sku": product_sku,
        "price": product_price,
        "stock": product_stock,
        "image": product_image,
        "description": product_description,
        "features": product_table_dict,
    }
    return product_dict


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
    # i = 0
    # for item in read_json_file("links_data").values():
    #     link = read_url(url=item, delay=0.5)
    #
    #     if link.status_code == 200:
    #         save_html_file("product", link, i)
    #         print(link.status_code)
    #     else:
    #         print(link.status_code)
    #         continue
    #
    #     i += 1

    # scrap product data
    products = []
    for i in range(0, 5):
        try:
            file = read_html_file(f"product_{i}")
            products.append(scrap_product_data(file))
            print(f"Processing file {i}")
        except FileNotFoundError:
            print(f"File {i} not found")
            break

    save_to_json(products, "products")
