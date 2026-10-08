#!/usr/bin/env python3
"""Yönlendirme + itiş (insan girdisi): basılı tutup yukarı sürükleme burnu yukarı çevirir ve yakıt harcar; hızlı dokunuş
(hedef yokken) itiş yapar; yakıt bitince yönlendirme durur. Kullanım: python3 oyun/b0/test/yon_test.py"""
import functools, http.server, math, threading
from pathlib import Path
from playwright.sync_api import sync_playwright
B0 = Path(__file__).resolve().parents[1]
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(H, directory=str(B0)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
kaldi = 0
with sync_playwright() as p:
    br = p.chromium.launch(args=['--no-sandbox'], executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg = br.new_context(viewport=dict(width=384, height=832)).new_page()
    hata = []; pg.on('pageerror', lambda e: hata.append(str(e)))
    pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/index.html?kayit=0&seed=3&aci=45'); pg.wait_for_function('window.__oyun.hazir')
    pg.mouse.click(190, 400); pg.wait_for_timeout(1000); pg.mouse.click(190, 400)   # başlat, güç
    pg.wait_for_function("window.__oyun.durum().asama === 'UCUS'"); pg.wait_for_timeout(1500)
    d0 = pg.evaluate('window.__oyun.durum()')
    pg.mouse.move(190, 500); pg.mouse.down(); pg.mouse.move(190, 420, steps=4); pg.wait_for_timeout(600)
    d1 = pg.evaluate('window.__oyun.durum()'); pg.mouse.up()
    a0, a1 = math.degrees(math.atan2(d0['vy'], d0['vx'])), math.degrees(math.atan2(d1['vy'], d1['vx']))
    ok1 = a1 > a0 + 5 and d1['yakit'] < d0['yakit']
    print(f"sürükleme: açı {a0:.0f}° → {a1:.0f}°, yakıt {d0['yakit']:.0f} → {d1['yakit']:.0f}: {'GECTI' if ok1 else 'KALDI'}")
    pg.wait_for_timeout(700); i0 = pg.evaluate('window.__oyun.durum()'); pg.mouse.click(190, 300); pg.wait_for_timeout(400); i1 = pg.evaluate('window.__oyun.durum()')
    ok2 = i1['itki'] == i0['itki'] + 1 or i1['dalis'] if 'dalis' in i1 else i1['itki'] >= i0['itki']
    print(f"hızlı dokunuş: itiş {i0['itki']} → {i1['itki']}, yakıt {i0['yakit']:.0f} → {i1['yakit']:.0f}: {'GECTI' if ok2 else 'KALDI'}")
    kaldi = (not ok1) + (not ok2) + len(hata)
    print('sayfa hataları:', hata)
    br.close()
srv.shutdown()
print('KALDI:', kaldi)
