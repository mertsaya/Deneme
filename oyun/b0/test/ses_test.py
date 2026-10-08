#!/usr/bin/env python3
"""Motor sesi testi: uçuşta motor aktif ve kazanç > 0, hızla perde değişir; duraklatta kesilir.
İki yol: ses dosyaları normal (mp3) ve engelli (sentez yedek). Kullanım: python3 oyun/b0/test/ses_test.py"""
import functools, http.server, threading
from pathlib import Path
from playwright.sync_api import sync_playwright
B0 = Path(__file__).resolve().parents[1]
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(H, directory=str(B0)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f'http://127.0.0.1:{srv.server_address[1]}/index.html?kayit=0&seed=3&bot=iyi'
kaldi = 0
with sync_playwright() as p:
    br = p.chromium.launch(args=['--no-sandbox'], executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    for yol in ('normal', 'engelli'):
        pg = br.new_context(viewport=dict(width=384, height=832)).new_page()
        if yol == 'engelli': pg.route('**/ses/*', lambda r: r.abort())
        hata = []; pg.on('pageerror', lambda e: hata.append(str(e)))
        pg.goto(URL); pg.wait_for_function('window.__oyun && window.__oyun.hazir')
        pg.mouse.click(190, 400)   # ilk dokunuş: AudioContext
        pg.wait_for_function("window.__oyun.durum().asama === 'UCUS'", timeout=10000); pg.wait_for_timeout(1500)
        d1 = pg.evaluate('window.__oyun.sesDurum()'); pg.wait_for_timeout(1500); d2 = pg.evaluate('window.__oyun.sesDurum()')
        pg.click('#durBtn'); pg.wait_for_timeout(300); d3 = pg.evaluate('window.__oyun.sesDurum()')
        bek = 'mp3' if yol == 'normal' else 'sentez'
        ok = d1['motorAktif'] and d1['kazanc'] > 0 and d1['perde'] > 0 and d1['motorTur'] == bek and not d3['motorAktif'] and not hata
        kaldi += not ok
        print(f"{yol}: {'GECTI' if ok else 'KALDI'}  uçuş {d1}  1,5 s sonra perde {d2['perde']:.3f} kazanç {d2['kazanc']:.3f}  duraklat → motorAktif={d3['motorAktif']}  hata={hata}")
        pg.close()
    br.close()
srv.shutdown()
print('KALDI:', kaldi)
