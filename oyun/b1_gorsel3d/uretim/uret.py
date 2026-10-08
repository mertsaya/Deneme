# Son Durak: Plüton · B1 3B sprite üretimi (Blender 5.0.1 / bpy 5.0.1, Cycles CPU + OIDN)
# Kullanım:  <bpy-venv>/bin/python uret.py <set> [stil]     ya da   blender -b --factory-startup -P uret.py -- <set> [stil]
# Setler: stil | roket | alev | pilot | zeplin | balon | bulut | efekt | hepsi
# Çıktı: sprite/ham/*.png (konursuz, alfa). Kontur + sayfalar için: python kontur.py ve sayfa.py
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ortak as O
import modeller as M
import bpy

arg = O.argumanlar()
SET = arg[0] if arg else "hepsi"
STIL = arg[1] if len(arg) > 1 else "B"

def kayit_blend(ad):
    d = os.path.join(O.KOK, "model"); os.makedirs(d, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(d, ad + ".blend"), check_existing=False)

def glb(kok, ad):
    """Oyuna 3B gerekirse: GLB + base64 .txt (iç kontur kabuğu dışarıda bırakılır)."""
    d = os.path.join(O.KOK, "model"); os.makedirs(d, exist_ok=True)
    for o in bpy.context.scene.objects: o.select_set(False)
    for o in O.alt_nesneler(kok):
        o.select_set(True)
        if o.type == "MESH" and "kabuk" in o.modifiers: o.modifiers["kabuk"].show_viewport = False
    yol = os.path.join(d, ad + ".glb")
    bpy.ops.export_scene.gltf(filepath=yol, use_selection=True, export_apply=True, export_morph=True, export_yup=True)
    import base64
    with open(yol, "rb") as f, open(yol[:-4] + ".glb.b64.txt", "w") as g: g.write(base64.b64encode(f.read()).decode())
    for o in O.alt_nesneler(kok):
        if o.type == "MESH" and "kabuk" in o.modifiers: o.modifiers["kabuk"].show_viewport = True

def set_stil():
    for st in ("A", "B", "C"):
        O.sifirla(st)
        r = M.roket(); z = M.zeplin(); z.location = (0, 0, -6)
        p = M.pilot(); p.location = (0, 0, -12)
        O.ifade_sec(z, "normal"); O.ifade_sec(p, "heyecan")
        O.cek([r], f"stil_{st}_roket", 512, ornek=48)
        O.cek([z], f"stil_{st}_zeplin", 512, ornek=48)
        O.cek([p], f"stil_{st}_pilot", 384, ornek=48)

def set_roket():
    O.sifirla(STIL)
    r = M.roket()
    # açı kareleri: -30..+45 (8 kare), sabit ışık
    acilar = [-30 + i * 75 / 7 for i in range(8)]
    cer = None
    xs = []
    for a in acilar:
        r.rotation_euler = (0, -math.radians(a), 0); xs.append(O.sinir([r]))
    cer = (min(b[0] for b in xs), max(b[1] for b in xs), min(b[2] for b in xs), max(b[3] for b in xs))
    for i, a in enumerate(acilar):
        r.rotation_euler = (0, -math.radians(a), 0)
        O.cek([r], f"roket_aci_{i}", 640, cerceve=cer, pay=0.04)
    r.rotation_euler = (0, 0, 0)
    O.cek([r], "roket", 768)
    # kademeler ayrı (kopma / son şans)
    k1 = bpy.data.objects["kademe_1"]; k2 = bpy.data.objects["kademe_2"]
    O.cek([k1], "roket_kademe_1", 512)
    O.cek([k2], "roket_kademe_2", 512)
    kayit_blend("roket"); glb(r, "roket")

def set_alev():
    O.sifirla(STIL)
    ks = [M.alev(i) for i in range(4)]
    for k in ks: k.location = (0, 0, 0)
    xs = [O.sinir([k]) for k in ks]
    cer = (min(b[0] for b in xs), max(b[1] for b in xs), min(b[2] for b in xs), max(b[3] for b in xs))
    for i, k in enumerate(ks):
        O.cek([k], f"alev_{i}", 384, cerceve=cer, pay=0.05, ornek=32)

def set_pilot():
    O.sifirla(STIL)
    p = M.pilot()
    p.rotation_euler = (0, 0, math.radians(16))
    adlar = list(M.PILOT_IFADE)
    for i, ad in enumerate(adlar): O.ifade_sec(p, ad, kare=i + 1)   # anahtar kareler: 1..5
    cer = O.sinir([p])
    for i, ad in enumerate(adlar):
        bpy.context.scene.frame_set(i + 1)
        O.cek([p], f"pilot_{ad}", 512, cerceve=cer, pay=0.05)
    kayit_blend("pilot")
    O.ifade_sec(p, "notr"); glb(p, "pilot")

class _CokmeHepsi:
    """Gövdedeki tüm 'cokme' şekil anahtarlarını birlikte süren vekil (zarf + yük şeritleri)."""
    def __init__(self, kok):
        self.kbs = [o.data.shape_keys.key_blocks["cokme"] for o in O.alt_nesneler(kok)
                    if o.type == "MESH" and o.data.shape_keys and "cokme" in o.data.shape_keys.key_blocks]
    @property
    def value(self): return self.kbs[0].value
    @value.setter
    def value(self, v):
        for k in self.kbs: k.value = v

def _ezilme(kok, govde, zarf, ad, olcekler, ifadeler, gen):
    """olcekler: (sz, cokme) kare başına; hacim korunur: sx=sy=1/sqrt(sz)."""
    kb = _CokmeHepsi(kok)
    durum = []
    for (sz, ck), ifd in zip(olcekler, ifadeler):
        durum.append((sz, ck, ifd))
    bbs = []
    for sz, ck, ifd in durum:
        s = 1 / math.sqrt(sz); govde.scale = (s, s, sz); kb.value = ck; O.ifade_sec(kok, ifd); bbs.append(O.sinir([kok]))
    cer = (min(b[0] for b in bbs), max(b[1] for b in bbs), min(b[2] for b in bbs), max(b[3] for b in bbs))
    for i, (sz, ck, ifd) in enumerate(durum):
        s = 1 / math.sqrt(sz); govde.scale = (s, s, sz); kb.value = ck; O.ifade_sec(kok, ifd)
        O.cek([kok], f"{ad}_ezilme_{i}", gen, cerceve=cer, pay=0.04)
    govde.scale = (1, 1, 1); kb.value = 0

def set_nesne(ad):
    O.sifirla(STIL)
    kok = M.zeplin() if ad == "zeplin" else M.balon()
    govde = bpy.data.objects[ad + "_govde"]; zarf = bpy.data.objects["zarf" if ad == "zeplin" else "balon_zarf"]
    gen = 640 if ad == "zeplin" else 448
    for ifd in M.NESNE_IFADE:
        O.ifade_sec(kok, ifd)
        if ifd == "ezik":
            _CokmeHepsi(kok).value = 0.7; s = 1 / math.sqrt(0.78); govde.scale = (s, s, 0.78)
        O.cek([kok], f"{ad}_{ifd}", gen)
        _CokmeHepsi(kok).value = 0; govde.scale = (1, 1, 1)
    # ezilme dizisi (çarpma → geri sıçrama → toparlanma)
    _ezilme(kok, govde, zarf, ad, [(1.0, 0.0), (0.70, 1.0), (1.14, 0.0), (0.95, 0.15)], ["normal", "ezik", "saskin", "normal"], gen)
    kayit_blend(ad); O.ifade_sec(kok, "normal"); glb(kok, ad)

def set_bulut():
    O.sifirla(STIL)
    for i in range(3):
        b = M.bulut(i, seed=3 + i); b.location = (0, 0, -8 * i)
        O.cek([b], f"bulut_{i}", [384, 512, 640][i])

def set_efekt():
    O.sifirla(STIL)
    ks = [M.patlama(i) for i in range(3)]
    cer = None
    xs = [O.sinir([k]) for k in ks]; cer = (min(b[0] for b in xs), max(b[1] for b in xs), min(b[2] for b in xs), max(b[3] for b in xs))
    for i, k in enumerate(ks): O.cek([k], f"efekt_yildiz_{i}", 448, cerceve=cer, pay=0.04, ornek=48)
    for k in ks: k.hide_render = True
    ts = [M.toz(i) for i in range(3)]
    xs = [O.sinir([k]) for k in ts]; cer = (min(b[0] for b in xs), max(b[1] for b in xs), min(b[2] for b in xs), max(b[3] for b in xs))
    for i, k in enumerate(ts): O.cek([k], f"efekt_toz_{i}", 384, cerceve=cer, pay=0.04, ornek=48)
    ss = [M.ses_duvari(i) for i in range(2)]
    xs = [O.sinir([k]) for k in ss]; cer = (min(b[0] for b in xs), max(b[1] for b in xs), min(b[2] for b in xs), max(b[3] for b in xs))
    for i, k in enumerate(ss): O.cek([k], f"efekt_ses_{i}", 448, cerceve=cer, pay=0.06, ornek=48)

SETLER = {"stil": set_stil, "roket": set_roket, "alev": set_alev, "pilot": set_pilot,
          "zeplin": lambda: set_nesne("zeplin"), "balon": lambda: set_nesne("balon"), "bulut": set_bulut, "efekt": set_efekt}
if SET == "hepsi":
    for k in ("roket", "alev", "pilot", "zeplin", "balon", "bulut", "efekt"): SETLER[k]()
else:
    SETLER[SET]()
