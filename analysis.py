import pandas as pd
from scipy.stats import linregress

fed_fund_rate = pd.read_excel("data/美联储联邦基金利率.xlsx")
fed_fund_rate["month"] = fed_fund_rate["date"].astype(str).replace("-", "", regex=True).str.slice(start=0, stop=6).astype(int)
fed_fund_rate_monthly = fed_fund_rate.groupby("month")["FED Fund Rate"].mean()
fed_fund_rate_monthly.name = "美联储联邦基金利率"

hangseng_index = pd.read_excel("data/恒生指数.xlsx")
hangseng_index["month"] = hangseng_index["date"].astype(str).replace("-", "", regex=True).str.slice(start=0, stop=6).astype(int)
hangseng_index_monthly = hangseng_index.groupby("month")["hangseng index"].mean()
hangseng_index_monthly.name = "恒生指数"

price_index_weekly = pd.read_excel("data/中原城市领先指数(中小型單位).xlsx")
price_index_weekly["month"] = price_index_weekly["日期"].str.split(" - ").str[1].replace('/', '', regex=True).str.slice(start=0, stop=6).astype(int)
price_index_monthly = price_index_weekly.groupby("month")["中原城市(中小型單位)領先指數"].mean()
price_index_monthly.name = "中原城市领先指数(中小型单位)"

price_index_max_drawdown = (price_index_monthly.expanding().max() - price_index_monthly) / price_index_monthly.expanding().max()

rent_monthly = pd.read_excel("data/中原城市租金指數(中小型單位).xlsx")
rent_monthly["month"] = rent_monthly["日期"].str.split(" - ").str[1].replace('/', '', regex=True).str.slice(start=0, stop=6).astype(int)
rent_index_monthly = rent_monthly.groupby("month")["中原城市(中小型單位)租金指數"].mean()
rent_index_monthly.name = "中原城市租金指数(中小型单位)"
rent_return_monthly = rent_monthly.groupby("month")["回報率"].mean()
rent_return_monthly.name = "中原城市租金回报率(中小型单位)"

deal_statistic = pd.read_excel("data/楼宇成交金额.xlsx")
deal_statistic = deal_statistic.set_index("Date")
deal_statistic["总成交数"] = deal_statistic["First Hand Contract Number"] + deal_statistic["Second Hand Contract Number"]
deal_statistic["总成交金额"] = deal_statistic["First Hand Contract Value"] + deal_statistic["Second Hand Contract Value"]

deal_statistic["总成交数(12个月移动平均)"] = deal_statistic["总成交数"].rolling(12).mean()
deal_statistic["总成交金额(12个月移动平均)"] = deal_statistic["总成交金额"].rolling(12).mean()

mainland_price_index_monthly = pd.read_excel("data/中原内地一线城市房价指数.xlsx")
mainland_price_index_monthly["month"] = mainland_price_index_monthly["month"].astype(str).replace("-", "", regex=True).str.slice(start=0, stop=6).astype(int)
mainland_price_index_monthly = mainland_price_index_monthly.set_index("month")
mainland_price_index_monthly = mainland_price_index_monthly.sort_index()

ashare_index = pd.read_excel("data/A股指数.xlsx")
ashare_index["month"] = ashare_index["date"].astype(str).replace("-", "", regex=True).str.slice(start=0, stop=6).astype(int)
ashare_index_monthly = ashare_index.groupby("month")[["沪深300", "上证综合指数"]].mean()
ashare_index_monthly = ashare_index_monthly.reindex(price_index_monthly.index)

result = pd.concat([fed_fund_rate_monthly, hangseng_index_monthly, price_index_monthly, rent_index_monthly, rent_return_monthly, deal_statistic, mainland_price_index_monthly, ashare_index_monthly], axis=1)

x = rent_return_monthly[rent_return_monthly > 0]
y = price_index_monthly.loc[x.index]
slope, intercept, r, p, std = linregress(x.values, y.values)

pass