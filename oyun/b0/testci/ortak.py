"""Ortak yardimcilar: sunucu, tarayici, sayfa acma, kanca denetimi.
Tum betikler bunu kullanir. Oyun kodu degistirilmez; yalnizca TASARIM.md 17 kancalari kullanilir.

Ortam: PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers (varsayilan olarak burada ayarlanir).
"""
import contextlib, functools, http.server, json, os, socket, sys, threading, time
from pathlib import Path

os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")

TESTCI = Path(__file__).resolve().parent
B0 = TESTCI.parent
CIKTI = TESTCI / "cikti"
GORUNUM = dict(width=384, height=832)
DPR = 2
GEREKLI_KANCALAR = ["durum", "adim", "dokun", "tur", "kampanya", "olaylar", "kayit"]


class Hata(SystemExit):
    pass


def dur(mesaj):
    print("HATA: " + mesaj, file=sys.stderr)
    raise Hata(2)


class _Sessiz(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


@contextlib.contextmanager
def sunucu(kok=None, port=0):
    """kok klasorunu yerel http.server ile sunar (python -m http.server esdegeri, ayri iplikte). (taban_url) verir."""
    kok = Path(kok or B0)
    h = functools.partial(_Sessiz, directory=str(kok))
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", port), h)
    th = threading.Thread(target=srv.serve_forever, daemon=True)
    th.start()
    try:
        yield f"http://127.0.0.1:{srv.server_address[1]}"
    finally:
        srv.shutdown()
        srv.server_close()


def sayfa_dosyasi(args_sayfa):
    """--sayfa verilmezse index.html; yoksa anlamli hata."""
    ad = args_sayfa or "index.html"
    p = Path(ad)
    if not p.is_absolute():
        p = B0 / ad
        if not p.exists() and (TESTCI / ad).exists():
            p = TESTCI / ad
    if not p.exists():
        dur(f"Sayfa yok: {p}\n  oyun/b0/index.html henuz yazilmamis olabilir. Deneme icin: --sayfa testci/sahte.html")
    return p.resolve()


def sayfa_url(taban, dosya, sorgu=""):
    rel = os.path.relpath(dosya, B0)
    if rel.startswith(".."):
        dur("Sayfa oyun/b0 altinda olmali (sunucu kok klasoru): " + str(dosya))
    return f"{taban}/{rel}" + (("?" + sorgu.lstrip("?")) if sorgu else "")


def tarayici_baslat(p):
    args = ["--use-gl=swiftshader", "--use-angle=swiftshader", "--enable-unsafe-swiftshader",
            "--ignore-gpu-blocklist", "--autoplay-policy=document-user-activation-required", "--no-sandbox"]
    try:
        return p.chromium.launch(headless=True, args=args)
    except Exception as e:
        dur("Chromium acilamadi: %s\n  PLAYWRIGHT_BROWSERS_PATH=%s" % (str(e).splitlines()[0], os.environ["PLAYWRIGHT_BROWSERS_PATH"]))


FPS_JS = """
(() => {
  window.__fps = {kare: 0, t0: performance.now(), son: performance.now(), en_uzun: 0, ornek: []};
  const f = (t) => {
    const F = window.__fps; const dt = t - F.son; F.son = t; F.kare++;
    if (dt > F.en_uzun) F.en_uzun = dt;
    if (F.ornek.length < 20000) F.ornek.push(dt);
    requestAnimationFrame(f);
  };
  requestAnimationFrame(f);
})();
"""


RED_JS = """
(() => {
  // Telefonda tam ekran / yon kilidi / titresim reddedilebilir: hepsini reddettir.
  window.__red = {tamekran: 0, kilit: 0, titresim: 0, ses: []};
  const rj = (k) => function () { window.__red[k]++; return Promise.reject(new DOMException('reddedildi', 'NotAllowedError')); };
  try { Element.prototype.requestFullscreen = rj('tamekran'); } catch (e) {}
  try { Element.prototype.webkitRequestFullscreen = rj('tamekran'); } catch (e) {}
  try { if (screen.orientation) screen.orientation.lock = rj('kilit'); } catch (e) {}
  try { navigator.vibrate = function () { window.__red.titresim++; return false; }; } catch (e) {}
  // AudioContext izleme: baslangic durumu ve ilk dokunustan sonraki durum
  const AC = window.AudioContext || window.webkitAudioContext;
  if (AC) {
    const W = class extends AC {
      constructor(...a) { super(...a); const k = {ilk: this.state, resume: 0, olusma: performance.now(), ctx: this}; window.__red.ses.push(k);
        this.__k = k; const r = this.resume.bind(this); this.resume = () => { k.resume++; return r(); }; }
    };
    window.AudioContext = W; window.webkitAudioContext = W;
    window.__sesDurumlari = () => window.__red.ses.map(k => k);
  }
})();
"""


def baglam_ac(br, dpr=DPR, mobil=True, fps=True, reddet=True):
    ctx = br.new_context(viewport=GORUNUM, device_scale_factor=dpr, is_mobile=mobil, has_touch=mobil,
                         user_agent="Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 Chrome/120 Mobile Safari/537.36")
    if reddet:
        ctx.add_init_script(RED_JS)
    if fps:
        ctx.add_init_script(FPS_JS)
    return ctx


def sayfa_ac(ctx, url, hatalar=None, bekle_kanca=True, zaman=15000):
    """Sayfayi acar, konsol hata ve sayfa hatalarini 'hatalar' listesine toplar."""
    pg = ctx.new_page()
    if hatalar is not None:
        pg.on("console", lambda m: hatalar.append(("console." + m.type, m.text)) if m.type == "error" else None)
        pg.on("pageerror", lambda e: hatalar.append(("pageerror", str(e))))
        pg.on("requestfailed", lambda r: hatalar.append(("requestfailed", r.url)))
    r = pg.goto(url, wait_until="load", timeout=zaman)
    if r is None or r.status >= 400:
        dur(f"Sayfa yuklenemedi ({r.status if r else '?'}): {url}")
    if bekle_kanca:
        try:
            pg.wait_for_function("typeof window.__oyun === 'object' && window.__oyun !== null", timeout=zaman)
        except Exception:
            dur("window.__oyun yok (TASARIM.md 17.2). Kanca eksik: sayfa kancalari acmiyor.")
    return pg


def kanca_denetle(pg):
    """Eksik __oyun alanlarini dondurur."""
    return pg.evaluate("(g) => g.filter(k => !(k in window.__oyun))", GEREKLI_KANCALAR)


def kanca_sart(pg, gerekli):
    eksik = pg.evaluate("(g) => g.filter(k => !(k in window.__oyun))", gerekli)
    if eksik:
        dur("Eksik kanca(lar): window.__oyun." + ", ".join(eksik))


def fps_oku(pg):
    return pg.evaluate("""() => { const F = window.__fps; if (!F) return null;
      const s = F.ornek.slice(2).sort((a,b)=>a-b); if (!s.length) return null;
      const ort = s.reduce((a,b)=>a+b,0)/s.length;
      return {kare: F.kare, ort_fps: 1000/ort, min_fps: 1000/s[s.length-1], p95_ms: s[Math.floor(s.length*0.95)], en_uzun_ms: F.en_uzun}; }""")


def json_yaz(yol, veri):
    Path(yol).parent.mkdir(parents=True, exist_ok=True)
    Path(yol).write_text(json.dumps(veri, ensure_ascii=False, indent=1), encoding="utf-8")


def ortak_arg(ap):
    ap.add_argument("--sayfa", default=None, help="varsayilan oyun/b0/index.html; ornek: testci/sahte.html")
    ap.add_argument("--port", type=int, default=0)
    ap.add_argument("--gorunum", default="384x832")
    return ap


def ses_durumu(pg):
    """AudioContext'lerin simdiki durumu ve ilk durumu (RED_JS izlemesi)."""
    return pg.evaluate("""() => { const r = window.__red; if (!r) return null; return {sayi: r.ses.length, ilk: r.ses.map(k=>k.ilk), simdi_ac: r.ses.map(k=>k.ctx.state), resume: r.ses.map(k=>k.resume),
      simdi: (window.__oyun && window.__oyun.sesDurum) ? window.__oyun.sesDurum() : null,
      tamekran: r.tamekran, kilit: r.kilit, titresim: r.titresim}; }""")
