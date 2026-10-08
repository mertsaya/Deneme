"""Teknik yol karşılaştırması: Canvas2D sprite roketi ile Blender toon roketi, yakın (3×) ve telefon (1×) boyutunda, gök zemininde.
Çalıştır (uret.py ve blender_roket_toon.py'den sonra): python3 oyun/b1_gorsel/uretim/yol_karsilastir.py"""
import json, pathlib
from PIL import Image, ImageDraw, ImageFont
F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
K = pathlib.Path(__file__).resolve().parent.parent
j = json.loads((K / "sprite/atlas.json").read_text()); A = Image.open(K / "sprite/atlas_0.png")
def sp(ad):
    p, x, y, w, h, ax, ay, d = j["sprite"][ad]; return A.crop((x, y, x + w, y + h)), ax, ay
alt, ax1, ay1 = sp("roket_alt"); ust, ax2, ay2 = sp("roket_ust"); pil, ax3, ay3 = sp("pilot_heyecan"); cam, ax4, ay4 = sp("cam")
roket = Image.new("RGBA", (260, 160), (0, 0, 0, 0)); o = (150, 80)
for im, ax, ay, dx, dy in ((alt, ax1, ay1, 0, 0), (ust, ax2, ay2, 0, 0), (pil, ax3, ay3, 2.1, -0.7), (cam, ax4, ay4, 0, 0)):
    roket.alpha_composite(im, (int(o[0] - ax + dx), int(o[1] - ay + dy)))
bl = Image.open(K / "onizleme/blender_roket_toon.png").convert("RGBA"); bl = bl.crop(bl.getbbox())
bl = bl.resize((int(bl.width * roket.getbbox()[2] / bl.width * 0.0 + 230), int(bl.height * 230 / bl.width)))
W, H = 1000, 460
C = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(C)
for y in range(H): d.line([(0, y), (W, y)], fill=(47 + y // 6, 140 + y // 8, 240, 255))
rk = roket.crop(roket.getbbox())
for i, (im, ad) in enumerate(((rk, "A · Canvas2D kod çizimi (seçilen)"), (bl, "B · Blender toon render (Cycles + Freestyle)"))):
    X = 40 + i * 480
    big = im.resize((im.width * 3 // 2, im.height * 3 // 2)); C.alpha_composite(big, (X, 60))
    small = im.resize((max(1, im.width * 19 // 70), max(1, im.height * 19 // 70)), Image.LANCZOS); C.alpha_composite(small, (X + 30, 330))
    d.text((X, 20), ad, fill="white", font=F); d.text((X, 400), "telefon ölçeği 1× (1,9 px/birim)", fill="white", font=F)
C.convert("RGB").save(K / "onizleme/karsilastirma_teknik_yol.png"); print("tamam")
