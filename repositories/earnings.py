from datetime import datetime
from sqlite3 import Connection

from models.queries.earnings_statements import INSERT_EARNINGS_STATEMENTS_TABLE, SELECT_EARNINGS_STATEMENT, \
    SELECT__EARNINGS_STATEMENT_BY_SYMBOL


class EarningsRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    def find_all(self, symbol='', limit=100, offset=0):
        cursor = self.conn.cursor()
        if symbol:
            res = cursor.execute(SELECT__EARNINGS_STATEMENT_BY_SYMBOL, (symbol, limit, offset))
        else:
            res = cursor.execute(SELECT_EARNINGS_STATEMENT, (limit, offset))
        return [
            {
                'symbol': record[0],
                'fiscalDateEnding': datetime.strptime(record[1], '%Y-%m-%d'),
                'reportedEPS': record[2],
                'reportedDate': record[3],
                'estimatedEPS': record[4],
                'surprise': record[5],
                'surprisePercentage': record[6],
                'period': record[7]
            }
            for record in res.fetchall()
        ]

    def bulk_insert(self, statement: dict):
        cursor = self.conn.cursor()

        cursor.executemany(
            INSERT_EARNINGS_STATEMENTS_TABLE,
            [
                [
                    statement['symbol'],
                    report['fiscalDateEnding'],
                    report['reportedEPS'],
                    report.get('reportedDate'),
                    float(report.get('estimatedEPS', 0)),
                    float(report.get('surprise', 0)),
                    float(report.get('surprisePercentage', 0)),
                    report_type
                ]
                for report_type in ('quarterlyEarnings', 'annualEarnings')
                for report in [
                {key: (value if value != 'None' else '0') for key, value in item.items()}
                for item in statement.get(report_type, [])
            ]
            ]
        )
        self.conn.commit()
