import time
import requests
from datetime import datetime
import json
import pandas as pd
from matplotlib import pyplot as plt


headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Mobile Safari/537.36'}


udsc = '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'
now = int(time.time())
session = requests.Session()

tokens = {'weth': {'matic': '0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619',
                   'eth': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'},
          'wbtc': {'matic': '0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6',
                   'eth': '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599'},
          'wmatic': {'matic': '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270',
                     'eth': '0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0'},
          'link': {'matic': '0x53E0bca35eC356BD5ddDFebbD1Fc0fD03FaBad39',
                   'eth': '0x514910771AF9Ca656af840dff83E8264EcF986CA'},
          'uni': {'matic': '0xb33EaAd8d922B1083446DC23f610c2567fB5180f',
                  'eth': '0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984'},
          'dydx': {
              'eth': '0x92D6C1e31e14520e676a687F0a93788B716BEff5'},
          'crv': {'matic': '0x172370d5Cd63279eFa6d502DAB29171933a610AF',
                  'eth': '0xD533a949740bb3306d119CC777fa900bA034cd52'},
          'aave': {'matic': '0xD6DF932A45C0f255f85145f286eA0b292B21C90B',
                   'eth': '0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9'},
          'sand': {'matic': '0xBbba073C31bF03b8ACf7c28EF0738DeCF3695683',
                   'eth': '0x3845badAde8e6dFF049820680d1F14bD3903a5d0'},
          '1inch': {
              'eth': '0x111111111117dC0aa78b770fA6A738034120C302'},
          'bat': {
              'eth': '0x0D8775F648430679A709E98d2b0Cb6250d2887EF'},
          }

benchmark_btc = '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599'
portfolio_eth = {1668027600: [['0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599', 127993, 8, 3717, 'WBTC'],
                                ['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 21776471812120992, 18, 2396, 'WETH'],
                                ['0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0', 10441018799739258884, 18, 3890, 'WMATIC'],
                                ['0x514910771AF9Ca656af840dff83E8264EcF986CA', 1021823184633396117, 18, 1975, 'LINK'],
                                ['0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9', 72976716795658229, 18, 7278, 'AAVE'],
                                ['0x92D6C1e31e14520e676a687F0a93788B716BEff5', 2879466989980354114, 18, 11156, 'DYDX'],
                                ['0x111111111117dC0aa78b770fA6A738034120C302', 9088559699238587189, 18, 8104, '1INCH'],
                                ['0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984', 878670451260201281, 18, 7083, 'UNI'],
                                ['0xD533a949740bb3306d119CC777fa900bA034cd52', 7084455523615695893, 18, 6538, 'CRV'],
                                ['0x3845badAde8e6dFF049820680d1F14bD3903a5d0', 7441859748909011098, 18, 6210, 'SAND'],
                                ['0x0D8775F648430679A709E98d2b0Cb6250d2887EF', 18608000787810665730, 18, 1697, 'BAT']]}
portfolio_matic = {1668632400: [['0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619', 18748750083327778, 18, 2396, 'WETH'],
                                  ['0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6', 136322, 8, 3717, 'WBTC'],
                                  ['0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270', 14144911157642520000, 18, 3890, 'WMATIC'],
                                  ['0x53E0bca35eC356BD5ddDFebbD1Fc0fD03FaBad39', 1615508885298869144, 18, 1975, 'LINK'],
                                  ['0xb33EaAd8d922B1083446DC23f610c2567fB5180f', 2158622112211221138, 18, 7083, 'UNI'],
                                  ['0xD6DF932A45C0f255f85145f286eA0b292B21C90B', 127703047846075260, 18, 7278, 'AAVE'],
                                  ['0x172370d5Cd63279eFa6d502DAB29171933a610AF', 13624250439155005822, 18, 6538, 'CRV'],
                                  ['0xBbba073C31bF03b8ACf7c28EF0738DeCF3695683', 8894175011949527871, 18, 6210, 'SAND']]}


def history_quotes(token_id, start_time, end_time=now, q_dict=None):
    if q_dict is None:
        q_dict = {}
    sep = 7776000
    time.sleep(0.2)
    url = f'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id={str(token_id)}&convertId=2781&timeStart={str(start_time)}&timeEnd={str(end_time)}'
    resp = session.get(url, headers=headers)
    content = json.loads(resp.text)['data']['quotes']
    dict_quotes = {datetime.strptime(x['timeClose'][:10], "%Y-%m-%d"): x['quote'] for x in content}
    q_dict = q_dict | dict_quotes
    if start_time < end_time:
        return dict(sorted(q_dict.items()))
    else:
        return history_quotes(token_id, start_time - sep, end_time - sep, q_dict)


def get_prices(portfolio, token):
    session = requests.Session()
    if token == 'B4BO':
        start_time = list(portfolio_eth.keys())[-1]

    elif token == 'B4BM':
        start_time = list(portfolio_matic.keys())[-1]
    prices = pd.DataFrame()
    for balance_date in portfolio.keys():
        for token_id in portfolio[balance_date]:
            data = history_quotes(int(token_id[3]), start_time)
            data = {time.mktime(k.timetuple()): v for k, v in data.items()}
            data_pr = pd.DataFrame(data).T
            data_pr = data_pr.rename(columns={'close': token_id[3]})
            data_pr = data_pr[[token_id[3]]]
            prices = pd.merge(prices, data_pr, how='outer', left_index=True, right_index=True)
    return prices


def calculate_return(prices, portfolio, token):
    performance = pd.DataFrame()
    benchmark_btc = prices[3717].pct_change().cumsum() + 1
    benchmark_btc = benchmark_btc.fillna(1)

    if token == 'B4BO':
        portfolio_dict = portfolio_eth

    elif token == 'B4BM':
        portfolio_dict = portfolio_matic

    for balance_date in portfolio.keys():
        for date in prices.index:
            weight = [x[1]/(10**x[2]) for x in portfolio[balance_date]]
            performance.loc[pd.to_datetime(date, unit='s'), token] = sum(prices.loc[date, :] * weight)
    performance.iloc[0, 0] = 100
    weight = {'weight': (prices.loc[date, :] * weight).values, 'ticker': [x[4] for x in portfolio_dict[list(portfolio.keys())[-1]]]}

    return performance, benchmark_btc, weight


def return_full_data(token):
    if token == 'B4BO':
        portfolio_dict = portfolio_eth

    elif token == 'B4BM':
        portfolio_dict = portfolio_matic

    perf, bench, weight = calculate_return(get_prices(portfolio_dict, token), portfolio_dict, token)
    return perf, bench, weight