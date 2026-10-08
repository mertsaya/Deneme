#!/usr/bin/env python3
"""Mantık denetimi bulgularının yeniden üretimi (MANTIK_RAPOR.md maddeleri). Her madde GECTI/KALDI basar.
Kullanım: python3 oyun/b0/test/mantik_test.py
"""
import functools, http.server, json, threading
from pathlib import Path
from playwright.sync_api import sync_playwright

B0 = Path(__file__).resolve().parents[1]
SONUC = []


def yaz(m, ok, ayr=''):
    SONUC.append((m, ok)); print(f"[{m:3s}] {'GECTI' if ok else 'KALDI'}  {ayr}")


class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(H, directory=str(B0)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f'http://127.0.0.1:{srv.server_address[1]}/index.html'
hata = []
with sync_playwright() as p:
    br = p.chromium.launch(args=['--no-sandbox'], executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    ctx = br.new_context(viewport=dict(width=384, height=832), is_mobile=True, has_touch=True)
    pg = ctx.new_page()
    pg.on('pageerror', lambda e: hata.append(str(e)))
    hazir = lambda: pg.wait_for_function('window.__oyun && window.__oyun.hazir')
    asama = lambda: pg.evaluate('window.__oyun.durum().asama')

    def kayitla(k, q='?seed=1'):
        pg.goto(URL + '?kayit=0'); hazir()
        pg.evaluate('(k) => { localStorage.clear(); localStorage.setItem("sdp_kayit", typeof k === "string" ? k : JSON.stringify(k)); }', k)
        pg.goto(URL + q); hazir()

    pg.goto(URL + '?kayit=0'); hazir()
    taban = pg.evaluate('window.__oyun.kayit.oku()')
    # 1) sv.rampa = 7 (B0 tavanı 6): çökme yok, 6'ya kırpılır
    k = json.loads(json.dumps(taban)); k['tur'] = 2; k['sv']['rampa'] = 7
    n0 = len(hata); kayitla(k)
    o = pg.evaluate('window.__oyun.kayit.oku()')
    yaz('1', len(hata) == n0 and o['sv']['rampa'] == 6 and asama() == 'HANGAR', f"sv.rampa={o['sv']['rampa']} asama={asama()} hata={hata[n0:]}")
    # 2) UÇ'tan hemen sonra ikinci dokunuş zayıf kalkış yapmaz (0,25 s kilit)
    pg.click('#ucBtn'); pg.mouse.click(190, 400)
    f1 = pg.evaluate('window.__oyun.durum().rampa_faz'); pg.wait_for_timeout(300); pg.mouse.click(190, 400); pg.wait_for_timeout(50)
    f2 = pg.evaluate('window.__oyun.durum().rampa_faz'); pg.mouse.click(190, 400); f3 = asama()   # açı kilidinden hemen sonra çift dokunuş
    pg.wait_for_timeout(300); pg.mouse.click(190, 400); pg.wait_for_timeout(50)
    yaz('2', f1 == 'aci' and f2 == 'guc' and f3 == 'RAMPA' and asama() == 'UCUS', f'UÇ+ek dokunuş → {f1}; 0,3 s sonra → {f2}; hemen ikinci → {f3}; 0,3 s sonra → {asama()}')
    # 3) kara kutu: düğme dışı dokunuş (atlama) kilidi geçmez
    pg.goto(URL + '?kayit=0&seed=3&bot=hic&hiz=8'); hazir()
    pg.wait_for_function("window.__oyun.durum().asama === 'KARA_KUTU'", timeout=60000)
    pg.mouse.click(190, 120); pg.click('#kkTekrar', force=True); a = asama()
    pg.wait_for_timeout(400); dis = pg.evaluate("document.getElementById('kkTekrar').disabled")
    yaz('3', a == 'KARA_KUTU' and not dis, f'atlama + hemen TEKRAR UÇ → {a}; 0,4 s sonra düğme açık={not dis}')
    # 4) max_v ≥ ses_v ama kırılmadı → negatif Δ yok
    pg.goto(URL + '?kayit=0&seed=3&t=3'); hazir()
    m = pg.evaluate("window.__oyun.durduranMetin({duvar: [], max_v: 120, ip: 0, bitis: 'yer', son_y: 0})")
    yaz('4', 'yakındın' in m and '-' not in m, m)
    # 5) geri sayımda gizlenme → menü açılır, sayım iptal; geri sayımda duraklat düğmesi çalışır
    pg.goto(URL + '?kayit=0&seed=1&bot=hic'); hazir(); pg.wait_for_function("window.__oyun.durum().asama === 'UCUS'", timeout=10000)
    pg.click('#durBtn'); pg.click('#mDevam'); pg.wait_for_timeout(200)
    pg.evaluate("Object.defineProperty(document,'hidden',{value:true,configurable:true}); document.dispatchEvent(new Event('visibilitychange'))")
    m1 = pg.evaluate("!document.getElementById('menu').hidden && document.getElementById('sayim').hidden")
    pg.evaluate("Object.defineProperty(document,'hidden',{value:false,configurable:true}); document.dispatchEvent(new Event('visibilitychange'))")
    pg.click('#mDevam'); pg.wait_for_timeout(200); pg.click('#durBtn')
    m2 = pg.evaluate("!document.getElementById('menu').hidden && document.getElementById('sayim').hidden")
    yaz('5', m1 and m2, f'gizlenince menü={m1}, sayımda duraklat düğmesi={m2}')
    # 6) ilk dokunuş bir düğmeye (duraklat) gelse de ipucu "Yeşilde dokun"a döner
    pg.goto(URL + '?kayit=0&seed=1'); hazir(); pg.wait_for_timeout(200)
    i0 = pg.evaluate("document.querySelector('#ipucu span').textContent")
    pg.click('#durBtn'); i1 = pg.evaluate("document.querySelector('#ipucu span').textContent")
    yaz('6', i0 == 'Başlamak için dokun' and i1 in ('Yeşilde dokun', 'Önce açıyı seç, sonra gücü'), f'{i0!r} → {i1!r}')
    # 7) alan bazında onarım, NaN yok; ikinci bozulma ilk yedeği ezmez
    k = json.loads(json.dumps(taban)); k['tur'] = 3; k['jeton'] = 77; k['ayar']['efekt'] = 'x'; k['ayar']['yazi'] = 9; k['duvar']['ses'] = 'evet'; k['rekor']['max_v'] = -1
    kayitla(k)
    o = pg.evaluate('window.__oyun.kayit.oku()')
    ok7a = o['jeton'] == 77 and o['tur'] == 3 and o['ayar']['efekt'] == 80 and o['ayar']['yazi'] == 1 and o['duvar']['ses'] is None and o['rekor']['max_v'] == 0
    pg.evaluate("localStorage.setItem('sdp_kayit', '{bozuk 1')"); pg.reload(); hazir()
    pg.evaluate("localStorage.setItem('sdp_kayit', '{bozuk 2')"); pg.reload(); hazir()
    y = pg.evaluate("[localStorage.getItem('sdp_kayit_bozuk'), Object.keys(localStorage).filter(k => k.startsWith('sdp_kayit_bozuk_')).length]")
    yaz('7', ok7a and y[0] == '{bozuk 1' and y[1] == 1, f'onarım={ok7a} ilk yedek={y[0]!r} zaman damgalı={y[1]}')
    # 8) bekleyen yolunda duvar.ses numarası = tur + elle + 1 (turSonu ile aynı)
    k = json.loads(json.dumps(taban)); k['tur'] = 2; k['elle'] = 1; k['bekleyen'] = {'j': 10, 'ses': True}
    kayitla(k)
    o = pg.evaluate('window.__oyun.kayit.oku()')
    yaz('8', o['duvar']['ses'] == 4 and o['elle'] == 2 and o['jeton'] == 10, f"duvar.ses={o['duvar']['ses']} elle={o['elle']}")
    # 9) "Kaydı sıfırla" duraklat menüsündeki ayarlarda yok, hangarda var
    pg.click('#dislibtn'); h = pg.evaluate("!document.getElementById('aSifirla').hidden"); pg.click('#aKapat')
    pg.click('#ucBtn'); pg.wait_for_timeout(100); pg.click('#durBtn'); pg.click('#mAyar')
    m = pg.evaluate("document.getElementById('aSifirla').hidden")
    yaz('9', h and m, f'hangarda görünür={h}, duraklat menüsünde gizli={m}')
    # 12) ?b0s eksik değerde varsayılana düşer
    pg.goto(URL + '?kayit=0&b0s=1000,,abc'); hazir()
    b = pg.evaluate('window.__oyun.B0S'); r = pg.evaluate('window.__oyun.tur(1,{},"iyi",1)')
    yaz('12', all(isinstance(v, (int, float)) for v in b.values()) and r['sure_tur'] > 0, json.dumps(b))
    pg.evaluate('localStorage.clear()')
    br.close()
srv.shutdown()
print('sayfa hataları:', hata)
print('TOPLAM:', sum(1 for _, ok in SONUC if ok), '/', len(SONUC))
