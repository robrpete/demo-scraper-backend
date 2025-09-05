import sqlite3
from schemas import STOCKS_TABLE_SQL, STOCK_DETAILS_TABLE_SQL
from datetime import datetime


def init_db(db_path="stocks.db"):
    """Initialize the database and create tables if they don't exist."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(STOCKS_TABLE_SQL)
        cursor.execute(STOCK_DETAILS_TABLE_SQL)
        conn.commit()
        print("Database initialized.")
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()


def save_to_db(prices, db_path="stocks.db"):
    """Save a list of price dictionaries from scrape_prices to the stocks table."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        for price in prices:
            cursor.execute("""
                INSERT INTO stocks (
                    timestamp, ticker, name, price, change, change_percent,
                    volume, avg_vol, market_cap, pe_ratio, _52w_change
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                price.get("timestamp"),
                price.get("ticker"),
                price.get("name"),
                price.get("price"),
                price.get("change"),
                price.get("change_percent"),
                price.get("volume"),
                price.get("avg_vol"),
                price.get("market_cap"),
                price.get("pe_ratio"),
                price.get("52w_change")
            ))
        conn.commit()
        print(f"Saved {len(prices)} records to stocks table.")
    except sqlite3.Error as e:
        print(f"Error saving to stocks table: {e}")
    finally:
        conn.close()


def save_to_db_details(data, ticker, db_path="stocks.db"):
    """Save label-value pairs from scrape_one to the stock_details table."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Map original labels to database column names
        label_map = {
            "Previous Close": "PrevClose",
            "Open": "Open",
            "Bid": "Bid",
            "Ask": "Ask",
            "Day's Range": "DayRange",
            "52 Week Range": "Week52Range",
            "Volume": "Volume",
            "Avg. Volume": "AvgVolume",
            "Market Cap (intraday)": "MarketCap",
            "Beta (5Y Monthly)": "Beta5Y",
            "PE Ratio (TTM)": "PERatio",
            "EPS (TTM)": "EPS",
            "Earnings Date": "EarningsDate",
            "Forward Dividend & Yield": "DividendYield",
            "Ex-Dividend Date": "ExDividendDate",
            "1y Target Est": "TargetEst1Y"
        }
        # Convert zip object to dict for easier column mapping
        price_data = {label_map.get(label, label)
                                    : value for label, value in data}
        cursor.execute("""
            INSERT INTO stock_details (
                timestamp, ticker, PrevClose, Open, Bid, Ask, DayRange,
                Week52Range, Volume, AvgVolume, MarketCap, Beta5Y, PERatio,
                EPS, EarningsDate, DividendYield, ExDividendDate, TargetEst1Y
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            timestamp,
            ticker,
            price_data.get("PrevClose"),
            price_data.get("Open"),
            price_data.get("Bid"),
            price_data.get("Ask"),
            price_data.get("DayRange"),
            price_data.get("Week52Range"),
            price_data.get("Volume"),
            price_data.get("AvgVolume"),
            price_data.get("MarketCap"),
            price_data.get("Beta5Y"),
            price_data.get("PERatio"),
            price_data.get("EPS"),
            price_data.get("EarningsDate"),
            price_data.get("DividendYield"),
            price_data.get("ExDividendDate"),
            price_data.get("TargetEst1Y")
        ))
        conn.commit()
        print(f"Saved details for {ticker} to stock_details table.")
    except sqlite3.Error as e:
        print(f"Error saving to stock_details table: {e}")
    finally:
        conn.close()


def get_current_day_stocks(db_path="stocks.db"):
    """Fetch all stock data from the stocks table for the current day."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        current_day = datetime.now().strftime("%Y-%m-%d")
        cursor.execute(
            "SELECT * FROM stocks WHERE timestamp LIKE ?", (f"{current_day}%",))
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        result = [dict(zip(columns, row)) for row in rows]
        return result
    except sqlite3.Error as e:
        print(f"Error fetching current day stocks: {e}")
        return []
    finally:
        conn.close()


def get_one_stock_details(ticker, timestamp, db_path="stocks.db"):
    """Fetch stock_details for a specific ticker and timestamp."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM stock_details WHERE ticker = ? AND timestamp = ?
        """, (ticker, timestamp))
        columns = [desc[0] for desc in cursor.description]
        row = cursor.fetchone()
        return dict(zip(columns, row)) if row else {}
    except sqlite3.Error as e:
        print(f"Error fetching stock details for {ticker} at {timestamp}: {e}")
        return {}
    finally:
        conn.close()
