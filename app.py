import asyncio
import logging
import sqlite3
import tomllib

from aiohttp import ClientSession

from models.queries.Income_statements import CREATE_INCOME_STATEMENT_TABLE
from models.queries.balance_sheets import CREATE_BALANCE_SHEET_TABLE
from models.queries.cash_flows import CREATE_CASH_FLOW_TABLE
from models.queries.earnings_statements import CREATE_EARNINGS_STATEMENT_TABLE
from models.queries.stocks import CREATE_STOCKS_TABLE
from repositories.balance_sheet import BalanceSheetRepository
from repositories.cash_flow import CashFlowRepository
from repositories.earnings import EarningsRepository
from repositories.income_statement import IncomeStatementRepository
from repositories.stocks import StockRepository
from services.alpha_vantage import AlphaVantageService
from services.batch import BatchService


async def main(config: dict):
    conn = sqlite3.connect(config['db']['connection_uri'], check_same_thread=False)
    balance_sheet_repo = BalanceSheetRepository(conn)
    cash_flow_repo = CashFlowRepository(conn)
    earnings_repo = EarningsRepository(conn)
    stock_repo = StockRepository(conn)
    income_statement_repo = IncomeStatementRepository(conn)
    client_session = ClientSession()
    batch_service = BatchService(
        AlphaVantageService(config['alphavantage']['api_key'], client_session),
        income_statement_repo,
        balance_sheet_repo,
        cash_flow_repo,
        earnings_repo,
        stock_repo,
        config['batch_job']['schedule_period_hr'],
        config['batch_job']['batch_size'],
    )

    conn.execute(CREATE_STOCKS_TABLE)
    conn.execute(CREATE_BALANCE_SHEET_TABLE)
    conn.execute(CREATE_CASH_FLOW_TABLE)
    conn.execute(CREATE_EARNINGS_STATEMENT_TABLE)
    conn.execute(CREATE_INCOME_STATEMENT_TABLE)

    try:
        await batch_service.run()
    finally:
        await client_session.close()
        await asyncio.to_thread(conn.close)


if __name__ == "__main__":
    with open("application.toml", "rb") as f:
        conf = tomllib.load(f)

    logging.basicConfig(format='%(asctime)s::%(name)s::%(levelname)s:: %(message)s', level=logging.INFO)
    asyncio.run(main(conf))
