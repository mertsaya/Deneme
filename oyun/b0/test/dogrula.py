#!/usr/bin/env python3
"""Uygulayıcı doğrulaması: sim eşliği (K8 benzeri), deger() birim testi, belirlenimlilik, ?t= ekran görüntüleri.
Kullanım: python3 oyun/b0/test/dogrula.py [n=200]   (yerel http.server'ı kendisi açar; çıktı oyun/b0/test/)
"""
import functools, http.server, importlib.util, json, math, os, statistics as st, sys, threading
from pathlib import Path
from playwright.sync_api import sync_playwright

os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', '/opt/pw-browsers')
B0 = Path(__file__).resolve().parents[1]
TEST = B0 / 'test'
N = int(sys.argv[1]) if len(sys.argv) > 1 else 200


def sim():
    sp = importlib.util.spec_from_file_location('ucus_sim', B0.parent / 'sim' / 'ucus_sim.py')
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    return m


class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


def ort(a): return sum(a) / len(a)


def ci(a):
    m, s = ort(a), st.stdev(a); h = 1.96 * s / math.sqrt(len(a)); return m - h, m + h


def main():
    m = sim()
    for k in list(m.TIPLER):
        if k not in ('balon', 'zeplin', 'marti', 'ucurtma'):
            del m.TIPLER[k]
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(H, directory=str(B0)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = f'http://127.0.0.1:{srv.server_address[1]}/index.html'
    hatalar, rapor = [], {}
    with sync_playwright() as p:
        br = p.chromium.launch(args=['--no-sandbox'], executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
        ctx = br.new_context(viewport=dict(width=384, height=832), device_scale_factor=2, is_mobile=True, has_touch=True)
        pg = ctx.new_page()
        pg.on('console', lambda x: hatalar.append(x.text) if x.type in ('error', 'warning') else None)
        pg.on('pageerror', lambda e: hatalar.append(str(e)))
        pg.goto(url + '?kayit=0&seed=1&b0seyrek=0&tipler=balon,zeplin,marti,ucurtma'); pg.wait_for_function('window.__oyun && window.__oyun.hazir')
        # 1) sim eşliği
        sat = []
        for b in ('hic', 'orta', 'iyi'):
            js = pg.evaluate('([b,n]) => { const o=[]; for (let i=1;i<=n;i++) o.push(window.__oyun.tur(i,{},b,1)); return o; }', [b, N])
            py = [m.tur_oyna(s, {}, b, 1) for s in range(1, N + 1)]
            for ad in ('sure_tur', 'mesafe', 'max_v', 'sekme', 'kazanc', 'mukemmel', 'dalis', 'son_sans', 'mesafe_g'):
                a, c = [r[ad] for r in js], [r[ad] for r in py]
                fark = abs(ort(a) - ort(c)) / max(1e-9, abs(ort(c)))
                ca, cc = ci(a), ci(c)
                ok = fark <= 0.10 or (ca[0] <= cc[1] and cc[0] <= ca[1])
                sat.append(dict(bot=b, olcu=ad, js=round(ort(a), 2), sim=round(ort(c), 2), fark=round(fark * 100, 1), gecti=ok))
            vay = lambda rs: sum(1 for r in rs if r['vay_t'] is not None and r['vay_t'] <= 5) / len(rs)
            sat.append(dict(bot=b, olcu='vay<=5', js=vay(js), sim=vay(py)))
        for b in ('orta', 'iyi'):   # kalkış açısı seçimi (aci='bot') eşliği
            js = pg.evaluate('([b,n]) => { const o=[]; for (let i=1;i<=n;i++) o.push(window.__oyun.tur(i,{},b,1,{aci:"bot"})); return o; }', [b, N])
            py = [m.tur_oyna(s, {}, b, 1, aci='bot') for s in range(1, N + 1)]
            for ad in ('sure_tur', 'mesafe', 'max_v', 'kazanc', 'aci'):
                a, c = [r[ad] for r in js], [r[ad] for r in py]
                fark = abs(ort(a) - ort(c)) / max(1e-9, abs(ort(c))); ca, cc = ci(a), ci(c)
                sat.append(dict(bot=b + '+aci', olcu=ad, js=round(ort(a), 2), sim=round(ort(c), 2), fark=round(fark * 100, 1), gecti=fark <= 0.10 or (ca[0] <= cc[1] and cc[0] <= ca[1])))
        rapor['eslik'] = sat
        # 2) deger() birim testi
        dd = []
        for bot in ('iyi', 'hic'):
            for son in ({}, {'max_v': 130, 'dalis': 5, 'sekme': 9, 'kazanc': 300}, {'max_v': 50, 'dalis': 0, 'sekme': 1}):
                for sv in ({}, {'yakit_ac': 1, 'kademe_n': 0}):
                    for ad in ('rampa', 'bolge', 'verim', 'dalis', 'kademe_itki', 'yakit_ac', 'yakit_s'):
                        j = pg.evaluate('([a,sv,son,b]) => window.__oyun.deger(a,sv,son,b)', [ad, sv, son, bot])
                        s = m.deger(ad, sv, son, bot)
                        if abs(j - s) > 1e-9: dd.append((bot, ad, sv, son, j, s))
        rapor['deger_fark'] = dd
        # 3) belirlenimlilik
        a = pg.evaluate('window.__oyun.tur(7,{rampa:2},"orta",3)'); b_ = pg.evaluate('window.__oyun.tur(7,{rampa:2},"orta",3)')
        rapor['belirlenimli'] = json.dumps(a, sort_keys=True) == json.dumps(b_, sort_keys=True)
        k = pg.evaluate('window.__oyun.kampanya(1,"iyi",15)')
        rapor['kampanya_iyi'] = [(t['tur'], round(t['sure']), round(t['kazanc']), t['al']) for t in k['turlar']]
        rapor['kampanya_ilk'] = k['ilk']
        # 4) ?t= ekran görüntüleri
        goruntu = []
        for ad, q in [('t0_5_rampa', 't=0.5&bot=iyi&seed=3'), ('t2_kalkis', 't=1.6&bot=iyi&seed=3'), ('t4_ucus', 't=4&bot=iyi&seed=3'),
                      ('t9_ucus', 't=9&bot=iyi&seed=3'), ('t14_ucus', 't=14&bot=iyi&seed=3'), ('t9_debug', 't=9&bot=iyi&seed=3&debug=1'),
                      ('t20_yakit', 't=20&bot=iyi&seed=4&sv=yakit_ac:1,yakit_s:4,rampa:4'), ('t60_kara_kutu', 't=60&bot=orta&seed=3')]:
            pg.goto(url + '?kayit=0&' + q); pg.wait_for_function('window.__oyun && window.__oyun.hazir'); pg.wait_for_timeout(300)
            pg.screenshot(path=str(TEST / f'{ad}.png')); goruntu.append(ad)
        # hangar ve ayarlar (kayıtlı oyun)
        pg.goto(url + '?seed=1'); pg.wait_for_function('window.__oyun && window.__oyun.hazir')
        pg.evaluate('() => { const k = window.__oyun.kayit.oku(); k.tur = 3; k.jeton = 400; k.sv.rampa = 2; window.__oyun.kayit.yaz(k); }')
        pg.reload(); pg.wait_for_function('window.__oyun && window.__oyun.hazir'); pg.wait_for_timeout(300)
        pg.screenshot(path=str(TEST / 'hangar.png')); goruntu.append('hangar')
        pg.click('#dislibtn'); pg.wait_for_timeout(200); pg.screenshot(path=str(TEST / 'ayarlar.png')); goruntu.append('ayarlar')
        pg.evaluate('localStorage.clear()')
        rapor['goruntu'] = goruntu
        br.close()
    srv.shutdown()
    rapor['konsol'] = hatalar
    (TEST / 'dogrula.json').write_text(json.dumps(rapor, ensure_ascii=False, indent=1), encoding='utf-8')
    for s in rapor['eslik']:
        print(s)
    print('deger farkı:', rapor['deger_fark'][:5], '| belirlenimli:', rapor['belirlenimli'], '| konsol:', hatalar[:5])
    print('kampanya iyi:', rapor['kampanya_ilk'], rapor['kampanya_iyi'][:8])


if __name__ == '__main__':
    main()
