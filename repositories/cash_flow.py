import asyncio
from sqlite3 import Connection

from models.queries.cash_flows import INSERT_CASH_FLOWS_TABLE, SELECT_CASH_FLOW_REPORT, \
    SELECT_CASH_FLOW_REPORT_BY_SYMBOL


class CashFlowRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    async def find_all(self, symbol='', limit=100, offset=0):
        return await asyncio.to_thread(lambda: self.find_all_sync(symbol, limit, offset))

    def find_all_sync(self, symbol='', limit=100, offset=0):
        cursor = self.conn.cursor()
        if symbol:
            res = cursor.execute(SELECT_CASH_FLOW_REPORT_BY_SYMBOL, (symbol, limit, offset))
        else:
            res = cursor.execute(SELECT_CASH_FLOW_REPORT, (limit, offset))
        return [
            {
                'symbol': record[0],
                'fiscalDateEnding': record[1],
                'reportedCurrency': record[2],
                'operatingCashflow': record[3],
                'paymentsForOperatingActivities': record[4],
                'proceedsFromOperatingActivities': record[5],
                'changeInOperatingLiabilities': record[6],
                'changeInOperatingAssets': record[7],
                'depreciationDepletionAndAmortization': record[8],
                'capitalExpenditures': record[9],
                'changeInReceivables': record[10],
                'changeInInventory': record[11],
                'profitLoss': record[12],
                'cashflowFromInvestment': record[13],
                'cashflowFromFinancing': record[14],
                'proceedsFromRepaymentsOfShortTermDebt': record[15],
                'paymentsForRepurchaseOfCommonStock': record[16],
                'paymentsForRepurchaseOfEquity': record[17],
                'paymentsForRepurchaseOfPreferredStock': record[18],
                'dividendPayout': record[19],
                'dividendPayoutCommonStock': record[20],
                'dividendPayoutPreferredStock': record[21],
                'proceedsFromIssuanceOfCommonStock': record[22],
                'proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet': record[23],
                'proceedsFromIssuanceOfPreferredStock': record[24],
                'proceedsFromRepurchaseOfEquity': record[25],
                'proceedsFromSaleOfTreasuryStock': record[26],
                'changeInCashAndCashEquivalents': record[27],
                'changeInExchangeRate': record[28],
                'netIncome': record[29],
                'period': record[30],
            }
            for record in res.fetchall()
        ]

    async def bulk_insert(self, statements: dict):
        await asyncio.to_thread(lambda: self._bulk_insert(statements))

    def _bulk_insert(self, statement: dict):
        cursor = self.conn.cursor()

        cursor.executemany(
            INSERT_CASH_FLOWS_TABLE,
            [
                [
                    statement['symbol'],
                    report['fiscalDateEnding'],
                    report['reportedCurrency'],
                    float(report['operatingCashflow']),
                    float(report['paymentsForOperatingActivities']),
                    float(report['proceedsFromOperatingActivities']),
                    float(report['changeInOperatingLiabilities']),
                    float(report['changeInOperatingAssets']),
                    float(report['depreciationDepletionAndAmortization']),
                    float(report['capitalExpenditures']),
                    float(report['changeInReceivables']),
                    float(report['changeInInventory']),
                    float(report['profitLoss']),
                    float(report['cashflowFromInvestment']),
                    float(report['cashflowFromFinancing']),
                    float(report['proceedsFromRepaymentsOfShortTermDebt']),
                    float(report['paymentsForRepurchaseOfCommonStock']),
                    float(report['paymentsForRepurchaseOfEquity']),
                    float(report['paymentsForRepurchaseOfPreferredStock']),
                    float(report['dividendPayout']),
                    float(report['dividendPayoutCommonStock']),
                    float(report['dividendPayoutPreferredStock']),
                    float(report['proceedsFromIssuanceOfCommonStock']),
                    float(report['proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet']),
                    float(report['proceedsFromIssuanceOfPreferredStock']),
                    float(report['proceedsFromRepurchaseOfEquity']),
                    float(report['proceedsFromSaleOfTreasuryStock']),
                    float(report['changeInCashAndCashEquivalents']),
                    float(report['changeInExchangeRate']),
                    float(report['netIncome']),
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
