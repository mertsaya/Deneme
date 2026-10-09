# Son Durak: Plüton — tarz denemeleri. Aynı anı (roket ~12 km'de, altında bulut tabakası ve Dünya) üç farklı tarzda çizer.
# Çalıştır: blender -b --factory-startup -P oyun/blender/tarz_karesi.py -- <sinematik|mobil|minyatur> [örnek_sayısı]
# Çıktı: oyun/blender/kareler/<tarz>.png (telefon dikey: 720×1280). Roket roket.blend'den alınır (önce roket.py çalıştır).
import bpy, math, os, sys
from mathutils import Vector

TARZ = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "sinematik"
ORNEK = int(sys.argv[sys.argv.index("--") + 2]) if "--" in sys.argv and len(sys.argv) > sys.argv.index("--") + 2 else 96
KOK = os.path.dirname(os.path.abspath(__file__))
A0 = os.path.join(KOK, "..", "a0")
CIKTI = os.path.join(KOK, "kareler", TARZ + ".png")
os.makedirs(os.path.dirname(CIKTI), exist_ok=True)

sc = bpy.context.scene
for ob in list(bpy.data.objects): bpy.data.objects.remove(ob)

# ---------------------------------------------------------------- yardımcılar
def dugum_mat(ad):
    m = bpy.data.materials.new(ad); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    return m, nt, nt.nodes.new("ShaderNodeOutputMaterial")

def bsdf_mat(ad, renk, puruz=0.5, metal=0.0, kaplama=0.0, sss=0.0):
    m, nt, out = dugum_mat(ad)
    b = nt.nodes.new("ShaderNodeBsdfPrincipled")
    b.inputs["Base Color"].default_value = (*renk, 1); b.inputs["Roughness"].default_value = puruz; b.inputs["Metallic"].default_value = metal
    for ad_, v in (("Coat Weight", kaplama), ("Subsurface Weight", sss)):
        if ad_ in b.inputs: b.inputs[ad_].default_value = v
    nt.links.new(b.outputs[0], out.inputs["Surface"])
    return m

def resim(yol):
    return bpy.data.images.load(os.path.abspath(yol), check_existing=True)

def gok_doku(tur_listesi, **ayar):
    """Blender sürümüne göre gökyüzü dokusunu kur (5.x'te türlerin adları değişti)."""
    w = bpy.data.worlds.new("Gok"); sc.world = w; w.use_nodes = True
    nt = w.node_tree; nt.nodes.clear()
    sky = nt.nodes.new("ShaderNodeTexSky")
    for tur in tur_listesi:
        try: sky.sky_type = tur; break
        except Exception: pass
    for k, v in ayar.items():
        try: setattr(sky, k, v)
        except Exception: pass
    bg = nt.nodes.new("ShaderNodeBackground"); out = nt.nodes.new("ShaderNodeOutputWorld")
    nt.links.new(sky.outputs[0], bg.inputs[0]); nt.links.new(bg.outputs[0], out.inputs[0])
    return w, nt, bg

def gradyan_gok(alt, ust, guc=1.0, kamera_guc=None):
    """Kameradan görünen gök: aşağıdan yukarı iki renk; aydınlatmaya da aynı renkler katkı verir."""
    w = bpy.data.worlds.new("Gok"); sc.world = w; w.use_nodes = True
    nt = w.node_tree; nt.nodes.clear()
    # bakış yönü = −Incoming; z'si ufukta 0, tepede 1
    geo = nt.nodes.new("ShaderNodeNewGeometry"); sep = nt.nodes.new("ShaderNodeSeparateXYZ"); ters = nt.nodes.new("ShaderNodeMath"); ters.operation = "MULTIPLY"; ters.inputs[1].default_value = -1
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    nt.links.new(geo.outputs["Incoming"], sep.inputs[0]); nt.links.new(sep.outputs["Z"], ters.inputs[0]); nt.links.new(ters.outputs[0], ramp.inputs[0])
    ramp.color_ramp.elements[0].position = 0.0; ramp.color_ramp.elements[0].color = (*alt, 1)
    ramp.color_ramp.elements[1].position = 0.45; ramp.color_ramp.elements[1].color = (*ust, 1)
    bg = nt.nodes.new("ShaderNodeBackground"); bg.inputs[1].default_value = guc; out = nt.nodes.new("ShaderNodeOutputWorld")
    nt.links.new(ramp.outputs[0], bg.inputs[0])
    if kamera_guc is None: nt.links.new(bg.outputs[0], out.inputs[0]); return
    # kamera parlak göğü görür, sahneyi ise daha az gök ışığı aydınlatır
    bg2 = nt.nodes.new("ShaderNodeBackground"); bg2.inputs[1].default_value = kamera_guc; nt.links.new(ramp.outputs[0], bg2.inputs[0])
    lp = nt.nodes.new("ShaderNodeLightPath"); mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lp.outputs["Is Camera Ray"], mix.inputs[0]); nt.links.new(bg.outputs[0], mix.inputs[1]); nt.links.new(bg2.outputs[0], mix.inputs[2]); nt.links.new(mix.outputs[0], out.inputs[0])

def gunes(yukseklik_derece, yon_derece, guc, renk=(1, 0.96, 0.9), aci=0.5):
    d = bpy.data.lights.new("Gunes", "SUN"); d.energy = guc; d.color = renk; d.angle = math.radians(aci)
    o = bpy.data.objects.new("Gunes", d); sc.collection.objects.link(o)
    o.rotation_euler = (math.radians(90 - yukseklik_derece), 0, math.radians(yon_derece))
    return o

def kamera(konum, hedef, lens=35, odak=None, fstop=None):
    c = bpy.data.cameras.new("Kamera"); c.lens = lens; c.clip_start = 0.5; c.clip_end = 3e6
    o = bpy.data.objects.new("Kamera", c); sc.collection.objects.link(o); sc.camera = o
    o.location = konum; o.rotation_euler = (Vector(hedef) - Vector(konum)).to_track_quat("-Z", "Y").to_euler()
    if odak:
        c.dof.use_dof = True; c.dof.focus_distance = odak; c.dof.aperture_fstop = fstop
    return o

# ---------------------------------------------------------------- roket (roket.blend'den)
def roket_yukle(olcek=1.0, sisman=1.0):
    with bpy.data.libraries.load(os.path.join(KOK, "roket.blend")) as (kaynak, hedef):
        hedef.objects = kaynak.objects
    kok = bpy.data.objects.new("Roket", None); sc.collection.objects.link(kok)
    for o in hedef.objects:
        if o is None or o.type != "MESH": continue
        sc.collection.objects.link(o); o.parent = kok
        for p in o.data.polygons: p.use_smooth = True
    kok.scale = (olcek * sisman, olcek * sisman, olcek)
    return kok, [o for o in hedef.objects if o and o.type == "MESH"]

def alev(kok, uzun, genis, renkler, guc):
    """Meme altındaki alev: koni, uca doğru sönen ışıma (Cycles'ta kendisi ışık kaynağıdır)."""
    bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=genis, radius2=0.7, depth=uzun, location=(0, 0, -21.9 - uzun / 2))
    o = bpy.context.active_object; o.name = "Alev"; o.parent = kok
    m, nt, out = dugum_mat("Alev")
    tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ"); ramp = nt.nodes.new("ShaderNodeValToRGB")
    nt.links.new(tc.outputs["Generated"], sep.inputs[0]); nt.links.new(sep.outputs["Z"], ramp.inputs[0])
    els = ramp.color_ramp.elements; els[0].position = 0.0; els[0].color = (*renkler[-1], 1); els[1].position = 1.0; els[1].color = (*renkler[0], 1)
    for i, r in enumerate(renkler[1:-1]): e = els.new(0.85 - i * 0.3); e.color = (*r, 1)
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[1].default_value = guc
    sat = nt.nodes.new("ShaderNodeBsdfTransparent"); mix = nt.nodes.new("ShaderNodeMixShader")
    pw = nt.nodes.new("ShaderNodeMath"); pw.operation = "POWER"; pw.inputs[1].default_value = 1.8
    nt.links.new(ramp.outputs[0], em.inputs[0]); nt.links.new(sep.outputs["Z"], pw.inputs[0])
    nt.links.new(pw.outputs[0], mix.inputs[0]); nt.links.new(sat.outputs[0], mix.inputs[1]); nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    o.data.materials.append(m)
    return o

def renk_degistir(parcalar, tablo):
    for o in parcalar:
        for i, m in enumerate(o.data.materials):
            if m and m.name.split(".")[0] in tablo: o.data.materials[i] = tablo[m.name.split(".")[0]]

# ---------------------------------------------------------------- yer ve bulut (sinematik ve mobil)
H = 12000.0                                                    # roketin irtifası: yer z = −H
def yer(doku_yolu, parlaklik=1.0, doygunluk=1.0):
    """NASA bölge görüntüsü (24–46° D, 28–44° K) gerçek boyutunda bir düzlem; üs (33,85° D, 36,25° K) roketin tam altında."""
    gx, gy = 22 * math.cos(math.radians(36)) * 111e3, 16 * 111e3
    bpy.ops.mesh.primitive_plane_add(size=1, location=((35 - 33.85) * math.cos(math.radians(36)) * 111e3, (36 - 36.25) * 111e3, -H))
    o = bpy.context.active_object; o.name = "Yer"; o.scale = (gx, gy, 1)
    m, nt, out = dugum_mat("Yer")
    tx = nt.nodes.new("ShaderNodeTexImage"); tx.image = resim(doku_yolu); tx.interpolation = "Cubic"
    hsv = nt.nodes.new("ShaderNodeHueSaturation"); hsv.inputs["Saturation"].default_value = doygunluk; hsv.inputs["Value"].default_value = parlaklik
    b = nt.nodes.new("ShaderNodeBsdfPrincipled"); b.inputs["Roughness"].default_value = 0.9
    nt.links.new(tx.outputs[0], hsv.inputs["Color"]); nt.links.new(hsv.outputs[0], b.inputs["Base Color"]); nt.links.new(b.outputs[0], out.inputs["Surface"])
    o.data.materials.append(m)
    return o

def hacim_bulut(z0, z1, alan, yogunluk, olcek, esik):
    """Gerçek hacimli bulut tabakası (Cycles): gürültüyle şekillenen yoğunluk."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, (z0 + z1) / 2))
    o = bpy.context.active_object; o.name = "Bulutlar"; o.scale = (alan, alan, z1 - z0)
    m, nt, out = dugum_mat("Bulut")
    tc = nt.nodes.new("ShaderNodeTexCoord"); mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (1 / olcek, 1 / olcek, 1 / (olcek * 0.35))
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 1.0; nz.inputs["Detail"].default_value = 6; nz.inputs["Roughness"].default_value = 0.5
    nt.links.new(tc.outputs["Object"], mp.inputs[0]); mp.inputs["Location"].default_value = (0, 0, 0)
    # nesne koordinatı −0,5…0,5 → dünya ölçeğine
    mp2 = nt.nodes.new("ShaderNodeVectorMath"); mp2.operation = "MULTIPLY"; mp2.inputs[1].default_value = (alan, alan, z1 - z0)
    nt.links.new(tc.outputs["Object"], mp2.inputs[0]); nt.links.new(mp2.outputs[0], mp.inputs[0]); nt.links.new(mp.outputs[0], nz.inputs[0])
    # yükseklikle incelen tabaka (alt ve üst kenar yumuşak)
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Object"], sep.inputs[0])
    kat = nt.nodes.new("ShaderNodeMapRange"); kat.inputs[1].default_value = -0.5; kat.inputs[2].default_value = 0.5; kat.inputs[3].default_value = 0; kat.inputs[4].default_value = 1
    nt.links.new(sep.outputs["Z"], kat.inputs[0])
    tepe = nt.nodes.new("ShaderNodeFloatCurve")
    c = tepe.mapping.curves[0]; c.points[0].location = (0, 0); c.points[1].location = (1, 0); c.points.new(0.25, 1); c.points.new(0.55, 0.85)
    nt.links.new(kat.outputs[0], tepe.inputs["Value"])
    carp = nt.nodes.new("ShaderNodeMath"); carp.operation = "MULTIPLY"; nt.links.new(nz.outputs[0], carp.inputs[0]); nt.links.new(tepe.outputs[0], carp.inputs[1])
    yog = nt.nodes.new("ShaderNodeMapRange"); yog.inputs[1].default_value = esik; yog.inputs[2].default_value = esik + 0.12; yog.inputs[3].default_value = 0; yog.inputs[4].default_value = yogunluk
    nt.links.new(carp.outputs[0], yog.inputs[0])
    v = nt.nodes.new("ShaderNodeVolumePrincipled"); v.inputs["Color"].default_value = (1, 1, 1, 1)
    if "Anisotropy" in v.inputs: v.inputs["Anisotropy"].default_value = 0.6
    nt.links.new(yog.outputs[0], v.inputs["Density"]); nt.links.new(v.outputs[0], out.inputs["Volume"])
    o.data.materials.append(m)
    return o

def puf_bulut(merkezler, renk_ust, renk_alt, olcek=1.0):
    """Mobil tarz: kabarık, yumuşak gölgeli bulut kümeleri (her küme birkaç küre)."""
    import random; random.seed(4)
    m, nt, out = dugum_mat("PufBulut")
    b = nt.nodes.new("ShaderNodeBsdfPrincipled"); b.inputs["Roughness"].default_value = 0.85
    if "Subsurface Weight" in b.inputs: b.inputs["Subsurface Weight"].default_value = 0.35; b.inputs["Subsurface Radius"].default_value = (300, 300, 300)
    tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ"); ramp = nt.nodes.new("ShaderNodeValToRGB")
    nt.links.new(tc.outputs["Normal"], sep.inputs[0]); nt.links.new(sep.outputs["Z"], ramp.inputs[0])
    ramp.color_ramp.elements[0].position = 0.35; ramp.color_ramp.elements[0].color = (*renk_alt, 1); ramp.color_ramp.elements[1].position = 0.75; ramp.color_ramp.elements[1].color = (*renk_ust, 1)
    nt.links.new(ramp.outputs[0], b.inputs["Base Color"]); nt.links.new(b.outputs[0], out.inputs["Surface"])
    for (cx, cy, cz, r) in merkezler:
        for k in range(7):
            rr = r * (0.45 + random.random() * 0.55) * olcek
            bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=rr, location=(cx + (random.random() - 0.5) * r * 1.6, cy + (random.random() - 0.5) * r * 1.6, cz + random.random() * r * 0.35))
            o = bpy.context.active_object; o.scale.z = 0.62; o.data.materials.append(m)
            for p in o.data.polygons: p.use_smooth = True

def duman_izi(kok, uzunluk, r0, r1, renk, adet=26, opak=False):
    """Roketin arkasındaki egzoz izi: genişleyen kabarık bulutçuklar."""
    import random; random.seed(9)
    m, nt, out = dugum_mat("Duman")
    b = nt.nodes.new("ShaderNodeBsdfPrincipled"); b.inputs["Base Color"].default_value = (*renk, 1); b.inputs["Roughness"].default_value = 0.95
    if not opak and "Transmission Weight" in b.inputs: pass
    nt.links.new(b.outputs[0], out.inputs["Surface"])
    for i in range(adet):
        u = i / (adet - 1); z = -24 - u * uzunluk; r = r0 + (r1 - r0) * u
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=r * (0.8 + random.random() * 0.4), location=((random.random() - 0.5) * r * 0.5, (random.random() - 0.5) * r * 0.5, z))
        o = bpy.context.active_object; o.parent = kok; o.data.materials.append(m)
        for p in o.data.polygons: p.use_smooth = True

def hacim_iz(kok, uzunluk, r0, r1, yogunluk):
    """Sinematik egzoz izi: genişleyen, uca doğru seyrelen hacimli duman konisi."""
    bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=r1, radius2=r0, depth=uzunluk, location=(0, 0, -24 - uzunluk / 2))
    o = bpy.context.active_object; o.name = "Iz"; o.parent = kok
    m, nt, out = dugum_mat("Iz")
    tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 6; nz.inputs["Detail"].default_value = 6
    nt.links.new(tc.outputs["Object"], nz.inputs[0])
    seyrel = nt.nodes.new("ShaderNodeMath"); seyrel.operation = "POWER"; seyrel.inputs[1].default_value = 2.0; nt.links.new(sep.outputs["Z"], seyrel.inputs[0])
    c1 = nt.nodes.new("ShaderNodeMath"); c1.operation = "MULTIPLY"; nt.links.new(seyrel.outputs[0], c1.inputs[0]); nt.links.new(nz.outputs[0], c1.inputs[1])
    c2 = nt.nodes.new("ShaderNodeMath"); c2.operation = "MULTIPLY"; c2.inputs[1].default_value = yogunluk; nt.links.new(c1.outputs[0], c2.inputs[0])
    v = nt.nodes.new("ShaderNodeVolumePrincipled"); v.inputs["Color"].default_value = (0.95, 0.95, 0.95, 1)
    nt.links.new(c2.outputs[0], v.inputs["Density"]); nt.links.new(v.outputs[0], out.inputs["Volume"])
    o.data.materials.append(m)

def cycles(ornek, gurultu_azalt=True):
    sc.render.engine = "CYCLES"; cy = sc.cycles; cy.samples = ornek; cy.use_denoising = gurultu_azalt
    try:
        pref = bpy.context.preferences.addons["cycles"].preferences
        for tur in ("OPTIX", "CUDA"):
            try: pref.compute_device_type = tur; pref.get_devices(); break
            except Exception: pass
        for d in pref.devices: d.use = True
        cy.device = "GPU"
    except Exception as e: print("GPU yok:", e)
    cy.volume_step_rate = 4.0; cy.max_bounces = 6

def isima(esik=1.0, guc=0.6, boyut=7):
    """Parlak yerlere hafif ışıma (alev, güneş)."""
    sc.use_nodes = True
    nt = sc.node_tree if hasattr(sc, "node_tree") and sc.node_tree else None
    if nt is None:
        try:
            g = bpy.data.node_groups.new("Bilesim", "CompositorNodeTree"); sc.compositing_node_group = g; nt = g
        except Exception as e: print("bileşim yok:", e); return
    nt.nodes.clear()
    rl = nt.nodes.new("CompositorNodeRLayers"); gl = nt.nodes.new("CompositorNodeGlare")
    for k, v in (("glare_type", "BLOOM"), ("glare_type", "FOG_GLOW"), ("threshold", esik), ("mix", guc - 1), ("size", boyut)):
        try: setattr(gl, k, v)
        except Exception: pass
    try:
        out = nt.nodes.new("CompositorNodeComposite")
    except Exception:
        out = nt.nodes.new("NodeGroupOutput"); nt.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    nt.links.new(rl.outputs["Image"], gl.inputs[0]); nt.links.new(gl.outputs[0], out.inputs[0])

sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 720, 1280, 100
sc.render.film_transparent = False
try: sc.view_settings.view_transform = "AgX"
except Exception: pass

# ================================================================ TARZLAR
if TARZ == "sinematik":
    # Film gibi: fiziksel gökyüzü, gerçek hacimli bulutlar, NASA yer görüntüsü, ışık saçan alev, hafif sis
    cycles(ORNEK)
    gok_doku(["MULTIPLE_SCATTERING", "NISHITA", "SINGLE_SCATTERING", "HOSEK_WILKIE"], sun_elevation=math.radians(24), sun_rotation=math.radians(205),
             altitude=H, air_density=1.0, dust_density=1.2, aerosol_density=1.2, ozone_density=1.0, sun_intensity=0.6)
    gunes(24, 205, 2.4)
    kok, parca = roket_yukle()
    kok.rotation_euler = (0, math.radians(14), 0)
    alev(kok, 30, 4.2, [(1, 0.97, 0.88), (1, 0.75, 0.38), (1, 0.42, 0.12), (0.6, 0.12, 0.04)], 40)
    hacim_iz(kok, 1400, 3.5, 110, 0.018)
    yer(os.path.join(A0, "bolge.jpg"), parlaklik=0.9)
    hacim_bulut(-H + 1800, -H + 3600, 160000, 0.02, 9000, 0.52)
    sc.view_settings.exposure = -1.4
    try: sc.view_settings.look = "AgX - Medium High Contrast"
    except Exception: pass
    kamera((52, -96, 18), (6, 0, -4), lens=32)

elif TARZ == "mobil":
    # Parlak mobil oyun: tok ve doygun renkler, cilalı boya, hafif tombul roket, kabarık bulutlar, temiz gök
    cycles(max(32, ORNEK // 2))
    gradyan_gok((0.55, 0.85, 1.0), (0.07, 0.32, 0.85), 0.35, 1.1)
    sc.view_settings.view_transform = "Standard"                 # AgX doygun renkleri soldurur; mobil tarzda tok renk istiyoruz
    sc.view_settings.exposure = -0.3
    gunes(34, 205, 6.0, (1, 0.95, 0.85), 2.5)
    kok, parca = roket_yukle(1.0, 1.18)
    kok.rotation_euler = (0, math.radians(14), 0)
    renk_degistir(parca, {
        "Boya_Beyaz": bsdf_mat("M_Beyaz", (0.95, 0.94, 0.9), 0.25, kaplama=0.8),
        "Boya_KirikBeyaz": bsdf_mat("M_Krem", (0.98, 0.82, 0.45), 0.3, kaplama=0.8),
        "Karbon_Siyah": bsdf_mat("M_Lacivert", (0.04, 0.09, 0.28), 0.3, kaplama=0.6),
        "Serit_Turuncu": bsdf_mat("M_Kirmizi", (0.9, 0.08, 0.05), 0.3, kaplama=0.8),
        "Metal_Gri": bsdf_mat("M_Gri", (0.6, 0.65, 0.72), 0.25, 0.7),
        "Nozul_Isil": bsdf_mat("M_Nozul", (0.35, 0.18, 0.1), 0.35, 0.9)})
    alev(kok, 26, 4.6, [(1, 1, 0.75), (1, 0.85, 0.2), (1, 0.45, 0.05), (0.95, 0.15, 0.05)], 25)
    duman_izi(kok, 380, 3, 22, (1, 1, 1), adet=34)
    yer(os.path.join(A0, "harita.png").replace("harita.png", "bolge_harita.png"), parlaklik=1.05, doygunluk=1.15)
    puf_bulut([(x * 2400 + 1200 * (i % 2), y * 2400, -H + 2600 + (i % 3) * 200, 900) for i, (x, y) in enumerate((a, b) for a in range(-4, 5) for b in range(-2, 9))],
              (1, 1, 1), (0.62, 0.75, 0.95))
    kamera((52, -96, 18), (6, 0, -4), lens=32)
    isima(0.9, 0.5, 8)

elif TARZ == "minyatur":
    # Minyatür: oyuncak bir küre ve ondan kalkan küçük roket; yumuşak stüdyo ışığı, güçlü alan derinliği (tilt-shift)
    cycles(ORNEK)
    gradyan_gok((0.05, 0.06, 0.16), (0.01, 0.01, 0.04), 0.6)
    R = 60.0
    bpy.ops.mesh.primitive_uv_sphere_add(segments=128, ring_count=64, radius=R, location=(0, 0, -R - 8))
    kure = bpy.context.active_object; kure.name = "Kure"
    for p in kure.data.polygons: p.use_smooth = True
    m, nt, out = dugum_mat("Kure")
    tc = nt.nodes.new("ShaderNodeTexCoord"); tx = nt.nodes.new("ShaderNodeTexImage"); tx.image = resim(os.path.join(A0, "harita.png")); tx.projection = "SPHERE"
    nt.links.new(tc.outputs["Object"], tx.inputs[0])
    b = nt.nodes.new("ShaderNodeBsdfPrincipled"); b.inputs["Roughness"].default_value = 0.55
    if "Coat Weight" in b.inputs: b.inputs["Coat Weight"].default_value = 0.4
    nt.links.new(tx.outputs[0], b.inputs["Base Color"]); nt.links.new(b.outputs[0], out.inputs["Surface"])
    kure.data.materials.append(m)
    # üs (36° K, 34° D) kürenin tepesinde olsun
    kure.rotation_euler = (math.radians(90 - 36), 0, math.radians(-34 - 90))
    # pamuk bulutlar küre çevresinde
    import random; random.seed(3)
    bm, bnt, bout = dugum_mat("Pamuk")
    bb = bnt.nodes.new("ShaderNodeBsdfPrincipled"); bb.inputs["Base Color"].default_value = (1, 1, 1, 1); bb.inputs["Roughness"].default_value = 1
    if "Subsurface Weight" in bb.inputs: bb.inputs["Subsurface Weight"].default_value = 0.5
    bnt.links.new(bb.outputs[0], bout.inputs["Surface"])
    for i in range(46):
        th, ph = random.random() * 2 * math.pi, random.random() * 0.9
        yon = Vector((math.sin(ph) * math.cos(th), math.sin(ph) * math.sin(th), math.cos(ph)))
        for k in range(4):
            bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=10, radius=1.6 + random.random() * 1.8, location=Vector((0, 0, -R - 8)) + yon * (R + 3.5) + Vector(((random.random() - .5) * 4, (random.random() - .5) * 4, 0)))
            o = bpy.context.active_object; o.scale.z = 0.6; o.data.materials.append(bm)
            for p in o.data.polygons: p.use_smooth = True
    kok, parca = roket_yukle(0.4)
    kok.location = (0, 0, 22); kok.rotation_euler = (0, math.radians(8), 0)
    renk_degistir(parca, {
        "Boya_Beyaz": bsdf_mat("O_Beyaz", (0.93, 0.92, 0.88), 0.45, sss=0.05),
        "Boya_KirikBeyaz": bsdf_mat("O_Krem", (0.9, 0.85, 0.75), 0.5),
        "Karbon_Siyah": bsdf_mat("O_Lacivert", (0.06, 0.08, 0.2), 0.5),
        "Serit_Turuncu": bsdf_mat("O_Kirmizi", (0.85, 0.12, 0.08), 0.45),
        "Metal_Gri": bsdf_mat("O_Gri", (0.55, 0.57, 0.6), 0.4, 0.6),
        "Nozul_Isil": bsdf_mat("O_Nozul", (0.3, 0.2, 0.15), 0.4, 0.8)})
    alev(kok, 20, 3.5, [(1, 0.97, 0.8), (1, 0.7, 0.25), (1, 0.35, 0.08), (0.7, 0.1, 0.03)], 30)
    duman_izi(kok, 70, 3, 14, (0.97, 0.97, 0.98), adet=22)
    # stüdyo ışığı: sıcak ana ışık, serin kenar ışığı
    for ad, konum, guc, renk, boyut in (("Ana", (60, -70, 90), 120000, (1, 0.9, 0.78), 40), ("Kenar", (-70, 60, 40), 60000, (0.6, 0.75, 1), 30)):
        L = bpy.data.lights.new(ad, "AREA"); L.energy = guc; L.color = renk; L.size = boyut
        o = bpy.data.objects.new(ad, L); sc.collection.objects.link(o); o.location = konum
        o.rotation_euler = (Vector((0, 0, 10)) - Vector(konum)).to_track_quat("-Z", "Y").to_euler()
    kamera((48, -78, 30), (0, 0, 14), lens=50, odak=(Vector((48, -78, 30)) - Vector((0, 0, 18))).length, fstop=0.12)
    isima(1.0, 0.45, 7)

sc.render.filepath = CIKTI
bpy.ops.render.render(write_still=True)
print("yazıldı:", CIKTI)
