from flask import Flask, render_template
import json
from datetime import datetime
import os

app = Flask(__name__)

def load_json(filename):
    """JSONファイルを読み込む"""
    filepath = os.path.join(os.path.dirname(__file__), 'data', filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

@app.route('/')
def index():
    """トップページ - コモディティ価格と地政学リスク"""
    prices = load_json('prices.json')
    risks = load_json('geopolitical_risks.json')
    return render_template('index.html',
                          prices=prices,
                          risks=risks,
                          today=datetime.now().strftime('%Y-%m-%d'))

@app.route('/gold')
def gold():
    """ゴールド詳細ページ"""
    gold_data = load_json('gold_analysis.json')
    return render_template('gold.html', data=gold_data)

@app.route('/silver')
def silver():
    """シルバー詳細ページ"""
    silver_data = load_json('silver_analysis.json')
    return render_template('silver.html', data=silver_data)

@app.route('/oil')
def oil():
    """原油詳細ページ"""
    oil_data = load_json('oil_analysis.json')
    return render_template('oil.html', data=oil_data)

@app.route('/defense-stocks')
def defense_stocks():
    """軍需株ページ"""
    stocks = load_json('defense_stocks.json')
    return render_template('defense_stocks.html', stocks=stocks)

@app.route('/sanmei')
def sanmei():
    """算命学ページ"""
    sanmei_data = load_json('sanmei.json')
    return render_template('sanmei.html', data=sanmei_data)

@app.route('/geopolitics')
def geopolitics():
    """地政学リスク詳細ページ"""
    risks = load_json('geopolitical_risks.json')
    return render_template('geopolitics.html', risks=risks)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
