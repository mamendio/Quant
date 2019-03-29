from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import pandas_datareader as pdr
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Folder Templates - will hold all html files
#Folder Static - will hold all css files
#create web app

#----------Backend------------------

def EMA(df, column="Close", period=8):
    ema = df[column].ewm(span=period, adjust=False).mean()
    sma = df[column].rolling(window=21, min_periods=1).mean()
    result1 = df.join(ema.to_frame('EMA'))
    result2 = df.join(sma.to_frame('SMA'))
    fig, ax = plt.subplots(figsize=(16,9))
    ax.plot(sma.index, sma, label = '21-days SMA')
    ax.plot(ema.index, ema, label = '8-days EMA')
    ax.legend(loc='best')
    ax.set_ylabel('Price in $')
    frames = [result1, result2]
    result = pd.concat(frames)
    return result

#-----Controller methods--------#
app = Flask(__name__)
app.config['SECRET_KEY'] = "secret!"
socketio = SocketIO(app)
@app.route("/", methods=['GET','POST'])
def main():
    return render_template('index.html')


@app.route("/runAlg", methods=['GET','POST'])
def runAlg():
    ticker = request.form['ticker']#'tdoc'
    data = pdr.get_data_yahoo(ticker, start=datetime.datetime.now() + datetime.timedelta(-30), end=datetime.datetime.now())
    result = EMA(data)
    plt.grid(True)
    plt.title(ticker.upper())
    plt.plot()
    plt.savefig('static/images/graph.png')
    return render_template('runAlg.html')

if __name__ == "__main__":
    socketio.run(app)





#--------side notes ---------------
# Should look at the daily data
# https://www.youtube.com/watch?v=6up7mTY9ZnI webscraper for tradingview
# https://www.tradingview.com/rest-api-spec/
