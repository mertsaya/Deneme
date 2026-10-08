#!/usr/bin/env python3
"""(a) hic dokunmadan 3 tur; (b) spam; (c) yalniz rampada dokun. Canli (gercek zamanli) oyun, kayit acik."""
import sys, time, json
from playwright.sync_api import sync_playwright
import ortak as o
from senaryo_ortak import *

MOD = sys.argv[1]  # hic | spam | rampa
SONUC = {"mod": MOD, "turlar": []}

def kk_oku(pg):
    return pg.evaluate("document.getElementById('karakutu').innerText")

with o.sunucu() as taban, sync_playwright() as p:
    br, ctx, pg, hat = yeni(p, "seed=11", taban)
    t0 = time.time()
    if MOD == "spam":
        pg.mouse.click(190, 400)  # sesi/ilk dokunus baslatici
        pg.evaluate(SPAM_JS)
    for tur in range(3):
        kayit = {"tur": tur + 1, "olay_t": [], "ss": []}
        # RAMPA bekle
        try:
            bekle_asama(pg, "RAMPA", 20000)
        except Exception:
            kayit["not"] = "RAMPA gelmedi: " + str(durum(pg)["asama"])
        tR = time.time()
        d = durum(pg)
        if MOD == "hic" and tur == 0:
            pg.screenshot(path=str(SS / "a_hic_rampa.png"))
        if MOD == "rampa":
            # rampada yesilde dokun: p>0.84 civari. iglenin konumunu rampa_t'den tahmin etmeden: sabit gecikmeyle deneme
            pg.wait_for_timeout(840)
            pg.mouse.click(190, 400)
        # ucus
        ilk5 = None
        try:
            if MOD != "rampa":
                pg.wait_for_function("window.__oyun.durum().asama==='UCUS'", timeout=8000)
            else:
                pg.wait_for_function("window.__oyun.durum().asama==='UCUS'", timeout=8000)
        except Exception:
            kayit["not"] = "UCUS gelmedi"
        tU = time.time(); kayit["rampa_gercek_s"] = round(tU - tR, 2)
        pg.wait_for_timeout(5000)
        ev5 = pg.evaluate("window.__oyun.olaylar.filter(e=>e[0]<=5).map(e=>e[1])")
        kayit["ilk5s_olay"] = ev5
        if tur == 0:
            pg.screenshot(path=str(SS / f"{MOD}_t5s.png"))
        # en yavas an: surekli ornekle
        en_yavas = [1e9, None]
        mx = 0
        while True:
            d = durum(pg)
            if d["asama"] in ("BITIS", "KARA_KUTU"): break
            v = (d["vx"] ** 2 + d["vy"] ** 2) ** .5
            mx = max(mx, v)
            if d["asama"] == "UCUS" and d["t"] > 3 and v < en_yavas[0]:
                en_yavas = [v, d["t"]]
            pg.wait_for_timeout(120)
            if time.time() - tU > 80: kayit["not"] = "tur 80 s'de bitmedi"; break
        kayit["ucus_gercek_s"] = round(time.time() - tU, 1); kayit["max_v_ornek"] = round(mx, 1)
        kayit["en_yavas"] = en_yavas
        if tur == 0:
            try: bekle_asama(pg, "KARA_KUTU", 8000)
            except Exception: pass
            pg.wait_for_timeout(2500)
            pg.screenshot(path=str(SS / f"{MOD}_karakutu.png"))
        else:
            try: bekle_asama(pg, "KARA_KUTU", 8000)
            except Exception: pass
            pg.wait_for_timeout(2500)
        kayit["kk"] = kk_oku(pg)[:400]
        kayit["res"] = pg.evaluate("({sonuc:null, jeton: window.__oyun.durum().jeton, tur: window.__oyun.durum().tur})")
        if MOD == "spam":
            kayit["spam_n"] = pg.evaluate("window.__spam")
        SONUC["turlar"].append(kayit)
        if tur < 2:
            if not tikla_metin(pg, r"TEKRAR"): kayit["not2"] = "TEKRAR UC bulunamadi"
            if MOD == "spam": pass
    SONUC["fps"] = o.fps_oku(pg)
    SONUC["kayit"] = pg.evaluate("window.__oyun.kayit.oku()")
    SONUC["hata"] = [list(h) for h in hat]
    SONUC["sure_s"] = round(time.time() - t0, 1)
    br.close()
o.json_yaz(o.CIKTI / f"senaryo_{MOD}.json", SONUC)
print(json.dumps(SONUC, ensure_ascii=False, indent=1)[:5000])
