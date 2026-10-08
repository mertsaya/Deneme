#!/usr/bin/env python3
"""kontak.py: onemli anlarda ekran goruntusu + tek kontak sayfasi PNG (cikti/kontak.png).
Anlar: rampa, kalkis, ilk sekme, sekme zinciri, dalis, ses duvari, kara kutu, hangar.
Zamanlar: headless __oyun.tur(seed,{},bot,1) olay gunlugunden (olaylar) bulunur, sonra ?t=S&bot=..&seed=.. ile
dondurulmus kare alinir. Kara kutu ve hangar canli (?hiz=8) bot turu + 'HANGAR' dugmesiyle alinir.
Gerekli kancalar: ?t=, ?bot=, ?seed=, __oyun.tur, __oyun.olaylar, __oyun.durum().asama ('KARA_KUTU'),
sayfada gorunur metinli 'HANGAR' dugmesi. Bir an bulunamazsa gri yer tutucu konur (betik cokmez).
"""
import argparse, re
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
import ortak as o

OLAY_DESEN = {
    "sekme": r"sekme", "dalis": r"^dalis$|dalış", "ses": r"duvar|ses|mach|ses_duvari|kirilis",
}


def olay_bul(olaylar, desen, sira=0, M=None):
    bul = [e for e in olaylar if e and isinstance(e[0], (int, float)) and re.search(desen, str(e[1]), re.I)
           and (M is None or (M in [str(x) for x in e[2:]]))]
    return bul[sira][0] if len(bul) > sira else None


def kare(pg_ctx, taban, dosya, sorgu, ad, klasor, bekle=700, hatalar=None):
    pg = o.sayfa_ac(pg_ctx, o.sayfa_url(taban, dosya, sorgu), hatalar)
    pg.wait_for_timeout(bekle)
    yol = klasor / f"{ad}.png"
    pg.screenshot(path=str(yol))
    pg.close()
    return yol


def tikla_gorunur(pg, desen):
    """Metni desene uyan ilk GORUNUR ogeye tiklar (gizli menu kopyalarini atlar)."""
    for el in pg.get_by_text(re.compile(desen, re.I)).all():
        if el.is_visible():
            el.click(timeout=3000)
            return
    raise RuntimeError("gorunur oge yok: " + desen)


def calis(taban, dosya, seed, bot, klasor):
    hatalar, kareler, notlar = [], [], []
    with sync_playwright() as p:
        br = o.tarayici_baslat(p)
        ctx = o.baglam_ac(br, fps=False)
        pg = o.sayfa_ac(ctx, o.sayfa_url(taban, dosya, f"kayit=0&seed={seed}&bot={bot}"), hatalar)
        o.kanca_sart(pg, ["tur", "olaylar"])
        sonuc = pg.evaluate(f"window.__oyun.tur({seed}, {{}}, '{bot}', 1)")
        olay = pg.evaluate("window.__oyun.olaylar || []")
        pg.close()
        off = (sonuc.get("sure_tur") or 0) - (sonuc.get("sure_ucus") or 0)   # rampa suresi
        notlar.append(f"rampa={off:.2f}s ucus={sonuc.get('sure_ucus')} olay_sayisi={len(olay)}")
        # ses duvari: olay adi varsa o; yoksa max_v >= 115 ise ilk 115 asimi bilinmez -> yaklasik ucus ortasi
        t_s = olay_bul(olay, OLAY_DESEN["ses"])
        an = [
            ("1_rampa", 0.5, None),
            ("2_kalkis", off + 0.3, None),
            ("3_ilk_sekme", (olay_bul(olay, OLAY_DESEN["sekme"], 0) or None), None),
            ("4_zincir", (olay_bul(olay, OLAY_DESEN["sekme"], 3) or olay_bul(olay, OLAY_DESEN["sekme"], 1) or None), None),
            ("5_dalis", olay_bul(olay, OLAY_DESEN["dalis"], 0), None),
            ("6_ses_duvari", t_s, None),
        ]
        for ad, ts, _ in an:
            if ts is None:
                kareler.append((ad, None, "olay yok"))
                continue
            try:
                S = ts + (0 if ad in ("1_rampa", "2_kalkis") else off) + (0.08 if ad[0] in "3456" else 0)
                yol = kare(ctx, taban, dosya, f"kayit=0&seed={seed}&bot={bot}&t={S:.3f}", ad, klasor)
                kareler.append((ad, yol, f"t={S:.2f}s"))
            except SystemExit as e:
                kareler.append((ad, None, "kanca/sayfa hatasi"))
        # canli: kara kutu + hangar
        try:
            pg = o.sayfa_ac(ctx, o.sayfa_url(taban, dosya, f"kayit=0&seed={seed}&bot={bot}&hiz=8"), hatalar)
            pg.wait_for_function("window.__oyun.durum().asama === 'KARA_KUTU'", timeout=120000)
            pg.wait_for_timeout(1800)   # animasyon sonuna yakin
            y = klasor / "7_kara_kutu.png"; pg.screenshot(path=str(y)); kareler.append(("7_kara_kutu", y, "canli"))
            try:
                tikla_gorunur(pg, r"^\s*HANGAR\s*$")
                pg.wait_for_timeout(800)
                y = klasor / "8_hangar.png"; pg.screenshot(path=str(y)); kareler.append(("8_hangar", y, "canli"))
            except Exception:
                kareler.append(("8_hangar", None, "HANGAR dugmesi bulunamadi"))
            pg.close()
        except Exception as e:
            kareler.append(("7_kara_kutu", None, "KARA_KUTU asamasina varilmadi"))
            kareler.append(("8_hangar", None, "-"))
        br.close()
    return kareler, notlar, hatalar


def sayfa_yap(kareler, cikis, sutun=4, w=240):
    h = int(w * 832 / 384)
    try:
        f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except Exception:
        f = ImageFont.load_default()
    sat = (len(kareler) + sutun - 1) // sutun
    S = Image.new("RGB", (sutun * (w + 8) + 8, sat * (h + 34) + 8), (30, 30, 30))
    d = ImageDraw.Draw(S)
    for i, (ad, yol, aciklama) in enumerate(kareler):
        x, y = 8 + (i % sutun) * (w + 8), 8 + (i // sutun) * (h + 34)
        if yol:
            im = Image.open(yol).convert("RGB").resize((w, h))
            S.paste(im, (x, y + 26))
        else:
            d.rectangle([x, y + 26, x + w, y + 26 + h], fill=(70, 40, 40))
            d.text((x + 10, y + 26 + h // 2), "YOK: " + aciklama, fill=(255, 200, 200), font=f)
        d.text((x, y + 4), f"{ad}  {aciklama if yol else ''}", fill=(255, 255, 255), font=f)
    S.save(cikis)


def main():
    ap = o.ortak_arg(argparse.ArgumentParser())
    ap.add_argument("--seed", type=int, default=3)
    ap.add_argument("--bot", default="iyi")
    a = ap.parse_args()
    dosya = o.sayfa_dosyasi(a.sayfa)
    klasor = o.CIKTI / "kontak"
    klasor.mkdir(parents=True, exist_ok=True)
    with o.sunucu(port=a.port) as taban:
        kareler, notlar, hatalar = calis(taban, dosya, a.seed, a.bot, klasor)
    cikis = o.CIKTI / "kontak.png"
    sayfa_yap(kareler, cikis)
    print("\n".join(notlar))
    for ad, yol, ac in kareler:
        print(f"  {ad:14s} {'OK ' if yol else 'YOK'} {ac}")
    if hatalar:
        print("konsol hatalari:", hatalar[:5])
    print("kontak sayfasi:", cikis)


if __name__ == "__main__":
    main()
