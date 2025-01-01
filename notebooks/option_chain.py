from ib_async import *
util.startLoop()

ib = IB()
ib.connect('127.0.0.1', 7496, clientId=12, readonly=True)

spx = Index('SPX', 'CBOE')
ib.qualifyContracts(spx)

ib.reqMarketDataType(2)

[ticker] = ib.reqTickers(spx)
print(ticker)

spxValue = ticker.marketPrice()
print(spxValue)

chains = ib.reqSecDefOptParams(spx.symbol, '', spx.secType, spx.conId)

df = util.df(chains)

print(df)

chain = next(c for c in chains if c.tradingClass == 'SPX' and c.exchange == 'SMART')
print(chain)


strikes = [strike for strike in chain.strikes
        if strike % 5 == 0
        and spxValue - 20 < strike < spxValue + 20]
expirations = sorted(exp for exp in chain.expirations)[:3]
rights = ['P', 'C']

contracts = [Option('SPX', expiration, strike, right, 'SMART', tradingClass='SPX')
        for right in rights
        for expiration in expirations
        for strike in strikes]

contracts = ib.qualifyContracts(*contracts)
print(len(contracts))

print(contracts[0])


tickers = ib.reqTickers(*contracts)
print(len(tickers))
print(tickers[0])
ib.disconnect()
