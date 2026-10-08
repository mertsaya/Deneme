#!/usr/bin/env python3
"""K15 genişletmesi (testci/kabul.py'ye dokunmadan): 360x780, 384x832, 412x915 × yazı 1,0/1,2/1,4.
Denetlenen: kara kutu ve hangarın ana düğmeleri (TEKRAR UÇ, HANGAR, UÇ) tam görünür ve tek satır; ayarlarda düğmeler birbirine/etikete binmez;
hangar kart açıklaması ≥ 13 px; hangar roketi ≥ 100 px; yatay kaydırma yok; tüm görünür düğmeler ≥ 48 px. Görüntüler test/k15/.
"""
import functools, http.server, json, threading
from pathlib import Path
from playwright.sync_api import sync_playwright
B0 = Path(__file__).resolve().parents[1]; OUT = B0 / 'test' / 'k15'; OUT.mkdir(exist_ok=True)
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(H, directory=str(B0)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f'http://127.0.0.1:{srv.server_address[1]}/index.html'
JS = """(ids) => { const out = {gor: {}, kucuk: [], yatay: document.documentElement.scrollWidth > innerWidth + 1};
  for (const id of ids) { const e = document.getElementById(id); const r = e.getBoundingClientRect(); const rg = document.createRange(); rg.selectNodeContents(e); const satir = new Set([...rg.getClientRects()].map(q => Math.round(q.top))).size;
    out.gor[id] = {tam: r.top >= 0 && r.bottom <= innerHeight + 0.5 && r.left >= 0 && r.right <= innerWidth + 0.5, tek_satir: satir <= 1, r: [r.left, r.top, r.right, r.bottom].map(Math.round)}; }
  for (const b of document.querySelectorAll('button')) { const r = b.getBoundingClientRect(); if (r.width && r.height && (r.width < 48 || r.height < 48)) out.kucuk.push(b.textContent.trim().slice(0, 15)); }
  return out; }"""
CAK = """() => { const s = []; for (const a of document.querySelectorAll('#ayarlar .ayar')) { const el = [...a.querySelectorAll('label, button')].map(e => e.getBoundingClientRect());
  for (let i = 0; i < el.length; i++) for (let j = i + 1; j < el.length; j++) { const p = el[i], q = el[j]; if (p.left < q.right - 1 && q.left < p.right - 1 && p.top < q.bottom - 1 && q.top < p.bottom - 1) s.push(a.querySelector('label').textContent); } } return [...new Set(s)]; }"""
sonuc, kaldi = [], 0
with sync_playwright() as p:
    br = p.chromium.launch(args=['--no-sandbox'], executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    for w, h in [(360, 780), (384, 832), (412, 915)]:
        for y in (1.0, 1.2, 1.4):
            pg = br.new_context(viewport=dict(width=w, height=h), is_mobile=True, has_touch=True).new_page()
            pg.goto(URL + '?seed=3'); pg.wait_for_function('window.__oyun.hazir')
            pg.evaluate('(y) => { localStorage.clear(); const k = window.__oyun.kayit.oku(); k.tur = 2; k.jeton = 500; k.ayar.yazi = y; window.__oyun.kayit.yaz(k); }', y)
            pg.goto(URL + '?seed=3&bot=orta&hiz=8'); pg.wait_for_function("window.__oyun.durum().asama === 'KARA_KUTU'", timeout=90000)
            pg.mouse.click(w // 2, 60); pg.wait_for_timeout(500)
            kk = pg.evaluate(JS, ['kkTekrar', 'kkHangar']); pg.screenshot(path=str(OUT / f'kk_{w}x{h}_y{y}.png'))
            pg.click('#kkHangar'); pg.wait_for_timeout(300)
            hg = pg.evaluate(JS, ['ucBtn', 'dislibtn'])
            hg['kart_px'] = pg.evaluate("parseFloat(getComputedStyle(document.querySelector('.kart p')).fontSize)")
            hg['roket_px'] = pg.evaluate("document.querySelector('#hRoket svg').getBoundingClientRect().height")
            pg.screenshot(path=str(OUT / f'hangar_{w}x{h}_y{y}.png'))
            pg.click('#dislibtn'); pg.wait_for_timeout(200)
            ay = pg.evaluate(JS, ['aKapat']); ay['cakisan'] = pg.evaluate(CAK); pg.screenshot(path=str(OUT / f'ayar_{w}x{h}_y{y}.png'))
            ok = (all(v['tam'] and v['tek_satir'] for v in {**kk['gor'], **hg['gor'], **ay['gor']}.values()) and not ay['cakisan']
                  and hg['kart_px'] >= 13 and hg['roket_px'] >= 100 and not (kk['yatay'] or hg['yatay'] or ay['yatay']) and not (kk['kucuk'] or hg['kucuk'] or ay['kucuk']))
            kaldi += not ok
            sonuc.append(dict(gorunum=f'{w}x{h}', yazi=y, gecti=ok, kara_kutu=kk['gor'], hangar=hg['gor'], kart_px=hg['kart_px'], roket_px=round(hg['roket_px']), ayar_cakisan=ay['cakisan'], kucuk=kk['kucuk'] + hg['kucuk'] + ay['kucuk']))
            print(f"{w}x{h} y{y}: {'GECTI' if ok else 'KALDI'}  kart {hg['kart_px']:.1f}px roket {hg['roket_px']:.0f}px cakisan {ay['cakisan']} " + ('' if ok else json.dumps({**kk['gor'], **hg['gor']}, ensure_ascii=False)))
            pg.evaluate('localStorage.clear()'); pg.close()
    br.close()
srv.shutdown()
(OUT / 'k15_genis.json').write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding='utf-8')
print('KALDI:', kaldi, '/', len(sonuc))
