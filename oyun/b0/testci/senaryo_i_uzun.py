#!/usr/bin/env python3
"""(i) 5 dakika surekli canli oyun (bot=orta, hiz=1, gercek zaman): fps, JS heap, DOM dugum, tur sayisi."""
import time, json, sys
from playwright.sync_api import sync_playwright
import ortak as o
from senaryo_ortak import *
SURE = float(sys.argv[1]) if len(sys.argv) > 1 else 300
with o.sunucu() as taban, sync_playwright() as p:
    br, ctx, pg, hat = yeni(p, "bot=orta&seed=5", taban)
    cdp = ctx.new_cdp_session(pg); cdp.send("Performance.enable")
    def m():
        d = {x["name"]: x["value"] for x in cdp.send("Performance.getMetrics")["metrics"]}
        return d
    pg.evaluate("window.__fps.ornek.length=0; window.__fps.kare=0")
    ornekler = []; tur = 0; sonasama = None; t0 = time.time(); sonolcum = t0
    pg.mouse.click(190, 400)
    while time.time() - t0 < SURE:
        a = durum(pg)["asama"]
        if a == "KARA_KUTU":
            pg.wait_for_timeout(1200)
            if tikla_metin(pg, r"TEKRAR"): tur += 1
            pg.wait_for_timeout(300)
        elif a == "HANGAR":
            tikla_metin(pg, r"^\s*UÇ\s*$"); pg.wait_for_timeout(300)
        else:
            pg.wait_for_timeout(250)
        if time.time() - sonolcum >= 20:
            sonolcum = time.time()
            f = pg.evaluate("""() => { const F = window.__fps; const s = F.ornek.slice(); F.ornek.length = 0; s.sort((a,b)=>a-b);
              return s.length ? {ort: 1000/(s.reduce((a,b)=>a+b,0)/s.length), p99_ms: s[Math.floor(s.length*.99)], max_ms: s[s.length-1], n: s.length} : null; }""")
            mm = m()
            ornekler.append({"t": round(sonolcum - t0), "tur": tur, "fps": f, "heap_MB": round(mm["JSHeapUsedSize"] / 1e6, 1), "dom": int(mm["Nodes"]), "listener": int(mm["JSEventListeners"]), "pr": durum(pg)["pr"], "asama": a})
            print(ornekler[-1], flush=True)
    pg.screenshot(path=str(SS / "i_son.png"))
    out = {"sure": SURE, "tur": tur, "ornekler": ornekler, "hata": [list(h) for h in hat], "kayit_tur": pg.evaluate("window.__oyun.kayit.oku().tur"), "jeton": pg.evaluate("window.__oyun.kayit.oku().jeton")}
    br.close()
o.json_yaz(o.CIKTI / "senaryo_i.json", out)
print(json.dumps({k: v for k, v in out.items() if k != "ornekler"}, ensure_ascii=False))
