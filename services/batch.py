import asyncio
import json
import logging
from asyncio import TaskGroup, Lock
from typing import Sequence

from more_itertools import batched

from repositories.balance_sheet import BalanceSheetRepository
from repositories.cash_flow import CashFlowRepository
from repositories.earnings import EarningsRepository
from repositories.income_statement import IncomeStatementRepository
from repositories.stocks import StockRepository
from services.alpha_vantage import AlphaVantageService


class BatchService:
    LOGGER = logging.getLogger(__name__)

    def __init__(
            self,
            alpha_vantage: AlphaVantageService,
            income_statement_repo: IncomeStatementRepository,
            balance_sheet_repo: BalanceSheetRepository,
            cash_flow_repo: CashFlowRepository,
            earnings_repo: EarningsRepository,
            stock_repo: StockRepository,
            schedule_period_hr: float,
            batch_size: int
    ):
        self.alpha_vantage = alpha_vantage
        self.schedule_period_hr = schedule_period_hr
        self.income_statement_repo = income_statement_repo
        self.balance_sheet_repo = balance_sheet_repo
        self.cash_flow_repo = cash_flow_repo
        self.stock_repo = stock_repo
        self.earnings_repo = earnings_repo
        self.lock = Lock()
        self.batch_size = batch_size

    async def run(self):
        while True:
            self.LOGGER.info('Scheduling batch job')
            try:
                await self._schedule_batch()
            except Exception as e:
                print(e)
            await asyncio.sleep(self.schedule_period_hr * 60 * 60)

    async def _schedule_batch(self):
        self.LOGGER.info('fetching symbols...')
        ticker_listing = await self.alpha_vantage.fetch_ticker_listing()
        symbols = [ticker['symbol'] for ticker in ticker_listing]

        await self.stock_repo.bulk_insert(ticker_listing)

        for chunk in batched(symbols, self.batch_size):
            async with TaskGroup() as group:
                group.create_task(self._fetch_income_statements(chunk))
                group.create_task(self._fetch_balance_sheets(chunk))
                group.create_task(self._fetch_earnings(chunk))
                group.create_task(self._fetch_cash_flows(chunk))

    async def _fetch_income_statements(self, symbols: Sequence[str]):
        async with TaskGroup() as group:
            for symbol in symbols:
                self.LOGGER.info(f'fetching {symbol} income statements...')
                group.create_task(self._store_income_statements(symbol))

    async def _store_income_statements(self, symbol: str):
        data = await self.alpha_vantage.fetch_income_statement(symbol)
        self.LOGGER.info(f'fetch completed - {symbol} income statements...')
        async with self.lock:
            await self.income_statement_repo.bulk_insert(data)

    async def _fetch_balance_sheets(self, symbols: Sequence[str]):
        async with TaskGroup() as group:
            for symbol in symbols:
                self.LOGGER.info(f'fetching {symbol} balance sheets...')
                group.create_task(self._store_balance_sheets(symbol))

    async def _store_balance_sheets(self, symbol: str):
        data = await self.alpha_vantage.fetch_balance_sheet(symbol)
        self.LOGGER.info(f'fetch completed - {symbol} balance sheets...')

        async with self.lock:
            self.LOGGER.info(f'persisting {symbol} balance sheets...')
            await self.balance_sheet_repo.bulk_insert(data)
            self.LOGGER.info(f'persisted {symbol} balance sheets...')

    async def _fetch_earnings(self, symbols: Sequence[str]):
        async with TaskGroup() as group:
            for symbol in symbols:
                self.LOGGER.info(f'fetching {symbol} earnings report...')
                group.create_task(self._store_earnings(symbol))

    async def _store_earnings(self, symbol: str):
        data = await self.alpha_vantage.fetch_earnings(symbol)
        self.LOGGER.info(f'fetch completed - {symbol} earnings report...')
        async with self.lock:
            self.LOGGER.info(f'persisting {symbol} earnings report...')
            await self.earnings_repo.bulk_insert(data)
            self.LOGGER.info(f'persisted {symbol} earnings report...')

    async def _fetch_cash_flows(self, symbols: Sequence[str]):
        async with TaskGroup() as group:
            for symbol in symbols:
                self.LOGGER.info(f'fetching {symbol} cash flows...')
                group.create_task(self._store_cash_flows(symbol))

    async def _store_cash_flows(self, symbol: str):
        data = await self.alpha_vantage.fetch_cash_flow(symbol)
        self.LOGGER.info(f'fetch completed - {symbol} cash flows...')
        async with self.lock:
            self.LOGGER.info(f'persisting {symbol} cash flows...')
            await self.cash_flow_repo.bulk_insert(data)
            self.LOGGER.info(f'persisted {symbol} cash flows...')
