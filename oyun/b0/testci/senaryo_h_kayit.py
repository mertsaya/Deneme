#!/usr/bin/env python3
"""(h) hizli ardisik 10 tur: kayit tutarliligi (jeton, tur, son[], rekor, kk toplami)."""
import json, re
from playwright.sync_api import sync_playwright
import ortak as o
from senaryo_ortak import *
rows = []
with o.sunucu() as taban, sync_playwright() as p:
    br, ctx, pg, hat = yeni(p, "bot=iyi&seed=31&hiz=8", taban)
    K = pg.evaluate("window.__oyun.kayit.oku()"); prev = K["jeton"]
    for i in range(10):
        bekle_asama(pg, "KARA_KUTU", 90000); pg.wait_for_timeout(300)
        # animasyon bitmeden kapat: hemen TEKRAR (kilit 0,3 s)
        pg.wait_for_timeout(2200)
        kk = pg.evaluate("document.getElementById('kkToplam').innerText"); K = pg.evaluate("window.__oyun.kayit.oku()")
        dok = pg.evaluate("document.getElementById('kkDokum').innerText")
        num = int(re.sub(r"\D", "", kk) or -1)
        rows.append({"tur": i + 1, "kayit_tur": K["tur"], "jeton_fark": K["jeton"] - prev, "kk_toplam": num, "fark_esit": (K["jeton"] - prev) == num, "son": K["son"], "bekleyen": K["bekleyen"], "elle": K.get("elle"), "rekor": K["rekor"]})
        prev = K["jeton"]
        tikla_metin(pg, r"TEKRAR")
        pg.wait_for_timeout(100)
    # son turlarin kayit zinciri
    # reload sonrasi ayni mi
    Ka = pg.evaluate("window.__oyun.kayit.oku()")
    pg.reload(wait_until="load"); pg.wait_for_timeout(1500)
    Kb = pg.evaluate("window.__oyun.kayit.oku()")
    out = {"satirlar": rows, "reload_ayni": Ka["jeton"] == Kb["jeton"] and Ka["tur"] == Kb["tur"], "Ka": [Ka["jeton"], Ka["tur"]], "Kb": [Kb["jeton"], Kb["tur"]], "hata": [list(h) for h in hat]}
    br.close()
o.json_yaz(o.CIKTI / "senaryo_h.json", out)
for r in rows: print(r)
print({k: v for k, v in out.items() if k != "satirlar"})
