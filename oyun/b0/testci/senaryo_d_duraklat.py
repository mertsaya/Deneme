#!/usr/bin/env python3
"""(d) duraklat->devam->yeniden basla ; (e) visibilitychange ortasinda tur."""
import time, json
from playwright.sync_api import sync_playwright
import ortak as o
from senaryo_ortak import *
R = {"d": {}, "e": {}}
GIZLE = "(h)=>{ Object.defineProperty(document,'hidden',{configurable:true,get:()=>h}); Object.defineProperty(document,'visibilityState',{configurable:true,get:()=>h?'hidden':'visible'}); document.dispatchEvent(new Event('visibilitychange')); }"
TAP = "document.body.dispatchEvent(new PointerEvent('pointerdown',{isPrimary:true,bubbles:true,pointerType:'touch',clientX:190,clientY:400}))"

def baslat_ucus(pg, bekle_s=3.0):
    pg.wait_for_timeout(1200); pg.mouse.click(190, 400)  # ilk dokunus
    pg.wait_for_timeout(300)
    pg.evaluate("""() => new Promise(r => { const f = () => { const d = window.__oyun.durum(); if (d.asama !== 'RAMPA') return r(); if (d.rampa_t % 2 >= 0.88) { document.body.dispatchEvent(new PointerEvent('pointerdown',{isPrimary:true,bubbles:true,pointerType:'touch',clientX:190,clientY:400})); return r(); } requestAnimationFrame(f); }; f(); })""")
    pg.wait_for_function("(s)=>{const d=window.__oyun.durum(); return d.asama==='UCUS' && d.t>=s}", arg=bekle_s, timeout=20000)

with o.sunucu() as taban, sync_playwright() as p:
    # ---------- (d)
    br, ctx, pg, hat = yeni(p, "seed=21", taban)
    baslat_ucus(pg, 3.0)
    d0 = durum(pg); J0 = d0["jeton"]
    pg.click("#durBtn"); pg.wait_for_timeout(500)
    d1 = durum(pg); pg.wait_for_timeout(1500); d2 = durum(pg)
    R["d"]["duraklatta_x_degisti"] = d2["x"] != d1["x"]; R["d"]["duraklat_bayrak"] = d1["duraklat"]
    pg.screenshot(path=str(SS / "d_menu.png"))
    R["d"]["menu_metin"] = pg.evaluate("document.getElementById('menu').innerText")
    # ekrana (menu disi) dokunus: dalis olmamali
    g0 = durum(pg)["gosterge"]; pg.mouse.click(30, 120); pg.wait_for_timeout(200)
    R["d"]["menude_dokunus_dalis"] = durum(pg)["gosterge"] != g0
    pg.click("#mDevam"); pg.wait_for_timeout(250)
    pg.screenshot(path=str(SS / "d_sayim.png"))
    ds = durum(pg); pg.mouse.click(30, 120); pg.wait_for_timeout(100)
    R["d"]["sayimda_dalis"] = durum(pg)["gosterge"] != ds["gosterge"]
    R["d"]["sayimda_x_ilerledi"] = durum(pg)["x"] != ds["x"]
    pg.wait_for_timeout(1800)
    d3 = durum(pg); R["d"]["devamdan_sonra_duraklat"] = d3["duraklat"]; R["d"]["devamdan_sonra_x_ilerliyor"] = d3["x"] > ds["x"]
    pg.screenshot(path=str(SS / "d_devam_sonrasi.png"))
    # duraklat -> devam -> hemen tekrar duraklat (yaris)
    pg.click("#durBtn"); pg.wait_for_timeout(100); pg.click("#mDevam"); pg.wait_for_timeout(100)
    try:
        pg.click("#durBtn", timeout=1500); R["d"]["sayim_sirasinda_duraklat_dugmesi"] = "tiklandi: duraklat=%s" % durum(pg)["duraklat"]
    except Exception as e:
        R["d"]["sayim_sirasinda_duraklat_dugmesi"] = "tiklanamadi (sayim kaplamasi?)"
    pg.screenshot(path=str(SS / "d_sayim_duraklat.png"))
    pg.wait_for_timeout(2500)
    ds2 = durum(pg); R["d"]["son_durum"] = {k: ds2[k] for k in ["asama", "duraklat"]}
    if not ds2["duraklat"]:
        pg.click("#durBtn"); pg.wait_for_timeout(300)
    K0 = pg.evaluate("window.__oyun.kayit.oku()")
    pg.click("#mYeniden"); pg.wait_for_timeout(700)
    K1 = pg.evaluate("window.__oyun.kayit.oku()"); d4 = durum(pg)
    R["d"]["yeniden_sonrasi"] = {"asama": d4["asama"], "duraklat": d4["duraklat"], "jeton_once": K0["jeton"], "jeton_sonra": K1["jeton"], "tur_once": K0["tur"], "tur_sonra": K1["tur"], "elle": K1.get("elle")}
    pg.screenshot(path=str(SS / "d_yeniden.png"))
    R["d"]["yeniden_bildirim"] = pg.evaluate("document.getElementById('bildirim').innerText")
    # rampada duraklat
    pg.wait_for_function("window.__oyun.durum().asama==='RAMPA'", timeout=5000)
    t_a = durum(pg)["rampa_t"]; pg.click("#durBtn"); pg.wait_for_timeout(800); t_b = durum(pg)["rampa_t"]
    R["d"]["rampada_duraklat_igne_durdu"] = abs(t_b - t_a) < 0.1
    pg.click("#mDevam"); pg.wait_for_timeout(2200)
    R["d"]["rampa_devam_asama"] = durum(pg)["asama"]
    # HANGAR
    pg.wait_for_function("window.__oyun.durum().asama==='UCUS'", timeout=8000); pg.wait_for_timeout(1500)
    pg.click("#durBtn"); pg.wait_for_timeout(300); pg.click("#mHangar"); pg.wait_for_timeout(700)
    d5 = durum(pg); R["d"]["hangar_asama"] = d5["asama"]; R["d"]["hangar_jeton"] = d5["jeton"]
    pg.screenshot(path=str(SS / "d_hangar.png"))
    # hangar -> UC
    pg.click("#ucBtn"); pg.wait_for_timeout(1500)
    R["d"]["hangardan_uc"] = durum(pg)["asama"]
    R["d"]["hata"] = [list(h) for h in hat]
    br.close()

    # ---------- (e) visibilitychange
    br, ctx, pg, hat = yeni(p, "seed=22", taban)
    baslat_ucus(pg, 4.0)
    xa = durum(pg)["x"]
    pg.evaluate(GIZLE, True); pg.wait_for_timeout(300)
    K = pg.evaluate("window.__oyun.kayit.oku()"); dg = durum(pg)
    R["e"]["gizlenince"] = {"duraklat": dg["duraklat"], "bekleyen": K["bekleyen"], "jeton": K["jeton"]}
    pg.wait_for_timeout(2000); R["e"]["gizliyken_x_ilerledi"] = durum(pg)["x"] != dg["x"]
    pg.evaluate(GIZLE, False); pg.wait_for_timeout(500)
    K = pg.evaluate("window.__oyun.kayit.oku()"); dv = durum(pg)
    R["e"]["gorununce"] = {"duraklat": dv["duraklat"], "bekleyen": K["bekleyen"], "asama": dv["asama"]}
    pg.screenshot(path=str(SS / "e_gorunur_menu.png"))
    # gizle->gorun->gizle (cift): bekleyen tek
    pg.evaluate(GIZLE, True); pg.wait_for_timeout(100); pg.evaluate(GIZLE, False); pg.wait_for_timeout(100)
    K = pg.evaluate("window.__oyun.kayit.oku()"); R["e"]["cift_gizle_bekleyen"] = K["bekleyen"]
    pg.click("#mDevam"); pg.wait_for_timeout(2500)
    # turu bitir, jeton farki == karakutu toplami mi
    J_once = pg.evaluate("window.__oyun.kayit.oku().jeton")
    bekle_asama(pg, "KARA_KUTU", 90000); pg.wait_for_timeout(2500)
    kk = pg.evaluate("document.getElementById('kkToplam').innerText")
    J_sonra = pg.evaluate("window.__oyun.kayit.oku().jeton")
    R["e"]["tur_sonu"] = {"jeton_once": J_once, "jeton_sonra": J_sonra, "kk_toplam_metin": kk, "bekleyen": pg.evaluate("window.__oyun.kayit.oku().bekleyen")}
    pg.screenshot(path=str(SS / "e_tur_sonu.png"))
    # gizliyken oldurulme: yeni tur, hidden, sayfayi yeniden yukle
    tikla_metin(pg, r"TEKRAR"); pg.wait_for_timeout(600)
    pg.evaluate("""() => new Promise(r => { const f = () => { const d = window.__oyun.durum(); if (d.asama !== 'RAMPA') return r(); if (d.rampa_t % 2 >= 0.88) { document.body.dispatchEvent(new PointerEvent('pointerdown',{isPrimary:true,bubbles:true,pointerType:'touch',clientX:190,clientY:400})); return r(); } requestAnimationFrame(f); }; f(); })""")
    pg.wait_for_function("window.__oyun.durum().asama==='UCUS' && window.__oyun.durum().t>4", timeout=20000)
    Jx = pg.evaluate("window.__oyun.kayit.oku().jeton")
    pg.evaluate(GIZLE, True); pg.wait_for_timeout(200)
    bk = pg.evaluate("window.__oyun.kayit.oku().bekleyen")
    pg.reload(wait_until="load"); pg.wait_for_function("window.__oyun && window.__oyun.hazir", timeout=10000); pg.wait_for_timeout(700)
    K = pg.evaluate("window.__oyun.kayit.oku()")
    R["e"]["olduruldu"] = {"jeton_once": Jx, "bekleyen_yazildi": bk, "reload_sonrasi_jeton": K["jeton"], "bekleyen": K["bekleyen"], "asama": durum(pg)["asama"], "bildirim": pg.evaluate("document.getElementById('bildirim').innerText")}
    pg.screenshot(path=str(SS / "e_olduruldu_yeniden.png"))
    pg.reload(wait_until="load"); pg.wait_for_timeout(700)
    R["e"]["ikinci_reload_jeton"] = pg.evaluate("window.__oyun.kayit.oku().jeton")
    # gizli iken RAMPA
    br2 = None
    R["e"]["hata"] = [list(h) for h in hat]
    # gercek ikinci sekme
    pg2 = ctx.new_page(); pg2.bring_to_front(); pg2.wait_for_timeout(500)
    R["e"]["gercek_sekme_hidden"] = pg.evaluate("document.hidden")
    br.close()
o.json_yaz(o.CIKTI / "senaryo_de.json", R)
print(json.dumps(R, ensure_ascii=False, indent=1))
