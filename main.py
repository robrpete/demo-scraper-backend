from fastapi import FastAPI, HTTPException
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from scraper import scrape_info, scrape_one
from database import init_db, save_to_db, save_to_db_details, get_current_day_stocks, get_one_stock_details
from contextlib import asynccontextmanager
from datetime import datetime


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database and scheduler
    try:
        init_db()
    except Exception as e:
        print(f"Error initializing database: {e}")

    scheduler = AsyncIOScheduler()

    def scrape_and_save():
        """Scrape most-active stocks and save to database."""
        try:
            prices = scrape_info()
            if prices:
                save_to_db(prices)
            else:
                print("No data scraped from scrape_info")
        except Exception as e:
            print(f"Error in scrape_and_save: {e}")

    try:
        scheduler.add_job(
            scrape_and_save,
            trigger=CronTrigger(hour=8, minute=0, timezone="America/New_York")
        )
        scheduler.start()
    except Exception as e:
        print(f"Error setting up scheduler: {e}")

    yield  # Application runs here

    # Shutdown: Stop scheduler
    try:
        scheduler.shutdown()
    except Exception as e:
        print(f"Error shutting down scheduler: {e}")

app = FastAPI(lifespan=lifespan)


@app.get("/stocks/today")
async def get_today_stocks():
    """Return all stock data from the stocks table for the current day."""
    try:
        stocks = get_current_day_stocks()
        if not stocks:
            raise HTTPException(
                status_code=404, detail="No stocks found for today")
        return stocks
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching today's stocks: {str(e)}")


@app.get("/stocks/details/{ticker}/{timestamp}")
async def get_stock_details(ticker: str, timestamp: str):
    """Return stock details for a specific ticker and timestamp."""
    try:
        details = get_one_stock_details(ticker, timestamp)
        if not details:
            raise HTTPException(
                status_code=404, detail=f"No details found for ticker {ticker} at {timestamp}")
        return details
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching stock details: {str(e)}")


@app.get("/stocks/scrape-most-active")
async def scrape_most_active():
    """Scrape most-active stocks and save to database for testing purposes."""
    try:
        prices = scrape_info()
        for p in prices:
            print(p)
        if prices:
            save_to_db(prices)
            return f"Successfully scraped and saved {len(prices)} stocks"
        else:
            raise HTTPException(status_code=404, detail="No stocks scraped")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error scraping most-active stocks: {str(e)}")

# from scraper import scrape_info, scrape_one
# if __name__ == "__main__":
#     prices = scrape_info()

#     for index, p in enumerate(prices):
#         print(str(index + 1) + " " + p["Ticker"] + " " + p["Name"] + " " + p["Price"] + " " + p["Change"] + " " + p["Change%"] +
#               " " + p["Volume"] + " " + p["av"] + " " + p["mc"] + " " + p["per"] + " " + p["52w"] + " " + p["timestamp"])

#         print("")

#     one = scrape_one("OPEN")
#     for label, value in one:
#         print(label, value)
