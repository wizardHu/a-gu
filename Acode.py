'''
Created on 2017/5/7
@author: 3xtrees
'''
# -*- coding: gbk -*-
import requests
import json
import timeit
from Ashare import *
import os


def load_all_quote_symbol():
    print("load_all_quote_symbol start..." + "\n")
    start = timeit.default_timer()
    all_quotes = []
    all_quotes_url = 'http://money.finance.sina.com.cn/d/api/openapi_proxy.php'
    try:
        count = 1
        while (count < 100):
            para_val = '[["hq","hs_a","",0,' + str(count) + ',500]]'
            r_params = {'__s': para_val}
            r = requests.get(all_quotes_url, params=r_params)
            if (len(r.json()[0]['items']) == 0):
                break
            for item in r.json()[0]['items']:
                quote = {}
                code = item[0]
                name = item[2]
                if "ST" in name:
                    all_quotes.append(code)
            count += 1
    except Exception as e:
        print("Error: Failed to load all stock symbol..." + "\n")
        print(e)
    print("load_all_quote_symbol end... time cost: " + str(round(timeit.default_timer() - start)) + "s" + "\n")
    print("total " + str(len(all_quotes)) + " quotes are loaded..." + "\n")
    return all_quotes




if __name__ == '__main__':
    all_quotes = load_all_quote_symbol()

    directory3 = "/Users/game-netease/Documents/stock3"

    # for quote in all_quotes:
    #     if f"{quote}.csv" in os.listdir(directory3) or quote.startswith("bj"):
    #         continue
    #     code = f"{quote[2:8]}.XSHG" if quote.startswith("sh") else f"{quote[2:8]}.XSHE"
    #     print(code)
    #     df = get_price(f'{code}', frequency='1d', count=750)
    #     if df.iloc[-1].name.day != 19:
    #         continue
    #     df.to_csv(f"/Users/game-netease/Documents/stock3/{quote}.csv", index=True)

    # for quote in all_quotes:
    #     if f"{quote}.csv" in os.listdir(directory3):
    #         print(quote)
    #         os.remove(f"{directory3}/{quote}.csv")
    for filename in os.listdir(directory3):
        code = filename[2:8]
        if code.startswith("300") or code.startswith("688"):
            os.remove(f"{directory3}/{filename}")