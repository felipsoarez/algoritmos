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


#Esolhe a Criptomoedas e valores de negociação
criptomoeda = input('========= DataCrypto Analytics =========' 
                    '\n\nDigite o par de criptomoedas listada na Binance:')

print('O par de criptomoeda informada foi: %s' 
      '\n \nDataCrypto Analytics esta buscando os valores,' 
      'por favor aguarde alguns segundos!' %(criptomoeda))


#Cria URL da API Binance
root_url = 'https://api.binance.com/api/v1/klines'

symbol = criptomoeda

interval = '1D'

url = root_url + '?symbol=' + symbol + '&interval=' + interval
print(url)

#Monta URL e o Gráfico e DataFrane
def get_bars(symbol, interval = '1d'):
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

# Plot outputs
plt.figure(figsize=(9,5))
plt.title('DataCrypto Analytics')
plt.style.use('dark_background')
plt.style.use('fivethirtyeight')
plt.scatter(X_test, y_test,  color='g')
plt.plot(X_test, criptomoeda_y_pred, color='red', linewidth=3)
plt.show()
