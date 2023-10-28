CREATE_EARNINGS_STATEMENT_TABLE = '''
CREATE TABLE IF NOT EXISTS earning_statements (
        symbol TEXT NOT NULL,
        fiscalDateEnding TEXT NOT NULL,
        reportedEPS REAL NOT NULL ,
        reportedDate TEXT,
        estimatedEPS REAL,
        surprise REAL,
        surprisePercentage REAL,
        period TEXT NOT NULL,
        UNIQUE (symbol, fiscalDateEnding, period),
            FOREIGN KEY (symbol)
                REFERENCES stocks (symbol)
);
'''
INSERT_EARNINGS_STATEMENTS_TABLE = '''
INSERT OR IGNORE INTO earning_statements VALUES (
?, ?, ?, ?, ?, ?, ?, ?
)
'''
SELECT__EARNINGS_STATEMENT_BY_SYMBOL = '''
SELECT * FROM earning_statements WHERE symbol = ? LIMIT ? OFFSET ?;
'''

SELECT_EARNINGS_STATEMENT = '''
SELECT * FROM earning_statements LIMIT ? OFFSET ?;
'''