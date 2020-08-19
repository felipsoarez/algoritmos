#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 15:20:28 2019

@author: Felipe Soares
"""

import requests
import json
import pandas as pd
import datetime as dt
from matplotlib import pyplot as plt


criptomoeda = input('DataCrypto Analytics | Linear Regression |'
                    '\n\n | Twitter @DataCryptoML |'
                    '\n | Github @datacryptoanalytics |'
                    '\n \nDigite o par de criptomoedas listada na Binance: ')

print('\nO par de criptomoeda informada foi: %s'
      '\n\nDataCrypto Analytics esta buscando os valores,'
      ' por favor aguarde alguns segundos!' %(criptomoeda))


root_url = 'https://api.binance.com/api/v1/klines'

symbol = criptomoeda

interval = input('Digite o Timeframe (Exemplo: 15m, 30m, 1h, 1d, 1M): ')

url = root_url + '?symbol=' + symbol + '&interval=' + interval
print(url)

#Monta URL e o Gráfico e DataFrane
def get_bars(symbol, interva = interval):
   url = root_url + '?symbol=' + symbol + '&interval=' + interval
   data = json.loads(requests.get(url).text)
   df = pd.DataFrame(data)
   df.columns = ['open_time',
                 'o', 'h', 'l', 'c', 'v',
                 'close_time', 'qav', 'num_trades',
                 'taker_base_vol', 'taker_quote_vol', 'ignore']
   df.index = [dt.datetime.fromtimestamp(x/1000.0) for x in df.close_time]
   return df

criptomoeda = get_bars(criptomoeda)

criptomoeda_fechamento = criptomoeda['c'].astype('float').values
criptomoeda_abertura = criptomoeda['o'].astype('float').values
criptomoeda_num_trades = criptomoeda['num_trades'].astype('float')
criptomoeda_maxima = criptomoeda['h'].astype('float')
criptomoeda_minima = criptomoeda['l'].astype('float')
criptomoeda_volume = criptomoeda['v'].astype('float')
criptomoeda_datas_fechamento = criptomoeda['close_time'].astype('float')
criptomoeda_datas_abertura = criptomoeda['open_time'].astype('float')
taker_base_vol = criptomoeda['taker_base_vol'].astype('float')
taker_quote_vol = criptomoeda['taker_quote_vol'].astype('float')

#============
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['DejaVu Sans']

criptomoeda_regressao = criptomoeda_abertura

criptomoeda_X_train = criptomoeda_abertura
criptomoeda_X_test = criptomoeda_abertura
X_train = np.reshape(criptomoeda_X_train, (-1,1))
X_test = np.reshape(criptomoeda_X_test, (-1,1))

criptomoeda_y_train = criptomoeda_fechamento
criptomoeda_y_test = criptomoeda_fechamento
y_train = np.reshape(criptomoeda_y_train, (-1,1))
y_test = np.reshape(criptomoeda_y_test, (-1,1))

regr = linear_model.LinearRegression()

regr.fit(X_train, y_train)

criptomoeda_y_pred = regr.predict(X_test)

# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean squared error
print("Mean squared error: %.2f"
      % mean_squared_error(y_test, criptomoeda_y_pred))
# Explained variance score: 1 is perfect prediction
print('Score de variância(próximo de 1.0 bom > ruim): %.2f'
      % r2_score(y_test, criptomoeda_y_pred))

#============  Criar Gráfico
plt.style.use('bmh')
plt.rcParams['figure.figsize'] = (9,5)

plt.subplot(2, 1, 1)
plt.plot(criptomoeda_fechamento, '-', color="black")
plt.legend(['Close'], loc=0)
plt.title('')
plt.ylabel('Price')

plt.subplot(2, 1, 2)
plt.scatter(X_test, y_test, color="black", alpha=0.5)
plt.plot(X_test, criptomoeda_y_pred, color='red', linewidth=2)
plt.legend(['linear regression', 'close'], loc=0)
plt.xlabel('')
plt.ylabel('Linear Regression')

plt.show()
