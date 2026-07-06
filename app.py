from flask import Flask, render_template, redirect
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
    """トップページ - 金銀価格（自動取得）＋今週のひとこと"""
    hitokoto = load_json('hitokoto.json')
    return render_template('index.html',
                          hitokoto=hitokoto,
                          today=datetime.now().strftime('%Y-%m-%d'))

@app.route('/gold')
def gold():
    """ゴールドページ"""
    hitokoto = load_json('hitokoto.json')
    return render_template('gold.html', hitokoto=hitokoto)

@app.route('/silver')
def silver():
    """シルバーページ"""
    hitokoto = load_json('hitokoto.json')
    return render_template('silver.html', hitokoto=hitokoto)

@app.route('/kaikata')
def kaikata():
    """金の買い方 比較記事"""
    return render_template('kaikata.html')

@app.route('/bichiku')
def bichiku():
    """備蓄ページ"""
    return render_template('備蓄.html')

# 旧ページはトップへリダイレクト（外部リンク・ブックマーク対策）
@app.route('/weekly')
@app.route('/copper')
@app.route('/oil')
@app.route('/defense-stocks')
@app.route('/geopolitics')
@app.route('/trades')
@app.route('/history')
@app.route('/reel')
@app.route('/sanmei')
def legacy_redirect():
    return redirect('/', code=301)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
