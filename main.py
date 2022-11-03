import requests
from bs4 import BeautifulSoup
import csv


CSV = "disks.csv"
# https://hotline.ua/ua/computer/zhestkie-diski/941-945-9517-31348-602322/?mode=series
# https://hotline.ua/ua/computer/zhestkie-diski/941-9517-31348-602322-639535/?mode=series
urls = [
    "https://hotline.ua/ua/computer-zhestkie-diski/wd-red-plus-series/",  # WD Red Plus
    "https://hotline.ua/ua/computer-zhestkie-diski/seagate-ironwolf-series/",  # Seagate IronWolf
    "https://hotline.ua/ua/computer-zhestkie-diski/seagate-exos-x16-series/",  # Seagate Exos X16
    "https://hotline.ua/ua/computer-zhestkie-diski/toshiba-mg08-series/",  # Toshiba MG08
    "https://hotline.ua/ua/computer-zhestkie-diski/seagate-exos-x18-series/",  # Seagate Exos X18
    "https://hotline.ua/ua/computer-zhestkie-diski/wd-red-pro-series/",  # WD Red Pro
    "https://hotline.ua/ua/computer-zhestkie-diski/seagate-ironwolf-pro-series/",  # Seagate IronWolf Pro
    "https://hotline.ua/ua/computer-zhestkie-diski/wd-caviar-red-series/",  # WD Red
    "https://hotline.ua/ua/computer-zhestkie-diski/wd-gold-series/",  # WD Gold
    "https://hotline.ua/ua/computer-zhestkie-diski/synology-hat5300-series/",  # Synology HAT5300
    "https://hotline.ua/ua/computer-zhestkie-diski/seagate-exos-7e8-sata-series/",  # Seagate Exos 7E8 SATA
    "https://hotline.ua/ua/computer-zhestkie-diski/seagate-exos-7e10-series/",  # Seagate Exos 7E10
    "https://hotline.ua/ua/computer-zhestkie-diski/seagate-enterprise-capacity-3point5-hdd-series/",  # Seagate Enterprise Capacity 3.5 HDD
    "https://hotline.ua/ua/computer-zhestkie-diski/seagate-nas-hdd-series/",  # Seagate NAS HDD
    "https://hotline.ua/ua/computer-zhestkie-diski/seagate-exos-x14-sata-series/",  # Seagate Exos X14 SATA
    "https://hotline.ua/ua/computer-zhestkie-diski/toshiba-n300-series/"  # Toshiba N300
]

HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.68 Safari/537.36"
}


def get_html(url, params=""):
    response = requests.get(url, headers=HEADERS, params=params)
    return response


def get_content(html):
    soup = BeautifulSoup(html, "lxml")
    # soup.decode_contents()
    # print(soup.decode_contents())
    items = soup.find("tbody").find_all("tr")
    disks = []
    for item in items:
        disks.append(
            {
                "item": item.find("td").find("a").get_text(strip=True),
                "url": "https://hotline.ua" + item.find("td").find("a").get("href"),
                "price": item.find("td").find_next_sibling("td").find("span", class_="price__value").get_text(strip=True),
                "capacity": item.find("td").find_next_sibling("td").find_next_sibling("td").find_next_sibling("td").find_next_sibling("td").get_text(strip=True)

            }
        )
    return disks


# html = get_html(URL00)
# print(html.text)
# print(get_content(html.text))


def save_doc(items, path):
    with open(path, "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["item", "price", "capacity"])
        for item in items:
            writer.writerow([item["item"], item["price"], item["capacity"]])


disks = []
for url in urls:
    print("Parsing " + url)
    html = get_html(url)
    disks.extend(get_content(html.text))

# print("Parsing URL01")
# html = get_html(URL01)
# disks.extend(get_content(html.text))
# print("Parsing URL02")
# html = get_html(URL02)
# disks.extend(get_content(html.text))
# print("Parsing URL03")
# html = get_html(URL03)
# disks.extend(get_content(html.text))
# print("Parsing URL04")
# html = get_html(URL04)
# disks.extend(get_content(html.text))
# print("Parsing URL05")
# html = get_html(URL05)
# disks.extend(get_content(html.text))
# print("Parsing URL06")
# html = get_html(URL06)
# disks.extend(get_content(html.text))
# print("Parsing URL07")
# html = get_html(URL07)
# disks.extend(get_content(html.text))
# print("Parsing URL08")
# html = get_html(URL08)
# disks.extend(get_content(html.text))
# print("Parsing URL09")
# html = get_html(URL09)
# disks.extend(get_content(html.text))
# print("Parsing URL10")
# html = get_html(URL10)
# disks.extend(get_content(html.text))
# print("Parsing URL11")
# html = get_html(URL11)
# disks.extend(get_content(html.text))
# print("Parsing URL12")
# html = get_html(URL12)
# disks.extend(get_content(html.text))
# print("Parsing URL13")
# html = get_html(URL13)
# disks.extend(get_content(html.text))
# print("Parsing URL14")
# html = get_html(URL14)
# disks.extend(get_content(html.text))
# print("Parsing URL15")
# html = get_html(URL15)
# disks.extend(get_content(html.text))
# print("Saving doc...")
save_doc(disks, CSV)
