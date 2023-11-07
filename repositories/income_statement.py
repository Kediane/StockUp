from datetime import datetime
from sqlite3 import Connection

from models.queries.Income_statements import INSERT_INCOME_STATEMENTS_TABLE, SELECT_INCOME_STATEMENT, \
    SELECT__INCOME_STATEMENT_BY_SYMBOL


class IncomeStatementRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    def find_all(self, symbol='', limit=100, offset=0):
        cursor = self.conn.cursor()
        if symbol:
            res = cursor.execute(SELECT__INCOME_STATEMENT_BY_SYMBOL, (symbol, limit, offset))
        else:
            res = cursor.execute(SELECT_INCOME_STATEMENT, (limit, offset))
        return [
            {
                'symbol': record[0],
                'fiscalDateEnding': datetime.strptime(record[1], '%Y-%m-%d'),
                'reportedCurrency': record[2],
                'grossProfit': record[3],
                'totalRevenue': record[4],
                'costOfRevenue': record[5],
                'costofGoodsAndServicesSold': record[6],
                'operatingIncome': record[7],
                'sellingGeneralAndAdministrative': record[8],
                'researchAndDevelopment': record[9],
                'operatingExpenses': record[10],
                'investmentIncomeNet': record[11],
                'netInterestIncome': record[12],
                'interestIncome': record[13],
                'interestExpense': record[14],
                'nonInterestIncome': record[15],
                'otherNonOperatingIncome': record[16],
                'depreciation': record[17],
                'depreciationAndAmortization': record[18],
                'incomeBeforeTax': record[19],
                'incomeTaxExpense': record[20],
                'interestAndDebtExpense': record[21],
                'netIncomeFromContinuingOperations': record[22],
                'comprehensiveIncomeNetOfTax': record[23],
                'ebit': record[24],
                'ebitda': record[25],
                'netIncome': record[26],
                'report_type': record[27]
            }
            for record in res.fetchall()
        ]

    def bulk_insert(self, statement: dict):
        cursor = self.conn.cursor()

        data = [
            [
                statement['symbol'],
                report['fiscalDateEnding'],
                report['reportedCurrency'],
                float(report['grossProfit']),
                float(report['totalRevenue']),
                float(report['costOfRevenue']),
                float(report['costofGoodsAndServicesSold']),
                float(report['operatingIncome']),
                float(report['sellingGeneralAndAdministrative']),
                float(report['researchAndDevelopment']),
                float(report['operatingExpenses']),
                float(report['investmentIncomeNet']),
                float(report['netInterestIncome']),
                float(report['interestIncome']),
                float(report['interestExpense']),
                float(report['nonInterestIncome']),
                float(report['otherNonOperatingIncome']),
                float(report['depreciation']),
                float(report['depreciationAndAmortization']),
                float(report['incomeBeforeTax']),
                float(report['incomeTaxExpense']),
                float(report['interestAndDebtExpense']),
                float(report['netIncomeFromContinuingOperations']),
                float(report['comprehensiveIncomeNetOfTax']),
                float(report['ebit']),
                float(report['ebitda']),
                float(report['netIncome']),
                report_type
            ]
            for report_type in ('annualReports', 'quarterlyReports')
            for report in [
                {key: (value if value != 'None' else '0') for key, value in item.items()}
                for item in statement.get(report_type, [])
            ]
        ]
        cursor.executemany(
            INSERT_INCOME_STATEMENTS_TABLE,
            data
        )
        self.conn.commit()
