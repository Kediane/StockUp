import pickle
import sqlite3

import tomli as tomllib
from streamlit import cache_resource

from repositories.balance_sheet import BalanceSheetRepository
from repositories.cash_flow import CashFlowRepository
from repositories.earnings import EarningsRepository
from repositories.income_statement import IncomeStatementRepository
from repositories.stocks import StockRepository


@cache_resource
def load_db_resources():
    with open("application.toml", "rb") as f:
        conf = tomllib.load(f)
    conn = sqlite3.connect(conf['db']['connection_uri'], check_same_thread=False)
    balance_sheet_repo = BalanceSheetRepository(conn)
    cash_flow_repo = CashFlowRepository(conn)
    earnings_repo = EarningsRepository(conn)
    stock_repo = StockRepository(conn)
    income_statement_repo = IncomeStatementRepository(conn)
    close_db = lambda: conn.close()
    return balance_sheet_repo, cash_flow_repo, earnings_repo, stock_repo, income_statement_repo, close_db


@cache_resource
def load_ml_model():
    with open('data/dtree_model.ml', 'rb') as file:
        with open('data/feature_symbols.binary', 'rb') as file2:
            return pickle.load(file), pickle.load(file2)


balance_sheet_repo, cash_flow_repo, earnings_repo, stock_repo, income_statement_repo, close_db = load_db_resources()
stock_prediction_model, feature_symbols = load_ml_model()
