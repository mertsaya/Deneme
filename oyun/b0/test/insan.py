#!/usr/bin/env python3
"""İnsan akışı dumanı: rampa dokunuşu, uçuşta dokunuşlar, dron halkası, duraklat → yeniden başla, kara kutu → hangar → satın al → uç."""
import functools, http.server, os, threading
from pathlib import Path
from playwright.sync_api import sync_playwright
B0 = Path(__file__).resolve().parents[1]; T = B0 / 'test'
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(H, directory=str(B0)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f'http://127.0.0.1:{srv.server_address[1]}/index.html'
hata = []
with sync_playwright() as p:
    br = p.chromium.launch(args=['--no-sandbox'], executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg = br.new_context(viewport=dict(width=384, height=832), device_scale_factor=2, is_mobile=True, has_touch=True).new_page()
    pg.on('console', lambda x: hata.append(x.text) if x.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: hata.append(str(e)))
    pg.goto(url + '?seed=11'); pg.wait_for_function('window.__oyun && window.__oyun.hazir')
    k = pg.evaluate('window.__oyun.kayit.oku()'); k['tur'] = 2; k['jeton'] = 2000; k['sv']['yakit_ac'] = 1; k['sv']['yakit_s'] = 4
    pg.evaluate('(k) => window.__oyun.kayit.yaz(k)', k); pg.reload(); pg.wait_for_function('window.__oyun.hazir')
    print('açılış:', pg.evaluate('window.__oyun.durum().asama'))
    pg.click('#ucBtn'); pg.wait_for_timeout(840); pg.mouse.click(190, 300)   # yeşile yakın
    print('kalkış:', pg.evaluate('window.__oyun.durum()')['asama'])
    halka_goruldu = False
    for i in range(80):
        d = pg.evaluate('window.__oyun.durum()')
        if d['asama'] != 'UCUS': break
        if d['halka'] and not halka_goruldu:
            halka_goruldu = True; pg.screenshot(path=str(T / 'insan_halka.png'))
        if d['halka'] and d['halka']['tau'] <= 0.2 and d['halka']['deneme'] is None: pg.mouse.click(190, 400)
        elif not d['halka'] and i % 6 == 0: pg.mouse.click(190, 400)
        pg.wait_for_timeout(150)
    print('halka görüldü:', halka_goruldu, 'uçuş sonu:', pg.evaluate('window.__oyun.durum()'))
    pg.screenshot(path=str(T / 'insan_ucus.png'))
    pg.wait_for_function("window.__oyun.durum().asama === 'KARA_KUTU'", timeout=90000); pg.wait_for_timeout(4200)
    pg.screenshot(path=str(T / 'insan_kara_kutu.png'))
    o = [e for e in pg.evaluate('window.__oyun.olaylar') if e[1] == 'firsat']; print('fırsatlar:', o)
    j0 = pg.evaluate('window.__oyun.kayit.oku().jeton'); print('jeton:', j0)
    pg.click('#kkHangar'); pg.wait_for_timeout(300)
    pg.click('#kartlar .kart >> nth=0'); pg.wait_for_timeout(200)
    print('satın alma sonrası:', pg.evaluate('window.__oyun.kayit.oku()')['sv'], pg.evaluate('window.__oyun.kayit.oku().jeton'))
    pg.click('#ucBtn'); pg.wait_for_timeout(4000)
    pg.click('#durBtn'); pg.wait_for_timeout(200); pg.screenshot(path=str(T / 'insan_duraklat.png'))
    j1 = pg.evaluate('window.__oyun.kayit.oku()')
    pg.click('#mYeniden'); pg.wait_for_timeout(300)
    j2 = pg.evaluate('window.__oyun.kayit.oku()')
    print('elle bitirme: jeton', j1['jeton'], '->', j2['jeton'], 'tur', j1['tur'], '->', j2['tur'], 'asama', pg.evaluate('window.__oyun.durum().asama'))
    # büyük yazıyla kara kutu
    pg.goto(url + '?kayit=0&seed=3&bot=orta&t=40'); pg.wait_for_function('window.__oyun.hazir')
    pg.evaluate("document.documentElement.style.setProperty('--yazi', 1.4)"); pg.wait_for_timeout(200)
    pg.screenshot(path=str(T / 'kara_kutu_yazi14.png'))
    br.close()
srv.shutdown()
print('konsol:', hata)
