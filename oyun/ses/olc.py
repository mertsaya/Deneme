#!/usr/bin/env python3
"""Ses adaylarini olcer, kusurlulari eler, OLCUM.md + spektrogramlar + secici verisi (adaylar/liste.js, adaylar/gomulu.js) uretir.

Olcum, oyunun kullanacagi dosya uzerinde yapilir: mp3 cozulur (kodlama kaynakli kirpilma/dongu hatasi da yakalanir).
Calistir: python3 oyun/ses/olc.py   (once uret.py)
"""
import base64
import json
import os
import sys

import numpy as np
import soundfile as sf
from scipy import signal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ses_lib import KOK, SR, coz, gercek_tepe_db, lufs_i, lufs_m, lufs_tepe, n_, telefon  # noqa: E402

import matplotlib  # noqa: E402
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

ADAY = os.path.join(KOK, 'adaylar')
ARA = os.path.join(KOK, '_ara')
SPEK = os.path.join(KOK, 'spektrogram')

# Eleme esikleri (gerekce OLCUM.md'de)
E_EKSIK = 3.0        # dB: hedef ses siddetine tavan yuzunden ulasamama
E_TEL = 10.0         # dB: telefon hoparloru benzetiminde ses siddeti kaybi
E_ATAK = 30.0        # ms: darbe seslerinde tepeye varis
E_TIZ = 0.35         # 6 kHz ustu enerji orani
E_DONGU = -25.0      # dB: dongu periyodiklik hatasi
E_SON = -40.0        # dB: son 10 ms seviyesi, tepeye gore (tik riski)
E_DIKIS = 6.0        # dB: dongu ekinde tiz gurultu patlamasi (tik)


def db(x):
    return 20 * np.log10(max(x, 1e-12))


def bantlar(x):
    f, P = signal.welch(x, SR, nperseg=4096 if len(x) >= 4096 else len(x))
    P = P / (P.sum() + 1e-20)
    sinir = [(0, 150), (150, 600), (600, 3000), (3000, 8000), (8000, SR / 2 + 1)]
    b = [float(P[(f >= a) & (f < c)].sum()) for a, c in sinir]
    merkez = float((f * P).sum())
    tiz6 = float(P[f >= 6000].sum())
    return b, merkez, tiz6


def aktif_sure(x):
    w = n_(0.01)
    e = np.sqrt(np.convolve(x ** 2, np.ones(w) / w, 'same'))
    m = e.max()
    idx = np.nonzero(e > m * 10 ** (-45 / 20))[0]
    return (idx[-1] - idx[0]) / SR if len(idx) else 0.0


def olc_tek(x, kat, K):
    """x: (c, n) cozulmus dosya."""
    mono = x.mean(axis=0)
    m = {}
    m['dosya_s'] = x.shape[1] / SR
    m['aktif_s'] = aktif_sure(mono)
    m['tepe_dbfs'] = db(np.max(np.abs(x)))
    m['gercek_tepe_dbtp'] = gercek_tepe_db(x)
    act = mono[np.abs(mono) > 0] if np.any(mono) else mono
    w = n_(0.01)
    e = np.sqrt(np.convolve(mono ** 2, np.ones(w) / w, 'same'))
    on = e > e.max() * 10 ** (-30 / 20)
    m['rms_dbfs'] = db(np.sqrt(np.mean(mono[on] ** 2))) if on.any() else -99
    m['tepe_rms_db'] = m['tepe_dbfs'] - m['rms_dbfs']
    olcf = lufs_tepe if K['olcu'] == 'tepe' else lufs_i
    m['lufs'] = olcf(x)
    m['lufs_m'] = lufs_m(x)
    tel = np.vstack([telefon(c) for c in x])
    m['telefon_kaybi_db'] = m['lufs'] - olcf(tel)
    m['kirpilma'] = int(np.sum(np.abs(x) >= 0.999))
    m['dc'] = float(np.mean(mono))
    b, mer, tiz6 = bantlar(mono)
    m['bant'] = b
    m['merkez_hz'] = mer
    m['tiz6k'] = tiz6
    pk = np.max(np.abs(mono))
    i_ilk = np.argmax(np.abs(mono) > pk * 10 ** (-40 / 20))
    i_tepe = np.argmax(np.abs(mono) > pk * 10 ** (-6 / 20))
    m['atak_ms'] = (i_tepe - i_ilk) / SR * 1000
    m['bas_gecikme_ms'] = i_ilk / SR * 1000
    m['son_dbfs'] = db(np.sqrt(np.mean(mono[-n_(0.002):] ** 2)))
    del act
    return m


def dongu_hatasi(x, Ls):
    """Periyodiklik: x[n] ile x[n+L] farki (dB). Kayipsiz ara wav'da olculur (mp3 dalga bicimini korumaz)."""
    Lp = n_(Ls)
    a = x[:, :x.shape[1] - Lp]
    b = x[:, Lp:]
    return db(np.sqrt(np.mean((a - b) ** 2))) - db(np.sqrt(np.mean(a ** 2)))


def dikis_tiki(x, p0, p1):
    """Tarayicidaki gibi dongu govdesi (p0..p1) iki kez arka arkaya calinir; ekteki 4 ms'lik 5 kHz ustu enerji,
    govdenin geri kalanindaki 4 ms pencerelerin %99'luk degerine gore kac dB fazla (tik varsa buyuk)."""
    from ses_lib import hp
    g = x[:, p0:p1].mean(axis=0)
    y = hp(np.r_[g, g], 5000, 4)
    w = n_(0.004)
    e = np.convolve(y ** 2, np.ones(w) / w, 'same')
    j = len(g)
    ek = e[j - w:j + w].max()
    ic = np.r_[e[n_(0.05):j - n_(0.05)], e[j + n_(0.05):-n_(0.05)]]
    return 10 * np.log10((ek + 1e-20) / (np.percentile(ic, 99) + 1e-20))


def main():
    os.makedirs(SPEK, exist_ok=True)
    U = json.load(open(os.path.join(ARA, 'uretim.json')))
    KAT = U['kategori']
    sonuc = []
    sinyal = {}
    for a in U['adaylar']:
        kat = a['kat']
        K = KAT[kat]
        r = dict(a)
        neden = []
        if kat == 'muzik':
            st = [coz(os.path.join(ADAY, f), 2) for f in a['dosyalar']]
            n = min(s.shape[1] for s in st)
            tum = sum(s[:, :n] for s in st)
            p0, p1 = n_(a['dongu'][0]), n_(a['dongu'][1])
            m = olc_tek(tum[:, p0:p1], kat, K)
            m['katman_lufs'] = [lufs_i(s[:, p0:p1]) for s in st]
            m['dongu_hatasi_db'] = max(dongu_hatasi(np.atleast_2d(sf.read(os.path.join(ARA, f.replace('.mp3', '.wav')))[0].T), a['sure']) for f in a['dosyalar'])
            m['dikis_db'] = max(dikis_tiki(s, p0, p1) for s in st)
            m['kirpilma'] = int(np.sum(np.abs(tum) >= 0.999))
            sinyal[a['id']] = tum[:, p0:p0 + n_(10)].mean(axis=0)
        elif kat == 'motor_ucus':
            x = coz(os.path.join(ADAY, a['dosyalar'][0]))
            p0, p1 = n_(a['dongu'][0]), n_(a['dongu'][1])
            m = olc_tek(x[:, p0:p1], kat, K)
            m['dongu_hatasi_db'] = dongu_hatasi(np.atleast_2d(sf.read(os.path.join(ARA, a['dosyalar'][0].replace('.mp3', '.wav')))[0]), a['sure'])
            m['dikis_db'] = dikis_tiki(x, p0, p1)
            d = coz(os.path.join(ADAY, a['demo']))
            m['demo_lufs'] = lufs_i(d)
            m['demo_kirpilma'] = int(np.sum(np.abs(d) >= 0.999))
            sinyal[a['id']] = d.mean(axis=0)
        else:
            x = coz(os.path.join(ADAY, a['dosyalar'][0]))
            m = olc_tek(x, kat, K)
            sinyal[a['id']] = x.mean(axis=0)
        # ---- eleme
        if m['kirpilma'] > 0 or m.get('demo_kirpilma', 0) > 0:
            neden.append(f"kırpılma ({m['kirpilma']} örnek)")
        if a['eksik_db'] > E_EKSIK:
            neden.append(f"çok sivri: hedef yüksekliğe {a['eksik_db']:.1f} dB eksik kalıyor (tepe/RMS {m['tepe_rms_db']:.0f} dB)")
        if m['telefon_kaybi_db'] > E_TEL:
            neden.append(f"telefonda kaybolur: hoparlör benzetiminde {m['telefon_kaybi_db']:.1f} dB düşüş")
        if K.get('darbe') and m['atak_ms'] > E_ATAK:
            neden.append(f"geç vuruş: tepeye {m['atak_ms']:.0f} ms")
        if K.get('sure') and not (K['sure'][0] <= m['aktif_s'] <= K['sure'][1]):
            neden.append(f"süre uygun değil: {m['aktif_s']:.2f} s (beklenen {K['sure'][0]}–{K['sure'][1]} s)")
        if m['tiz6k'] > E_TIZ:
            neden.append(f"sert/tiz: enerjinin %{100 * m['tiz6k']:.0f}'i 6 kHz üstünde")
        if 'dongu_hatasi_db' in m and m['dongu_hatasi_db'] > E_DONGU:
            neden.append(f"döngü periyodik değil: {m['dongu_hatasi_db']:.0f} dB")
        if 'dikis_db' in m and m['dikis_db'] > E_DIKIS:
            neden.append(f"döngü ekinde tık: {m['dikis_db']:.1f} dB")
        if abs(m['dc']) > 0.01:
            neden.append('DC kayması')
        if not K.get('dongu') and m['son_dbfs'] - m['tepe_dbfs'] > E_SON:
            neden.append(f"sonu kesik (tık riski): son 2 ms tepeye göre {m['son_dbfs'] - m['tepe_dbfs']:.0f} dB")
        # ---- puan (yalniz gecenler icin anlamli; olcum temelli, zevk degil)
        puan = 100.0
        puan -= 6 * max(0, m['telefon_kaybi_db'] - 4)
        puan -= 10 * a['eksik_db']
        puan -= 80 * max(0, m['tiz6k'] - 0.15)
        puan -= 2 * abs(m['lufs'] - K['hedef'])
        if K.get('sure'):
            orta = (K['sure'][0] + K['sure'][1]) / 2
            puan -= 10 * abs(m['aktif_s'] - orta) / (K['sure'][1] - K['sure'][0])
        r.update(olcum=m, elendi=bool(neden), neden=neden, puan=round(puan, 1))
        sonuc.append(r)
    # ---- oneri: kategori basina gecenler arasinda en yuksek puan
    for kat in KAT:
        gec = sorted([s for s in sonuc if s['kat'] == kat and not s['elendi']], key=lambda s: -s['puan'])
        for i, s in enumerate(gec):
            s['sira'] = i + 1
        if gec:
            gec[0]['oneri'] = True
    json.dump(dict(kategori=KAT, adaylar=sonuc), open(os.path.join(ARA, 'olcum.json'), 'w'), ensure_ascii=False, indent=1)
    spektrogram(KAT, sonuc, sinyal)
    rapor(KAT, sonuc)
    secici_verisi(KAT, sonuc)
    el = [s['id'] for s in sonuc if s['elendi']]
    print('aday', len(sonuc), 'elenen', len(el), el)


def spektrogram(KAT, sonuc, sinyal):
    for kat in KAT:
        ss = [s for s in sonuc if s['kat'] == kat]
        if not ss:
            continue
        fig, ax = plt.subplots(len(ss), 1, figsize=(9, 2.1 * len(ss)), squeeze=False)
        for i, s in enumerate(ss):
            x = sinyal[s['id']]
            f, t, S = signal.spectrogram(x, SR, nperseg=1024, noverlap=768)
            Sd = 10 * np.log10(S + 1e-12)
            a = ax[i, 0]
            a.pcolormesh(t, f, Sd, vmin=Sd.max() - 80, vmax=Sd.max(), shading='auto', cmap='magma')
            a.set_yscale('symlog', linthresh=200)
            a.set_ylim(30, 16000)
            renk = '#c0392b' if s['elendi'] else ('#1e8449' if s.get('oneri') else 'black')
            et = ' [ELENDİ]' if s['elendi'] else (' [ÖNERİ]' if s.get('oneri') else '')
            m = s['olcum']
            a.set_title(f"{s['id']} — {s['ad']}{et}  | {m['lufs']:.1f} LUFS, tel. kaybı {m['telefon_kaybi_db']:.1f} dB", fontsize=8, color=renk, loc='left')
            a.tick_params(labelsize=7)
            a.axhline(500, color='cyan', lw=0.5, ls='--')
        ax[-1, 0].set_xlabel('s')
        fig.tight_layout()
        fig.savefig(os.path.join(SPEK, f'{kat}.png'), dpi=80)
        plt.close(fig)


def rapor(KAT, sonuc):
    L = ['# Ses adayları: ölçüm ve eleme', '',
         '`python3 oyun/ses/olc.py` üretir (elle düzenleme). Ölçüm, oyunun kullanacağı **mp3 dosyası çözülerek** yapılır.', '',
         '## Ölçüler', '',
         '- **LUFS**: ITU-R BS.1770 K-ağırlıklı ses şiddeti. Tek atımlık seslerde en yüksek 100 ms pencere (kısa seslerin algısına daha yakın), döngülerde bütünleşik (kapılı).',
         '- **Hedef**: kategori başına ses şiddeti hedefi (uret.py `KATEGORI`). Adaylar hedefe getirildi; tepe −1,5 dBTP tavanına çarparsa kalan fark **eksik** olarak yazılır.',
         '- **Tel. kaybı**: 500 Hz altını 12 dB/oktav kısan, 10 kHz üstünü kesen kaba telefon hoparlörü benzetiminde ses şiddeti düşüşü. Büyükse ses telefonda "kaybolur".',
         '- **Tepe/RMS**: sivrilik (dB). **Atak**: ilk sesten tepeye ms. **Bantlar**: enerji yüzdesi <150 / 150–600 / 600–3k / 3k–8k / >8k Hz. **Merkez**: spektral ağırlık merkezi.',
         '- **Döngü**: kayıpsız ara dosyada x[n] ile x[n+L] farkı (dB; −100 civarı = tam periyodik). **Dikiş**: mp3 çözülüp döngü gövdesi tarayıcıdaki gibi arka arkaya çalınınca ekteki 5 kHz üstü enerji, gövdenin geri kalanının %99 değerine göre kaç dB fazla (tık varsa büyür).', '',
         '## Eleme kuralları', '',
         f'1. Kırpılma (|x| ≥ 0,999) olmamalı.',
         f'2. Hedef ses şiddetine tavan yüzünden {E_EKSIK:.0f} dB\'den fazla eksik kalmamalı (çok sivri ses diğerlerinin yanında cılız kalır).',
         f'3. Telefon kaybı ≤ {E_TEL:.0f} dB (oyun telefonda oynanır).',
         f'4. Darbe seslerinde atak ≤ {E_ATAK:.0f} ms (vuruş ile görüntü eş zamanlı).',
         '5. Etkin süre kategori aralığında.',
         f'6. 6 kHz üstü enerji ≤ %{100 * E_TIZ:.0f} (sık çalan seste yorucu olmasın).',
         f'7. Döngü periyodiklik hatası ≤ {E_DONGU:.0f} dB ve dikiş ≤ {E_DIKIS:.0f} dB. 8. DC kayması yok (|ort.| ≤ 0,01). 9. Son 2 ms, tepeye göre ≤ {E_SON:.0f} dB (kesik son tık yapar).', '',
         '**Puan** (yalnız geçenler arasında sıralama için): 100 − 6·max(0, tel. kaybı − 4) − 10·eksik − 80·max(0, 6k üstü − 0,15) − 2·|LUFS − hedef| − süre sapması. '
         'Zevk ölçmez; telefonda net, dengeli ve hedef yükseklikte olanı öne alır. **Son karar kulakla verilir.**', '']
    for kat, K in KAT.items():
        ss = [s for s in sonuc if s['kat'] == kat]
        L += [f'## {K["ad"]} (`{kat}`)', '', f'Hedef {K["hedef"]} LUFS ({"100 ms tepe" if K["olcu"] == "tepe" else "bütünleşik"})' +
              (f', etkin süre {K["sure"][0]}–{K["sure"][1]} s' if K.get('sure') else '') + f'. Spektrogram: `spektrogram/{kat}.png`', '']
        L += ['| Aday | Kaynak | LUFS | Tepe dBTP | Tepe/RMS | Eksik | Tel. kaybı | Atak ms | Süre s | Bantlar % | Merkez Hz | ' +
              ('Döngü / dikiş dB | ' if K.get('dongu') else '') + 'Puan | Sonuç |',
              '|---|---|---|---|---|---|---|---|---|---|---|' + ('---|' if K.get('dongu') else '') + '---|---|']
        for s in ss:
            m = s['olcum']
            b = '/'.join(f'{100 * v:.0f}' for v in m['bant'])
            sonucs = ('ELENDİ: ' + '; '.join(s['neden'])) if s['elendi'] else (f"**ÖNERİ** (1.)" if s.get('oneri') else f"geçti ({s.get('sira')}.)")
            L.append(f"| {s['kod']}. {s['ad']} | {s['kaynak']} | {m['lufs']:.1f} | {m['gercek_tepe_dbtp']:.1f} | {m['tepe_rms_db']:.1f} | {s['eksik_db']:.1f} | "
                     f"{m['telefon_kaybi_db']:.1f} | {m['atak_ms']:.0f} | {m['aktif_s']:.2f} | {b} | {m['merkez_hz']:.0f} | " +
                     (f"{m['dongu_hatasi_db']:.0f} / {m['dikis_db']:.1f} | " if K.get('dongu') else '') + f"{s['puan']:.0f} | {sonucs} |")
        if kat == 'muzik':
            L += ['', 'Katman ses şiddetleri (k1 temel / k2 orta / k3 ezgi, bütünleşik LUFS):', '']
            for s in ss:
                kl = ' / '.join(f'{v:.1f}' for v in s['olcum']['katman_lufs'])
                L.append(f"- {s['kod']}. {s['ad']}: {kl} · {s['bpm']} BPM · döngü {s['sure']:.1f} s")
        L.append('')
    open(os.path.join(KOK, 'OLCUM.md'), 'w').write('\n'.join(L))


def secici_verisi(KAT, sonuc):
    kats = [dict(id=k, ad=v['ad'], hedef=v['hedef'], dongu=bool(v.get('dongu'))) for k, v in KAT.items()]
    ad = []
    dosyalar = set()
    for s in sonuc:
        m = s['olcum']
        d = dict(id=s['id'], kat=s['kat'], kod=s['kod'], ad=s['ad'], aciklama=s['aciklama'], kaynak=s['kaynak'],
                 dosyalar=s['dosyalar'], elendi=s['elendi'], neden=s['neden'], oneri=bool(s.get('oneri')), sira=s.get('sira'),
                 puan=s['puan'], lufs=round(m['lufs'], 1), tel=round(m['telefon_kaybi_db'], 1), sure=round(m['aktif_s'], 2))
        if 'dongu' in s:
            d['dongu'] = s['dongu']
        if 'demo' in s:
            d['demo'] = s['demo']
            dosyalar.add(s['demo'])
        if 'bpm' in s:
            d['bpm'] = s['bpm']
        dosyalar.update(s['dosyalar'])
        ad.append(d)
    with open(os.path.join(ADAY, 'liste.js'), 'w') as f:
        f.write('// olc.py uretir. Elle duzenleme.\nwindow.SES_LISTE = ')
        json.dump(dict(kategori=kats, adaylar=ad), f, ensure_ascii=False)
        f.write(';\n')
    # file:// ile acildiginda fetch calismaz: mp3'ler base64 olarak da gomulur (yalniz file:// iken yuklenir)
    with open(os.path.join(ADAY, 'gomulu.js'), 'w') as f:
        f.write('// olc.py uretir: file:// icin mp3 verisi (base64).\nwindow.SES_GOMULU = {\n')
        for d in sorted(dosyalar):
            b = base64.b64encode(open(os.path.join(ADAY, d), 'rb').read()).decode()
            f.write(f'"{d}":"{b}",\n')
        f.write('};\n')


if __name__ == '__main__':
    main()
