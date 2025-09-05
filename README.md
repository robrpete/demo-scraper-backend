# Python Web Scraper

## Packages Used

- `requests`: For making HTTP requests to fetch web pages.
- `beautifulsoup4`: For parsing HTML content from Yahoo Finance.
- `fastapi`: For creating API endpoints to access stock data.
- `uvicorn`: ASGI server to run the FastAPI application.
- `apscheduler`: For scheduling daily scraping tasks.

## Description

- A FastAPI-based web scraper that collects stock data from Yahoo Finance. It scrapes the most-active stocks daily and stores them in a SQLite database (`stocks` table).
- It also allows scraping detailed metrics for a specific stock (`stock_details` table) via an API endpoint.
- The project demonstrates efficient data storage with batch inserts and is designed for small-scale deployment on platforms like PythonAnywhere or Streamlit Cloud.

## Setup

1. Create and activate a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Run the FastAPI app:

   ```
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## API Endpoints

- `GET /all_stocks`: Returns all most active stock data for that day from the `stocks` table.
- `GET /stock_info/{ticker}`: Scrapes and saves detailed metrics for a specific stock.

## Database

- **SQLite**: Uses `stocks.db` with two tables:
  - `stocks`: Stores stocks daily data from yahoo's most-active stocks page (e.g., `ticker`, `price`, `volume`).
  - `stock_details`: Stores detailed metrics for individual stocks (e.g., `PrevClose`, `Open`, `Bid`).
- **Schema**: Defined in `schema.py`

## Notes

- **Scraping Schedule**: Daily scrape of most-active stocks runs at 08:00 EDT.
