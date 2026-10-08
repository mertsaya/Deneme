# Son Durak: Plüton · önizleme sayfaları (Pillow + numpy). Kullanım: python sayfa.py [stil|kahraman|eski_yeni|sahne|hepsi]
import os, sys, json, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kontur as K

KOK = K.KOK; HAM = K.HAM; SPR = K.CIK; ONI = os.path.join(KOK, "onizleme"); os.makedirs(ONI, exist_ok=True)
OYUN = os.path.dirname(KOK)

def font(b, kalin=True):
    for f in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if kalin else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",):
        if os.path.exists(f): return ImageFont.truetype(f, b)
    return ImageFont.load_default()

def gok(w, h, ust=(58, 140, 240), alt=(172, 222, 255)):
    y = np.linspace(0, 1, h)[:, None, None]
    a = np.array(ust)[None, None] * (1 - y) + np.array(alt)[None, None] * y
    return Image.fromarray(np.repeat(a, w, 1).astype(np.uint8), "RGB").convert("RGBA")

def sigdir(im, w, h):
    s = min(w / im.width, h / im.height); return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)

def yapistir(zemin, im, x, y):
    zemin.alpha_composite(im, (int(x), int(y)))

def yazi(d, xy, t, b=18, renk=(255, 255, 255), golge=True, kalin=True):
    f = font(b, kalin)
    if golge: d.text((xy[0] + 2, xy[1] + 2), t, font=f, fill=(20, 20, 60, 160))
    d.text(xy, t, font=f, fill=renk)

# ------------------------------------------------------------------ stil karşılaştırma
def stil():
    W, H = 1500, 1080
    z = gok(W, H); d = ImageDraw.Draw(z)
    bas = {"A": "A · standart üç nokta ışık", "B": "B · gök kubbesi + kenar ışığı ★", "C": "C · cel/toon BSDF + kenar"}
    for i, st in enumerate("ABC"):
        x0 = 20 + i * 495
        yazi(d, (x0, 14), bas[st], 19)
        y = 60
        for ad, hh in (("roket", 230), ("zeplin", 270), ("pilot", 380)):
            im = K.isle(os.path.join(HAM, f"stil_{st}_{ad}.png"))
            im = sigdir(im, 470, hh); yapistir(z, im, x0 + (470 - im.width) / 2, y); y += hh + 12
        # telefon ölçeği: 77 px roket, konturu o boyda
        ph = K.kucult_konturla(os.path.join(HAM, f"stil_{st}_roket.png"), 77 * 1, 1.6)
        yapistir(z, ph, x0 + 10, H - 60); yazi(d, (x0 + 100, H - 52), "telefon 1x (77 px)", 15)
        ph3 = K.kucult_konturla(os.path.join(HAM, f"stil_{st}_roket.png"), 77 * 2, 2.4)
        yapistir(z, ph3, x0 + 270, H - 80)
    z.convert("RGB").save(os.path.join(ONI, "karsilastirma_stil.png"))
    print("onizleme/karsilastirma_stil.png")

# ------------------------------------------------------------------ yardımcılar
def spr(ad):
    """Konturlu 1x sprite (sprite/ad.png); yoksa hamdan üret."""
    y = os.path.join(SPR, ad + ".png")
    if os.path.exists(y): return Image.open(y).convert("RGBA")
    return K.isle(os.path.join(HAM, ad + ".png"), sabit_px=K.sabit(ad))

def akis(z, d, y, baslik, ogeler, hh, W, x0=30, ara=18, etiket=True):
    """ogeler: [(ad, im)] tek satır akışı, gerekirse alt satıra geçer. Döner: yeni y."""
    yazi(d, (x0, y), baslik, 24); y += 40; x = x0; satir_h = 0
    for ad, im in ogeler:
        im = sigdir(im, hh * 2.2, hh)
        if x + im.width > W - 20: x = x0; y += satir_h + 34; satir_h = 0
        yapistir(z, im, x, y + (hh - im.height) / 2)
        if etiket: yazi(d, (x, y + hh + 4), ad, 13, kalin=False)
        x += im.width + ara; satir_h = max(satir_h, hh)
    return y + satir_h + 44

def dose(im, n=2):
    out = Image.new("RGBA", (im.width * n, im.height), (0, 0, 0, 0))
    for i in range(n): out.alpha_composite(im, (i * im.width, 0))
    return out

def arka(ad):
    """Arka plan katmanı: 3x döşeyip konturla, ortadakini kes (dikişte kontur kopmasın)."""
    im = Image.open(os.path.join(HAM, ad + ".png")).convert("RGBA")
    renk = K.hex2("#5b64b8") if ad == "arka_uzak" else K.hex2("#2d6b45")
    t = K.kontur(dose(im, 3), 2.2, renk); p = (t.width - 3 * im.width) // 2
    return t.crop((p + im.width, p, p + 2 * im.width, p + im.height))

# ------------------------------------------------------------------ kahraman sayfa
def kahraman():
    W = 1800; z = gok(W, 4200); d = ImageDraw.Draw(z)
    yazi(d, (30, 20), "Son Durak: Plüton · B1 3B kahraman kareler (Blender Cycles, stil B)", 30)
    y = 80
    y = akis(z, d, y, "Roket (kopabilen kademeler ayrı)", [(n, spr(n)) for n in ("roket", "roket_kademe_1", "roket_kademe_2")], 190, W)
    y = akis(z, d, y, "Roket burun açısı: -30° … +45° (8 kare, ışık sabit)", [(f"roket_aci_{i}", spr(f"roket_aci_{i}")) for i in range(8)], 150, W, ara=6)
    y = akis(z, d, y, "Motor alevi (4 kare)", [(f"alev_{i}", spr(f"alev_{i}")) for i in range(4)], 110, W)
    y = akis(z, d, y, "Maskot pilot: nötr · heyecan · şaşkın · korku · zafer (şekil anahtarı)", [(f"pilot_{n}", spr(f"pilot_{n}")) for n in ("notr", "heyecan", "saskin", "korku", "zafer")], 300, W)
    y = akis(z, d, y, "Zeplin: normal · ezik · şaşkın  |  ezilme 0-3 (çarpma → sıçrama → toparlanma)",
             [(f"zeplin_{n}", spr(f"zeplin_{n}")) for n in ("normal", "ezik", "saskin")] + [(f"zeplin_ezilme_{i}", spr(f"zeplin_ezilme_{i}")) for i in range(4)], 170, W, ara=10)
    y = akis(z, d, y, "Reklam balonu: normal · ezik · şaşkın  |  ezilme 0-3",
             [(f"balon_{n}", spr(f"balon_{n}")) for n in ("normal", "ezik", "saskin")] + [(f"balon_ezilme_{i}", spr(f"balon_ezilme_{i}")) for i in range(4)], 230, W, ara=14)
    y = akis(z, d, y, "Bulutlar (3B metaball, 3 çeşit)", [(f"bulut_{i}", spr(f"bulut_{i}")) for i in range(3)], 170, W)
    y = akis(z, d, y, "Efektler: yıldız patlaması (3) · toz (3) · ses duvarı halkası (2)",
             [(f"efekt_yildiz_{i}", spr(f"efekt_yildiz_{i}")) for i in range(3)] + [(f"efekt_toz_{i}", spr(f"efekt_toz_{i}")) for i in range(3)] + [(f"efekt_ses_{i}", spr(f"efekt_ses_{i}")) for i in range(2)], 150, W, ara=10)
    yazi(d, (30, y), "Arka plan katmanları (yatay döşenir; 2 kopya yan yana = dikiş testi)", 24); y += 40
    for ad in ("arka_uzak", "arka_yakin"):
        if not os.path.exists(os.path.join(HAM, ad + ".png")): continue
        im = dose(arka(ad), 2); im = sigdir(im, W - 60, 400); yapistir(z, im, 30, y); yazi(d, (30, y + im.height + 4), ad, 13, kalin=False); y += im.height + 34
    y += 10
    # telefon ölçeği: 77 px roket; diğerleri eski atlas dünya birimi oranıyla (zeplin 49, balon 38.5, roket 38 birim)
    yazi(d, (30, y), "Telefon ölçeği 1x (roket 77 px; kontur bu boyda eklendi) ve 2x (retina)", 24); y += 44
    x = 30
    for kat in (1, 2):
        for ad, uz, rp in (("roket_aci_3", 77, 1.6), ("alev_0", 30, 1.2), ("pilot_heyecan", 40, 1.4), ("zeplin_normal", 100, 1.6), ("balon_normal", 78, 1.6),
                           ("bulut_1", 90, 1.2), ("efekt_yildiz_1", 50, 1.4)):
            im = K.kucult_konturla(os.path.join(HAM, ad + ".png"), uz * kat, rp * kat)
            yapistir(z, im, x, y); x += im.width + 14
        x += 30
    y += 200
    z = z.crop((0, 0, W, y))
    z.convert("RGB").save(os.path.join(ONI, "kahraman_sayfa.png"))
    k = sigdir(z, 900, 99999); k.convert("RGB").save(os.path.join(ONI, "kahraman_sayfa_kucuk.png"))
    print("onizleme/kahraman_sayfa.png", z.size)

# ------------------------------------------------------------------ sahne önizleme 384x832
def sahne(dosya="sahne_onizleme.png", olc=1.0):
    W, H = 384, 832
    z = gok(W, H, (40, 118, 232), (168, 220, 255))
    # uzak katman ufukta, yakın katman altta (yarım hızda kayıyormuş gibi kaydırılmış)
    uz = arka("arka_uzak"); uz = uz.resize((int(uz.width * 0.75), int(uz.height * 0.75)), Image.LANCZOS)
    yk = arka("arka_yakin"); yk = yk.resize((int(yk.width * 0.62), int(yk.height * 0.62)), Image.LANCZOS)
    for i in range(-1, 2): z.alpha_composite(uz, (i * uz.width - 120, H - uz.height - 70))
    for i in range(-1, 2): z.alpha_composite(yk, (i * yk.width - 60, H - yk.height + 6))
    def koy(ad, uzun, x, y, r=1.6, aci=0):
        im = K.kucult_konturla(os.path.join(HAM, ad + ".png"), int(uzun * olc), r * olc)
        if aci: im = im.rotate(aci, Image.BICUBIC, expand=True)
        z.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))
    koy("bulut_2", 230, 300, 250, 1.4); koy("bulut_0", 110, 60, 120, 1.2); koy("bulut_1", 150, 70, 560, 1.3)
    koy("balon_normal", 100, 300, 430)
    koy("zeplin_ezilme_1", 128, 150, 650)
    # roket: 3. açı karesi (~+2°) yerine dalış sonrası yükseliş karesi; alev roketin arkasına
    koy("efekt_ses_1", 120, 238, 520, 0)
    ra = 6  # +34° kare
    im = K.kucult_konturla(os.path.join(HAM, f"roket_aci_{ra}.png"), int(118 * olc), 1.7 * olc)
    al = K.kucult_konturla(os.path.join(HAM, "alev_1.png"), int(44 * olc), 1.2 * olc).rotate(34, Image.BICUBIC, expand=True)
    rx, ry = 190, 540
    z.alpha_composite(al, (int(rx - 54 * olc - al.width / 2), int(ry + 36 * olc - al.height / 2)))
    z.alpha_composite(im, (int(rx - im.width / 2), int(ry - im.height / 2)))
    koy("efekt_yildiz_0", 70, 168, 606, 1.4)
    koy("efekt_toz_1", 60, 120, 640, 1.0)
    # pilot rozeti (arayüz yeri)
    koy("pilot_heyecan", 62, 44, 50, 1.4)
    z.convert("RGB").save(os.path.join(ONI, dosya)); print("onizleme/" + dosya)
    return z

# ------------------------------------------------------------------ eski / yeni / konsept
def eski_yeni():
    W, H = 1500, 1000
    z = gok(W, H, (30, 40, 80), (60, 70, 120)); d = ImageDraw.Draw(z)
    kon = Image.open(os.path.join(OYUN, "konsept", "oyun_ici_1.jpg")).convert("RGBA").resize((336, 597), Image.LANCZOS)
    eski = Image.open(os.path.join(OYUN, "b1_gorsel", "onizleme", "sahne_04_zeplin.png")).convert("RGBA").resize((384, 832), Image.LANCZOS)
    yeni = sahne("sahne_onizleme.png")
    yazi(d, (30, 18), "Konsept (onaylı, 112 px küçük görsel ×3)", 18); z.alpha_composite(kon, (30, 60))
    yazi(d, (400, 18), "Eski: Canvas2D vektör (b1_gorsel)", 18); z.alpha_composite(eski, (400, 60))
    yazi(d, (810, 18), "Yeni: Blender 3B → sprite (b1_gorsel3d)", 18); z.alpha_composite(yeni.convert("RGBA"), (810, 60))
    # yakın plan sprite çiftleri
    at = Image.open(os.path.join(OYUN, "b1_gorsel", "sprite", "atlas_0.png")).convert("RGBA")
    js = json.load(open(os.path.join(OYUN, "b1_gorsel", "sprite", "atlas.json")))["sprite"]
    def eski_s(ad):
        p, x, y, w, h = js[ad][:5]; return at.crop((x, y, x + w, y + h))
    x = 1215; y = 60
    yazi(d, (x, y - 42), "eski | yeni", 18)
    for e, n in (("zeplin_normal", "zeplin_normal"), ("balon", "balon_normal"), ("portre_heyecan", "pilot_heyecan"), ("roket_ust", "roket_kademe_2")):
        a = sigdir(eski_s(e), 130, 130); b = sigdir(spr(n), 130, 130)
        z.alpha_composite(a, (x, y + (130 - a.height) // 2)); z.alpha_composite(b, (x + 140, y + (130 - b.height) // 2)); y += 150
    yazi(d, (30, 680), "Not: konsept görseli yalnız 112×199 px mevcut; büyütme bulanık.", 15, kalin=False)
    z.convert("RGB").save(os.path.join(ONI, "karsilastirma_eski_yeni.png")); print("onizleme/karsilastirma_eski_yeni.png")

if __name__ == "__main__":
    ne = sys.argv[1] if len(sys.argv) > 1 else "hepsi"
    for k, f in (("stil", stil), ("kahraman", kahraman), ("eski_yeni", eski_yeni), ("sahne", sahne)):
        if ne in (k, "hepsi") and not (ne == "hepsi" and k == "sahne"): f()
