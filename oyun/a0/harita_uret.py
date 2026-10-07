"""Stilize mod için düz renkli Dünya haritası üretir.

NASA Blue Marble dokularını (dunya.jpg, bolge.jpg) piksel rengine göre sınıflara ayırır
(derin deniz, sığ deniz, çöl, bozkır, bitki örtüsü, kar/buz), sınıfları yumuşatıp
retro afiş paletiyle düz renge boyar ve kıyılara mürekkep çizgisi çeker.
Kıyı şekilleri birebir NASA görüntüsünden gelir; yalnızca boyama stilize edilir.

Çalıştır: python harita_uret.py   ->  harita.png, bolge_harita.png
"""
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

KOK = Path(__file__).parent

# retro ajans afişi paleti (index.html'deki PALET ile aynı)
PALET = {
    "derin": (0x2E, 0x5E, 0x6E),
    "sig":   (0x4E, 0x8C, 0x8F),
    "col":   (0xE9, 0xC2, 0x7E),
    "bozkir": (0xC8, 0x8A, 0x4E),
    "bitki": (0x6F, 0x7D, 0x47),
    "kar":   (0xF4, 0xEB, 0xD8),
    "murekkep": (0x1F, 0x2A, 0x3A),
}
SINIF = ["derin", "sig", "col", "bozkir", "bitki", "kar"]


def siniflar(rgb):
    f = rgb.astype(np.float32) / 255
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    mx, mn = f.max(-1), f.min(-1)
    sat = (mx - mn) / np.maximum(mx, 1e-4)
    su = ((b > r + 0.06) & (b >= g - 0.02)) | (mx < 0.10) | ((g > r + 0.05) & (b > r + 0.05) & (mx < 0.45))
    kar = (~su) & (mx > 0.70) & (sat < 0.20)
    kara = ~(su | kar)
    yesil = kara & ((g >= r - 0.015) | (mx < 0.27))
    col = kara & ~yesil & (mx > 0.62)
    bozkir = kara & ~yesil & ~col
    s = np.zeros(r.shape, np.uint8)
    s[su] = 0; s[col] = 2; s[bozkir] = 3; s[yesil] = 4; s[kar] = 5
    return s, su


def yumusat(s, sigma, n=len(SINIF)):
    # sınıfları ayrı ayrı bulanıklaştırıp en güçlüsünü seç: küçük lekeler kaybolur, düz alanlar kalır
    w = np.stack([ndimage.gaussian_filter((s == i).astype(np.float32), sigma) for i in range(n)])
    return w.argmax(0).astype(np.uint8)


def uret(kaynak, hedef, sigma, sig_px, cizgi_px, boyut=None):
    im = Image.open(KOK / kaynak).convert("RGB")
    if boyut:
        im = im.resize(boyut, Image.LANCZOS)
    s, _ = siniflar(np.asarray(im))
    s = yumusat(s, sigma)
    su = s == 0
    # sığ deniz: kıyıya sig_px pikselden yakın su
    uzak = ndimage.distance_transform_edt(su)
    s[su & (uzak <= sig_px)] = 1
    out = np.zeros(s.shape + (3,), np.uint8)
    for i, ad in enumerate(SINIF):
        out[s == i] = PALET[ad]
    # kıyı çizgisi: suyun karayla komşu olduğu kenar
    kara = ~su
    kenar = kara & ndimage.binary_dilation(su, iterations=cizgi_px)
    out[kenar] = PALET["murekkep"]
    Image.fromarray(out).save(KOK / hedef, optimize=True)
    print(hedef, out.shape[1], "x", out.shape[0])


if __name__ == "__main__":
    uret("dunya.jpg", "harita.png", sigma=1.6, sig_px=6, cizgi_px=1)
    # yakın plan 100 km'den bakılıyor: büyütüp sınıflandır ki kıyılar basamaklı değil yumuşak olsun (4096, telefonda güvenli doku sınırı)
    uret("bolge.jpg", "bolge_harita.png", sigma=5.5, sig_px=25, cizgi_px=3, boyut=(4096, 2979))
