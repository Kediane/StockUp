import asyncio
from sqlite3 import Connection

from models.queries.balance_sheets import INSERT_BALANCE_SHEETS_TABLE, SELECT_BALANCE_SHEET, \
    SELECT_BALANCE_SHEET_BY_SYMBOL


class BalanceSheetRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    def find_all(self, symbol='', limit=100, offset=0):
        cursor = self.conn.cursor()
        if symbol:
            res = cursor.execute(SELECT_BALANCE_SHEET_BY_SYMBOL, (symbol, limit, offset))
        else:
            res = cursor.execute(SELECT_BALANCE_SHEET, (limit, offset))
        return [
            {
                'symbol': record[0],
                'fiscalDateEnding': record[1],
                'reportedCurrency': record[2],
                'totalAssets': record[3],
                'totalCurrentAssets': record[4],
                'cashAndCashEquivalentsAtCarryingValue': record[5],
                'cashAndShortTermInvestments': record[6],
                'inventory': record[7],
                'currentNetReceivables': record[8],
                'totalNonCurrentAssets': record[9],
                'propertyPlantEquipment': record[10],
                'accumulatedDepreciationAmortizationPPE': record[11],
                'intangibleAssets': record[12],
                'intangibleAssetsExcludingGoodwill': record[13],
                'goodwill': record[14],
                'investments': record[15],
                'longTermInvestments': record[16],
                'shortTermInvestments': record[17],
                'otherCurrentAssets': record[18],
                'otherNonCurrentAssets': record[19],
                'totalLiabilities': record[20],
                'totalCurrentLiabilities': record[21],
                'currentAccountsPayable': record[22],
                'deferredRevenue': record[23],
                'currentDebt': record[24],
                'shortTermDebt': record[25],
                'totalNonCurrentLiabilities': record[26],
                'capitalLeaseObligations': record[27],
                'longTermDebt': record[28],
                'currentLongTermDebt': record[29],
                'longTermDebtNoncurrent': record[30],
                'shortLongTermDebtTotal': record[31],
                'otherCurrentLiabilities': record[32],
                'otherNonCurrentLiabilities': record[33],
                'totalShareholderEquity': record[34],
                'treasuryStock': record[35],
                'retainedEarnings': record[36],
                'commonStock': record[37],
                'commonStockSharesOutstanding': record[38],
                'period': record[39],
            }
            for record in res.fetchall()
        ]

    def bulk_insert(self, statement: dict):
        cursor = self.conn.cursor()

        cursor.executemany(
            INSERT_BALANCE_SHEETS_TABLE,
            [
                [
                    statement['symbol'],
                    report['fiscalDateEnding'],
                    report['reportedCurrency'],
                    float(report['totalAssets']),
                    float(report['totalCurrentAssets']),
                    float(report['cashAndCashEquivalentsAtCarryingValue']),
                    float(report['cashAndShortTermInvestments']),
                    float(report['inventory']),
                    float(report['currentNetReceivables']),
                    float(report['totalNonCurrentAssets']),
                    float(report['propertyPlantEquipment']),
                    float(report['accumulatedDepreciationAmortizationPPE']),
                    float(report['intangibleAssets']),
                    float(report['intangibleAssetsExcludingGoodwill']),
                    float(report['goodwill']),
                    float(report['investments']),
                    float(report['longTermInvestments']),
                    float(report['shortTermInvestments']),
                    float(report['otherCurrentAssets']),
                    float(report['otherNonCurrentAssets']),
                    float(report['totalLiabilities']),
                    float(report['totalCurrentLiabilities']),
                    float(report['currentAccountsPayable']),
                    float(report['deferredRevenue']),
                    float(report['currentDebt']),
                    float(report['shortTermDebt']),
                    float(report['totalNonCurrentLiabilities']),
                    float(report['capitalLeaseObligations']),
                    float(report['longTermDebt']),
                    float(report['currentLongTermDebt']),
                    float(report['longTermDebtNoncurrent']),
                    float(report['shortLongTermDebtTotal']),
                    float(report['otherCurrentLiabilities']),
                    float(report['otherNonCurrentLiabilities']),
                    float(report['totalShareholderEquity']),
                    float(report['treasuryStock']),
                    float(report['retainedEarnings']),
                    float(report['commonStock']),
                    float(report['commonStockSharesOutstanding']),
                    report_type
                ]
                for report_type in ('annualReports', 'quarterlyReports')
                for report in [
                {key: (value if value != 'None' else '0') for key, value in item.items()}
                for item in statement.get(report_type, [])
            ]
            ]
        )
        self.conn.commit()
