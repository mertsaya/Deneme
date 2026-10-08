#!/usr/bin/env python3
"""Olculebilir his gostergeleri: ilk 5 s olay sayisi, ilk dokunus tepkisi (pointerdown -> sonraki kare degisimi), tur suresi dagilimi, olu zaman."""
import json, statistics as st, collections, time
from playwright.sync_api import sync_playwright
import ortak as o
from senaryo_ortak import *
out = {}
with o.sunucu() as taban, sync_playwright() as p:
    br, ctx, pg, hat = yeni(p, "kayit=0&seed=1", taban)
    for bot in ["iyi", "orta", "kotu", "hic"]:
        rows = []
        for s in range(1, 21):
            r = pg.evaluate("([s,b])=>{const r=window.__oyun.tur(s,{},b,1); return {r, ol: window.__oyun.olaylar}}", [s, bot])
            ol = r["ol"]; sonuc = r["r"]
            rampa = (sonuc["sure_tur"] or 0) - (sonuc["sure_ucus"] or 0)
            tipler = collections.Counter(e[1] for e in ol if isinstance(e[0], (int, float)) and e[0] <= 5)
            rows.append({"sure_tur": sonuc["sure_tur"], "rampa": rampa, "ilk5": sum(tipler.values()), "tipler": dict(tipler), "ilk_olay_t": min([e[0] for e in ol if e[1] in ("sekme", "temas", "marti", "ip")] or [None], default=None) if ol else None,
                         "tum_tipler": sorted(set(e[1] for e in ol))})
        sure = [x["sure_tur"] for x in rows]
        out[bot] = {"sure_ort": st.mean(sure), "sure_min": min(sure), "sure_max": max(sure), "sure_med": st.median(sure),
                    "ilk5_olay_ort": st.mean(x["ilk5"] for x in rows), "ilk5_olay_min": min(x["ilk5"] for x in rows),
                    "ilk_olay_t_ort": st.mean([x["ilk_olay_t"] for x in rows if x["ilk_olay_t"] is not None] or [0]),
                    "olay_tipleri": rows[0]["tum_tipler"], "tipler_ilk5_ornek": rows[0]["tipler"]}
        print(bot, json.dumps(out[bot], ensure_ascii=False), flush=True)
    br.close()
# canli: tepki suresi
with o.sunucu() as taban, sync_playwright() as p:
    br, ctx, pg, hat = yeni(p, "kayit=0&seed=4", taban)
    pg.wait_for_timeout(1000); pg.mouse.click(190, 400); pg.wait_for_timeout(500)
    JS = """() => new Promise(res => {
      const kay = {};
      // rampa dokunusu
      const ilk = () => { const d = window.__oyun.durum(); if (d.asama !== 'RAMPA') return requestAnimationFrame(ilk);
         if (d.rampa_t % 2 < 0.88) return requestAnimationFrame(ilk);
         const t0 = performance.now(); document.body.dispatchEvent(new PointerEvent('pointerdown',{isPrimary:true,bubbles:true,pointerType:'touch',clientX:190,clientY:400}));
         const iz = () => { const e = window.__oyun.durum(); if (e.asama !== 'RAMPA') { kay.rampa_tepki_ms = performance.now() - t0; return dalis(); } requestAnimationFrame(iz); }; iz(); };
      const dalis = () => { const w = () => { const d = window.__oyun.durum(); if (d.asama === 'UCUS' && d.gosterge >= 1 && d.t > 1.5 && !window.__oyun.durum().halka) {
          const g0 = d.gosterge, vy0 = d.vy, t0 = performance.now(); document.body.dispatchEvent(new PointerEvent('pointerdown',{isPrimary:true,bubbles:true,pointerType:'touch',clientX:190,clientY:400}));
          const iz = () => { const e = window.__oyun.durum(); if (e.gosterge < g0 - 0.5 || e.vy < vy0 - 5 || Math.abs(e.vy - vy0) > 5) { kay.dalis_tepki_ms = performance.now() - t0; kay.dalis_g = [g0, e.gosterge]; return res(kay); } if (performance.now() - t0 > 1000) { kay.dalis_tepki_ms = null; return res(kay); } requestAnimationFrame(iz); }; iz();
        } else if (d.asama !== 'UCUS') { kay.dalis_tepki_ms = 'ucus bitti'; res(kay); } else requestAnimationFrame(w); }; w(); };
      ilk(); })"""
    out["tepki"] = pg.evaluate(JS)
    print(out["tepki"])
    # olu zaman: kara kutu -> TEKRAR -> igne hareketi
    bekle_asama(pg, "BITIS", 90000)
    t_bitis = time.time(); bekle_asama(pg, "KARA_KUTU", 5000); t_kk = time.time()
    pg.wait_for_timeout(500)
    t1 = time.time(); tikla_metin(pg, r"TEKRAR"); pg.wait_for_function("window.__oyun.durum().asama==='RAMPA'", timeout=5000)
    t2 = time.time()
    out["olu_zaman"] = {"bitis_to_kk_s": round(t_kk - t_bitis, 2), "kk_gosterim_to_tikla_s(0.5 bekleme)": 0.5, "tikla_to_rampa_s": round(t2 - t1, 2)}
    out["hata"] = [list(h) for h in hat]
    br.close()
o.json_yaz(o.CIKTI / "senaryo_his.json", out)
print(out["olu_zaman"], out["hata"])
