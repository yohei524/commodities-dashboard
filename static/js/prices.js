// 金銀価格の自動取得（gold-api.com ＋ open.er-api.com・いずれも無料/キー不要/CORS可）
// 手打ちJSON更新を廃止するためのスクリプト。ページ内の data-price 属性を持つ要素に流し込む。

const TROY_OZ_GRAMS = 31.1035;

function fmt(num, digits = 0) {
  return num.toLocaleString('ja-JP', { maximumFractionDigits: digits, minimumFractionDigits: digits });
}

function setText(sel, text) {
  document.querySelectorAll(sel).forEach(el => { el.textContent = text; });
}

async function fetchJSON(url) {
  const res = await fetch(url, { cache: 'no-store' });
  if (!res.ok) throw new Error(url + ' -> ' + res.status);
  return res.json();
}

async function loadPrices() {
  try {
    const [xau, xag, fx] = await Promise.all([
      fetchJSON('https://api.gold-api.com/price/XAU'),
      fetchJSON('https://api.gold-api.com/price/XAG'),
      fetchJSON('https://open.er-api.com/v6/latest/USD'),
    ]);
    const jpy = fx.rates && fx.rates.JPY;

    // 金
    setText('[data-price="gold-usd"]', '$' + fmt(xau.price) + '/oz');
    // 銀
    setText('[data-price="silver-usd"]', '$' + fmt(xag.price, 2) + '/oz');

    if (jpy) {
      setText('[data-price="usdjpy"]', fmt(jpy, 2) + ' 円/ドル');
      // 円建てグラム換算（税・手数料・スプレッドを含まない理論値）
      setText('[data-price="gold-jpyg"]', '約' + fmt(xau.price / TROY_OZ_GRAMS * jpy) + ' 円/g');
      setText('[data-price="silver-jpyg"]', '約' + fmt(xag.price / TROY_OZ_GRAMS * jpy) + ' 円/g');
    }

    const updated = new Date(xau.updatedAt);
    setText('[data-price="updated"]',
      updated.toLocaleString('ja-JP', { timeZone: 'Asia/Tokyo', month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' }) + ' 時点');
  } catch (e) {
    setText('[data-price]', '取得できませんでした');
    console.error('price fetch failed:', e);
  }
}

document.addEventListener('DOMContentLoaded', loadPrices);
