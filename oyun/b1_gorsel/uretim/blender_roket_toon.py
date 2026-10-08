# B1 teknik yol karşılaştırması: aynı roketin Blender'da toon (Shader to RGB + Freestyle kontur) yandan ortografik render'ı.
# Çalıştır: <python3.11 venv, pip install bpy> python blender_roket_toon.py   ya da   blender -b --factory-startup -P blender_roket_toon.py
# Çıktı: oyun/b1_gorsel/onizleme/blender_roket_toon.png (saydam zemin, 640×320)
import bpy, math, os
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CIKTI = os.path.join(KOK, "onizleme", "blender_roket_toon.png")
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

def mat(ad, renk):
    m = bpy.data.materials.new(ad); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    # toon: dünya normali · sabit ışık yönü → basamaklı renk rampası (Cycles'ta da çalışır; GPU gerekmez)
    geo = nt.nodes.new("ShaderNodeNewGeometry"); dot = nt.nodes.new("ShaderNodeVectorMath"); dot.operation = "DOT_PRODUCT"
    dot.inputs[1].default_value = (-0.35, -0.55, 0.76)
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.interpolation = "CONSTANT"
    ramp.color_ramp.elements[0].position = 0.0; ramp.color_ramp.elements[0].color = (renk[0] * 0.55, renk[1] * 0.5, renk[2] * 0.7, 1)
    ramp.color_ramp.elements[1].position = 0.05; ramp.color_ramp.elements[1].color = (*renk, 1)
    e = ramp.color_ramp.elements.new(0.8); e.color = tuple(min(1, c * 1.15 + 0.1) for c in renk) + (1,)
    em = nt.nodes.new("ShaderNodeEmission"); out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(geo.outputs["Normal"], dot.inputs[0]); nt.links.new(dot.outputs["Value"], ramp.inputs[0]); nt.links.new(ramp.outputs[0], em.inputs[0]); nt.links.new(em.outputs[0], out.inputs[0])
    return m

BEYAZ = mat("beyaz", (0.92, 0.93, 0.97)); KIRMIZI = mat("kirmizi", (1.0, 0.05, 0.08)); METAL = mat("metal", (0.35, 0.4, 0.5)); CAM = mat("cam", (0.08, 0.15, 0.45))

def ekle(ob, m):
    ob.data.materials.append(m); bpy.ops.object.shade_smooth(); return ob

# eksen: roket +X yönünde (yan görünüş, kamera −Y'den bakar)
def silindir(x0, x1, r, m, r2=None):
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=r, depth=x1 - x0, location=((x0 + x1) / 2, 0, 0), rotation=(0, math.pi / 2, 0))
    else:
        bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=r, radius2=r2, depth=x1 - x0, location=((x0 + x1) / 2, 0, 0), rotation=(0, math.pi / 2, 0))
    return ekle(bpy.context.object, m)

silindir(-18.4, -5.0, 4.5, BEYAZ); silindir(-10.6, -9.0, 4.55, KIRMIZI); silindir(-6.1, -4.9, 4.55, METAL)
silindir(-5.6, 4.5, 4.2, BEYAZ); silindir(-5.6, -4.4, 4.25, KIRMIZI)
silindir(4.4, 12.5, 4.2, KIRMIZI, 0.3)
silindir(-20.3, -18.3, 3.1, METAL, 2.2)
bpy.ops.mesh.primitive_uv_sphere_add(radius=2.7, location=(0.3, -3.3, 0), scale=(1, 0.35, 1)); ekle(bpy.context.object, CAM)
bpy.ops.mesh.primitive_torus_add(major_radius=2.9, minor_radius=0.45, location=(0.3, -3.6, 0), rotation=(math.pi / 2, 0, 0)); ekle(bpy.context.object, METAL)
for z in (1, -1):
    for x0, x1, h, yer in ((-18.9, -11.2, 9.6, -4.0), (-6.9, -1.6, 7.2, -3.6)):
        verts = [(x1, -0.35, z * 4.0), (x0, -0.35, z * 4.0), (x0 - 0.3, -0.35, z * h), (x0 + 1.4, -0.35, z * h), (x1, 0.35, z * 4.0), (x0, 0.35, z * 4.0), (x0 - 0.3, 0.35, z * h), (x0 + 1.4, 0.35, z * h)]
        faces = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
        me = bpy.data.meshes.new("kanat"); me.from_pydata(verts, [], faces); ob = bpy.data.objects.new("kanat", me); sc.collection.objects.link(ob); ob.data.materials.append(KIRMIZI)

# ışık + kamera
bpy.ops.object.light_add(type="SUN", rotation=(math.radians(50), math.radians(-30), math.radians(-20))); bpy.context.object.data.energy = 4
bpy.ops.object.camera_add(location=(-4, -60, 0), rotation=(math.pi / 2, 0, 0)); cam = bpy.context.object; sc.camera = cam
cam.data.type = "ORTHO"; cam.data.ortho_scale = 36
sc.render.engine = "CYCLES"; sc.cycles.samples = 16; sc.cycles.device = "CPU"
sc.render.resolution_x, sc.render.resolution_y = 640, 320; sc.render.film_transparent = True
sc.view_settings.view_transform = "Standard"
sc.render.use_freestyle = True
ls = sc.view_layers[0].freestyle_settings.linesets[0] if sc.view_layers[0].freestyle_settings.linesets else sc.view_layers[0].freestyle_settings.linesets.new("hat")
if ls.linestyle is None: ls.linestyle = bpy.data.linestyles.new("hat")
ls.linestyle.color = (0.14, 0.12, 0.3); ls.linestyle.thickness = 5
sc.render.filepath = CIKTI
bpy.ops.render.render(write_still=True)
print("yazıldı", CIKTI)
