# Son Durak: Plüton — minyatür tarzı örnek kareler. Boyalı plastik oyuncak dünya, abartılı ölçek, masa üstü kamera.
# Sahne gerçek bir oyuncak boyutunda kurulur (küre yarıçapı 30 cm); böylece alan derinliği gerçek bir makro çekim gibi bulanıklaşır.
# Çalıştır: blender -b --factory-startup -P oyun/blender/minyatur_kareleri.py -- <kalkis|ayrilma|uzay> [örnek_sayısı]
# Çıktı: oyun/blender/kareler/minyatur_<kare>.png (telefon dikey: 720×1280). Roket roket.blend'den alınır.
import bpy, math, os, sys, random
from mathutils import Vector

ARG = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
KARE = ARG[0] if ARG else "kalkis"
ORNEK = int(ARG[1]) if len(ARG) > 1 else 128
KOK = os.path.dirname(os.path.abspath(__file__))
A0 = os.path.join(KOK, "..", "a0")
CIKTI = os.path.join(KOK, "kareler", "minyatur_" + KARE + ".png")
os.makedirs(os.path.dirname(CIKTI), exist_ok=True)

sc = bpy.context.scene
for ob in list(bpy.data.objects): bpy.data.objects.remove(ob)

R = 0.30                  # oyuncak kürenin yarıçapı (m); merkez (0,0,−R), üs kürenin tepesinde (0,0,0)
S = 0.0021                # roket ölçeği: 54 m'lik roket ≈ 11 cm
SISMAN = 1.35             # oyuncak oranı: roket biraz tombul
MERKEZ = Vector((0, 0, -R))

# ---------------------------------------------------------------- yardımcılar
def dugum_mat(ad):
    m = bpy.data.materials.new(ad); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    return m, nt, nt.nodes.new("ShaderNodeOutputMaterial")

def plastik(ad, renk, puruz=0.32, kaplama=0.35, metal=0.0, sss=0.04):
    """Boyalı plastik: hafif parlak, yumuşak yansıma, çok az ışık geçirgenliği."""
    m, nt, out = dugum_mat(ad)
    b = nt.nodes.new("ShaderNodeBsdfPrincipled")
    b.inputs["Base Color"].default_value = (*renk, 1); b.inputs["Roughness"].default_value = puruz; b.inputs["Metallic"].default_value = metal
    for k, v in (("Coat Weight", kaplama), ("Coat Roughness", 0.15), ("Subsurface Weight", sss)):
        if k in b.inputs: b.inputs[k].default_value = v
    if "Subsurface Radius" in b.inputs: b.inputs["Subsurface Radius"].default_value = (0.004, 0.003, 0.002)
    nt.links.new(b.outputs[0], out.inputs["Surface"])
    return m

def isik_mat(ad, renk, guc):
    m, nt, out = dugum_mat(ad)
    e = nt.nodes.new("ShaderNodeEmission"); e.inputs[0].default_value = (*renk, 1); e.inputs[1].default_value = guc
    nt.links.new(e.outputs[0], out.inputs["Surface"])
    return m

def yumusak(o):
    for p in o.data.polygons: p.use_smooth = True
    return o

def kure_ekle(r, konum, mat, seg=32, basik=1.0):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, radius=r, location=konum)
    o = bpy.context.active_object; o.scale.z = basik; o.data.materials.append(mat)
    return yumusak(o)

def yuzey(enlem_derece, boylam_derece, yukseklik=0.0):
    """Üssün olduğu tepe noktasına göre küre yüzeyinde bir nokta (açılar tepe noktasından ölçülür)."""
    t, p = math.radians(enlem_derece), math.radians(boylam_derece)
    yon = Vector((math.sin(t) * math.cos(p), math.sin(t) * math.sin(p), math.cos(t)))
    return MERKEZ + yon * (R + yukseklik), yon

def bak(o, hedef):
    o.rotation_euler = (Vector(hedef) - o.location).to_track_quat("-Z", "Y").to_euler()

def kamera(konum, hedef, lens, odak_nokta=None, fstop=2.8):
    c = bpy.data.cameras.new("Kamera"); c.lens = lens; c.clip_start = 0.005; c.clip_end = 100
    o = bpy.data.objects.new("Kamera", c); sc.collection.objects.link(o); sc.camera = o
    o.location = konum; bak(o, hedef)
    if odak_nokta is not None:
        c.dof.use_dof = True; c.dof.focus_distance = (Vector(odak_nokta) - Vector(konum)).length; c.dof.aperture_fstop = fstop
        c.dof.aperture_blades = 6; c.dof.aperture_rotation = math.radians(10)
    return o

def alan_isigi(ad, konum, hedef, guc, renk, boyut):
    L = bpy.data.lights.new(ad, "AREA"); L.energy = guc; L.color = renk; L.size = boyut; L.shape = "DISK"          # yuvarlak softbox: plastikte yuvarlak parlama
    o = bpy.data.objects.new(ad, L); sc.collection.objects.link(o); o.location = konum; bak(o, hedef)
    return o

# ---------------------------------------------------------------- dünya (oyuncak küre)
def oyuncak_kure():
    bpy.ops.mesh.primitive_uv_sphere_add(segments=192, ring_count=96, radius=R, location=MERKEZ)
    k = yumusak(bpy.context.active_object); k.name = "Kure"
    m, nt, out = dugum_mat("Kure")
    tc = nt.nodes.new("ShaderNodeTexCoord"); tx = nt.nodes.new("ShaderNodeTexImage")
    tx.image = bpy.data.images.load(os.path.abspath(os.path.join(A0, "harita.png")), check_existing=True); tx.projection = "SPHERE"; tx.interpolation = "Cubic"
    nt.links.new(tc.outputs["Object"], tx.inputs[0])
    # kara maskesi: düz renkli haritada su mavi (B > R), kara sıcak tonlu (R ≥ B)
    sep = nt.nodes.new("ShaderNodeSeparateColor"); nt.links.new(tx.outputs[0], sep.inputs[0])
    fark = nt.nodes.new("ShaderNodeMath"); fark.operation = "SUBTRACT"; nt.links.new(sep.outputs[0], fark.inputs[0]); nt.links.new(sep.outputs[2], fark.inputs[1])
    kara = nt.nodes.new("ShaderNodeMapRange"); kara.inputs[1].default_value = -0.02; kara.inputs[2].default_value = 0.0
    nt.links.new(fark.outputs[0], kara.inputs[0])
    # kıtalar boyayla kabartılmış gibi hafif yüksek; su daha parlak, kara daha mat
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.6; bump.inputs["Distance"].default_value = 0.0015
    nt.links.new(kara.outputs[0], bump.inputs["Height"])
    puruz = nt.nodes.new("ShaderNodeMapRange"); puruz.inputs[3].default_value = 0.16; puruz.inputs[4].default_value = 0.5
    nt.links.new(kara.outputs[0], puruz.inputs[0])
    b = nt.nodes.new("ShaderNodeBsdfPrincipled")
    if "Coat Weight" in b.inputs: b.inputs["Coat Weight"].default_value = 0.15
    nt.links.new(tx.outputs[0], b.inputs["Base Color"]); nt.links.new(puruz.outputs[0], b.inputs["Roughness"]); nt.links.new(bump.outputs[0], b.inputs["Normal"])
    nt.links.new(b.outputs[0], out.inputs["Surface"])
    k.data.materials.append(m)
    k.rotation_euler = (math.radians(90 - 36), 0, math.radians(-34 - 90))     # üs (36° K, 34° D) tepede
    return k

def atmosfer(kalinlik=0.045, guc=2.2):
    """Kürenin çevresinde ince, kenarda parlayan mavi hale."""
    bpy.ops.mesh.primitive_uv_sphere_add(segments=128, ring_count=64, radius=R * (1 + kalinlik), location=MERKEZ)
    o = yumusak(bpy.context.active_object); o.name = "Atmosfer"
    m, nt, out = dugum_mat("Atmosfer")
    lw = nt.nodes.new("ShaderNodeLayerWeight"); lw.inputs[0].default_value = 0.5
    us = nt.nodes.new("ShaderNodeMath"); us.operation = "POWER"; us.inputs[1].default_value = 3.0
    nt.links.new(lw.outputs["Facing"], us.inputs[0])
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[0].default_value = (0.35, 0.65, 1.0, 1)
    gc = nt.nodes.new("ShaderNodeMath"); gc.operation = "MULTIPLY"; gc.inputs[1].default_value = guc
    nt.links.new(us.outputs[0], gc.inputs[0]); nt.links.new(gc.outputs[0], em.inputs[1])
    sat = nt.nodes.new("ShaderNodeBsdfTransparent"); top = nt.nodes.new("ShaderNodeAddShader")
    nt.links.new(sat.outputs[0], top.inputs[0]); nt.links.new(em.outputs[0], top.inputs[1]); nt.links.new(top.outputs[0], out.inputs["Surface"])
    o.data.materials.append(m)
    o.visible_shadow = False
    return o

def bulutlar(adet, bos_birak=12.0, tohum=3):
    """Küre üstünde pamuk gibi plastik bulut kümeleri (üssün çevresi boş kalır)."""
    random.seed(tohum)
    mat = plastik("Bulut", (0.97, 0.97, 0.98), puruz=0.6, kaplama=0.0, sss=0.25)
    for _ in range(adet):
        t, p = math.degrees(math.acos(1 - 2 * random.random())), random.random() * 360
        if t < bos_birak: continue
        merkez, yon = yuzey(t, p, 0.012)
        ana = 0.006 + random.random() * 0.006
        for k in range(4 + random.randint(0, 3)):
            sap = Vector(((random.random() - .5), (random.random() - .5), (random.random() - .5))) * ana * 2.2
            sap -= yon * sap.dot(yon)
            o = kure_ekle(ana * (0.55 + random.random() * 0.5), merkez + sap + yon * random.random() * ana * 0.3, mat, 24)
            o.rotation_euler = yon.to_track_quat("Z", "Y").to_euler(); o.scale = (1, 1, 0.62)

def yildizlar(adet=220, tohum=5):
    """Uzak arka planda küçük ışık noktaları; alan derinliğiyle yumuşak altıgen bokehlere dönüşür."""
    random.seed(tohum)
    mats = [isik_mat("Yildiz%d" % i, c, g) for i, (c, g) in enumerate((((1, 0.95, 0.85), 30), ((0.75, 0.85, 1), 25), ((1, 0.8, 0.6), 18)))]
    for _ in range(adet):
        y = Vector((random.gauss(0, 1), random.gauss(0, 1), random.gauss(0, 1))).normalized() * (3 + random.random() * 4)
        o = kure_ekle(0.004 + random.random() * 0.006, y, random.choice(mats), 8)
        o.visible_shadow = False

def gok(alt=(0.035, 0.05, 0.14), ust=(0.006, 0.008, 0.03), guc=1.0):
    w = bpy.data.worlds.new("Gok"); sc.world = w; w.use_nodes = True
    nt = w.node_tree; nt.nodes.clear()
    geo = nt.nodes.new("ShaderNodeNewGeometry"); sep = nt.nodes.new("ShaderNodeSeparateXYZ"); ters = nt.nodes.new("ShaderNodeMath"); ters.operation = "MULTIPLY"; ters.inputs[1].default_value = -1
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    nt.links.new(geo.outputs["Incoming"], sep.inputs[0]); nt.links.new(sep.outputs["Z"], ters.inputs[0]); nt.links.new(ters.outputs[0], ramp.inputs[0])
    ramp.color_ramp.elements[0].position = -0.2; ramp.color_ramp.elements[0].color = (*alt, 1)
    ramp.color_ramp.elements[1].position = 0.6; ramp.color_ramp.elements[1].color = (*ust, 1)
    bg = nt.nodes.new("ShaderNodeBackground"); bg.inputs[1].default_value = guc; out = nt.nodes.new("ShaderNodeOutputWorld")
    nt.links.new(ramp.outputs[0], bg.inputs[0]); nt.links.new(bg.outputs[0], out.inputs[0])

# ---------------------------------------------------------------- roket (oyuncak boya)
KADEME1 = {"Kademe1", "MotorEtegi", "AraKademe", "Serit", "KabloKanali"}
def kademe1_mi(ad):
    ad = ad.split(".")[0]
    return ad in KADEME1 or ad.startswith(("PanelCizgisi_", "Kanatcik_", "Izgara_", "Motor_"))

def roket_yukle():
    with bpy.data.libraries.load(os.path.join(KOK, "roket.blend")) as (kaynak, hedef):
        hedef.objects = kaynak.objects
    BOYA = {
        "Boya_Beyaz": plastik("O_Beyaz", (0.92, 0.91, 0.87)),
        "Boya_KirikBeyaz": plastik("O_Krem", (0.93, 0.86, 0.7)),
        "Karbon_Siyah": plastik("O_Lacivert", (0.04, 0.07, 0.2)),
        "Serit_Turuncu": plastik("O_Turuncu", (0.95, 0.38, 0.06)),
        "Metal_Gri": plastik("O_Gri", (0.62, 0.64, 0.68), puruz=0.3, metal=0.6, kaplama=0.0),
        "Nozul_Isil": plastik("O_Nozul", (0.32, 0.22, 0.17), puruz=0.35, metal=0.8, kaplama=0.0)}
    KIRMIZI = plastik("O_Kirmizi", (0.82, 0.07, 0.05))
    k1 = bpy.data.objects.new("Kademe1Kok", None); k2 = bpy.data.objects.new("RoketKok", None)
    for k in (k1, k2): sc.collection.objects.link(k); k.scale = (S * SISMAN, S * SISMAN, S)
    for o in hedef.objects:
        if o is None or o.type != "MESH": continue
        sc.collection.objects.link(o); yumusak(o)
        o.parent = k1 if kademe1_mi(o.name) else k2
        for i, m in enumerate(o.data.materials):
            if m and m.name.split(".")[0] in BOYA: o.data.materials[i] = BOYA[m.name.split(".")[0]]
        # oyuncak vurgusu: burun ve kanatçıklar kırmızı
        if o.name.split(".")[0] == "Burun" or o.name.startswith("Kanatcik_"): o.data.materials[0] = KIRMIZI
    return k1, k2

def alev(kok, uzun, genis, guc, z_ust=-21.9, r_ust=0.7):
    """Oyuncak alev: sarı çekirdekten turuncu-kırmızıya, uca doğru sönen ışıklı koni (roket biriminde)."""
    bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=genis, radius2=r_ust, depth=uzun, location=(0, 0, z_ust - uzun / 2))
    o = bpy.context.active_object; o.name = "Alev"; o.parent = kok
    m, nt, out = dugum_mat("Alev")
    tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ"); ramp = nt.nodes.new("ShaderNodeValToRGB")
    nt.links.new(tc.outputs["Generated"], sep.inputs[0]); nt.links.new(sep.outputs["Z"], ramp.inputs[0])
    els = ramp.color_ramp.elements
    els[0].position = 0.0; els[0].color = (0.85, 0.12, 0.03, 1); els[1].position = 1.0; els[1].color = (1, 0.97, 0.75, 1)
    e = els.new(0.45); e.color = (1, 0.42, 0.05, 1); e = els.new(0.8); e.color = (1, 0.8, 0.2, 1)
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[1].default_value = guc
    sat = nt.nodes.new("ShaderNodeBsdfTransparent"); mix = nt.nodes.new("ShaderNodeMixShader")
    pw = nt.nodes.new("ShaderNodeMath"); pw.operation = "POWER"; pw.inputs[1].default_value = 1.4
    nt.links.new(ramp.outputs[0], em.inputs[0]); nt.links.new(sep.outputs["Z"], pw.inputs[0])
    nt.links.new(pw.outputs[0], mix.inputs[0]); nt.links.new(sat.outputs[0], mix.inputs[1]); nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    o.data.materials.append(m); o.visible_shadow = False
    return o

def duman(noktalar, tohum=9):
    """Plastik pamuk duman: verilen (konum, yarıçap) listesindeki her noktaya 2–3 top."""
    random.seed(tohum)
    mat = plastik("Duman", (0.95, 0.94, 0.93), puruz=0.7, kaplama=0.0, sss=0.3)
    for (p, r) in noktalar:
        for k in range(2 + random.randint(0, 1)):
            sap = Vector(((random.random() - .5), (random.random() - .5), (random.random() - .5))) * r * 0.9
            kure_ekle(r * (0.65 + random.random() * 0.45), Vector(p) + sap, mat, 24)

def roket_ekseni(kok):
    return (kok.matrix_world.to_3x3().normalized() @ Vector((0, 0, 1))).normalized()

def rampa():
    """Kalkış rampası: gri yuvarlak taban ve kırmızı-beyaz çizgili kule."""
    gri = plastik("Rampa", (0.55, 0.57, 0.6), puruz=0.45); kir = plastik("Kule_K", (0.8, 0.1, 0.06)); bey = plastik("Kule_B", (0.93, 0.92, 0.88))
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.022, depth=0.006, location=(0, 0, 0.001))
    o = yumusak(bpy.context.active_object); o.data.materials.append(gri)
    bpy.ops.object.modifier_add(type="BEVEL"); o.modifiers[-1].width = 0.0015; o.modifiers[-1].segments = 3
    for i in range(7):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.016, 0.0, 0.004 + 0.0075 * i + 0.00375))
        o = bpy.context.active_object; o.scale = (0.006, 0.006, 0.0075); o.data.materials.append(kir if i % 2 == 0 else bey)
        bpy.ops.object.modifier_add(type="BEVEL"); o.modifiers[-1].width = 0.0006; o.modifiers[-1].segments = 2
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.011, 0, 0.04))
    o = bpy.context.active_object; o.scale = (0.008, 0.002, 0.0018); o.data.materials.append(gri)

# ---------------------------------------------------------------- render ayarları
def cycles(ornek):
    sc.render.engine = "CYCLES"; cy = sc.cycles; cy.samples = ornek; cy.use_denoising = True
    try:
        pref = bpy.context.preferences.addons["cycles"].preferences
        for tur in ("OPTIX", "CUDA"):
            try: pref.compute_device_type = tur; pref.get_devices(); break
            except Exception: pass
        for d in pref.devices: d.use = True
        cy.device = "GPU"
    except Exception as e: print("GPU yok:", e)
    cy.max_bounces = 8; cy.transparent_max_bounces = 16

def isima(esik=1.0, guc=0.5, boyut=7):
    sc.use_nodes = True
    nt = sc.node_tree if hasattr(sc, "node_tree") and sc.node_tree else None
    if nt is None:
        try: g = bpy.data.node_groups.new("Bilesim", "CompositorNodeTree"); sc.compositing_node_group = g; nt = g
        except Exception as e: print("bileşim yok:", e); return
    nt.nodes.clear()
    rl = nt.nodes.new("CompositorNodeRLayers"); gl = nt.nodes.new("CompositorNodeGlare")
    for k, v in (("glare_type", "BLOOM"), ("glare_type", "FOG_GLOW"), ("threshold", esik), ("mix", guc - 1), ("size", boyut)):
        try: setattr(gl, k, v)
        except Exception: pass
    try: out = nt.nodes.new("CompositorNodeComposite")
    except Exception:
        out = nt.nodes.new("NodeGroupOutput"); nt.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    nt.links.new(rl.outputs["Image"], gl.inputs[0]); nt.links.new(gl.outputs[0], out.inputs[0])

sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 720, 1280, 100
try:
    sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Punchy"
except Exception: pass
cycles(ORNEK)
gok()
oyuncak_kure()
atmosfer()
yildizlar()
# stüdyo ışığı: sıcak ana ışık sağ üstten, serin kenar ışığı arkadan, zayıf dolgu soldan
alan_isigi("Ana", (0.9, -0.7, 1.0), (0, 0, 0), 24, (1, 0.9, 0.78), 0.6)
alan_isigi("Kenar", (-0.8, 0.9, 0.5), (0, 0, 0), 16, (0.55, 0.72, 1), 0.5)
alan_isigi("Dolgu", (-1.0, -0.9, 0.2), (0, 0, 0), 5, (0.8, 0.85, 1), 1.0)

# ================================================================ KARELER
if KARE == "kalkis":
    # Rampadan yeni ayrılan roket, tabanda kabaran duman; kamera masa başında eğilmiş biri gibi yakından bakar
    bulutlar(70, bos_birak=6)
    rampa()
    k1, k2 = roket_yukle()
    for k in (k1, k2): k.location = (0, 0, 0.004 + 21.9 * S + 0.03)
    alev(k1, 16, 3.0, 26)
    random.seed(2)
    nok = []
    for i in range(26):                                  # rampada yanlara yayılan duman halkası
        a = random.random() * 2 * math.pi; d = 0.012 + random.random() * 0.03
        nok.append(((math.cos(a) * d, math.sin(a) * d, 0.006 + random.random() * 0.006), 0.006 + random.random() * 0.006))
    for i in range(6):                                   # alevin altında yükselen sütun
        nok.append(((0, 0, 0.008 + i * 0.0035), 0.007 - i * 0.0006))
    duman(nok)
    kamera((0.17, -0.24, 0.085), (0, 0, 0.05), 50, odak_nokta=(0, 0, 0.055), fstop=5.6)

elif KARE == "ayrilma":
    # Kademe ayrılması: ilk kademe boşalmış, yavaşça geride kalıp dönüyor; ikinci kademe motorunu ateşliyor
    bulutlar(90, bos_birak=0)
    k1, k2 = roket_yukle()
    egim = math.radians(32)
    k2.location = (0.05, 0, 0.17); k2.rotation_euler = (0, egim, 0)
    eks = Vector((math.sin(egim), 0, math.cos(egim)))
    k1.location = Vector(k2.location) - eks * 0.026 + Vector((0.002, 0.004, 0)); k1.rotation_euler = (math.radians(8), egim + math.radians(14), 0)
    alev(k2, 9, 2.6, 30, z_ust=31.7 - 20.0 - 0.5, r_ust=0.9)
    # ayrılma iticilerinden küçük duman püskürmeleri ve geride kalan ilk kademe izi
    alt = Vector(k1.location) - roket_ekseni(k1) * 22 * S
    duman([(alt - eks * (0.006 + i * 0.007) + Vector((0, 0, -0.002 * i)), 0.003 + i * 0.0012) for i in range(8)], tohum=4)
    hedef = Vector(k2.location) - eks * 0.01
    kamera(hedef + Vector((0.12, -0.25, 0.02)), hedef + Vector((0, 0, -0.03)), 45, odak_nokta=hedef, fstop=6.3)

elif KARE == "uzay":
    # Uzaydan bakış: küre bütünüyle görünür, kalkıştan yörüngeye kesik çizgi; roket küçük, yanında oyuncak Ay
    AZ = float(ARG[2]) if len(ARG) > 2 else -165.0        # kameranın küre çevresindeki açısı (derece); Afrika ve Avrupa görünsün
    bulutlar(150, bos_birak=0)
    k1, k2 = roket_yukle()
    for o in list(k1.children): bpy.data.objects.remove(o)
    sag = AZ + 90                                          # kadrajın sağı
    p, yon = yuzey(30, sag, 0.13)
    k2.location = p; k2.rotation_euler = (0, math.radians(62), math.radians(sag))
    alev(k2, 9, 2.6, 30, z_ust=31.7 - 20.0 - 0.5, r_ust=0.9)
    # yörünge izi: kesik kesik beyaz çizgi (oyuncak harita çizgisi gibi)
    cizgi = plastik("Iz", (1, 0.95, 0.85), puruz=0.4, kaplama=0.0)
    for i in range(46):
        u = i / 45; t = 2 + u * 26; h = 0.004 + 0.122 * (u ** 1.6)
        q, _ = yuzey(t, sag, h)
        if i % 2 == 0: kure_ekle(0.0022, q, cizgi, 12)
    a = math.radians(AZ); ileri = Vector((math.cos(a), math.sin(a), 0)); sagv = Vector((-math.sin(a), math.cos(a), 0))
    kam = kamera(MERKEZ + ileri * 1.19 + Vector((0, 0, 1.05)), (0.03 * sagv.x, 0.03 * sagv.y, -0.2), 40, odak_nokta=(0, 0, -0.05), fstop=8.0)
    # oyuncak Ay: gri, kraterli plastik; kadrajın sol üstünde, kürenin biraz gerisinde
    m, nt, out = dugum_mat("Ay")
    nz = nt.nodes.new("ShaderNodeTexVoronoi"); nz.inputs["Scale"].default_value = 9
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.5; bump.inputs["Distance"].default_value = 0.004
    nt.links.new(nz.outputs["Distance"], bump.inputs["Height"])
    b = nt.nodes.new("ShaderNodeBsdfPrincipled"); b.inputs["Base Color"].default_value = (0.72, 0.71, 0.68, 1); b.inputs["Roughness"].default_value = 0.5
    nt.links.new(bump.outputs[0], b.inputs["Normal"]); nt.links.new(b.outputs[0], out.inputs["Surface"])
    kure_ekle(0.06, MERKEZ - ileri * 0.3 - sagv * 0.22 + Vector((0, 0, 0.42)), m, 96)

sc.render.filepath = CIKTI
bpy.ops.render.render(write_still=True)
print("yazıldı:", CIKTI)
