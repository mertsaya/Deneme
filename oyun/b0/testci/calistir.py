#!/usr/bin/env python3
"""calistir.py: yerel http.server + 384x832 DPR2 mobil gorunum; konsol hatalari, fps, kanca ve
tam ekran/kilit/titresim reddi + AudioContext (suspended -> ilk dokunusta calisir) denetimi.

Kullanim:  python3 calistir.py [--sayfa index.html] [--sorgu "bot=iyi&seed=3&kayit=0"] [--sure 8]
Cikti: cikti/calistir.json ; cikis kodu 1 = konsol hatasi / kanca eksigi / ses sorunu.
"""
import argparse, sys
from playwright.sync_api import sync_playwright
import ortak as o


def calis(taban, dosya, sorgu, sure, reddet=True):
    hatalar, sonuc = [], {}
    with sync_playwright() as p:
        br = o.tarayici_baslat(p)
        ctx = o.baglam_ac(br, reddet=reddet)
        pg = o.sayfa_ac(ctx, o.sayfa_url(taban, dosya, sorgu), hatalar)
        sonuc["eksik_kanca"] = o.kanca_denetle(pg)
        sonuc["ses_once"] = o.ses_durumu(pg)           # dokunustan ONCE: AudioContext yok ya da suspended olmali
        pg.wait_for_timeout(500)
        d0 = pg.evaluate("window.__oyun.durum && window.__oyun.durum()")
        pg.mouse.click(190, 400)                        # ilk dokunus (gercek fare/dokunma olayi)
        pg.wait_for_timeout(600)
        sonuc["ses_sonra"] = o.ses_durumu(pg)
        t_bas = pg.evaluate("performance.now()")
        pg.wait_for_timeout(int(sure * 1000))
        sonuc["fps"] = o.fps_oku(pg)
        sonuc["durum_bas"], sonuc["durum_son"] = d0, pg.evaluate("window.__oyun.durum && window.__oyun.durum()")
        sonuc["baslik"] = pg.title()
        sonuc["tampon"] = pg.evaluate("({w: innerWidth, h: innerHeight, dpr: devicePixelRatio})")
        pg.screenshot(path=str(o.CIKTI / "calistir.png"))
        br.close()
    sonuc["konsol_hata"] = [list(h) for h in hatalar]
    return sonuc


def degerlendir(s):
    sorun = []
    if s["eksik_kanca"]:
        sorun.append("eksik kanca: " + ",".join(s["eksik_kanca"]))
    if s["konsol_hata"]:
        sorun.append(f"{len(s['konsol_hata'])} konsol/sayfa hatasi")
    a0, a1 = s["ses_once"], s["ses_sonra"]
    if a1 is not None:
        if a1["sayi"] == 0:
            sorun.append("ilk dokunustan sonra AudioContext olusmadi (ses calmaz)")
        else:
            if "running" in (a0["simdi_ac"] if a0 else []):
                sorun.append("AudioContext dokunustan ONCE running (tarayici izin vermis olabilir; bilgi)")
            if "running" not in a1["simdi_ac"]:
                sorun.append("ilk dokunustan sonra AudioContext running degil: " + str(a1["simdi_ac"]))
    return sorun


def main():
    ap = o.ortak_arg(argparse.ArgumentParser())
    ap.add_argument("--sorgu", default="kayit=0")
    ap.add_argument("--sure", type=float, default=6)
    ap.add_argument("--reddetme", action="store_true", help="tam ekran/kilit/titresim reddini kapat")
    a = ap.parse_args()
    dosya = o.sayfa_dosyasi(a.sayfa)
    with o.sunucu(port=a.port) as taban:
        s = calis(taban, dosya, a.sorgu, a.sure, reddet=not a.reddetme)
    s["sorunlar"] = degerlendir(s)
    o.json_yaz(o.CIKTI / "calistir.json", s)
    f = s["fps"] or {}
    print(f"sayfa={dosya.name}  fps ort={f.get('ort_fps', 0):.1f} min={f.get('min_fps', 0):.1f}  konsol hata={len(s['konsol_hata'])}")
    print("ses once:", s["ses_once"] and s["ses_once"]["simdi_ac"], " sonra:", s["ses_sonra"] and s["ses_sonra"]["simdi_ac"])
    print("reddedilen API cagrilari:", s["ses_sonra"] and {k: s["ses_sonra"][k] for k in ("tamekran", "kilit", "titresim")})
    for h in s["konsol_hata"][:10]:
        print("  !", h)
    for x in s["sorunlar"]:
        print("SORUN:", x)
    print("OK" if not s["sorunlar"] else "KALDI")
    sys.exit(1 if s["sorunlar"] else 0)


if __name__ == "__main__":
    main()
