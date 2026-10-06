# Son Durak: Plüton — A0 roketi. Blender'ın Python modülüyle (bpy) scriptle üretilir.
# Çalıştır: <bpy ortamı>/python oyun/blender/roket.py  ->  oyun/a0/roket.glb
# Ölçek: 1 birim = 1 metre. Blender Z-yukarı; glTF dışa aktarımı Y-yukarıya çevirir.
# Parçalar ayrı nesneler olarak adlandırılır; oyun hasarda göçük, kopma ve parçalanma için bunları ayrı ayrı kullanır.
import bpy, bmesh, math, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "a0", "roket.glb")

bpy.ops.wm.read_factory_settings(use_empty=True)

def malzeme(ad, renk, metal=0.0, puruz=0.5, isik=None):
    m = bpy.data.materials.new(ad)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*renk, 1)
    b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = puruz
    if isik:
        b.inputs["Emission Color"].default_value = (*isik, 1)
        b.inputs["Emission Strength"].default_value = 2.0
    return m

BEYAZ = malzeme("Boya_Beyaz", (0.86, 0.86, 0.84), 0.0, 0.42)
KIRIK = malzeme("Boya_KirikBeyaz", (0.78, 0.78, 0.75), 0.0, 0.5)
SIYAH = malzeme("Karbon_Siyah", (0.035, 0.036, 0.04), 0.1, 0.55)
GRI = malzeme("Metal_Gri", (0.42, 0.43, 0.45), 0.9, 0.35)
NOZUL = malzeme("Nozul_Isil", (0.30, 0.20, 0.14), 1.0, 0.3)
TURUNCU = malzeme("Serit_Turuncu", (0.95, 0.42, 0.08), 0.0, 0.45)

def silindir(ad, r1, r2, z0, z1, seg=48, halka=1, mat=BEYAZ, kapak=True):
    """z0..z1 arasında r1→r2 yarıçaplı, 'halka' adet yatay kesitli silindir/koni (göçük için yeterli köşe)."""
    me = bpy.data.meshes.new(ad)
    bm = bmesh.new()
    rings = []
    for i in range(halka + 1):
        t = i / halka
        z = z0 + (z1 - z0) * t
        r = r1 + (r2 - r1) * t
        rings.append([bm.verts.new((r * math.cos(2 * math.pi * k / seg), r * math.sin(2 * math.pi * k / seg), z)) for k in range(seg)])
    for i in range(halka):
        for k in range(seg):
            a, b = rings[i][k], rings[i][(k + 1) % seg]
            c, d = rings[i + 1][(k + 1) % seg], rings[i + 1][k]
            bm.faces.new((a, b, c, d))
    if kapak:
        bm.faces.new(list(reversed(rings[0])))
        if r2 > 1e-4:
            bm.faces.new(rings[-1])
    bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    ob = bpy.data.objects.new(ad, me)
    bpy.context.collection.objects.link(ob)
    ob.data.materials.append(mat)
    return ob

def ogive(ad, r, z0, h, seg=48, halka=18, mat=BEYAZ):
    """Teğet ogive burun konisi."""
    rho = (r * r + h * h) / (2 * r)
    me = bpy.data.meshes.new(ad); bm = bmesh.new(); rings = []
    for i in range(halka + 1):
        t = i / halka
        x = h * t
        y = math.sqrt(max(0.0, rho * rho - x * x)) + r - rho
        y = max(y, 0.0)
        if i == halka: y = 0.0
        z = z0 + x
        if y < 1e-4:
            rings.append([bm.verts.new((0, 0, z))]); break
        rings.append([bm.verts.new((y * math.cos(2 * math.pi * k / seg), y * math.sin(2 * math.pi * k / seg), z)) for k in range(seg)])
    # burun ucu ters: taban r'de olmalı -> ogive tabanı z0'da geniş, tepe z0+h'de sivri
    for i in range(len(rings) - 1):
        A, B = rings[i], rings[i + 1]
        for k in range(seg):
            if len(B) == 1:
                bm.faces.new((A[k], A[(k + 1) % seg], B[0]))
            else:
                bm.faces.new((A[k], A[(k + 1) % seg], B[(k + 1) % seg], B[k]))
    bm.faces.new(list(reversed(rings[0])))
    bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    ob = bpy.data.objects.new(ad, me); bpy.context.collection.objects.link(ob)
    ob.data.materials.append(mat); return ob

def kutu(ad, sx, sy, sz, x, y, z, mat, rz=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z), rotation=(0, 0, rz))
    ob = bpy.context.active_object; ob.name = ad
    ob.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(scale=True)
    ob.data.materials.append(mat); return ob

def kanatcik(ad, aci, mat):
    """Tabanda yamuk biçimli kanatçık (kopabilir parça)."""
    me = bpy.data.meshes.new(ad); bm = bmesh.new()
    R, k = 1.83, 0.12
    prof = [(R, 0.6), (R + 1.4, 0.6), (R + 1.4, 1.6), (R, 4.2)]
    v = []
    for s in (-k, k):
        v.append([bm.verts.new((px, s, pz)) for px, pz in prof])
    bm.faces.new(v[0]); bm.faces.new(list(reversed(v[1])))
    for i in range(4):
        bm.faces.new((v[0][i], v[0][(i + 1) % 4], v[1][(i + 1) % 4], v[1][i]))
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(ad, me); bpy.context.collection.objects.link(ob)
    ob.data.materials.append(mat); ob.rotation_euler = (0, 0, aci)
    return ob

# --- gövde (taban z=0, burun ~z=50)
s1 = silindir("Kademe1", 1.83, 1.83, 1.2, 31.0, seg=56, halka=40, mat=BEYAZ)
etek = silindir("MotorEtegi", 2.05, 1.83, 0.0, 1.2, seg=56, halka=2, mat=SIYAH)
ara = silindir("AraKademe", 1.85, 1.85, 31.0, 34.2, seg=56, halka=4, mat=SIYAH)
s2 = silindir("Kademe2", 1.83, 1.83, 34.2, 43.0, seg=56, halka=12, mat=KIRIK)
kab = silindir("Kaporta", 2.15, 2.15, 43.0, 46.0, seg=56, halka=4, mat=BEYAZ)
burun = ogive("Burun", 2.15, 46.0, 6.0, seg=56, halka=20, mat=BEYAZ)

# panel çizgileri ve renk şeridi (ince halkalar)
for i, z in enumerate((6.0, 12.0, 18.0, 24.0)):
    silindir(f"PanelCizgisi_{i}", 1.845, 1.845, z, z + 0.06, seg=56, mat=SIYAH, kapak=False)
silindir("Serit", 1.842, 1.842, 27.0, 27.6, seg=56, mat=TURUNCU, kapak=False)
silindir("KaportaDikis", 2.165, 2.165, 45.95, 46.05, seg=56, mat=GRI, kapak=False)

# kanatçıklar (4 adet, kopabilir)
for i in range(4):
    kanatcik(f"Kanatcik_{i}", math.pi / 4 + i * math.pi / 2, SIYAH)

# ızgara kanatçıkları ara kademede (4 küçük panel)
for i in range(4):
    a = i * math.pi / 2
    kutu(f"Izgara_{i}", 0.9, 0.08, 0.9, math.cos(a) * 1.95, math.sin(a) * 1.95, 32.6, GRI, rz=a + math.pi / 2)

# motorlar: merkez + 4 çevre çan
def can(ad, x, y, r_bogaz, r_cikis, uzun):
    ob = silindir(ad, r_cikis, r_bogaz, -uzun, 0.0, seg=32, halka=6, mat=NOZUL, kapak=False)
    ob.location = (x, y, 0.0)
    return ob
can("Motor_0", 0, 0, 0.35, 0.78, 1.9)
for i in range(4):
    a = i * math.pi / 2 + math.pi / 4
    can(f"Motor_{i+1}", math.cos(a) * 1.05, math.sin(a) * 1.05, 0.25, 0.55, 1.5)

# ikinci kademe boşluk motoru: ara kademenin içinde gizli, kademe ayrılınca görünür
m2 = silindir("Motor2", 0.95, 0.32, 31.7, 34.2, seg=40, halka=6, mat=NOZUL, kapak=False)

# anten (kopabilir küçük parça) ve kablo kanalı
kutu("Anten", 0.08, 0.08, 1.4, 1.95, 0.0, 40.0, GRI)
kutu("KabloKanali", 0.18, 0.28, 25.0, 0.0, 1.9, 16.0, KIRIK)

# kökeni roketin ağırlık merkezi civarına: oyunda 0 noktası tabandan 20 m yukarıda olsun
for ob in bpy.context.collection.objects:
    ob.location.z -= 20.0

os.makedirs(os.path.dirname(OUT), exist_ok=True)
bpy.ops.export_scene.gltf(filepath=OUT, export_format="GLB", export_apply=True, export_yup=True)
print("yazıldı:", os.path.abspath(OUT), os.path.getsize(OUT), "bayt")

# Yayın sistemi .glb sunmadığı için, aynı modeli verisi gömülü glTF JSON olarak da yaz (roket.json)
import json, struct, base64
b = open(OUT, "rb").read()
n = struct.unpack("<I", b[12:16])[0]
j = json.loads(b[20:20 + n])
o = 20 + n
bn = struct.unpack("<I", b[o:o + 4])[0]
j["buffers"][0]["uri"] = "data:application/octet-stream;base64," + base64.b64encode(b[o + 8:o + 8 + bn]).decode()
JOUT = OUT[:-4] + ".json"
json.dump(j, open(JOUT, "w"), separators=(",", ":"))
print("yazıldı:", os.path.abspath(JOUT), os.path.getsize(JOUT), "bayt")
