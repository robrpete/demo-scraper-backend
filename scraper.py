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


def scrape_info():
    try:
        response = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table")
        if not table:
            raise ValueError("Error: No table found!")

        header_row = table.find("thead").find("tr").find_all("th")
        header_names = [header.get_text(strip=True) for header in header_row]

        header_map = {}
        data_index = 0
        for header in header_names:
            if header == "":
                data_index += 1
                continue
            header_map[header] = data_index
            data_index += 1
        print(header_map)
        prices = []

        for tr in table.find_all("tr"):
            cells = tr.find_all("td")
            row = [cell.get_text(strip=True) for cell in cells]
            if row:  # skip empty rows
                price_data = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M-%S"),
                    "Ticker": row[header_map["Symbol"]] if "Symbol" in header_map else "",
                    "Name": row[header_map["Name"]] if "Name" in header_map else "",
                    "Price": row[header_map["Price"]] if "Price" in header_map else "",
                    "Change": row[header_map["Change"]] if "Change" in header_map else "",
                    "Change%": row[header_map["Change %"]] if "Change %" in header_map else "",
                    "Volume": row[header_map["Volume"]] if "Volume" in header_map else "",
                    "av": row[header_map["Avg Vol (3M)"]] if "Avg Vol (3M)" in header_map else "",
                    "mc": row[header_map["Market Cap"]] if "Market Cap" in header_map else "",
                    "per": row[header_map["P/E Ratio(TTM)"]] if "P/E Ratio(TTM)" in header_map else "",
                    "52w": row[header_map["52 WkChange %"]] if "52 WkChange %" in header_map else "",
                }

                # try:
                #     if price_data["Price"]:
                #         # price_data["Price"] = float(
                #         #     price_data["Price"].split()[0])
                #         print(price_data["Price"])

                # except (ValueError, IndexError) as e:
                #     print(f"Error parsing data for row {row}: {e}")

                prices.append(price_data)

        for index, p in enumerate(prices):
            #     # print(p["Ticker"] + " " + p["Name"] + " " + p["Price"] + " " + p["Change"] + " " + p["Change%"] +
            #     #       " " + p["Volume"] + " " + p["av"] + " " + p["mc"] + " " + p["per"] + " " + p["52w"])
            print(p)
            print("")
            if index == 3:
                break

    except Exception as e:
        print(f"Error getting data: {e}")


if __name__ == "__main__":
    scrape_info()


# prices = []
#     for item in soup.select(".thumbnail"):
#         name = item.select_one(".title").get_text(strip=True)
#         price = item.select_one(".price").get_text(strip=True)
#         rating = item.select_one(".ratings p[data-rating]")["data-rating"]
#         link = "https://webscraper.io" + item.select_one(".title")["href"]
# streamlit cloud
