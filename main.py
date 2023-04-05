import requests
from bs4 import BeautifulSoup
import lxml
import json

url1 = "https://arttidesign.com.ua/ua/g86105736-vertikalnye-dizajnerskie-radiatory"


def get_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    return response


def save_html_file(file_name, response, counter=0):
    with open(f"data/{file_name}_{counter}.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    counter += 1


def read_html_file(file_name):
    with open(f"data/{file_name}.html", encoding="utf-8") as f:
        src = f.read()
    return src
