import streamlit as st

st.set_page_config(layout="wide")

from services.streamlit.resources import stock_repo, balance_sheet_repo, cash_flow_repo, income_statement_repo, \
    earnings_repo
import pandas as pd


def symbol_search():
    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            stock = st.text_input("Enter the name of the stock/etf to analyse")
        with col2:
            st.markdown('''
            <style>
            #custom-padding {
                margin-bottom: 28px;
            }
            </style>
            <div id="custom-padding"></div>
            ''', unsafe_allow_html=True)
            clicked = st.button('Search')
    if clicked:
        return stock
    else:
        return None


def fundamentals(balance_sheet_df, cash_flow_df, income_statements_df, earnings_df):
    with st.expander('Balance Sheets'):
        st.write(balance_sheet_df)

    with st.expander(' Cash Flows'):
        st.write(cash_flow_df)

    with st.expander('Income Statements'):
        st.write(income_statements_df)

    with st.expander('Earnings Statement'):
        st.write(earnings_df)


def data_analysis(balance_sheet_df, cash_flow_df, income_statements_df, earnings_df):
    def income():
        annual_income_statements = income_statements_df[income_statements_df['report_type'] == 'annualReports']
        quarterly_income_statements = income_statements_df[income_statements_df['report_type'] == 'quarterlyReports']

        with st.expander('Income Statement Analysis'):
            st.subheader('Revenue')
            if display_annual:
                st.line_chart(
                    annual_income_statements,
                    x='fiscalDateEnding',
                    y='totalRevenue',
                    color='#5b7c99'
                )
            else:
                st.line_chart(
                    quarterly_income_statements,
                    x='fiscalDateEnding',
                    y='totalRevenue',
                    color='#5b7c99'
                )

            annual_income_statements['gross_profit_margin'] = annual_income_statements['grossProfit'] / \
                                                              annual_income_statements['totalRevenue']
            quarterly_income_statements['gross_profit_margin'] = quarterly_income_statements['grossProfit'] / \
                                                                 quarterly_income_statements['totalRevenue']

            st.text('')
            st.text('')
            st.subheader('Gross Profit Margin')
            if display_annual:
                st.line_chart(
                    annual_income_statements,
                    x='fiscalDateEnding',
                    y='gross_profit_margin',
                    color='#5b7c99'
                )
            else:
                st.line_chart(
                    quarterly_income_statements,
                    x='fiscalDateEnding',
                    y='gross_profit_margin',
                    color='#5b7c99'
                )

            annual_income_statements['net_profit_margin'] = annual_income_statements['grossProfit'] / \
                                                            annual_income_statements['netIncome']
            quarterly_income_statements['net_profit_margin'] = quarterly_income_statements['grossProfit'] / \
                                                               quarterly_income_statements['netIncome']

            st.text('')
            st.text('')
            st.subheader('Net Profit')
            if display_annual:
                st.line_chart(
                    annual_income_statements,
                    x='fiscalDateEnding',
                    y='net_profit_margin',
                    color='#5b7c99'
                )
            else:
                st.line_chart(
                    quarterly_income_statements,
                    x='fiscalDateEnding',
                    y='net_profit_margin',
                    color='#5b7c99'
                )

            st.subheader('Ebitda')
            if display_annual:
                st.line_chart(
                    annual_income_statements,
                    x='fiscalDateEnding',
                    y='ebitda',
                    color='#5b7c99'
                )
            else:
                st.line_chart(
                    quarterly_income_statements,
                    x='fiscalDateEnding',
                    y='ebitda',
                    color='#5b7c99'
                )

    def balance_sheet():
        annual_balance_sheet_statements = balance_sheet_df[balance_sheet_df['period'] == 'annualReports']
        quarterly_balance_sheet_statements = balance_sheet_df[balance_sheet_df['period'] == 'quarterlyReports']
        annual_balance_sheet_statements['Debt To Equity Ratio'] = annual_balance_sheet_statements['totalLiabilities'] / \
                                                                  annual_balance_sheet_statements[
                                                                      'totalShareholderEquity']
        quarterly_balance_sheet_statements['Debt To Equity Ratio'] = quarterly_balance_sheet_statements['totalLiabilities'] / \
                                                                  quarterly_balance_sheet_statements[
                                                                      'totalShareholderEquity']

        with st.expander('Balance Sheet Analysis'):
            st.subheader('Total Assets')
            if display_annual:
                st.bar_chart(
                    annual_balance_sheet_statements,
                    x='fiscalDateEnding',
                    y='totalAssets',
                    color='#32CD32'
                )
            else:
                st.bar_chart(
                    quarterly_balance_sheet_statements,
                    x='fiscalDateEnding',
                    y='totalAssets',
                    color='#32CD32'
                )

            st.subheader('Total Current Assets')
            if display_annual:
                st.bar_chart(
                    annual_balance_sheet_statements,
                    x='fiscalDateEnding',
                    y='totalCurrentAssets',
                    color='#cd32cd'
                )
            else:
                st.bar_chart(
                    quarterly_balance_sheet_statements,
                    x='fiscalDateEnding',
                    y='totalCurrentAssets',
                    color='#cd32cd'
                )

            st.subheader('Liabilities')
            if display_annual:
                st.bar_chart(
                    annual_balance_sheet_statements,
                    x='fiscalDateEnding',
                    y='totalLiabilities',
                    color='#32CD32'
                )
            else:
                st.bar_chart(
                    quarterly_balance_sheet_statements,
                    x='fiscalDateEnding',
                    y='totalLiabilities',
                    color='#32CD32'
                )

            st.subheader('Current Liabilities')
            if display_annual:
                st.bar_chart(
                    annual_balance_sheet_statements,
                    x='fiscalDateEnding',
                    y='totalCurrentLiabilities',
                    color='#cd32cd'
                )
            else:
                st.bar_chart(
                    quarterly_balance_sheet_statements,
                    x='fiscalDateEnding',
                    y='totalCurrentLiabilities',
                    color='#cd32cd'
                )

            st.subheader('Debt to Equity Ratio')
            if display_annual:
                st.line_chart(
                    annual_balance_sheet_statements,
                    x='fiscalDateEnding',
                    y='Debt To Equity Ratio',
                    color='#0080ff'
                )
            else:
                st.line_chart(
                    quarterly_balance_sheet_statements,
                    x='fiscalDateEnding',
                    y='Debt To Equity Ratio',
                    color='#32CD32'
                )

    def cash_flow():
        annual_cash_flow_statements = cash_flow_df[cash_flow_df['period'] == 'annualReports']
        quarterly_cash_flow_statements = cash_flow_df[cash_flow_df['period'] == 'quarterlyReports']

        with st.expander('Cash Flow Analysis'):
            st.subheader('Operating Cashflow')
            if display_annual:
                st.line_chart(
                    annual_cash_flow_statements,
                    x='fiscalDateEnding',
                    y='operatingCashflow',
                    color='#32CD32'
                )
            else:
                st.line_chart(
                    quarterly_cash_flow_statements,
                    x='fiscalDateEnding',
                    y='operatingCashflow',
                    color='#32CD32'
                )

            st.subheader('Cashflow from Investment')
            if display_annual:
                st.line_chart(
                    annual_cash_flow_statements,
                    x='fiscalDateEnding',
                    y='cashflowFromInvestment',
                    color='#b3b300'
                )
            else:
                st.line_chart(
                    quarterly_cash_flow_statements,
                    x='fiscalDateEnding',
                    y='cashflowFromInvestment',
                    color='#b3b300'
                )

            st.subheader('Cashflow from Financing')
            if display_annual:
                st.line_chart(
                    annual_cash_flow_statements,
                    x='fiscalDateEnding',
                    y='cashflowFromFinancing',
                    color='#ff748c'
                )
            else:
                st.line_chart(
                    quarterly_cash_flow_statements,
                    x='fiscalDateEnding',
                    y='cashflowFromFinancing',
                    color='#ff748c'
                )

    st.header('Data Analysis')
    display_annual = st.toggle('Show Annual Report Analysis')
    income()
    balance_sheet()
    cash_flow()


def app():
    st.title('Welcome to StockUp')
    st.subheader('Investment ideas backed by science and not guesses!')
    symbol = symbol_search()

    if not symbol and 'symbol' in st.session_state:
        symbol = st.session_state['symbol']
    elif symbol:
        st.session_state['symbol'] = symbol

    if symbol:
        results = stock_repo.find_all_sync(symbol)
        selected_company = None
        selected_symbol = None

        if len(results) > 1:
            selected_company = st.selectbox('Please select one of the matching stock/etf to analyse',
                                            [item['name'] for item in results])
            selected_symbol = next(map(lambda x: x['symbol'], filter(lambda x: x['name'] == selected_company, results)))
        elif len(results) == 1:
            selected_company = results[0]['name']
            selected_symbol = next(map(lambda x: x['symbol'], filter(lambda x: x['name'] == selected_company, results)))
        else:
            st.write(f'Could not find any stock/etf matching search {symbol}')

        if selected_company:
            balance_sheets = balance_sheet_repo.find_all_sync(selected_symbol)
            balance_sheet_df = pd.DataFrame(balance_sheets)

            cash_flow = cash_flow_repo.find_all_sync(selected_symbol)
            cash_flow_df = pd.DataFrame(cash_flow)

            income_statements = income_statement_repo.find_all_sync(selected_symbol)
            income_statements_df = pd.DataFrame(income_statements)

            earnings = earnings_repo.find_all_sync(selected_symbol)
            earnings_df = pd.DataFrame(earnings)

            expert_tab, analysis_tab, fundamentals_tab = st.tabs(["💰 Expert Advisor", "📈 Data Analysis", "🗃 Fundamentals"])

            with analysis_tab:
                data_analysis(balance_sheet_df, cash_flow_df, income_statements_df, earnings_df)

            with fundamentals_tab:
                fundamentals(balance_sheet_df, cash_flow_df, income_statements_df, earnings_df)


app()
