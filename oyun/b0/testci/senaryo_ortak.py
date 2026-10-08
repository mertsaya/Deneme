"""Senaryo yardimcilari (oyun kodu degismez)."""
import json, time, re
from playwright.sync_api import sync_playwright
import ortak as o

SS = o.CIKTI / "senaryo"
SS.mkdir(parents=True, exist_ok=True)

def durum(pg):
    return pg.evaluate("window.__oyun.durum()")

def bekle_asama(pg, asama, zaman=90000):
    pg.wait_for_function("(a)=>window.__oyun.durum().asama===a", arg=asama, timeout=zaman)

def tikla_metin(pg, desen):
    for el in pg.get_by_text(re.compile(desen, re.I)).all():
        if el.is_visible():
            el.click(timeout=3000); return True
    return False

def yeni(p, url_sorgu, taban, w=384, h=832, dpr=2, ctx_kw=None):
    br = o.tarayici_baslat(p)
    o.GORUNUM.update(width=w, height=h)
    ctx = o.baglam_ac(br, dpr=dpr)
    hatalar = []
    pg = o.sayfa_ac(ctx, f"{taban}/index.html" + (("?" + url_sorgu) if url_sorgu else ""), hatalar)
    return br, ctx, pg, hatalar

SPAM_JS = """() => { window.__spam = 0; const f = () => { if (window.__spamDur) return;
  document.body.dispatchEvent(new PointerEvent('pointerdown', {isPrimary: true, bubbles: true, pointerType: 'touch', clientX: 190, clientY: 400}));
  window.__spam++; requestAnimationFrame(f); }; requestAnimationFrame(f); }"""

# ilk 5 s olay metrikleri
def olay_ozet(pg):
    return pg.evaluate("window.__oyun.olaylar")
