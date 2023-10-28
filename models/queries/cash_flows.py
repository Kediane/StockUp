CREATE_CASH_FLOW_TABLE = '''
CREATE TABLE IF NOT EXISTS cash_flow_reports (
        symbol TEXT NOT NULL,
        fiscalDateEnding TEXT NOT NULL,
        reportedCurrency TEXT NOT NULL,
        operatingCashflow REAL,
        paymentsForOperatingActivities REAL,
        proceedsFromOperatingActivities REAL,
        changeInOperatingLiabilities REAL,
        changeInOperatingAssets REAL,
        depreciationDepletionAndAmortization REAL,
        capitalExpenditures REAL,
        changeInReceivables REAL,
        changeInInventory REAL,
        profitLoss REAL,
        cashflowFromInvestment REAL,
        cashflowFromFinancing REAL,
        proceedsFromRepaymentsOfShortTermDebt REAL,
        paymentsForRepurchaseOfCommonStock REAL,
        paymentsForRepurchaseOfEquity REAL,
        paymentsForRepurchaseOfPreferredStock REAL,
        dividendPayout REAL,
        dividendPayoutCommonStock REAL,
        dividendPayoutPreferredStock REAL,
        proceedsFromIssuanceOfCommonStock REAL,
        proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet REAL,
        proceedsFromIssuanceOfPreferredStock REAL,
        proceedsFromRepurchaseOfEquity REAL,
        proceedsFromSaleOfTreasuryStock REAL,
        changeInCashAndCashEquivalents REAL,
        changeInExchangeRate REAL,
        netIncome REAL,
        period TEXT NOT NULL,
        UNIQUE (symbol, fiscalDateEnding, period),
        FOREIGN KEY (symbol)
        REFERENCES stocks (symbol)
);
'''

INSERT_CASH_FLOWS_TABLE = '''
INSERT OR IGNORE INTO cash_flow_reports VALUES (
?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
)
'''

SELECT_CASH_FLOW_REPORT_BY_SYMBOL = '''
SELECT * FROM cash_flow_reports WHERE symbol = ? LIMIT ? OFFSET ?;
'''

SELECT_CASH_FLOW_REPORT = '''
SELECT * FROM cash_flow_reports LIMIT ? OFFSET ?;
'''