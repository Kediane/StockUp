CREATE_STOCKS_TABLE = '''
CREATE TABLE IF NOT EXISTS stocks (
    symbol TEXT NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    icon TEXT
);
'''

INSERT_STOCK = '''
INSERT OR IGNORE INTO stocks (symbol, name, icon)
VALUES (?, ?, ?)
'''

SELECT_STOCK_BY_SYMBOL = '''
SELECT * FROM stocks WHERE symbol = ?;
'''

SELECT_STOCKS = '''
SELECT * FROM stocks LIMIT ? OFFSET ?;
'''

SELECT_STOCKS_BY_KEYWORD = '''
SELECT DISTINCT * FROM stocks WHERE instr(lower(symbol), lower(?)) > 0 OR instr(lower(name), lower(?)) > 0 
LIMIT ? OFFSET ?;
'''