import requests
from bs4 import BeautifulSoup
import csv


CSV = "disks.csv"
HOST = "https://hotline.ua/"
url = input("Enter target URL to parse: ")
urls = []

HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.68 Safari/537.36"
}


def get_html(url):
    response = requests.get(url, headers=HEADERS)
    return response


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("div", class_="list-item list-item--row")
    disks = []
    for item in items:
        disks.append(
            {
                "item": item.find("div", class_="list-item__info").find("a").get_text(strip=True),
                "url": "https://hotline.ua" + item.find("div", class_="list-item__info").find("a").get("href"),
                "price": item.find("div", class_="list-item__value--overlay m_b-5").find("div", class_="m_b-5").get_text(strip=True).replace("\xa0","").replace(" – ",";").replace(" грн",""),
                "capacity": item.find("span", class_="spec-item spec-item--bullet").find_next_sibling("span").find_next_sibling("span").get_text(strip=True).replace(" ГБ", "")

            }
        )
    return disks


def get_urls(html):
    soup = BeautifulSoup(html, "html.parser")
    pages = soup.find("div", class_="pagination__pages flex").find_all("a", class_="page")
    last_page = pages[-1].get_text()
    page = int(last_page)
    x = 0
    while x < page:
        x += 1
        urls.append(url + "?p=" + str(x))
    return last_page


def save_doc(items, path):
    with open(path, "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["item", "url", "price", "capacity"])
        for item in items:
            writer.writerow([item["item"], item["url"], item["price"], item["capacity"]])


html = get_html(url)
last_page = get_urls(html.text)


disks = []
for url in urls:
    print("Parsing " + url)
    html = get_html(url)
    disks.extend(get_content(html.text))

save_doc(disks, CSV)
