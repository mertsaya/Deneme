"""B1 sahnesini Playwright ile açar: konsol hatası, açılış süresi, fps ölçer; olay anlarının ekran görüntülerini alır.
Çalıştır: python3 oyun/b1_gorsel/uretim/onizle.py   → oyun/b1_gorsel/onizleme/sahne_*.png + kontak_sahne.png
"""
import functools, http.server, json, pathlib, threading, time
from playwright.sync_api import sync_playwright
from PIL import Image

KOK = pathlib.Path(__file__).resolve().parent.parent
ONIZ = KOK / "onizleme"


def sunucu():
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(KOK))
    h.log_message = lambda *a: None
    s = http.server.ThreadingHTTPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s


def main():
    s = sunucu(); url = f"http://127.0.0.1:{s.server_port}/index.html"
    exe = next((str(p) for p in pathlib.Path("/opt/pw-browsers").glob("chromium-*/chrome-linux*/chrome")), None)
    hatalar = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=exe) if exe else pw.chromium.launch()
        sayfa = b.new_page(viewport={"width": 384, "height": 832}, device_scale_factor=2)
        sayfa.on("console", lambda m: hatalar.append(m.text) if m.type in ("error", "warning") else None)
        sayfa.on("pageerror", lambda e: hatalar.append(str(e)))
        sayfa.on("requestfailed", lambda r: hatalar.append("istek: " + r.url))
        t0 = time.time(); sayfa.goto(url); sayfa.wait_for_function("window.__sahne && window.__sahne.hazir", timeout=10000)
        acilis = time.time() - t0
        sayfa.wait_for_timeout(3000); fps = sayfa.evaluate("window.__sahne.fps()")
        sayfa.screenshot(path=str(ONIZ / "sahne_canli.png"))
        olaylar = sayfa.evaluate("window.__sahne.tumu()")
        anlar = [("rampa", 0.6), ("kalkis", None)]
        sec = {}
        for o in olaylar:
            sec.setdefault(o["ad"], o["t"])
        cekim = [("01_rampa", 0.7)]
        for ad, ek, dosya in [("kalkis", 0.35, "02_kalkis"), ("ucurtma_ip", 0.12, "03_ucurtma"), ("sekme_zeplin", 0.06, "04_zeplin"),
                              ("sekme_balon", 0.06, "05_balon"), ("marti", 0.15, "06_marti"), ("dalis_oto", 0.25, "07_dalis"),
                              ("ses_duvari", 0.05, "08_ses_duvari"), ("dron", 0.3, "09_dron"), ("kademe_ayrilma", 0.7, "10_kademe"), ("kademe_ayrilma", 4.8, "11_gece")]:
            if ad in sec: cekim.append((dosya, sec[ad] + ek))
        for o in olaylar:
            if o["ad"].startswith("sekme_balon_mukemmel"): cekim.append(("07b_dalis_sekme", o["t"] + 0.06))
        dosyalar = []
        for dosya, t in sorted(cekim, key=lambda x: x[0]):
            sayfa.evaluate(f"window.__sahne.git({t})")
            yol = ONIZ / f"sahne_{dosya}.png"; sayfa.screenshot(path=str(yol)); dosyalar.append(yol)
        # dokunuş denemesi: canlı oynatmada 3 dokunuş, hata olmamalı
        sayfa.goto(url); sayfa.wait_for_function("window.__sahne.hazir"); sayfa.wait_for_timeout(2500)
        for i in range(3):
            sayfa.mouse.click(200, 400); sayfa.wait_for_timeout(700)
        sayfa.screenshot(path=str(ONIZ / "sahne_dokunus.png"))
        dokunus = [o["ad"] for o in sayfa.evaluate("window.__sahne.olaylar()")]
        b.close()
    s.shutdown()
    # kontak sayfası (yarım boyut)
    ims = [Image.open(p).resize((384, 832)) for p in dosyalar]
    n = len(ims); sut = 6; sat = (n + sut - 1) // sut
    K = Image.new("RGB", (sut * 390, sat * 838), (20, 20, 40))
    for i, im in enumerate(ims): K.paste(im, ((i % sut) * 390, (i // sut) * 838))
    K.save(ONIZ / "kontak_sahne.png")
    print(json.dumps({"acilis_s": round(acilis, 2), "fps_headless": round(fps, 1), "hatalar": hatalar, "olaylar": olaylar, "dokunus_olaylari": dokunus}, ensure_ascii=False))


if __name__ == "__main__":
    main()
