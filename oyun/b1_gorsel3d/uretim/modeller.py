# Son Durak: Plüton · B1 3B modeller, 2. yön (olgun/premium) · Blender 5.0.1 / bpy 5.0.1 ile denendi
# Kopabilen parçalar adlandırılmıştır: roket/kademe_1, kademe_2, burun, kanat_*, nozul, pencere, kablo_kanali;
# zeplin/kanat_*, gondol, motor_*, pervane; balon/sepet, tabela, brulor.
import math, random
from mathutils import Vector
import ortak as O
from ortak import (plastik, isikli, kabuk, yumusat, torna, yay, plaka, kure, silindir, simit, metatop, detayli, boru,
                   elips, nokta, bez, serit, K, agiz, sisir, ic_bolge, Yuzey, cikartma, bos, lin, _m, _mix, _smooth)

# ================================================================= palet (sRGB) — daha olgun, uyumlu: kırmızı-krem-lacivert + altın/teal vurgu
P = dict(kirmizi="#e3343c", kirmizi_k="#a81f2a", beyaz="#f6f3ec", gri="#9ba3b0", koyu_gri="#3a4150", civit=O.CIVIT,
         mor="#6a4fe0", krem="#f1e7d2", sari="#f2b33d", teal="#14a99a", lacivert="#22305e", ten="#f0b896",
         sac="#3a2418", agiz_ic="#5a1424", dil="#d9566e", ter="#8fdcff", altin="#e2a73c", iris="#5a7fb8")

def _xyz(N, L):
    tc = N.new("ShaderNodeTexCoord"); sp = N.new("ShaderNodeSeparateXYZ"); L.new(tc.outputs["Object"], sp.inputs[0]); return sp

# ================================================================= yüz kurucu (olgun oranlar: badem göz + iris + göz kapağı çizgisi)
def _badem(cx, cy, rx, ry, egim=0.0, alt_oran=0.75):
    """Badem göz: üst kavis yüksek, alt kavis basık; egim: dış köşe yukarı (+)."""
    def u(s): return cy + ry * (1 - s * s) ** 0.62 + egim * s * ry
    def a(s): return cy - ry * alt_oran * (1 - s * s) ** 0.85 + egim * s * ry
    return agiz(cx, 0, rx * 2, lambda s: u(s), lambda s: a(s))

def _kirp_icine(sek, goz):
    """Şekli (iris/bebek) göz şeklinin içine sıkıştır (kapak altında kalsın)."""
    gu, ga = goz
    xs = [p[0] for p in gu]
    def sinir(x):
        x = min(max(x, xs[0]), xs[-1])
        for i in range(len(xs) - 1):
            if xs[i] <= x <= xs[i + 1]:
                t = (x - xs[i]) / max(xs[i + 1] - xs[i], 1e-9)
                return x, gu[i][1] * (1 - t) + gu[i + 1][1] * t, ga[i][1] * (1 - t) + ga[i + 1][1] * t
        return x, gu[-1][1], ga[-1][1]
    def kp(p):
        x, ut, al = sinir(p[0]); return (x, min(max(p[1], al), ut))
    return [kp(p) for p in sek[0]], [kp(p) for p in sek[1]]

def yuz_kur(ad, yuzey, kok, F, ifadeler, kas_renk=None, birim=0.004, iris_renk=None):
    ex, ey, rx, ry, lw = F["ex"], F["ey"], F["rx"], F["ry"], F["lw"]
    mx, my, mw = F["mx"], F["my"], F["mw"]
    cx = F.get("cx", 0.0)
    parcalar = {}
    def ekle(parca, ifade, sek): parcalar.setdefault(parca, {})[ifade] = sek
    for ia, sp in ifadeler.items():
        for sd in (-1, 1):
            k = "l" if sd < 0 else "r"
            gx = cx + sd * ex
            tip = sp.get("goz", "acik"); go = sp.get("goz_olcek", 1.0)
            ryy = ry * go; rxx = rx * sp.get("goz_gen", 1.0)
            if tip in ("acik", "genis", "yari"):
                eg = sp.get("egim", 0.15) * (1 if sd > 0 else -1) * 0  # simetrik eğim (dış köşe)
                ak = _badem(gx, ey, rxx, ryy, 0.0, 0.8 if tip != "genis" else 0.95)
                if tip == "yari":
                    ust = ey + ryy * sp.get("kapak", 0.3)
                    ak = ([(p[0], min(p[1], ust)) for p in ak[0]], [(p[0], min(p[1], ust)) for p in ak[1]])
                cz = sisir(ak, lw * 0.55)
                ir = min(rxx * 0.62, ryy * 1.15) * sp.get("bebek", 1.0)
                bx, by = sp.get("bakis", (0.15, 0.0))
                pcx = gx + bx * (rxx - ir) * 0.8; pcy = ey + by * ryy * 0.3
                iris = _kirp_icine(elips(pcx, pcy, ir, ir), ak)
                beb = _kirp_icine(elips(pcx, pcy, ir * 0.48, ir * 0.48), ak)
                i1 = _kirp_icine(elips(pcx - ir * 0.32, pcy + ir * 0.34, ir * 0.22, ir * 0.22), ak)
                # üst kapak çizgisi (kalın, dışta hafif kanat)
                ust = ak[0]
                kap_u, kap_a = [], []
                for i_, p_ in enumerate(ust):
                    s_ = -1 + 2 * i_ / (K - 1); w_ = lw * (0.25 + 0.75 * (1 - s_ * s_) ** 0.5) + lw * 0.35 * max(0, s_ * sd)
                    kap_u.append((p_[0], p_[1] + w_)); kap_a.append((p_[0], p_[1] - lw * 0.15))
                kap = (kap_u, kap_a)
                ekle(f"goz_{k}_cizgi", ia, cz); ekle(f"goz_{k}_ak", ia, ak); ekle(f"goz_{k}_iris", ia, iris)
                ekle(f"goz_{k}_bebek", ia, beb); ekle(f"goz_{k}_isik1", ia, i1); ekle(f"goz_{k}_kapak", ia, kap)
            else:
                if tip == "mutlu":
                    cz = serit(bez((gx - rxx, ey - ryy * 0.3), (gx, ey + ryy * 1.3), (gx + rxx, ey - ryy * 0.3)), lw * 1.7, 0.5)
                else:  # sikik
                    yon = -sd
                    cz = serit(bez((gx - yon * rxx * 0.95, ey + ryy * 0.9), (gx + yon * rxx * 1.15, ey), (gx - yon * rxx * 0.95, ey - ryy * 0.9)), lw * 1.7, 0.5)
                p0 = nokta(gx, ey)
                ekle(f"goz_{k}_cizgi", ia, cz)
                for n in ("ak", "iris", "bebek", "isik1", "kapak"): ekle(f"goz_{k}_{n}", ia, p0)
            kh, kt, kc = sp.get("kas", (0.5, 0.0, 0.1))
            by0 = ey + ryy + kh * ry
            dis_x = gx + sd * rxx * 1.25; ic_x = gx - sd * rxx * 0.85
            p_dis = (dis_x, by0 - kt * rx * 0.35); p_ic = (ic_x, by0 + kt * rx * 0.9)
            orta = ((p_dis[0] * 0.55 + p_ic[0] * 0.45), (p_dis[1] + p_ic[1]) / 2 + kc * ry)
            a0, a2 = (p_dis, p_ic) if sd < 0 else (p_ic, p_dis)
            # kaş: içte kalın, dışa doğru incelen
            e = bez(a0, orta, a2); ust_, alt_ = [], []
            for i in range(K):
                t = i / (K - 1); p = e(t); p1 = e(min(1, t + 1e-3)); p0_ = e(max(0, t - 1e-3))
                tx, ty = p1[0] - p0_[0], p1[1] - p0_[1]; n = math.hypot(tx, ty) or 1; nx, ny = -ty / n, tx / n
                ic_t = t if sd < 0 else 1 - t
                w = lw * (0.9 + 1.6 * ic_t) * (max(0.0, math.sin(math.pi * t)) ** 0.25) / 2
                ust_.append((p[0] + nx * w, p[1] + ny * w)); alt_.append((p[0] - nx * w, p[1] - ny * w))
            ekle(f"kas_{k}", ia, (ust_, alt_))
        t = sp.get("agiz", "gulumse"); P0 = nokta(mx, my)
        if t in ("gulumse", "smirk", "dalga", "duz"):
            g = mw * 0.45
            if t == "dalga":
                cz = serit(lambda s: (mx - g + 2 * g * s, my + mw * 0.05 * math.sin(s * math.pi * 3.0)), lw * 1.2, 0.35)
            elif t == "duz":
                cz = serit(bez((mx - g, my), (mx, my - mw * 0.03), (mx + g, my)), lw * 1.2, 0.35)
            elif t == "smirk":   # tek yana kalkık güvenli gülüş
                cz = serit(lambda s: (mx - g + 2 * g * s, my - mw * 0.06 * math.sin(math.pi * s) + mw * 0.12 * s ** 3), lw * 1.25, 0.4)
            else:
                cz = serit(bez((mx - g, my + mw * 0.07), (mx, my - mw * 0.2), (mx + g, my + mw * 0.07)), lw * 1.25, 0.4)
            ic = dil = dis = disa = P0
        else:
            if t == "acik_gulus":
                sek = agiz(mx, my, mw, lambda s: mw * 0.07 * s * s + mw * 0.03, lambda s: mw * 0.07 * s * s - mw * 0.36 * (1 - s * s) ** 0.85)
                dil = ic_bolge(sek, 0.32, 0.04); dis = ic_bolge(sek, 0.97, 0.70); disa = P0
            elif t == "zafer":
                w2 = mw * 1.15
                sek = agiz(mx, my, w2, lambda s: w2 * 0.12 * s * s + w2 * 0.0, lambda s: w2 * 0.12 * s * s - w2 * 0.38 * (1 - s * s) ** 0.8)
                dil = ic_bolge(sek, 0.30, 0.04); dis = ic_bolge(sek, 0.97, 0.66); disa = P0
            elif t == "O":
                sek = elips(mx, my - mw * 0.06, mw * 0.17, mw * 0.25)
                dil = ic_bolge(sek, 0.3, 0.05); dis = disa = P0
            elif t == "korku":
                hh = lambda s: mw * 0.13 * (1 - s ** 8) ** 0.5
                orta_f = lambda s: -mw * 0.03 - mw * 0.10 * s * s + mw * 0.02 * math.sin(s * 9)
                sek = agiz(mx, my, mw * 1.05, lambda s: orta_f(s) + hh(s), lambda s: orta_f(s) - hh(s))
                dis = ic_bolge(sek, 0.96, 0.54); disa = ic_bolge(sek, 0.46, 0.04); dil = P0
            elif t == "ezik_acik":
                hh = lambda s: mw * 0.11 * (1 - s ** 8) ** 0.5
                orta_f = lambda s: mw * 0.06 * math.sin(s * math.pi * 1.5)
                sek = agiz(mx, my, mw * 1.1, lambda s: orta_f(s) + hh(s), lambda s: orta_f(s) - hh(s))
                dis = ic_bolge(sek, 0.95, 0.52); disa = ic_bolge(sek, 0.48, 0.05); dil = P0
            cz = sisir(sek, lw * 0.6); ic = sek
        ekle("agiz_cizgi", ia, cz); ekle("agiz_ic", ia, ic); ekle("dil", ia, dil); ekle("dis", ia, dis); ekle("dis_alt", ia, disa)
        if "terx" in F:
            if sp.get("ter"):
                tx, ty, tr = F["terx"], F["tery"], F["terr"]
                ekle("ter", ia, agiz(tx, ty, tr * 1.4, lambda s: tr * 1.6 * (1 - abs(s)) ** 1.6, lambda s: -tr * 0.9 * (1 - s * s) ** 0.5))
            else:
                ekle("ter", ia, nokta(F["terx"], F["tery"]))
    kas_renk = kas_renk or O.CIVIT
    M = {"cizgi": isikli("yuz_cizgi", "#24182e"), "ak": plastik("goz_ak", "#f6f3ee", rough=0.18, sss=0.0, kenar=0.0),
         "iris": plastik("iris_" + (iris_renk or P["iris"]), iris_renk or P["iris"], rough=0.15, sss=0, kenar=0, coat=0.8),
         "bebek": plastik("bebek", "#0e0a14", rough=0.1, sss=0.0, kenar=0.0, coat=1.0), "isik": isikli("goz_isik", "#ffffff", 1.0),
         "kapak": isikli("kapak", "#1d1220"), "kas": isikli("kas_" + kas_renk, kas_renk),
         "ic": plastik("agiz_ic", P["agiz_ic"], rough=0.4, sss=0, kenar=0), "dil": plastik("dil", P["dil"], rough=0.35, kenar=0),
         "dis": plastik("dis", "#fbf8f2", rough=0.25, sss=0, kenar=0), "ter": plastik("ter", P["ter"], rough=0.05, kenar=0.6)}
    duzen = {"cizgi": ("cizgi", 2), "ak": ("ak", 3), "iris": ("iris", 4), "bebek": ("bebek", 5), "isik1": ("isik", 6), "kapak": ("kapak", 7),
             "kas": ("kas", 3), "agiz_cizgi": ("cizgi", 2), "agiz_ic": ("ic", 3), "dil": ("dil", 4), "dis": ("dis", 4), "dis_alt": ("dis", 4), "ter": ("ter", 8)}
    yuz = bos(ad + "_yuz", parent=kok)
    for parca, ifs in parcalar.items():
        anahtar = parca.split("_")[-1] if parca.startswith("goz") else ("kas" if parca.startswith("kas") else parca)
        mk, kat = duzen[anahtar]
        cikartma(parca, yuzey, ifs, M[mk], kat, yuz, birim=birim)
    return yuz

# ================================================================= ROKET (ince, ayrıntılı)
def _beyaz_govde(ad, x0=0.0, is_=None):
    return detayli(ad, P["beyaz"], rough=0.38, coat=0.35, panel=dict(eksen="X", adim=0.46, n=8, R=0.40, x0=x0), percin=True,
                   kir=0.45, asinma=0.6, asinma_renk="#9aa1ad", is_=is_, cizik=0.25)

def _kirmizi(ad, panel=None, is_=None, asinma=0.7):
    return detayli(ad, P["kirmizi"], rough=0.33, coat=0.5, panel=panel, percin=bool(panel), kir=0.45, asinma=asinma, asinma_renk="#a9aeb8", is_=is_, cizik=0.2)

def _metal(ad, hexc="#a7aebb", rough=0.32, kir=0.5):
    return detayli(ad, hexc, rough=rough, coat=0.0, metal=1.0, kir=kir, kenar=0.25, cizik=0.4)

def _isi_renk(nt, N, L):
    sp = _xyz(N, L)
    rp = N.new("ShaderNodeValToRGB"); e = rp.color_ramp.elements
    e[0].position = 0.0; e[0].color = lin("#8d93a0"); e[1].position = 1.0; e[1].color = lin("#c5a873")
    e.new(0.35).color = lin("#5d6fae"); e.new(0.62).color = lin("#9a6fa0")
    mr = N.new("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = -3.25; mr.inputs["From Max"].default_value = -2.6
    L.new(sp.outputs["X"], mr.inputs["Value"]); L.new(mr.outputs["Result"], rp.inputs[0])
    return rp.outputs[0]

def _dama_renk(nt, N, L):
    """Ara halkada siyah-krem dama (yuvarlanma işareti, klasik roket)."""
    sp = _xyz(N, L)
    a = _m(N, L, "FLOOR", _m(N, L, "MULTIPLY", _m(N, L, "ARCTAN2", sp.outputs["Z"], sp.outputs["Y"]), 8 / (2 * math.pi)))
    b = _m(N, L, "FLOOR", _m(N, L, "MULTIPLY", sp.outputs["X"], 1 / 0.06))
    f = _m(N, L, "MODULO", _m(N, L, "ABSOLUTE", _m(N, L, "ADD", a, b)), 2)
    return _mix(N, L, f, lin("#1d2030"), lin(P["krem"]))

def roket(pilot_ifade="heyecan", R=0.40):
    kok = bos("roket")
    k1 = bos("kademe_1", parent=kok); k2 = bos("kademe_2", parent=kok)
    hk = 0.012
    BEY1 = _beyaz_govde("govde_1_boya", 0.3, is_=(-3.0, -1.6))
    BEY2 = _beyaz_govde("govde_2_boya", 0.1)
    KIR = _kirmizi("kirmizi_boya")
    KIRP = _kirmizi("kirmizi_panel", panel=dict(eksen="X", adim=0.4, n=6, R=R, x0=0.2))
    MET = _metal("metal"); KMET = _metal("koyu_metal", P["koyu_gri"], 0.4)
    # --- alt kademe
    pr = [(-2.62, 0)] + yay(-2.56, R - 0.06, 0.06, 180, 90) + yay(-0.52, R - 0.05, 0.05, 90, 0) + [(-0.47, 0)]
    g1 = torna("govde_1", pr, BEY1, parent=k1, seg=64); kabuk(yumusat(g1, 1), hk)
    s1 = torna("serit_1", [(-2.45, 0), (-2.45, R + 0.006), (-2.05, R + 0.006), (-2.05, 0)], _kirmizi("serit_kir", is_=(-3.0, -1.9)), parent=k1, seg=64); kabuk(s1, hk)
    taban = torna("itki_halkasi", [(-2.70, 0), (-2.70, R - 0.02), (-2.62, R - 0.01), (-2.58, R - 0.01), (-2.58, 0)], KMET, parent=k1, seg=64); kabuk(taban, hk)
    nz = torna("nozul", [(-2.6, 0), (-2.6, 0.2), (-2.72, 0.21), (-2.82, 0.19), (-2.98, 0.24), (-3.15, 0.31), (-3.24, 0.33), (-3.25, 0.30), (-3.12, 0.26), (-2.95, 0.15), (-2.85, 0.0)],
                detayli("nozul_isi", "#9aa0aa", rough=0.33, metal=0.7, coat=0.2, kir=0.3, renk_dugum=_isi_renk, kenar=0.2), parent=k1, seg=48)
    kabuk(yumusat(nz, 1), hk)
    for i in range(10):   # nozul soğutma halkaları
        x = -2.98 - i * 0.025
    for j, xr in enumerate((-2.9, -3.05)):
        r_ = 0.21 + (abs(xr) - 2.85) * 0.5
        kabuk(simit(f"nozul_halka_{j}", r_ + 0.005, 0.012, KMET, loc=(xr, 0, 0), rot=(0, math.pi / 2, 0), parent=k1), hk)
    fin = [(-1.55, 0), (-2.0, 0.42), (-2.38, 0.62), (-2.72, 0.64), (-2.66, 0.30), (-2.5, 0)]
    for i, phi in enumerate((0, 120, 240)):
        f = plaka(f"kanat_1{'abc'[i]}", [(x, z + R - 0.05) for x, z in fin], 0.07, KIR, parent=k1, pah=0.02, seg=2)
        f.rotation_euler = (math.radians(phi), 0, 0); yumusat(f, 1); kabuk(f, hk)
        # metal hücum kenarı
        le = boru(f"kanat_1{'abc'[i]}_kenar", [(-1.55, 0, R - 0.05), (-2.0, 0, R + 0.37), (-2.38, 0, R + 0.57)], 0.022, MET, parent=k1)
        le.rotation_euler = (math.radians(phi), 0, 0); kabuk(le, hk * 0.6)
    # kablo kanalı (yan, hafif kameraya dönük üstte)
    ph = math.radians(-60)
    cy_, cz_ = (R + 0.025) * -math.sin(math.radians(60)), (R + 0.025) * math.cos(math.radians(60))
    kc = boru("kablo_kanali", [(-2.35, cy_, cz_), (-0.6, cy_, cz_)], 0.03, KMET, parent=k1, seg=8); kabuk(kc, hk)
    kc2 = boru("kablo_kanali_2", [(-0.3, cy_, cz_), (0.95, cy_, cz_)], 0.026, KMET, parent=k2, seg=8); kabuk(kc2, hk)
    # --- ara halka (dama)
    ah = torna("ara_halka", [(-0.50, 0), (-0.50, R - 0.005), (-0.30, R - 0.005), (-0.30, 0)],
               detayli("ara_dama", "#ffffff", rough=0.4, coat=0.3, kir=0.4, asinma=0.4, renk_dugum=_dama_renk), parent=k2, seg=64); kabuk(ah, hk)
    # --- üst kademe
    pr2 = [(-0.32, 0)] + yay(-0.27, R - 0.05, 0.05, 180, 90) + [(1.12, R - 0.005)] + [(1.13, 0)]
    g2 = torna("govde_2", pr2, BEY2, parent=k2, seg=64)
    ICK = plastik("kabin_ic", "#141b33", rough=0.6, sss=0, kenar=0)
    px_ = 0.45
    kes = silindir("pencere_oyuk", 0.215, 1.0, ICK, loc=(px_, -0.5, 0.0), rot=(math.pi / 2, 0, 0), seg=40)
    kes.hide_render = True; kes["gizli"] = True; kes.parent = k2
    g2.data.materials.append(ICK)
    b = g2.modifiers.new("oyuk", "BOOLEAN"); b.operation = "DIFFERENCE"; b.object = kes; b.solver = "EXACT"; b.material_mode = "TRANSFER"
    kabuk(g2, hk)
    s2 = torna("serit_2", [(-0.27, 0), (-0.27, R + 0.006), (-0.12, R + 0.006), (-0.12, 0)], KIR, parent=k2, seg=64); kabuk(s2, hk)
    # burun (ogive) + metal uç
    nose = [(1.10, 0), (1.10, R + 0.012), (1.18, R + 0.012)]
    L_ = 1.75
    for i in range(1, 23):
        t = i / 23; x = 1.18 + L_ * t; r = R * (1 - t ** 1.7) ** 0.6
        nose.append((x, r))
    nose.append((1.18 + L_ * 0.985, 0))
    bu = torna("burun", nose, KIRP, parent=k2, seg=64); kabuk(yumusat(bu, 1), hk)
    uc = torna("burun_uc", [(2.72, 0), (2.72, 0.07), (2.86, 0.045), (2.95, 0.0)], MET, parent=k2); kabuk(yumusat(uc, 1), hk)
    # RCS iticileri (burun dibinde, kameraya bakan yüzde)
    for j, (ang, x) in enumerate(((-90, 1.3), (-90 + 120, 1.3))):
        a = math.radians(ang); y_, z_ = (R - 0.02) * math.cos(a), (R - 0.02) * math.sin(a)
        rc = plaka(f"rcs_{j}", [(-0.08, -0.06), (0.08, -0.06), (0.08, 0.06), (-0.08, 0.06)], 0.06, KMET, duzlem="XY", parent=k2, pah=0.015)
        rc.location = (x, y_, z_); rc.rotation_euler = (a - math.pi / 2 + math.pi, 0, 0); kabuk(rc, hk)
    fin2 = [(0.15, 0), (-0.1, 0.22), (-0.28, 0.27), (-0.33, 0.12), (-0.32, 0)]
    for i, phi in enumerate((0, 120, 240)):
        f = plaka(f"kanat_2{'abc'[i]}", [(x, z + R - 0.04) for x, z in fin2], 0.05, KIR, parent=k2, pah=0.015)
        f.rotation_euler = (math.radians(phi), 0, 0); yumusat(f, 1); kabuk(f, hk)
    # pencere: cıvatalı metal çerçeve + cam + pilot
    pen = bos("pencere", parent=k2)
    cer = simit("pencere_cerceve", 0.235, 0.045, MET, loc=(px_, -R + 0.03, 0.0), rot=(math.pi / 2, 0, 0), parent=pen); kabuk(yumusat(cer, 1), hk)
    for i in range(10):
        a = 2 * math.pi * i / 10
        kure(f"civata_{i}", 0.018, KMET, loc=(px_ + 0.235 * math.cos(a), -R - 0.012, 0.235 * math.sin(a)), parent=pen, seg=8, halka=6)
    kure("kabin_arka", 0.24, ICK, loc=(px_, -0.02, 0.0), parent=pen)
    pk = pilot(govde=False, anten=False, ifadeler={pilot_ifade: PILOT_IFADE[pilot_ifade]}, olcek=0.2, ad="pilot_kabin")
    pk.parent = pen; pk.location = (px_, -0.17, -0.03); pk.rotation_euler = (0, 0, math.radians(10))
    camo = kure("pencere_cam", 0.215, cam_mat(), loc=(px_, -R + 0.01, 0.0), olcek=(1, 0.3, 1), parent=pen)
    camo.visible_shadow = False
    par = kure("cam_parilti", 0.055, isikli("parilti_beyaz", "#ffffff", 1.0, alfa=0.7), loc=(px_ - 0.08, -R - 0.06, 0.1), olcek=(1.0, 0.3, 0.4), parent=pen)
    par.rotation_euler = (0, math.radians(35), 0); par.visible_shadow = False
    return kok

def vizor_mat():
    return detayli("vizor_altin", "#f0b43c", rough=0.15, metal=0.55, coat=0.8, kir=0.1, kenar=0.8, cizik=0.3)

def cam_mat():
    m, nt, N, L = O._yeni("cam")
    out = N.new("ShaderNodeOutputMaterial"); tr = N.new("ShaderNodeBsdfTransparent"); tr.inputs[0].default_value = lin("#bfe6ff")
    gl = N.new("ShaderNodeBsdfGlossy"); gl.inputs["Roughness"].default_value = 0.04
    lw = N.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.25
    mr = N.new("ShaderNodeMapRange"); mr.inputs["To Min"].default_value = 0.1; mr.inputs["To Max"].default_value = 0.85
    L.new(lw.outputs["Fresnel"], mr.inputs["Value"])
    mx = N.new("ShaderNodeMixShader"); L.new(mr.outputs["Result"], mx.inputs[0]); L.new(tr.outputs[0], mx.inputs[1]); L.new(gl.outputs[0], mx.inputs[2])
    L.new(mx.outputs[0], out.inputs[0])
    return m

# ================================================================= PİLOT (genç yetişkin astronot)
PILOT_IFADE = {
    "notr":    dict(goz="acik", bebek=1.0, bakis=(0.35, 0.0), kas=(0.55, -0.15, 0.12), agiz="smirk"),
    "heyecan": dict(goz="acik", goz_olcek=1.25, bebek=0.95, bakis=(0.3, 0.2), kas=(0.95, -0.2, 0.2), agiz="acik_gulus"),
    "saskin":  dict(goz="genis", goz_olcek=1.65, goz_gen=1.05, bebek=0.62, bakis=(0, 0), kas=(1.25, 0.0, 0.25), agiz="O"),
    "korku":   dict(goz="genis", goz_olcek=1.5, bebek=0.5, bakis=(-0.3, -0.3), kas=(0.75, 1.4, -0.05), agiz="korku", ter=True),
    "zafer":   dict(goz="mutlu", kas=(0.75, -0.35, 0.18), agiz="zafer"),
}

def kafa_r(z):
    """Yumurta kafa profili (çene daralır)."""
    if z >= 0: return 0.56 * math.sqrt(max(0.0, 1 - (z / 0.66) ** 2))
    t = -z / 0.78
    return 0.56 * math.sqrt(max(0.0, 1 - t * t)) * (1 - 0.16 * t)

def pilot(govde=True, anten=True, ifadeler=None, olcek=1.0, ad="pilot"):
    ifadeler = ifadeler or PILOT_IFADE
    kok = bos(ad); kok.scale = (olcek,) * 3
    hk = 0.016
    import bmesh
    from mathutils import Matrix
    KASK = detayli("kask_boya", "#f2efe8", rough=0.3, coat=0.6, panel=dict(eksen="Z", adim=0.7, n=6, R=1.0, x0=0.5), kir=0.35, cizik=0.35, asinma=0.3)
    MET = _metal("metal"); KMET = _metal("koyu_metal", P["koyu_gri"], 0.4)
    TEN = plastik("ten", P["ten"], rough=0.5, sss=0.4, coat=0.05, kenar=0.25)
    SAC = detayli("sac", P["sac"], rough=0.45, coat=0.2, kumas=0.06, kir=0.2, kenar=0.3)
    def kapak_kure(adk, r, tut, mat):
        bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=56, v_segments=28, radius=r)
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / 2, 3, "X"))
        sil = [f for f in bm.faces if not tut(f.calc_center_median())]
        bmesh.ops.delete(bm, geom=sil, context="FACES")
        me = O.bpy.data.meshes.new(adk); bm.to_mesh(me); bm.free()
        o = O.bpy.data.objects.new(adk, me); O.bpy.context.scene.collection.objects.link(o)
        me.materials.append(mat); o.parent = kok
        for p in me.polygons: p.use_smooth = True
        return o
    ac = math.radians(50)
    kask = kapak_kure("kask", 1.0, lambda c: c.y > -math.cos(ac) * 1.0, KASK)
    so = kask.modifiers.new("kalinlik", "SOLIDIFY"); so.thickness = 0.07; so.offset = -1
    yumusat(kask, 1); kabuk(kask, hk)
    hal = simit("kask_halka", math.sin(ac) * 0.99, 0.06, KMET, loc=(0, -math.cos(ac) * 0.98, 0), rot=(math.pi / 2, 0, 0), parent=kok)
    kabuk(yumusat(hal, 1), hk)
    for i in range(12):
        a = 2 * math.pi * (i + 0.5) / 12; rr = math.sin(ac) * 0.99
        kure(f"kask_civata_{i}", 0.028, MET, loc=(rr * math.cos(a), -math.cos(ac) * 0.98 - 0.055, rr * math.sin(a)), parent=kok, seg=10, halka=6)
    # kalkık altın vizör (kaska yapışık)
    viz = kapak_kure("vizor", 1.03, lambda c: c.y < -math.cos(math.radians(36)) * 1.03, vizor_mat())
    so = viz.modifiers.new("kalinlik", "SOLIDIFY"); so.thickness = 0.03; so.offset = -1
    viz.rotation_euler = (math.radians(-80), 0, 0); yumusat(viz, 1); kabuk(viz, hk)
    # vizör menteşe kolları + yan lambalar
    for sd in (-1, 1):
        kl = silindir(f"kulak_{'l' if sd < 0 else 'r'}", 0.2, 0.12, KMET, loc=(sd * 0.99, 0.0, 0.05), rot=(0, math.pi / 2, 0), parent=kok, seg=32, pah=0.03)
        yumusat(kl, 1); kabuk(kl, hk)
        lam = silindir(f"lamba_{'l' if sd < 0 else 'r'}", 0.075, 0.14, MET, loc=(sd * 0.74, -0.58, 0.46), rot=(math.pi / 2, 0, 0), parent=kok, seg=20, pah=0.015)
        kabuk(lam, hk)
        kure(f"lamba_cam_{'l' if sd < 0 else 'r'}", 0.06, isikli("lamba_isik", "#fff3c4", 2.0), loc=(sd * 0.74, -0.66, 0.46), olcek=(1, 0.4, 1), parent=kok, seg=16, halka=8)
    if anten:
        a = silindir("anten", 0.018, 0.55, MET, loc=(-0.55, 0.25, 0.98), rot=(0, math.radians(-28), 0), parent=kok); kabuk(a, hk)
        kabuk(kure("anten_uc", 0.04, isikli("anten_led", "#ff4a3a", 2.0), loc=(-0.68, 0.25, 1.23), parent=kok), hk)
    # kafa (yumurta) + burun + saç
    hc = (0, -0.08, -0.06)
    prf = [(-0.78, 0)] + [(z, kafa_r(z)) for z in [-0.78 + 1.44 * i / 40 for i in range(1, 40)]] + [(0.66, 0)]
    kafa = torna("kafa", prf, TEN, eksen="Z", parent=kok, seg=48); kafa.location = hc
    yz = Yuzey(kafa_r, "Z", merkez=hc)
    burun_p = yz.nokta(0.0, -0.12, 0.0)
    kabuk(kure("burun_pilot", 0.075, TEN, loc=tuple(burun_p), olcek=(0.85, 0.9, 1.15), parent=kok, seg=20, halka=10), hk * 0.7)
    sac = metatop("sac", [(-0.4, -0.3, 0.42, 0.2), (-0.2, -0.4, 0.5, 0.22), (0.05, -0.42, 0.52, 0.22), (0.28, -0.36, 0.5, 0.2),
                          (0.45, -0.22, 0.42, 0.17), (0.0, -0.1, 0.6, 0.32), (-0.45, -0.05, 0.35, 0.22), (0.5, 0.0, 0.3, 0.2),
                          (0.18, -0.48, 0.45, 0.13)], SAC, parent=kok, coz=0.03)
    sac.location = hc; kabuk(sac, hk)
    F = dict(ex=0.215, ey=0.02, rx=0.115, ry=0.07, lw=0.03, mx=0.0, my=-0.29, mw=0.34, terx=0.40, tery=0.22, terr=0.05)
    yuz_kur("pilot", yz, kok, F, ifadeler, kas_renk="#2e1a10", birim=0.004)
    if govde:
        TUL = detayli("giysi", "#e9e6df", rough=0.75, coat=0.0, panel=dict(eksen="Z", adim=0.55, n=4, R=0.9, x0=0.3), kumas=0.05, kir=0.4, kenar=0.3)
        tor = torna("govde", [(-0.8, 0), (-0.8, 0.42), (-0.9, 0.7), (-1.05, 0.95), (-1.3, 1.0), (-1.7, 0.95), (-2.1, 0.86), (-2.2, 0)], TUL, eksen="Z", parent=kok, seg=48)
        tor.scale = (1.3, 0.78, 1.0); yumusat(tor, 1); kabuk(tor, hk)
        yaka = simit("boyun_halkasi", 0.62, 0.09, KMET, loc=(0, 0, -0.86), parent=kok); yaka.scale = (1.1, 0.95, 1); kabuk(yumusat(yaka, 1), hk)
        for i in range(10):
            a = 2 * math.pi * i / 10
            kure(f"yaka_civata_{i}", 0.026, MET, loc=(0.62 * 1.1 * math.cos(a), 0.62 * 0.95 * math.sin(a) - 0.06, -0.80), parent=kok, seg=8, halka=6)
        # göğüs kontrol ünitesi + düğmeler + hortum
        ku = plaka("kontrol_unitesi", [(-0.36, -1.18), (0.36, -1.18), (0.36, -1.6), (-0.36, -1.6)], 0.14, detayli("unite", "#596274", rough=0.4, metal=0.6, kir=0.5, cizik=0.5), parent=kok, pah=0.03)
        ku.location = (0, -0.70, 0); kabuk(ku, hk)
        for j, (renk, x) in enumerate((("#ff3b30", -0.2), ("#ffcc33", -0.05), ("#3be27a", 0.1))):
            silindir(f"dugme_{j}", 0.045, 0.05, isikli(f"dugme_{renk}", renk, 1.6), loc=(x, -0.79, -1.3), rot=(math.pi / 2, 0, 0), parent=kok, seg=16)
        kabuk(plaka("ekran", [(0.17, -1.42), (0.31, -1.42), (0.31, -1.24), (0.17, -1.24)], 0.03, isikli("ekran", "#7fe7ff", 1.2), parent=kok, pah=0.005), hk).location = (0, -0.79, 0)
        hp = [(0.36, -0.72, -1.45), (0.62, -0.62, -1.55), (0.85, -0.45, -1.4), (0.98, -0.35, -1.15)]
        kabuk(boru("hortum", hp, 0.055, detayli("hortum", "#c9ced8", rough=0.5, kumas=0.08, kir=0.3)), hk).parent = kok
        # omuz arması (bayrak yerine yıldızlı mavi yama; yazı yok)
        ar = silindir("arma", 0.17, 0.03, detayli("arma", P["lacivert"], rough=0.6, kumas=0.04, kenar=0.3), loc=(-0.98, -0.5, -1.25), rot=(math.radians(80), 0, math.radians(-50)), parent=kok, seg=32)
        kabuk(ar, hk)
        y_ = plaka("arma_yildiz", __import__("modeller").yildiz_sekil(0.1, 0.045, 5), 0.02, isikli("arma_yildiz", P["sari"], 1.0), parent=kok, pah=0)
        y_.location = (-1.01, -0.53, -1.25); y_.rotation_euler = (math.radians(-10), 0, math.radians(-50))
    return kok

# ================================================================= nesne yüzleri (olgun, abartılı)
NESNE_IFADE = {
    "normal": dict(goz="yari", kapak=0.7, bebek=1.05, bakis=(0.45, 0.0), kas=(0.55, -0.45, 0.05), agiz="smirk"),
    "ezik":   dict(goz="sikik", kas=(0.2, 1.2, -0.1), agiz="ezik_acik"),
    "saskin": dict(goz="genis", goz_olcek=1.75, bebek=0.6, bakis=(0, 0.1), kas=(1.3, 0.0, 0.2), agiz="O"),
}

def zarf_renk(nt, N, L):
    sp = _xyz(N, L); z = sp.outputs["Z"]; x = sp.outputs["X"]
    bant = _m(N, L, "MULTIPLY", _m(N, L, "GREATER_THAN", z, -0.47), _m(N, L, "LESS_THAN", z, -0.22))
    cizgi = _m(N, L, "MAXIMUM", _m(N, L, "MULTIPLY", _m(N, L, "GREATER_THAN", z, -0.20), _m(N, L, "LESS_THAN", z, -0.17)),
               _m(N, L, "MULTIPLY", _m(N, L, "GREATER_THAN", z, -0.52), _m(N, L, "LESS_THAN", z, -0.49)))
    burun = _smooth(N, L, x, 1.62, 1.66)
    c = _mix(N, L, bant, lin(P["mor"]), lin(P["kirmizi"]))
    c = _mix(N, L, cizgi, c, lin(P["altin"]))
    return _mix(N, L, burun, c, lin(P["krem"]))

def zeplin_r(x):
    if x >= 0: return 1.0 * max(0.0, 1 - (x / 2.0) ** 2) ** 0.5
    return 1.0 * max(0.0, 1 - (x / 2.35) ** 2) ** 0.62

def zeplin(ifadeler=None):
    ifadeler = ifadeler or NESNE_IFADE
    kok = bos("zeplin"); govde = bos("zeplin_govde", parent=kok)
    hk = 0.016
    pr = [(2.0, 0)]
    for i in range(1, 72):
        t = i / 72; x = 2.0 - t * 4.35; pr.append((x, zeplin_r(x)))
    pr.append((-2.35, 0))
    ZARF = detayli("zarf", P["mor"], rough=0.42, coat=0.3, sss=0.1, panel=dict(eksen="X", adim=40.0, n=16, R=0.95, x0=0.5),
                   kir=0.15, kumas=0.03, renk_dugum=zarf_renk, kenar=0.4)
    zarf = torna("zarf", pr, ZARF, parent=govde, seg=72)
    zarf.shape_key_add(name="Basis", from_mix=False); kb = zarf.shape_key_add(name="cokme", from_mix=False)
    for j, v in enumerate(zarf.data.vertices):
        x, y, z = v.co; w = math.exp(-((x + 0.1) / 0.75) ** 2) * max(0.0, z) ** 1.5
        kb.data[j].co = (x, y * (1 + 0.08 * w), z - 0.38 * w)
    yumusat(zarf, 1); kabuk(zarf, hk)
    MET = _metal("metal"); KMET = _metal("koyu_metal", P["koyu_gri"], 0.4)
    # burun çıtaları (8)
    for i in range(10):
        f = 2 * math.pi * i / 10; pts = []
        for j in range(12):
            x = 1.98 - j * 0.06; r = zeplin_r(x) + 0.012
            pts.append((x, r * math.cos(f), r * math.sin(f)))
        kabuk(boru(f"burun_cita_{i}", pts, 0.022, KMET, parent=govde, seg=8), hk)
    kabuk(torna("burun_kapak", [(2.03, 0), (2.03, 0.05), (1.96, 0.13), (1.93, 0)], MET, parent=govde), hk)
    KIR = _kirmizi("zeplin_kanat", panel=None, asinma=0.5)
    fin = [(-1.25, 0.35), (-1.85, 1.02), (-2.38, 1.06), (-2.28, 0.25)]
    for i, phi in enumerate((0, 90, 180, 270)):
        f = plaka(f"kanat_{i}", fin, 0.09, KIR, parent=govde, pah=0.03); f.rotation_euler = (math.radians(phi), 0, 0)
        yumusat(f, 1); kabuk(f, hk)
        # dümen yüzeyi (ayrı parça, menteşe çizgisi)
        d = plaka(f"dumen_{i}", [(-2.3, 0.3), (-2.38, 1.0), (-2.6, 0.98), (-2.55, 0.28)], 0.07, _metal("dumen", "#c9cdd6", 0.35), parent=govde, pah=0.02)
        d.rotation_euler = (math.radians(phi), 0, 0); kabuk(d, hk)
    gon = bos("gondol", parent=govde)
    GON = detayli("gondol_boya", P["krem"], rough=0.4, coat=0.4, panel=dict(eksen="X", adim=0.3, n=4, R=0.2), percin=True, kir=0.45, asinma=0.4,
                  renk_dugum=lambda nt, N, L: _mix(N, L, _m(N, L, "MULTIPLY", _m(N, L, "GREATER_THAN", _xyz(N, L).outputs["Z"], -0.02),
                                                                      _m(N, L, "LESS_THAN", _xyz(N, L).outputs["Z"], 0.09)), lin(P["krem"]), lin("#1a2340")))
    g = torna("gondol_govde", [(-0.25, 0)] + yay(-0.12, 0.10, 0.13, 180, 90) + yay(1.0, 0.1, 0.13, 90, 0) + [(1.18, 0)], GON, parent=gon, seg=40)
    g.location = (0.0, 0, -1.02); g.scale = (1, 0.85, 1); yumusat(g, 1); kabuk(g, hk)
    for sx in (0.05, 0.9):
        kabuk(silindir(f"gondol_dikme_{sx}", 0.025, 0.3, KMET, loc=(sx, 0, -0.82), parent=gon), hk)
    # motor kapsülleri + pervaneler
    for sd, yy in (("on", -0.42), ("arka", 0.42)):
        mt = torna(f"motor_{sd}", [(0.05, 0), (0.05, 0.07), (0.15, 0.11), (0.45, 0.10), (0.55, 0.05), (0.6, 0)], GON, parent=gon, seg=24)
        mt.location = (0.25, yy, -1.0); kabuk(yumusat(mt, 1), hk)
        kabuk(boru(f"motor_kol_{sd}", [(0.45, yy * 0.25, -1.0), (0.45, yy, -1.0)], 0.02, KMET, parent=gon), hk)
        pv = kure(f"pervane_{sd}", 0.26, isikli("pervane_iz", "#e6e9f0", 1.0, alfa=0.18), loc=(0.02, yy, -1.0), olcek=(0.02, 1, 1), parent=gon, seg=24, halka=12)
        pv.visible_shadow = False
    # kuyruk pervanesi
    per = bos("pervane", parent=govde, loc=(-2.42, 0, 0))
    kabuk(kure("pervane_gobek", 0.09, MET, parent=per), hk)
    for i, a in enumerate((20, 140, 260)):
        b = plaka(f"pervane_kanat_{i}", [(0, 0.0), (0.05, 0.08), (0.03, 0.42), (-0.03, 0.42), (-0.05, 0.08)], 0.03, KMET, parent=per, pah=0.01)
        b.rotation_euler = (math.radians(a), 0, 0); kabuk(b, hk)
    yz = Yuzey(zeplin_r, "X")
    F = dict(cx=1.08, ex=0.3, ey=0.16, rx=0.18, ry=0.13, lw=0.036, mx=1.12, my=-0.25, mw=0.42)
    yuz_kur("zeplin", yz, govde, F, ifadeler, birim=0.005, kas_renk="#1d1430", iris_renk="#e0a530")
    kok.rotation_euler = (0, 0, math.radians(-16))
    return kok

# ================================================================= REKLAM BALONU (sıcak hava balonu)
def balon_r(z):
    if z >= -0.6: return math.sqrt(max(0.0, 1 - z * z))
    t = (-0.6 - z) / 0.68; t = min(1, max(0, t))
    h00 = 2 * t ** 3 - 3 * t ** 2 + 1; h10 = t ** 3 - 2 * t ** 2 + t; h01 = -2 * t ** 3 + 3 * t ** 2
    return h00 * 0.8 + h10 * (-0.51) + h01 * 0.17

NG = 12  # dilim sayısı
def balon_renk(nt, N, L):
    sp = _xyz(N, L)
    ac = _m(N, L, "ADD", _m(N, L, "ARCTAN2", sp.outputs["Y"], sp.outputs["X"]), math.pi / 2 + math.pi / NG)
    idx = _m(N, L, "FLOOR", _m(N, L, "MULTIPLY", _m(N, L, "FRACT", _m(N, L, "DIVIDE", ac, 2 * math.pi)), NG))
    cift = _m(N, L, "MODULO", idx, 2)
    c = _mix(N, L, cift, lin(P["kirmizi"]), lin(P["krem"]))
    z = sp.outputs["Z"]
    etek = _smooth(N, L, z, -0.62, -0.66)
    c = _mix(N, L, etek, c, lin(P["teal"]))
    tac = _m(N, L, "MULTIPLY", _m(N, L, "GREATER_THAN", z, 0.80), 1.0)
    c = _mix(N, L, tac, c, lin(P["teal"]))
    ince = _m(N, L, "MAXIMUM", _m(N, L, "MULTIPLY", _m(N, L, "GREATER_THAN", z, 0.74), _m(N, L, "LESS_THAN", z, 0.79)),
              _m(N, L, "MULTIPLY", _m(N, L, "GREATER_THAN", z, -0.62), _m(N, L, "LESS_THAN", z, -0.57)))
    return _mix(N, L, ince, c, lin(P["sari"]))

def _hasir(nt, N, L):
    sp = _xyz(N, L)
    a = _m(N, L, "SINE", _m(N, L, "MULTIPLY", _m(N, L, "ARCTAN2", sp.outputs["Y"], sp.outputs["X"]), 28))
    b = _m(N, L, "SINE", _m(N, L, "MULTIPLY", sp.outputs["Z"], 70))
    f = _smooth(N, L, _m(N, L, "MULTIPLY", a, b), -0.2, 0.4)
    return _mix(N, L, f, lin("#8a5426"), lin("#d39a55"))

def balon(ifadeler=None):
    ifadeler = ifadeler or NESNE_IFADE
    kok = bos("balon"); govde = bos("balon_govde", parent=kok)
    hk = 0.014
    pr = [(-1.28, 0)]
    for i in range(0, 72):
        z = -1.28 + 2.28 * i / 71; pr.append((z, balon_r(z)))
    pr[-1] = (1.0, 0)
    ZARF = detayli("balon_zarf", "#ffffff", rough=0.45, coat=0.25, sss=0.12, kumas=0.025, kir=0.3, renk_dugum=balon_renk, kenar=0.4)
    zarf = torna("balon_zarf", pr, ZARF, eksen="Z", parent=govde, seg=96)
    # dilim şişkinliği: yük şeritleri arasında kumaş kabarır
    for v in zarf.data.vertices:
        f = math.atan2(v.co.y, v.co.x) + math.pi / 2
        s = 0.975 + 0.025 * abs(math.cos(NG * f / 2)) ** 0.5
        v.co.x *= s; v.co.y *= s
    zarf.shape_key_add(name="Basis", from_mix=False); kb = zarf.shape_key_add(name="cokme", from_mix=False)
    for j, v in enumerate(zarf.data.vertices):
        x, y, z = v.co; w = max(0.0, z) ** 2.2 * math.exp(-(x * x) / 0.5)
        kb.data[j].co = (x * (1 + 0.06 * w), y * (1 + 0.06 * w), z - 0.4 * w)
    yumusat(zarf, 1); kabuk(zarf, hk)
    IP = detayli("ip", "#5b3b22", rough=0.7, kumas=0.1, kir=0.2, kenar=0.2)
    # yük şeritleri (dikişlerde)
    for i in range(NG):
        f = 2 * math.pi * i / NG - math.pi / 2 + math.pi / NG * 0 + math.pi / NG
        pts = [(balon_r(z) * 0.985 * math.cos(f), balon_r(z) * 0.985 * math.sin(f), z) for z in [-1.24 + 2.2 * j / 40 for j in range(41)]]
        kabuk(boru(f"yuk_serit_{i}", pts, 0.012, IP, parent=govde, seg=6), hk * 0.5)
    MET = _metal("metal"); KMET = _metal("koyu_metal", P["koyu_gri"], 0.4)
    kabuk(torna("balon_boyun", [(-1.36, 0), (-1.36, 0.16), (-1.26, 0.2), (-1.22, 0)], KMET, eksen="Z", parent=govde), hk)
    # brülör + çerçeve
    br = bos("brulor", parent=kok)
    kabuk(yumusat(torna("brulor_govde", [(-1.58, 0), (-1.58, 0.1), (-1.48, 0.12), (-1.40, 0.08), (-1.40, 0)], MET, eksen="Z", parent=br), 1), hk)
    sep = bos("sepet", parent=kok)
    s = torna("sepet_govde", [(-2.05, 0), (-2.05, 0.25), (-2.02, 0.28), (-1.76, 0.30), (-1.74, 0.0)],
              detayli("hasir", "#b47a3c", rough=0.7, coat=0, kir=0.5, renk_dugum=_hasir, kenar=0.2), eksen="Z", parent=sep, seg=48)
    yumusat(s, 1); kabuk(s, hk)
    kabuk(simit("sepet_kenar", 0.30, 0.045, detayli("deri", "#4a2c1a", rough=0.5, kir=0.3, cizik=0.3), loc=(0, 0, -1.74), parent=sep), hk)
    for i in range(4):
        a = math.radians(45 + 90 * i); x, y = 0.28 * math.cos(a), 0.28 * math.sin(a)
        x2, y2 = 0.14 * math.cos(a), 0.14 * math.sin(a)
        kabuk(boru(f"ip_{i}", [(x, y, -1.72), (x2, y2, -1.36)], 0.014, KMET, parent=sep, seg=6), hk * 0.5)
    tab = bos("tabela", parent=kok)
    t = plaka("tabela_levha", [(-0.75, -2.36), (0.75, -2.36), (0.75, -2.82), (-0.75, -2.82)], 0.06, detayli("tabela", "#f7f1e3", rough=0.5, kir=0.35, asinma=0.2), parent=tab, pah=0.02)
    kabuk(t, hk)
    cerc = plaka("tabela_cerceve", [(-0.81, -2.30), (0.81, -2.30), (0.81, -2.88), (-0.81, -2.88)], 0.05, _metal("tabela_cerceve", "#c2c7d0", 0.3), parent=tab, pah=0.015)
    cerc.location = (0, 0.035, 0); kabuk(cerc, hk)
    for sx in (-0.5, 0.5):
        kabuk(boru(f"tabela_zincir_{sx}", [(sx * 0.4, 0, -1.98), (sx * 1.1, 0, -2.30)], 0.012, KMET, parent=tab, seg=6), hk * 0.5)
    yz = Yuzey(balon_r, "Z")
    F = dict(cx=0.0, ex=0.29, ey=0.16, rx=0.17, ry=0.12, lw=0.034, mx=0.0, my=-0.22, mw=0.4)
    yuz_kur("balon", yz, govde, F, ifadeler, birim=0.012, kas_renk="#1d1430", iris_renk="#2f8f86")
    kok.rotation_euler = (0, 0, math.radians(10))
    return kok


def _math(N, L, op, a, b=None): return _m(N, L, op, a, b)

# ================================================================= BULUT
def bulut(cesit, seed=1):
    random.seed(seed)
    kok = bos(f"bulut_{cesit}")
    if cesit == 0:   # küçük kabarık
        toplar = [(-0.9, 0, -0.1, 0.55), (-0.3, 0, 0.25, 0.75), (0.45, 0, 0.15, 0.68), (1.0, 0, -0.1, 0.5), (0.0, 0, -0.25, 0.6)]
    elif cesit == 1:  # orta: iki tepeli
        toplar = [(-1.6, 0, -0.2, 0.55), (-1.0, 0, 0.2, 0.75), (-0.2, 0, 0.55, 0.95), (0.7, 0, 0.35, 0.85), (1.45, 0, -0.05, 0.62),
                  (2.0, 0, -0.25, 0.45), (0.0, 0, -0.3, 0.7), (-0.9, 0, -0.3, 0.6), (1.0, 0, -0.3, 0.6)]
    else:             # geniş bulut kümesi (kule)
        toplar = [(-2.6, 0, -0.4, 0.55), (-2.0, 0, -0.05, 0.75), (-1.2, 0, 0.45, 0.95), (-0.3, 0, 1.05, 1.1), (0.5, 0, 1.4, 0.85),
                  (1.1, 0, 0.75, 1.0), (1.9, 0, 0.2, 0.8), (2.6, 0, -0.3, 0.55), (-0.5, 0, 0.0, 1.0), (0.9, 0, -0.2, 0.9), (-1.6, 0, -0.4, 0.7)]
    toplar = [(x, y + random.uniform(-0.25, 0.25), z, r) for x, y, z, r in toplar]
    # tabanı düzleştirmek için alttaki topları yassılt: alt kesim aşağıda yapılır
    BUL = plastik("bulut", "#fbfdff", rough=0.75, coat=0.0, sss=0.45, kenar=0.9)
    o = metatop(f"bulut_{cesit}_g", toplar, BUL, parent=kok, coz=0.06)
    # tabanı yassılt
    zmin = min(v.co.z for v in o.data.vertices); kes = zmin + 0.35
    for v in o.data.vertices:
        if v.co.z < kes: v.co.z = kes - (kes - v.co.z) * 0.35
    o.scale = (1, 0.7, 1)
    return kok

# ================================================================= ALEV
def alev(kare):
    random.seed(100 + kare)
    kok = bos(f"alev_{kare}")
    katman = [("dis", "#ff3d1f", 1.0, 0.0), ("orta", "#ff9a1a", 0.74, -0.18), ("cekirdek", "#fff2a8", 0.46, -0.34)]
    uz = [1.0, 1.12, 0.92, 1.06][kare]
    for i, (ad, renk, s, yoff) in enumerate(katman):
        pr = [(0.05, 0)]
        for j in range(1, 30):
            t = j / 29; x = -t * 1.7 * uz * (0.85 + 0.15 * s)
            r = s * 0.42 * (math.sin(math.pi * min(1, t * 1.0 + 0.08)) ** 0.7) * (1 - t) ** 0.25 if t < 0.999 else 0
            r = (0.32 * s) * (1 - t) ** 0.9 + 0.12 * s * math.sin(math.pi * t) if t < 1 else 0
            pr.append((x, r))
        pr[-1] = (pr[-1][0], 0)
        m = isikli("alev_" + ad, renk, 1.0)
        o = torna(f"alev_{kare}_{ad}", pr, m, parent=kok, seg=32)
        o.scale = (1, 0.28, 1); o.location = (0, yoff, 0)
        d = o.modifiers.new("titre", "DISPLACE")
        tx = O.bpy.data.textures.new(f"alev_tx_{kare}_{i}", "CLOUDS"); tx.noise_scale = 0.35; tx.noise_depth = 1
        d.texture = tx; d.strength = 0.16 * s; d.texture_coords = "GLOBAL"
        hedef = bos(f"alev_tx_ob_{kare}_{i}", loc=(kare * 1.7 + i * 0.4, 0, kare * 0.9))
        d.texture_coords = "OBJECT"; d.texture_coords_object = hedef
        yumusat(o, 1)
    return kok

# ================================================================= EFEKTLER
def yildiz_sekil(r1, r2, n=5, don=0.0):
    pts = []
    for i in range(2 * n):
        a = math.pi / 2 + don + math.pi * i / n
        r = r1 if i % 2 == 0 else r2
        pts.append((r * math.cos(a), r * math.sin(a)))
    return pts

def patlama(kare):
    """Yıldız patlaması (çarpışma): 3 kare."""
    random.seed(7)
    kok = bos(f"patlama_{kare}")
    olc = [0.85, 1.25, 0.7][kare]; ic_al = [1.0, 0.75, 0.35][kare]
    # sivri flaş: dış turuncu + iç sarı-beyaz
    def flas(r_d, r_i, n, renk, ad, y):
        pts = []
        for i in range(2 * n):
            a = math.pi * i / n + 0.15
            r = (r_d * (0.75 + 0.25 * ((i * 37) % 5) / 4)) if i % 2 == 0 else r_i
            pts.append((r * math.cos(a), r * math.sin(a)))
        o = plaka(ad, pts, 0.04, isikli("flas_" + renk, renk, 1.0), parent=kok, pah=0.0)
        o.location = (0, y, 0); return o
    flas(1.6 * olc, 0.75 * olc * ic_al, 11, "#ff8a1f", f"flas_dis_{kare}", 0.0)
    flas(1.15 * olc * ic_al, 0.55 * olc * ic_al, 11, "#ffe14a", f"flas_orta_{kare}", -0.08)
    flas(0.65 * olc * ic_al, 0.35 * olc * ic_al, 9, "#fffbe0", f"flas_ic_{kare}", -0.16)
    YIL = plastik("yildiz", "#ffd21f", rough=0.25, coat=0.8, kenar=0.9)
    yol = [0.95, 1.55, 2.05][kare]
    for i in range(6):
        a = math.radians(30 + 60 * i + random.uniform(-12, 12))
        rr = 0.36 * random.uniform(0.75, 1.15) * [1.0, 0.9, 0.7][kare]
        y = plaka(f"yildiz_{kare}_{i}", yildiz_sekil(rr * 1.2, rr * 0.3, 4, random.uniform(0, 1) + kare * 0.5), 0.16, YIL, duzlem="XZ", parent=kok, pah=0.05)
        y.location = (math.cos(a) * yol, -0.4, math.sin(a) * yol); y.rotation_euler = (random.uniform(-0.4, 0.4), random.uniform(-0.6, 0.6), 0)
        yumusat(y, 1); kabuk(y, 0.02)
    KIV = isikli("kivilcim", "#fff1b0", 1.0)
    for i in range(10):
        a = math.radians(i * 36 + 18 + random.uniform(-8, 8)); r0 = [0.9, 1.4, 1.9][kare]; L_ = [0.7, 0.9, 0.5][kare] * random.uniform(0.7, 1.2)
        w = 0.06 * [1.0, 0.8, 0.5][kare]
        pts = [(r0, 0), (r0 + L_ * 0.5, w), (r0 + L_, 0), (r0 + L_ * 0.5, -w)]
        rp = [(x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)) for x, y in pts]
        k = plaka(f"kivilcim_{kare}_{i}", rp, 0.02, KIV, parent=kok, pah=0); k.location = (0, -0.3, 0)
    return kok

def toz(kare):
    random.seed(11)
    kok = bos(f"toz_{kare}")
    olc = [0.6, 1.0, 1.3][kare]; kuc = [1.0, 0.85, 0.5][kare]
    top = []
    for i in range(9):
        a = math.radians(i * 40 + random.uniform(-10, 10)); r = olc * random.uniform(0.9, 1.25)
        top.append((math.cos(a) * r * 1.4, random.uniform(-0.2, 0.2), math.sin(a) * r * 0.7, 0.55 * kuc * random.uniform(0.8, 1.2)))
    if kare == 0: top.append((0, 0, 0, 0.8))
    o = metatop(f"toz_{kare}_g", top, plastik("toz", "#f4e7cf", rough=0.8, coat=0, sss=0.4, kenar=0.7), parent=kok, coz=0.05)
    return kok

def ses_duvari(kare):
    """Ses duvarı buhar konisi + parlak halka: 2 kare."""
    kok = bos(f"ses_{kare}")
    acik = [0.75, 1.0][kare]
    pr = []
    for j in range(30):
        t = j / 29; x = 0.9 - t * 1.9 * acik
        pr.append((x, 0.12 + 1.15 * acik * (t ** 0.75)))
    def koni_alfa(N, L):
        lw = N.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.5
        sp = _xyz(N, L)
        # uca doğru (x küçüldükçe) silinsin
        mr = N.new("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = -1.1 * acik; mr.inputs["From Max"].default_value = 0.6
        L.new(sp.outputs["X"], mr.inputs["Value"])
        f = _math(N, L, "MULTIPLY", _math(N, L, "POWER", lw.outputs["Facing"], 1.5), mr.outputs["Result"])
        return _math(N, L, "MINIMUM", _math(N, L, "MULTIPLY", f, 1.4), 1.0)
    k = torna(f"ses_koni_{kare}", pr, isikli("ses_koni", "#eaf8ff", 1.0, alfa=koni_alfa), parent=kok, seg=48)
    # açık uçlu kabuk: ilk ve son halka arası tek yüzey, iki yüz görünür
    hal = simit(f"ses_halka_{kare}", 0.12 + 1.15 * acik, 0.05 + 0.03 * kare, isikli("ses_halka", "#bff4ff", 1.0), loc=(0.9 - 1.9 * acik, 0, 0), rot=(0, math.pi / 2, 0), parent=kok)
    hal2 = simit(f"ses_halka2_{kare}", 0.75 * acik, 0.03, isikli("ses_halka2", "#ffffff", 1.0), loc=(0.9 - 1.9 * acik * 0.55, 0, 0), rot=(0, math.pi / 2, 0), parent=kok)
    kok.rotation_euler = (0, 0, math.radians(-25))  # hafif üç çeyrek: halka elips görünsün
    return kok
