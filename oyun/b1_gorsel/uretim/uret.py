"""B1 görsel dilimi: sprite atlası üretici.
Çalıştır:  python3 oyun/b1_gorsel/uretim/uret.py
cizim.js'teki Canvas2D çizimlerini Chromium'da (Playwright) çizer; dış konturu ekler, atlasa dizer.
Çıktı: oyun/b1_gorsel/sprite/atlas_*.png + atlas.json, oyun/b1_gorsel/onizleme/{kontak,karsilastirma_tarz,karsilastirma_pilot}.png
"""
import base64, json, os, pathlib
from playwright.sync_api import sync_playwright

KOK = pathlib.Path(__file__).resolve().parent.parent
SPRITE = KOK / "sprite"; ONIZ = KOK / "onizleme"
SPRITE.mkdir(exist_ok=True); ONIZ.mkdir(exist_ok=True)


def yaz(yol, data_url):
    yol.write_bytes(base64.b64decode(data_url.split(",", 1)[1]))


def main():
    exe = None
    for p in pathlib.Path("/opt/pw-browsers").glob("chromium-*/chrome-linux*/chrome"):
        exe = str(p)
    with sync_playwright() as pw:
        tarayici = pw.chromium.launch(executable_path=exe) if exe else pw.chromium.launch()
        sayfa = tarayici.new_page()
        hatalar = []
        sayfa.on("console", lambda m: hatalar.append(m.text) if m.type == "error" else None)
        sayfa.on("pageerror", lambda e: hatalar.append(str(e)))
        sayfa.goto((KOK / "uretim" / "uretici.html").as_uri())
        sayfa.wait_for_function("window.hazir === true")
        r = sayfa.evaluate("window.uret()")
        tarayici.close()
    if hatalar:
        raise SystemExit("Konsol hatası: " + "; ".join(hatalar))
    for eski in SPRITE.glob("atlas_*.png"):
        eski.unlink()
    for i, d in enumerate(r["atlas"]["png"]):
        yaz(SPRITE / f"atlas_{i}.png", d)
    (SPRITE / "atlas.json").write_text(json.dumps(r["atlas"]["json"], ensure_ascii=False, separators=(",", ":")))
    yaz(ONIZ / "kontak.png", r["kontak"])
    yaz(ONIZ / "karsilastirma_tarz.png", r["karsilastir"])
    yaz(ONIZ / "karsilastirma_pilot.png", r["pilot"])
    toplam = sum(f.stat().st_size for f in SPRITE.iterdir())
    print(f"{len(r['atlas']['json']['sprite'])} sprite, {len(r['atlas']['png'])} atlas sayfası, sprite klasörü {toplam/1024:.0f} KB")


if __name__ == "__main__":
    main()
