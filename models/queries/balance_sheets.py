CREATE_BALANCE_SHEET_TABLE = '''
CREATE TABLE IF NOT EXISTS balance_sheets(
        symbol TEXT NOT NULL, 
        fiscalDateEnding TEXT NOT NULL,
        reportedCurrency TEXT NOT NULL,
        totalAssets REAL,
        totalCurrentAssets REAL,
        cashAndCashEquivalentsAtCarryingValue REAL,
        cashAndShortTermInvestments REAL,
        inventory REAL,
        currentNetReceivables REAL,
        totalNonCurrentAssets REAL,
        propertyPlantEquipment REAL,
        accumulatedDepreciationAmortizationPPE REAL,
        intangibleAssets REAL,
        intangibleAssetsExcludingGoodwill REAL,
        goodwill REAL,
        investments REAL,
        longTermInvestments REAL,
        shortTermInvestments REAL,
        otherCurrentAssets REAL,
        otherNonCurrentAssets REAL,
        totalLiabilities REAL,
        totalCurrentLiabilities REAL,
        currentAccountsPayable REAL,
        deferredRevenue REAL,
        currentDebt REAL,
        shortTermDebt REAL,
        totalNonCurrentLiabilities REAL,
        capitalLeaseObligations REAL,
        longTermDebt REAL,
        currentLongTermDebt REAL,
        longTermDebtNoncurrent REAL,
        shortLongTermDebtTotal REAL,
        otherCurrentLiabilities REAL,
        otherNonCurrentLiabilities REAL,
        totalShareholderEquity REAL,
        treasuryStock REAL,
        retainedEarnings REAL,
        commonStock REAL,
        commonStockSharesOutstanding REAL,
        period TEXT NOT NULL,
        UNIQUE (symbol, fiscalDateEnding, period),
            FOREIGN KEY (symbol) 
                REFERENCES stocks (symbol)
);
'''
INSERT_BALANCE_SHEETS_TABLE = '''
INSERT OR IGNORE INTO balance_sheets VALUES (
?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
)
'''

SELECT_BALANCE_SHEET_BY_SYMBOL = '''
SELECT * FROM balance_sheets WHERE symbol = ? LIMIT ? OFFSET ?;
'''

SELECT_BALANCE_SHEET = '''
SELECT * FROM balance_sheets LIMIT ? OFFSET ?;
'''