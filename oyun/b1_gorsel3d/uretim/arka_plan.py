# Son Durak: Plüton · gökyüzü paralaks katmanları (Blender 5.0.1 / bpy 5.0.1, Cycles CPU)
# Kullanım: <bpy-venv>/bin/python arka_plan.py   (ya da blender -b --factory-startup -P arka_plan.py)
# Çıktı: sprite/ham/arka_uzak.png, sprite/ham/arka_yakin.png  (768 px genişlik, yatayda DİKİŞSİZ döşenir; deniz yok)
# Döşeme: tüm geometri W periyotlu işlevlerle kurulur ve ±W kopyalanır; ortografik kamera tam bir periyodu görür.
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as O
import modeller as M
import bpy
from mathutils import Vector

W = 16.0           # bir periyot (dünya birimi) = 768 px
TAU = 2 * math.pi

def periyodik(x, terimler):
    return sum(a * math.sin(TAU * k * x / W + f) for k, a, f in terimler)

def arazi(ad, hf, x_n, y0, y1, y_n, mat, renk_f=None):
    V, F = [], []
    xs = [-1.5 * W + 3 * W * i / x_n for i in range(x_n + 1)]
    ys = [y0 + (y1 - y0) * j / y_n for j in range(y_n + 1)]
    for y in ys:
        for x in xs: V.append((x, y, hf(x, y)))
    n = x_n + 1
    for j in range(y_n):
        for i in range(x_n):
            a = j * n + i; F.append((a, a + 1, a + n + 1, a + n))
    o = O.mesh_obj(ad, V, F, mat)
    import bmesh
    bm = bmesh.new(); bm.from_mesh(o.data); bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    for f in bm.faces:
        if f.normal.z < 0: f.normal_flip()
    bm.to_mesh(o.data); bm.free()
    return o

def periyodik_voronoi(nt, N, L, olcek, renkler, koyu=None):
    """x yönünde periyodik hücre deseni: x -> silindir açısı, 3B Voronoi."""
    tc = N.new("ShaderNodeTexCoord"); sp = N.new("ShaderNodeSeparateXYZ"); L.new(tc.outputs["Object"], sp.inputs[0])
    def m(op, a, b=None):
        n = N.new("ShaderNodeMath"); n.operation = op
        for i, v in enumerate((a, b)):
            if v is None: continue
            if isinstance(v, (int, float)): n.inputs[i].default_value = v
            else: L.new(v, n.inputs[i])
        return n.outputs[0]
    ang = m("MULTIPLY", sp.outputs["X"], TAU / W); Rr = W / TAU
    cx = m("MULTIPLY", m("COSINE", ang), Rr); cy = m("MULTIPLY", m("SINE", ang), Rr)
    cb = N.new("ShaderNodeCombineXYZ"); L.new(cx, cb.inputs[0]); L.new(cy, cb.inputs[1]); L.new(m("MULTIPLY", sp.outputs["Y"], 1.6), cb.inputs[2])
    vo = N.new("ShaderNodeTexVoronoi"); vo.inputs["Scale"].default_value = olcek; vo.inputs["Randomness"].default_value = 0.55
    L.new(cb.outputs[0], vo.inputs["Vector"])
    rp = N.new("ShaderNodeValToRGB"); rp.color_ramp.interpolation = "CONSTANT"
    e = rp.color_ramp.elements; e[0].position = 0; e[0].color = O.lin(renkler[0]); e[1].position = 1 / len(renkler); e[1].color = O.lin(renkler[1])
    for i, r in enumerate(renkler[2:]): e.new((i + 2) / len(renkler)).color = O.lin(r)
    sc = N.new("ShaderNodeSeparateColor"); L.new(vo.outputs["Color"], sc.inputs[0]); L.new(sc.outputs[0], rp.inputs[0])
    if not koyu: return rp.outputs[0]
    # tarla sınırı (çit/çalı çizgisi): F2-F1 küçükse koyu
    vo2 = N.new("ShaderNodeTexVoronoi"); vo2.feature = "DISTANCE_TO_EDGE"; vo2.inputs["Scale"].default_value = olcek; vo2.inputs["Randomness"].default_value = 0.55
    L.new(cb.outputs[0], vo2.inputs["Vector"])
    kenar = m("LESS_THAN", vo2.outputs["Distance"], 0.018)
    mx = N.new("ShaderNodeMix"); mx.data_type = "RGBA"; L.new(kenar, mx.inputs[0]); L.new(rp.outputs[0], mx.inputs[6]); mx.inputs[7].default_value = O.lin(koyu)
    return mx.outputs[2]

def cogalt(o):
    """Periyot kopyaları (-W, +W)."""
    for dx in (-W, W):
        c = o.copy(); c.location = o.location + Vector((dx, 0, 0)); bpy.context.scene.collection.objects.link(c)

def kur_isik():
    for n in ("kenar_soguk", "kenar_sicak", "yuz_dolgu"):
        if n in bpy.data.objects: bpy.data.objects[n].data.energy *= 0.25
    g = bpy.data.objects["gunes"]; g.data.energy = 3.2
    g.rotation_euler = (Vector((0.6, 0.9, -0.75))).to_track_quat("-Z", "Y").to_euler()  # sol önden, alçak: tepelerde uzun yumuşak gölge

def kamera(z0, z1, tilt=0.0, px=768):
    s = bpy.context.scene; cam = s.camera
    h = z1 - z0; s.render.resolution_x = px; s.render.resolution_y = int(round(px * h / W / 2)) * 2
    cam.data.ortho_scale = W
    cam.rotation_euler = (math.pi / 2 - math.radians(tilt), 0, 0)
    d = 60; cy = (z0 + z1) / 2
    cam.location = (0, -d * math.cos(math.radians(tilt)), cy + d * math.sin(math.radians(tilt)))
    cam.data.clip_end = 300

def uzak():
    O.sifirla("B"); kur_isik(); random.seed(5)
    # en uzak sıradağ (lavanta, puslu)
    t1 = [(1, 0.55, 0.3), (2, 0.35, 1.7), (3, 0.42, 4.0), (5, 0.22, 2.2), (7, 0.12, 0.5)]
    dag = O.plastik("dag_uzak", "#a7b3f0", rough=0.9, coat=0, sss=0.2, kenar=0.5)
    arazi("dag_uzak", lambda x, y: (2.3 + periyodik(x, t1)) * math.sin(math.pi * (y - 14) / 4) ** 0.7, 900, 14, 18, 14, dag).location = (0, 0, -1.2)
    # orta tepeler (mavi-yeşil)
    t2 = [(2, 0.4, 0.9), (3, 0.3, 2.6), (4, 0.25, 0.2), (6, 0.15, 3.3)]
    tep = O.plastik("tepe_uzak", "#8fbfb0", rough=0.85, coat=0, sss=0.2, kenar=0.45)
    arazi("tepe_uzak", lambda x, y: (1.25 + periyodik(x, t2)) * math.sin(math.pi * (y - 8) / 4) ** 0.6, 900, 8, 12, 12, tep).location = (0, 0, -2.4)
    # bulut kümeleri (ufkun üstünde, dağların arkasında ve önünde)
    BUL = O.plastik("bulut_uzak", "#eef3ff", rough=0.8, coat=0, sss=0.25, kenar=0.5)
    for i in range(6):
        x = -W / 2 + W * (i + random.uniform(0.1, 0.5)) / 6
        y = 22 if i % 2 == 0 else 11
        b = M.bulut_mesh(f"uzak_bulut_{i}", M.kumulus(random.uniform(2.6, 4.2), random.uniform(0.9, 1.4), 40 + i), BUL, coz=0.08)
        b.location = (x, y, random.uniform(1.4, 2.6) if y > 15 else 0.2); b.scale = (1, 0.6, 0.85); cogalt(b)
    kamera(-3.0, 5.0, tilt=0.0)
    for o in bpy.context.scene.objects:
        if o.type == "MESH": o.hide_render = False
    bpy.context.scene.render.filepath = os.path.join(O.HAM, "arka_uzak.png"); bpy.context.scene.cycles.samples = 64
    import time; t = time.time(); bpy.ops.render.render(write_still=True); print(f"[render] arka_uzak {time.time() - t:.1f} sn", flush=True)
    with open(os.path.join(O.HAM, "_sureler.txt"), "a") as f: f.write(f"arka_uzak.png\t768x{bpy.context.scene.render.resolution_y}\t64\t{time.time() - t:.1f}\n")

def yakin():
    O.sifirla("B"); kur_isik(); random.seed(9)
    t = [(1, 0.5, 0.4), (2, 0.55, 2.0), (3, 0.35, 4.1), (5, 0.18, 1.0)]
    def h(x, y):
        # önde alçak, geride yükselen dalgalı tepeler (y: derinlik)
        dy = max(0.0, y) / 9
        return (0.9 + periyodik(x + y * 0.35, t)) * (0.35 + 0.9 * dy) + 0.25 * math.sin(TAU * 4 * x / W + y * 1.3) * dy + min(0.0, y) * 0.12
    tarla = O.plastik("tarla", "#7cc95a", rough=0.85, coat=0, sss=0.1, kenar=0.35,
                      renk_dugum=lambda nt, N, L: periyodik_voronoi(nt, N, L, 0.9, ["#5fae4a", "#7dbb4c", "#4f9c45", "#a9c55a", "#6fb350", "#c9b45c"], koyu="#2f6e3a"))
    ar = arazi("arazi", h, 640, -10, 9, 80, tarla)
    # ağaçlar (lolipop) ve bir çiftlik evi
    GOV = O.plastik("agac_govde", "#8a5a34", rough=0.7, coat=0); YAP = O.plastik("agac", "#2f9e57", rough=0.6, sss=0.2, kenar=0.7)
    YAP2 = O.plastik("agac2", "#46b65a", rough=0.6, sss=0.2, kenar=0.7)
    for i in range(26):
        x = -W / 2 + W * i / 26 + random.uniform(-0.2, 0.2); y = random.uniform(0.6, 7.5)
        z = h(x, y); s = random.uniform(0.75, 1.15) * (0.9 + 0.05 * y)
        g = O.silindir(f"agac_g_{i}", 0.05 * s, 0.4 * s, GOV, loc=(x, y, z + 0.18 * s))
        k = O.kure(f"agac_t_{i}", 0.3 * s, YAP if i % 3 else YAP2, loc=(x, y, z + 0.5 * s), olcek=(1, 1, 1.05), seg=20, halka=10)
        O.kabuk(k, 0.02, "#1f5a3a"); cogalt(g); cogalt(k)
    x, y = 2.2, 3.0; z = h(x, y)
    ev = O.plaka("ev", [(-0.35, 0), (0.35, 0), (0.35, 0.42), (-0.35, 0.42)], 0.5, O.plastik("ev", "#fff3df", rough=0.6), pah=0.02)
    ev.location = (x, y + 0.25, z - 0.05); O.kabuk(ev, 0.015)
    cati = O.plaka("cati", [(-0.45, 0.4), (0.45, 0.4), (0, 0.78)], 0.62, O.plastik("cati", "#e8413c", rough=0.5), pah=0.02)
    cati.location = (x, y + 0.31, z - 0.05); O.kabuk(cati, 0.015); cogalt(ev); cogalt(cati)
    kamera(-1.4, 4.6, tilt=16.0)
    for o in bpy.context.scene.objects:
        if o.type == "MESH": o.hide_render = False
    bpy.context.scene.render.filepath = os.path.join(O.HAM, "arka_yakin.png"); bpy.context.scene.cycles.samples = 64
    import time; t0 = time.time(); bpy.ops.render.render(write_still=True); print(f"[render] arka_yakin {time.time() - t0:.1f} sn", flush=True)
    with open(os.path.join(O.HAM, "_sureler.txt"), "a") as f: f.write(f"arka_yakin.png\t768x{bpy.context.scene.render.resolution_y}\t64\t{time.time() - t0:.1f}\n")

arg = O.argumanlar()
if not arg or arg[0] in ("uzak", "hepsi"): uzak()
if not arg or arg[0] in ("yakin", "hepsi"): yakin()
