# Son Durak: Plüton — minyatür (boyalı plastik oyuncak) oyun modelleri.
# Roketi roket.blend'den alır, oyuncak boyasıyla boyar; oyuncak fırlatma kulesi, rampa ve yolcu uçağını üretir.
# Çalıştır: blender -b --factory-startup -P oyun/blender/minyatur_modeller.py
# Çıktı: oyun/a0/minyatur.glb (+ minyatur.txt = base64; yayın sayfası .glb sunmuyor) ve oyun/blender/minyatur.blend
# Ölçek: 1 birim = 1 metre (oyun fiziğiyle aynı). Oyuncak oranları (tombul roket, büyük kuşlar) oyunda ölçekle verilir.
# Kök nesneler: Roket, Kule, Rampa, Ucak. Parça adları oyun kodunda kullanılır; değiştirme.
import bpy, bmesh, math, os, base64
from mathutils import Vector

KOK = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(KOK, "..", "a0", "minyatur.glb")
sc = bpy.context.scene
for ob in list(bpy.data.objects): bpy.data.objects.remove(ob)

# ---------------------------------------------------------------- malzemeler: boyalı plastik
def plastik(ad, renk, puruz=0.32, kaplama=0.35, metal=0.0):
    m = bpy.data.materials.new(ad); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*renk, 1); b.inputs["Roughness"].default_value = puruz; b.inputs["Metallic"].default_value = metal
    if "Coat Weight" in b.inputs:
        b.inputs["Coat Weight"].default_value = kaplama; b.inputs["Coat Roughness"].default_value = 0.15
    return m

def isikli(ad, renk, guc=3.0):
    m = plastik(ad, renk, 0.4, 0.0)
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Emission Color"].default_value = (*renk, 1); b.inputs["Emission Strength"].default_value = guc
    return m

BOYA = {
    "Boya_Beyaz": plastik("O_Beyaz", (0.92, 0.91, 0.87)),
    "Boya_KirikBeyaz": plastik("O_Krem", (0.93, 0.86, 0.7)),
    "Karbon_Siyah": plastik("O_Lacivert", (0.04, 0.07, 0.2)),
    "Serit_Turuncu": plastik("O_Turuncu", (0.95, 0.38, 0.06)),
    "Metal_Gri": plastik("O_Gri", (0.62, 0.64, 0.68), puruz=0.3, kaplama=0.0, metal=0.6),
    "Nozul_Isil": plastik("O_Nozul", (0.32, 0.22, 0.17), puruz=0.35, kaplama=0.0, metal=0.8)}
KIRMIZI = plastik("O_Kirmizi", (0.82, 0.07, 0.05))
BEYAZ, LACI, GRI = BOYA["Boya_Beyaz"], BOYA["Karbon_Siyah"], plastik("O_Rampa", (0.55, 0.57, 0.6), puruz=0.45, kaplama=0.15)
KOYU = plastik("O_Koyu", (0.16, 0.17, 0.2), puruz=0.5, kaplama=0.1)
SARI = plastik("O_Sari", (0.98, 0.72, 0.1))
CAM = plastik("O_Cam", (0.05, 0.09, 0.16), puruz=0.12, kaplama=0.8)

def bos(ad):
    o = bpy.data.objects.new(ad, None); sc.collection.objects.link(o); return o

def yumusak(o):
    if o.type == "MESH":
        for p in o.data.polygons: p.use_smooth = True
    return o

def pah(o, gen, seg=3):
    """Oyuncak kenarı: keskin köşe yok, plastik döküm gibi yuvarlatılmış."""
    m = o.modifiers.new("Pah", "BEVEL"); m.width = gen; m.segments = seg; m.limit_method = "ANGLE"
    o.modifiers.new("Yumusat", "WEIGHTED_NORMAL")
    return o

def kutu(ad, boyut, konum, mat, ebeveyn, pah_gen=None, don=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=konum, rotation=don)
    o = bpy.context.active_object; o.name = ad; o.scale = boyut
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(mat); o.parent = ebeveyn
    pah(o, pah_gen if pah_gen is not None else min(boyut) * 0.18)
    return o

def silindir(ad, r, uz, konum, mat, ebeveyn, don=(0, 0, 0), seg=40, r2=None, pah_gen=None):
    bpy.ops.mesh.primitive_cone_add(vertices=seg, radius1=r, radius2=r if r2 is None else r2, depth=uz, location=konum, rotation=don)
    o = yumusak(bpy.context.active_object); o.name = ad; o.data.materials.append(mat); o.parent = ebeveyn
    if pah_gen: pah(o, pah_gen)
    return o

def kure(ad, r, konum, mat, ebeveyn, olcek=(1, 1, 1), seg=32):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, radius=r, location=konum)
    o = yumusak(bpy.context.active_object); o.name = ad; o.scale = olcek
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(mat); o.parent = ebeveyn
    return o

# ---------------------------------------------------------------- roket (roket.blend'den, oyuncak boyası)
roket = bos("Roket")
with bpy.data.libraries.load(os.path.join(KOK, "roket.blend")) as (kaynak, hedef):
    hedef.objects = kaynak.objects
for o in hedef.objects:
    if o is None or o.type != "MESH": continue
    sc.collection.objects.link(o); yumusak(o); o.parent = roket
    for i, m in enumerate(o.data.materials):
        if m and m.name.split(".")[0] in BOYA: o.data.materials[i] = BOYA[m.name.split(".")[0]]
    if o.name.split(".")[0] == "Burun" or o.name.startswith("Kanatcik_"): o.data.materials[0] = KIRMIZI

# ---------------------------------------------------------------- rampa: yuvarlak gri kaide, sarı uyarı halkası, dört tutucu
rampa = bos("Rampa")
silindir("Rampa_Taban", 13.0, 3.0, (0, 0, 1.5), GRI, rampa, seg=64, pah_gen=0.8)
silindir("Rampa_Serit", 13.05, 0.6, (0, 0, 2.2), SARI, rampa, seg=64)
silindir("Rampa_Kaide", 4.2, 2.0, (0, 0, 4.0), KOYU, rampa, seg=40, pah_gen=0.4)
for i in range(4):
    a = i * math.pi / 2 + math.pi / 4
    kutu(f"Rampa_Tutucu_{i}", (1.2, 1.2, 3.0), (math.cos(a) * 3.9, math.sin(a) * 3.9, 6.5), KIRMIZI, rampa, 0.3)

# ---------------------------------------------------------------- oyuncak fırlatma kulesi: kırmızı ayaklar, beyaz kafes çubukları, açılan kollar
# Kule (0,0) kökünde durur; oyunda rampanın −x yanına konur. Kollar menteşeden (kule iç yüzü) döner: Kol_Ust, Kol_Alt.
kule = bos("Kule")
YUK, EN = 62.0, 7.0
for i, (x, y) in enumerate(((-1, -1), (1, -1), (-1, 1), (1, 1))):
    kutu(f"Kule_Ayak_{i}", (1.1, 1.1, YUK), (x * EN / 2, y * EN / 2, YUK / 2), KIRMIZI, kule, 0.35)
kat = 0
for z in [5.0 + 7.0 * k for k in range(9)]:
    for yon in range(4):
        a = yon * math.pi / 2
        cx, cy = math.cos(a) * EN / 2, math.sin(a) * EN / 2
        kutu(f"Kule_Kusak_{kat}_{yon}", (0.7, EN, 0.7), (cx, cy, z), BEYAZ, kule, 0.22, don=(0, 0, a))
        # çapraz çubuk: kafes görünümü
        kutu(f"Kule_Capraz_{kat}_{yon}", (0.45, math.hypot(EN, 7.0) * 0.98, 0.45), (cx, cy, z + 3.5), BEYAZ, kule, 0.15, don=(math.atan2(7.0, EN) * (1 if kat % 2 else -1), 0, a))
    kat += 1
kutu("Kule_Cati", (EN + 1.6, EN + 1.6, 1.4), (0, 0, YUK + 0.7), KIRMIZI, kule, 0.4)
silindir("Kule_Direk", 0.35, 6.0, (0, 0, YUK + 4.4), BEYAZ, kule, seg=16)
kure("Kule_Isik", 0.9, (0, 0, YUK + 7.6), isikli("O_KirmiziIsik", (1, 0.12, 0.08), 6.0), kule, seg=16)

def kol(ad, z, uz, kal):
    """Menteşe kökü kulenin roket tarafındaki yüzünde (x = +EN/2); kol +x yönüne uzanır, roketin gövdesine dayanır."""
    k = bos(ad); k.parent = kule; k.location = (EN / 2, 0, z)
    kutu(ad + "_Govde", (uz, kal, kal), (EN / 2 + uz / 2, 0, z), BEYAZ, k, 0.3).parent = k
    for o in k.children:
        o.location = (uz / 2, 0, 0)
    kutu(ad + "_Uc", (1.0, kal * 1.8, kal * 1.4), (uz, 0, 0), KIRMIZI, k, 0.3).location = (uz - 0.3, 0, 0)
    return k
# kule rampa merkezinin 15 m yanında; kollar menteşeden tombul roketin yüzeyine (yarıçap ≈ 2,5 m) uzanır: 15 − 3,5 − 2,5 ≈ 9 m
kol("Kol_Ust", 46.0, 9.0, 1.4)
kol("Kol_Alt", 24.0, 9.0, 1.2)

# ---------------------------------------------------------------- oyuncak yolcu uçağı (A320 boyu, tombul oyuncak oranlarıyla)
# Burun −x yönünde. Blender'da kanat ±y; glTF'de bu ±z olur. Sağ kanat ucu (glTF +z = Blender −y) ayrı nesne: çarpışmada kopar.
ucak = bos("Ucak")
GOV_R = 2.6
silindir("Ucak_Govde", GOV_R, 26.0, (0.5, 0, 0), BEYAZ, ucak, don=(0, math.pi / 2, 0), seg=40)
kure("Ucak_Burun", GOV_R, (-12.5, 0, 0), BEYAZ, ucak, olcek=(2.0, 1, 1))
silindir("Ucak_Kuyruk", GOV_R, 8.0, (17.5, 0, 0.9), BEYAZ, ucak, don=(0, math.pi / 2, 0), seg=40, r2=0.7)
# pencereler: burunda iri oyuncak kabin camı, yanlarda yuvarlak lombozlar
kure("Ucak_Kabin", 1.5, (-15.6, 0, 0.9), CAM, ucak, olcek=(1.1, 1.6, 0.6))
for i in range(9):
    for yan in (-1, 1):
        kure(f"Ucak_Pencere_{i}_{yan}", 0.42, (-8.0 + i * 2.6, yan * GOV_R * 0.97, 0.7), CAM, ucak, olcek=(1, 0.35, 1), seg=12)

def kanat_parca(ad, y0, y1, kok, uc, ok, kal, z, ebeveyn, mat):
    """y0→y1 arasında kökte 'kok', uçta 'uc' veteri olan, geriye 'ok' oranında kayan kalın oyuncak kanat."""
    me = bpy.data.meshes.new(ad); bm = bmesh.new(); kat = []
    for y, c in ((y0, kok), (y1, uc)):
        x0 = abs(y) * ok
        kat.append([bm.verts.new((x0 - c / 2 + dx * c, y, z + dz * kal)) for dx, dz in ((0, 0.5), (1, 0.5), (1, -0.5), (0, -0.5))])
    bm.faces.new(kat[0][::-1]); bm.faces.new(kat[1])
    for i in range(4):
        bm.faces.new((kat[0][i], kat[0][(i + 1) % 4], kat[1][(i + 1) % 4], kat[1][i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(ad, me); sc.collection.objects.link(o); o.data.materials.append(mat); o.parent = ebeveyn
    pah(o, kal * 0.4, 3)
    return o

for yan in (1, -1):
    s = "L" if yan > 0 else "R"
    kanat_parca(f"Ucak_Kanat_{s}", 0, yan * 11.5, 7.0, 3.6, 0.5, 0.9, -1.2, ucak, BEYAZ)
    uc = kanat_parca("Ucak_KanatUcu" if yan < 0 else "Ucak_KanatUcuSol", yan * 11.5, yan * 17.6, 3.6, 1.8, 0.5, 0.7, -1.2, ucak, BEYAZ)
    kutu(f"Ucak_Kanatcik_{s}", (1.6, 0.4, 2.6), (8.8 + 0.5 * 0, yan * 17.6, 0.1), LACI, uc if yan < 0 else ucak, 0.15)
    silindir(f"Ucak_Motor_{s}", 1.35, 4.6, (-3.0, yan * 5.8, -2.8), LACI, ucak, don=(0, math.pi / 2, 0), seg=32, pah_gen=0.25)
    silindir(f"Ucak_MotorAgiz_{s}", 1.0, 0.4, (-5.35, yan * 5.8, -2.8), KOYU, ucak, don=(0, math.pi / 2, 0), seg=32)
    kanat_parca(f"Ucak_Yatay_{s}", 0, yan * 6.4, 3.6, 1.6, 0.55, 0.45, 1.6, ucak, BEYAZ).location.x = 16.0
# dikey kuyruk: lacivert, üstünde kırmızı şerit
me = bpy.data.meshes.new("Ucak_Dikey"); bm = bmesh.new()
prof = [(13.5, 2.0), (20.0, 2.0), (22.6, 9.6), (19.4, 9.6)]
kat2 = [[bm.verts.new((x, y, z)) for x, z in prof] for y in (-0.35, 0.35)]
bm.faces.new(kat2[0][::-1]); bm.faces.new(kat2[1])
for i in range(4): bm.faces.new((kat2[0][i], kat2[0][(i + 1) % 4], kat2[1][(i + 1) % 4], kat2[1][i]))
bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
d = bpy.data.objects.new("Ucak_Dikey", me); sc.collection.objects.link(d); d.data.materials.append(LACI); d.parent = ucak; pah(d, 0.25)
kure("Ucak_IsikK", 0.4, (8.8, -17.8, -1.2), isikli("O_IsikK", (1, 0.1, 0.08)), ucak, seg=12)
kure("Ucak_IsikY", 0.4, (8.8, 17.8, -1.2), isikli("O_IsikY", (0.1, 1, 0.3)), ucak, seg=12)

# kanat ucunun kendi kökü ucunda olsun: koparken kendi çevresinde dönsün
kanat_ucu = bpy.data.objects["Ucak_KanatUcu"]
bpy.context.view_layer.update()
cocuk = {c: c.matrix_world.copy() for c in kanat_ucu.children}
for o in sc.objects: o.select_set(False)
kanat_ucu.select_set(True); bpy.context.view_layer.objects.active = kanat_ucu
bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
bpy.context.view_layer.update()
for c, mw in cocuk.items(): c.matrix_world = mw

# ---------------------------------------------------------------- dışa aktar
os.makedirs(os.path.dirname(OUT), exist_ok=True)
for o in sc.objects: o.select_set(True)
bpy.ops.export_scene.gltf(filepath=OUT, export_format="GLB", export_apply=True, export_yup=True)
print("yazıldı:", os.path.abspath(OUT), os.path.getsize(OUT), "bayt")
TOUT = OUT[:-4] + ".txt"
open(TOUT, "w").write(base64.b64encode(open(OUT, "rb").read()).decode())
print("yazıldı:", os.path.abspath(TOUT), os.path.getsize(TOUT), "bayt")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(KOK, "minyatur.blend"))
