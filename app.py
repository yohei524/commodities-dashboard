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
    weekly = load_json('weekly_outlook.json')
    stocks = load_json('defense_stocks.json')
    return render_template('index.html',
                          prices=prices,
                          risks=risks,
                          weekly=weekly,
                          stocks=stocks,
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

@app.route('/copper')
def copper():
    """銅詳細ページ"""
    copper_data = load_json('copper_analysis.json')
    return render_template('copper.html', data=copper_data)

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

@app.route('/trades')
def trades():
    """トレード日誌ページ"""
    trades_data = load_json('trades.json')
    # 統計計算
    if trades_data.get('trades'):
        total_pnl = sum(t.get('pnl', 0) for t in trades_data['trades'])
        win_trades = [t for t in trades_data['trades'] if t.get('pnl', 0) > 0]
        lose_trades = [t for t in trades_data['trades'] if t.get('pnl', 0) < 0]
        win_rate = len(win_trades) / len(trades_data['trades']) * 100 if trades_data['trades'] else 0
        avg_win = sum(t.get('pnl', 0) for t in win_trades) / len(win_trades) if win_trades else 0
        avg_lose = sum(t.get('pnl', 0) for t in lose_trades) / len(lose_trades) if lose_trades else 0
        trades_data['stats'] = {
            'total_pnl': total_pnl,
            'total_trades': len(trades_data['trades']),
            'win_trades': len(win_trades),
            'lose_trades': len(lose_trades),
            'win_rate': round(win_rate, 1),
            'avg_win': round(avg_win),
            'avg_lose': round(avg_lose),
            'profit_factor': round(abs(sum(t.get('pnl', 0) for t in win_trades) / sum(t.get('pnl', 0) for t in lose_trades)), 2) if lose_trades and sum(t.get('pnl', 0) for t in lose_trades) != 0 else 0
        }
    return render_template('trades.html', data=trades_data)

@app.route('/weekly')
def weekly():
    """週次判断ページ"""
    weekly_data = load_json('weekly_outlook.json')
    return render_template('weekly.html', data=weekly_data)

@app.route('/history')
def history():
    """過去イベント検証ページ"""
    history_data = load_json('history.json')
    sanmei_data = load_json('sanmei_record.json')
    return render_template('history.html', history=history_data, sanmei=sanmei_data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
