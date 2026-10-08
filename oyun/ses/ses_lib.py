"""Son Durak: Pluton ses araclari: sentez yardimcilari + olcum (K-agirlikli ses siddeti vb.).

uret.py (aday uretimi) ve olc.py (olcum/eleme) bu modulu kullanir.
"""
import os
import subprocess

import numpy as np
from scipy import signal

SR = 44100
KOK = os.path.dirname(os.path.abspath(__file__))
R = np.random.default_rng(20261008)


def tohum(s):
    global R
    R = np.random.default_rng(s)


# ---------------------------------------------------------------- temel
def n_(d):
    return int(round(d * SR))


def t_(d):
    return np.arange(n_(d)) / SR


def arr(v, n):
    v = np.asarray(v, float)
    return np.full(n, float(v)) if v.ndim == 0 else v[:n]


def expc(a, b, n):
    return a * (b / a) ** np.linspace(0, 1, n)


def osc(f, n, kind='sine', duty=0.5, ph0=0.0):
    """Frekans dizisi (Hz) ile osilator. Kare/testere 4x asiri ornekleme ile (katlanma azaltilir)."""
    f = arr(f, n)
    if kind == 'sine':
        return np.sin(2 * np.pi * (np.cumsum(f) / SR + ph0)) * (f < SR * 0.45)
    if kind == 'tri':
        fr = (np.cumsum(f) / SR + ph0) % 1.0
        return 2 * np.abs(2 * fr - 1) - 1
    O = 4
    fr = (np.cumsum(np.repeat(f, O)) / (SR * O) + ph0) % 1.0
    x = 2 * fr - 1 if kind == 'saw' else np.where(fr < duty, 1.0, -1.0) - (2 * duty - 1)   # kare: DC payi cikarilir
    return signal.resample_poly(x, 1, O)[:n]


def white(n):
    return R.standard_normal(n)


def _renkli(n, us):
    X = np.fft.rfft(R.standard_normal(n))
    f = np.arange(len(X), dtype=float)
    f[0] = 1
    X /= f ** us
    x = np.fft.irfft(X, n)
    return x / (np.std(x) + 1e-12)


def pink(n):
    """Pembe gurultu (FFT ile sekillenir, n ornekte kendi kendine dongulu)."""
    return _renkli(n, 0.5)


def brown(n):
    return _renkli(n, 1.0)


def lp(x, f, o=2):
    return signal.sosfilt(signal.butter(o, min(f, SR * 0.45), 'low', fs=SR, output='sos'), x)


def hp(x, f, o=2):
    return signal.sosfilt(signal.butter(o, f, 'high', fs=SR, output='sos'), x)


def bp(x, f1, f2, o=2):
    return signal.sosfilt(signal.butter(o, [f1, min(f2, SR * 0.45)], 'band', fs=SR, output='sos'), x)


def sweep(x, f, q=0.7, kind='lp', blk=64):
    """Zamanla degisen RBJ biquad (lp/hp/bp), blok blok."""
    n = len(x)
    f = arr(f, n)
    y = np.zeros(n)
    zi = np.zeros(2)
    for i in range(0, n, blk):
        fc = min(max(f[min(i + blk // 2, n - 1)], 10.0), SR * 0.45)
        w = 2 * np.pi * fc / SR
        al = np.sin(w) / (2 * q)
        c = np.cos(w)
        if kind == 'lp':
            b = [(1 - c) / 2, 1 - c, (1 - c) / 2]
        elif kind == 'hp':
            b = [(1 + c) / 2, -(1 + c), (1 + c) / 2]
        else:
            b = [al, 0, -al]
        a = [1 + al, -2 * c, 1 - al]
        y[i:i + blk], zi = signal.lfilter(np.array(b) / a[0], np.array(a) / a[0], x[i:i + blk], zi=zi)
    return y


def dongu_filtre(x, kazanc_fn):
    """Dairesel (sifir faz) frekans alani suzgeci: dongu bozulmaz."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X * kazanc_fn(f), len(x))


def bw_lp(fc, o=2):
    return lambda f: 1 / np.sqrt(1 + (f / fc) ** (2 * o))


def bw_hp(fc, o=2):
    return lambda f: 1 / np.sqrt(1 + (fc / np.maximum(f, 1e-3)) ** (2 * o))


def env_exp(n, tau, att=0.002):
    t = np.arange(n) / SR
    e = np.exp(-t / tau)
    a = n_(att)
    if a > 1:
        e[:a] *= np.linspace(0, 1, a)
    return e


def env_adsr(n, a, d, s, r):
    e = np.zeros(n)
    ia, idd, ir = n_(a), n_(d), n_(r)
    ia = max(ia, 1)
    e[:ia] = np.linspace(0, 1, ia)[:n]
    j = min(ia + idd, n)
    if j > ia:
        e[ia:j] = np.linspace(1, s, idd)[:j - ia]
    e[j:] = s
    if ir > 0:
        k = max(n - ir, 0)
        e[k:] *= np.linspace(1, 0, n - k)
    return e


def fade(x, fi=0.0, fo=0.005):
    x = x.copy()
    a, b = n_(fi), n_(fo)
    if a > 1:
        x[:a] *= np.linspace(0, 1, a)
    if b > 1:
        x[-b:] *= np.linspace(1, 0, b)
    return x


def sat(x, d=2.0):
    return np.tanh(d * x) / np.tanh(d)


def verb(x, dur=0.8, mix=0.2, lpf=5000, seed=1):
    """Basit yanki: ustel sonumlu suzulmus gurultu durtu yaniti."""
    rr = np.random.default_rng(seed)
    m = n_(dur)
    ir = rr.standard_normal(m) * np.exp(-6.9 * np.arange(m) / m)
    ir = lp(ir, lpf)
    ir /= np.sqrt(np.sum(ir ** 2)) + 1e-12
    wet = signal.fftconvolve(x, ir)
    out = np.zeros(len(wet))
    out[:len(x)] += x
    return out + mix * wet * (np.sqrt(np.mean(x ** 2)) / (np.sqrt(np.mean(wet[:len(x)] ** 2)) + 1e-12))


def karis(*items):
    """(x, t0_saniye, kazanc) parcalarini toplar."""
    L = max(n_(t) + len(x) for x, t, g in items)
    y = np.zeros(L)
    for x, t, g in items:
        i = n_(t)
        y[i:i + len(x)] += g * x
    return y


def hiz(x, r):
    """Yeniden ornekleyerek perde/sure degisimi (r>1 tiz ve kisa)."""
    idx = np.arange(0, len(x) - 1, r)
    return np.interp(idx, np.arange(len(x)), x)


def kirp_sessiz(x, esik_db=-50):
    e = np.abs(x)
    m = e.max() + 1e-12
    i = np.argmax(e > m * 10 ** (esik_db / 20))
    return x[i:]


def normal(x):
    return x / (np.max(np.abs(x)) + 1e-12)


def kenney(rel):
    """Kenney CC0 dosyasini (oyun/ses/kaynak/kenney/...) ffmpeg ile cozer. Dosya guvenilmez sayilir: yalniz ham ornek okunur."""
    p = os.path.join(KOK, 'kaynak', 'kenney', rel)
    out = subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-i', p, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(out, np.float32).astype(float)
    return fade(x, 0, min(0.03, 0.2 * len(x) / SR))   # bazi Kenney dosyalari kesik bitiyor


def coz(yol, kanal=None):
    """Herhangi bir ses dosyasini float diziye cozer: (kanal, n)."""
    arg = ['ffmpeg', '-v', 'error', '-nostdin', '-i', yol, '-f', 'f32le', '-ar', str(SR)]
    if kanal:
        arg += ['-ac', str(kanal)]
    pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=channels', '-of', 'csv=p=0', yol],
                        capture_output=True, text=True, check=True)
    ch = kanal or int(pr.stdout.strip().split(',')[0])
    out = subprocess.run(arg + ['-'], capture_output=True, check=True).stdout
    x = np.frombuffer(out, np.float32).astype(float)
    return x.reshape(-1, ch).T


# ---------------------------------------------------------------- olcum (ITU-R BS.1770 K-agirligi, pyloudnorm katsayi yontemi)
def _k_sos():
    fs = SR
    G, Q, fc = 3.999843853973347, 0.7071752369554196, 1681.974450955533
    A = 10 ** (G / 40)
    w0 = 2 * np.pi * fc / fs
    al = np.sin(w0) / (2 * Q)
    c = np.cos(w0)
    sa = np.sqrt(A)
    b = [A * ((A + 1) + (A - 1) * c + 2 * sa * al), -2 * A * ((A - 1) + (A + 1) * c), A * ((A + 1) + (A - 1) * c - 2 * sa * al)]
    a = [(A + 1) - (A - 1) * c + 2 * sa * al, 2 * ((A - 1) - (A + 1) * c), (A + 1) - (A - 1) * c - 2 * sa * al]
    s1 = np.r_[np.array(b) / a[0], np.array(a) / a[0]]
    Q2, fc2 = 0.5003270373238773, 38.13547087602444
    w0 = 2 * np.pi * fc2 / fs
    al = np.sin(w0) / (2 * Q2)
    c = np.cos(w0)
    a = [1 + al, -2 * c, 1 - al]
    s2 = np.r_[np.array([1, -2, 1]) / a[0], np.array(a) / a[0]]
    return np.vstack([s1, s2])


KSOS = _k_sos()


def _kms(xc, win, hop):
    """Kanal dizisi (c,n) -> pencere ortalama karelerinin kanal toplami."""
    xc = np.atleast_2d(xc)
    w, h = n_(win), n_(hop)
    ms = []
    for ch in xc:
        y = signal.sosfilt(KSOS, ch)
        if len(y) < w:
            y = np.r_[y, np.zeros(w - len(y))]
        c2 = np.r_[0, np.cumsum(y ** 2)]
        st = np.arange(0, len(y) - w + 1, h)
        ms.append((c2[st + w] - c2[st]) / w)
    return np.sum(ms, axis=0)


def lufs_tepe(x, win=0.1):
    """En yuksek kisa pencere (varsayilan 100 ms) K-agirlikli ses siddeti; tek atimlik sesler icin."""
    ms = _kms(x, win, 0.01)
    return -0.691 + 10 * np.log10(ms.max() + 1e-12)


def lufs_m(x):
    """En yuksek anlik (400 ms) ses siddeti."""
    ms = _kms(x, 0.4, 0.1)
    return -0.691 + 10 * np.log10(ms.max() + 1e-12)


def lufs_i(x):
    """Butunlesik (kapili) ses siddeti."""
    ms = _kms(x, 0.4, 0.1)
    l = -0.691 + 10 * np.log10(ms + 1e-12)
    g = ms[l > -70]
    if len(g) == 0:
        return -99.0
    rel = -0.691 + 10 * np.log10(g.mean()) - 10
    g2 = ms[(l > -70) & (l > rel)]
    return -0.691 + 10 * np.log10(g2.mean() + 1e-12)


def tepe_db(x):
    return 20 * np.log10(np.max(np.abs(x)) + 1e-12)


def gercek_tepe_db(x):
    xc = np.atleast_2d(x)
    m = max(np.max(np.abs(signal.resample_poly(c, 4, 1))) for c in xc)
    return 20 * np.log10(m + 1e-12)


def telefon(x):
    """Kaba telefon hoparloru benzetimi: 500 Hz alti 12 dB/oktav duser, 10 kHz ustu kesilir."""
    return lp(hp(x, 500, 2), 10000, 2)
