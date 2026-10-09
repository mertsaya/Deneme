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

# stilize palet: canlı ve temiz (index.html'deki PALET ile aynı)
PALET = {
    "derin": (0x1D, 0x5F, 0x8C),
    "sig":   (0x2F, 0xA8, 0xB5),
    "col":   (0xF0, 0xC6, 0x7C),
    "bozkir": (0xD9, 0x97, 0x55),
    "bitki": (0x5A, 0x9A, 0x3A),
    "kar":   (0xFB, 0xF8, 0xF1),
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


def bulut(hedef="bulut.png", W=2048, H=1024, tohum=7):
    """Küresel bulut örtüsü (gri tonlu, beyaz = bulut). Çok ölçekli gürültü; enleme göre gerçekçi dağılım:
    ekvatorda ve orta enlemlerde çok, ~25° çöl kuşağında az."""
    rng = np.random.default_rng(tohum)
    n = np.zeros((H, W), np.float32)
    for o in range(7):
        gh, gw = 6 * 2 ** o, 18 * 2 ** o   # doğu-batı yönünde uzun (rüzgâr kuşakları)
        g = rng.random((gh + 3, gw + 3)).astype(np.float32)
        z = ndimage.zoom(g, (H / gh, W / gw), order=3)[:H, :W]
        n += z * 0.62 ** o
    n = (n - n.min()) / (n.max() - n.min())
    enlem = np.abs(np.linspace(90, -90, H))[:, None]
    agirlik = 1 - 0.28 * np.exp(-((enlem - 25) / 9) ** 2) + 0.1 * np.exp(-(enlem / 8) ** 2)
    c = np.clip((n * agirlik - 0.44) / 0.2, 0, 1)
    c = c * c * (3 - 2 * c)
    Image.fromarray((c * 255).astype(np.uint8), "L").save(KOK / hedef, optimize=True)
    print(hedef, W, "x", H)


if __name__ == "__main__":
    bulut()
    uret("dunya.jpg", "harita.png", sigma=1.6, sig_px=6, cizgi_px=1)
    # yakın plan 100 km'den bakılıyor: büyütüp sınıflandır ki kıyılar basamaklı değil yumuşak olsun (4096, telefonda güvenli doku sınırı)
    uret("bolge.jpg", "bolge_harita.png", sigma=5.5, sig_px=25, cizgi_px=3, boyut=(4096, 2979))
