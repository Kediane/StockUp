import requests as rq


class AlphaVantageService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.domain = 'https://www.alphavantage.co'

    def fetch_symbol_ticker(self, keyterm: str):
        return self._fetch_data('SYMBOL_SEARCH', keyterm, 'keywords')

    def fetch_income_statement(self, symbol: str) -> dict:
        return self._fetch_data('INCOME_STATEMENT', symbol)

    def fetch_ticker_listing(self):
        data: str = self._fetch_data('LISTING_STATUS', is_json=False)
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

    def fetch_balance_sheet(self, symbol: str):
        return self._fetch_data('BALANCE_SHEET', symbol)

    def fetch_cash_flow(self, symbol: str):
        return self._fetch_data('CASH_FLOW', symbol)

    def fetch_earnings(self, symbol: str):
        return self._fetch_data('EARNINGS', symbol)

    def _fetch_data(
            self,
            functor: str,
            term: str | None = None,
            term_name: str = 'symbol',
            is_json: bool = True
    ):
        url = f'{self.domain}/query?function={functor}&apikey={self.api_key}'

        if term is not None:
            url += f'&{term_name}={term}'

        response = rq.get(url)
        if not response.ok:
            raise LookupError(f'Failed to lookup {functor} for symbol {term}')

        if is_json:
            return response.json()
        else:
            return response.text
