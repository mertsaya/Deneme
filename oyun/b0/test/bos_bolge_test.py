#!/usr/bin/env python3
"""Kalkış boş bölgesi testi: tüm botlar × 100 tohum, ilk baslangic_bos_x biriminde çarpışma 0;
tur ≤ yavaslatici_tur iken x < yavaslatici_ac_x'te yavaşlatıcı teması 0. Kullanım: python3 oyun/b0/test/bos_bolge_test.py"""
import functools, http.server, threading
from pathlib import Path
from playwright.sync_api import sync_playwright
B0 = Path(__file__).resolve().parents[1]
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(H, directory=str(B0)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
JS = """([b, tur, aci]) => { const A = window.__oyun.AYAR; let ihlal = 0, yv = 0, minx = 1e9;
  for (let s = 1; s <= 100; s++) { const r = window.__oyun.tur(s, {}, b, tur, aci ? {aci} : {});
    if (r.ilk_temas_x !== null) { minx = Math.min(minx, r.ilk_temas_x); if (r.ilk_temas_x < A.baslangic_bos_x) ihlal++; }
    if (tur <= A.yavaslatici_tur) yv += r.erken_yv; }
  return [ihlal, yv, minx, A.baslangic_bos_x, A.yavaslatici_ac_x]; }"""
kaldi = 0
with sync_playwright() as p:
    br = p.chromium.launch(args=['--no-sandbox'], executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg = br.new_page(); pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/index.html?kayit=0'); pg.wait_for_function('window.__oyun.hazir')
    for b in ('hic', 'kotu', 'orta', 'iyi', 'usta'):
        for tur, aci in ((1, None), (1, 'bot'), (3, None)):
            ih, yv, mx, bx, yx = pg.evaluate(JS, [b, tur, aci])
            ok = ih == 0 and yv == 0; kaldi += not ok
            print(f"{b:4s} tur {tur} açı {aci or '38'}: {'GECTI' if ok else 'KALDI'}  x<{bx:.0f} çarpışma {ih}, x<{yx:.0f} yavaşlatıcı {yv}, en küçük ilk temas x {mx:.0f}")
    br.close()
srv.shutdown()
print('KALDI:', kaldi)
