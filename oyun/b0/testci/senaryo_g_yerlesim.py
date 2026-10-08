#!/usr/bin/env python3
"""(g) 384x832, 360x780, 412x915 yerlesim: ekran goruntuleri + HUD cakisma / tasma denetimi."""
import json, itertools
from playwright.sync_api import sync_playwright
import ortak as o
from senaryo_ortak import *
BOYUT = [(384, 832), (360, 780), (412, 915)]
HUD = ["jeton", "mesafe", "durBtn", "irtifa", "hizg", "dalisd", "ipucu", "mesaj"]
KUTU_JS = """(ids) => { const out = {}; for (const id of ids) { const e = document.getElementById(id); if (!e) { out[id] = null; continue; }
  const cs = getComputedStyle(e); const r = e.getBoundingClientRect(); out[id] = {x: r.x, y: r.y, w: r.width, h: r.height, gorunur: r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' && !e.hidden && +cs.opacity > 0.05}; }
  const tasan = []; for (const e of document.querySelectorAll('body *')) { const r = e.getBoundingClientRect(); const cs = getComputedStyle(e); if (r.width === 0 || cs.display === 'none' || cs.visibility === 'hidden') continue;
    if (e.closest('[hidden]')) continue;
    if (e.scrollWidth > e.clientWidth + 2 && cs.overflow !== 'visible' && e.clientWidth > 0 && e.tagName !== 'CANVAS' && (e.innerText||'').trim()) tasan.push((e.id || e.className || e.tagName) + ' sw' + e.scrollWidth + '>cw' + e.clientWidth);
    if (e.tagName !== 'CANVAS' && (e.innerText||'').trim() && (r.right > innerWidth + 1 || r.left < -1 || r.bottom > innerHeight + 1) && !e.closest('canvas')) tasan.push('DISARI ' + (e.id || e.className || e.tagName) + ' ' + Math.round(r.left) + ',' + Math.round(r.top) + ',' + Math.round(r.right) + ',' + Math.round(r.bottom)); }
  return {kutular: out, tasan: tasan.slice(0, 15), vw: innerWidth, vh: innerHeight}; }"""
def cakisma(k):
    res = []
    g = {i: v for i, v in k["kutular"].items() if v and v["gorunur"]}
    for a, b in itertools.combinations(g, 2):
        A, B = g[a], g[b]
        if A["x"] < B["x"] + B["w"] and B["x"] < A["x"] + A["w"] and A["y"] < B["y"] + B["h"] and B["y"] < A["y"] + A["h"]:
            res.append(f"{a} x {b}")
    return res
out = {}
with o.sunucu() as taban, sync_playwright() as p:
    br = o.tarayici_baslat(p)
    for (w, h) in BOYUT:
        o.GORUNUM.update(width=w, height=h)
        r = {}
        for ad, q in [("rampa", "t=0.4&seed=7&bot=iyi&kayit=0"), ("ucus5", "t=5&seed=7&bot=iyi&kayit=0"), ("ucus9", "t=9&seed=7&bot=iyi&kayit=0")]:
            ctx = o.baglam_ac(br); hat = []
            pg = o.sayfa_ac(ctx, f"{taban}/index.html?{q}", hat); pg.wait_for_timeout(700)
            k = pg.evaluate(KUTU_JS, HUD)
            r[ad] = {"cakisma": cakisma(k), "tasan": k["tasan"], "hata": [list(x) for x in hat]}
            pg.screenshot(path=str(SS / f"g_{w}x{h}_{ad}.png")); ctx.close()
        # canli: kara kutu + hangar + menu + ayarlar (yazi boyutlari)
        for yazi in (1.0, 1.4):
            ctx = o.baglam_ac(br); hat = []
            ctx.add_init_script("localStorage.setItem('sdp_kayit', JSON.stringify({v:1,jeton:420,tur:4,sv:{rampa:2,dalis:1},ayar:{yazi:%s,efekt:80,titresim:true,hareket_azalt:null,isik:false,kalite:'oto'}}))" % yazi)
            pg = o.sayfa_ac(ctx, f"{taban}/index.html?bot=orta&seed=9&hiz=8", hat)
            try:
                bekle_asama(pg, "KARA_KUTU", 90000); pg.wait_for_timeout(2000)
                k = pg.evaluate(KUTU_JS, ["kkBaslik", "kkToplam", "kkDokum", "kkRekor", "kkDurduran", "kkKart", "kkHangar", "kkTekrar"])
                r[f"kk_y{yazi}"] = {"cakisma": cakisma(k), "tasan": k["tasan"]}
                pg.screenshot(path=str(SS / f"g_{w}x{h}_kk_y{yazi}.png"))
                tikla_metin(pg, r"^\s*HANGAR\s*$"); pg.wait_for_timeout(800)
                k = pg.evaluate(KUTU_JS, ["hJeton", "hRoket", "kartlar", "dislibtn", "ucBtn"])
                r[f"hangar_y{yazi}"] = {"cakisma": cakisma(k), "tasan": k["tasan"], "kutular": {a: (None if not v else [round(v['x']), round(v['y']), round(v['w']), round(v['h'])]) for a, v in k["kutular"].items()}}
                pg.screenshot(path=str(SS / f"g_{w}x{h}_hangar_y{yazi}.png"))
                pg.click("#dislibtn"); pg.wait_for_timeout(500)
                k = pg.evaluate(KUTU_JS, ["aEfekt", "aSifirla", "aKapat"]); r[f"ayar_y{yazi}"] = {"tasan": k["tasan"]}
                pg.screenshot(path=str(SS / f"g_{w}x{h}_ayar_y{yazi}.png"))
            except Exception as e:
                r[f"hata_y{yazi}"] = str(e)[:200]
            r[f"konsol_y{yazi}"] = [list(x) for x in hat]
            ctx.close()
        out[f"{w}x{h}"] = r
        print(w, h, json.dumps(r, ensure_ascii=False)[:1500], flush=True)
    br.close()
o.json_yaz(o.CIKTI / "senaryo_g.json", out)
