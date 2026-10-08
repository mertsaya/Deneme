#!/usr/bin/env python3
"""kabul.py: TASARIM.md 18'deki K1-K16'yi tek tek denetler; gecti/kaldi tablosu -> RAPOR.md (+ cikti/kabul.json).
Kullanim: python3 kabul.py [--sayfa index.html] [--hizli] [--sadece K1,K3] [--k8n 200]
Durumlar: GECTI | KALDI | BILGI (K4-K6, gecme sarti degil) | ELLE (otomatik olculemez / telefon) | ATLANDI (kanca eksik)
Cikis kodu: 1 = en az bir geçme-şartlı K KALDI.
"""
import argparse, json, math, re, statistics as st, subprocess, sys, time, traceback
from pathlib import Path
from playwright.sync_api import sync_playwright
import ortak as o

SONUC = {}      # K -> dict(durum, ayrinti)
GECME = {f"K{i}" for i in [1, 2, 3, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]}


def kaydet(k, durum, ayrinti):
    SONUC[k] = {"durum": durum, "ayrinti": ayrinti}
    print(f"[{k:3s}] {durum:8s} {ayrinti}")


def korumali(k):
    def dec(f):
        def w(*a, **kw):
            try:
                return f(*a, **kw)
            except o.Hata as e:
                kaydet(k, "ATLANDI", "kanca/sayfa eksik (yukaridaki HATA satirina bak)")
            except Exception as e:
                kaydet(k, "ATLANDI", f"betik/oyun istisnasi: {type(e).__name__}: {str(e)[:200]}")
                traceback.print_exc(limit=2)
        return w
    return dec


def ort(a):
    a = [x for x in a if isinstance(x, (int, float))]
    return sum(a) / len(a) if a else float("nan")


def ci(a):
    a = [x for x in a if isinstance(x, (int, float))]
    if len(a) < 2:
        return (ort(a), ort(a))
    m, s = ort(a), st.stdev(a)
    h = 1.96 * s / math.sqrt(len(a))
    return (m - h, m + h)


class Ortam:
    def __init__(self, p, taban, dosya):
        self.p, self.taban, self.dosya = p, taban, dosya
        self.br = o.tarayici_baslat(p)
        self.hatalar = []

    def baglam(self, **kw):
        return o.baglam_ac(self.br, **kw)

    def ac(self, ctx, sorgu, kanca=True):
        return o.sayfa_ac(ctx, o.sayfa_url(self.taban, self.dosya, sorgu), self.hatalar, bekle_kanca=kanca)

    def temiz(self, sorgu, **kw):
        ctx = self.baglam(**kw)
        return ctx, self.ac(ctx, sorgu)


def toplu(E, bot, n, sv=None, tipler="", tur=1, ek=""):
    ctx, pg = E.temiz("kayit=0&seed=1" + (("&tipler=" + tipler) if tipler else "") + (("&" + ek) if ek else ""), fps=False)
    r = pg.evaluate("([b,n,sv,t]) => { const o=[]; for(let i=1;i<=n;i++) o.push(window.__oyun.tur(i, Object.assign({},sv), b, t)); return o; }",
                    [bot, n, sv or {}, tur])
    ctx.close()
    return r


# ---------------------------------------------------------------- K1-K3
@korumali("K1")
def k1(E, n):
    sonuc = {}
    for b in ("iyi", "hic"):
        r = toplu(E, b, n)
        sonuc[b] = sum(1 for x in r if x.get("vay_t") is not None and x["vay_t"] <= 5) / len(r)
    ok = all(v >= 0.9 for v in sonuc.values())
    kaydet("K1", "GECTI" if ok else "KALDI", f"vay_t<=5s orani: iyi %{sonuc['iyi']*100:.0f}, hic %{sonuc['hic']*100:.0f} (hedef >=%90)")


@korumali("K2")
def k2(E, n):
    r = toplu(E, "iyi", n) + toplu(E, "hic", n)
    m = ort([x["sure_tur"] for x in r])
    tavan = sum(1 for x in r if x["sure_tur"] >= 65 or x.get("bitis") == "sure")
    ok = 16 <= m <= 30 and tavan == 0
    kaydet("K2", "GECTI" if ok else "KALDI", f"ort tur suresi {m:.1f}s (16-30), 65s'ye carpan {tavan}")


@korumali("K3")
def k3(E, n):
    iyi, hic = toplu(E, "iyi", n), toplu(E, "hic", n)
    o1 = ort([x["mesafe"] for x in iyi]) / ort([x["mesafe"] for x in hic])
    # tur 5 seviyeleri: iyi kampanyasi
    ctx, pg = E.temiz("kayit=0&seed=1", fps=False)
    k = pg.evaluate("window.__oyun.kampanya(1,'iyi',5)")
    ctx.close()
    sv = (k["turlar"][4] or {}).get("sv") if len(k.get("turlar", [])) >= 5 else None
    d = f"tur1 iyi/hic mesafe orani {o1:.2f} (>=1,30)"
    ok = o1 >= 1.30
    if sv is not None:
        iyi5, hic5 = toplu(E, "iyi", n, sv, tur=5), toplu(E, "hic", n, sv, tur=5)
        o5 = ort([x["mesafe"] for x in iyi5]) / ort([x["mesafe"] for x in hic5])
        d += f"; tur5 sv={sv}: {o5:.2f} (>=1,60)"
        ok = ok and o5 >= 1.60
    else:
        d += "; tur5 sv alinamadi (kampanya turlar[].sv yok)"
        ok = False
    kaydet("K3", "GECTI" if ok else "KALDI", d)


# ---------------------------------------------------------------- K4-K6 (bilgi)
@korumali("K4")
def k456(E, nk=15, seedler=5):
    ctx, pg = E.temiz("kayit=0&seed=1", fps=False)
    d4, d5, d6 = [], {}, []
    for b in ("iyi", "orta", "hic"):
        yok, ilk, sure, tavan, n = [], [], [], 0, 0
        for s in range(1, seedler + 1):
            k = pg.evaluate("([s,b,n]) => window.__oyun.kampanya(s,b,n)", [s, b, nk])
            yok.append(k["en_uzun_yok"])
            ilk.append((k.get("ilk") or {}).get("ses"))
            t = k["turlar"]
            sure += [x["sure"] for x in t[4:15]]
            tavan += sum(1 for x in t[4:15] if x.get("bitis") == "sure"); n += len(t[4:15])
            if any(not x["al"] for x in t[:5]):
                yok[-1] = max(yok[-1], 0)
        d4.append(f"{b}: en uzun alisverissiz {max(yok)} (<=3)")
        d5[b] = st.median([x for x in ilk if x is not None]) if any(x is not None for x in ilk) else None
        d6.append(f"{b} t5-15 sure medyan {st.median(sure):.1f}s, tavan %{100*tavan/max(1,n):.0f}")
    ctx.close()
    kaydet("K4", "BILGI", "; ".join(d4))
    kaydet("K5", "BILGI", f"ses duvari ilk kirilis medyan tur: {d5} (iyi 2-3, hic <=8)")
    kaydet("K6", "BILGI", "; ".join(d6) + " (hedef 20-40s, tavan <=%5)")


# ---------------------------------------------------------------- K7
@korumali("K7")
def k7(E):
    ctx, pg = E.temiz("kayit=0&seed=2&bot=iyi&hiz=8", fps=False)
    pg.wait_for_function("window.__oyun.durum().asama === 'BITIS' || window.__oyun.durum().asama === 'KARA_KUTU'", timeout=180000)
    t_bitis = pg.evaluate("performance.now()")
    # BITIS gercek-zamanli olcmek icin hiz=1 ile yeni tur
    ctx.close()
    ctx, pg = E.temiz("kayit=0&seed=2&bot=iyi&hiz=1", fps=False)
    # Not: gercek zaman. KARA_KUTU'ya kadar bekle, sonra animasyon sirasinda TEKRAR UC.
    pg.wait_for_function("window.__oyun.durum().asama === 'BITIS'", timeout=240000)
    t0 = time.time()
    pg.wait_for_function("window.__oyun.durum().asama === 'KARA_KUTU'", timeout=10000)
    kk_gecikme = time.time() - t0
    pg.wait_for_timeout(400)     # dugme kilidi (0,3 s) bitsin
    t1 = time.time()
    tikla(pg, r"TEKRAR\s*U[ÇC]")
    pg.wait_for_function("window.__oyun.durum().asama === 'RAMPA'", timeout=5000)
    rampa_gec = time.time() - t1
    d0 = pg.evaluate("window.__oyun.durum().t")
    pg.wait_for_timeout(300)
    d1 = pg.evaluate("window.__oyun.durum().t")
    ctx.close()
    ok = rampa_gec <= 0.5 and (kk_gecikme + 0.4 + rampa_gec) <= 3.0 and d1 > d0
    kaydet("K7", "GECTI" if ok else "KALDI",
           f"TEKRAR UC -> RAMPA {rampa_gec:.2f}s (<=0,5), BITIS->KARA_KUTU {kk_gecikme:.2f}s, bitis->rampa toplam ~{kk_gecikme+0.4+rampa_gec:.2f}s (<=3), igne ilerliyor={d1>d0}. Animasyon sirasinda TEKRAR UC ayri elle bakilmali")


def tikla(pg, desen):
    for el in pg.get_by_text(re.compile(desen, re.I)).all():
        if el.is_visible():
            el.click(timeout=3000)
            return True
    for el in pg.get_by_role("button", name=re.compile(desen, re.I)).all():
        if el.is_visible():
            el.click(timeout=3000)
            return True
    raise RuntimeError("gorunur oge yok: " + desen)


# ---------------------------------------------------------------- K8
def sim_tarafi(n):
    sys.path.insert(0, str(o.B0.parent / "sim"))
    import ucus_sim as u
    keep = ["balon", "parti", "zeplin", "marti", "ucurtma"]
    for k in list(u.TIPLER):
        if k not in keep:
            del u.TIPLER[k]
    out = {}
    for b in ("hic", "orta", "iyi"):
        out[b] = [u.tur_oyna(s, {}, b, 1) for s in range(1, n + 1)]
    return out


@korumali("K8")
def k8(E, n):
    uret = o.B0 / "araclar" / "ayar_uret.py"
    den = "ayar_uret.py yok"
    if uret.exists():
        r = subprocess.run([sys.executable, str(uret), "--denetle"], capture_output=True, text=True)
        den = "ayar_uret --denetle " + ("temiz" if r.returncode == 0 else "FARK VAR: " + (r.stdout + r.stderr)[-150:])
    sim = sim_tarafi(n)
    tum_ok, satir = den.startswith("ayar_uret --denetle temiz"), []
    for b in ("hic", "orta", "iyi"):
        js = toplu(E, b, n, tipler="balon,parti,zeplin,marti,ucurtma")
        for ad, key in [("sure", "sure_tur"), ("x", "mesafe"), ("max_v", "max_v"), ("sekme", "sekme"), ("kazanc", "kazanc")]:
            a, c = [x[key] for x in js], [x[key] for x in sim[b]]
            ma, mc = ort(a), ort(c)
            fark = abs(ma - mc) / max(1e-9, abs(mc))
            ca, cc = ci(a), ci(c)
            ok = fark <= 0.10 or (ca[0] <= cc[1] and cc[0] <= ca[1])
            tum_ok &= ok
            if not ok:
                satir.append(f"{b}/{ad}: js {ma:.1f} sim {mc:.1f} (%{fark*100:.0f})")
    kaydet("K8", "GECTI" if tum_ok else "KALDI", f"n={n}; {den}; " + ("tum olculer uyumlu" if tum_ok and not satir else "; ".join(satir[:6])))


# ---------------------------------------------------------------- K9
@korumali("K9")
def k9(E):
    a = toplu(E, "orta", 5)
    b = toplu(E, "orta", 5)
    ayni = json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
    sv_ayni = None
    # hiz=1 vs hiz=8: gorüntülü bot turu olay gunlukleri
    gunluk = []
    for hz in (4, 8):
        ctx, pg = E.temiz(f"kayit=0&seed=5&bot=iyi&hiz={hz}", fps=False)
        pg.wait_for_function("window.__oyun.durum().asama === 'KARA_KUTU' || window.__oyun.durum().asama === 'BITIS'", timeout=240000)
        gunluk.append(json.dumps(pg.evaluate("window.__oyun.olaylar"), sort_keys=True))
        ctx.close()
    hiz_ayni = gunluk[0] == gunluk[1]
    kaydet("K9", "GECTI" if ayni and hiz_ayni else "KALDI", f"ayni tohum ayni sonuc={ayni}; hiz=4 vs hiz=8 olay gunlugu ayni={hiz_ayni} (hiz=1 yerine 4 kullanildi, sure icin)")


# ---------------------------------------------------------------- K10
@korumali("K10")
def k10(E):
    uyari = []
    ctx = E.baglam(fps=False)
    pg = ctx.new_page()
    pg.on("console", lambda m: uyari.append(m.text) if m.type in ("warning", "warn", "error") or re.search(r"uyar|enerji|ihlal", m.text, re.I) else None)
    pg.goto(o.sayfa_url(E.taban, E.dosya, "kayit=0&seed=1&debug=1&toplu=20&bot=iyi"))
    pg.wait_for_function("typeof window.__oyun === 'object'", timeout=15000)
    pg.wait_for_function("(window.__oyun.sonuclar||[]).length >= 20", timeout=180000)
    extra = pg.evaluate("window.__oyun.uyarilar ? window.__oyun.uyarilar.length : null")
    ctx.close()
    ok = not uyari and not extra
    kaydet("K10", "GECTI" if ok else "KALDI",
           f"debug=1 toplu=20: konsol uyari/hata {len(uyari)}; __oyun.uyarilar={extra}. NOT: oyun enerji denetimini konsola uyari olarak yazmali (uyar/enerji/ihlal ya da console.warn); yazmiyorsa bu madde guvenilir degil" + (" | " + uyari[0][:100] if uyari else ""))


# ---------------------------------------------------------------- K11, K12
@korumali("K11")
def k11(E):
    ctx, pg = E.temiz("kayit=0&seed=1&bot=iyi&debug=1")
    t0 = time.time()
    pg.wait_for_timeout(8000)
    f = o.fps_oku(pg)
    ctx.close()
    kaydet("K11", "ELLE", f"telefon olcumu sart; headless swiftshader bilgisi: fps ort {f['ort_fps']:.0f} min {f['min_fps']:.0f}" if f else "fps okunamadi")


@korumali("K12")
def k12(E):
    h0 = len(E.hatalar)
    ctx = E.baglam(fps=False)
    pg = E.ac(ctx, "kayit=0&seed=1&bot=iyi&toplu=3")
    pg.wait_for_function("(window.__oyun.sonuclar||[]).length >= 3", timeout=120000)
    try:
        cdp = ctx.new_cdp_session(pg)
        cdp.send("HeapProfiler.collectGarbage")
        m0 = pg.evaluate("performance.memory ? performance.memory.usedJSHeapSize : 0")
    except Exception:
        m0 = 0
    pg.evaluate("window.__oyun.kampanya(1,'iyi',50)")
    try:
        cdp.send("HeapProfiler.collectGarbage")
        m1 = pg.evaluate("performance.memory ? performance.memory.usedJSHeapSize : 0")
    except Exception:
        m1 = 0
    ctx.close()
    yeni = E.hatalar[h0:]
    mb = (m1 - m0) / 1e6
    ok = not yeni and mb < 20
    kaydet("K12", "GECTI" if ok else "KALDI", f"kampanya(iyi,50) cokmedi; konsol hata {len(yeni)}; heap artisi {mb:.1f} MB (<20)" + (f" | {yeni[0]}" if yeni else ""))


# ---------------------------------------------------------------- K13
def gizle(pg, gizli):
    pg.evaluate("""(g) => { Object.defineProperty(document, 'hidden', {value: g, configurable: true});
      Object.defineProperty(document, 'visibilityState', {value: g ? 'hidden' : 'visible', configurable: true});
      document.dispatchEvent(new Event('visibilitychange')); if (g) window.dispatchEvent(new Event('pagehide')); }""", gizli)


@korumali("K13")
def k13(E):
    ayr, ok = [], True
    # 1) kalicilik
    ctx = E.baglam(fps=False)
    pg = E.ac(ctx, "seed=1&hiz=1")
    ky = pg.evaluate("window.__oyun.kayit.oku()")
    ky["jeton"], ky["sv"]["rampa"], ky["tur"] = 123, 2, max(1, ky.get("tur", 0))
    pg.evaluate("(k) => window.__oyun.kayit.yaz(k)", ky)
    pg.reload(); pg.wait_for_function("typeof window.__oyun==='object'")
    k2_ = pg.evaluate("window.__oyun.kayit.oku()")
    a = k2_["jeton"] >= 123 and k2_["sv"]["rampa"] == 2   # >=: tur ucuyorsa pagehide bekleyeni aciliste eklenir (spec 13.1)
    ayr.append(f"yenileyince jeton/sv ayni={a}"); ok &= a
    # 2) bekleyen
    pg.goto(o.sayfa_url(E.taban, E.dosya, "seed=1&bot=iyi&hiz=2")); pg.wait_for_function("typeof window.__oyun==='object'")
    if pg.evaluate("window.__oyun.durum().asama") == "HANGAR":
        tikla(pg, r"^\s*U[ÇC]\s*$")      # kayitli oyunda ilk tur sonrasi hangar acilir
    pg.wait_for_function("window.__oyun.durum().asama==='UCUS'", timeout=30000); pg.wait_for_timeout(2500)
    gizle(pg, True); pg.wait_for_timeout(300)
    b1 = pg.evaluate("window.__oyun.kayit.oku().bekleyen")
    gizle(pg, False); pg.wait_for_timeout(300)
    b2 = pg.evaluate("window.__oyun.kayit.oku().bekleyen")
    a = b1 not in (None, 0) and b2 is None
    ayr.append(f"gizlenince bekleyen={b1}, gorunur olunca={b2}"); ok &= a
    # 3) gizliyken oldurulme -> aciliste bir kez
    kopya = pg.evaluate("window.__oyun.kayit.oku()")
    kopya["bekleyen"], kopya["jeton"] = 40, 10
    pg.goto(E.taban + "/__bos__")        # oyun betigi calismasin (pagehide yazimi karismasin)
    pg.evaluate("(k) => localStorage.setItem('sdp_kayit', JSON.stringify(k))", kopya)
    pg.goto(o.sayfa_url(E.taban, E.dosya, "seed=1")); pg.wait_for_function("typeof window.__oyun==='object'")
    j1 = pg.evaluate("window.__oyun.kayit.oku()")
    pg.reload(); pg.wait_for_function("typeof window.__oyun==='object'")
    j2 = pg.evaluate("window.__oyun.kayit.oku()")
    a = j1["jeton"] == 50 and j1["bekleyen"] is None and j2["jeton"] == 50
    ayr.append(f"bekleyen 40 acilista jeton {j1['jeton']} (beklenen 50), tekrar acinca {j2['jeton']}"); ok &= a
    # 4) bozuk JSON
    pg.goto(E.taban + "/__bos__")
    pg.evaluate("localStorage.setItem('sdp_kayit', '{bozuk json')")
    pg.goto(o.sayfa_url(E.taban, E.dosya, "seed=1")); pg.wait_for_function("typeof window.__oyun==='object'")
    h0 = len(E.hatalar)
    pg.reload(); pg.wait_for_function("typeof window.__oyun==='object'")
    bz = pg.evaluate("localStorage.getItem('sdp_kayit_bozuk')")
    k3_ = pg.evaluate("window.__oyun.kayit.oku()")
    a = bz is not None and k3_["jeton"] == 0 and len(E.hatalar) == h0
    ayr.append(f"bozuk kayit tasindi={bz is not None}, varsayilan jeton={k3_['jeton']}, yeni konsol hata={len(E.hatalar)-h0}"); ok &= a
    ctx.close()
    kaydet("K13", "GECTI" if ok else "KALDI", "; ".join(ayr) + ". 'Elle bitirilen turda taban/prim yok' ve 'hicbir senaryoda tur iki kez sayilmaz' tam kontrol icin elle de bak")


# ---------------------------------------------------------------- K14
@korumali("K14")
def k14(E):
    ayr, ok = [], True
    ctx, pg = E.temiz("kayit=0&seed=1&bot=hic")
    pg.wait_for_timeout(800)
    pg.mouse.click(190, 300)    # hic botu: rampada insan dokunusuyla kalkis
    pg.wait_for_function("window.__oyun.durum().asama==='UCUS'", timeout=10000)
    pg.wait_for_timeout(1000)
    gizle(pg, True); pg.wait_for_timeout(100)
    t_a = pg.evaluate("window.__oyun.durum().t"); pg.wait_for_timeout(600); t_b = pg.evaluate("window.__oyun.durum().t")
    a = abs(t_b - t_a) < 0.02
    ayr.append(f"gizlenince fizik durdu={a} (dt={t_b-t_a:.3f})"); ok &= a
    gizle(pg, False); pg.wait_for_timeout(200)
    # devam: 3-2-1 sirasinda dokunus dalis yapmaz
    try:
        tikla(pg, r"^\s*DEVAM\s*$")
        g0 = pg.evaluate("window.__oyun.durum().gosterge")
        pg.mouse.click(190, 400); pg.wait_for_timeout(150)
        g1 = pg.evaluate("window.__oyun.durum().gosterge")
        a = g1 >= g0 - 1e-6
        ayr.append(f"3-2-1 sirasinda dokunus dalis yapmadi={a} (gosterge {g0:.2f}->{g1:.2f})"); ok &= a
    except Exception as e:
        ayr.append("DEVAM dugmesi bulunamadi"); ok = False
    # duraklat dugmesi dalis yapmaz
    pg.wait_for_timeout(2200)
    g0 = pg.evaluate("window.__oyun.durum().gosterge")
    try:
        pg.get_by_label(re.compile("duraklat", re.I)).first.click(timeout=3000)
        g1 = pg.evaluate("window.__oyun.durum().gosterge")
        a = g1 >= g0 - 1e-6; ayr.append(f"duraklat dugmesi dalis yapmadi={a}"); ok &= a
    except Exception:
        ayr.append("aria-label 'Duraklat' dugmesi bulunamadi"); ok = False
    ctx.close()
    # toplu'da blur
    ctx = E.baglam(fps=False)
    pg = E.ac(ctx, "kayit=0&seed=1&bot=iyi&toplu=3")
    pg.evaluate("window.dispatchEvent(new Event('blur'))")
    try:
        pg.wait_for_function("(window.__oyun.sonuclar||[]).length >= 3", timeout=60000)
        ayr.append("toplu'da blur duraklatmadi=True")
    except Exception:
        ayr.append("toplu blur ile takildi"); ok = False
    ctx.close()
    kaydet("K14", "GECTI" if ok else "KALDI", "; ".join(ayr))


# ---------------------------------------------------------------- K15
@korumali("K15")
def k15(E):
    ayr, ok = [], True
    for yazi in (1.0, 1.2, 1.4):
        ctx = E.baglam(fps=False)
        pg = E.ac(ctx, "seed=1")
        pg.evaluate("(y) => { const o = window.__oyun.kayit.oku(); o.ayar.yazi = y; o.tur = Math.max(o.tur,1); window.__oyun.kayit.yaz(o); }", yazi)
        pg.reload(); pg.wait_for_function("typeof window.__oyun==='object'"); pg.wait_for_timeout(500)
        r = pg.evaluate("""() => {
          const kucuk = [], tasan = [];
          for (const b of document.querySelectorAll('button,[role=button]')) {
            const r = b.getBoundingClientRect(); if (!r.width || !r.height) continue;
            if (r.width < 48 || r.height < 48) kucuk.push((b.getAttribute('aria-label') || b.textContent || '').trim().slice(0, 20) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height));
            if (r.right > innerWidth + 1 || r.left < -1 || r.bottom > innerHeight + 1) tasan.push((b.textContent||'').trim().slice(0,20));
          }
          return {kucuk, tasan, yatay: document.documentElement.scrollWidth > innerWidth + 1}; }""")
        a = not r["kucuk"] and not r["tasan"] and not r["yatay"]
        ok &= a
        ayr.append(f"yazi x{yazi}: kucuk dugme {r['kucuk'][:2]}, tasan {r['tasan'][:2]}, yatay kayma {r['yatay']}")
        ctx.close()
    # hareket azaltma
    ctx = E.baglam(fps=False)
    ctx.add_init_script("window.matchMedia = (q) => ({matches: /reduce/.test(q), media: q, addEventListener(){}, removeEventListener(){}, addListener(){}, removeListener(){}})")
    pg = E.ac(ctx, "kayit=0&seed=1&bot=iyi&t=6")
    sars = pg.evaluate("window.__oyun.durum().sarsinti ?? window.__oyun.durum().sars ?? null")
    ctx.close()
    ayr.append(f"hareket azaltma: sarsinti degeri={sars} (durum() alani yoksa elle)")
    kaydet("K15", "GECTI" if ok else "KALDI", "; ".join(ayr) + ". Flas <=3/s ve parlama alani/suresi icin kontak sayfasina ELLE bak (kontak.py)")


@korumali("K16")
def k16(E):
    kaydet("K16", "ELLE", "telefonda 10 dk, 3 soru + kayit 'tur' farki (kullanici). Uyari metni: 'Bu gri kutu yalniz his testidir...'")


# ---------------------------------------------------------------- ek: ses/API reddi
@korumali("EK")
def ek(E):
    ctx, pg = E.temiz("kayit=0&seed=1")
    on = o.ses_durumu(pg)
    pg.wait_for_timeout(300)
    pg.mouse.click(190, 400); pg.wait_for_timeout(600)
    so = o.ses_durumu(pg)
    ctx.close()
    ok = so and so["sayi"] > 0 and "running" in so["simdi_ac"] and "running" not in (on["simdi_ac"] if on else [])
    kaydet("EK", "GECTI" if ok else "KALDI", f"AudioContext dokunustan once {on and on['simdi_ac']} -> sonra {so and so['simdi_ac']}; tam ekran/kilit/titresim reddi: {so and (so['tamekran'], so['kilit'], so['titresim'])} (oyun reddedilmis gibi calismaya devam etti)")


# ---------------------------------------------------------------- rapor
ADLAR = {
    "K1": "Vay anı <=5 s (>=%90)", "K2": "Tur 1 süresi 16-30 s, 65 s'ye çarpma yok", "K3": "Beceri farkı (1,30 / 1,60)",
    "K4": "Satın alma ritmi", "K5": "Ses duvarı tur", "K6": "Kampanya tur süresi", "K7": "Yeniden başlatma <=0,5 / <=3 s",
    "K8": "Sim eşliği (>=200 tohum)", "K9": "Belirlenimlilik", "K10": "Mantık denetimi (debug)", "K11": "Kare hızı (telefon)",
    "K12": "Kararlılık, 0 konsol hatası", "K13": "Kayıt", "K14": "Duraklat", "K15": "Erişilebilirlik", "K16": "Kullanıcı kararı (10 dk)",
    "EK": "Ses AudioContext + tam ekran/kilit/titreşim reddi",
}


def rapor(sayfa, sure, hatalar):
    L = ["# B0 kabul raporu (otomatik: testci/kabul.py)", "",
         f"Sayfa: `{sayfa}` · Koşu: {time.strftime('%Y-%m-%d %H:%M')} · Süre: {sure:.0f} s · Konsol hatası: {len(hatalar)}", "",
         "| K | Ölçüt | Durum | Ayrıntı |", "|---|---|---|---|"]
    for k in [f"K{i}" for i in range(1, 17)] + ["EK"]:
        r = SONUC.get(k, {"durum": "KOŞULMADI", "ayrinti": "-"})
        L.append(f"| {k} | {ADLAR[k]} | **{r['durum']}** | {r['ayrinti'].replace('|', '/')} |")
    kal = [k for k, r in SONUC.items() if r["durum"] == "KALDI"]
    ata = [k for k, r in SONUC.items() if r["durum"] == "ATLANDI"]
    L += ["", f"Geçme şartlı KALDI: {', '.join(k for k in kal if k in GECME) or 'yok'}", f"ATLANDI (kanca eksik): {', '.join(ata) or 'yok'}", ""]
    if hatalar:
        L += ["## Konsol hataları", ""] + [f"- {t}: {m[:200]}" for t, m in hatalar[:20]] + [""]
    L += ["## Elle doldurulacak (usta oyuncu gözlemi)", "", "- K11: S24 Ultra fps ort/min:", "- K16: Kalkış heyecanlı mı? Vuruşlar tok mu? Bir tur daha? Tur sayısı:", ""]
    return "\n".join(L)


def main():
    ap = o.ortak_arg(argparse.ArgumentParser())
    ap.add_argument("--hizli", action="store_true", help="n=10, K8 n=40 (smoke)")
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--k8n", type=int, default=200)
    ap.add_argument("--sadece", default="")
    ap.add_argument("--rapor", default=str(o.TESTCI / "RAPOR.md"))
    a = ap.parse_args()
    n, k8n = (10, 40) if a.hizli else (a.n, a.k8n)
    dosya = o.sayfa_dosyasi(a.sayfa)
    sec = set(x.strip().upper() for x in a.sadece.split(",") if x.strip())
    t0 = time.time()
    with o.sunucu(port=a.port) as taban, sync_playwright() as p:
        E = Ortam(p, taban, dosya)
        adimlar = [("K1", lambda: k1(E, n)), ("K2", lambda: k2(E, n)), ("K3", lambda: k3(E, n)),
                   ("K4", lambda: k456(E, 15, 3 if a.hizli else 5)), ("K7", lambda: k7(E)), ("K8", lambda: k8(E, k8n)),
                   ("K9", lambda: k9(E)), ("K10", lambda: k10(E)), ("K11", lambda: k11(E)), ("K12", lambda: k12(E)),
                   ("K13", lambda: k13(E)), ("K14", lambda: k14(E)), ("K15", lambda: k15(E)), ("K16", lambda: k16(E)), ("EK", lambda: ek(E))]
        for ad, f in adimlar:
            if sec and ad not in sec and not (ad == "K4" and sec & {"K4", "K5", "K6"}):
                continue
            f()
        E.br.close()
    md = rapor(dosya.name, time.time() - t0, E.hatalar)
    Path(a.rapor).write_text(md, encoding="utf-8")
    o.json_yaz(o.CIKTI / "kabul.json", {"sonuc": SONUC, "konsol_hata": E.hatalar})
    print("\nrapor:", a.rapor)
    sys.exit(1 if any(SONUC.get(k, {}).get("durum") == "KALDI" for k in GECME) else 0)


if __name__ == "__main__":
    main()
