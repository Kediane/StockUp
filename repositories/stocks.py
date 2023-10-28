import asyncio
from sqlite3 import Connection

from models.queries.stocks import INSERT_STOCK, SELECT_STOCKS, SELECT_STOCKS_BY_KEYWORD


class StockRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    async def find_all(self, keyword='', limit=100, offset=0):
        return await asyncio.to_thread(lambda: self.find_all_sync(keyword, limit, offset))

    def find_all_sync(self, keyword='', limit=100, offset=0):
        cursor = self.conn.cursor()
        if keyword:
            res = cursor.execute(SELECT_STOCKS_BY_KEYWORD, (keyword, keyword, limit, offset))
        else:
            res = cursor.execute(SELECT_STOCKS, (limit, offset))
        return [
            {
                'symbol': record[0],
                'name': record[1]
            }
            for record in res.fetchall()
        ]

    async def bulk_insert(self, statements: dict):
        await asyncio.to_thread(lambda: self._bulk_insert(statements))

    def _bulk_insert(self, statements: list[dict]):
        cursor = self.conn.cursor()

        cursor.executemany(
            INSERT_STOCK,
            [
                [
                    statement['symbol'],
                    statement['name'],
                    None
                ]
                for statement in statements
            ]
        )
        self.conn.commit()
