# Son Durak: Plüton · dış kalın kontur (kompozit, alfa genişletme). Python 3.11+, Pillow, numpy.
# Kullanım: python kontur.py        -> sprite/ham/*.png  ->  sprite/*.png (konturlu, 1x hedef boy)
# Kontur render'dan SONRA ve HEDEF çözünürlükte eklenir: küçültülmüş sprite'ta da kalınlık piksel olarak korunur
# (kucult_konturla). Böylece telefon boyunda (77 px roket) çizgi kaybolmaz.
import os, sys, glob
import numpy as np
from PIL import Image, ImageFilter

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HAM = os.path.join(KOK, "sprite", "ham"); CIK = os.path.join(KOK, "sprite")
CIVIT = (42, 29, 79)

def hex2(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def kontur(im, r, renk=CIVIT, golge=None):
    """im: RGBA. r: piksel kalınlık (kesirli olabilir). Kenar yumuşatmalı disk genişletme."""
    im = im.convert("RGBA"); p = int(np.ceil(r)) + 2
    a = np.asarray(im).astype(np.float32) / 255.0
    H, W = a.shape[:2]
    big = np.zeros((H + 2 * p, W + 2 * p, 4), np.float32); big[p:p + H, p:p + W] = a
    al = big[..., 3]
    out = np.zeros_like(al)
    R = int(np.ceil(r)) + 1
    for dy in range(-R, R + 1):
        for dx in range(-R, R + 1):
            d = (dx * dx + dy * dy) ** 0.5
            w = min(1.0, max(0.0, r + 0.5 - d))
            if w <= 0: continue
            sh = np.roll(np.roll(al, dy, 0), dx, 1)
            np.maximum(out, sh * w, out=out)
    rgb = big[..., :3]; sa = al[..., None]
    c = np.array(renk, np.float32)[None, None, :] / 255.0
    # önce kontur, üstüne sprite (premultiplied 'over')
    oa = out[..., None]
    res_a = sa + oa * (1 - sa)
    res_rgb = (rgb * sa + c * oa * (1 - sa)) / np.maximum(res_a, 1e-6)
    res = np.concatenate([res_rgb, res_a], -1)
    return Image.fromarray((np.clip(res, 0, 1) * 255 + 0.5).astype(np.uint8), "RGBA")

def parilti(im, r, guc=1.0, renk=(200, 245, 255)):
    """Işıklı efektler için yumuşak hale (bloom)."""
    im = im.convert("RGBA"); p = int(r * 2.5)
    big = Image.new("RGBA", (im.width + 2 * p, im.height + 2 * p), (0, 0, 0, 0)); big.paste(im, (p, p))
    a = np.asarray(big).astype(np.float32) / 255.0
    bl = np.asarray(big.filter(ImageFilter.GaussianBlur(r))).astype(np.float32) / 255.0
    ga = np.clip(bl[..., 3] * guc, 0, 1)[..., None]
    c = np.array(renk, np.float32)[None, None, :] / 255.0
    sa = a[..., 3:4]
    res_a = sa + ga * (1 - sa); res_rgb = (a[..., :3] * sa + c * ga * (1 - sa)) / np.maximum(res_a, 1e-6)
    return Image.fromarray((np.clip(np.concatenate([res_rgb, res_a], -1), 0, 1) * 255 + 0.5).astype(np.uint8), "RGBA")

# ad önekine göre kontur kuralı: (kalınlık oranı (en uzun kenara göre), renk, hale)
KURAL = [
    ("bulut", 0.010, hex2("#8fa6e6"), None),
    ("alev", 0.016, hex2("#9a1f0c"), None),
    ("efekt_ses", 0.0, None, (10, 0.9)),
    ("efekt_toz", 0.012, hex2("#7b6a8f"), None),
    ("", 0.0135, CIVIT, None),
]

def kural(ad):
    for on, oran, renk, hale in KURAL:
        if ad.startswith(on): return oran, renk, hale

def isle(yol, hedef_gen=None, oran_carp=1.0, sabit_px=None):
    ad = os.path.basename(yol)[:-4]; im = Image.open(yol).convert("RGBA")
    if hedef_gen and hedef_gen != im.width:
        im = im.resize((hedef_gen, max(1, round(im.height * hedef_gen / im.width))), Image.LANCZOS)
    oran, renk, hale = kural(ad)
    if hale: return parilti(im, hale[0] * im.width / 448, hale[1])
    if oran <= 0: return im
    # dizideki tüm kareler aynı kalınlıkta olsun: oran, dizinin ortak tuval boyuna göre
    r = sabit_px if sabit_px else max(1.6, oran * oran_carp * max(im.size))
    return kontur(im, r, renk)

# dizi başına sabit kalınlık (px, 1x sprite boyunda)
SABIT = {"roket_aci": 9.0, "pilot_": 7.0, "zeplin_": 8.5, "balon_": 7.5, "efekt_yildiz": 6.5, "efekt_toz": 4.5, "alev_": 4.0}

def sabit(ad):
    for k, v in SABIT.items():
        if ad.startswith(k): return v
    return None

def kucult_konturla(yol, hedef_uzun, r_px=2.0):
    """Ham render'ı hedef boya küçültüp konturu o boyda ekler (telefon ölçeği önizleme)."""
    ad = os.path.basename(yol)[:-4]; im = Image.open(yol).convert("RGBA")
    s = hedef_uzun / max(im.size)
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    oran, renk, hale = kural(ad)
    if hale: return parilti(im, max(2, hale[0] * s * 1.2), hale[1])
    if oran <= 0: return im
    return kontur(im, r_px, renk)

if __name__ == "__main__":
    filt = sys.argv[1] if len(sys.argv) > 1 else ""
    for y in sorted(glob.glob(os.path.join(HAM, "*.png"))):
        ad = os.path.basename(y)[:-4]
        if not ad.startswith(filt) or ad.startswith("stil_"): continue
        out = isle(y, sabit_px=sabit(ad)); out.save(os.path.join(CIK, ad + ".png"), optimize=True)
        print("kontur", ad, out.size)
