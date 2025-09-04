from scraper import scrape_info, scrape_one
if __name__ == "__main__":
    prices = scrape_info()

    for index, p in enumerate(prices):
        print(str(index + 1) + " " + p["Ticker"] + " " + p["Name"] + " " + p["Price"] + " " + p["Change"] + " " + p["Change%"] +
              " " + p["Volume"] + " " + p["av"] + " " + p["mc"] + " " + p["per"] + " " + p["52w"] + " " + p["timestamp"])

        print("")

    one = scrape_one("OPEN")
    for label, value in one:
        print(label, value)
