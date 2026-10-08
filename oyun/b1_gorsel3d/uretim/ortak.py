# Son Durak: Plüton · B1 3B görsel deneme · ortak altyapı
# Sürüm: Blender 5.0.1 (pip 'bpy' 5.0.1, Python 3.11) ile yazıldı/denendi; Blender 5.2 ile de çalışması beklenir.
# Çalıştırma: python3.11 -m venv v && v/bin/pip install bpy pillow numpy ;  v/bin/python uret.py <set>
#   ya da   blender -b --factory-startup -P uret.py -- <set>
# İçerik: sahne/render ayarı, malzemeler (boyalı plastik + kenar ışığı), ışık düzenleri (A/B/C),
#         torna (lathe) gövde, ters-kabuk iç kontur, 'çıkartma' yüz sistemi (şekil anahtarlı ifadeler).
import bpy, bmesh, math, os, sys
from mathutils import Vector, Matrix, Euler

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HAM = os.path.join(KOK, "sprite", "ham")      # konursuz ham render (alfa)
os.makedirs(HAM, exist_ok=True)

STIL = "B"      # A: klasik üç nokta (AgX) · B: gök kubbesi + kenar ışığı (önerilen) · C: cel/toon BSDF
CIVIT = "#2a1d4f"   # dış kontur rengi (çivit)

def argumanlar():
    a = sys.argv
    return a[a.index("--") + 1:] if "--" in a else a[1:]

def lin(h):
    h = h.lstrip("#"); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple((x / 12.92) if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)

# ---------------------------------------------------------------- sahne
def sifirla(stil=None):
    global STIL, _MATS
    if stil: STIL = stil
    _MATS = {}
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    s.render.engine = "CYCLES"; s.cycles.device = "CPU"
    s.cycles.samples = 64; s.cycles.use_adaptive_sampling = True; s.cycles.adaptive_threshold = 0.02
    s.cycles.use_denoising = True; s.cycles.denoiser = "OPENIMAGEDENOISE"
    s.cycles.max_bounces = 6; s.cycles.diffuse_bounces = 3; s.cycles.glossy_bounces = 2
    s.cycles.transmission_bounces = 4; s.cycles.transparent_max_bounces = 24
    s.cycles.caustics_reflective = False; s.cycles.caustics_refractive = False
    s.render.film_transparent = True
    s.render.image_settings.file_format = "PNG"; s.render.image_settings.color_mode = "RGBA"
    s.render.resolution_percentage = 100
    if STIL == "A":
        s.view_settings.view_transform = "AgX"; s.view_settings.look = "AgX - Punchy"
    else:
        s.view_settings.view_transform = "Standard"
    s.view_settings.exposure = 0.0
    cam = bpy.data.objects.new("kamera", bpy.data.cameras.new("kamera"))
    s.collection.objects.link(cam); s.camera = cam
    cam.data.type = "ORTHO"; cam.location = (0, -40, 0); cam.rotation_euler = (math.pi / 2, 0, 0)
    cam.data.clip_end = 200
    isik_kur()
    return s

def bos(ad, loc=(0, 0, 0), parent=None):
    o = bpy.data.objects.new(ad, None); bpy.context.scene.collection.objects.link(o)
    o.location = loc
    if parent: o.parent = parent
    return o

def mesh_obj(ad, verts, faces, mat=None, parent=None, smooth=True):
    me = bpy.data.meshes.new(ad); me.from_pydata([tuple(v) for v in verts], [], faces); me.update()
    o = bpy.data.objects.new(ad, me); bpy.context.scene.collection.objects.link(o)
    if mat: me.materials.append(mat)
    if smooth:
        for p in me.polygons: p.use_smooth = True
    if parent: o.parent = parent
    return o

# ---------------------------------------------------------------- ışık
def _dunya(ust, ufuk, alt, guc):
    w = bpy.data.worlds.new("dunya"); bpy.context.scene.world = w
    w.use_nodes = True; nt = w.node_tree; N = nt.nodes; L = nt.links
    bg = N["Background"]; tc = N.new("ShaderNodeTexCoord"); sp = N.new("ShaderNodeSeparateXYZ")
    mr = N.new("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = -1; mr.inputs["From Max"].default_value = 1
    rp = N.new("ShaderNodeValToRGB"); e = rp.color_ramp.elements
    e[0].position = 0.30; e[0].color = lin(alt); e[1].position = 0.75; e[1].color = lin(ust)
    m = e.new(0.52); m.color = lin(ufuk)
    L.new(tc.outputs["Generated"], sp.inputs[0]); L.new(sp.outputs["Z"], mr.inputs["Value"])
    L.new(mr.outputs["Result"], rp.inputs[0]); L.new(rp.outputs[0], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = guc

def isik(ad, tip, loc, hedef=(0, 0, 0), guc=100, boy=2.0, renk="#ffffff", aci=None):
    ld = bpy.data.lights.new(ad, tip); ld.energy = guc; ld.color = lin(renk)[:3]
    if tip == "AREA": ld.size = boy; ld.shape = "DISK"
    if tip == "SUN" and aci is not None: ld.angle = math.radians(aci)
    o = bpy.data.objects.new(ad, ld); bpy.context.scene.collection.objects.link(o)
    o.location = loc
    d = Vector(hedef) - Vector(loc); o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    return o

def isik_kur():
    if STIL == "A":
        # STANDART TARİF: üç nokta ışık (anahtar + dolgu + arka/kenar), nötr gri dünya
        _dunya("#6f7380", "#6f7380", "#5a5d66", 0.35)
        isik("anahtar", "AREA", (-6, -9, 7), guc=2600, boy=5, renk="#fff1de")
        isik("dolgu", "AREA", (8, -8, -1), guc=700, boy=6, renk="#dfe8ff")
        isik("arka", "AREA", (2, 8, 7), guc=2200, boy=3, renk="#ffffff")
    else:
        # GÖK KUBBESİ: oyunun kendi gökyüzü ışığı (mavi zenit, açık ufuk, alttan sıcak bulut sekmesi)
        # + yumuşak sıcak güneş (sol üst ön) + iki renkli kenar ışığı (arkadan sağ-üst soğuk, sol sıcak)
        _dunya("#4f9dff", "#d9ecff", "#ffe2b8", 0.85)
        isik("gunes", "SUN", (-5, -6, 8), guc=3.6, renk="#fff0d6", aci=12)
        isik("kenar_soguk", "AREA", (6, 9, 6), guc=2600, boy=4, renk="#d8f0ff")
        isik("kenar_sicak", "AREA", (-8, 8, 1), guc=1500, boy=4, renk="#ffd2a6")
        # yüz dolgusu: kameradan gelen zayıf, geniş, sıcak ışık (kask içindeki yüz kararmasın)
        isik("yuz_dolgu", "AREA", (1, -14, 2), guc=900, boy=10, renk="#fff4e8")

# ---------------------------------------------------------------- malzemeler
_MATS = {}

def _yeni(ad):
    m = bpy.data.materials.new(ad); m.use_nodes = True
    nt = m.node_tree; N = nt.nodes; N.clear()
    return m, nt, N, nt.links

def _kenar_isigi(N, L, renk_lin, guc):
    """Yüzeyin kameraya dik kaldığı yerde (kenar) ışık; üst-sol yarıda daha güçlü. Çıkış: emisyon gücü düğümü."""
    lw = N.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.35
    pw = N.new("ShaderNodeMath"); pw.operation = "POWER"; pw.inputs[1].default_value = 2.2
    L.new(lw.outputs["Facing"], pw.inputs[0])
    g = N.new("ShaderNodeNewGeometry"); dp = N.new("ShaderNodeVectorMath"); dp.operation = "DOT_PRODUCT"
    dp.inputs[1].default_value = (0.25, 0.35, 0.9)
    L.new(g.outputs["Normal"], dp.inputs[0])
    mr = N.new("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = -0.4; mr.inputs["From Max"].default_value = 0.9
    mr.inputs["To Min"].default_value = 0.25; mr.inputs["To Max"].default_value = 1.0
    L.new(dp.outputs["Value"], mr.inputs["Value"])
    m1 = N.new("ShaderNodeMath"); m1.operation = "MULTIPLY"; L.new(pw.outputs[0], m1.inputs[0]); L.new(mr.outputs["Result"], m1.inputs[1])
    m2 = N.new("ShaderNodeMath"); m2.operation = "MULTIPLY"; m2.inputs[1].default_value = guc; L.new(m1.outputs[0], m2.inputs[0])
    return m2

def plastik(ad, hexc, rough=0.36, coat=0.4, sss=0.12, kenar=0.55, renk_dugum=None, alfa=1.0):
    """Boyalı plastik. renk_dugum: (nt, N, L) -> soket döndüren işlev (desenli renk için)."""
    key = (ad, hexc)
    if key in _MATS and renk_dugum is None: return _MATS[key]
    m, nt, N, L = _yeni(ad)
    out = N.new("ShaderNodeOutputMaterial")
    c = lin(hexc)
    if STIL == "C":
        # cel: toon diffuse + keskin toon parlama + kenar ışığı
        td = N.new("ShaderNodeBsdfToon"); td.component = "DIFFUSE"; td.inputs["Size"].default_value = 0.62; td.inputs["Smooth"].default_value = 0.06
        tg = N.new("ShaderNodeBsdfToon"); tg.component = "GLOSSY"; tg.inputs["Size"].default_value = 0.12; tg.inputs["Smooth"].default_value = 0.04
        tg.inputs["Color"].default_value = (1, 1, 1, 1)
        amb = N.new("ShaderNodeEmission")  # gölgede rengin %35'i kalsın (cel 'ortam' bandı)
        amb.inputs["Strength"].default_value = 0.30
        sk = renk_dugum(nt, N, L) if renk_dugum else None
        for t in (td, amb):
            if sk: L.new(sk, t.inputs["Color"])
            else: t.inputs["Color"].default_value = c
        a1 = N.new("ShaderNodeAddShader"); L.new(td.outputs[0], a1.inputs[0]); L.new(amb.outputs[0], a1.inputs[1])
        mg = N.new("ShaderNodeMixShader"); mg.inputs[0].default_value = 0.12
        L.new(a1.outputs[0], mg.inputs[1]); L.new(tg.outputs[0], mg.inputs[2])
        ke = N.new("ShaderNodeEmission"); ke.inputs["Color"].default_value = (1, 1, 1, 1)
        L.new(_kenar_isigi(N, L, c, 0.9).outputs[0], ke.inputs["Strength"])
        a2 = N.new("ShaderNodeAddShader"); L.new(mg.outputs[0], a2.inputs[0]); L.new(ke.outputs[0], a2.inputs[1])
        L.new(a2.outputs[0], out.inputs[0])
    else:
        p = N.new("ShaderNodeBsdfPrincipled")
        sk = renk_dugum(nt, N, L) if renk_dugum else None
        if sk: L.new(sk, p.inputs["Base Color"])
        else: p.inputs["Base Color"].default_value = c
        p.inputs["Roughness"].default_value = rough
        p.inputs["Subsurface Weight"].default_value = sss
        p.inputs["Subsurface Radius"].default_value = (1.0, 0.45, 0.3)
        p.inputs["Subsurface Scale"].default_value = 0.06
        p.inputs["Coat Weight"].default_value = coat; p.inputs["Coat Roughness"].default_value = 0.08
        p.inputs["Specular IOR Level"].default_value = 0.45
        p.inputs["Alpha"].default_value = alfa
        if STIL == "B" and kenar > 0:
            # kenar rengi: malzeme renginin açık/doygun hâli
            kr = tuple(min(1.0, x * 0.5 + 0.5) for x in c[:3]) + (1,)
            p.inputs["Emission Color"].default_value = kr
            L.new(_kenar_isigi(N, L, c, kenar).outputs[0], p.inputs["Emission Strength"])
        L.new(p.outputs[0], out.inputs[0])
    if renk_dugum is None: _MATS[key] = m
    return m

def isikli(ad, hexc, guc=1.0, alfa=None):
    """Düz ışık yayan (göz parıltısı, alev, efekt). alfa: (N,L)->soket ya da sayı."""
    m, nt, N, L = _yeni(ad); out = N.new("ShaderNodeOutputMaterial")
    e = N.new("ShaderNodeEmission"); e.inputs["Color"].default_value = lin(hexc); e.inputs["Strength"].default_value = guc
    if alfa is None:
        L.new(e.outputs[0], out.inputs[0])
    else:
        tr = N.new("ShaderNodeBsdfTransparent"); mx = N.new("ShaderNodeMixShader")
        if isinstance(alfa, (int, float)): mx.inputs[0].default_value = alfa
        else: L.new(alfa(N, L), mx.inputs[0])
        L.new(tr.outputs[0], mx.inputs[1]); L.new(e.outputs[0], mx.inputs[2]); L.new(mx.outputs[0], out.inputs[0])
    return m

def kabuk_mat(hexc=None):
    """Ters kabuk (inverted hull) kontur malzemesi: yalnız kamera ışınında, arka yüzde görünür."""
    hexc = hexc or CIVIT
    if ("kabuk", hexc) in _MATS: return _MATS[("kabuk", hexc)]
    m, nt, N, L = _yeni("kabuk_" + hexc)
    o = N.new("ShaderNodeOutputMaterial"); mix = N.new("ShaderNodeMixShader")
    em = N.new("ShaderNodeEmission"); em.inputs[0].default_value = lin(hexc); tr = N.new("ShaderNodeBsdfTransparent")
    g = N.new("ShaderNodeNewGeometry"); lp = N.new("ShaderNodeLightPath")
    inv = N.new("ShaderNodeMath"); inv.operation = "SUBTRACT"; inv.inputs[0].default_value = 1
    L.new(lp.outputs["Is Camera Ray"], inv.inputs[1])
    mx = N.new("ShaderNodeMath"); mx.operation = "MAXIMUM"
    L.new(g.outputs["Backfacing"], mx.inputs[0]); L.new(inv.outputs[0], mx.inputs[1])
    L.new(mx.outputs[0], mix.inputs[0]); L.new(em.outputs[0], mix.inputs[1]); L.new(tr.outputs[0], mix.inputs[2])
    L.new(mix.outputs[0], o.inputs[0])
    _MATS[("kabuk", hexc)] = m
    return m

def kabuk(o, kalinlik, hexc=None):
    """İç kontur: parçalar arası ayrım çizgisi (dış kalın kontur kompozitte eklenir)."""
    o.data.materials.append(kabuk_mat(hexc))
    sm = o.modifiers.new("kabuk", "SOLIDIFY"); sm.thickness = kalinlik; sm.offset = 1
    sm.use_flip_normals = True; sm.use_rim = False; sm.material_offset = len(o.data.materials) - 1
    sm.use_even_offset = True
    return o

def yumusat(o, seviye=1, bevel=None, seg=3):
    if bevel:
        b = o.modifiers.new("pah", "BEVEL"); b.width = bevel; b.segments = seg; b.limit_method = "ANGLE"
        b.angle_limit = math.radians(35); b.harden_normals = False
    if seviye:
        s = o.modifiers.new("alt", "SUBSURF"); s.levels = seviye; s.render_levels = seviye
    return o

# ---------------------------------------------------------------- geometri
def torna(ad, profil, mat, seg=48, eksen="X", parent=None, loc=(0, 0, 0)):
    """profil: [(eksen_konumu, yarıçap), ...]; yarıçap≈0 ise kutup noktası."""
    V, F, halkalar = [], [], []
    for a, r in profil:
        if r < 1e-5:
            halkalar.append([len(V)]); V.append((a, 0, 0) if eksen == "X" else (0, 0, a))
        else:
            h = []
            for k in range(seg):
                f = 2 * math.pi * k / seg
                h.append(len(V))
                V.append((a, r * math.cos(f), r * math.sin(f)) if eksen == "X" else (r * math.cos(f), r * math.sin(f), a))
            halkalar.append(h)
    for h1, h2 in zip(halkalar, halkalar[1:]):
        if len(h1) == 1 and len(h2) == 1: continue
        if len(h1) == 1:
            for k in range(seg): F.append((h1[0], h2[(k + 1) % seg], h2[k]))
        elif len(h2) == 1:
            for k in range(seg): F.append((h1[k], h1[(k + 1) % seg], h2[0]))
        else:
            for k in range(seg): F.append((h1[k], h1[(k + 1) % seg], h2[(k + 1) % seg], h2[k]))
    o = mesh_obj(ad, V, F, mat, parent)
    o.location = loc
    # normaller dışa baksın
    bm = bmesh.new(); bm.from_mesh(o.data); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(o.data); bm.free()
    return o

def yay(cx, cr, rad, a0, a1, n=6):
    """profil köşesi yuvarlatma: (eksen, yarıçap) düzleminde çember yayı."""
    return [(cx + rad * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cr + rad * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]

def plaka(ad, nokta2d, kalinlik, mat, duzlem="XZ", parent=None, pah=0.03, seg=3):
    """2B çokgeni kalınlaştırıp pahlar (kanatçık, yıldız, tabela)."""
    bm = bmesh.new()
    vs = []
    for (a, b) in nokta2d:
        if duzlem == "XZ": vs.append(bm.verts.new((a, kalinlik / 2, b)))
        else: vs.append(bm.verts.new((a, b, kalinlik / 2)))
    f = bm.faces.new(vs)
    r = bmesh.ops.extrude_face_region(bm, geom=[f])
    off = (0, -kalinlik, 0) if duzlem == "XZ" else (0, 0, -kalinlik)
    bmesh.ops.translate(bm, vec=off, verts=[e for e in r["geom"] if isinstance(e, bmesh.types.BMVert)])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(ad); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(ad, me); bpy.context.scene.collection.objects.link(o)
    me.materials.append(mat)
    if parent: o.parent = parent
    if pah:
        b = o.modifiers.new("pah", "BEVEL"); b.width = pah; b.segments = seg; b.limit_method = "ANGLE"
        b.angle_limit = math.radians(30)
    for p in me.polygons: p.use_smooth = True
    # keskin düz yüzler: yumuşak gölgelemede bozulmasın diye ağırlıklı normal
    wn = o.modifiers.new("wn", "WEIGHTED_NORMAL"); wn.keep_sharp = True
    return o

def kure(ad, r, mat, loc=(0, 0, 0), olcek=(1, 1, 1), parent=None, seg=32, halka=16):
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=halka, radius=r)
    me = bpy.data.meshes.new(ad); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(ad, me); bpy.context.scene.collection.objects.link(o)
    me.materials.append(mat); o.location = loc; o.scale = olcek
    for p in me.polygons: p.use_smooth = True
    if parent: o.parent = parent
    return o

def silindir(ad, r, boy, mat, loc=(0, 0, 0), rot=(0, 0, 0), parent=None, seg=24, pah=0.0):
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=boy)
    me = bpy.data.meshes.new(ad); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(ad, me); bpy.context.scene.collection.objects.link(o)
    me.materials.append(mat); o.location = loc; o.rotation_euler = rot
    if parent: o.parent = parent
    for p in me.polygons: p.use_smooth = True
    if pah:
        b = o.modifiers.new("pah", "BEVEL"); b.width = pah; b.segments = 3; b.limit_method = "ANGLE"
    return o

def simit(ad, R, r, mat, loc=(0, 0, 0), rot=(0, 0, 0), parent=None):
    bm = bmesh.new()
    V, F = [], []
    n1, n2 = 48, 12
    for i in range(n1):
        a = 2 * math.pi * i / n1
        for j in range(n2):
            b = 2 * math.pi * j / n2
            V.append(((R + r * math.cos(b)) * math.cos(a), (R + r * math.cos(b)) * math.sin(a), r * math.sin(b)))
    for i in range(n1):
        for j in range(n2):
            F.append((i * n2 + j, ((i + 1) % n1) * n2 + j, ((i + 1) % n1) * n2 + (j + 1) % n2, i * n2 + (j + 1) % n2))
    bm.free()
    o = mesh_obj(ad, V, F, mat, parent); o.location = loc; o.rotation_euler = rot
    return o

def metatop(ad, toplar, mat, parent=None, coz=0.06):
    """toplar: [(x,y,z,r)] -> metaball -> mesh (bulut, toz, saç)."""
    mb = bpy.data.metaballs.new(ad); mb.resolution = coz; mb.render_resolution = coz
    for (x, y, z, r) in toplar:
        e = mb.elements.new(); e.co = (x, y, z); e.radius = r
    tmp = bpy.data.objects.new(ad + "_mb", mb); bpy.context.scene.collection.objects.link(tmp)
    dg = bpy.context.evaluated_depsgraph_get(); dg.update()
    me = bpy.data.meshes.new_from_object(tmp.evaluated_get(dg))
    bpy.data.objects.remove(tmp); bpy.data.metaballs.remove(mb)
    o = bpy.data.objects.new(ad, me); bpy.context.scene.collection.objects.link(o)
    me.materials.clear(); me.materials.append(mat)
    for p in me.polygons: p.use_smooth = True
    if parent: o.parent = parent
    return o

# ---------------------------------------------------------------- yüz (çıkartma) sistemi
# Her yüz parçası iki eğriyle tanımlı şerit: ust[K], alt[K] (yüz düzleminde u sağ, v yukarı).
# Tüm ifadeler aynı köşe sayısını kullanır -> ifade = şekil anahtarı; ara kareler kendiliğinden ara-değerlenir.
K = 28; SATIR = 5

def _rot(p, c, a):
    x, y = p[0] - c[0], p[1] - c[1]; ca, sa = math.cos(a), math.sin(a)
    return (c[0] + x * ca - y * sa, c[1] + x * sa + y * ca)

def elips(cx, cy, rx, ry, aci=0.0):
    ust, alt = [], []
    for i in range(K):
        t = math.pi * (1 - i / (K - 1))
        ust.append(_rot((cx + rx * math.cos(t), cy + ry * math.sin(t)), (cx, cy), aci))
        alt.append(_rot((cx + rx * math.cos(t), cy - ry * math.sin(t)), (cx, cy), aci))
    return ust, alt

def nokta(cx, cy):
    return [(cx, cy)] * K, [(cx, cy)] * K

def bez(p0, p1, p2):
    return lambda t: ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])

def serit(egri, w, uc=0.35):
    """Fırça darbesi: eğri boyunca w kalınlık, uçlarda incelir (uc: 0=düz, 1=sivri)."""
    ust, alt = [], []
    for i in range(K):
        t = i / (K - 1); p = egri(t)
        p1 = egri(min(1, t + 1e-3)); p0 = egri(max(0, t - 1e-3))
        tx, ty = p1[0] - p0[0], p1[1] - p0[1]; n = math.hypot(tx, ty) or 1
        nx, ny = -ty / n, tx / n
        ww = w * (max(0.0, math.sin(math.pi * t)) ** uc) / 2
        ust.append((p[0] + nx * ww, p[1] + ny * ww)); alt.append((p[0] - nx * ww, p[1] - ny * ww))
    return ust, alt

def agiz(cx, cy, gen, ust_f, alt_f):
    """ust_f, alt_f: s∈[-1,1] -> dikey konum (cy'ye göre)."""
    ust, alt = [], []
    for i in range(K):
        s = -1 + 2 * i / (K - 1)
        ust.append((cx + s * gen / 2, cy + ust_f(s))); alt.append((cx + s * gen / 2, cy + alt_f(s)))
    return ust, alt

def sisir(sekil, w):
    """Şekli dışa doğru w kadar büyütür (çizgi/kontur katmanı)."""
    ust, alt = sekil
    cx = sum(p[0] for p in ust + alt) / (2 * K); cy = sum(p[1] for p in ust + alt) / (2 * K)
    def it(p, yon):
        dx, dy = p[0] - cx, p[1] - cy; n = math.hypot(dx, dy) or 1
        return (p[0] + dx / n * w, p[1] + dy / n * w)
    # şerit kalınlığı yönü: üst eğri yukarı, alt aşağı; uçlarda yatay
    u2, a2 = [], []
    for i in range(K):
        pu, pa = ust[i], alt[i]
        vx, vy = pu[0] - pa[0], pu[1] - pa[1]; n = math.hypot(vx, vy)
        if n < 1e-4:
            # sivri uç: merkeze göre dışa it
            u2.append(it(pu, 1)); a2.append(it(pa, -1))
        else:
            k = 1.0 if i in (0, K - 1) else 1.0
            u2.append((pu[0] + vx / n * w * k, pu[1] + vy / n * w * k)); a2.append((pa[0] - vx / n * w * k, pa[1] - vy / n * w * k))
    return u2, a2

def ic_bolge(sekil, kesir_ust, kesir_alt, tumsek=0.0):
    """Ağız içinde alt (dil) ya da üst (diş) bölge: her sütunda ust-alt arasının bir dilimi."""
    ust, alt = sekil; u2, a2 = [], []
    for i in range(K):
        s = -1 + 2 * i / (K - 1); b = (1 - s * s) ** 0.5
        pu, pa = ust[i], alt[i]
        f1 = kesir_ust + tumsek * b; f0 = kesir_alt
        u2.append((pa[0] + (pu[0] - pa[0]) * f1, pa[1] + (pu[1] - pa[1]) * f1))
        a2.append((pa[0] + (pu[0] - pa[0]) * f0, pa[1] + (pu[1] - pa[1]) * f0))
    return u2, a2

class Yuzey:
    """Torna gövde yüzeyi: eksen X (zeplin, roket) ya da Z (balon, kafa). Yüz -Y yönüne bakar."""
    def __init__(self, rf, eksen="Z", merkez=(0, 0, 0), h=1e-3):
        self.rf, self.eksen, self.c, self.h = rf, eksen, Vector(merkez), h
    def nokta(self, u, v, ofset):
        if self.eksen == "Z":
            a, q = v, u  # eksen boyu = v (yerel z), kesit içi = u
        else:
            a, q = u, v
        r = self.rf(a); y = -math.sqrt(max(r * r - q * q, 1e-6))
        dr = (self.rf(a + self.h) - self.rf(a - self.h)) / (2 * self.h)
        if self.eksen == "Z":
            p = Vector((q, y, a)); n = Vector((q, y, -r * dr))
        else:
            p = Vector((a, y, q)); n = Vector((-r * dr, y, q))
        n.normalize()
        return self.c + p + n * ofset

def cikartma(ad, yuzey, ifadeler, mat, katman, parent, kubbe=0.0, birim=0.004):
    """ifadeler: {ad: (ust,alt)}; ilk anahtar temel. Parçayı yüzeye oturtur, ifade başına şekil anahtarı ekler."""
    adlar = list(ifadeler.keys())
    def koseler(sek):
        ust, alt = sek; V = []
        for r in range(SATIR + 1):
            f = r / SATIR
            for i in range(K):
                u = ust[i][0] * (1 - f) + alt[i][0] * f; v = ust[i][1] * (1 - f) + alt[i][1] * f
                bomb = kubbe * math.sin(math.pi * f) * math.sin(math.pi * i / (K - 1))
                V.append(yuzey.nokta(u, v, katman * birim + bomb))
        return V
    F = []
    for r in range(SATIR):
        for i in range(K - 1):
            a = r * K + i
            F.append((a, a + K, a + K + 1, a + 1))
    o = mesh_obj(ad, koseler(ifadeler[adlar[0]]), F, mat, parent)
    o.shape_key_add(name="Basis", from_mix=False)
    for n in adlar:
        kb = o.shape_key_add(name=n, from_mix=False)
        for j, co in enumerate(koseler(ifadeler[n])): kb.data[j].co = co
    o.visible_shadow = False
    return o

def ifade_sec(kok, ad, kare=None):
    """kok altındaki tüm çıkartmalarda 'ad' şekil anahtarını 1, diğerlerini 0 yapar; kare verilirse anahtar kare ekler."""
    for o in alt_nesneler(kok):
        sk = o.data.shape_keys if o.type == "MESH" else None
        if not sk: continue
        for kb in sk.key_blocks[1:]:
            kb.value = 1.0 if kb.name == ad else 0.0
            if kare is not None: kb.keyframe_insert("value", frame=kare)

def alt_nesneler(kok):
    out = [kok]
    for c in kok.children: out += alt_nesneler(c)
    return out

# ---------------------------------------------------------------- render
def goster(kokler):
    izin = set()
    for k in kokler:
        for o in alt_nesneler(k): izin.add(o.name)
    for o in bpy.context.scene.objects:
        if o.type in ("LIGHT", "CAMERA"): continue
        o.hide_render = (o.name not in izin) or bool(o.get("gizli"))

def sinir(kokler):
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    xs, zs = [], []
    for k in kokler:
        for o in alt_nesneler(k):
            if o.type != "MESH" or o.hide_render: continue
            oe = o.evaluated_get(dg)
            for c in oe.bound_box:
                w = oe.matrix_world @ Vector(c); xs.append(w.x); zs.append(w.z)
    return min(xs), max(xs), min(zs), max(zs)

def cek(kokler, dosya, gen_px, pay=0.07, cerceve=None, ornek=64):
    """Ortografik yan görünüş render. cerceve=(x0,x1,z0,z1) verilmezse sınırdan hesaplanır."""
    s = bpy.context.scene; goster(kokler)
    x0, x1, z0, z1 = cerceve or sinir(kokler)
    w, h = x1 - x0, z1 - z0; m = max(w, h) * pay
    x0 -= m; x1 += m; z0 -= m; z1 += m; w, h = x1 - x0, z1 - z0
    s.render.resolution_x = gen_px; s.render.resolution_y = max(8, int(round(gen_px * h / w / 2)) * 2)
    cam = s.camera; cam.data.ortho_scale = max(w, h)
    cam.location = ((x0 + x1) / 2, -40, (z0 + z1) / 2)
    s.cycles.samples = ornek
    s.render.filepath = dosya if dosya.endswith(".png") else os.path.join(HAM, dosya + ".png")
    import time; t = time.time()
    bpy.ops.render.render(write_still=True)
    sure = time.time() - t
    print(f"[render] {os.path.basename(s.render.filepath)} {s.render.resolution_x}x{s.render.resolution_y} {ornek} örnek {sure:.1f} sn", flush=True)
    with open(os.path.join(HAM, "_sureler.txt"), "a") as f:
        f.write(f"{os.path.basename(s.render.filepath)}\t{s.render.resolution_x}x{s.render.resolution_y}\t{ornek}\t{sure:.1f}\n")
    return (x0, x1, z0, z1)
