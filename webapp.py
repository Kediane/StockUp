import random
from datetime import datetime

import streamlit as st
from finvizfinance.quote import finvizfinance
from streamlit.components.v1 import html

st.set_page_config(layout="wide")

from services.streamlit.resources import stock_repo, balance_sheet_repo, cash_flow_repo, income_statement_repo, \
    earnings_repo
import pandas as pd


def fundamentals(balance_sheet_df, cash_flow_df, income_statements_df, earnings_df):
    with st.expander('Balance Sheets'):
        st.write(balance_sheet_df)

    with st.expander(' Cash Flows'):
        st.write(cash_flow_df)

    with st.expander('Income Statements'):
        st.write(income_statements_df)

    with st.expander('Earnings Statement'):
        st.write(earnings_df)


def data_analysis(balance_sheet_df, cash_flow_df, income_statements_df):
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
        quarterly_balance_sheet_statements['Debt To Equity Ratio'] = quarterly_balance_sheet_statements[
                                                                         'totalLiabilities'] / \
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


def news_listing(selected_symbol):
    stock = finvizfinance(selected_symbol.lower())
    news_df = stock.ticker_news().sort_values(by=['Date'], ascending=False)
    current_date = datetime.now()
    colors = [
        '#FF5733',
        '#FF9C33',
        '#FFC133',
        '#C1FF33',
        '#7AFF33',
        '#33FF9F',
        '#33FCFF',
        '#335EFF',
        '#6E33FF',
        '#D733FF',
        '#FF33CE',
        '#FF3352',
    ]
    style = """
    <style>
        @import url(https://fonts.googleapis.com/css?family=Raleway:400,600,700);
        @import url(https://code.ionicframework.com/ionicons/2.0.1/css/ionicons.min.css);
        figure.snip1216 {
          font-family: 'Raleway', Arial, sans-serif;
          color: #fff;
          position: relative;
          display: inline-block;
          overflow: hidden;
          margin: 10px;
          min-width: 220px;
          max-width: 350px;
          width: 100%;
          background-color: #262626;
          color: #ffffff;
          text-align: left;
          font-size: 16px;
          box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
        }
        figure.snip1216 * {
          -webkit-box-sizing: border-box;
          box-sizing: border-box;
          -webkit-transition: all 0.3s ease;
          transition: all 0.3s ease;
        }
        figure.snip1216 .image {
          height: 180px;
          overflow: hidden;
        }
        figure.snip1216 .image div {
          font-size: 140px;
          text-align: center;
        }
        figure.snip1216 figcaption {
          padding: 25px;
          position: relative;
        }
        figure.snip1216 .date {
          background-color: #c0392b;
          top: 25px;
          color: #fff;
          left: 25px;
          min-height: 48px;
          min-width: 48px;
          position: absolute;
          text-align: center;
          font-size: 20px;
          font-weight: 700;
          text-transform: uppercase;
        }
        figure.snip1216 .date span {
          display: block;
          line-height: 24px;
        }
        figure.snip1216 .date .month {
          font-size: 14px;
          background-color: rgba(0, 0, 0, 0.1);
        }
        figure.snip1216 h4,
        figure.snip1216 p {
          margin: 0;
          padding: 0;
        }
        figure.snip1216 h4 {
          min-height: 50px;
          margin-bottom: 10px;
          margin-left: 60px;
          display: inline-block;
          font-weight: 600;
          text-transform: uppercase;
        }
        figure.snip1216 p {
          font-size: 0.8em;
          margin-bottom: 20px;
          line-height: 1.6em;
        }
        figure.snip1216 footer {
          padding: 0 25px;
          background-color: rgba(0, 0, 0, 0.5);
          color: #e6e6e6;
          font-size: 0.8em;
          line-height: 30px;
          text-align: right;
        }
        figure.snip1216 a {
          left: 0;
          right: 0;
          top: 0;
          bottom: 0;
          position: absolute;
          z-index: 1;
        }
        figure.snip1216:hover img,
        figure.snip1216.hover img {
          -webkit-transform: scale(1.1);
          transform: scale(1.1);
        }
    </style>
    """
    content = f"""
    {style}
    <div style="display: flex; justify-content: space-between;height: 100%;flex-wrap:wrap;">
        {''.join([
        f'''
        <figure class="snip1216" style="cursor: pointer;" onclick="window.open('{row['Link']}', '_blank')">
          <div class="image" style="background-color: {random.choice(colors)}">
            <div>{row['Title'][0].upper()}</div>
          </div>
          <figcaption>
            <div class="date">
                <span class="day">{row['Date'].day}</span>
                <span class="month">{row['Date'].strftime('%b')}</span>
            </div>
            <h4>{' '.join(row['Title'].split(' ')[:3])}...</h4>
            <p>{row['Title']}</p>
          </figcaption>
        </figure>
        '''
        for index, row in news_df.iterrows()
        if current_date.year == row['Date'].year
    ])}
    </dv>
    """
    st.markdown(
        """
        <style>
            iframe {
                height: calc(100vh - 25rem) !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    html(content, scrolling=True)


def app():
    st.title('Welcome to StockUp')
    st.subheader('Investment ideas backed by science and not guesses!')
    results = stock_repo.find_all_sync(limit=1_000_000)
    selected_company = st.selectbox('Please select one of the matching stock/etf to analyse',
                                    [item['name'] for item in results])
    selected_symbol = next(map(lambda x: x['symbol'], filter(lambda x: x['name'] == selected_company, results)))

    if selected_company:
        balance_sheets = balance_sheet_repo.find_all_sync(selected_symbol)
        balance_sheet_df = pd.DataFrame(balance_sheets)

        cash_flow = cash_flow_repo.find_all_sync(selected_symbol)
        cash_flow_df = pd.DataFrame(cash_flow)

        income_statements = income_statement_repo.find_all_sync(selected_symbol)
        income_statements_df = pd.DataFrame(income_statements)

        earnings = earnings_repo.find_all_sync(selected_symbol)
        earnings_df = pd.DataFrame(earnings)

        expert_tab, analysis_tab, fundamentals_tab, news_tab = st.tabs(
            ["💰 Expert Advisor", "📈 Data Analysis", "🗃 Fundamentals", "News"])

        with analysis_tab:
            data_analysis(balance_sheet_df, cash_flow_df, income_statements_df)

        with fundamentals_tab:
            fundamentals(balance_sheet_df, cash_flow_df, income_statements_df, earnings_df)
        with news_tab:
            news_listing(selected_symbol)


app()
