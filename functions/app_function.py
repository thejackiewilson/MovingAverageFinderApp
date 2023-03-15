from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stock_name = request.form['stock_name']
        stock = yf.Ticker(stock_name)
        stock_data = yf.Ticker(stock_name).history(period='1y')
        stock_data['MA50'] = stock_data['Close'].rolling(window=50).mean()
        stock_data['MA200'] = stock_data['Close'].rolling(window=200).mean()
        stock_data['total'] = stock_data['Close'] * stock_data['Volume']
        stock_data['cumulative_total'] = stock_data['total'].cumsum()
        stock_data['cumulative_volume'] = stock_data['Volume'].cumsum()
        stock_data['VWAP'] = stock_data['cumulative_total'] / stock_data['cumulative_volume']
        last_price = stock_data.iloc[-1]['Close']
        ma50 = stock_data.iloc[-1]['MA50']
        ma200 = stock_data.iloc[-1]['MA200']

        stock_data['Date'] = pd.to_datetime(stock_data.index)
        fig, ax = plt.subplots()
        ax.plot(stock_data['Date'], stock_data['Close'], label='Price')
        ax.plot(stock_data['Date'], stock_data['MA50'], label='MA50')
        ax.plot(stock_data['Date'], stock_data['MA200'], label='MA200')
        ax.legend()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.set_title(f'{stock_name} Price Performance')
        plt.tight_layout()
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode()
        graph = f'data:image/png;base64,{graph_url}'
        df = stock.history(period='1y')
        df['50ma'] = df['Close'].rolling(window=50).mean()
        df['200ma'] = df['Close'].rolling(window=200).mean()
        last_close = df['Close'][-1]
        last_50ma = df['50ma'][-1]
        last_200ma = df['200ma'][-1]
        success = df['50ma'].iloc[-1] > df['200ma'].iloc[-1]
        return render_template('index.html', stock_name=stock_name, last_price=last_price, ma50=ma50, ma200=ma200, success=success, last_close=last_close, last_50ma=last_50ma, last_200ma=last_200ma, graph=graph)
    else:
        return render_template('index.html')
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
