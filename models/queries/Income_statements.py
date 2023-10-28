CREATE_INCOME_STATEMENT_TABLE = '''
CREATE TABLE IF NOT EXISTS income_statements (
        symbol TEXT NOT NULL,
        fiscalDateEnding TEXT NOT NULL,
        reportedCurrency TEXT NOT NULL ,
        grossProfit REAL,
        totalRevenue REAL,
        costOfRevenue REAL,
        costofGoodsAndServicesSold REAL,
        operatingIncome REAL,
        sellingGeneralAndAdministrative REAL,
        researchAndDevelopment REAL,
        operatingExpenses REAL,
        investmentIncomeNet REAL,
        netInterestIncome REAL,
        interestIncome REAL,
        interestExpense REAL,
        nonInterestIncome REAL,
        otherNonOperatingIncome REAL,
        depreciation REAL,
        depreciationAndAmortization REAL,
        incomeBeforeTax REAL,
        incomeTaxExpense REAL,
        interestAndDebtExpense REAL,
        netIncomeFromContinuingOperations REAL,
        comprehensiveIncomeNetOfTax REAL,
        ebit REAL,
        ebitda REAL,
        netIncome REAL,
        period TEXT NOT NULL,
        UNIQUE (symbol, fiscalDateEnding, period),
            FOREIGN KEY (symbol)
                REFERENCES stocks (symbol)
);
'''
INSERT_INCOME_STATEMENTS_TABLE = '''
INSERT OR IGNORE INTO income_statements VALUES (
?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
)
'''
SELECT__INCOME_STATEMENT_BY_SYMBOL = '''
SELECT * FROM income_statements WHERE symbol = ? LIMIT ? OFFSET ?;
'''

SELECT_INCOME_STATEMENT = '''
SELECT * FROM income_statements LIMIT ? OFFSET ?;
'''