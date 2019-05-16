from flask import Flask, render_template, request, g, url_for, jsonify
#, session from flask.ext.session import Session
from flask_socketio import SocketIO, emit
import pandas_datareader as pdr
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os, fnmatch
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls
plotly.tools.set_credentials_file(username='mamendio', api_key='XVNkOrNxyfr2Yi5oAElG')
#Folder Templates - will hold all html files
#Folder Static - will hold all css files
#create web app

#----------Backend------------------
cache = {}

def getSmaEmaGraph(df, column="Close", period=8):
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
    result = pd.concat(frames, sort=True)
    return result

def getSmaEmaValues(df, column="Close", period=8):
    ema = df[column].ewm(span=period, adjust=False).mean()
    sma = df[column].rolling(window=21, min_periods=1).mean()
    return [ema.iloc[-1],sma.iloc[-1]]

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
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
    ticker = ""
    isPost = False;
    if request.method == 'POST':
        isPost = True;
        ticker = request.form['ticker']
        if ticker != "":
            cache['ticker'] = ticker
        try:
            data = pdr.get_data_yahoo(cache['ticker'], start=datetime.datetime.now() + datetime.timedelta(-30), end=datetime.datetime.now())
            valuesResult = getSmaEmaValues(data)
            # print(str(round(valuesResult[0], 2)))
            # print(str(round(valuesResult[1], 2)))
            # graphResult = getSmaEmaGraph(data)
            # plt.grid(True)
            # plt.title(ticker.upper())
            # plt.plot()

            ohlc = []
            while x < y:
                append_me = data.date[x], data.Open[x], data.High[x], data.Low[x], data.Close[x], data.Volume[x]
                ohlc.append(append_me)
                x+=1


            Dates = pd.date_range(end = pd.datetime.today(), periods = 30).tolist()
            trace = go.CandleStick(x = Dates,
                            open=data.Open,
                            high=data.High,
                            low=data.Low,
                            close=data.Close)

            layout = go.Layout(
                autosize=False,
                width=500,
                height=500,
                xaxis = dict(
                    rangeslider = dict(
                        visible = False
                    )
                )
            )

            data = [trace]

            fig = go.Figure(data=data,layout=layout)
            url=py.plot(fig, filename=cache['ticker'],auto_open=False, config={'displayModeBar': False})
            cache['Url'] = url
        except:
            return render_template('runAlg.html', ema=-1,sma=-1, isPost=str(isPost), graphUrl = cache['Url'], Ticker = cache['ticker'])
        # plt.savefig('static/images/graph.png')
        return render_template('runAlg.html', ema=str(round(valuesResult[0], 2)),sma=str(round(valuesResult[1], 2)), isPost=str(isPost), graphUrl = cache['Url'], Ticker = cache['ticker'])
    elif request.method == 'GET':
        if ticker != "":
            cache['ticker'] = ticker
        try:
            data = pdr.get_data_yahoo(cache['ticker'], start=datetime.datetime.now() + datetime.timedelta(-30), end=datetime.datetime.now())
            valuesResult = getSmaEmaValues(data)
            # print(str(round(valuesResult[0], 2)))
            # print(str(round(valuesResult[1], 2)))
        except:
            return jsonify(ema=-1,sma=-1, isPost=str(isPost), graphUrl = cache['Url'], Ticker = cache['ticker'])
        return jsonify(ema=str(round(valuesResult[0], 2)),sma=str(round(valuesResult[1], 2)), isPost=str(isPost), graphUrl = cache['Url'], Ticker = cache['ticker'])


if __name__ == "__main__":
    socketio.run(app, debug=True)


#blue 8 day
#red 21 day

#--------side notes ---------------
# Should look at the daily data
