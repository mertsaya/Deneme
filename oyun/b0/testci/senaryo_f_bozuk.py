#!/usr/bin/env python3
"""(f) bozuk localStorage ile acilis."""
import json
from playwright.sync_api import sync_playwright
import ortak as o
from senaryo_ortak import *
VAKALAR = {
 "json_bozuk": "{bozuk",
 "null": "null",
 "dizi": "[]",
 "sayi": "42",
 "bos_nesne": "{}",
 "jeton_yazi": '{"v":1,"jeton":"abc","tur":0}',
 "jeton_eksi": '{"v":1,"jeton":-500,"tur":3,"sv":{"rampa":2}}',
 "jeton_dev": '{"v":1,"jeton":1e308,"tur":3}',
 "sv_asiri": '{"v":1,"jeton":10,"tur":3,"sv":{"rampa":99,"dalis":-4,"bolge":"x"}}',
 "surum_yeni": '{"v":99,"jeton":777,"tur":5}',
 "ayar_bozuk": '{"v":1,"jeton":10,"tur":3,"ayar":{"yazi":9,"efekt":"x","kalite":"zzz"}}',
 "son_dizi_degil": '{"v":1,"jeton":10,"tur":3,"son":"abc","son_dalis":5,"rekor":null,"duvar":3}',
 "bekleyen_garip": '{"v":1,"jeton":10,"tur":3,"bekleyen":{"j":"abc"}}',
 "bekleyen_eksi": '{"v":1,"jeton":10,"tur":3,"bekleyen":-9999}',
 "bekleyen_dev": '{"v":1,"jeton":10,"tur":3,"bekleyen":1e12}',
 "ok_kayit_tur3": '{"v":1,"jeton":200,"tur":3,"sv":{"rampa":1}}',
}
out = {}
with o.sunucu() as taban, sync_playwright() as p:
    br = o.tarayici_baslat(p)
    for ad, ham in VAKALAR.items():
        o.GORUNUM.update(width=384, height=832)
        ctx = o.baglam_ac(br)
        ctx.add_init_script("if(!sessionStorage.getItem('x')){localStorage.setItem('sdp_kayit', %s); sessionStorage.setItem('x','1');}" % json.dumps(ham))
        hat = []
        try:
            pg = o.sayfa_ac(ctx, f"{taban}/index.html?seed=3", hat)
            pg.wait_for_timeout(1500)
            K = pg.evaluate("window.__oyun.kayit.oku()"); d = durum(pg)
            r = {"asama": d["asama"], "jeton": K["jeton"], "tur": K["tur"], "sv": K["sv"], "yazi": K["ayar"]["yazi"], "kalite": K["ayar"]["kalite"],
                 "bildirim": pg.evaluate("document.getElementById('bildirim').innerText"),
                 "bozuk_anahtar": pg.evaluate("localStorage.getItem('sdp_kayit_bozuk')"), "ham_sonra": pg.evaluate("localStorage.getItem('sdp_kayit')")[:120],
                 "hata": [list(h) for h in hat]}
            # oyna: ilk dokunus + bir tur sonuna kadar (hizli degil, 25 s)
            pg.mouse.click(190, 400); pg.wait_for_timeout(1500)
            pg.mouse.click(190, 400); pg.wait_for_timeout(300)
            try:
                bekle_asama(pg, "KARA_KUTU", 70000); pg.wait_for_timeout(1500)
                K2 = pg.evaluate("window.__oyun.kayit.oku()")
                r["tur_sonu"] = {"jeton": K2["jeton"], "tur": K2["tur"], "kk": pg.evaluate("document.getElementById('kkToplam').innerText")}
            except Exception as e:
                r["tur_sonu"] = "KARA_KUTU gelmedi: " + str(durum(pg)["asama"])
            r["hata"] = [list(h) for h in hat]
            if ad in ("json_bozuk", "jeton_dev", "bekleyen_dev", "surum_yeni", "sv_asiri"):
                pg.screenshot(path=str(SS / f"f_{ad}.png"))
        except SystemExit as e:
            r = {"CÖKTÜ": str(e), "hata": [list(h) for h in hat]}
        except Exception as e:
            r = {"ISTISNA": str(e)[:200], "hata": [list(h) for h in hat]}
        out[ad] = r
        print(ad, json.dumps(r, ensure_ascii=False)[:600], flush=True)
        ctx.close()
    br.close()
o.json_yaz(o.CIKTI / "senaryo_f.json", out)
