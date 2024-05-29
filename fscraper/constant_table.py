YAHOO_XPATH = {
    "Market Cap (intraday)": "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[1]/td[2]",
    "Enterprise Value": "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[2]/td[2]",
    "Trailing P/E": "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[3]/td[2]",
    "Forward P/E": "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[4]/td[2]",
    "PEG Ratio (5 yr expected)": "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[5]/td[2]",
    "Price/Sales (ttm)": "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[6]/td[2]",
    "Price/Book (mrq)": "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[7]/td[2]",
    "Enterprise Value/Revenue": "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[8]/td[2]",
    "Enterprise Value/EBITDA": "/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[9]/td[2]"
}


# Yahoo! Finance
INCOME_STATEMENT_ITEMS = ['TotalRevenue', 'OperatingIncome', 'PretaxIncome',
                          'NetIncome', 'BasicEPS']

BALANCE_SHEET_ITEMS = ['TotalAssets', 'TotalEquityGrossMinorityInterest',
                       'StockholdersEquity', 'RetainedEarnings', 'ShareIssued', 'OrdinarySharesNumber',
                       'TreasurySharesNumber']

CASH_FLOW_ITEMS = ['OperatingCashFlow', 'InvestingCashFlow', 'FinancingCashFlow',
                   'EndCashPosition', 'CapitalExpenditure', 'FreeCashFlow']

REPORT_TABLE = {
    "incomestatement": INCOME_STATEMENT_ITEMS,
    "balancesheet": BALANCE_SHEET_ITEMS,
    'cashflow': CASH_FLOW_ITEMS
}
