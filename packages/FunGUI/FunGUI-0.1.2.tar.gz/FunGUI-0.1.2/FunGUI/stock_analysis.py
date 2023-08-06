
import yfinance as yf


aapl= yf.Ticker("aapl")
aapl_historical = aapl.history(period="max",start="2001-12-21", end="2021-01-06", interval="1d")
app_close = aapl_historical['Close'].tolist()
# app_close = app_close[500:]

def stock_fun_analysis(sell_low = -2,
sell_high = 20,
buy_high = 10,
buy_low = -10,
origin_invest = 1000,to_buy = False):
    money = origin_invest
    ref = app_close[0]
    shares = int(money/ref)
    rest_money = money - shares*ref

    money_trend = []
    for i in app_close:
        print('price:'+str(i))
        print('change:'+str((i-ref)/ref*100))
        if to_buy:
            if (i-ref)/ref>=buy_high/100 or (i-ref)/ref<=buy_low/100:
                shares = int(money/i)
                rest_money = money - shares*i
                to_buy = False
                ref=i
                print('buy')
                print(money)
            else:
                pass
        else:
            if (i-ref)/ref>=sell_high/100 or (i-ref)/ref<=sell_low/100:
                print('sell')
                money = shares*i+rest_money
                ref=i
                print(money)
                to_buy = True
            else:
                pass
        money_trend.append(money)
    earn_with_operation = money_trend[-1]/origin_invest*100 #@
    earn_without_operation = app_close[-1]/app_close[1]*100 #@
    earn_compare = round((earn_with_operation-earn_without_operation)/earn_without_operation*100,2) #@
    print(earn_with_operation)
    print(earn_without_operation)


# stock_fun_analysis(sell_low = -2,
# sell_high = 20,
# buy_high = 10,
# buy_low = -10,
# origin_invest = 1000,to_buy = False)
