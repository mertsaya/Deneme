# Son Durak: Plüton · B1 3B modeller (Blender 5.0.1 / bpy 5.0.1 ile denendi)
# Kopabilen parçalar adlandırılmıştır: roket/kademe_1, roket/kademe_2, burun, kanat_*, nozul, pencere; zeplin/kanat_*, gondol, pervane; balon/sepet, tabela.
import math, random
from mathutils import Vector
import ortak as O
from ortak import (plastik, isikli, kabuk, yumusat, torna, yay, plaka, kure, silindir, simit, metatop,
                   elips, nokta, bez, serit, agiz, sisir, ic_bolge, Yuzey, cikartma, bos, lin)

# ================================================================= renk paleti (sRGB)
P = dict(kirmizi="#ff2e45", kirmizi_k="#c8102e", beyaz="#f7f4ee", gri="#9aa6c2", koyu_gri="#4a5270", civit=O.CIVIT,
         mor="#7d4cf0", sari="#ffc93a", mavi="#2f8cff", ten="#ffc79e", sac="#8a4520", turuncu="#ff8a1f",
         agiz_ic="#7a1232", dil="#ff6f8e", yanak="#ff7a9a", ter="#8fdcff", cam="#7fd0ff", altin="#ffb62e")

# ================================================================= karton yüz kurucu
def _kirp(sek, ymax):
    u, a = sek
    return [(p[0], min(p[1], ymax)) for p in u], [(p[0], min(p[1], ymax)) for p in a]

def yuz_kur(ad, yuzey, kok, F, ifadeler, kas_renk=None, yanak=True, birim=0.004):
    """F: yüz ölçüleri (yerel birim). ifadeler: {ad: spec}. Her parça tüm ifadeleri şekil anahtarı olarak taşır."""
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
                ak = elips(gx, ey, rxx, ryy)
                cz = sisir(ak, lw)
                pr = min(rxx, ryy) * sp.get("bebek", 0.55)
                bx, by = sp.get("bakis", (0.1, 0.0))
                pcx = gx + bx * (rxx - pr) * 0.85; pcy = ey + by * (ryy - pr) * 0.85
                bb = elips(pcx, pcy, pr * 0.95, pr * 1.05)
                i1 = elips(pcx - pr * 0.32, pcy + pr * 0.36, pr * 0.30, pr * 0.30)
                i2 = elips(pcx + pr * 0.38, pcy - pr * 0.34, pr * 0.13, pr * 0.13)
                if tip == "yari":
                    ust = ey + ryy * sp.get("kapak", 0.25)
                    ak = _kirp(ak, ust); cz = _kirp(cz, ust + lw); bb = _kirp(bb, ust); i1 = _kirp(i1, ust); i2 = _kirp(i2, ust)
                ekle(f"goz_{k}_cizgi", ia, cz); ekle(f"goz_{k}_ak", ia, ak); ekle(f"goz_{k}_bebek", ia, bb)
                ekle(f"goz_{k}_isik1", ia, i1); ekle(f"goz_{k}_isik2", ia, i2)
            else:
                if tip == "mutlu":   # ^ ^
                    cz = serit(bez((gx - rxx, ey - ryy * 0.2), (gx, ey + ryy * 1.25), (gx + rxx, ey - ryy * 0.2)), lw * 2.3, 0.45)
                else:                # sikik: > <
                    yon = -sd
                    cz = serit(bez((gx - yon * rxx * 0.9, ey + ryy * 0.62), (gx + yon * rxx * 1.25, ey), (gx - yon * rxx * 0.9, ey - ryy * 0.62)), lw * 2.2, 0.45)
                p0 = nokta(gx, ey)
                ekle(f"goz_{k}_cizgi", ia, cz)
                for n in ("ak", "bebek", "isik1", "isik2"): ekle(f"goz_{k}_{n}", ia, p0)
            # kaş: dıştan içe
            kh, kt, kc = sp.get("kas", (0.12, 0.0, 0.05))
            by0 = ey + ryy + lw + kh * ry
            dis_x = gx + sd * rxx * 1.05; ic_x = gx - sd * rxx * 0.75
            p_dis = (dis_x, by0 - kt * rx * 0.3); p_ic = (ic_x, by0 + kt * rx)
            orta = ((p_dis[0] + p_ic[0]) / 2, (p_dis[1] + p_ic[1]) / 2 + kc * ry)
            a0, a2 = (p_dis, p_ic) if sd < 0 else (p_ic, p_dis)
            ekle(f"kas_{k}", ia, serit(bez(a0, orta, a2), lw * 1.9, 0.55))
        # ağız
        t = sp.get("agiz", "gulumse"); P0 = nokta(mx, my)
        cz = ic = dil = dis = disa = None
        if t in ("gulumse", "kucuk", "dalga", "duz"):
            g = mw * (0.42 if t == "gulumse" else 0.28 if t == "kucuk" else 0.42)
            if t == "dalga":
                cz = serit(lambda s: (mx - g + 2 * g * s, my + mw * 0.06 * math.sin(s * math.pi * 3.0)), lw * 1.7, 0.35)
            elif t == "duz":
                cz = serit(bez((mx - g, my), (mx, my - mw * 0.04), (mx + g, my)), lw * 1.7, 0.35)
            else:
                cz = serit(bez((mx - g, my + mw * 0.08), (mx, my - mw * 0.26), (mx + g, my + mw * 0.08)), lw * 1.8, 0.4)
            ic = dil = dis = disa = P0
        else:
            if t == "acik_gulus":
                sek = agiz(mx, my, mw, lambda s: mw * 0.07 * s * s + mw * 0.02, lambda s: mw * 0.07 * s * s - mw * 0.44 * (1 - s * s) ** 0.85)
                dil = ic_bolge(sek, 0.42, 0.04, 0.0); dis = ic_bolge(sek, 0.97, 0.80); disa = P0
            elif t == "zafer":
                w2 = mw * 1.2
                sek = agiz(mx, my, w2, lambda s: w2 * 0.12 * s * s - w2 * 0.01, lambda s: w2 * 0.12 * s * s - w2 * 0.46 * (1 - s * s) ** 0.8)
                dil = ic_bolge(sek, 0.45, 0.04); dis = ic_bolge(sek, 0.97, 0.78); disa = P0
            elif t == "O":
                sek = elips(mx, my - mw * 0.04, mw * 0.17, mw * 0.23)
                dil = ic_bolge(sek, 0.38, 0.05); dis = disa = P0
            elif t == "korku":
                hh = lambda s: mw * 0.15 * (1 - s ** 8) ** 0.5
                orta_f = lambda s: -mw * 0.03 - mw * 0.10 * s * s + mw * 0.025 * math.sin(s * 9)
                sek = agiz(mx, my, mw * 1.05, lambda s: orta_f(s) + hh(s), lambda s: orta_f(s) - hh(s))
                dis = ic_bolge(sek, 0.96, 0.56); disa = ic_bolge(sek, 0.44, 0.04); dil = P0
            elif t == "ezik_acik":   # ezilirken: yamuk, dişler sıkılı
                hh = lambda s: mw * 0.12 * (1 - s ** 8) ** 0.5
                orta_f = lambda s: mw * 0.06 * math.sin(s * math.pi * 1.5)
                sek = agiz(mx, my, mw * 1.1, lambda s: orta_f(s) + hh(s), lambda s: orta_f(s) - hh(s))
                dis = ic_bolge(sek, 0.95, 0.52); disa = ic_bolge(sek, 0.48, 0.05); dil = P0
            cz = sisir(sek, lw); ic = sek
        ekle("agiz_cizgi", ia, cz); ekle("agiz_ic", ia, ic); ekle("dil", ia, dil); ekle("dis", ia, dis); ekle("dis_alt", ia, disa)
        if yanak:
            yo = sp.get("yanak", 1.0)
            for sd, k in ((-1, "l"), (1, "r")):
                ekle(f"yanak_{k}", ia, elips(cx + sd * F["yx"], F["yy"], F["yr"] * yo, F["yr"] * 0.55 * yo) if yo > 0 else nokta(cx + sd * F["yx"], F["yy"]))
        if "terx" in F:
            if sp.get("ter"):
                tx, ty, tr = F["terx"], F["tery"], F["terr"]
                ekle("ter", ia, agiz(tx, ty, tr * 1.4, lambda s: tr * 1.6 * (1 - abs(s)) ** 1.6, lambda s: -tr * 0.9 * (1 - s * s) ** 0.5))
            else:
                ekle("ter", ia, nokta(F["terx"], F["tery"]))

    kas_renk = kas_renk or O.CIVIT
    M = {"cizgi": isikli("yuz_cizgi", O.CIVIT), "ak": plastik("goz_ak", "#ffffff", rough=0.2, sss=0.0, kenar=0.0),
         "bebek": plastik("bebek", "#1c1238", rough=0.15, sss=0.0, kenar=0.0), "isik": isikli("goz_isik", "#ffffff", 1.0),
         "kas": isikli("kas_" + kas_renk, kas_renk), "ic": plastik("agiz_ic", P["agiz_ic"], rough=0.4, sss=0, kenar=0),
         "dil": plastik("dil", P["dil"], rough=0.35, kenar=0), "dis": plastik("dis", "#ffffff", rough=0.3, sss=0, kenar=0),
         "yanak": plastik("yanak", P["yanak"], rough=0.6, sss=0, kenar=0, alfa=0.55), "ter": plastik("ter", P["ter"], rough=0.1, kenar=0.6)}
    duzen = {"yanak": ("yanak", 1), "cizgi": ("cizgi", 2), "ak": ("ak", 3), "bebek": ("bebek", 4), "isik1": ("isik", 5), "isik2": ("isik", 5),
             "kas": ("kas", 3), "agiz_cizgi": ("cizgi", 2), "agiz_ic": ("ic", 3), "dil": ("dil", 4), "dis": ("dis", 4), "dis_alt": ("dis", 4), "ter": ("ter", 6)}
    yuz = bos(ad + "_yuz", parent=kok)
    for parca, ifs in parcalar.items():
        anahtar = parca.split("_")[-1] if parca.startswith("goz") else ("kas" if parca.startswith("kas") else "yanak" if parca.startswith("yanak") else parca)
        mk, kat = duzen[anahtar]
        cikartma(parca, yuzey, ifs, M[mk], kat, yuz, birim=birim)
    return yuz

# ================================================================= ROKET
def roket(pilot_ifade="heyecan", R=0.52):
    kok = bos("roket")
    k1 = bos("kademe_1", parent=kok); k2 = bos("kademe_2", parent=kok)
    BEYAZ = plastik("beyaz", P["beyaz"]); KIR = plastik("kirmizi", P["kirmizi"], sss=0.15)
    GRI = plastik("metal", P["gri"], rough=0.3, sss=0.0, coat=0.6); KGRI = plastik("koyu_metal", P["koyu_gri"], rough=0.35, sss=0)
    hk = 0.022  # iç kontur kalınlığı
    # alt kademe
    pr = [(-2.0, 0)] + yay(-1.92, R - 0.08, 0.08, 180, 90) + yay(-0.40, R - 0.07, 0.07, 90, 0) + [(-0.33, 0)]
    g1 = torna("govde_1", pr, BEYAZ, parent=k1); kabuk(yumusat(g1, 1), hk)
    s1 = torna("serit_1", [(-0.95, 0)] + yay(-0.92, R - 0.01, 0.03, 180, 90) + yay(-0.70, R - 0.01, 0.03, 90, 0) + [(-0.67, 0)], KIR, parent=k1)
    kabuk(yumusat(s1, 1), hk)
    s1b = torna("serit_1b", [(-1.82, 0)] + yay(-1.80, R - 0.01, 0.025, 180, 90) + yay(-1.66, R - 0.01, 0.025, 90, 0) + [(-1.64, 0)], KIR, parent=k1)
    kabuk(yumusat(s1b, 1), hk)
    nz = torna("nozul", [(-1.9, 0), (-1.9, 0.27), (-2.05, 0.28), (-2.22, 0.33), (-2.4, 0.42), (-2.47, 0.43), (-2.48, 0.38), (-2.36, 0.31), (-2.15, 0.0)], GRI, parent=k1)
    kabuk(yumusat(nz, 1), hk)
    fin = [(-1.05, 0), (-1.55, 0.55), (-1.95, 0.78), (-2.32, 0.80), (-2.25, 0.45), (-2.0, 0)]
    for i, phi in enumerate((0, 120, 240)):
        f = plaka(f"kanat_1{'abc'[i]}", [(x, z + R - 0.08) for x, z in fin], 0.13, KIR, parent=k1, pah=0.045, seg=3)
        f.rotation_euler = (math.radians(phi), 0, 0); yumusat(f, 1); kabuk(f, hk)
    # ara halka
    ah = torna("ara_halka", [(-0.36, 0), (-0.36, R - 0.04), (-0.27, R - 0.04), (-0.27, 0)], KGRI, parent=k2); kabuk(ah, hk)
    # üst kademe
    pr2 = [(-0.28, 0)] + yay(-0.22, R - 0.07, 0.06, 180, 90) + [(0.95, R - 0.01)] + [(0.96, 0)]
    g2 = torna("govde_2", pr2, BEYAZ, parent=k2)
    # pencere oyuğu (boolean; iç yüzey koyu)
    ICK = plastik("kabin_ic", "#1d2a5c", rough=0.6, sss=0, kenar=0)
    kes = silindir("pencere_oyuk", 0.275, 1.0, ICK, loc=(0.36, -0.55, 0.02), rot=(math.pi / 2, 0, 0), seg=40)
    kes.hide_render = True; kes["gizli"] = True; kes.parent = k2
    g2.data.materials.append(ICK)
    b = g2.modifiers.new("oyuk", "BOOLEAN"); b.operation = "DIFFERENCE"; b.object = kes; b.solver = "EXACT"; b.material_mode = "TRANSFER"
    kabuk(g2, hk)
    s2 = torna("serit_2", [(-0.2, 0), (-0.2, R + 0.005), (-0.08, R + 0.005), (-0.08, 0)], KIR, parent=k2); kabuk(yumusat(s2, 1), hk)
    # burun (ogive)
    nose = [(0.93, 0)] + [(0.93, R + 0.015), (1.02, R + 0.015)]
    for i in range(1, 25):
        t = i / 24; x = 1.02 + 1.25 * t; r = (R + 0.0) * (1 - t ** 1.9) ** 0.62
        nose.append((x, max(r, 0.0) if i < 24 else 0.0))
    bu = torna("burun", nose, KIR, parent=k2); kabuk(yumusat(bu, 1), hk)
    fin2 = [(0.25, 0), (-0.05, 0.30), (-0.22, 0.36), (-0.3, 0.2), (-0.28, 0)]
    for i, phi in enumerate((0, 120, 240)):
        f = plaka(f"kanat_2{'abc'[i]}", [(x, z + R - 0.06) for x, z in fin2], 0.09, KIR, parent=k2, pah=0.03)
        f.rotation_euler = (math.radians(phi), 0, 0); yumusat(f, 1); kabuk(f, hk)
    # pencere
    pen = bos("pencere", parent=k2)
    cer = simit("pencere_cerceve", 0.30, 0.06, GRI, loc=(0.36, -R + 0.05, 0.02), rot=(math.pi / 2, 0, 0), parent=pen); kabuk(yumusat(cer, 1), hk)
    kure("kabin_arka", 0.30, ICK, loc=(0.36, -0.05, 0.02), parent=pen)
    # pilot kafası pencerede
    pk = pilot(govde=False, anten=False, ifadeler={pilot_ifade: PILOT_IFADE[pilot_ifade]}, olcek=0.25, ad="pilot_kabin")
    pk.parent = pen; pk.location = (0.36, -0.17, -0.02); pk.rotation_euler = (0, 0, math.radians(8))
    cam = cam_mat()
    camo = kure("pencere_cam", 0.28, cam, loc=(0.36, -R + 0.02, 0.02), olcek=(1, 0.32, 1), parent=pen)
    camo.visible_shadow = False
    par = kure("cam_parilti", 0.07, isikli("parilti_beyaz", "#ffffff", 1.0, alfa=0.85), loc=(0.25, -R - 0.06, 0.15), olcek=(1.0, 0.3, 0.45), parent=pen)
    par.rotation_euler = (0, math.radians(35), 0); par.visible_shadow = False
    return kok

def cam_mat():
    m, nt, N, L = O._yeni("cam")
    out = N.new("ShaderNodeOutputMaterial"); tr = N.new("ShaderNodeBsdfTransparent"); tr.inputs[0].default_value = lin("#cdeeff")
    gl = N.new("ShaderNodeBsdfGlossy"); gl.inputs["Roughness"].default_value = 0.04
    lw = N.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.25
    mr = N.new("ShaderNodeMapRange"); mr.inputs["To Min"].default_value = 0.12; mr.inputs["To Max"].default_value = 0.9
    L.new(lw.outputs["Fresnel"], mr.inputs["Value"])
    mx = N.new("ShaderNodeMixShader"); L.new(mr.outputs["Result"], mx.inputs[0]); L.new(tr.outputs[0], mx.inputs[1]); L.new(gl.outputs[0], mx.inputs[2])
    L.new(mx.outputs[0], out.inputs[0])
    return m

# ================================================================= PİLOT
PILOT_IFADE = {
    "notr":    dict(goz="acik", bebek=0.56, bakis=(0.25, 0.05), kas=(0.10, 0.0, 0.06), agiz="gulumse"),
    "heyecan": dict(goz="acik", goz_olcek=1.06, bebek=0.60, bakis=(0.2, 0.15), kas=(0.22, -0.1, 0.10), agiz="acik_gulus", yanak=1.25),
    "saskin":  dict(goz="genis", goz_olcek=1.28, goz_gen=1.08, bebek=0.36, bakis=(0, 0), kas=(0.42, 0.0, 0.12), agiz="O", yanak=0.6),
    "korku":   dict(goz="genis", goz_olcek=1.22, bebek=0.27, bakis=(0.0, -0.2), kas=(0.25, 0.75, 0.0), agiz="korku", ter=True, yanak=0.0),
    "zafer":   dict(goz="mutlu", kas=(0.30, -0.15, 0.12), agiz="zafer", yanak=1.35),
}

def pilot(govde=True, anten=True, ifadeler=None, olcek=1.0, ad="pilot"):
    ifadeler = ifadeler or PILOT_IFADE
    kok = bos(ad); kok.scale = (olcek,) * 3
    BEYAZ = plastik("beyaz", P["beyaz"]); KIR = plastik("kirmizi", P["kirmizi"], sss=0.15)
    GRI = plastik("metal", P["gri"], rough=0.3, sss=0.0, coat=0.6)
    TEN = plastik("ten", P["ten"], rough=0.45, sss=0.35, coat=0.1)
    SAC = plastik("sac", P["sac"], rough=0.5, sss=0.1)
    hk = 0.03
    # kask: kutbu -Y'ye bakan küre, ön açıklık 52°
    import bmesh
    def kapak_kure(adk, r, tut, mat):
        bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=48, v_segments=24, radius=r)
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=__import__("mathutils").Matrix.Rotation(math.pi / 2, 3, "X"))
        sil = [f for f in bm.faces if not tut(f.calc_center_median())]
        bmesh.ops.delete(bm, geom=sil, context="FACES")
        me = O.bpy.data.meshes.new(adk); bm.to_mesh(me); bm.free()
        o = O.bpy.data.objects.new(adk, me); O.bpy.context.scene.collection.objects.link(o)
        me.materials.append(mat); o.parent = kok
        for p in me.polygons: p.use_smooth = True
        return o
    ac = math.radians(52)
    kask = kapak_kure("kask", 1.0, lambda c: c.y > -math.cos(ac) * 1.0, BEYAZ)
    so = kask.modifiers.new("kalinlik", "SOLIDIFY"); so.thickness = 0.08; so.offset = -1
    yumusat(kask, 1); kabuk(kask, hk)
    hal = simit("kask_halka", math.sin(ac) * 0.985, 0.075, GRI, loc=(0, -math.cos(ac) * 0.98, 0), rot=(math.pi / 2, 0, 0), parent=kok)
    kabuk(yumusat(hal, 1), hk)
    # açık vizör: kaskın üstüne kalkmış altın cam
    viz = kapak_kure("vizor", 1.06, lambda c: c.y < -math.cos(math.radians(44)) * 1.06, plastik("vizor", "#46b8ff", rough=0.06, sss=0, coat=1.0, kenar=1.2))
    so = viz.modifiers.new("kalinlik", "SOLIDIFY"); so.thickness = 0.04; so.offset = -1
    viz.rotation_euler = (math.radians(-80), 0, 0); yumusat(viz, 1); kabuk(viz, hk)
    # kulaklıklar
    for sd in (-1, 1):
        k = silindir(f"kulak_{'l' if sd < 0 else 'r'}", 0.27, 0.16, KIR, loc=(sd * 0.98, 0.0, -0.02), rot=(0, math.pi / 2, 0), parent=kok, seg=32, pah=0.05)
        yumusat(k, 1); kabuk(k, hk)
    if anten:
        a = silindir("anten", 0.03, 0.5, GRI, loc=(0.42, 0.05, 1.08), rot=(0, math.radians(22), 0), parent=kok)
        kabuk(a, hk)
        kabuk(kure("anten_top", 0.11, KIR, loc=(0.52, 0.05, 1.33), parent=kok), hk)
    # kafa
    Rh = 0.72; hc = (0, -0.07, -0.05)
    kafa = kure("kafa", Rh, TEN, loc=hc, parent=kok, seg=48, halka=24)
    # saç perçemi
    sac = metatop("sac", [(-0.42, -0.42, 0.42, 0.24), (-0.18, -0.55, 0.50, 0.26), (0.08, -0.56, 0.52, 0.25), (0.30, -0.50, 0.46, 0.24),
                          (0.48, -0.36, 0.38, 0.2), (0.0, -0.2, 0.62, 0.35), (-0.05, -0.62, 0.40, 0.14), (0.22, -0.63, 0.36, 0.12)], SAC, parent=kok, coz=0.035)
    sac.location = hc; kabuk(sac, hk)
    yz = Yuzey(lambda a: math.sqrt(max(Rh * Rh - a * a, 0.0)), "Z", merkez=hc)
    F = dict(ex=0.27, ey=0.0, rx=0.155, ry=0.195, lw=0.035, mx=0.0, my=-0.33, mw=0.40, yx=0.47, yy=-0.2, yr=0.11,
             terx=0.50, tery=0.20, terr=0.06)
    yuz_kur("pilot", yz, kok, F, ifadeler, kas_renk="#5a2a10", birim=0.004)
    if govde:
        tor = torna("govde", [(-0.78, 0), (-0.78, 0.40), (-0.92, 0.62), (-1.15, 0.80), (-1.5, 0.86), (-1.78, 0.80), (-1.9, 0.55), (-1.93, 0)], BEYAZ, eksen="Z", parent=kok)
        yumusat(tor, 1); kabuk(tor, hk)
        yaka = simit("yaka", 0.6, 0.11, GRI, loc=(0, 0, -0.86), parent=kok); kabuk(yumusat(yaka, 1), hk)
        rozet = silindir("rozet", 0.17, 0.06, KIR, loc=(-0.28, -0.80, -1.30), rot=(math.radians(84), 0, math.radians(-16)), parent=kok, seg=32, pah=0.02)
        kabuk(rozet, hk)
        pan = plaka("gogus_panel", [(0.12, -1.18), (0.44, -1.18), (0.44, -1.42), (0.12, -1.42)], 0.06, plastik("mavi", P["mavi"]), parent=kok, pah=0.02)
        pan.location = (0, -0.84, 0); pan.rotation_euler = (0, 0, math.radians(14)); kabuk(pan, hk)
    return kok

# ================================================================= ortak nesne yüzü
NESNE_IFADE = {
    "normal": dict(goz="yari", kapak=0.45, bebek=0.58, bakis=(0.35, 0.05), kas=(0.18, -0.1, 0.02), agiz="gulumse"),
    "ezik":   dict(goz="sikik", kas=(0.05, 0.5, -0.05), agiz="ezik_acik", yanak=0.0),
    "saskin": dict(goz="genis", goz_olcek=1.25, bebek=0.34, bakis=(0, 0.1), kas=(0.45, 0.0, 0.12), agiz="O", yanak=0.6),
}

def _renk_karistir(N, L, fac, a, b):
    m = N.new("ShaderNodeMix"); m.data_type = "RGBA"
    if isinstance(fac, float): m.inputs[0].default_value = fac
    else: L.new(fac, m.inputs[0])
    for idx, v in ((6, a), (7, b)):
        if isinstance(v, tuple): m.inputs[idx].default_value = v
        else: L.new(v, m.inputs[idx])
    return m.outputs[2]

def _math(N, L, op, a, b=None):
    m = N.new("ShaderNodeMath"); m.operation = op
    for i, v in enumerate((a, b)):
        if v is None: continue
        if isinstance(v, (int, float)): m.inputs[i].default_value = v
        else: L.new(v, m.inputs[i])
    return m.outputs[0]

def _xyz(N, L):
    tc = N.new("ShaderNodeTexCoord"); sp = N.new("ShaderNodeSeparateXYZ"); L.new(tc.outputs["Object"], sp.inputs[0]); return sp

def zarf_renk(nt, N, L):
    sp = _xyz(N, L)
    z = sp.outputs["Z"]
    serit_ = _math(N, L, "MULTIPLY", _math(N, L, "GREATER_THAN", z, -0.44), _math(N, L, "LESS_THAN", z, -0.20))
    ac = _math(N, L, "ARCTAN2", sp.outputs["Z"], sp.outputs["Y"])
    fr = _math(N, L, "FRACT", _math(N, L, "MULTIPLY", ac, 12 / (2 * math.pi)))
    dikis = _math(N, L, "LESS_THAN", _math(N, L, "ABSOLUTE", _math(N, L, "SUBTRACT", fr, 0.5)), 0.035)
    c = _renk_karistir(N, L, dikis, lin(P["mor"]), lin("#5f33c4"))
    return _renk_karistir(N, L, serit_, c, lin(P["sari"]))

def zeplin_r(x):
    if x >= 0: return 1.0 * max(0.0, 1 - (x / 2.0) ** 2) ** 0.5
    return 1.0 * max(0.0, 1 - (x / 2.35) ** 2) ** 0.62

def zeplin(ifadeler=None):
    ifadeler = ifadeler or NESNE_IFADE
    kok = bos("zeplin"); govde = bos("zeplin_govde", parent=kok)
    hk = 0.03
    pr = [(2.0, 0)]
    for i in range(1, 60):
        t = i / 60; x = 2.0 - t * 4.35; pr.append((x, zeplin_r(x)))
    pr.append((-2.35, 0))
    zarf = torna("zarf", pr, plastik("zarf", P["mor"], renk_dugum=zarf_renk, sss=0.18), parent=govde, seg=64)
    # ezilme şekil anahtarı: tepeye çökme
    zarf.shape_key_add(name="Basis", from_mix=False); kb = zarf.shape_key_add(name="cokme", from_mix=False)
    for j, v in enumerate(zarf.data.vertices):
        x, y, z = v.co; w = math.exp(-((x + 0.1) / 0.75) ** 2) * max(0.0, z) ** 1.5
        kb.data[j].co = (x, y * (1 + 0.08 * w), z - 0.38 * w)
    yumusat(zarf, 1); kabuk(zarf, hk)
    KIR = plastik("kirmizi", P["kirmizi"], sss=0.15); SARI = plastik("sari", P["sari"])
    fin = [(-1.25, 0.35), (-1.85, 1.08), (-2.38, 1.12), (-2.28, 0.25)]
    for i, phi in enumerate((0, 90, 180, 270)):
        f = plaka(f"kanat_{i}", fin, 0.14, KIR, parent=govde, pah=0.05); f.rotation_euler = (math.radians(phi), 0, 0)
        yumusat(f, 1); kabuk(f, hk)
    gon = bos("gondol", parent=govde)
    g = torna("gondol_govde", [(-0.15, 0)] + yay(-0.05, 0.15, 0.12, 180, 90) + yay(0.95, 0.12, 0.15, 90, 0) + [(1.1, 0)], SARI, parent=gon)
    g.location = (0.0, 0, -1.02); yumusat(g, 1); kabuk(g, hk)
    for sx in (0.15, 0.85):
        d = silindir(f"gondol_ip_{sx}", 0.03, 0.3, plastik("metal", P["gri"]), loc=(sx, 0, -0.82), parent=gon); kabuk(d, 0.015)
    for i, sx in enumerate((0.2, 0.47, 0.74)):
        w = kure(f"gondol_pencere_{i}", 0.085, plastik("pencere", "#2b4fa8", rough=0.1, coat=1, kenar=0), loc=(sx, -0.25, -1.0), olcek=(1, 0.35, 1), parent=gon)
        kabuk(w, 0.02)
    per = bos("pervane", parent=govde, loc=(-2.42, 0, 0))
    kabuk(kure("pervane_gobek", 0.12, plastik("metal", P["gri"]), parent=per), hk)
    for i, a in enumerate((20, 200)):
        b = plaka(f"pervane_kanat_{i}", [(0, 0.0), (0.06, 0.1), (0.04, 0.48), (-0.04, 0.48), (-0.06, 0.1)], 0.05, SARI, parent=per, pah=0.02)
        b.rotation_euler = (math.radians(a), 0, 0); kabuk(b, 0.015)
    yz = Yuzey(zeplin_r, "X")
    F = dict(cx=1.12, ex=0.30, ey=0.12, rx=0.16, ry=0.21, lw=0.038, mx=1.15, my=-0.25, mw=0.44, yx=0.48, yy=-0.10, yr=0.12)
    yuz_kur("zeplin", yz, govde, F, ifadeler, birim=0.005)
    kok.rotation_euler = (0, 0, math.radians(-16))
    return kok

# ================================================================= REKLAM BALONU
def balon_r(z):
    if z >= -0.6: return math.sqrt(max(0.0, 1 - z * z))
    t = (-0.6 - z) / 0.68; t = min(1, max(0, t))
    h00 = 2 * t ** 3 - 3 * t ** 2 + 1; h10 = t ** 3 - 2 * t ** 2 + t; h01 = -2 * t ** 3 + 3 * t ** 2
    return h00 * 0.8 + h10 * (-0.51) + h01 * 0.17

def balon_renk(nt, N, L):
    sp = _xyz(N, L)
    ac = _math(N, L, "ARCTAN2", sp.outputs["Y"], sp.outputs["X"])
    # ön dilim -Y yönünde ortalı olsun: açıyı kaydır
    k = _math(N, L, "FRACT", _math(N, L, "MULTIPLY", _math(N, L, "ADD", ac, math.pi / 2 + math.pi / 8), 8 / (2 * math.pi)))
    idx = _math(N, L, "FLOOR", _math(N, L, "MULTIPLY", _math(N, L, "FRACT", _math(N, L, "MULTIPLY", _math(N, L, "ADD", ac, math.pi / 2 + math.pi / 8), 1 / (2 * math.pi))), 8))
    m4 = _math(N, L, "MODULO", idx, 4)
    rp = N.new("ShaderNodeValToRGB"); rp.color_ramp.interpolation = "CONSTANT"
    e = rp.color_ramp.elements; e[0].position = 0.0; e[0].color = lin("#fff6e8"); e[1].position = 0.3; e[1].color = lin(P["kirmizi"])
    e.new(0.55).color = lin(P["sari"]); e.new(0.8).color = lin(P["mavi"])
    L.new(_math(N, L, "DIVIDE", m4, 3.2), rp.inputs[0])
    return rp.outputs[0]

def balon(ifadeler=None):
    ifadeler = ifadeler or NESNE_IFADE
    kok = bos("balon"); govde = bos("balon_govde", parent=kok)
    hk = 0.025
    pr = [(-1.28, 0)]
    for i in range(0, 64):
        z = -1.28 + (2.28) * i / 63; pr.append((z, balon_r(z)))
    pr[-1] = (1.0, 0)
    zarf = torna("balon_zarf", pr, plastik("balon_zarf", "#ffffff", renk_dugum=balon_renk, sss=0.2), eksen="Z", parent=govde, seg=64)
    zarf.shape_key_add(name="Basis", from_mix=False); kb = zarf.shape_key_add(name="cokme", from_mix=False)
    for j, v in enumerate(zarf.data.vertices):
        x, y, z = v.co; w = max(0.0, z) ** 2.2 * math.exp(-(x * x) / 0.5)
        kb.data[j].co = (x * (1 + 0.06 * w), y * (1 + 0.06 * w), z - 0.4 * w)
    yumusat(zarf, 1); kabuk(zarf, hk)
    boyun = torna("balon_boyun", [(-1.38, 0), (-1.38, 0.15), (-1.26, 0.19), (-1.20, 0)], plastik("metal", P["gri"]), eksen="Z", parent=govde); kabuk(boyun, hk)
    sep = bos("sepet", parent=kok)
    HAS = plastik("hasir", "#c9803a", rough=0.6, sss=0.1)
    s = torna("sepet_govde", [(-2.0, 0), (-2.0, 0.24), (-1.98, 0.27), (-1.72, 0.30), (-1.70, 0.0)], HAS, eksen="Z", parent=sep); yumusat(s, 1); kabuk(s, hk)
    kabuk(simit("sepet_kenar", 0.30, 0.04, plastik("hasir_k", "#8f5420"), loc=(0, 0, -1.70), parent=sep), hk)
    for i in range(4):
        a = math.radians(45 + 90 * i); x, y = 0.27 * math.cos(a), 0.27 * math.sin(a)
        x2, y2 = 0.16 * math.cos(a), 0.16 * math.sin(a)
        L_ = math.dist((x, y, -1.70), (x2, y2, -1.36))
        ip = silindir(f"ip_{i}", 0.014, L_, plastik("ip", "#6e4a2c"), loc=((x + x2) / 2, (y + y2) / 2, -1.53), parent=sep, seg=8)
        d = Vector((x2 - x, y2 - y, 0.34)); ip.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
    tab = bos("tabela", parent=kok)
    TB = plastik("tabela", "#fffaf0", rough=0.5)
    t = plaka("tabela_levha", [(-0.75, -2.32), (0.75, -2.32), (0.75, -2.78), (-0.75, -2.78)], 0.08, TB, parent=tab, pah=0.04)
    kabuk(t, hk)
    cerc = plaka("tabela_cerceve", [(-0.82, -2.26), (0.82, -2.26), (0.82, -2.84), (-0.82, -2.84)], 0.06, plastik("kirmizi", P["kirmizi"]), parent=tab, pah=0.03)
    cerc.location = (0, 0.04, 0); kabuk(cerc, hk)
    for sx in (-0.5, 0.5):
        silindir(f"tabela_ip_{sx}", 0.014, 0.28, plastik("ip", "#6e4a2c"), loc=(sx * 0.7, 0, -2.13), rot=(0, math.radians(-sx * 30), 0), parent=tab, seg=8)
    yz = Yuzey(balon_r, "Z")
    F = dict(cx=0.0, ex=0.29, ey=0.12, rx=0.15, ry=0.2, lw=0.036, mx=0.0, my=-0.24, mw=0.4, yx=0.46, yy=-0.1, yr=0.11)
    yuz_kur("balon", yz, govde, F, ifadeler, birim=0.005)
    kok.rotation_euler = (0, 0, math.radians(10))
    return kok

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
        y = plaka(f"yildiz_{kare}_{i}", yildiz_sekil(rr, rr * 0.48, 5, random.uniform(0, 1) + kare * 0.5), 0.16, YIL, duzlem="XZ", parent=kok, pah=0.05)
        y.location = (math.cos(a) * yol, -0.4, math.sin(a) * yol); y.rotation_euler = (random.uniform(-0.4, 0.4), random.uniform(-0.6, 0.6), 0)
        yumusat(y, 1); kabuk(y, 0.02)
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
