import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# target url
URL = "https://finance.yahoo.com/markets/stocks/most-active/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0 Safari/537.36"
}


def scrape_prices():
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    prices = []
    for tr in table.find_all("tr"):
        cells = tr.find_all("td")
        row = [cell.get_text(strip=True) for cell in cells]
        if row:  # skip empty rows
            prices.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M-%S"),
                "ticker": row[0],
                "name": row[1],
                "price": row[3],
                "change": row[4],
                "change%": row[5],
                "volume": row[6],
                "avg vol": row[7],
                "mc": row[8],
                "p/e": row[9],
                "52w": row[10],
            })

    for p in prices:
        print(p)
        print("")


if __name__ == "__main__":
    scrape_prices()

# streamlit cloud


# prices = []
#     for item in soup.select(".thumbnail"):
#         name = item.select_one(".title").get_text(strip=True)
#         price = item.select_one(".price").get_text(strip=True)
#         rating = item.select_one(".ratings p[data-rating]")["data-rating"]
#         link = "https://webscraper.io" + item.select_one(".title")["href"]

#         prices.append({
#             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M-%S"),
#             "name": name,
#             "price": price,
#             "rating": rating,
#             "url": link
#         })
