STOCKS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    ticker TEXT,
    name TEXT,
    price REAL,
    change TEXT,
    change_percent TEXT,
    volume REAL,
    avg_vol TEXT,
    market_cap TEXT,
    pe_ratio TEXT,
    _52w_change TEXT
)
"""

STOCK_DETAILS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS stock_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    ticker TEXT,
    PrevClose TEXT,
    Open TEXT,
    Bid TEXT,
    Ask TEXT,
    DayRange TEXT,
    Week52Range TEXT,
    Volume TEXT,
    AvgVolume TEXT,
    MarketCap TEXT,
    Beta5Y TEXT,
    PERatio TEXT,
    EPS TEXT,
    EarningsDate TEXT,
    DividendYield TEXT,
    ExDividendDate TEXT,
    TargetEst1Y TEXT
)
"""
