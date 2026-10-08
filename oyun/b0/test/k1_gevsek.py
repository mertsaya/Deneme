#!/usr/bin/env python3
"""K1 (gevşetilmiş, kullanıcı kararı): tur 1'de ilk olumlu sekme ('vay') kalkış anından ≤ 6,5 s, iyi ve hic botlarında turların ≥ %90'ı.
Rampadaki bekleme sayılmaz. Ayrıca ilk temasın kalkıştan en erken ~2,5 s sonra olduğu raporlanır."""
import functools, http.server, sys, threading
from pathlib import Path
from playwright.sync_api import sync_playwright
B0 = Path(__file__).resolve().parents[1]; ESIK = float(sys.argv[1]) if len(sys.argv) > 1 else 6.5
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(H, directory=str(B0)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
kaldi = 0
with sync_playwright() as p:
    br = p.chromium.launch(args=['--no-sandbox'], executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg = br.new_page(); pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/index.html?kayit=0'); pg.wait_for_function('window.__oyun.hazir')
    for b in ('hic', 'iyi'):
        r = pg.evaluate('(b) => { const o = []; for (let s = 1; s <= 100; s++) { const x = window.__oyun.tur(s, {}, b, 1); o.push([x.vay_t === null ? null : x.vay_t - (x.sure_tur - x.sure_ucus), x.ilk_temas_x, x.sure_tur]); } return o; }', b)
        oran = sum(1 for v, _, _ in r if v is not None and v <= ESIK) / len(r)
        ok = oran >= 0.9; kaldi += not ok
        print(f"{b}: {'GECTI' if ok else 'KALDI'}  vay (kalkıştan) ≤ {ESIK} s oranı %{oran * 100:.0f}; ort tur süresi {sum(x[2] for x in r) / len(r):.1f} s")
    br.close()
srv.shutdown()
print('KALDI:', kaldi)
