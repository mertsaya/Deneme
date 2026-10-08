#!/usr/bin/env python3
"""bot_tur.py: botlarla n tur (gorüntüsüz, window.__oyun.tur) + istege bagli kampanya.
Kullanim: python3 bot_tur.py [--botlar iyi,orta,kotu,hic] [--n 20] [--seed 1] [--kampanya 15] [--sv rampa:3,dalis:2] [--tipler ...]
Gerekli kancalar: __oyun.tur ; --kampanya icin __oyun.kampanya. Cikti: cikti/bot_tur.json
"""
import argparse, statistics as st
from playwright.sync_api import sync_playwright
import ortak as o

JS_TUR = """([botlar, n, seed, sv, turNo]) => {
  const out = {};
  for (const b of botlar) { out[b] = [];
    for (let i = 0; i < n; i++) out[b].push(window.__oyun.tur(seed + i, Object.assign({}, sv), b, turNo)); }
  return out; }"""
JS_KAMP = "([b, seed, n]) => window.__oyun.kampanya(seed, b, n)"
ANAHTAR = ["sure_tur", "mesafe", "mesafe_g", "kazanc", "max_v", "max_y", "vay_t", "sekme", "mukemmel", "dalis", "son_sans", "firsat", "firsat_tut"]


def ort(a):
    a = [x for x in a if isinstance(x, (int, float))]
    return sum(a) / len(a) if a else None


def med(a):
    a = [x for x in a if isinstance(x, (int, float))]
    return st.median(a) if a else None


def ozet(rs):
    d = {"n": len(rs)}
    for k in ANAHTAR:
        v = [r.get(k) for r in rs]
        d[k] = {"ort": ort(v), "medyan": med(v), "min": min([x for x in v if x is not None], default=None),
                "maks": max([x for x in v if x is not None], default=None)}
    d["vay_5s_oran"] = sum(1 for r in rs if r.get("vay_t") is not None and r["vay_t"] <= 5) / len(rs)
    d["bitis"] = {}
    for r in rs:
        d["bitis"][r.get("bitis")] = d["bitis"].get(r.get("bitis"), 0) + 1
    d["sure_65_cakan"] = sum(1 for r in rs if (r.get("sure_tur") or 0) >= 65 or r.get("bitis") == "sure")
    return d


def sv_coz(s):
    out = {}
    for p in (s or "").split(","):
        if ":" in p:
            k, v = p.split(":")
            out[k] = int(v)
    return out


def kamp_ozet(k):
    t = k.get("turlar", [])
    sure = [x.get("sure") for x in t[4:15]]
    return {"ilk": k.get("ilk"), "en_uzun_yok": k.get("en_uzun_yok"), "tur_sayisi": len(t),
            "ilk5_alim_olmayan": [x["tur"] for x in t[:5] if not x.get("al")],
            "tur5_15_sure_medyan": med(sure), "tavana_carpan": sum(1 for x in t if x.get("bitis") == "sure"),
            "tur5_sv": (t[4].get("sv") if len(t) >= 5 else None),
            "alim_turlari": [x["tur"] for x in t if x.get("al")]}


def calis(taban, dosya, botlar, n, seed, sv, kamp, tipler, sorgu_ek=""):
    hatalar = []
    q = "kayit=0&seed=%d" % seed + (("&tipler=" + tipler) if tipler else "") + (("&" + sorgu_ek) if sorgu_ek else "")
    with sync_playwright() as p:
        br = o.tarayici_baslat(p)
        ctx = o.baglam_ac(br, fps=False)
        pg = o.sayfa_ac(ctx, o.sayfa_url(taban, dosya, q), hatalar)
        o.kanca_sart(pg, ["tur"] + (["kampanya"] if kamp else []))
        ham = pg.evaluate(JS_TUR, [botlar, n, seed, sv, 1])
        res = {"ayar": dict(botlar=botlar, n=n, seed=seed, sv=sv, tipler=tipler), "botlar": {}}
        for b in botlar:
            res["botlar"][b] = ozet(ham[b])
            res["botlar"][b]["ham"] = [{k: r.get(k) for k in ANAHTAR + ["bitis", "duvar"]} for r in ham[b]]
        if kamp:
            res["kampanya"] = {}
            for b in botlar:
                if b == "kotu" and False:
                    continue
                res["kampanya"][b] = kamp_ozet(pg.evaluate(JS_KAMP, [b, seed, kamp]))
        br.close()
    res["konsol_hata"] = [list(h) for h in hatalar]
    return res


def tablo(res):
    s = ["bot   | sure ort | mesafe ort | mesafe_g | kazanc | max_v | vay<=5s | bitis"]
    for b, d in res["botlar"].items():
        f = lambda k: d[k]["ort"] if d[k]["ort"] is not None else float("nan")
        s.append(f"{b:5s} | {f('sure_tur'):8.1f} | {f('mesafe'):10.0f} | {f('mesafe_g'):8.2f} | {f('kazanc'):6.1f} | {f('max_v'):5.0f} | %{d['vay_5s_oran']*100:3.0f}   | {d['bitis']}")
    for b, k in res.get("kampanya", {}).items():
        s.append(f"kampanya {b}: ilk esikler={k['ilk']} alisverissiz-en-uzun={k['en_uzun_yok']} t5-15 sure medyan={k['tur5_15_sure_medyan']}")
    return "\n".join(s)


def main():
    ap = o.ortak_arg(argparse.ArgumentParser())
    ap.add_argument("--botlar", default="iyi,orta,kotu,hic")
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--sv", default="")
    ap.add_argument("--tipler", default="")
    ap.add_argument("--kampanya", type=int, default=0)
    ap.add_argument("--cikti", default="bot_tur.json")
    a = ap.parse_args()
    dosya = o.sayfa_dosyasi(a.sayfa)
    with o.sunucu(port=a.port) as taban:
        res = calis(taban, dosya, a.botlar.split(","), a.n, a.seed, sv_coz(a.sv), a.kampanya, a.tipler)
    o.json_yaz(o.CIKTI / a.cikti, res)
    print(tablo(res))
    if res["konsol_hata"]:
        print("KONSOL HATALARI:", res["konsol_hata"][:5])
    print("yazildi:", o.CIKTI / a.cikti)


if __name__ == "__main__":
    main()
