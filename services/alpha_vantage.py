from aiohttp import ClientSession
from aiohttp_retry import RetryClient


class AlphaVantageService:
    def __init__(self, api_key: str, client_session: ClientSession):
        self.api_key = api_key
        self.domain = 'https://www.alphavantage.co'
        self.retry_client = RetryClient(client_session=client_session)

    async def fetch_symbol_ticker(self, keyterm: str):
        return await self._fetch_data('SYMBOL_SEARCH', keyterm, 'keywords')

    async def fetch_income_statement(self, symbol: str) -> dict:
        return await self._fetch_data('INCOME_STATEMENT', symbol)

    async def fetch_ticker_listing(self):
        data: str = await self._fetch_data('LISTING_STATUS', is_json=False)
        rows: list[list[str]] = [item.split(',') for item in data.split('\n')]
        rows.pop(0)
        rows.pop()

        return [
            {
                'symbol': row[0],
                'name': row[1],
                'exchange': row[2],
                'assetType': row[3],
                'ipoDate': row[4]
            }
            for row in rows
            if row[6].strip() == 'Active'
        ]

    async def fetch_balance_sheet(self, symbol: str):
        return await self._fetch_data('BALANCE_SHEET', symbol)

    async def fetch_cash_flow(self, symbol: str):
        return await self._fetch_data('CASH_FLOW', symbol)

    async def fetch_earnings(self, symbol: str):
        return await self._fetch_data('EARNINGS', symbol)

    async def _fetch_data(
            self,
            functor: str,
            term: str | None = None,
            term_name: str = 'symbol',
            is_json: bool = True
    ):
        url = f'{self.domain}/query?function={functor}&apikey={self.api_key}'

        if term is not None:
            url += f'&{term_name}={term}'

        async with self.retry_client.get(url) as response:
            if not response.ok:
                raise LookupError(f'Failed to lookup {functor} for symbol {term}')

            if is_json:
                return await response.json()
            else:
                return await response.text()
