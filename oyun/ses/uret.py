#!/usr/bin/env python3
"""Son Durak: Pluton ses adaylarini uretir (efektler + motor donguleri + muzik katmanlari).

Calistir:  python3 oyun/ses/uret.py      (sonra: python3 oyun/ses/olc.py)
Cikti:     oyun/ses/adaylar/*.mp3 + oyun/ses/_ara/*.wav (ara dosya, git disi) + oyun/ses/_ara/uretim.json
Ses seviyeleri: KATEGORI[...]['hedef'] (K-agirlikli LUFS). Bir kategoriyi toptan kisip acmak icin bu sayiyi degistir.
"""
import json
import os
import subprocess
import sys

import numpy as np
import soundfile as sf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ses_lib import *  # noqa: E402,F401,F403
import ses_lib as L  # noqa: E402

ADAY = os.path.join(KOK, 'adaylar')
ARA = os.path.join(KOK, '_ara')
TAVAN = -1.5          # dBTP tavani (mp3 asmasi icin pay)
DONGU_PAY = 0.5       # dongu dosyalarinin basina/sonuna eklenen dongu parcasi (s); kesintisiz dongu icin

# olcu: 'tepe' = en yuksek 100 ms LUFS (tek atim), 'i' = butunlesik LUFS (dongu)
KATEGORI = {
    'motor_tutusma': dict(ad='Motor tutuşma (rampa)', hedef=-12, olcu='tepe', sure=(1.0, 3.0), darbe=False),
    'motor_ucus':    dict(ad='Motor uçuş döngüsü (hızla tizleşir)', hedef=-20, olcu='i', sure=None, darbe=False, dongu=True),
    'sekme_trambolin': dict(ad='Sekme: trambolin "boing"', hedef=-13, olcu='tepe', sure=(0.15, 0.8), darbe=True),
    'carpma_marti':  dict(ad='Çarpma: martı dağılma', hedef=-14, olcu='tepe', sure=(0.15, 1.0), darbe=True),
    'carpma_balon':  dict(ad='Çarpma: balon patlama', hedef=-13, olcu='tepe', sure=(0.1, 0.8), darbe=True),
    'kademe_ayrilma': dict(ad='Kademe ayrılma', hedef=-12, olcu='tepe', sure=(0.4, 1.6), darbe=True),
    'dalis':         dict(ad='Dalış (vuuş + vuruş)', hedef=-12, olcu='tepe', sure=(0.2, 1.0), darbe=False),
    'mukemmel':      dict(ad='Mükemmel sekme', hedef=-12, olcu='tepe', sure=(0.3, 1.3), darbe=True),
    'ses_duvari':    dict(ad='Ses duvarı kırılışı (sinematik)', hedef=-10, olcu='tepe', sure=(1.2, 4.0), darbe=False),
    'jeton':         dict(ad='Jeton / kazanç', hedef=-15, olcu='tepe', sure=(0.1, 0.7), darbe=True),
    'ui_tik':        dict(ad='Arayüz tıklama', hedef=-20, olcu='tepe', sure=(0.01, 0.2), darbe=True),
    'kart_satin':    dict(ad='Kart satın alma', hedef=-15, olcu='tepe', sure=(0.3, 1.2), darbe=True),
    'son_sans':      dict(ad='Son şans uyarısı', hedef=-13, olcu='tepe', sure=(0.9, 2.0), darbe=False),
    'muzik':         dict(ad='Müzik döngüsü (hızla katman kazanır)', hedef=-18, olcu='i', sure=None, darbe=False, dongu=True),
}

ADAYLAR = []


def aday(kat, kod, ad, aciklama, kaynak='sentez'):
    def deco(fn):
        ADAYLAR.append(dict(kat=kat, kod=kod, ad=ad, aciklama=aciklama, kaynak=kaynak, fn=fn))
        return fn
    return deco


# ================================================================ ortak parcalar
def tok(f0=120, f1=45, tau=0.09, n=0.5):
    """Tok vurus: alcalan sinus + kisa tik."""
    N = n_(n)
    x = osc(expc(f0, f1, N), N) * env_exp(N, tau, 0.001)
    k = lp(white(N), 3500) * env_exp(N, 0.006, 0.0005) * 0.5
    return x + k


def pat(n=0.3):
    """Balon patlamasi: keskin durtu + tiz gurultu."""
    N = n_(n)
    x = hp(white(N), 800) * env_exp(N, 0.025, 0.0003)
    x[:n_(0.002)] += white(n_(0.002)) * 2.5
    return x


def yumusat(x, d=3.0):
    """Yumusak sinirlayici (tepe/RMS oranini dusurur, vurusu dolgunlastirir)."""
    return np.tanh(d * normal(x)) / np.tanh(d)


def pat_dolgun(n=0.3):
    return yumusat(pat(n), 3.0)


def boing(f_bas=160, f_ust=420, n=0.55, vib=14, derin=0.08, tau=0.18):
    N = n_(n)
    t = np.arange(N) / SR
    f = (f_bas + (f_ust - f_bas) * (1 - np.exp(-t / 0.05))) * (1 + derin * np.exp(-t / 0.3) * np.sin(2 * np.pi * vib * t))
    x = osc(f, N) + 0.35 * osc(2 * f, N) + 0.12 * osc(f, N, 'saw')
    return x * env_exp(N, tau, 0.003)


def ciglik(n=0.22, f0=1300, f1=850, rr=38):
    """Cizgi film marti cigligi: testere + gezen formant + puruzluluk."""
    N = n_(n)
    t = np.arange(N) / SR
    f = f0 + (f1 - f0) * (t / n) ** 0.7
    f *= 1 + 0.12 * np.sin(np.pi * np.minimum(t / 0.04, 1))
    x = osc(f, N, 'saw') * (1 + 0.45 * np.sin(2 * np.pi * rr * t))
    x = sweep(x, 2 * f, q=2.5, kind='bp') * 2 + 0.3 * bp(x, 900, 4000)
    return x * env_adsr(N, 0.012, 0.05, 0.7, 0.08)


def kanat(n=0.5, flap=22, tau=0.22):
    N = n_(n)
    t = np.arange(N) / SR
    am = np.clip(np.sin(2 * np.pi * flap * t * (1 - 0.3 * t)), 0, 1) ** 2
    return bp(white(N), 1500, 5500) * am * env_exp(N, tau, 0.01)


def metal(fs=(613, 1187, 1964, 2871), gs=(1, .7, .45, .3), tau=0.25, n=1.0):
    N = n_(n)
    x = sum(g * osc(f * np.linspace(1, 0.996, N), N) * env_exp(N, tau / (1 + 0.4 * i), 0.0005) for i, (f, g) in enumerate(zip(fs, gs)))
    return x


def vuus(n=0.3, f0=400, f1=3000, q=1.4, sekil='artan'):
    N = n_(n)
    x = sweep(white(N), expc(f0, f1, N), q=q, kind='bp')
    e = np.linspace(0, 1, N) ** 1.6 if sekil == 'artan' else np.sin(np.pi * np.linspace(0, 1, N)) ** 1.5
    return x * e


def can(f, n=0.6, tau=0.25, harm=((1, 1), (2.0, 0.25), (3.01, 0.1))):
    N = n_(n)
    return sum(g * osc(f * r, N) * env_exp(N, tau / r ** 0.5, 0.001) for r, g in harm)


def fm_can(fc=1320, oran=3.5, indeks=4.0, n=1.0, tau=0.35):
    N = n_(n)
    t = np.arange(N) / SR
    I = indeks * np.exp(-t / (tau * 0.4))
    mod = np.sin(2 * np.pi * fc * oran * t) * I
    return np.sin(2 * np.pi * fc * t + mod) * env_exp(N, tau, 0.001)


def kivilcim(n=0.6, adet=8, f=(4000, 8000), bas=0.0, yay=0.5):
    N = n_(n)
    y = np.zeros(N)
    for _ in range(adet):
        fr = L.R.uniform(*f)
        i = n_(bas + L.R.uniform(0, yay))
        m = n_(0.08)
        if i + m < N:
            y[i:i + m] += osc(fr, m) * env_exp(m, 0.018, 0.0005) * L.R.uniform(0.3, 1)
    return y


def gurultu_patlama(n=1.5, lpf=900, tau=0.4):
    N = n_(n)
    return lp(brown(N) * 0.6 + pink(N) * 0.4, lpf) * env_exp(N, tau, 0.004)


# ================================================================ motor tutusma
@aday('motor_tutusma', 'a', 'Kükreyen tutuşma', 'Kıvılcım, sonra kapağı açılan gürültü kükremesi ve alçak testere gövdesi.')
def _():
    N = n_(2.2)
    t = np.arange(N) / SR
    kiv = hp(white(N), 3000) * env_exp(N, 0.012, 0.0005)
    govde = sweep(brown(N) * 0.7 + pink(N) * 0.5, np.interp(t, [0, 0.6, 2.2], [150, 2600, 2200]), kind='lp', q=0.9)
    e = np.interp(t, [0, 0.05, 0.3, 1.5, 2.2], [0, 0.4, 1, 0.9, 0])
    cat = np.zeros(N)
    for i in L.R.integers(n_(0.1), N - 400, 120):
        cat[i:i + 300] += white(300) * env_exp(300, 0.002) * L.R.uniform(0.2, 1)
    cat = bp(cat, 1000, 4500) * np.interp(t, [0, 0.4, 2.2], [0, 1, 0.3])
    tes = lp(osc(np.interp(t, [0, 0.8, 2.2], [55, 88, 92]), N, 'saw'), 500) * e
    x = govde * e * 0.9 + cat * 0.5 + tes * 0.6 + kiv * 0.6
    return verb(sat(x * 0.8, 1.6), 0.7, 0.15)


@aday('motor_tutusma', 'b', 'Fıs... VUUM!', 'Çizgi film fitili (ince tıslama) ve ardından tombul bir "vuum" ateşleme.')
def _():
    fit = sweep(white(n_(0.5)), expc(2000, 5000, n_(0.5)), q=3, kind='bp') * np.linspace(0.2, 1, n_(0.5))
    for k in range(6):
        i = n_(0.05 + k * 0.075)
        fit[i:i + 200] += white(200) * env_exp(200, 0.002) * 1.5
    N = n_(1.6)
    t = np.arange(N) / SR
    f = np.interp(t, [0, 0.35, 1.6], [70, 140, 120])
    vuum = lp(osc(f, N, 'saw') + 0.5 * osc(f * 0.5, N, 'square'), 1400) * env_adsr(N, 0.01, 0.4, 0.55, 0.6)
    gur = sweep(pink(N), np.interp(t, [0, 0.3, 1.6], [400, 3000, 1800]), kind='lp') * env_adsr(N, 0.005, 0.3, 0.6, 0.6)
    pf = tok(160, 50, 0.12, 0.6)
    return verb(sat(karis((fit, 0, 0.35), (vuum, 0.55, 0.7), (gur, 0.55, 0.8), (pf, 0.55, 0.9)), 1.8), 0.6, 0.18)


@aday('motor_tutusma', 'c', 'Turbo şarj + ateşleme', 'Yükselen şarj ıslığı (gerilim), tepede patlayan ateşleme ve kısa kükreme.')
def _():
    n1 = n_(1.1)
    t1 = np.arange(n1) / SR
    f = expc(180, 1100, n1)
    sarj = (osc(f, n1) + 0.25 * osc(f * 0.5, n1, 'square')) * np.linspace(0.1, 1, n1) ** 1.5
    sarj += sweep(white(n1), f * 2, q=4, kind='bp') * np.linspace(0, 0.6, n1)
    N = n_(1.3)
    t = np.arange(N) / SR
    ates = hp(white(N), 1200) * env_exp(N, 0.03) * 0.8 + tok(110, 40, 0.15, 1.3) + gurultu_patlama(1.3, 1500, 0.45) * 1.2
    ates += lp(osc(np.interp(t, [0, 1.3], [80, 95]), N, 'saw'), 600) * env_adsr(N, 0.01, 0.3, 0.4, 0.5) * 0.5
    return verb(sat(karis((sarj, 0, 0.35), (ates, 1.1, 1.0)), 1.5), 0.8, 0.2)


@aday('motor_tutusma', 'd', 'Kenney itici + tok başlangıç', 'Kenney "thrusterFire_000" (CC0) itici sesi, başına sentez tok ateşleme vuruşu eklendi.', 'karma')
def _():
    k = kenney('kenney_sci-fi-sounds/thrusterFire_000.ogg')
    k = fade(kirp_sessiz(k)[:n_(2.2)], 0.08, 0.5)
    k = normal(k)
    return karis((k, 0.04, 0.9), (tok(140, 45, 0.12, 0.7), 0, 0.8), (hp(white(n_(0.1)), 2500) * env_exp(n_(0.1), 0.01), 0, 0.5))


@aday('motor_tutusma', 'e', 'Pıt-pıt-VRUUM', 'Üç tekleme (çizgi film arabası gibi) ve ardından yükselen kükreme. En komik olanı.')
def _():
    parca = []
    for k, tt in enumerate([0, 0.22, 0.38]):
        n = n_(0.12)
        p = lp(white(n), 1500) * env_exp(n, 0.03, 0.001) + osc(expc(130, 70, n), n) * env_exp(n, 0.04)
        parca.append((p, tt, 0.7 + 0.1 * k))
    N = n_(1.5)
    t = np.arange(N) / SR
    f = np.interp(t, [0, 0.5, 1.5], [60, 100, 105])
    vr = lp(osc(f, N, 'saw') * (1 + 0.3 * np.sin(2 * np.pi * 18 * t)), 1100) * env_adsr(N, 0.02, 0.3, 0.7, 0.5)
    g = sweep(pink(N), np.interp(t, [0, 0.5, 1.5], [500, 2600, 2000]), kind='lp') * env_adsr(N, 0.03, 0.3, 0.6, 0.5)
    return verb(sat(karis(*parca, (vr, 0.55, 0.8), (g, 0.55, 0.7)), 1.6), 0.5, 0.15)


# ================================================================ motor ucus dongusu (L = 2,0 s, frekanslar 0,5 Hz katlari -> dongu kesintisiz)
DL = 2.0
DN = n_(DL)
DT = np.arange(DN) / SR


def dongu_sinus(f, kind='sine'):
    f = round(f * DL) / DL
    if kind == 'saw':
        return sum(((-1) ** (k + 1)) * np.sin(2 * np.pi * k * f * DT) / k for k in range(1, int(16000 / f)))
    return np.sin(2 * np.pi * f * DT)


@aday('motor_ucus', 'a', 'Gürleyen roket', 'Kalın gürültü kükremesi + 55 Hz testere gövde, 6 Hz hafif dalgalanma. Klasik roket.')
def _():
    g = dongu_filtre(brown(DN) * 0.6 + pink(DN) * 0.6, lambda f: bw_lp(900, 2)(f) * bw_hp(40, 2)(f))
    mid = dongu_filtre(pink(DN), lambda f: bw_lp(1800, 2)(f) * bw_hp(400, 2)(f)) * 0.5
    d = dongu_filtre(dongu_sinus(55, 'saw'), bw_lp(500, 2)) * 0.35
    am = 1 + 0.15 * np.sin(2 * np.pi * 6 * DT)
    return (g + mid + d) * am


@aday('motor_ucus', 'b', 'Çizgi film jet ıslığı', 'Daha tiz: 880/1320 Hz ıslık + orta bant hava sesi. Telefonda en iyi duyulan tür.')
def _():
    hava = dongu_filtre(pink(DN), lambda f: bw_hp(600, 2)(f) * bw_lp(4500, 2)(f))
    gov = dongu_filtre(brown(DN), lambda f: bw_lp(400, 2)(f) * bw_hp(50, 2)(f)) * 0.5
    fm = 1 + 0.004 * np.sin(2 * np.pi * 5 * DT)
    isl = np.sin(2 * np.pi * np.cumsum(np.full(DN, 880.0) * fm) / SR) * 0.18 + dongu_sinus(1320) * 0.08
    return hava * 0.7 + gov + isl


@aday('motor_ucus', 'c', 'Derin çatırtılı', 'Alçak gürleme ve sürekli çatırtı (yanma). Ağır, güçlü his; telefonda alçak kısım kaybolabilir.')
def _():
    g = dongu_filtre(brown(DN), lambda f: bw_lp(220, 2)(f) * bw_hp(30, 2)(f)) * 1.2
    mid = dongu_filtre(pink(DN), lambda f: bw_lp(1200, 2)(f) * bw_hp(300, 2)(f)) * 0.35
    cat = np.zeros(DN)
    for i in L.R.integers(0, DN, 90):
        j = (i + np.arange(250)) % DN
        cat[j] += L.R.standard_normal(250) * np.exp(-np.arange(250) / 60) * L.R.uniform(0.3, 1)
    cat = dongu_filtre(cat, lambda f: bw_hp(800, 2)(f) * bw_lp(3500, 2)(f)) * 0.5
    return g + mid + cat


@aday('motor_ucus', 'd', 'Kenney uzay motoru', 'Kenney "spaceEngineLarge_000" (CC0) kesitinden çapraz geçişle döngü yapıldı.', 'kenney')
def _():
    k = kenney('kenney_sci-fi-sounds/spaceEngineLarge_000.ogg')
    a = n_(1.0)
    xf = n_(0.3)
    y = k[a:a + DN].copy()
    tail = k[a + DN:a + DN + xf]
    w = np.linspace(0, np.pi / 2, xf)
    y[:xf] = y[:xf] * np.sin(w) + tail * np.cos(w)
    return y


@aday('motor_ucus', 'e', 'Pırpır çizgi film', 'Testere 110 Hz, 25 Hz "pırpır" titreşimi ve hafif hava. Oyuncak roket gibi, en karikatür.')
def _():
    d = dongu_filtre(dongu_sinus(110, 'saw') + 0.5 * dongu_sinus(55, 'saw'), lambda f: bw_lp(1300, 2)(f))
    am = 0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 12.5 * DT))
    hava = dongu_filtre(pink(DN), lambda f: bw_hp(500, 2)(f) * bw_lp(3000, 2)(f)) * 0.35
    return d * am * 0.6 + hava


def motor_demo(loop, sure=5.0):
    """Hiz 0 -> 1 (4 s) -> 1: oynatma hizi 0,7 -> 1,6, alcak geciren 1200 -> 6800 Hz, kazanc 0,55 -> 1. secici.html ayni eslemeyi kullanir."""
    N = n_(sure)
    t = np.arange(N) / SR
    s = np.clip(t / 4.0, 0, 1)
    r = 0.7 + 0.9 * s
    pos = np.cumsum(r)
    tiled = np.tile(loop, int(pos[-1] / len(loop)) + 2)
    y = np.interp(pos, np.arange(len(tiled)), tiled)
    y = sweep(y, 1200 * 2 ** (2.5 * s), q=0.7, kind='lp') * (0.55 + 0.45 * s)
    return fade(y, 0.15, 0.3)


# ================================================================ trambolin
@aday('sekme_trambolin', 'a', 'Şartname "boing" (sinüs 300→600 Hz, 120 ms)', 'TASARIM §14\'teki basit tarif, aynen.')
def _():
    N = n_(0.16)
    return osc(expc(300, 600, N), N) * env_exp(N, 0.05, 0.003)


@aday('sekme_trambolin', 'b', 'Yay boyoing', 'Hızla yükselen perde, sönen titreşim (yay), altında tok vuruş. Klasik çizgi film.')
def _():
    return karis((boing(), 0, 0.8), (tok(110, 50, 0.06, 0.3), 0, 0.6))


@aday('sekme_trambolin', 'c', 'Ağız arpı "boyoyoyng"', 'Testere + gezen formant (12 Hz). Daha "lastik", daha gülünç.')
def _():
    N = n_(0.6)
    t = np.arange(N) / SR
    x = osc(np.interp(t, [0, 0.05, 0.6], [100, 130, 125]), N, 'saw')
    fc = 700 + 600 * np.sin(2 * np.pi * 12 * t) * np.exp(-t / 0.3) + 500 * np.exp(-t / 0.08)
    y = sweep(x, fc, q=4, kind='bp') * env_exp(N, 0.2, 0.003)
    return karis((y, 0, 1.2), (tok(120, 55, 0.05, 0.3), 0, 0.5))


@aday('sekme_trambolin', 'd', 'Kenney yumuşak + cıvıltı', 'Kenney "impactSoft_heavy_000" (CC0) yumuşak vuruş + sentez yükselen cıvıltı.', 'karma')
def _():
    k = normal(kirp_sessiz(kenney('kenney_impact-sounds/impactSoft_heavy_000.ogg')))
    N = n_(0.25)
    c = osc(expc(250, 520, N), N) * env_exp(N, 0.1, 0.003)
    return karis((k, 0, 0.9), (c, 0.01, 0.5))


@aday('sekme_trambolin', 'e', 'Lastik tok', 'Kısa, tok, doygun alçak vuruş + minik lastik gıcırtısı. En "vurucu" olanı, en az müzikal.')
def _():
    N = n_(0.05)
    sq = osc(expc(900, 1400, N), N) * env_exp(N, 0.015, 0.001)
    return sat(karis((tok(140, 55, 0.08, 0.35), 0, 1.0), (sq, 0.005, 0.35)), 2.0)


# ================================================================ marti
@aday('carpma_marti', 'a', 'Şartname "pof" (gürültü 60 ms)', 'TASARIM §14 tarifi aynen.')
def _():
    N = n_(0.06)
    return lp(white(N), 2500) * env_exp(N, 0.02, 0.001)


@aday('carpma_marti', 'b', 'Pof + tüy + çığlık', 'Yumuşak pof, kanat çırpınışı ve çizgi film martı çığlığı. Olanı tam anlatıyor.')
def _():
    pof = lp(pink(n_(0.2)), 1800) * env_exp(n_(0.2), 0.04, 0.001)
    return karis((pof, 0, 0.9), (tok(140, 70, 0.05, 0.25), 0, 0.6), (kanat(0.5), 0.03, 0.5), (ciglik(), 0.07, 0.45))


@aday('carpma_marti', 'c', 'Kenney yumruk + kumaş kanat', 'Kenney "impactPunch_medium_000" + "cloth1" (CC0) ve sentez çığlık.', 'karma')
def _():
    p = normal(kirp_sessiz(kenney('kenney_impact-sounds/impactPunch_medium_000.ogg')))
    c = normal(kirp_sessiz(kenney('kenney_rpg-audio/cloth1.ogg')))
    return karis((p, 0, 0.9), (c, 0.02, 0.5), (ciglik(0.2, 1400, 950), 0.06, 0.35))


@aday('carpma_marti', 'd', 'Çift çığlık', 'Pof ve iki kısa çığlık (ikincisi tiz): kalabalık sürü dağılıyor hissi.')
def _():
    pof = lp(pink(n_(0.2)), 1600) * env_exp(n_(0.2), 0.035, 0.001)
    return karis((pof, 0, 0.9), (ciglik(0.16, 1250, 900), 0.05, 0.4), (ciglik(0.16, 1550, 1150, 45), 0.2, 0.32), (kanat(0.45, 26, 0.18), 0.02, 0.4))


@aday('carpma_marti', 'e', 'Yastık + tüy bulutu', 'Yumuşak yastık vuruşu ve uzun tüy hışırtısı; çığlık yok, en sakin olanı.')
def _():
    N = n_(0.7)
    th = lp(brown(n_(0.25)), 400) * env_exp(n_(0.25), 0.06, 0.002)
    tuy = np.zeros(N)
    for _ in range(14):
        i = n_(L.R.uniform(0.02, 0.5))
        m = n_(0.05)
        tuy[i:i + m] += white(m) * np.hanning(m) * L.R.uniform(0.3, 1)
    tuy = bp(tuy, 2500, 7000)
    return karis((th, 0, 1.0), (tuy, 0, 0.6), (tok(120, 60, 0.05, 0.25), 0, 0.4))


# ================================================================ balon
@aday('carpma_balon', 'a', 'Keskin "pat"', 'Kısa, temiz patlama ve küçük oda yankısı.')
def _():
    return verb(pat(0.15), 0.25, 0.25)


@aday('carpma_balon', 'b', 'Pat + lastik + konfeti', 'Patlama, ardından lastiğin "fivv" savrulması ve ince konfeti şıngırtısı.')
def _():
    N = n_(0.14)
    fw = sweep(white(N), expc(3000, 600, N), q=3, kind='bp') * env_exp(N, 0.06, 0.002)
    return karis((pat_dolgun(0.2), 0, 1.0), (fw, 0.02, 0.6), (kivilcim(0.5, 6, (4500, 7500), 0.05, 0.3), 0, 0.2))


@aday('carpma_balon', 'c', 'Pat + hava kaçışı', 'Patlama ve alçalan ıslık (çizgi filmde sönen balon). Komik.')
def _():
    N = n_(0.35)
    isl = osc(expc(1400, 350, N), N) * env_adsr(N, 0.01, 0.1, 0.7, 0.1)
    return karis((pat_dolgun(0.2), 0, 1.0), (isl, 0.02, 0.3), (lp(white(N), 3000) * env_exp(N, 0.1), 0.02, 0.15))


@aday('carpma_balon', 'd', 'Büyük reklam balonu', 'Patlama + gövdeli alçak "bum" + yankı. Büyük balon için iri.')
def _():
    return yumusat(verb(karis((pat_dolgun(0.25), 0, 1.0), (tok(130, 60, 0.15, 0.6), 0, 0.9), (gurultu_patlama(0.5, 600, 0.1), 0, 0.6)), 0.5, 0.2), 2.0)


@aday('carpma_balon', 'e', 'Kenney çatırtı tiz', 'Kenney "explosionCrunch_000" (CC0) 1,6 kat hızlandırılıp tizleştirildi + tık.', 'karma')
def _():
    k = normal(hiz(kirp_sessiz(kenney('kenney_sci-fi-sounds/explosionCrunch_000.ogg')), 1.6))
    return karis((k, 0, 0.9), (pat(0.08), 0, 0.5))


# ================================================================ kademe ayrilma
@aday('kademe_ayrilma', 'a', 'Piro cıvata + metal halka', 'Patlayıcı cıvata çatlaması, çınlayan halka ve gövdeye tok darbe (A0 motorundaki "piro"nun gelişmişi).')
def _():
    N = n_(0.15)
    cr = hp(white(N), 2200) * env_exp(N, 0.012, 0.0005)
    return verb(yumusat(karis((cr, 0, 1.0), (metal(n=1.0), 0, 0.25), (lp(brown(n_(0.6)), 200) * env_exp(n_(0.6), 0.12, 0.003), 0, 1.0),
                              (tok(95, 45, 0.15, 0.5), 0, 0.6)), 2.5), 0.6, 0.2)


@aday('kademe_ayrilma', 'b', 'Kenney metal + tıslama', 'Kenney "impactMetal_heavy_000" (CC0) + basınç tıslaması + alçak vuruş.', 'karma')
def _():
    k = normal(kirp_sessiz(kenney('kenney_impact-sounds/impactMetal_heavy_000.ogg')))
    N = n_(0.8)
    his = hp(white(N), 2500) * env_adsr(N, 0.02, 0.1, 0.6, 0.6) * 0.5
    return verb(karis((k, 0, 1.0), (his, 0.05, 0.5), (tok(100, 45, 0.12, 0.5), 0, 0.7)), 0.4, 0.15)


@aday('kademe_ayrilma', 'c', 'Ka-çank + pışşş', 'İki metal vuruş (ka-ÇANK) ve uzun tıslama. Çizgi film, ritmik.')
def _():
    m1 = metal((420, 1090, 1730), (1, .6, .4), 0.08, 0.3)
    m2 = metal((380, 980, 1610, 2400), (1, .7, .5, .3), 0.15, 0.5)
    N = n_(0.9)
    his = bp(white(N), 2000, 8000) * env_adsr(N, 0.01, 0.2, 0.5, 0.6)
    return verb(karis((m1, 0, 0.6), (tok(160, 70, 0.04, 0.2), 0, 0.5), (m2, 0.12, 0.9), (tok(110, 45, 0.1, 0.4), 0.12, 0.9), (his, 0.16, 0.35)), 0.4, 0.15)


@aday('kademe_ayrilma', 'd', 'Patlamalı ayrılma', 'Kenney "explosionCrunch_001" (CC0) patlaması + metal halka + tok vuruş. En dramatik.', 'karma')
def _():
    k = normal(kirp_sessiz(kenney('kenney_sci-fi-sounds/explosionCrunch_001.ogg')))
    return verb(karis((k, 0, 0.9), (metal(n=1.0, tau=0.3), 0.01, 0.2), (tok(90, 40, 0.15, 0.6), 0, 0.7)), 0.7, 0.2)


@aday('kademe_ayrilma', 'e', 'Yay fırlatma', 'Klank + yay "boink" bırakma + yukarı süpüren vuuş: "yeniden fırladın" hissi.')
def _():
    N = n_(0.35)
    t = np.arange(N) / SR
    yay = osc(expc(600, 200, N) * (1 + 0.1 * np.sin(2 * np.pi * 18 * t)), N) * env_exp(N, 0.15)
    return karis((metal((520, 1310), (1, .5), 0.06, 0.3), 0, 0.6), (tok(120, 50, 0.06, 0.3), 0, 0.7), (yay, 0.03, 0.5), (vuus(0.45, 500, 3500, 1.2), 0.12, 0.6))


# ================================================================ dalis
@aday('dalis', 'a', 'Şartname "vuuş" (bant süpürme 250 ms)', 'TASARIM §14 tarifi; vuruş katmanı yok.')
def _():
    return vuus(0.25, 500, 2500, 1.5, 'tepe')


@aday('dalis', 'b', 'Vuuş + tok vuruş', 'Yükselen hava süpürmesi, tam tepede doygun tok vuruş. Dengeli.')
def _():
    return sat(karis((vuus(0.28, 400, 3000), 0, 0.8), (tok(120, 45, 0.09, 0.45), 0.27, 1.0)), 1.5)


@aday('dalis', 'c', 'Bomba ıslığı + güm', 'Alçalan çizgi film ıslığı ("fiiiuuu") ve güm. En karikatür.')
def _():
    N = n_(0.35)
    t = np.arange(N) / SR
    isl = osc(expc(1900, 600, N) * (1 + 0.01 * np.sin(2 * np.pi * 7 * t)), N) * env_adsr(N, 0.02, 0.1, 0.8, 0.02)
    return karis((isl, 0, 0.35), (tok(110, 40, 0.12, 0.5), 0.35, 1.0), (gurultu_patlama(0.3, 1200, 0.06), 0.35, 0.5))


@aday('dalis', 'd', 'Vuuş + Kenney yumruk', 'Sentez vuuş + Kenney "impactPunch_heavy_000" (CC0) yumruk.', 'karma')
def _():
    k = normal(kirp_sessiz(kenney('kenney_impact-sounds/impactPunch_heavy_000.ogg')))
    return karis((vuus(0.26, 400, 3200), 0, 0.7), (k, 0.25, 1.0))


@aday('dalis', 'e', 'Hava yırtılması + klank', 'Yukarıdan aşağı inen hava yırtılması ve metalik klank.')
def _():
    N = n_(0.3)
    y = sweep(white(N), expc(4000, 800, N), q=2, kind='bp') * np.linspace(0.3, 1, N)
    return yumusat(karis((y, 0, 0.8), (metal((700, 1650, 2600), (1, .5, .3), 0.07, 0.3), 0.29, 0.5), (tok(130, 50, 0.07, 0.35), 0.29, 0.9)), 2.5)


# ================================================================ mukemmel
@aday('mukemmel', 'a', 'Şartname "ding" (880 + 1320 Hz, 200 ms)', 'TASARIM §14 tarifi aynen.')
def _():
    N = n_(0.22)
    return (osc(880, N) + osc(1320, N) * 0.7) * env_exp(N, 0.07, 0.002)


@aday('mukemmel', 'b', 'Arpej + parıltı + boing', 'Do-Mi-Sol-Do hızlı arpej, kıvılcım parıltısı ve altta yay boing. "Aferin" hissi.')
def _():
    notalar = [1047, 1319, 1568, 2093]
    parc = [(can(f, 0.5, 0.2), i * 0.045, 0.5) for i, f in enumerate(notalar)]
    return verb(karis(*parc, (kivilcim(0.7, 10, (5000, 9000), 0.1, 0.4), 0, 0.2), (boing(200, 450, 0.4), 0, 0.45), (tok(130, 60, 0.05, 0.3), 0, 0.5)), 0.5, 0.2)


@aday('mukemmel', 'c', 'FM çan + şok dalgası', 'Parlak FM çanı, aşağı süpüren şok "vuuş" ve tok vuruş.')
def _():
    return verb(karis((fm_can(1320, 3.5, 3.0, 0.9, 0.35), 0, 0.5), (vuus(0.3, 3000, 800, 1.2, 'tepe'), 0, 0.6), (tok(130, 55, 0.07, 0.35), 0, 0.8)), 0.5, 0.2)


@aday('mukemmel', 'd', 'Kenney güç + boing', 'Kenney "powerUp2" (CC0) ve sentez yay boing.', 'karma')
def _():
    k = normal(kirp_sessiz(kenney('kenney_digital-audio/powerUp2.ogg')))
    return karis((k, 0, 0.7), (boing(200, 450, 0.4), 0, 0.5), (tok(130, 60, 0.05, 0.3), 0, 0.5))


@aday('mukemmel', 'e', 'Zil + boing', 'Kenney "impactBell_heavy_000" (CC0) zil (0,8 s) ve yay boing. Ring zili gibi.', 'karma')
def _():
    k = normal(fade(kirp_sessiz(kenney('kenney_impact-sounds/impactBell_heavy_000.ogg'))[:n_(0.8)], 0, 0.2))
    return karis((k, 0, 0.7), (boing(200, 450, 0.4), 0, 0.5))


# ================================================================ ses duvari
@aday('ses_duvari', 'a', 'Şartname "BUM" (60 Hz sinüs + gürültü, 400 ms)', 'TASARIM §14 tarifi aynen. Ölçüm: telefonda büyük kısmı kaybolur.')
def _():
    N = n_(0.4)
    return osc(60, N) * env_exp(N, 0.15, 0.003) + lp(white(N), 1500) * env_exp(N, 0.08) * 0.4


@aday('ses_duvari', 'b', 'N-dalga çift çatlak + parıltı', 'Gerçek ses patlaması gibi iki çatlak (0,1 s arayla), gövdeli bum, ardından yükselen parıltılı "vuuum".')
def _():
    def catlak():
        N = n_(0.6)
        c = hp(white(N), 1500) * env_exp(N, 0.006, 0.0002)
        c[:20] += 3 * np.sign(white(20))
        return c + bp(white(N), 200, 2000) * env_exp(N, 0.12, 0.001) * 0.8
    N = n_(1.8)
    t = np.arange(N) / SR
    pari = bp(pink(N), 1000, 5000) * np.sin(np.pi * np.clip(t / 1.8, 0, 1)) ** 2 * 0.25 + (osc(660, N) + osc(990, N) * 0.6) * np.sin(np.pi * t / 1.8) ** 3 * 0.08
    x = karis((catlak(), 0, 1.0), (catlak(), 0.1, 0.9), (gurultu_patlama(1.6, 700, 0.5), 0, 1.0), (tok(80, 35, 0.4, 1.5), 0, 0.8), (pari, 0.3, 1.0))
    return yumusat(verb(sat(x, 1.6), 1.6, 0.3), 2.5)


@aday('ses_duvari', 'c', 'Emme + BUM + çınlama', 'Ters "emme" (0,45 s gerilim), sonra çatlak + doygun bum + metalik çınlama ve uzun kuyruk. En sinematik.')
def _():
    n1 = n_(0.45)
    em = sweep(white(n1), expc(300, 6000, n1), kind='lp') * np.linspace(0, 1, n1) ** 3
    N = n_(2.2)
    c = hp(white(N), 1500) * env_exp(N, 0.008, 0.0002)
    bum = sat(gurultu_patlama(2.2, 1200, 0.35) * 2.0, 2.5) + tok(70, 30, 0.5, 2.2) * 0.7
    cin = metal((880, 1320, 1975, 2637), (1, .8, .5, .3), 0.8, 2.0) * 0.12
    return yumusat(verb(karis((em, 0, 0.6), (c, 0.45, 1.0), (bum, 0.45, 0.9), (cin, 0.47, 1.0)), 2.0, 0.3), 2.5)


@aday('ses_duvari', 'd', 'Kenney alçak patlama + çatlak', 'Kenney "lowFrequency_explosion_000" (CC0) + sentez çatlak ve orta bant takviyesi.', 'karma')
def _():
    k = normal(kirp_sessiz(kenney('kenney_sci-fi-sounds/lowFrequency_explosion_000.ogg')))
    N = n_(0.6)
    c = hp(white(N), 1500) * env_exp(N, 0.008, 0.0002) + bp(white(N), 300, 2500) * env_exp(N, 0.15) * 0.7
    return verb(karis((k, 0, 1.0), (c, 0, 0.8)), 1.2, 0.2)


@aday('ses_duvari', 'e', 'BUM + fanfar', 'Bum ve hemen ardından iki vuruşlu bakır fanfar ("ta-DAA!"). Ödül anı gibi, en neşeli.')
def _():
    def bakir(fs, n):
        N = n_(n)
        x = sum(osc(f * np.r_[1.0], N, 'saw') + osc(f * 1.004, N, 'saw') for f in fs)
        t = np.arange(N) / SR
        x = sweep(x, 400 + 3500 * (1 - np.exp(-t / 0.06)) * np.exp(-t / 1.5), q=0.8, kind='lp')
        return x * env_adsr(N, 0.015, 0.2, 0.7, 0.25) / len(fs)
    N = n_(0.6)
    c = hp(white(N), 1500) * env_exp(N, 0.008, 0.0002)
    akor = [233.1, 293.7, 349.2, 466.2]
    return yumusat(verb(karis((c, 0, 1.0), (gurultu_patlama(1.2, 800, 0.35), 0, 1.0), (tok(80, 35, 0.3, 1.0), 0, 0.7),
                           (bakir(akor, 0.16), 0.3, 0.9), (bakir([f * 1.335 for f in akor], 1.2), 0.5, 1.0)), 1.0, 0.2), 2.5)


# ================================================================ jeton
@aday('jeton', 'a', 'İki nota (Re-La)', 'Yumuşatılmış kare dalga, beşli aralık yukarı. Arcade jetonu.')
def _():
    n1, n2 = n_(0.07), n_(0.25)
    a = lp(osc(1175, n1, 'square'), 6000) * env_adsr(n1, 0.002, 0.02, 0.8, 0.005)
    b = lp(osc(1760, n2, 'square'), 6000) * env_exp(n2, 0.09, 0.002)
    return np.r_[a, b] * 0.6


@aday('jeton', 'b', 'Metal çın', 'Gerçek madeni para gibi uyumsuz kısmi tonlar (2,2 kHz kökenli) + tık.')
def _():
    return karis((metal((2200, 2200 * 2.76, 2200 * 5.4), (1, .5, .2), 0.18, 0.5), 0, 1.0), (hp(white(n_(0.01)), 3000) * env_exp(n_(0.01), 0.002), 0, 0.4))


@aday('jeton', 'c', 'Kenney para şıngırtısı', 'Kenney "handleCoins2" (CC0) aynen (kırpıldı).', 'kenney')
def _():
    return kirp_sessiz(kenney('kenney_rpg-audio/handleCoins2.ogg'))


@aday('jeton', 'd', 'Parıltılı iki çan', 'Mi-Si iki çan sesi 40 ms arayla + çok ince parıltı. Yumuşak, tekrar dinlemeye dayanıklı.')
def _():
    return karis((can(1319, 0.4, 0.12), 0, 0.6), (can(1976, 0.45, 0.14), 0.04, 0.6), (kivilcim(0.4, 5, (6000, 9000), 0.02, 0.15), 0, 0.15))


@aday('jeton', 'e', 'Kenney fiş + ding', 'Kenney "chips-collide-1" (CC0) + sentez yüksek ding.', 'karma')
def _():
    k = normal(kirp_sessiz(kenney('kenney_casino-audio/chips-collide-1.ogg')))
    return karis((k, 0, 0.8), (can(2637, 0.3, 0.08), 0.005, 0.3))


# ================================================================ ui tik
@aday('ui_tik', 'a', 'Yumuşak pop', 'Sinüs 1200→500 Hz, 35 ms. Yuvarlak, parlak arayüze uygun.')
def _():
    N = n_(0.05)
    return osc(expc(1200, 500, N), N) * env_exp(N, 0.012, 0.001)


@aday('ui_tik', 'b', 'Tahta tık', 'Kısa bant gürültü + 380 Hz gövde. Kuru, net.')
def _():
    N = n_(0.05)
    return bp(white(N), 1800, 3500) * env_exp(N, 0.004, 0.0003) + osc(380, N) * env_exp(N, 0.015, 0.0005) * 0.6


@aday('ui_tik', 'c', 'Kenney click_001', 'Kenney "Interface Sounds" (CC0) aynen.', 'kenney')
def _():
    return kirp_sessiz(kenney('kenney_interface-sounds/click_001.ogg'))


@aday('ui_tik', 'd', 'Kenney select_001', 'Kenney "Interface Sounds" (CC0) aynen.', 'kenney')
def _():
    return kirp_sessiz(kenney('kenney_interface-sounds/select_001.ogg'))


@aday('ui_tik', 'e', 'Baloncuk "blup"', 'Sinüs 380→900 Hz yükselen, 45 ms. Sevimli, çocuksu.')
def _():
    N = n_(0.06)
    return osc(expc(380, 900, N), N) * env_adsr(N, 0.003, 0.02, 0.6, 0.02)


# ================================================================ kart satin alma
@aday('kart_satin', 'a', 'Ka-çing!', 'Mekanik iki tık ve çan akoru (kasa çekmecesi gibi) + jeton parıltısı.')
def _():
    N = n_(0.03)
    tik = hp(white(N), 2500) * env_exp(N, 0.004, 0.0003)
    return verb(karis((tik, 0, 0.6), (tik, 0.05, 0.8), (fm_can(2093, 1.4, 2.0, 0.8, 0.35), 0.07, 0.4), (fm_can(2637, 1.4, 2.0, 0.8, 0.35), 0.07, 0.3),
                      (kivilcim(0.6, 6, (5000, 8000), 0.1, 0.3), 0, 0.15)), 0.4, 0.15)


@aday('kart_satin', 'b', 'Arpej + jeton yağmuru', 'Sol-Do-Mi-Sol yukarı arpej ve 6 jeton şıngırtısı. Ödül hissi en güçlü.')
def _():
    notalar = [784, 1047, 1319, 1568]
    parc = []
    for i, f in enumerate(notalar):
        n = n_(0.18)
        parc.append((lp(osc(f, n, 'square', 0.25), 5000) * env_exp(n, 0.06, 0.002), i * 0.05, 0.35))
    for k in range(6):
        parc.append((metal((2200 + 150 * k, (2200 + 150 * k) * 2.76), (1, .4), 0.1, 0.3), 0.15 + k * 0.07, 0.25))
    return karis(*parc)


@aday('kart_satin', 'c', 'Kenney onay', 'Kenney "confirmation_001" (CC0) aynen.', 'kenney')
def _():
    return kirp_sessiz(kenney('kenney_interface-sounds/confirmation_001.ogg'))


@aday('kart_satin', 'd', 'Kenney fiş yığını + çan', 'Kenney "chips-stack-1" (CC0) + sentez iki çan.', 'karma')
def _():
    k = normal(kirp_sessiz(kenney('kenney_casino-audio/chips-stack-1.ogg')))
    return karis((k, 0, 0.8), (can(1568, 0.5, 0.18), 0.12, 0.35), (can(2093, 0.5, 0.18), 0.17, 0.35))


@aday('kart_satin', 'e', 'Kart savur + damga', 'Kâğıt savurma vuuşu, tok damga vuruşu ve kısa parıltı arpeji.')
def _():
    N = n_(0.12)
    sw = sweep(white(N), expc(1500, 4000, N), q=1.5, kind='bp') * np.sin(np.pi * np.linspace(0, 1, N))
    parc = [(can(f, 0.3, 0.1), 0.18 + i * 0.04, 0.3) for i, f in enumerate([1319, 1568, 2093])]
    return karis((sw, 0, 0.6), (tok(160, 60, 0.06, 0.3), 0.12, 1.0), (hp(white(n_(0.03)), 1500) * env_exp(n_(0.03), 0.006), 0.12, 0.4), *parc)


# ================================================================ son sans
@aday('son_sans', 'a', 'İki ton alarm', 'Kare dalga 880/660 Hz, 3 tur (1,2 s). Net, tanıdık uyarı.')
def _():
    parc = []
    for k in range(6):
        n = n_(0.18)
        f = 880 if k % 2 == 0 else 660
        parc.append((lp(osc(f, n, 'square'), 3000) * env_adsr(n, 0.005, 0.03, 0.8, 0.03), k * 0.2, 0.5))
    return karis(*parc)


@aday('son_sans', 'b', 'Çizgi film korna "avuga"', 'İki kez burundan çalan korna, perde yukarı büküm. Komik ama acil.')
def _():
    def korna():
        N = n_(0.5)
        t = np.arange(N) / SR
        f = np.interp(t, [0, 0.25, 0.5], [290, 420, 410])
        x = osc(f, N, 'saw') * (1 + 0.3 * np.sin(2 * np.pi * 30 * t))
        return (bp(x, 600, 2200) + 0.3 * lp(x, 600)) * env_adsr(N, 0.02, 0.05, 0.9, 0.06)
    return karis((korna(), 0, 0.8), (korna(), 0.6, 0.8))


@aday('son_sans', 'c', 'Siren + kalp atışı', 'Tek tur siren (500→1300→500 Hz) ve altında iki "lup-dup" kalp atışı. Gerilimli.')
def _():
    N = n_(1.25)
    t = np.arange(N) / SR
    f = 500 + 800 * np.sin(np.pi * t / 1.25) ** 2
    sir = (osc(f, N, 'tri') + 0.3 * osc(2 * f, N)) * env_adsr(N, 0.03, 0.1, 0.9, 0.1)
    parc = [(sir, 0, 0.45)]
    for b in (0.05, 0.65):
        parc += [(tok(90, 50, 0.07, 0.3), b, 0.9), (tok(80, 45, 0.06, 0.3), b + 0.16, 0.7)]
    return karis(*parc)


@aday('son_sans', 'd', 'Kenney üç ton', 'Kenney "lowThreeTone" (CC0) aynen.', 'kenney')
def _():
    return kirp_sessiz(kenney('kenney_digital-audio/lowThreeTone.ogg'))


@aday('son_sans', 'e', 'Şartname "pat" + alçak gümbürtü', 'TASARIM §14 tarifi: patlama ve 1 s alçak gümbürtü.')
def _():
    N = n_(1.1)
    g = lp(brown(N), 150) * env_adsr(N, 0.02, 0.2, 0.7, 0.4)
    return karis((pat(0.2), 0, 0.8), (g, 0, 1.0))


# ================================================================ muzik
NOTA = {'C': 0, 'Db': 1, 'D': 2, 'Eb': 3, 'E': 4, 'F': 5, 'Gb': 6, 'G': 7, 'Ab': 8, 'A': 9, 'Bb': 10, 'B': 11}


def mf(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def akor(ad):
    """'Em', 'C', 'B7', 'C7', 'Bb' ... -> (kok midi 3. oktav, akor tonlari 4. oktav civari)"""
    kok = ad[:2] if len(ad) > 1 and ad[1] == 'b' else ad[:1]
    tur = ad[len(kok):]
    r = NOTA[kok]
    aral = [0, 3, 7] if tur.startswith('m') else [0, 4, 7]
    if tur.endswith('7'):
        aral = aral + [10]
    ton = [60 + ((r + a) % 12) for a in aral]
    ton = sorted(t if t < 67 else t - 12 for t in ton)
    return 36 + r if r < 7 else 24 + r, ton


# ---- calgilar (mono dizi dondurur)
def kick(v=1.0):
    N = n_(0.3)
    return (osc(48 + 112 * np.exp(-np.arange(N) / SR / 0.03), N) * env_exp(N, 0.12, 0.001) + lp(white(N), 4000) * env_exp(N, 0.004) * 0.3) * v


def snare(v=1.0):
    N = n_(0.25)
    return (bp(white(N), 1200, 7000) * env_exp(N, 0.07, 0.001) * 0.8 + osc(190, N) * env_exp(N, 0.04, 0.001) * 0.6) * v


def clap(v=1.0):
    N = n_(0.25)
    e = np.zeros(N)
    for d in (0, 0.01, 0.02):
        e[n_(d):] += env_exp(N - n_(d), 0.012 if d < 0.02 else 0.08, 0.0005)
    return bp(white(N), 900, 5000) * e * 0.7 * v


def hat(v=1.0, acik=False):
    N = n_(0.25 if acik else 0.06)
    return hp(white(N), 7000) * env_exp(N, 0.12 if acik else 0.015, 0.0005) * 0.5 * v


def tahta(v=1.0, f=1800):
    N = n_(0.08)
    return (osc(f, N) + 0.5 * osc(f * 2.7, N)) * env_exp(N, 0.015, 0.0005) * v


def bas_saw(f, d, v=1.0, lpf=700):
    N = n_(d)
    t = np.arange(N) / SR
    x = osc(f, N, 'saw') + 0.5 * osc(f / 2, N, 'square')
    return sweep(x, lpf * (0.5 + 1.5 * np.exp(-t / 0.08)), q=1.2, kind='lp') * env_adsr(N, 0.004, 0.08, 0.7, 0.03) * v * 0.6


def tuba(f, d, v=1.0):
    N = n_(d)
    t = np.arange(N) / SR
    x = osc(f * (1 + 0.006 * np.sin(2 * np.pi * 5 * t)), N, 'saw')
    return sweep(x, 250 + 600 * np.exp(-t / 0.1), q=0.9, kind='lp') * env_adsr(N, 0.02, 0.08, 0.75, 0.04) * v


def ucgen_bas(f, d, v=1.0):
    N = n_(d)
    return osc(f, N, 'tri') * env_adsr(N, 0.002, 0.02, 0.85, 0.01) * v * 0.8


def pulse(f, d, v=1.0, duty=0.5, vib=0.0, lpf=7000):
    N = n_(d)
    t = np.arange(N) / SR
    ff = f * (1 + vib * np.clip((t - 0.12) / 0.1, 0, 1) * np.sin(2 * np.pi * 6 * t))
    return lp(osc(ff, N, 'square', duty), lpf) * env_adsr(N, 0.003, 0.05, 0.7, 0.03) * v * 0.4


def ksilofon(f, d, v=1.0):
    N = n_(max(d, 0.35))
    return (osc(f, N) + 0.35 * osc(f * 3.93, N) * env_exp(N, 0.03) + 0.12 * osc(f * 9.2, N) * env_exp(N, 0.01)) * env_exp(N, 0.12, 0.001) * v * 0.7


def pizz(f, d, v=1.0):
    N = n_(0.3)
    x = sum(osc(f * k, N) * env_exp(N, 0.12 / k, 0.001) / k for k in range(1, 6))
    return x * v * 0.5


def stab(fs, d, v=1.0, lpf=2500):
    N = n_(d)
    t = np.arange(N) / SR
    x = sum(osc(mf(m), N, 'saw') + osc(mf(m) * 1.005, N, 'saw') for m in fs) / len(fs)
    return sweep(x, lpf * (0.4 + 0.6 * np.exp(-t / 0.05)), q=0.9, kind='lp') * env_adsr(N, 0.003, 0.05, 0.6, 0.02) * v * 0.6


def org(fs, d, v=1.0):
    N = n_(d)
    x = sum(osc(mf(m), N, 'square', 0.5) * 0.5 + osc(mf(m) * 2, N) * 0.3 for m in fs) / len(fs)
    return lp(x, 3500) * env_adsr(N, 0.004, 0.04, 0.8, 0.02) * v * 0.5


def bakir_lead(f, d, v=1.0):
    N = n_(d)
    t = np.arange(N) / SR
    ff = f * (1 + 0.012 * np.clip((t - 0.15) / 0.1, 0, 1) * np.sin(2 * np.pi * 5.5 * t))
    x = osc(ff, N, 'saw') + osc(ff * 1.003, N, 'saw')
    return sweep(x, 600 + 2800 * (1 - np.exp(-t / 0.04)), q=0.8, kind='lp') * env_adsr(N, 0.02, 0.1, 0.8, 0.04) * v * 0.3


def twang(f, d, v=1.0):
    """Surf gitari benzeri: kisa tel + tremolo + hafif dist."""
    N = n_(d + 0.1)
    t = np.arange(N) / SR
    x = sum(osc(f * k * (1 + 0.004 * np.sin(2 * np.pi * 6 * t)), N) * env_exp(N, 0.6 / k, 0.002) / k for k in range(1, 7))
    return sat(x * 1.3, 1.5) * env_adsr(N, 0.003, 0.05, 0.85, 0.06) * v * 0.45


# ---- izleyici
class Parca:
    def __init__(self, bpm, olcu):
        self.bpm, self.olcu = bpm, olcu
        self.vurus = 60.0 / bpm
        self.L = olcu * 4 * self.vurus
        self.N = n_(self.L)
        self.katman = [np.zeros((2, self.N + n_(3))) for _ in range(3)]

    def koy(self, k, x, vur, pan=0.0):
        """x'i vur. vuruşa (dörtlük) koyar; dongu sonunu asan kuyruk sonra basa katlanir."""
        i = n_(vur * self.vurus)
        a = np.cos((pan + 1) * np.pi / 4)
        b = np.sin((pan + 1) * np.pi / 4)
        buf = self.katman[k]
        x = x[:buf.shape[1] - i]
        buf[0, i:i + len(x)] += x * a
        buf[1, i:i + len(x)] += x * b

    def bitir(self, yanki=(0.15, 0.15, 0.2)):
        out = []
        for k, buf in enumerate(self.katman):
            y = buf[:, :self.N].copy()
            y[:, :buf.shape[1] - self.N] += buf[:, self.N:]
            if yanki[k] > 0:  # dairesel yanki (dongu bozulmaz)
                rr = np.random.default_rng(10 + k)
                m = n_(0.9)
                ir = np.zeros(self.N)
                ir[:m] = lp(rr.standard_normal(m) * np.exp(-6.9 * np.arange(m) / m), 4500)
                ir /= np.sqrt(np.sum(ir ** 2))
                I = np.fft.rfft(ir)
                for c in range(2):
                    wet = np.fft.irfft(np.fft.rfft(y[c]) * I, self.N)
                    y[c] += yanki[k] * wet * (np.std(y[c]) / (np.std(wet) + 1e-12))
            out.append(y)
        return out


def melodi(p, k, notalar, cal, bas_olcu=0, pan=0.0, v=1.0, okt=0):
    vur = bas_olcu * 4
    for m, d in notalar:
        if m > 0:
            p.koy(k, cal(mf(m + okt), d * p.vurus * 0.95, v), vur, pan)
        vur += d


def m_bar(*ler):
    out = []
    for b in ler:
        assert abs(sum(d for _, d in b) - 4) < 1e-9, b
        out += b
    return out


@aday('muzik', 'a', 'Roket sörfü (160 BPM, Mi minör)', 'Dörtnala surf basları, ardından kesik akorlar, en üstte tremololu "twang" gitar ezgisi. Hızlı ve çizgi filmsi.')
def _():
    p = Parca(160, 16)
    prog = ['Em', 'C', 'D', 'B7'] * 3 + ['Am', 'C', 'D', 'B7']
    for o, a in enumerate(prog):
        r, ton = akor(a)
        b = o * 4
        for s in range(4):
            p.koy(0, kick(1.0 if s % 2 == 0 else 0.0) if s % 2 == 0 else snare(0.9), b + s)
            p.koy(0, hat(0.6), b + s + 0.5, 0.3)
            p.koy(0, hat(0.4), b + s, 0.3)
        p.koy(0, kick(0.7), b + 2.5)
        pat_ = [0, 0, 0, 12, 0, 0, 7, 12]
        for s in range(8):
            p.koy(0, bas_saw(mf(r + pat_[s]), 0.45 * p.vurus, 0.9, 900), b + s * 0.5)
        for s in (0.5, 1.5, 2.5, 3.5):
            p.koy(1, stab(ton, 0.35 * p.vurus, 0.8, 2800), b + s, -0.4)
        for s in range(16):
            p.koy(1, hat(0.25), b + s * 0.25, 0.6)
    mel = m_bar([(71, .5), (76, .5), (79, 1), (78, .5), (76, .5), (74, 1)], [(76, 1.5), (72, .5), (71, 1), (67, 1)],
                [(74, .5), (78, .5), (81, 1), (79, .5), (78, .5), (74, 1)], [(75, 1.5), (78, .5), (83, 2)],
                [(83, .5), (81, .5), (79, .5), (76, .5), (79, 1), (76, 1)], [(72, .5), (76, .5), (79, 1), (84, 1), (79, 1)],
                [(81, 1), (78, .5), (74, .5), (78, 1), (81, 1)], [(83, 1), (78, 1), (75, 1), (71, 1)])
    melodi(p, 2, mel, twang, 0, 0.1)
    melodi(p, 2, mel, twang, 8, 0.1, 1.0)
    for o in range(16):
        p.koy(2, tahta(0.3, 2200), o * 4 + 3.5, -0.5)
    return p


@aday('muzik', 'b', 'Çiptün hız (150 BPM, Do majör)', 'Oyun konsolu tadında: üçgen bas, 16\'lık arpej, titreşimli kare dalga ezgi. En "oyunsu".')
def _():
    p = Parca(150, 16)
    prog = ['C', 'G', 'Am', 'F'] * 4
    for o, a in enumerate(prog):
        r, ton = akor(a)
        b = o * 4
        for s in range(4):
            p.koy(0, kick(0.9), b + s)
            if s % 2:
                p.koy(0, snare(0.7), b + s)
            p.koy(0, hat(0.35), b + s + 0.5, 0.2)
        for s in range(8):
            p.koy(0, ucgen_bas(mf(r + 12 + (12 if s % 2 else 0)), 0.45 * p.vurus, 1.0), b + s * 0.5)
        arp = ton + [ton[0] + 12]
        for s in range(16):
            p.koy(1, pulse(mf(arp[s % 4] + 12), 0.22 * p.vurus, 0.55, 0.125, 0, 6000), b + s * 0.25, -0.3 + 0.6 * (s % 2))
    mel = m_bar([(76, .5), (79, .5), (84, 1), (83, .5), (81, .5), (79, 1)], [(79, .5), (81, .5), (83, 1), (86, 1), (83, 1)],
                [(84, 1.5), (81, .5), (76, 1), (81, 1)], [(77, .5), (79, .5), (81, 1), (79, .5), (77, .5), (76, 1)],
                [(72, .5), (76, .5), (79, .5), (84, .5), (88, 1), (84, 1)], [(86, .5), (84, .5), (83, .5), (79, .5), (83, 2)],
                [(81, .5), (84, .5), (88, 1), (86, .5), (84, .5), (81, 1)], [(77, 1), (81, 1), (79, 1), (74, 1)])
    melodi(p, 2, mel, lambda f, d, v: pulse(f, d, v, 0.5, 0.01, 5000), 0, 0.0, 1.0, -12)
    melodi(p, 2, mel, lambda f, d, v: pulse(f, d, v, 0.5, 0.01, 5000), 8, 0.0, 1.0, -12)
    for o in range(16):
        for s in range(8):
            p.koy(2, hat(0.25, s == 7), o * 4 + s * 0.5 + 0.25, 0.5)
    return p


@aday('muzik', 'c', 'Çizgi film galopu (168 BPM, Fa majör)', 'Tuba "um-pa", pizzicato akorlar, koşturan ksilofon ezgisi. En klasik çizgi film (eski kovalamaca sahnesi).')
def _():
    p = Parca(168, 16)
    prog = ['F', 'F', 'C7', 'C7', 'C7', 'C7', 'F', 'F', 'Bb', 'Bb', 'F', 'F', 'C7', 'C7', 'F', 'F']
    for o, a in enumerate(prog):
        r, ton = akor(a)
        b = o * 4
        p.koy(0, tuba(mf(r + 12), 0.8 * p.vurus, 1.0), b)
        p.koy(0, tuba(mf(r + 7 if r + 7 <= 52 else r - 5) * 2, 0.8 * p.vurus, 0.9), b + 2)
        p.koy(0, kick(0.8), b)
        p.koy(0, kick(0.6), b + 2)
        for s in (1, 3):
            p.koy(0, snare(0.45), b + s)
            p.koy(0, tahta(0.35, 1600), b + s, 0.4)
        for s in (1, 3):
            p.koy(1, sum(pizz(mf(m + 12), 0.2) for m in ton) / 2, b + s, -0.4)
            p.koy(1, sum(pizz(mf(m + 12), 0.2) for m in ton) / 3, b + s + 0.5, -0.4)
        for s in range(8):
            p.koy(1, hat(0.22), b + s * 0.5, 0.5)
    mel = m_bar([(72, .5), (77, .5), (81, .5), (84, .5), (81, .5), (77, .5), (81, 1)], [(84, .5), (86, .5), (84, .5), (81, .5), (77, 1), (72, 1)],
                [(79, .5), (82, .5), (84, .5), (82, .5), (79, .5), (76, .5), (72, 1)], [(76, .5), (79, .5), (82, 1), (81, .5), (79, .5), (76, 1)],
                [(72, .5), (76, .5), (79, .5), (82, .5), (84, 1), (82, 1)], [(81, .5), (79, .5), (76, .5), (74, .5), (72, 2)],
                [(77, .5), (81, .5), (84, .5), (89, .5), (88, .5), (86, .5), (84, 1)], [(81, 1), (77, 1), (72, 1), (-1, 1)],
                [(82, .5), (86, .5), (89, 1), (86, .5), (82, .5), (77, 1)], [(74, .5), (77, .5), (82, .5), (86, .5), (84, 1), (82, 1)],
                [(81, .5), (84, .5), (89, 1), (84, .5), (81, .5), (77, 1)], [(72, .5), (77, .5), (81, .5), (84, .5), (81, 2)],
                [(79, .5), (82, .5), (84, .5), (88, .5), (91, 1), (88, 1)], [(84, .5), (82, .5), (79, .5), (76, .5), (72, 1), (76, 1)],
                [(77, .5), (81, .5), (84, .5), (81, .5), (77, .5), (72, .5), (77, 1)], [(89, 1), (84, 1), (77, 1), (-1, 1)])
    melodi(p, 2, mel, ksilofon, 0, 0.15, 1.0)
    melodi(p, 2, mel, ksilofon, 0, -0.3, 0.3, 12)
    return p


@aday('muzik', 'd', 'Uzay ska (136 BPM, Si♭ majör)', 'Ara vuruşta org "çak"ları, yürüyen bas, bakır üflemeli ezgi. Daha "havalı", en az acele eden.')
def _():
    p = Parca(136, 16)
    prog = ['Bb', 'Gm', 'Cm', 'F'] * 4
    for o, a in enumerate(prog):
        r, ton = akor(a)
        b = o * 4
        p.koy(0, kick(1.0), b)
        p.koy(0, kick(0.8), b + 2)
        p.koy(0, snare(0.8), b + 1)
        p.koy(0, snare(0.8), b + 3)
        for s in range(4):
            p.koy(0, hat(0.4), b + s + 0.5, 0.2)
        yur = [0, 4 if 'm' not in a else 3, 7, 9 if 'm' not in a else 10]
        for s in range(4):
            p.koy(0, bas_saw(mf(r + 12 + yur[s]), 0.85 * p.vurus, 0.9, 600), b + s)
        for s in range(4):
            p.koy(1, org([m + 12 for m in ton], 0.3 * p.vurus, 0.9), b + s + 0.5, 0.35)
        p.koy(1, hat(0.3, True), b + 3.5, -0.5)
    mel = m_bar([(77, 1), (74, .5), (77, .5), (82, 1.5), (81, .5)], [(79, 1), (74, 1), (70, 1), (74, 1)],
                [(75, .5), (79, .5), (84, 1), (82, .5), (79, .5), (75, 1)], [(77, 1.5), (81, .5), (84, 1), (72, 1)],
                [(82, .5), (81, .5), (82, .5), (86, .5), (89, 2)], [(86, 1), (82, .5), (79, .5), (74, 2)],
                [(84, .5), (82, .5), (79, .5), (75, .5), (79, 1), (84, 1)], [(81, 1), (77, 1), (72, 1), (-1, 1)])
    melodi(p, 2, mel, bakir_lead, 0, 0.0, 1.0, -12)
    melodi(p, 2, mel, bakir_lead, 8, 0.0, 1.0, -12)
    melodi(p, 2, mel, bakir_lead, 8, -0.2, 0.5, -24)
    return p


# ================================================================ cikti
def oranla(x, kat):
    """Kategori hedefine kazanc; tavani asarsa tavanla sinirla. (kazanc, eksik_db) dondurur."""
    K = KATEGORI[kat]
    olc = lufs_tepe(x) if K['olcu'] == 'tepe' else lufs_i(x)
    g = 10 ** ((K['hedef'] - olc) / 20)
    tp = gercek_tepe_db(x * g)
    eksik = 0.0
    if tp > TAVAN:
        eksik = tp - TAVAN
        g *= 10 ** (-eksik / 20)
    return g, eksik


def mp3(wav, cikti, stereo=False, q=None):
    # VBR: efektler -V5 (~ 100-130 kb/s mono), muzik -V6
    q = q if q is not None else (6 if stereo else 5)
    subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-y', '-i', wav, '-codec:a', 'libmp3lame', '-q:a', str(q), cikti], check=True)


def dongu_dosyasi(y):
    """y (c, N) -> pay + y + pay; dongu noktalari pay ve pay+N."""
    y = np.atleast_2d(y)
    p = n_(DONGU_PAY)
    return np.concatenate([y[:, -p:], y, y[:, :p]], axis=1)


def main():
    os.makedirs(ADAY, exist_ok=True)
    os.makedirs(ARA, exist_ok=True)
    kayit = []
    for a in ADAYLAR:
        kat, kod = a['kat'], a['kod']
        L.tohum(sum(map(ord, kat + kod)) * 7919)
        ad = f'{kat}_{kod}'
        print('uretiliyor', ad, flush=True)
        x = a['fn']()
        bilgi = dict(id=ad, kat=kat, kod=kod, ad=a['ad'], aciklama=a['aciklama'], kaynak=a['kaynak'])
        if kat == 'muzik':
            katman = x.bitir()
            tum = sum(katman)
            g, eksik = oranla(tum, kat)
            bilgi.update(kazanc_db=20 * np.log10(g), eksik_db=eksik, dongu=[DONGU_PAY, DONGU_PAY + x.L], bpm=x.bpm, sure=x.L, dosyalar=[])
            for k, y in enumerate(katman):
                yy = dongu_dosyasi(y * g)
                w = os.path.join(ARA, f'{ad}_k{k + 1}.wav')
                sf.write(w, yy.T, SR, subtype='FLOAT')
                mp3(w, os.path.join(ADAY, f'{ad}_k{k + 1}.mp3'), stereo=True)
                bilgi['dosyalar'].append(f'{ad}_k{k + 1}.mp3')
            w = os.path.join(ARA, f'{ad}_tum.wav')   # olcum icin tum karisim (dongu govdesi, paysiz)
            sf.write(w, (tum * g).T, SR, subtype='FLOAT')
        elif kat == 'motor_ucus':
            x = x - np.mean(x)
            g, eksik = oranla(x, kat)
            x = x * g
            yy = dongu_dosyasi(x)[0]
            w = os.path.join(ARA, f'{ad}.wav')
            sf.write(w, yy, SR, subtype='FLOAT')
            mp3(w, os.path.join(ADAY, f'{ad}.mp3'))
            d = motor_demo(x)
            dt = gercek_tepe_db(d)
            if dt > TAVAN:
                d *= 10 ** ((TAVAN - dt) / 20)
            wd = os.path.join(ARA, f'{ad}_demo.wav')
            sf.write(wd, d, SR, subtype='FLOAT')
            mp3(wd, os.path.join(ADAY, f'{ad}_demo.mp3'))
            bilgi.update(kazanc_db=20 * np.log10(g), eksik_db=eksik, dongu=[DONGU_PAY, DONGU_PAY + DL], sure=DL,
                         dosyalar=[f'{ad}.mp3'], demo=f'{ad}_demo.mp3')
        else:
            x = fade(x - np.mean(x), 0.0, 0.008)
            g, eksik = oranla(x, kat)
            x = x * g
            w = os.path.join(ARA, f'{ad}.wav')
            sf.write(w, x, SR, subtype='FLOAT')
            mp3(w, os.path.join(ADAY, f'{ad}.mp3'))
            bilgi.update(kazanc_db=20 * np.log10(g), eksik_db=eksik, sure=len(x) / SR, dosyalar=[f'{ad}.mp3'])
        kayit.append(bilgi)
    with open(os.path.join(ARA, 'uretim.json'), 'w') as f:
        json.dump(dict(kategori={k: {kk: vv for kk, vv in v.items()} for k, v in KATEGORI.items()}, adaylar=kayit), f, ensure_ascii=False, indent=1)
    print('tamam', len(kayit), 'aday')


if __name__ == '__main__':
    main()
