# -*- coding: utf-8 -*-
"""Son Durak: Plüton — başsız 2B uçuş + ekonomi simülasyonu.

Oyunun JS kodu bu dosyadaki kuralları birebir kullanacak: sabit dt = 1/120, tohumlu rastgele
(random.Random(seed)), tüm sayılar AYAR / TIPLER / GELISTIRME tablolarında.

Kullanım:
  python ucus_sim.py            # tam ölçüm (5 bot × 20 tohum × 60 tur; ayar ilk 25 tur, gerisi taslak), markdown tabloları basar
  python ucus_sim.py hizli      # 5 tohumla kısa deneme
  python ucus_sim.py ozet [n]   # ayar döngüsü: ilk 25 turun kısa özeti, beceri farkı, hic maks testi (n tohum, vars. 12)
  python ucus_sim.py tek 7 iyi  # tek tur (tohum 7, iyi bot, geliştirmesiz), olay günlüğü
  python ucus_sim.py egri       # güç eğrisi: tüm geliştirmeler maks'ın %f'sinde iken hic/iyi tur özeti
  python ucus_sim.py esleme     # iç hız/irtifa -> gösterge birimi tablosu
  python ucus_sim.py kontrol    # değişmez testleri (g_etkin >= 0, sekme büyüklüğü/açısı, ekran yoğunluğu, irtifa eşlemesi)
Para birimi: altın jeton.
"""
import math, random, sys, json
from multiprocessing import Pool

# ---------------------------------------------------------------- ayar (tek yerde)
# v < v_yörünge iken ek sürükleme: y0'da 0, y1'de ve üstünde 'ek' b/s² (doğrusal). Yüksekte asılı kalan yavaş uçuşlar bitsin
SONUM_ALT = dict(y0=300.0, y1=3500.0, ek=7.0)

AYAR = dict(
    dt=1 / 120,
    g=30.0,                    # taban yerçekimi b/s²
    v_yorunge=600.0,
    v_kacis=600.0 * math.sqrt(2),
    g_yatay=True,              # g_etkin formülünde v = yatay hız (fiziksel doğru; dikey atışla g "kapatılamaz")
    rho_olcek=400.0,           # ρ(y) = e^(−y/400)
    c_suruk=0.00012,           # a = −c·ρ·Cd·v²
    cd_ses=((85, 1.0), (100, 2.4), (115, 1.1)),   # transonik tepe (doğrusal ara değer)
    ses_v=115.0, ses_sure=0.3, isi_duvar_v=250.0, duvar_sure=1.0, isi_sure=2.5,   # ısı duvarı: 250 üstünde 2,5 s (S5 3 s önerdi; 40 tohumda 3 s iyi botu tur 13'e itti)
    uzay_kosul=True,           # yörünge ve kaçış yalnız y ≥ y_karman'da sayılır. Hız duvarı = eşiğin üstünde duvar_sure kadar kesintisiz kalmak
    isi_v=250.0, isi_y=1000.0,  # ısı duvarı yalnız atmosferde (y < tropopoz) kırılır
    isi_hiz=3.0,               # ısı/s = (v − 250) × ρ(y) × 3 × (1 − 0,15·kalkan) (S5: 2→3)
    isi_sogu=25.0,             # ısı/s soğuma
    isi_cd=2.5,                # ısı ≥ 100 iken Cd çarpanı (aşırı ısınma freni), 70'e soğuyunca kalkar
    y_karman=3500.0, y_tropopoz=1000.0,   # 2. ayar: Kármán 3000→3500 (hedef tur 18–19)
    sonum=22.0,                # yörünge sönümü b/s² (y ≥ y_karman ve v < v_kaçış); 14→22: turlar doğal bitsin
    sonum_yorunge=22.0,        # aynı sönüm v ≥ v_yörünge iken (SEÇENEK: düşürülürse yörünge öne gelir, RAPOR §6)
    sonum_alt=SONUM_ALT,       # v < v_yörünge iken üst atmosfer/uzayda ek sürükleme (yukarıda)
    ust_sonum=(2900.0, 6.0),   # y > 2900 ve yükselirken ek dikey sönüm b/s² (8. oturum: bilim balonu 40° fazla irtifası)
    v_dur=25.0, dur_sure=2.0,  # hız 2 s boyunca 25'in altında → kademe ya da tur sonu
    vx_dur=110.0,              # ya da tropopoz üstünde yatay hız 2 s boyunca bunun altında (yüksekte asılı kaldı) → aynı kural
    tur_tavan=65.0,            # tur süresi tavanı (rampa + uçuş, s) — yalnız emniyet; turların ≤ %10'u buna çarpmalı
    r_roket=4.0,
    # rampa
    rampa_y=60.0, rampa_aci=38.0, rampa_v=70.0, rampa_v_sv=16.0,   # 12→16: üst sınır 190→230 (zayıf oyuncu tabanı)
    rampa_oto=3.0,             # dokunmazsan 3 s sonra otomatik "iyi"
    kalite=dict(mukemmel=1.30, iyi=1.0, zayif=0.80),
    mukemmel_bolge=0.12, mukemmel_bolge_sv=0.024,
    mukemmel_bonus_sv=0.05,    # +%30 → +%55
    acilis_sekme_dt=1.8,       # açılış zeplini: kalkıştan 1,6 s sonraki rota noktasına konur ("vay" garantisi)
    # sekme
    k_tavan=0.92, k_sv=0.012,  # Sekme verimi: k + 0,012/sv, tavan 0,92
    tekrar_sure=2.0,           # aynı nesne 2 s içinde ikinci kez etki vermez
    # dalış
    dalis_aci=70.0, dalis_koni=(66.0, 76.0), dalis_menzil=150.0, dalis_menzil_k=1.0,   # koni içinde hedef varsa ona nişan alır. 60–80→66–76: zamanlama beceri farkı yaratsın
    dalis_itki=14.0, dalis_itki_sv=4.0, dalis_sure=1.2,   # sv 2,2→4,0 (14→54): geç oyun hızı, yörünge ~tur 25–27
    bos_dalis_sure=0.4, bos_dalis_kayip=0.0, bos_dalis_aci=(-10.0, 45.0),   # S6: konide hedef yoksa dalış 0,4 s sürer, sonra burun eski yönüne (−10..+45°) döner, |v| = dalış öncesi × (1 − kayıp); S6'daki 0,10 orta botu −%15 yavaşlattı, 0 seçildi
    dalis_kap=2, gosterge_bas=1.0,   # tur yarı dolu göstergeyle (1 dalış) başlar
    gosterge_tr=0.08, gosterge_diger=0.13, gosterge_m=0.10,   # tr 0,25→0,08, diğer 0,20→0,13: dalış zinciri kendini sonsuza dek beslemesin
    gosterge_firsat=0.30, gosterge_sv=0.10,
    mukemmel_sekme=0.10, mukemmel_sekme_tavan=12.0,
    # kademe son şansı
    kademe_y=25.0, kademe_vy=78.0, kademe_vy_sv=6.5, kademe_vx=15.0, kademe_vx_sv=6.5, kademe_x_kayip=0.9,   # itki/sv 5→6,5 (+%30)
    kademe_ust_vy_kat=0.5,     # S1: tropopoz üstünde ateşlenen kademe ileri ağırlıklı: vy × 0,5 (vx aynı formül)
    kademe_cd=0.85,            # her ayrılma sürüklemeyi %15 azaltır
    son_ates=19.5,             # Son ateşleme: +19,5/sv (15'ten +%30), yatay < 30 ve kademe yokken 1 kez
    # kamera / ekran (dikey telefon)
    ekran_w0=150.0, ekran_wk=0.5, ekran_wmax=500.0, ekran_oran=2.1,
    ekran_hedef=7,             # ekranda her an hedef nesne sayısı (6–10)
    romorkor_garanti=False,    # SEÇENEK (kapalı): uçuşta romorkor_y ilk geçilince römorkör garanti çıkar (RAPOR §6)
    romorkor_y=1500.0,         # uzay römorkörü yalnız bu yüksekliğin üstünde çıkar (üst atmosfer sonu / yörünge girişi)
    seyrek=dict(y=1000.0, t0=30.0, adim=10.0, kat=0.9, en_az=0.5),   # S8: y < 1.000'de (300 yetmedi: tavana çarpanlar bulut bandında) trambolin ağırlığı uçuşun 30. s'sinden sonra her 10 s'de ×0,9 (en az ×0,5)
    garanti_pay=25.0,          # sekme garantisi: rotanın en az 25 b altında, y ≥ 25
    # fırsat / ölümcül aralıkları (süre)
    firsat_ara=30.0, firsat_ara_sv=0.25, firsat_min=6.0,   # tür başına ortalama aralık /(1+0,25·sv), türler arası ≥ firsat_min s
    firsat_tur_max=5,          # bir turda en çok bu kadar fırsat (uzun uçuş kendini beslemesin)
    firsat_tur_muaf=('romorkor',),   # sınırdan muaf (yalnız romorkor_y üstünde çıkar; yörüngenin anahtarı)
    olumcul_ara=22.0, olumcul_uyari=1.5, olumcul_rota=True,  # kullanıcı kararı: rotaya konabilir, ≥1,2 s uyarı
    # ekonomi
    kombo_sure=3.0, kombo_sure_sv=0.5, kombo_adim=0.05, kombo_tavan=2.0, kombo_tavan_sv=0.33,
    carpan_tavan=4.0,          # tüm çarpanların çarpımı en çok ×4
    bant_carpan=((1000.0, 2.4), (3500.0, 4.3)),   # S3 (öneri 1,8 · 3,0; ayarla 2,4 · 4,3): irtifa bandı çarpanı (y ≥ eşik → ×), nesne ve km ödülüne; carpan_tavan dışında
    izlenme_sv=0.10,
    odul_kat=0.10,             # izlenme → jeton çevrimi (KULLANICI KARARI bekliyor; değiştirme)
    nesne_prim=2.8,            # nesne ödülüne sponsor primi (çevrimden bağımsız). S4 2,4→2,0 önerdi; geliri hedefin yarısına düşürdü, ayarla 2,8
    rakip_odul=0.2,             # rampa zeplin vuruşu: hasar × 0,2 jeton. S4 0,6→0,45 önerdi; tur 1 kazancının büyük payı olduğu için 0,2
    km_odul=75.0,              # iç km (1.000 b) başına jeton, bant çarpanıyla (S3). S4 55 önerdi, ayarla 75
    taban_odul=25.0, sure_odul=0.0,   # sponsor tabanı: tur başına sabit (para sıfırken bile kazanç > 0). Saniye ödemesi kaldırıldı (uzun turu ödüllendirmesin)
    firsat_guc_kat=dict(fisek=2.8, konfeti=2.8, jet=3.5, romorkor=5.5),   # S7: römorkör 4,5→5,5. FIRSATLAR güçlerinin çarpanı (ICERIK değerleri × bu); yörünge turunu bu ayarlar
    fiyat_us=1.55,
    ayar_tur=25,               # denge yalnız ilk 25 tur için ayarlı; 26–60 taslak
)

# duvarlar: (ad, ilk ödül, sonraki oran)
DUVARLAR = dict(ses=300, tropopoz=600, isi=1500, karman=3000, yorunge=6000, kacis=15000)
RAKIPLER = [(700, 500), (1100, 1500), (1800, 4000), (3200, 8000), (5200, 15000)]   # (can, nakavt ödülü)

# ---------------------------------------------------------------- nesne türleri
# sekme açısı (aci): trambolinler 40–55° (roketi yukarı çevirir); yalnız habitat (ayrı sınıf: kayma yüzeyi) 15°
# sinif: tr = trambolin, yv = yavaşlatıcı, fr = fırsat (hızlandırıcı/toplanır), ol = ölümcül
_YK = AYAR['y_karman']   # uzay bantları Kármán eşiğinden türer
TIPLER = {
    'balon':   dict(sinif='tr', r=12,  ymin=40,   ymax=200,  w=3.0, k=0.80, aci=50, yan=0.06, odul=15, omur=3, acilis=1),
    'parti':   dict(sinif='tr', r=10,  ymin=30,   ymax=150,  w=2.0, k=0.70, aci=42, yan=0.02, odul=10, omur=2, acilis=1),
    'zeplin':  dict(sinif='tr', r=22, ymin=80,   ymax=500,  w=1.2, k=0.85, aci=45, yan=0.10, odul=40, omur=3, acilis=1),
    'dron':    dict(sinif='tr', r=11,  ymin=60,   ymax=450,  w=0.6, k=0.80, aci=55, yan=0.25, odul=60, omur=1, acilis=2, ek_vy=15),
    'sicak':   dict(sinif='tr', r=20, ymin=250,  ymax=950,  w=1.0, k=0.85, aci=40, yan=0.08, odul=30, omur=3, acilis=9),
    # bilim 40° (8. oturum kararı); fazla irtifa AYAR['ust_sonum'] ile kesilir
    'bilim':   dict(sinif='tr', r=26, ymin=800,  ymax=_YK - 100, w=1.2, k=0.85, aci=40, yan=0.03, odul=30, omur=3, acilis='tropopoz'),
    # habitat: ayrı sınıf "kayma yüzeyi" (sığ 15°, fizik trambolinle aynı; görseli kullanıcı onayında)
    'habitat': dict(sinif='tr', kayma=True, r=26, ymin=_YK, ymax=9000, w=0.8, k=0.90, aci=15, yan=0.05, odul=60, omur=3, acilis='karman'),
    'marti':   dict(sinif='yv', r=13, ymin=25,   ymax=180,  w=3.0, kayip=0.06, odul=20, acilis=1),
    'ucurtma': dict(sinif='yv', r=7,  ymin=40,   ymax=220,  w=1.5, kayip=0.02, ip=0.15, odul=6, acilis=1),
    'afis':    dict(sinif='yv', r=14, ymin=60,   ymax=200,  w=0.4, kayip=0.35, odul=25, acilis=4, ip_tip=True),
    'sonde':   dict(sinif='yv', r=6,  ymin=50,   ymax=700,  w=1.0, kayip=0.02, odul=8, acilis=5),
    'goktasi': dict(sinif='yv', r=12, ymin=1000, ymax=_YK - 100, w=0.8, kayip=0.05, odul=20, acilis='tropopoz'),
    'uydu':    dict(sinif='yv', r=10, ymin=_YK + 100, ymax=9000, w=1.0, kayip=0.12, odul=50, acilis='karman'),
    'cop':     dict(sinif='yv', r=6,  ymin=_YK, ymax=9000, w=2.0, kayip=0.08, odul=15, acilis='karman'),
}
# fırsat nesneleri (satın alınınca). guc = sv0 değeri, guc_sv = seviye başına
FIRSATLAR = {
    'yakit':    dict(r=9,  odul=20, guc=1, guc_sv=0.25, f='F1'),    # +dalış hakkı
    'fisek':    dict(r=10, odul=40, guc=60, guc_sv=10, aci=35, sure=1.2, f='F2'),
    'konfeti':  dict(r=10, odul=35, guc=45, guc_sv=10, f='F3'),
    'termal':   dict(r=60, odul=3,  guc=8, guc_sv=1.6, sure=3.0, f='F4'),   # +b/s² yukarı, sütun
    'jet':      dict(r=30, odul=5,  guc=12, guc_sv=1.2, V=180, V_sv=24, uzun=1500, f='F6'),
    'romorkor': dict(r=12, odul=120, guc=40, guc_sv=8, f='F10'),
}
KARGO = dict(r=22, kanat=40, odul=200, kanat_kayip=0.30, ymin=300, ymax=600, acilis=6)

# ---------------------------------------------------------------- hangar (ICERIK §6, §3)
# ad: (en çok sv, taban fiyat | sabit liste, görünür tur)
GELISTIRME = {
    'rampa':      (10, 60, 1), 'bolge': (5, 80, 2), 'm_bonus': (5, 200, 14), 'zeplin_h': (8, 120, 7),
    'verim':      (8, 90, 1), 'aero': (8, 150, 4), 'burun': (6, 120, 5), 'ip': (4, 100, 4),
    'kalkan':     (6, 1500, 8), 'zirh': (3, 2500, 6),
    'kademe_n':   (2, [600, 6000], 12), 'kademe_itki': (8, 200, 1),
    'dalis':      (10, 70, 1), 'dolum': (8, 90, 2), 'kapasite': (2, [900, 7000], 23), 'son_ates': (4, 400, 24),
    'izlenme':    (10, 150, 1), 'kombo_s': (5, 120, 9), 'kombo_t': (3, 1000, 20),
    # fırsatlar: aç (tek), sıklık (4), güç (5)
    'yakit_ac': (1, [150], 2), 'yakit_s': (4, 100, 2), 'yakit_g': (5, 120, 2),
    'fisek_ac': (1, [300], 3), 'fisek_s': (4, 150, 3), 'fisek_g': (5, 160, 3),
    'konfeti_ac': (1, [450], 6), 'konfeti_s': (4, 180, 6), 'konfeti_g': (5, 200, 6),
    'termal_ac': (1, [400], 8), 'termal_s': (4, 150, 8), 'termal_g': (5, 170, 8),
    'jet_ac': (1, [1200], 11), 'jet_s': (4, 300, 11), 'jet_g': (5, 350, 11),
    'romorkor_ac': (1, [5000], 21), 'romorkor_s': (4, 800, 21), 'romorkor_g': (5, 900, 21),
}


def fiyat(ad, sv):
    mx, taban, _ = GELISTIRME[ad]
    if sv >= mx:
        return None
    if isinstance(taban, list):
        return taban[sv]
    return round(taban * AYAR['fiyat_us'] ** sv)


# ---------------------------------------------------------------- gösterge eşlemeleri (tek yönlü)
def hiz_gosterge(v):
    """iç hız b/s → gerçek m/s. v ≤ 600: 343·(v/100)^p (p, 600→7.900 m/s'yi tutturur); üstü doğrusal (849 → 11,2 km/s)."""
    p = math.log(7900 / 343) / math.log(6)
    if v <= 600:
        return 343 * (max(v, 0) / 100) ** p
    return 7900 * v / 600


IRTIFA_TABLO = [(0, 0), (25, 0.2), (300, 2), (1000, 12), (AYAR['y_karman'], 100), (AYAR['y_karman'] + 3000, 400)]


def irtifa_km(y):
    t = IRTIFA_TABLO
    if y <= 0:
        return 0.0
    for (a, ka), (b, kb) in zip(t, t[1:]):
        if y <= b:
            return ka + (kb - ka) * (y - a) / (b - a)
    return t[-1][1] + (y - t[-1][0]) * 0.1


def cd_ses(v):
    t = AYAR['cd_ses']
    if v <= t[0][0]:
        return t[0][1]
    for (a, ca), (b, cb) in zip(t, t[1:]):
        if v <= b:
            return ca + (cb - ca) * (v - a) / (b - a)
    return t[-1][1]


# ---------------------------------------------------------------- nesne
class Nesne:
    __slots__ = ('tip', 'x', 'y', 'r', 'sinif', 'vurus', 'son_t', 'aktif', 'ek', 'dogus')

    def __init__(s, tip, x, y, sinif, r, ek=None, dogus=0.0):
        s.tip, s.x, s.y, s.sinif, s.r = tip, x, y, sinif, r
        s.vurus, s.son_t, s.aktif, s.ek, s.dogus = 0, -99.0, True, ek or {}, dogus


# ---------------------------------------------------------------- uçuş
class Ucus:
    """Tek tur. Mantık ve fizik burada; bot dışarıdan dokun() çağırır."""

    def __init__(s, seed, sv, tur=1, bayrak=None, bot='hic', rakip_hp=None):
        s.A = A = AYAR
        s.rng = random.Random(seed)
        s.sv = sv                      # geliştirme seviyeleri dict
        s.tur = tur
        s.bayrak = bayrak or set()     # kampanyada açılan eşikler (tropopoz, karman)
        s.bot = bot
        s.t = 0.0                      # uçuş zamanı (kalkıştan beri)
        s.rampa_t = 0.0
        s.nesneler = []
        s.aday = []
        s.olay = []
        s.bitti = None
        # istatistik
        s.st = dict(sekme=0, mukemmel=0, temas=0, son_sans=0, dalis=0, max_v=0.0, max_y=0.0, kazanc=0.0,
                    vay_t=None, isi_s=0.0, ekran_n=0, ekran_ornek=0, ekran_min=99, ekran_az=0, kademe_yuk=[], mesafe_g=0.0, olumcul=0, olumcul_kademe=0, firsat=0, firsat_tut=0, kademe_kalan=0)
        s.duvar = set()
        s.kombo_n, s.kombo_t = 0, -99.0
        s.isi, s.isi_kilit = 0.0, False
        s.isi_ok = 0.0
        s.ses_t = s.yor_t = s.kac_t = 0.0
        s.dur_t = 0.0
        s.gosterge = A['gosterge_bas']
        s.dalis_t = None
        s.bos = None                   # S6: boş dalış [kalan s, eski açı, eski |v|]
        s.kademe = 1 + sv.get('kademe_n', 0)
        s.cd_kat = 1.0
        s.son_ates_hak = sv.get('son_ates', 0) > 0
        s.firsat_zaman = {}
        s.son_firsat_t = -99.0
        s.firsat_n = 0                 # bu turda çıkan fırsat sayısı
        s.olumcul_zaman = A['olumcul_ara'] * (0.5 + s.rng.random())
        s.itis = None                  # sürekli itiş (fişek)
        s.termal_t = 0.0
        s.yon_t = 0.0
        s.garanti_t = 0.0
        s.cam_v = 0.0
        s.rakip_hp = rakip_hp
        s.rakip_hasar = 0.0
        s.x, s.y, s.vx, s.vy = 0.0, A['rampa_y'], 0.0, 0.0
        s.tepe_rampa = A['rampa_y']
        s.kad_izle, s.kad_y0 = None, 0.0

    # ---------- yardımcılar
    def ekran(s):
        A = s.A
        W = min(A['ekran_wmax'], A['ekran_w0'] + A['ekran_wk'] * s.cam_v)
        H = W * A['ekran_oran']
        cy = max(s.y, H / 2 - 10)
        return s.x - W / 3, s.x + 2 * W / 3, cy - H / 2, cy + H / 2, W, H

    def acik(s, tip):
        a = TIPLER[tip]['acilis']
        if a == 'tropopoz':
            return 'tropopoz' in s.bayrak
        if a == 'karman':
            return 'karman' in s.bayrak
        return s.tur >= a

    def k_etkin(s, k):
        return min(s.A['k_tavan'], k + s.A['k_sv'] * s.sv.get('verim', 0))

    def bant(s):
        """S3: irtifa bandı ödül çarpanı (y < 1.000 ×1; üst atmosfer ×1,8; uzay ×3)."""
        k = 1.0
        for y0, c in s.A['bant_carpan']:
            if s.y >= y0:
                k = c
        return k

    def odul(s, miktar, kombo=True):
        A = s.A
        if kombo:
            ks = A['kombo_sure'] + A['kombo_sure_sv'] * s.sv.get('kombo_s', 0)
            s.kombo_n = s.kombo_n + 1 if s.t - s.kombo_t <= ks else 0
            s.kombo_t = s.t
        tavan = A['kombo_tavan'] + A['kombo_tavan_sv'] * s.sv.get('kombo_t', 0)
        kc = min(tavan, 1 + A['kombo_adim'] * s.kombo_n)
        carp = min(A['carpan_tavan'], kc * (1 + A['izlenme_sv'] * s.sv.get('izlenme', 0)))
        s.st['kazanc'] += miktar * carp * A['odul_kat'] * A['nesne_prim'] * s.bant()

    def gosterge_ekle(s, m):
        cap = s.A['dalis_kap'] + s.sv.get('kapasite', 0)
        s.gosterge = min(cap, s.gosterge + m * (1 + s.A['gosterge_sv'] * s.sv.get('dolum', 0)))

    def log(s, *a):
        s.olay.append((round(s.t, 2),) + a)

    # ---------- rampa
    def kalkis(s, kalite, rampa_t):
        A = s.A
        s.rampa_t = rampa_t
        v = A['rampa_v'] + A['rampa_v_sv'] * s.sv.get('rampa', 0)
        q = A['kalite'][kalite]
        if kalite == 'mukemmel':
            q += A['mukemmel_bonus_sv'] * s.sv.get('m_bonus', 0)
        v *= q
        a = math.radians(A['rampa_aci'])
        s.vx, s.vy = v * math.cos(a), v * math.sin(a)
        s.v_kalkis = v
        s.kalite = kalite
        ge = s.g_etkin(s.vx)
        s.tepe_rampa = A['rampa_y'] + s.vy ** 2 / (2 * ge)
        # rakip zeplini (rampa yanı)
        if s.rakip_hp is not None:
            h = v * {'mukemmel': 1.0, 'iyi': 0.4, 'zayif': 0.0}[kalite] * (1 + 0.15 * s.sv.get('zeplin_h', 0))
            s.rakip_hasar += h
            s.st['kazanc'] += h * A['rakip_odul']
            s.st['kazanc_rakip'] = h * A['rakip_odul']
        s.ilk_doldur()
        # açılış zeplini: "vay" anı garantisi
        px, py = s.rota_nokta(A['acilis_sekme_dt'])
        z = TIPLER['zeplin']
        s.nesneler.append(Nesne('zeplin', px + 4, max(65.0, py - z['r'] * 0.5), 'tr', z['r']))

    def g_etkin(s, vx, vy=0.0):
        A = s.A
        v = abs(vx) if A['g_yatay'] else math.hypot(vx, vy)
        return A['g'] * max(0.0, 1 - (v / A['v_yorunge']) ** 2)

    def rota_nokta(s, tau):
        """Pasif rota (dalışsız, sürüklemesiz yaklaşık) üzerinde tau s sonraki nokta."""
        ge = s.g_etkin(s.vx, s.vy)
        return s.x + s.vx * tau, s.y + s.vy * tau - 0.5 * ge * tau * tau

    def rota(s, sure=6.0, ad=0.1):
        pts = []
        x, y, vx, vy = s.x, s.y, s.vx, s.vy
        t = 0.0
        while t < sure:
            ge = s.g_etkin(vx, vy)
            vy -= ge * ad
            x += vx * ad
            y += vy * ad
            t += ad
            pts.append((x, y))
            if y < s.A['kademe_y']:
                break
        return pts

    # ---------- dünya yönetmeni (ekran başına yoğunluk)
    def seyrek(s, y):
        """S8: uzun uçuşta alçak bantta trambolin ağırlığı çarpanı (1 → en az 0,5)."""
        Sy = s.A['seyrek']
        return max(Sy['en_az'], Sy['kat'] ** int(max(0.0, s.t - Sy['t0']) // Sy['adim'])) if y < Sy['y'] else 1.0

    def tip_sec(s, y, sadece_tr=False):
        sk = s.seyrek(y)
        tipler = [(n, T['w'] * (sk if T['sinif'] == 'tr' else 1.0)) for n, T in TIPLER.items()
                  if T['ymin'] <= y <= T['ymax'] and s.acik(n) and (not sadece_tr or T['sinif'] == 'tr')]
        if not tipler:
            return None
        top = sum(w for _, w in tipler)
        r = s.rng.random() * top
        for n, w in tipler:
            r -= w
            if r <= 0:
                return n
        return tipler[-1][0]

    def ekle(s, tip, x, y):
        T = TIPLER[tip]
        s.nesneler.append(Nesne(tip, x, y, T['sinif'], T['r'], dogus=s.t))

    def ilk_doldur(s):
        s.yonet(ilk=True)

    def yonet(s, ilk=False):
        A = s.A
        vl, vr, vb, vt, W, H = s.ekran()
        # temizlik
        s.nesneler = [o for o in s.nesneler if o.x > vl - W and abs(o.y - (vb + vt) / 2) < 2.5 * H and
                      (o.aktif or s.t - o.son_t < 0.5)]
        # bölge: ekran + önünde bir ekran, üstte/altta %30
        rl, rr = vl, vr + W
        rb, rt = max(25.0, vb - 0.3 * H), vt + 0.3 * H
        if rt <= rb:
            return
        yogun = A['ekran_hedef'] / (W * max(1.0, vt - max(25.0, vb)))
        hedef = yogun * (rr - rl) * (rt - rb)
        say = sum(1 for o in s.nesneler if o.sinif in ('tr', 'yv') and rl <= o.x <= rr and rb <= o.y <= rt)
        eksik = int(hedef - say)
        for _ in range(max(0, eksik)):
            for _d in range(8):
                x = rl + s.rng.random() * (rr - rl)
                y = rb + s.rng.random() * (rt - rb)
                if ilk or not (vl <= x <= vr and vb <= y <= vt):
                    break
            else:
                continue
            tip = s.tip_sec(y)
            if tip:
                s.ekle(tip, x, y)

    def garanti(s):
        """Dalış menzilinde (pasif rotanın altında, y ≥ 25) en az 1 trambolin."""
        pts = s.rota()
        if len(pts) < 3:
            return
        sk = s.seyrek(s.y)
        if sk < 1.0 and s.rng.random() > sk:   # S8: seyrelme garantiyi de kapsar
            return
        x0, x1 = s.x + 20, pts[-1][0]
        if x1 - x0 < 20:
            return
        pay = s.A['garanti_pay']
        for o in s.nesneler:
            if o.sinif == 'tr' and o.aktif and x0 <= o.x <= x1:
                # rota yüksekliği
                for px, py in pts:
                    if px >= o.x:
                        if 25 <= o.y <= py - pay * 0.6:
                            return
                        break
        # yoksa koy: rotanın uzak yarısında, ekran dışına yakın
        vl, vr, vb, vt, W, H = s.ekran()
        aday = [(px, py) for px, py in pts if px > x0 and py - pay > 30]
        if not aday:
            return
        dis = [p for p in aday if p[0] > vr] or aday[len(aday) // 2:]
        px, py = dis[s.rng.randrange(len(dis))]
        y = 30 + s.rng.random() * (py - pay - 30)
        tip = s.tip_sec(y, sadece_tr=True)
        if tip is None:  # bu yükseklikte açık trambolin yok → en yakın geçerli yükseklik
            for n, T in TIPLER.items():
                if T['sinif'] == 'tr' and s.acik(n) and T['ymin'] <= py - pay:
                    tip, y = n, min(py - pay, max(T['ymin'], y))
            if tip is None:
                return
            y = min(y, TIPLER[tip]['ymax'])
        s.ekle(tip, px, y)
        s.st['garanti'] = s.st.get('garanti', 0) + 1

    def firsat_yonet(s):
        A = s.A
        for ad, F in FIRSATLAR.items():
            if not s.sv.get(ad + '_ac'):
                continue
            ara = A['firsat_ara'] / (1 + A['firsat_ara_sv'] * s.sv.get(ad + '_s', 0))
            if ad not in s.firsat_zaman:
                s.firsat_zaman[ad] = ara * (0.3 + 0.7 * s.rng.random())
            if ad == 'romorkor' and A['romorkor_garanti'] and not s.st.get('rom_garanti') and s.y >= A['romorkor_y']:
                s.st['rom_garanti'] = 1            # seçenek: romorkor_y ilk geçilişte römorkör hemen gelir
                s.firsat_zaman[ad] = s.t
            if s.t < s.firsat_zaman[ad] or s.t - s.son_firsat_t < A['firsat_min']:
                continue
            if s.firsat_n >= A['firsat_tur_max'] and ad not in A['firsat_tur_muaf']:
                continue
            # bant koşulları
            if ad == 'romorkor' and s.y < A['romorkor_y']:
                continue
            if ad == 'termal' and s.y > 300:
                continue
            if ad == 'jet' and not (250 < s.y < 800):
                continue
            s.firsat_zaman[ad] = s.t + ara * (0.7 + 0.6 * s.rng.random())
            s.son_firsat_t = s.t
            s.firsat_n += ad not in A['firsat_tur_muaf']
            tau = 1.6 + s.rng.random()
            px, py = s.rota_nokta(tau)
            if ad == 'termal':
                s.nesneler.append(Nesne(ad, px, 140, 'bant', 60, dict(w=60), s.t))
            elif ad == 'jet':
                yc = min(650, max(400, py))
                s.nesneler.append(Nesne(ad, px, yc, 'bant', 30, dict(L=F['uzun']), s.t))
            else:
                py = max(30.0, py + s.rng.gauss(0, 12))
                s.nesneler.append(Nesne(ad, px, py, 'fr', F['r'], dogus=s.t))

    def olumcul_yonet(s):
        A = s.A
        if s.tur < KARGO['acilis'] or s.t < s.olumcul_zaman:
            return
        if not (200 < s.y < 750):
            return
        s.olumcul_zaman = s.t + A['olumcul_ara'] * (0.8 + 0.4 * s.rng.random())
        tau = A['olumcul_uyari'] + 0.5 + s.rng.random()   # uyarı ≥ 1,2 s önce görünür
        px, py = s.rota_nokta(tau)
        if A['olumcul_rota']:
            y = min(KARGO['ymax'], max(KARGO['ymin'], py + s.rng.gauss(0, 25)))
        else:
            y = py + (70 if s.rng.random() < 0.5 else -70)
            y = min(KARGO['ymax'], max(KARGO['ymin'], y))
        s.nesneler.append(Nesne('kargo', px, y, 'ol', KARGO['r'], dict(uyari=s.t), s.t))

    # ---------- oyuncu eylemi
    def dokun(s):
        """Tek dokunuş: fırsat halkası varsa onu, yoksa dalış."""
        if s.bitti or s.dalis_t is not None:
            return False
        if s.gosterge < 1.0:
            return False
        A = s.A
        v = math.hypot(s.vx, s.vy)
        sv = v + A['dalis_itki'] + A['dalis_itki_sv'] * s.sv.get('dalis', 0)
        h = s.dalis_hedef()
        s.bos = None if h else [A['bos_dalis_sure'], math.atan2(s.vy, s.vx), v]   # S6: boş dalış toparlanır
        a = -(h[1] if h else math.radians(A['dalis_aci']))
        s.vx, s.vy = sv * math.cos(a), sv * math.sin(a)
        s.gosterge -= 1.0
        s.kad_izle = None
        s.dalis_t = 0.0
        s.st['dalis'] += 1
        s.log('dalis', round(sv))
        return True

    def dalis_hedef(s):
        """Dalış koni yardımı: 60–80° aşağı konide, menzildeki en yakın trambolin (üst kenarına nişan)."""
        A = s.A
        v = math.hypot(s.vx, s.vy)
        menzil = max(A['dalis_menzil'], A['dalis_menzil_k'] * v)
        amin, amax = math.radians(A['dalis_koni'][0]), math.radians(A['dalis_koni'][1])
        en, en_d = None, 1e18
        for o in s.nesneler:
            if o.sinif != 'tr' or not o.aktif or s.t - o.son_t < A['tekrar_sure']:
                continue
            dx, dy = o.x - s.x, s.y - (o.y + 0.5 * o.r)
            if dx <= 0 or dy <= 5:
                continue
            d = dx * dx + dy * dy
            if d > menzil * menzil or d >= en_d:
                continue
            a = math.atan2(dy, dx)
            if amin <= a <= amax:
                en, en_d = (o, a), d
        return en

    # ---------- olaylar
    def kademe_ates(s, neden):
        A = s.A
        s.kademe -= 1
        s.cd_kat *= A['kademe_cd']
        s.vx = s.vx * A['kademe_x_kayip'] + A['kademe_vx'] + A['kademe_vx_sv'] * s.sv.get('kademe_itki', 0)
        s.vy = A['kademe_vy'] + A['kademe_vy_sv'] * s.sv.get('kademe_itki', 0)
        if s.y > A['y_tropopoz']:     # S1: yüksekte (durma) ateşleme ileri ağırlıklı
            s.vy *= A['kademe_ust_vy_kat']
        s.dalis_t = None
        s.bos = None
        s.itis = None
        s.dur_t = 0.0
        s.st['son_sans'] += 1
        s.kad_izle, s.kad_y0 = s.y, s.y
        s.log('son_sans', neden, s.kademe)

    def sekme(s, o, T):
        A = s.A
        v = math.hypot(s.vx, s.vy)
        mukemmel = s.dalis_t is not None
        if mukemmel:
            yv = v + min(v * A['mukemmel_sekme'], A['mukemmel_sekme_tavan'])
            s.st['mukemmel'] += 1
        else:
            yv = v * s.k_etkin(T['k'])
        a = math.radians(T['aci'])
        s.vx, s.vy = yv * math.cos(a), yv * math.sin(a) + T.get('ek_vy', 0)
        s.dalis_t = None
        s.bos = None
        s.st['sekme'] += 1
        s.gosterge_ekle(A['gosterge_m'] if mukemmel else A['gosterge_tr'])
        # "vay": kalkıştan sonraki ilk tepe aşımı
        if s.st['vay_t'] is None:
            tepe = s.y + s.vy ** 2 / (2 * max(1e-6, s.g_etkin(s.vx)))
            if tepe > s.tepe_rampa:
                s.st['vay_t'] = s.rampa_t + s.t
        s.log('sekme', o.tip, 'M' if mukemmel else '', round(yv))

    def yavaslat(s, oran):
        oran *= (1 - 0.08 * s.sv.get('burun', 0))
        s.vx *= (1 - oran)
        s.vy *= (1 - oran)

    def firsat_al(s, o):
        A, F = s.A, FIRSATLAR[o.tip]
        g = s.sv.get(o.tip + '_g', 0)
        s.st['firsat'] += 1
        tut = s.firsat_tut(o.tip)
        if o.tip == 'yakit':
            n = 1 if g < 4 else 2
            cap = A['dalis_kap'] + s.sv.get('kapasite', 0)
            s.gosterge = min(cap, s.gosterge + n + (0.25 if g >= 2 else 0) + (0.25 if tut else 0))
        elif o.tip == 'fisek':
            guc = (F['guc'] + F['guc_sv'] * g) * A['firsat_guc_kat']['fisek']
            guc *= 1.19 if tut else 1.0     # yeşil pencerede erken patlat: kalan ×1,25 → toplam ≈ ×1,19
            sure = F['sure'] + 0.1 * g
            s.itis = [sure, guc / sure, math.radians(F['aci'])]
        elif o.tip == 'konfeti':
            guc = (F['guc'] + F['guc_sv'] * g) * A['firsat_guc_kat']['konfeti'] * (1.2 if tut else 0.7)
            a = math.radians(30)
            v = math.hypot(s.vx, s.vy)
            # itki 30° yönünde vektörel eklenir
            s.vx += guc * math.cos(a)
            s.vy = max(s.vy, 0) + guc * math.sin(a)
        elif o.tip == 'romorkor':
            guc = (F['guc'] + F['guc_sv'] * g) * A['firsat_guc_kat']['romorkor']
            a = math.radians(10 if not tut else 0)
            s.vx += guc * math.cos(a)
            s.vy += guc * math.sin(a)
        s.gosterge_ekle(A['gosterge_firsat'])
        s.odul(F['odul'])
        s.log('firsat', o.tip, 'tut' if tut else '')

    def firsat_tut(s, tip):
        """Fırsatın mini zamanlama oyunu: tutturma olasılığı BOTLAR[bot]['tut']."""
        r = s.rng.random() < BOTLAR[s.bot]['tut']
        if r:
            s.st['firsat_tut'] += 1
        return r

    def carp(s, o):
        A = s.A
        if s.t - o.son_t < A['tekrar_sure'] or not o.aktif:
            return
        o.son_t = s.t
        s.st['temas'] += 1
        s.kad_izle = None
        if o.sinif == 'tr':
            T = TIPLER[o.tip]
            ust = s.y >= o.y and s.vy < 0.35 * math.hypot(s.vx, s.vy)   # üst yarıya değiyor ve dik yükselmiyor
            if ust:
                s.sekme(o, T)
            else:
                s.yavaslat(T['yan'])
                s.gosterge_ekle(A['gosterge_diger'])
                s.dalis_t = None
                s.bos = None
            o.vurus += 1
            if o.vurus >= T['omur']:
                o.aktif = False
            s.odul(T['odul'])
        elif o.sinif == 'yv':
            T = TIPLER[o.tip]
            s.yavaslat(T['kayip'])
            if o.tip == 'marti':   # yön 2° yukarı döner, büyüklük aynı
                a = math.radians(2)
                c, si = math.cos(a), math.sin(a)
                s.vx, s.vy = s.vx * c - s.vy * si, s.vx * si + s.vy * c
            o.aktif = False
            s.gosterge_ekle(A['gosterge_diger'])
            s.odul(T['odul'])
        elif o.sinif == 'fr':
            o.aktif = False
            s.firsat_al(o)
        elif o.sinif == 'ol':
            o.aktif = False
            s.st['olumcul'] += 1
            s.odul(KARGO['odul'], kombo=False)
            if s.sv.get('zirh', 0) > 0 and not s.st.get('zirh_kullan'):
                s.st['zirh_kullan'] = 1
                s.yavaslat(0.6 - 0.15 * (s.sv['zirh'] - 1))
                s.log('zirh')
            elif s.kademe > 0:
                s.st['olumcul_kademe'] += 1
                s.kademe_ates('olumcul')     # kullanıcı kararı: çarpan kademe parçalanır, üstteki fırlar
            else:
                s.bitti = 'olumcul'
                s.log('patlama')

    def ip_kontrol(s, x_onceki):
        for o in s.aday:
            if o.aktif and o.tip in ('ucurtma', 'afis') and x_onceki < o.x <= s.x and s.y < o.y - o.r:
                if s.t - o.son_t < s.A['tekrar_sure']:
                    continue
                if o.tip == 'ucurtma':
                    o.son_t = s.t
                    o.aktif = False
                    s.st['temas'] += 1
                    s.yavaslat(TIPLER['ucurtma']['ip'] * (1 - 0.2 * s.sv.get('ip', 0)))
                    s.odul(TIPLER['ucurtma']['odul'])

    # ---------- adım
    def adim(s):
        A = s.A
        dt = A['dt']
        v = math.hypot(s.vx, s.vy)
        s.cam_v += (v - s.cam_v) * min(1.0, dt / 0.8)
        # yönetmen (10 Hz) ve aday listesi
        s.yon_t -= dt
        if s.yon_t <= 0:
            s.yon_t = 0.1
            s.yonet()
            vl, vr, vb, vt, W, H = s.ekran()
            n = sum(1 for o in s.nesneler if o.aktif and o.sinif != 'bant' and vl <= o.x <= vr and vb <= o.y <= vt)
            s.st['ekran_n'] += n
            s.st['ekran_ornek'] += 1
            s.st['ekran_min'] = min(s.st['ekran_min'], n)
            s.st['ekran_az'] += n < 4
            if s.kad_izle is not None:
                s.kad_izle = max(s.kad_izle, s.y)
                if s.vy < 0:
                    s.st['kademe_yuk'].append(s.kad_izle - s.kad_y0)
                    s.kad_izle = None
            s.firsat_yonet()
            s.olumcul_yonet()
            s.garanti_t -= 0.1
            if s.garanti_t <= 0:
                s.garanti_t = 0.25
                s.garanti()
            ul = v * 0.15 + 80
            s.aday = [o for o in s.nesneler if abs(o.x - s.x) < ul + (o.ek.get('L', 0)) and
                      (abs(o.y - s.y) < ul or o.tip in ('ucurtma', 'afis', 'termal'))]
        # kuvvetler
        ax, ay = 0.0, -s.g_etkin(s.vx, s.vy)
        if v > 1e-6:
            cd = cd_ses(v) * s.cd_kat * (1 - 0.05 * s.sv.get('aero', 0))
            # ısı
            # ısınma ∝ ρ(y)·(v − 250): alçakta hızlı, yüksekte yavaş; soğuma sürekli; 0–120 arası
            isin = max(0.0, v - A['isi_v']) * A['isi_hiz'] * math.exp(-s.y / A['rho_olcek']) * (1 - 0.15 * s.sv.get('kalkan', 0))
            s.isi = min(120.0, max(0.0, s.isi + (isin - A['isi_sogu']) * dt))
            if s.isi >= 100:
                s.isi_kilit = True
            elif s.isi < 70:
                s.isi_kilit = False
            if s.isi_kilit:
                cd *= A['isi_cd']
                s.st['isi_s'] += dt
            ad = A['c_suruk'] * math.exp(-s.y / A['rho_olcek']) * cd * v * v
            if s.y >= A['y_karman'] and v < A['v_kacis']:
                ad += A['sonum'] if v < A['v_yorunge'] else A['sonum_yorunge']
            S = A['sonum_alt']
            if v < A['v_yorunge'] and s.y > S['y0']:
                ad += S['ek'] * min(1.0, (s.y - S['y0']) / (S['y1'] - S['y0']))
            ax -= ad * s.vx / v
            ay -= ad * s.vy / v
            if s.y > A['ust_sonum'][0] and s.vy > 0:
                ay -= A['ust_sonum'][1]
        # sürekli itiş (fişek)
        if s.itis:
            s.itis[0] -= dt
            ax += s.itis[1] * math.cos(s.itis[2])
            ay += s.itis[1] * math.sin(s.itis[2])
            if s.itis[0] <= 0:
                s.itis = None
        # bantlar
        for o in s.aday:
            if o.tip == 'termal' and abs(s.x - o.x) < 60 and 25 < s.y < 250 and s.termal_t < FIRSATLAR['termal']['sure']:
                ay += FIRSATLAR['termal']['guc'] + FIRSATLAR['termal']['guc_sv'] * s.sv.get('termal_g', 0)
                s.termal_t += dt
                s.st['kazanc'] += FIRSATLAR['termal']['odul'] * dt
            elif o.tip == 'jet' and o.x <= s.x <= o.x + o.ek['L'] and abs(s.y - o.y) < 30:
                g = s.sv.get('jet_g', 0)
                V = FIRSATLAR['jet']['V'] + FIRSATLAR['jet']['V_sv'] * g
                if v < V:
                    ax += (FIRSATLAR['jet']['guc'] + FIRSATLAR['jet']['guc_sv'] * g) * A['firsat_guc_kat']['jet'] * (1 - v / V)
                s.st['kazanc'] += FIRSATLAR['jet']['odul'] * dt
        # tümleştir (yarı örtük Euler)
        x_on = s.x
        s.vx += ax * dt
        s.vy += ay * dt
        s.x += s.vx * dt
        s.y += s.vy * dt
        s.t += dt
        if s.dalis_t is not None:
            s.dalis_t += dt
            if s.dalis_t > A['dalis_sure']:
                s.dalis_t = None
        if s.bos:   # S6: boş dalış toparlanması
            s.bos[0] -= dt
            if s.bos[0] <= 0:
                lo, hi = (math.radians(x) for x in A['bos_dalis_aci'])
                a = min(hi, max(lo, s.bos[1]))
                vb = s.bos[2] * (1 - A['bos_dalis_kayip'])
                s.vx, s.vy = vb * math.cos(a), vb * math.sin(a)
                s.bos, s.dalis_t = None, None
                s.log('bos_dalis')
        # çarpışmalar
        rr = A['r_roket']
        for o in s.aday:
            if not o.aktif or o.sinif == 'bant':
                continue
            dx, dy = s.x - o.x, s.y - o.y
            rad = o.r + rr
            if o.sinif == 'ol':
                if dx * dx + dy * dy < rad * rad:
                    s.carp(o)
                elif abs(dx) < KARGO['kanat'] and abs(dy) < 4 and s.t - o.son_t > A['tekrar_sure']:
                    o.son_t = s.t
                    s.yavaslat(KARGO['kanat_kayip'])
                    s.st['temas'] += 1
                continue
            if dx * dx + dy * dy < rad * rad:
                s.carp(o)
                if s.bitti:
                    return
        s.ip_kontrol(x_on)
        v = math.hypot(s.vx, s.vy)
        st = s.st
        st['km_bant'] = st.get('km_bant', 0.0) + (s.x - x_on) * s.bant()   # S3: km ödülü bulunduğu banttan
        if v > 1e-6:   # göstergedeki mesafe: gösterge hızının yatay bileşeninin tümlevi (km)
            st['mesafe_g'] += hiz_gosterge(v) * (s.vx / v) * dt / 1000
        if v > st['max_v']:
            st['max_v'] = v
        if s.y > st['max_y']:
            st['max_y'] = s.y
        # duvarlar
        s.ses_t = s.ses_t + dt if v >= A['ses_v'] else 0.0
        if s.ses_t >= A['ses_sure']:
            s.duvar.add('ses')
        if v >= A['isi_duvar_v'] and s.y < A['isi_y'] and not s.isi_kilit:
            s.isi_ok += dt
            if s.isi_ok >= A['isi_sure']:
                s.duvar.add('isi')
        if s.y >= A['y_tropopoz']:
            s.duvar.add('tropopoz')
            s.bayrak.add('tropopoz')
        if s.y >= A['y_karman']:
            s.duvar.add('karman')
            s.bayrak.add('karman')
        uzay = s.y >= A['y_karman'] or not A['uzay_kosul']
        s.yor_t = s.yor_t + dt if v >= A['v_yorunge'] and uzay else 0.0
        if s.yor_t >= A['duvar_sure']:
            s.duvar.add('yorunge')
        s.kac_t = s.kac_t + dt if v >= A['v_kacis'] and uzay else 0.0
        if s.kac_t >= A['duvar_sure']:
            s.duvar.add('kacis')
            s.bitti = 'kacis'
            return
        # son şans, durma, yer
        if s.y < A['kademe_y'] and s.vy < 0:
            if s.kademe > 0:
                s.kademe_ates('yer')
            elif s.son_ates_hak and abs(s.vx) < 30:
                s.son_ates_hak = False
                s.vx += A['son_ates'] * s.sv['son_ates']
                s.vy = abs(s.vy) * 0.5 + 20
                s.log('son_ates')
        if v < A['v_dur'] or (abs(s.vx) < A['vx_dur'] and s.y > A['y_tropopoz']):
            s.dur_t += dt
            if s.dur_t >= A['dur_sure']:
                if s.kademe > 0:      # S1: her irtifada (KARARLAR 8. oturum: vx_dur'da önce kademe ateşlenir)
                    s.kademe_ates('durma')
                else:
                    s.bitti = 'durma'
        else:
            s.dur_t = 0.0
        if s.y <= 0:
            s.y = 0.0
            s.bitti = 'yer'
        if s.t + s.rampa_t >= A['tur_tavan']:
            s.bitti = 'sure'

    def sonuc(s):
        st = dict(s.st)
        st['sure_ucus'] = s.t
        st['sure_tur'] = s.t + s.rampa_t
        st['mesafe'] = s.x
        st['bitis'] = s.bitti
        st['son_y'], st['son_v'] = s.y, math.hypot(s.vx, s.vy)
        st['duvar'] = sorted(s.duvar)
        st['kazanc_nesne'] = st['kazanc']
        st['kazanc_km'] = st.get('km_bant', s.x) / 1000 * s.A['km_odul']
        st['kazanc'] += st.get('km_bant', s.x) / 1000 * s.A['km_odul'] + s.A['taban_odul'] + s.A['sure_odul'] * s.t
        st['temas_s'] = st['temas'] / max(1e-6, s.t)
        st['kademe_kalan'] = s.kademe
        st['rakip_hasar'] = s.rakip_hasar
        st['ekran_ort'] = st['ekran_n'] / max(1, st['ekran_ornek'])
        st['ekran_az_oran'] = st['ekran_az'] / max(1, st['ekran_ornek'])
        return st


# ---------------------------------------------------------------- botlar
# Oyuncu modelleri (tek yerde). tepki: dokunma gecikmesi aralığı (s, düzgün dağılım). gurultu: hedefin konumunu
# tahmin hatası (dx, dy her biri ±oran, nesne başına sabit). ongoru: gecikmeyi ne kadar öngörüp erken dokunduğu (0–1).
# mukemmel: mükemmel kalkış olasılığı (alt + bölge/2, üst sınırla). tut: fırsat mini oyunu. vazgec: gecikme sonunda
# hedef artık konide değilse vazgeçme olasılığı. Görüş: iyi/orta/usta yalnız ekranda görünen nesneleri görür
# (roket sol üçte birde → ileri bakış ≤ ekran genişliğinin 2/3'ü). kotu: hedefe dokunmaya çalışır ama geç ve hatalı,
# ayrıca saniyede rastgele_s amaçsız dokunuş yapar. hic: rampada bekler, uçuşta hiç dokunmaz.
BOTLAR = dict(
    hic=dict(tut=0.0),
    kotu=dict(tepki=(0.40, 0.70), gurultu=0.50, ongoru=0.2, tut=0.25, vazgec=0.3, rampa_t=(0.4, 2.0), zayif=0.25, rastgele_s=0.15),
    orta=dict(tepki=(0.25, 0.40), gurultu=0.25, ongoru=0.7, mukemmel=(0.50, 0.60), tut=0.35, vazgec=0.5, rampa_t=(0.6, 1.4)),
    iyi=dict(tepki=(0.18, 0.30), gurultu=0.10, ongoru=0.8, mukemmel=(0.80, 0.95), tut=0.50, vazgec=0.8, rampa_t=(0.8, 1.1)),
    usta=dict(tepki=(0.00, 0.05), gurultu=0.0, ongoru=1.0, mukemmel=(0.97, 0.97), tut=1.00, vazgec=1.0, rampa_t=(0.8, 1.1)),
)
BOT_SIRA = ['hic', 'kotu', 'orta', 'iyi', 'usta']


def rampa_karar(bot, rng, sv):
    """(kalite, rampa süresi)."""
    A = AYAR
    bolge = A['mukemmel_bolge'] + A['mukemmel_bolge_sv'] * sv.get('bolge', 0)
    if bot == 'hic':
        return 'iyi', A['rampa_oto']
    B = BOTLAR[bot]
    if bot == 'kotu':   # zamanlaması dağınık: mükemmel ≈ bölge genişliği, %25 zayıf
        r = rng.random()
        a, b = B['rampa_t']
        return ('mukemmel' if r < bolge else 'zayif' if r > 1 - B['zayif'] else 'iyi'), a + (b - a) * rng.random()
    p = min(B['mukemmel'][1], B['mukemmel'][0] + bolge * 0.5)
    a, b = B['rampa_t']
    return ('mukemmel' if rng.random() < p else 'iyi'), a + (b - a) * rng.random()


def gorunur_hedef(u, bot, durum, on=0.0):
    """Botun gözüyle dalış hedefi: ekranda görünen, tahmin hatalı konumu 'on' s sonraki roket konumundan
    dalış konisinde ve menzilde kalan en yakın trambolin. Oyunun koni yardımı ayrıca kendi hedefini seçer."""
    A, B = AYAR, BOTLAR[bot]
    vl, vr, vb, vt, W, H = u.ekran()
    v = math.hypot(u.vx, u.vy)
    menzil = max(A['dalis_menzil'], A['dalis_menzil_k'] * v)
    px = u.x + u.vx * on
    py = u.y + u.vy * on - 0.5 * u.g_etkin(u.vx) * on * on
    amin, amax = math.radians(A['dalis_koni'][0]), math.radians(A['dalis_koni'][1])
    gm = B['gurultu']
    hata = durum.setdefault('hata', {})
    en, en_d = None, 1e18
    for o in u.nesneler:
        if o.sinif != 'tr' or not o.aktif or u.t - o.son_t < A['tekrar_sure']:
            continue
        if not (vl <= o.x <= vr and vb <= o.y <= vt):
            continue
        k = id(o)
        if k not in hata:
            hata[k] = (durum['rng'].uniform(-gm, gm), durum['rng'].uniform(-gm, gm)) if gm else (0.0, 0.0)
        ex, ey = hata[k]
        dx = (o.x - px) * (1 + ex)
        dy = (py - (o.y + 0.5 * o.r)) * (1 + ey)
        if dx <= 0 or dy <= 5:
            continue
        d = dx * dx + dy * dy
        if d > menzil * menzil or d >= en_d:
            continue
        if amin <= math.atan2(dy, dx) <= amax:
            en, en_d = o, d
    return en


def bot_karar(bot, u, rng, durum):
    if bot == 'hic':
        return False
    B = BOTLAR[bot]
    if B.get('rastgele_s') and rng.random() < B['rastgele_s'] * AYAR['dt']:
        return True                     # amaçsız dokunuş (kötü oyuncu)
    if durum.get('bekle') is not None:
        durum['bekle'] -= AYAR['dt']
        if durum['bekle'] <= 0:
            durum['bekle'] = None
            # gecikme sonunda hedef (botun gözüyle) koniden çıktıysa çoğu kez vazgeçer; kalanı = yanlış dokunuş
            if gorunur_hedef(u, bot, durum) is None and rng.random() < B['vazgec']:
                return False
            return True
        return False
    durum['t'] = durum.get('t', 0) - AYAR['dt']
    if durum['t'] > 0 or u.gosterge < 1.0 or u.dalis_t is not None:
        return False
    durum['t'] = 0.05
    a, b = B['tepki']
    if gorunur_hedef(u, bot, durum, B['ongoru'] * (a + b) / 2) is not None:
        durum['bekle'] = a + (b - a) * rng.random()
    return False


def tur_oyna(seed, sv, bot, tur=1, bayrak=None, rakip_hp=None, gunluk=False):
    rng = random.Random(seed * 7919 + 13)
    u = Ucus(seed, sv, tur, bayrak, bot, rakip_hp)
    kalite, rt = rampa_karar(bot, rng, sv)
    u.kalkis(kalite, rt)
    durum = {'rng': rng}
    while not u.bitti:
        if bot_karar(bot, u, rng, durum):
            u.dokun()
        u.adim()
    r = u.sonuc()
    if gunluk:
        r['olay'] = u.olay
    r['kalite'] = kalite
    return r


# ---------------------------------------------------------------- ekonomi botu
HIC_SIFIR = ('dalis', 'dolum', 'kapasite', 'bolge', 'm_bonus', 'yakit_ac', 'yakit_s', 'yakit_g', 'son_ates')


def deger(ad, sv, son, bot='iyi'):
    """Bir sonraki seviyenin "hız eşdeğeri" değeri (kara kutu kartı mantığı).
    hic botu dokunmayan oyuncudur: kara kutu kartı dalış/zamanlama geliştirmelerini ona önermez (değer 0)."""
    if bot == 'hic' and ad in HIC_SIFIR:
        return 0
    if bot == 'hic' and ad == 'rampa':
        return 45          # dokunmayan oyuncuda kara kutu kartı hep "Rampa gücü"nü gösterir
    vmax = max(son.get('max_v', 70), 60)
    dal = max(2, son.get('dalis', 2))
    sek = max(2, son.get('sekme', 3))
    kaz = max(50, son.get('kazanc', 100))
    para = 0.1 * kaz / 12.0                    # +%10 kazanç ≈ bu kadar b/s
    tab = {
        'rampa': 12 * 1.2, 'bolge': 3, 'm_bonus': 0.05 * (70 + 12 * sv.get('rampa', 0)),
        'zeplin_h': 0.5 * para, 'verim': 0.012 * vmax * min(sek, 6) * 0.4,
        'aero': 0.05 * vmax * (0.35 if vmax > 100 else 0.15), 'burun': 0.08 * 0.06 * vmax * 3, 'ip': 2,
        'kalkan': 25 if son.get('isi_s', 0) > 0.5 else 2, 'zirh': 6 if son.get('olumcul', 0) else 1,
        'kademe_n': 30, 'kademe_itki': 5 * (1 + sv.get('kademe_n', 0)) * 0.6,
        'dalis': 2.2 * dal, 'dolum': 0.1 * dal * 20, 'kapasite': 30, 'son_ates': 4,
        'izlenme': para, 'kombo_s': 0.4 * para, 'kombo_t': 1.5 * para,
    }
    for f in ('yakit', 'fisek', 'konfeti', 'termal', 'jet', 'romorkor'):
        baz = dict(yakit=25, fisek=40, konfeti=28, termal=18, jet=35, romorkor=45)[f]
        if f == 'romorkor':   # römorkör yalnız romorkor_y üstünde çıkar: oraya çıkabilen oyuncu için yörüngenin anahtarı
            baz = 90 if son.get('max_y', 0) >= AYAR['romorkor_y'] else 5
        if f == 'jet' and vmax < 140:
            baz = 8
        tab[f + '_ac'] = baz
        tab[f + '_s'] = baz * 0.35 if sv.get(f + '_ac') else 0
        tab[f + '_g'] = baz * 0.25 if sv.get(f + '_ac') else 0
    return tab.get(ad, 0)


def alisveris(sv, para, tur, son, bot='iyi', rng=None, rastgele=0.0):
    """Açgözlü alıcı: değer/fiyat en yüksek olanı alır. En iyi kalem yetmiyor ama 2 tur kazancı içinde ise
    biriktirir (kara kutu kartı "X jeton kaldı" der; oyuncu daha ucuz işe yaramaz şeylere harcamaz).
    rastgele > 0: dayanıklılık testi — her satın almada bu olasılıkla parasının yettiği rastgele bir kalemi alır."""
    alinan = []
    ufuk = 2.2 * max(60.0, son.get('kazanc', 100))
    while True:
        aday = []
        for ad, (mx, taban, gor) in GELISTIRME.items():
            if tur < gor:
                continue
            p = fiyat(ad, sv.get(ad, 0))
            if p is None:
                continue
            d = deger(ad, sv, son, bot)
            if d > 0:
                aday.append((d / p, ad, p))
        aday.sort(reverse=True)
        al = None
        if rastgele and rng.random() < rastgele:
            yet = [(ad, p) for _, ad, p in aday if p <= para]
            if not yet:   # değeri 0 olanlar dahil herhangi bir kalem
                yet = [(ad, fiyat(ad, sv.get(ad, 0))) for ad, (mx, _, g) in GELISTIRME.items()
                       if tur >= g and fiyat(ad, sv.get(ad, 0)) is not None and fiyat(ad, sv.get(ad, 0)) <= para]
            if yet:
                aday = []
                al = yet[rng.randrange(len(yet))]
        for sk, ad, p in ([] if al else aday):
            if p <= para:
                al = (ad, p)
                break
            if p <= ufuk:       # yakında alınabilir: biriktir
                break
        if al is None:
            break
        sv[al[0]] = sv.get(al[0], 0) + 1
        para -= al[1]
        alinan.append(al[0])
    return para, alinan


def kampanya(args):
    seed, bot, tur_max = args[:3]
    rastgele = args[3] if len(args) > 3 else 0.0
    rng_al = random.Random(seed * 31 + 7)
    en_uzun_yok25 = 0
    sv, para, bayrak = {}, 0.0, set()
    ilk = {}
    rakip_i, rakip_h = 0, 0.0
    satin_yok, en_uzun_yok = 0, 0
    harcama = 0.0
    turlar = []
    son = {}
    for tur in range(1, tur_max + 1):
        hp = RAKIPLER[rakip_i][0] if rakip_i < len(RAKIPLER) else None
        r = tur_oyna(seed * 1000 + tur, dict(sv), bot, tur, set(bayrak), hp)
        kaz = r['kazanc']
        for d in r['duvar']:
            if d not in ilk:
                ilk[d] = tur
                ilk[d + '_harcama'] = harcama
                kaz += DUVARLAR[d]
            elif d in DUVARLAR:
                kaz += DUVARLAR[d] * 0.1
            if d in ('tropopoz', 'karman'):
                bayrak.add(d)
        if hp is not None:
            rakip_h += r['rakip_hasar']
            if rakip_h >= hp:
                kaz += RAKIPLER[rakip_i][1]
                rakip_i += 1
                rakip_h = 0.0
        para += kaz
        son = r
        once = para
        para, al = alisveris(sv, para, tur, r, bot, rng_al, rastgele)
        harcama += once - para
        kalan = any(tur >= g and fiyat(a, sv.get(a, 0)) is not None for a, (_, _, g) in GELISTIRME.items())
        satin_yok = 0 if (al or not kalan) else satin_yok + 1
        en_uzun_yok = max(en_uzun_yok, satin_yok)
        if tur <= AYAR['ayar_tur']:
            en_uzun_yok25 = max(en_uzun_yok25, satin_yok)
        turlar.append(dict(tur=tur, sure=r['sure_tur'], mesafe=r['mesafe'], max_v=r['max_v'], max_y=r['max_y'],
                           kazanc=kaz, al=al, sekme=r['sekme'], son_sans=r['son_sans'], bitis=r['bitis'],
                           temas_s=r['temas_s'], mesafe_g=r['mesafe_g'], ekran=r['ekran_ort'], olumcul=r['olumcul'], sv=dict(sv), rakip=rakip_i, harcama=harcama, kazanc_ucus=r['kazanc']))
    return dict(seed=seed, bot=bot, ilk=ilk, en_uzun_yok=en_uzun_yok, en_uzun_yok25=en_uzun_yok25, turlar=turlar, para=para)


# ---------------------------------------------------------------- ölçüm ve rapor tabloları
def ort(a):
    a = [x for x in a if x is not None]
    return sum(a) / len(a) if a else float('nan')


def yuzde(a, p):
    a = sorted(a)
    if not a:
        return float('nan')
    return a[min(len(a) - 1, int(p * len(a)))]


def tek_tur_olc(havuz, botlar, tohumlar, sv=None, tur=1, bayrak=None):
    is_ = [(sd, sv or {}, b, tur, bayrak) for b in botlar for sd in tohumlar]
    sonuc = havuz.map(_tek, is_)
    out = {}
    for (sd, _, b, _, _), r in zip(is_, sonuc):
        out.setdefault(b, []).append(r)
    return out


def _tek(a):
    sd, sv, b, tur, bayrak = a
    return tur_oyna(sd, sv, b, tur, bayrak)


def tablo_tek(res, baslik):
    sat = [f'**{baslik}**', '',
           '| Bot | Tur süresi s (ort · min–maks) | Mesafe b | En yüksek hız b/s | En yüksek irtifa b | Sekme | Mükemmel | Temas/s | Son şans | Son şans sonrası yükselme b (en az) | Ekrandaki nesne (ort · en az · <4 olan örnek %) | "Vay" ≤5 s | Bitiş (yer/durma/ölümcül/süre/kaçış) |',
           '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for b, rs in res.items():
        vay = sum(1 for r in rs if r['vay_t'] is not None and r['vay_t'] <= 5) / len(rs)
        bit = {k: sum(1 for r in rs if r['bitis'] == k) for k in ('yer', 'durma', 'olumcul', 'sure', 'kacis')}
        sat.append(f"| {b} | {ort([r['sure_tur'] for r in rs]):.1f} · {min(r['sure_tur'] for r in rs):.0f}–{max(r['sure_tur'] for r in rs):.0f} "
                   f"| {ort([r['mesafe'] for r in rs]):.0f} | {ort([r['max_v'] for r in rs]):.0f} | {ort([r['max_y'] for r in rs]):.0f} "
                   f"| {ort([r['sekme'] for r in rs]):.1f} | {ort([r['mukemmel'] for r in rs]):.1f} | {ort([r['temas_s'] for r in rs]):.2f} "
                   f"| {ort([r['son_sans'] for r in rs]):.2f} | {min([y for r in rs for y in r['kademe_yuk']] or [0]):.0f} | {ort([r['ekran_ort'] for r in rs]):.1f} · {min(r['ekran_min'] for r in rs)} · %{100 * ort([r['ekran_az_oran'] for r in rs]):.1f} | %{vay * 100:.0f} | {'/'.join(str(bit[k]) for k in bit)} |")
    return '\n'.join(sat)


def ana(tohum_n=20, tur_max=60):
    tohumlar = list(range(1, tohum_n + 1))
    botlar = BOT_SIRA
    T = AYAR['ayar_tur']
    cikti = [f'Ayar yalnız ilk {T} tur için; {T + 1}+ satırları **taslak**. Hedef tablosu: `HEDEF` (iyi bot).']
    with Pool() as hv:
        # 1) geliştirmesiz tur 1
        r1 = tek_tur_olc(hv, botlar, tohumlar)
        cikti.append(tablo_tek(r1, f'Tur 1, geliştirmesiz, {tohum_n} tohum'))
        fark = ort([r['mesafe'] for r in r1['iyi']]) / ort([r['mesafe'] for r in r1['hic']]) - 1
        cikti.append(f'\nBeceri farkı (tur 1, mesafe): iyi / hiç − 1 = **%{fark * 100:.0f}** (hedef ≥ %{HEDEF["beceri"][1] * 100:.0f})\n')
        # 2) kampanyalar
        kp = hv.map(kampanya, [(sd, b, tur_max) for b in botlar for sd in tohumlar])
        kb = {}
        for k in kp:
            kb.setdefault(k['bot'], []).append(k)
        H = HEDEF['esik']
        sat = ['**İlerleme: eşiklerin ilk kırıldığı tur (medyan · %10–%90), en uzun alışverişsiz seri**', '',
               '| Bot | Ses | Tropopoz | Isı | Kármán | Yörünge | Kaçış (taslak) | O ana dek harcanan jeton (ses/ısı/yörünge/kaçış) | Alışverişsiz seri: ilk 25 tur ort · maks · 60 tur maks |', '|---|---|---|---|---|---|---|---|---|',
               '| **hedef (iyi)** | ' + ' | '.join(f'{a}–{b}' for a, b in H.values()) + ' | (40) | | ≤ 3 |']
        for b in botlar:
            ks = kb[b]
            hucre = []
            for d in ('ses', 'tropopoz', 'isi', 'karman', 'yorunge', 'kacis'):
                v = [k['ilk'].get(d) for k in ks]
                ok = [x for x in v if x]
                if not ok:
                    hucre.append('—')
                    continue
                hucre.append(f"{yuzde(ok, .5)} · {yuzde(ok, .1)}–{yuzde(ok, .9)}" + (f" ({len(ok)}/{len(v)})" if len(ok) < len(v) else ''))
            hh = []
            for d in ('ses', 'isi', 'yorunge', 'kacis'):
                v = [k['ilk'].get(d + '_harcama') for k in ks if d in k['ilk']]
                hh.append(f"{ort(v) / 1000:.0f}k" if v else '—')
            hucre.append(' / '.join(hh))
            yok = [k['en_uzun_yok25'] for k in ks]
            sat.append(f"| {b} | {' | '.join(hucre)} | {ort(yok):.1f} · {max(yok)} · {max(k['en_uzun_yok'] for k in ks)} |")
        cikti.append('\n'.join(sat))
        # 2b) rakip nakavt turları
        sat = ['\n**Rakip nakavt turu (medyan)**', '', '| Bot | R1 | R2 | R3 | R4 (taslak) | R5 (taslak) |', '|---|---|---|---|---|---|',
               '| **hedef (iyi)** | ' + ' | '.join(str(x) for x in HEDEF['rakip']) + ' | (30) | (39) |']
        for b in botlar:
            hucre = []
            for i in range(1, 6):
                v = sorted(next((x['tur'] for x in k['turlar'] if x['rakip'] >= i), 999) for k in kb[b])
                m = v[len(v) // 2]
                hucre.append(str(m) if m < 999 else '—')
            sat.append(f"| {b} | {' | '.join(hucre)} |")
        cikti.append('\n'.join(sat))
        # 3) tur profili (her bot)
        for pb in botlar:
            sat = [f'\n**Tur profili — "{pb}" bot ({tohum_n} tohum ortalaması)**', '',
                   '| Tur | Süre s (ort · medyan) | Mesafe gösterge km | En yüksek hız b/s | Gösterge | En yüksek irtifa b | İrtifa km | Kazanç jeton | Alınan | Sekme | Temas/s | Son şans | Ekrandaki nesne | Ölümcül temas | Tavana çarpan |',
                   '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
            for t in (1, 2, 3, 5, 8, 10, 12, 15, 20, 25, 30, 35, 40, 45, 50):
                rs = [k['turlar'][t - 1] for k in kb[pb] if len(k['turlar']) >= t]
                if not rs:
                    continue
                v = ort([r['max_v'] for r in rs])
                y = ort([r['max_y'] for r in rs])
                sat.append(f"| {t}{' (taslak)' if t > T else ''} | {ort([r['sure'] for r in rs]):.0f} · {yuzde([r['sure'] for r in rs], .5):.0f} | {ort([r['mesafe_g'] for r in rs]):.1f} | {v:.0f} | {gosterge_metni(v)} "
                           f"| {y:.0f} | {irtifa_km(y):.1f} | {ort([r['kazanc'] for r in rs]):.0f} | {ort([len(r['al']) for r in rs]):.1f} | {ort([r['sekme'] for r in rs]):.1f} "
                           f"| {ort([r['temas_s'] for r in rs]):.2f} | {ort([r['son_sans'] for r in rs]):.2f} | {ort([r['ekran'] for r in rs]):.1f} | {ort([r['olumcul'] for r in rs]):.2f} "
                           f"| {sum(1 for r in rs if r['bitis'] == 'sure')}/{len(rs)} |")
            cikti.append('\n'.join(sat))
        # 3b) tur süresi özeti (ilk 25 tur)
        sat = ['\n**Tur süresi (rampa + uçuş, s), ilk 25 tur: tur 15–25 medyanı, tavana (%.0f s) çarpan turlar**' % AYAR['tur_tavan'], '',
               '| Bot | Tur 15–25 medyan | %10–%90 | Tavana çarpan | Bitiş (yer/durma/ölümcül/süre/kaçış) |', '|---|---|---|---|---|']
        for b in botlar:
            tt = [x for k in kb[b] for x in k['turlar'][:T]]
            t15 = [x['sure'] for k in kb[b] for x in k['turlar'][14:T]]
            bit = '/'.join(str(sum(1 for x in tt if x['bitis'] == q)) for q in ('yer', 'durma', 'olumcul', 'sure', 'kacis'))
            sat.append(f"| {b} | {yuzde(t15, .5):.0f} | {yuzde(t15, .1):.0f}–{yuzde(t15, .9):.0f} | %{100 * sum(x['bitis'] == 'sure' for x in tt) / len(tt):.0f} | {bit} |")
        cikti.append('\n'.join(sat))
        # 3c) dayanıklılık: alıcı %30 olasılıkla rastgele satın alır
        kr = hv.map(kampanya, [(sd, b, tur_max, 0.3) for b in botlar for sd in tohumlar])
        sat = ['\n**Dayanıklılık: alıcı %30 olasılıkla rastgele satın alır** (eşik turu medyanı; çıkmaz = ilk 25 turda art arda 5 tur ne alım ne yeni eşik ne rakip nakavtı)', '',
               '| Bot | Ses | Tropopoz | Isı | Kármán | Yörünge | Alışverişsiz seri maks (ilk 25 · 60 tur) | Çıkmaz |', '|---|---|---|---|---|---|---|---|']
        for b in botlar:
            ks = [k for k in kr if k['bot'] == b]
            hucre = []
            for d in ('ses', 'tropopoz', 'isi', 'karman', 'yorunge'):
                ok = [k['ilk'][d] for k in ks if d in k['ilk']]
                hucre.append((f"{yuzde(ok, .5)}" + (f" ({len(ok)}/{len(ks)})" if len(ok) < len(ks) else '')) if ok else '—')
            sat.append(f"| {b} | {' | '.join(hucre)} | {max(k['en_uzun_yok25'] for k in ks)} · {max(k['en_uzun_yok'] for k in ks)} | {sum(cikmaz(k) for k in ks)}/{len(ks)} |")
        cikti.append('\n'.join(sat))
        # 4) aynı geliştirme durumunda beceri farkı (iyi botun 5., 10. ve 25. tur durumu)
        for t in (5, 10, 25):
            k0 = [k for k in kb['iyi'] if len(k['turlar']) >= t]
            if not k0:
                continue
            svs = [k['turlar'][t - 2]['sv'] if t > 1 else {} for k in k0]
            bay = {'tropopoz', 'karman'} if t >= 20 else ({'tropopoz'} if t >= 10 else set())
            isl = [(sd, svs[i % len(svs)], b, t, bay) for b in botlar for i, sd in enumerate(range(1, 3 * tohum_n + 1))]   # gürültü az olsun: 3× tur
            rr = hv.map(_tek, isl)
            out = {}
            for (sd, _, b, _, _), r in zip(isl, rr):
                out.setdefault(b, []).append(r)
            cikti.append('\n' + tablo_tek(out, f'Tur {t} — tüm botlar "iyi" botun o turdaki geliştirmeleriyle'))
            m0 = ort([r['mesafe'] for r in out['hic']])
            cikti.append(f'\nBeceri farkı tur {t} (mesafe, bot / hiç − 1): ' + ' · '.join(
                f"{b} %{(ort([r['mesafe'] for r in out[b]]) / m0 - 1) * 100:+.0f}" for b in botlar if b != 'hic') + '\n')
        # 5) ilk 12 turun alışveriş günlüğü (iyi, tohum 1)
        k = kb['iyi'][0]
        sat = ['\n**Örnek kampanya (iyi, tohum 1): satın alımlar**', '', '| Tur | Kazanç | Alınan |', '|---|---|---|']
        for r in k['turlar'][:45]:
            sat.append(f"| {r['tur']} | {r['kazanc']:.0f} | {', '.join(r['al']) or '—'} |")
        cikti.append('\n'.join(sat))
        json.dump({b: [dict(ilk=k['ilk'], turlar=[{x: y for x, y in t.items() if x != 'sv'} for t in k['turlar']]) for k in kb[b]]
                   for b in botlar}, open(_yol('kampanya.json'), 'w', encoding='utf-8'))
    return '\n\n'.join(cikti)


def cikmaz(k, n=5):
    """İlk ayar_tur içinde art arda n tur boyunca ne satın alım ne yeni eşik ne rakip nakavtı olduysa çıkmaz."""
    ilk_tur = set(v for a, v in k['ilk'].items() if not a.endswith('_harcama'))
    seri, rk = 0, 0
    for x in k['turlar'][:AYAR['ayar_tur']]:
        olay = x['al'] or x['tur'] in ilk_tur or x['rakip'] > rk
        rk = x['rakip']
        seri = 0 if olay else seri + 1
        if seri >= n:
            return True
    return False


def gosterge_metni(v):
    ms = hiz_gosterge(v)
    if ms < 1715:
        return f'Mach {ms / 343:.2f}'
    return f'{ms / 1000:.1f} km/s'


def _yol(ad):
    import os
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), ad)


def esleme_tablosu():
    sat = ['| İç hız b/s | m/s | km/sa | Mach |', '|---|---|---|---|']
    for v in (25, 50, 70, 100, 115, 150, 200, 250, 300, 400, 500, 600, 700, 849):
        ms = hiz_gosterge(v)
        sat.append(f'| {v} | {ms:.0f} | {ms * 3.6:,.0f} | {ms / 343:.2f} |')
    sat += ['', '| İç irtifa b | km |', '|---|---|']
    for y in (25, 60, 100, 250, 400, 700, 1000, 1500, 2000, 3000, 3500, 5000):
        sat.append(f'| {y} | {irtifa_km(y):.1f} |')
    return '\n'.join(sat)


# ---------------------------------------------------------------- güç eğrisi: tüm geliştirmeler maks'ın f oranında
def sv_oran(f, tur=40):
    sv = {}
    for a, (mx, _, g) in GELISTIRME.items():
        n = int(round(mx * f))
        if a.endswith('_ac'):
            n = 1 if f >= 0.15 else 0
        if n:
            sv[a] = n
    return sv


def maliyet(sv):
    return sum(sum(fiyat(a, i) for i in range(n)) for a, n in sv.items())


def guc_egrisi(havuz, tohum_n=10, botlar=('hic', 'iyi')):
    sat = ['| Geliştirme oranı | Harcanan jeton | ' + ' | '.join(f'{b}: süre s · en yüksek hız · irtifa · bitiş' for b in botlar) + ' |',
           '|---|---|' + '---|' * len(botlar)]
    for f in (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0):
        sv = sv_oran(f)
        bay = {'tropopoz', 'karman'}
        isl = [(sd, sv, b, 40, bay) for b in botlar for sd in range(1, tohum_n + 1)]
        rr = havuz.map(_tek, isl)
        hucre = []
        for b in botlar:
            rs = [r for (sd, _, bb, _, _), r in zip(isl, rr) if bb == b]
            bit = {}
            for r in rs:
                bit[r['bitis']] = bit.get(r['bitis'], 0) + 1
            hucre.append(f"{ort([r['sure_tur'] for r in rs]):.0f} · {ort([r['max_v'] for r in rs]):.0f} · {ort([r['max_y'] for r in rs]):.0f} · "
                         + ','.join(f'{k}{v}' for k, v in sorted(bit.items())))
        sat.append(f'| {f:.1f} | {maliyet(sv) / 1000:.0f}k | ' + ' | '.join(hucre) + ' |')
    return '\n'.join(sat)


# ---------------------------------------------------------------- hedefler (ilk 25 tur; tek birim: gösterge km, jeton)
# PLAN_B §5.3 S9 (D1–D6). Sim bunlara ayarlanır, hedef sim'e uydurulmaz. Eşik turu = 20+ tohum medyanı; ulaşamayan kampanya "ulaşamadı" sayılır.
HEDEF = dict(
    esik=dict(ses=(2, 3), tropopoz=(9, 10), isi=(11, 12), karman=(17, 19), yorunge=(24, 27)),   # iyi bot
    yorunge_usta=24, yorunge_orta=34,          # D2: usta ≤ 24, orta (tipik oyuncu) ≤ 34 (en çok)
    zayif=dict(isi=28, karman=50, karman_oran=0.75),   # kotu: ısı medyanı ≤ 28; Kármán ≤ 50 en az 15/20 kampanyada
    rakip=(7, 14, 22),                          # bilgi
    kazanc_ucus={1: 120, 5: 500, 10: 900, 15: 1600, 20: 2600, 25: 4000}, kazanc_tol=0.15,   # S2: uçuş kazancı, 3 tur kayan medyan (duvar + nakavt hariç)
    sure_t15=(45, 55), tavan=0.10,              # tur 15–25 medyan süresi; tavana (65 s) çarpan tur oranı (her bot) ≤ %10
    beceri={1: 0.30, 5: 0.60, 10: 0.60},        # D6: iyi / hiç − 1 (aynı geliştirmeler, mesafe)
    bilgi=dict(mesafe_km_25=(90, 130), sure={1: 18, 3: 30, 10: 50}),   # D1: mesafe ayar hedefi değil, bilgi satırı; D2: tur 25 hızı kaldırıldı
)


def esik_medyan(ks, d, sinir=99):
    """Ulaşamayan kampanya 'sinir' sayılır (sansürlü medyan); 99 = ulaşamadı."""
    return yuzde([k['ilk'].get(d, sinir) for k in ks], .5)


def hedef_kontrol(olc, bc):
    """HEDEF tablosuna karşı tuttu/tutmadı listesi (ozet çıktısı)."""
    H, sat = HEDEF, ['hedef kontrol:']
    def yaz(ad, deger, hedef, ok):
        sat.append(f"  {'✓' if ok else '✗'} {ad}: {deger} (hedef {hedef})")
    i = olc.get('iyi')
    if i:
        for d, (a, b) in H['esik'].items():
            m = i['sm'][d]
            yaz(f'iyi {d}', m if m < 99 else 'ulaşamadı', f'{a}–{b}', a <= m <= b)
        for t, h in H['kazanc_ucus'].items():
            v = i['kazanc'][t]
            yaz(f'iyi uçuş kazancı t{t}', round(v), f'{h} ±%{H["kazanc_tol"] * 100:.0f}', abs(v / h - 1) <= H['kazanc_tol'])
        yaz('iyi tur 15–25 medyan süre', round(i['t15']), f"{H['sure_t15'][0]}–{H['sure_t15'][1]} s", H['sure_t15'][0] <= i['t15'] <= H['sure_t15'][1])
    for b, hd in (('usta', H['yorunge_usta']), ('orta', H['yorunge_orta'])):
        if b in olc:
            m = olc[b]['sm']['yorunge']
            yaz(f'{b} yörünge', m if m < 99 else 'ulaşamadı', f'≤ {hd}', m <= hd)
    k = olc.get('kotu')
    if k:
        Z = H['zayif']
        yaz('kotu ısı', k['sm']['isi'] if k['sm']['isi'] < 99 else 'ulaşamadı', f"≤ {Z['isi']}", k['sm']['isi'] <= Z['isi'])
        oran = k['karman_le'] / k['n']
        yaz(f"kotu Kármán ≤ {Z['karman']}", f"{k['karman_le']}/{k['n']}", f"≥ %{Z['karman_oran'] * 100:.0f}", oran >= Z['karman_oran'])
    tv = {b: o['tavan'] for b, o in olc.items()}
    yaz('tavana çarpan (en kötü bot)', ' '.join(f'{b} %{v * 100:.0f}' for b, v in tv.items()), f"≤ %{H['tavan'] * 100:.0f}", max(tv.values()) <= H['tavan'])
    for t, h in H['beceri'].items():
        if t in bc and 'iyi' in bc[t]:
            yaz(f'beceri t{t} iyi/hiç', f"{bc[t]['iyi']:+.0%}", f'≥ +%{h * 100:.0f}', bc[t]['iyi'] >= h)
    n_ok = sum(1 for x in sat[1:] if x.startswith('  ✓'))
    sat.append(f'  → {n_ok}/{len(sat) - 1} tuttu')
    return '\n'.join(sat)


def kayan_medyan(k, t, alan='kazanc_ucus'):
    """Kampanyada t. tur çevresindeki 3 turun (t−1, t, t+1; uçta 2) medyanı (S2: tur bazındaki gürültüyü azaltır)."""
    tt = k['turlar']
    v = sorted(tt[i][alan] for i in range(max(0, t - 2), min(len(tt), t + 1)))
    return v[len(v) // 2] if len(v) % 2 else (v[len(v) // 2 - 1] + v[len(v) // 2]) / 2


OZET_TUR = dict(hic=60, kotu=60, orta=40, iyi=40, usta=40)   # eşik medyanı kesilmesin: yörünge/Kármán 25. turdan sonra da sayılır


def ozet(havuz, tohum_n=12, tur_max=None, botlar=None, rastgele=0.0):
    """Ayar döngüsü için kısa ölçüm (medyan): eşik turları, süre, uçuş kazancı (3 tur kayan medyan), tavan oranı."""
    botlar = botlar or BOT_SIRA
    tohumlar = list(range(1, tohum_n + 1))
    kp = havuz.map(kampanya, [(sd, b, tur_max or OZET_TUR[b], rastgele) for b in botlar for sd in tohumlar])
    kb = {}
    for k in kp:
        kb.setdefault(k['bot'], []).append(k)
    sat, olc = [], {}
    T = AYAR['ayar_tur']
    for b in botlar:
        ks = kb[b]
        o = olc[b] = {}
        h = []
        for d in ('ses', 'tropopoz', 'isi', 'karman', 'yorunge'):
            v = [k['ilk'].get(d) for k in ks]
            ok = [x for x in v if x]
            o[d] = (yuzde(ok, .5) if ok else None, len(ok), len(v))
            o.setdefault('sm', {})[d] = sm = esik_medyan(ks, d)
            h.append(f"{d}:{sm if sm < 99 else '—'}" + (f"({len(ok)}/{len(v)})" if len(ok) < len(v) else ''))
        o['n'] = len(ks)
        o['karman_le'] = sum(1 for k in ks if k['ilk'].get('karman', 99) <= HEDEF['zayif']['karman'])
        rk = []
        for i in range(1, 4):
            vv = sorted(next((x['tur'] for x in k['turlar'] if x['rakip'] >= i), 999) for k in ks)
            rk.append(str(vv[len(vv) // 2]))
        t15 = [x['sure'] for k in ks for x in k['turlar'][14:T]]
        o['t15'] = yuzde(t15, .5) if t15 else 0
        o['tavan'] = sum(1 for k in ks for x in k['turlar'][:T] if x['bitis'] == 'sure') / max(1, sum(len(k['turlar'][:T]) for k in ks))
        o['kazanc'] = {t: yuzde([kayan_medyan(k, t) for k in ks], .5) for t in (1, 5, 10, 15, 20, 25)}
        kz = ' '.join(f"{t}:{v:.0f}" for t, v in o['kazanc'].items())
        kt = ' '.join(f"{t}:{yuzde([k['turlar'][t - 1]['kazanc'] for k in ks], .5):.0f}" for t in (5, 15, 25))
        sr = ' '.join(f"{t}:{yuzde([k['turlar'][t - 1]['sure'] for k in ks], .5):.0f}" for t in (1, 3, 10, 15, 25))
        mz = ' '.join(f"{t}:{yuzde([k['turlar'][t - 1]['mesafe_g'] for k in ks], .5):.0f}" for t in (10, 25))
        ss = ' '.join(f"{t}:{ort([k['turlar'][t - 1]['son_sans'] for k in ks]):.1f}" for t in (10, 25))
        sat.append(f"{b:5} | {' '.join(h)} | rakip {'/'.join(rk)} | süre med {sr} · t15-25 {o['t15']:.0f} · tavan %{o['tavan'] * 100:.0f} "
                   f"| uçuş kazancı (3 tur kayan med) {kz} · toplam {kt} | km {mz} | son şans {ss} | seri25 maks {max(k['en_uzun_yok25'] for k in ks)}")
    return '\n'.join(sat), kb, olc


def beceri(havuz, kb, t, tohum_n=12, botlar=None):
    """Aynı geliştirmelerle (iyi botun t. tur durumu) tek tur: mesafe ortalaması bot başına."""
    botlar = botlar or BOT_SIRA
    k0 = [k for k in kb['iyi'] if len(k['turlar']) >= t]
    svs = [k['turlar'][t - 2]['sv'] if t > 1 else {} for k in k0]
    bay = {'tropopoz', 'karman'} if t >= 20 else ({'tropopoz'} if t >= 10 else set())
    isl = [(sd, svs[i % len(svs)], b, t, bay) for b in botlar for i, sd in enumerate(range(1, tohum_n + 1))]
    rr = havuz.map(_tek, isl)
    out = {}
    for (sd, _, b, _, _), r in zip(isl, rr):
        out.setdefault(b, []).append(r)
    return out


def ozet_yaz(hv, n, rastgele=0.0):
    """ozet + beceri farkı (tur 1, 5, 10; 3n uçuş) + hic maks testi + hedef kontrol."""
    txt, kb, olc = ozet(hv, n, rastgele=rastgele)
    out = [txt]
    bc = {}
    for t in (1, 5, 10):
        r = beceri(hv, kb, t, 3 * n)
        m = {b: ort([x['mesafe'] for x in rs]) for b, rs in r.items()}
        bc[t] = {b: m[b] / m['hic'] - 1 for b in m if b != 'hic'}
        out.append(f"beceri t{t}: " + ' '.join(f"{b}/hic {v:+.0%}" for b, v in bc[t].items()))
    mx = [tur_oyna(sd, sv_oran(1.0), 'hic', 40, {'tropopoz', 'karman'}) for sd in range(1, 11)]
    out.append(f"hic maks: irtifa ort {round(ort([r['max_y'] for r in mx]))} tropopoz {sum(r['max_y'] >= AYAR['y_tropopoz'] for r in mx)} /10")
    out.append(hedef_kontrol(olc, bc))
    return '\n'.join(out)


def kontrol():
    """Denetçi düzeltmelerinin değişmezleri (a, c, d): hata varsa AssertionError."""
    import math as m
    A = AYAR
    # (c) g_etkin hiçbir hızda negatif olmaz; v ≥ v_yörünge'de tam 0
    u = Ucus(1, {})
    for v in (0, 50, 300, 599, 600, 700, 849, 2000):
        assert u.g_etkin(v) >= 0, v
    assert u.g_etkin(600) == 0 and u.g_etkin(2000) == 0
    # (a) sekme: hız büyüklüğü tam ×k, yön tipin açısı; alçak/bulut bandında 40–55°
    for ad, T in TIPLER.items():
        if T['sinif'] != 'tr':
            continue
        u = Ucus(1, {}); u.t = 10.0
        u.vx, u.vy = 80.0, -60.0
        v0 = m.hypot(u.vx, u.vy)
        o = Nesne(ad, 0, 0, 'tr', T['r']); u.y = 50
        u.sekme(o, T)
        v1 = m.hypot(u.vx, u.vy - T.get('ek_vy', 0)) if T.get('ek_vy') else m.hypot(u.vx, u.vy)
        assert abs(m.hypot(u.vx, u.vy - T.get('ek_vy', 0)) - v0 * u.k_etkin(T['k'])) < 1e-6, (ad, v1, v0 * u.k_etkin(T['k']))
        assert T['k'] < 1.0
        if not T.get('kayma'):   # kayma yüzeyi (habitat) ayrı sınıf: sığ açı serbest
            assert 40 <= T['aci'] <= 55, (ad, T['aci'])
    # (d) yoğunluk ekran başına: 40 tur, ortalama ekrandaki nesne 7–12
    rs = [tur_oyna(sd, {}, b) for sd in range(1, 21) for b in ('iyi', 'orta')]
    ek = [r['ekran_ort'] for r in rs]
    assert 7 <= sum(ek) / len(ek) <= 12, ek
    # tur tavanı yalnız emniyet: geliştirmesiz tur 1'de hiçbir tur tavana çarpmaz
    assert all(r['sure_tur'] <= A['tur_tavan'] + A['dt'] and r['bitis'] != 'sure' for r in rs)
    # irtifa göstergesi tek yönlü ve Kármán = 100 km; uzay nesneleri Kármán'ın üstünde, atmosfer nesneleri altında
    km = [irtifa_km(y) for y in range(0, 8000, 50)]
    assert all(b >= a for a, b in zip(km, km[1:])) and abs(irtifa_km(A['y_karman']) - 100) < 1e-9
    for ad, T in TIPLER.items():
        if T['acilis'] == 'karman':
            assert T['ymin'] >= A['y_karman'], ad
        elif T['acilis'] == 'tropopoz':
            assert T['ymax'] < A['y_karman'], ad
    assert A['sure_odul'] == 0, 'saniye başına ödeme kaldırıldı'
    print('kontrol tamam: g_etkin >= 0, sekme |v| = k_etkin*|v|, trambolin açısı 40-55 (kayma yüzeyi hariç), ekran yoğunluğu',
          round(sum(ek) / len(ek), 1), ', tavan, irtifa eşlemesi, bantlar')



if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    a = sys.argv[1:]
    if a and a[0] == 'tek':
        r = tur_oyna(int(a[1]), {}, a[2], gunluk=True)
        for o in r.pop('olay'):
            print(o)
        print({k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items()})
    elif a and a[0] == 'egri':
        with Pool() as hv:
            print(guc_egrisi(hv))
    elif a and a[0] == 'esleme':
        print(esleme_tablosu())
    elif a and a[0] == 'kontrol':
        kontrol()
    elif a and a[0] == 'ozet':   # python ucus_sim.py ozet [tohum] [rastgele]
        with Pool() as hv:
            print(ozet_yaz(hv, int(a[1]) if len(a) > 1 else 12, float(a[2]) if len(a) > 2 else 0.0))
    else:
        n = 5 if a and a[0] == 'hizli' else 20
        print(ana(n, 60 if n == 20 else 50))
