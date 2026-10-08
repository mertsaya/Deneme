# -*- coding: utf-8 -*-
"""B0 yapılandırması: oyun/sim/ucus_sim.py'den JSON üretir (TASARIM §16).

Kullanım:
  python oyun/b0/araclar/ayar_uret.py            # oyun/b0/ayar.json ve index.html içindeki gömülü bloğu yazar
  python oyun/b0/araclar/ayar_uret.py --denetle  # yazmaz; fark varsa çıkış kodu 1
Sim'e yazmaz, yalnız içe aktarır (ana işlevi çalışmaz).
"""
import importlib.util, json, re, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]          # oyun/
SIM = KOK / 'sim' / 'ucus_sim.py'
B0 = KOK / 'b0'
CIKTI, SAYFA = B0 / 'ayar.json', B0 / 'index.html'

KARTLAR = ['rampa', 'bolge', 'verim', 'dalis', 'kademe_itki', 'yakit_ac', 'yakit_s']
TIPLER_B0 = ['balon', 'parti', 'zeplin', 'marti', 'ucurtma']   # parti yalnız eşlik testi (?tipler=)

# Sim kodunun içine gömülü sayılar (işlev adı yorumda). Sim bunları sabite taşırsa buradan silinip sim'den okunur.
SABIT_EK = {
    'ust_vy_oran': 0.35, 'marti_donus_derece': 2,                              # carp
    'acilis_zeplin': {'dx': 4, 'y_min': 65, 'r_kat': 0.5},                    # kalkis
    'rakip_kalite': {'mukemmel': 1.0, 'iyi': 0.4, 'zayif': 0.0},              # kalkis (rakip vuruşu = B0 kalkış primi)
    'cam_tau': 0.8, 'yonet_ara': 0.1,                                         # adim
    'yonet': {'on_ekran': 1, 'dikey_pay': 0.3, 'y_min': 25, 'deneme': 8},     # yonet
    'temizlik': {'arka_ekran': 1, 'dikey_ekran': 2.5, 'sonuk_sure': 0.5},     # yonet
    'ekran_az': 4,                                                            # adim (istatistik)
    'garanti_ara': 0.25, 'garanti_adim': 0.1,                                 # adim
    'rota_sure': 6.0, 'rota_adim': 0.1,                                       # rota
    'garanti_pay_kat': 0.6, 'garanti_y_min': 30, 'garanti_x0': 20, 'garanti_tr_y_min': 25,   # garanti
    'firsat': {'ilk': [0.3, 0.7], 'sonra': [0.7, 0.6], 'tau': [1.6, 1.0], 'y_sapma': 12, 'y_min': 30},   # firsat_yonet
    'yakit': {'tut_ek': 0.25, 'cift_sv': 4, 'ek_sv': 2, 'ek': 0.25},         # firsat_al
    'aday': [0.15, 80],                                                       # adim
    'bot_bolge_kat': 0.5,                                                     # rampa_karar (mükemmel olasılığına bölge/2)
    'hedef_dy_min': 5, 'hedef_r_kat': 0.5,                                    # dalis_hedef
    'bot_karar_ara': 0.05,                                                    # bot_karar
    'tohum_bot': [7919, 13], 'tohum_tur': 1000, 'tohum_alici': [31, 7],       # tur_oyna, kampanya
    'duvar_sonraki': 0.1,                                                     # kampanya (sonraki kırılış ödülü oranı)
    'alis_ufuk': [2.2, 60.0, 100.0],                                          # alisveris
}


def sim_yukle():
    sp = importlib.util.spec_from_file_location('ucus_sim', SIM)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def uret():
    m = sim_yukle()
    G = {k: list(m.GELISTIRME[k]) for k in KARTLAR}
    return {
        'kaynak': 'oyun/sim/ucus_sim.py (ayar_uret.py ile üretildi; elle düzenleme)',
        'AYAR': m.AYAR,
        'SONUM_ALT': m.SONUM_ALT,
        'DUVARLAR': {'ses': m.DUVARLAR['ses']},
        'TIPLER': {k: v for k, v in m.TIPLER.items() if k in TIPLER_B0},   # sim anahtar sırası korunur
        'FIRSATLAR': {'yakit': m.FIRSATLAR['yakit']},
        'GELISTIRME': G,
        'fiyatlar': {k: [m.fiyat(k, sv) for sv in range(G[k][0])] for k in KARTLAR},
        'BOTLAR': m.BOTLAR, 'BOT_SIRA': m.BOT_SIRA,
        'HIC_SIFIR': [k for k in m.HIC_SIFIR if k in KARTLAR],
        'IRTIFA_TABLO': m.IRTIFA_TABLO,
        'SABIT_EK': SABIT_EK,
    }


def metin(d):
    return json.dumps(d, ensure_ascii=False, sort_keys=False, separators=(',', ':'))


BLOK = re.compile(r'(<script type="application/json" id="ayar">)(.*?)(</script>)', re.S)


def main():
    denetle = '--denetle' in sys.argv
    yeni = metin(uret())
    fark = []
    eski_json = CIKTI.read_text(encoding='utf-8').strip() if CIKTI.exists() else ''
    if eski_json != yeni:
        fark.append(str(CIKTI))
    sayfa = SAYFA.read_text(encoding='utf-8') if SAYFA.exists() else None
    if sayfa is not None:
        mm = BLOK.search(sayfa)
        if not mm:
            print('index.html içinde <script type="application/json" id="ayar"> bloğu yok', file=sys.stderr)
            sys.exit(2)
        if mm.group(2).strip() != yeni:
            fark.append(str(SAYFA))
    if denetle:
        print('fark var: ' + ', '.join(fark) if fark else 'denetim tamam: yapılandırma sim ile aynı')
        sys.exit(1 if fark else 0)
    CIKTI.write_text(yeni + '\n', encoding='utf-8')
    if sayfa is not None:
        SAYFA.write_text(sayfa[:mm.start(2)] + yeni + sayfa[mm.end(2):], encoding='utf-8')
    print('yazıldı:', CIKTI, '(+ index.html gömülü blok)' if sayfa is not None else '', '| değişen:', ', '.join(fark) or 'yok')


if __name__ == '__main__':
    main()
