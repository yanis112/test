# -*- coding: utf-8 -*-
"""LSTM-Bot-Heroku.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mWbEW0DFZOJiS6cHAyBalU8xFljfl0eg
"""

import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow
from tensorflow import keras
import binance
from tensorflow.keras.layers import LSTM,Dense,Dropout,BatchNormalization
from tensorflow.keras.models import Sequential
from binance.client import Client
import time as time
#pip install ftx
import datetime
import requests
import ftx
from ftx import FtxClient
#!pip install ta
import ta
import math
import smtplib
import time


print(gagaga)

#!pip freeze > requirements.txt

def trade():
    
    
    time.sleep(60)
    
    def formatPrice(n):
        return ("-$" if n < 0 else "$") + "{0:.2f}".format(abs(n))

    

    #récuérer les poids du Denoiser et du LSTM grâce à GitHub
    #!git clone https://github.com/yanis112/LSTM_weight.git
    checkpoint_path1='denoiser_30_weight.hdf5'
    checkpoint_path2='normalized_LSTM_weight.hdf5'

    def destring(list):
        a=[]
        for k in list:
          a.append(float(k))
        return(a)

    #fonctions de normalisation dénormalisation des prix
    import statistics as st


    #Récupération des prix
    api_key='K2MmwHx4c4xKDP0LWSfuDCNMuFUOtU64U4OKuRYncY7ZPCPgJEUIW9xucrdrI5UV'
    api_secret='iLb0ZDB1bKMZ8o6mTXAW5xtmF4ULtwDigVuQLXCntUh0MUesjfA5jcndAJdAxrc4'
    client_binance=binance.client.Client(api_key,api_secret)
    client_binance.get_account()
    data2=pd.DataFrame(client_binance.get_historical_klines('BTCUSDT','30m','1000000 m ago UTC'))  #'30 m ago UTC'
    prix=data2[4].tolist()
    volume=data2[5].tolist()
    prix1=destring(prix)
    prix1=[prix1[i]-prix1[i-1] if i>0 else prix1[i] for i in range(len(prix1))]
    volume1=destring(volume) 


    ecart=st.stdev(prix1[-50000:])
    moy=st.mean(prix1[-50000:])
    moy2=st.mean(volume1[-50000:])
    ecart2=st.stdev(volume1[-50000:])



    

    def normalize(list):
      a=[]
      for i in list:
        a.append((i-moy)/ecart)
      return(a)

    def normalize_vol(list):
      a=[]
      for i in list:
        a.append((i-moy2)/ecart2)
      return(a)

    def moyenne_mob(list,period):
      moy=[]
      for i in range(len(list)):
        if i>=period-1:
          moy.append(st.mean(list[i-period+1:i+1]))
        else:
          moy.append(list[i])
      return(moy)


    #Denoising Autoencoder
    from tensorflow.keras.constraints import max_norm
    from tensorflow.keras.layers import Conv1DTranspose,Conv1D
    from tensorflow.keras.models import Sequential
    input_shape = (30, 1)
    no_epochs = 5
    train_test_split = 0.3
    validation_split = 0.2
    verbosity = 1
    max_norm_value = 2.0


    def init_denois():
      model = Sequential()
      model.add(Conv1D(128, kernel_size=3, kernel_constraint=max_norm(max_norm_value), activation='gelu', kernel_initializer='he_uniform', input_shape=input_shape))
      model.add(Conv1D(32, kernel_size=3, kernel_constraint=max_norm(max_norm_value), activation='gelu', kernel_initializer='he_uniform'))
      model.add(Conv1DTranspose(32, kernel_size=3, kernel_constraint=max_norm(max_norm_value), activation='gelu', kernel_initializer='he_uniform'))
      model.add(Conv1DTranspose(128, kernel_size=3, kernel_constraint=max_norm(max_norm_value), activation='gelu', kernel_initializer='he_uniform'))
      model.add(Conv1D(1, kernel_size=3, kernel_constraint=max_norm(max_norm_value), activation='tanh', padding='same'))

      # Compile and fit data
      model.compile(optimizer='adam', loss='binary_crossentropy')
      return(model)

    denoiser=init_denois()
    denoiser.load_weights(checkpoint_path1)

    #fonction pour débruiter les états
    def denoi_state(st):
      a=st
      b=normalize(a)
      p=denoiser.predict(np.array([b]))[0].reshape(1,-1)[0]
      return(np.array([np.array(p)]))

    def init():
      model=Sequential()
      model.add(LSTM(64,return_sequences=True,input_shape=(30,2),dropout=0.3))  #64-256 selon clément
      model.add(LSTM(64,return_sequences=False,dropout=0.3))
      model.add(Dense(64,activation='gelu'))
      model.add(Dense(units=2,activation='softmax'))
      model.compile(optimizer='adam', loss='binary_crossentropy',metrics=['accuracy'])
      return(model)

    model=init()
    model.load_weights(checkpoint_path2)

    def truncate(n, decimals=0):
        r = np.floor(float(n)*10**decimals)/10**decimals
        return str(r)

    def merge(tab1,tab2):
      l=[]
      for k in range(len(tab1)):
        l.append([tab1[k],tab2[k]])

      return(np.array(l))

    def get_BTC_balance():
      accountName = 'yanisyanis545@gmail.com'                 
      pairSymbol =  'BTC/USDT'    
      fiatSymbol = 'USDT'             
      cryptoSymbol = 'BTC'              
      client_ftx = ftx.FtxClient(api_key='SH6WTFG2zpVi3-1JTAMbaf7tlDO6Ng1LbQTcAhgg',api_secret='stiLn1NlokBaHlfZOLTSkYxGaNpPwJIHQPmYO4Ac')
      balance = client_ftx.get_balances()
      btc_total = [b['total'] for b in balance if b['coin'] == 'BTC']
      return(btc_total[0])

    print("BTC:",get_BTC_balance())

    def get_USD_balance():
      accountName = 'yanisyanis545@gmail.com'                 
      pairSymbol =  'BTC/USDT'    
      fiatSymbol = 'USDT'             
      cryptoSymbol = 'BTC'              
      client_ftx = ftx.FtxClient(api_key='SH6WTFG2zpVi3-1JTAMbaf7tlDO6Ng1LbQTcAhgg',api_secret='stiLn1NlokBaHlfZOLTSkYxGaNpPwJIHQPmYO4Ac')
      balance = client_ftx.get_balances()
      btc_total = [b['total'] for b in balance if b['coin']=='USD']
      return(btc_total[0])

    print("USD:",get_USD_balance())

    def is_bought():
      client_ftx = ftx.FtxClient(api_key='SH6WTFG2zpVi3-1JTAMbaf7tlDO6Ng1LbQTcAhgg',api_secret='stiLn1NlokBaHlfZOLTSkYxGaNpPwJIHQPmYO4Ac')    
      fiat=get_USD_balance()
      cryp=get_BTC_balance()
      if fiat<3:
        return(True)
      else: 
        return(False)

    

    #Connexion à FTX
    pairSymbol =  'BTC/USD'         
    fiatSymbol = 'USD'                 
    cryptoSymbol = 'BTC'             
    myTruncate = 4                  
    client_ftx = ftx.FtxClient(api_key='SH6WTFG2zpVi3-1JTAMbaf7tlDO6Ng1LbQTcAhgg',api_secret='stiLn1NlokBaHlfZOLTSkYxGaNpPwJIHQPmYO4Ac')                 

    # Récupérer les montants

    fiatAmount=get_USD_balance()
    cryptoAmount=get_BTC_balance()

    #Récupération des prix
    api_key='K2MmwHx4c4xKDP0LWSfuDCNMuFUOtU64U4OKuRYncY7ZPCPgJEUIW9xucrdrI5UV'
    api_secret='iLb0ZDB1bKMZ8o6mTXAW5xtmF4ULtwDigVuQLXCntUh0MUesjfA5jcndAJdAxrc4'
    client_binance=binance.client.Client(api_key,api_secret)
    client_binance.get_account()
    data2=pd.DataFrame(client_binance.get_historical_klines('BTCUSDT','30m','1000 m ago UTC'))  #'30 m ago UTC'
    prix=data2[4].tolist()
    volume=data2[5].tolist()
    prix1=destring(prix)
    prix2=destring(prix) 
    prix1=[prix1[i]-prix1[i-1] if i>0 else prix1[i] for i in range(len(prix1))]
    volume1=destring(volume) 

    state_pri = np.array(prix1[-30:])
    state_vol = np.array(volume1[-30:])
    state_pri= np.array(normalize(state_pri[-30:])).reshape(-1,1)
    state_vol= np.array(normalize_vol(state_vol)).reshape(-1,1)


    #on détermine l'action
    action=model.predict(np.array([merge(state_pri,state_vol)]))[0]




    if action[0]>=action[1] and not is_bought() :
        print("Buy: " + formatPrice(prix2[-1]))
        quantityBuy = (float(fiatAmount)/prix2[-1])*0.95
        time.sleep(20)
        try:
            buyOrder=client_ftx.place_order(market=f"BTC/USD",side="buy",price=None,size=quantityBuy,type='market')
            print("buy done")
        except :
               print("buy failed, trying again")
               time.sleep(20)
               try:
                    buyOrder=client_ftx.place_order(market=f"BTC/USD",side="buy",price=None,size=quantityBuy,type='market')
                    print("buy done")
               except :
                   print("buy failed, trying again")
                   time.sleep(20)
                   try:
                        buyOrder=client_ftx.place_order(market=f"BTC/USD",side="buy",price=None,size=quantityBuy,type='market')
                        print("buy done")
                   except :
                        print("failed")
     



    elif action[1]>=action[0] and is_bought() :
        print("Sell: " + formatPrice(prix2[-1]))
        for i in range(3):
            time.sleep(20)
            try:
               sellOrder=client_ftx.place_order(market=f"BTC/USD",side="sell",price=None,size=cryptoAmount,type='market')
               print("sell done")
               break
            except:
               print("sell failed, trying again")
               time.sleep(20)
               try:
                   sellOrder=client_ftx.place_order(market=f"BTC/USD",side="sell",price=None,size=cryptoAmount,type='market')
                   print("sell done")
                   break
               except:
                   print("sell failed,trying again")
                   time.sleep(20)
                   try:
                         sellOrder=client_ftx.place_order(market=f"BTC/USD",side="sell",price=None,size=cryptoAmount,type='market')
                         print("sell done")
                         break
                   except:
                         print("failed")
                             



    else :
        print("hold")
 
