# "Son Durak: Plüton" ilerleme ve ekonomi simülasyonu (ilk taslak).
# Amaç: kaç uçuşta hangi bölüme varıldığını ve toplam oyun süresini kodlamadan önce görmek.
# Model bilinçli olarak basit: her bölüm belirli dallarda belirli kademeleri gerektirir;
# eksik geliştirmeyle girilen bölümde oyuncu bölüm içinde rastgele bir noktada ölür.
# Gereken her şey varsa geçiş olasılığı oyuncunun o bölümdeki deneme sayısıyla (öğrenme) artar.
import random, statistics

DALLAR = ["İtki", "Uzun yol", "Gövde", "Aviyonik", "Enerji", "Lojistik"]
BOLUMLER = ["Troposfer", "Üst atmosfer", "Yörünge", "Ay", "Mars yolu", "Asteroit kuşağı",
            "Jüpiter", "Satürn", "Uranüs–Neptün–Kuiper", "Plüton"]
# her bölümü geçmek için gereken en düşük kademeler
GEREK = [
    {"Gövde": 1},
    {"İtki": 1, "Lojistik": 1},
    {"Aviyonik": 1, "İtki": 2, "Gövde": 2},
    {"Aviyonik": 2, "İtki": 3, "Lojistik": 2, "Enerji": 1},
    {"Gövde": 3, "Uzun yol": 1, "Enerji": 2, "Lojistik": 3},
    {"Aviyonik": 3, "Uzun yol": 2, "Gövde": 4},
    {"Gövde": 5, "Enerji": 3, "Aviyonik": 4, "Uzun yol": 3},
    {"Aviyonik": 5, "İtki": 4, "Lojistik": 4},
    {"Enerji": 5, "Uzun yol": 4, "İtki": 5},
    {"Gövde": 6, "Aviyonik": 6, "İtki": 6, "Lojistik": 6},
]
SURE_DK = [0.75, 1.0, 1.5, 2.5, 3.0, 3.0, 3.5, 3.5, 4.0, 4.0]  # bölüm içinde geçen ortalama dakika
CHECKPOINT = {4: 3, 5: 4, 7: 6, 9: 8}  # bu bölüme ulaşınca bir sonraki uçuş şu bölümden başlar (üsler)

KAZANC_TABAN, KAZANC_CARPAN = 60, 1.45     # kredi = taban * çarpan^derinlik
MALIYET_TABAN, MALIYET_CARPAN = 220, 1.95  # kademe k fiyatı = taban * çarpan^(k-1)

def maliyet(dal, kademe):
    return MALIYET_TABAN * MALIYET_CARPAN ** (kademe - 1)

def tek_oyun(rng):
    seviye = {d: 0 for d in DALLAR}
    kredi, ucus, dakika = 0.0, 0, 0.0
    basla, en_derin = 0, 0
    deneme = [0] * len(BOLUMLER)
    ilk_varis = {0: 0}
    while en_derin < len(BOLUMLER) and ucus < 2000:
        ucus += 1
        d = basla
        while d < len(BOLUMLER):
            eksik = any(seviye[k] < v for k, v in GEREK[d].items())
            deneme[d] += 1
            p = 0.92 - 0.55 * 0.6 ** (deneme[d] - 1)
            if eksik or rng.random() > p:
                f = rng.random() * (0.6 if eksik else 1.0)
                dakika += SURE_DK[d] * f
                derinlik = d + f
                break
            dakika += SURE_DK[d]
            d += 1
            derinlik = d
            if d not in ilk_varis:
                ilk_varis[d] = ucus
        en_derin = max(en_derin, d)
        basla = max([basla] + [v for k, v in CHECKPOINT.items() if en_derin >= k])
        kredi += KAZANC_TABAN * KAZANC_CARPAN ** derinlik
        dakika += 0.4  # hangar ve yeniden kalkış
        # alışveriş: önce bir sonraki bölümün eksik gereksinimleri, en ucuzdan başlayarak
        while True:
            hedef = GEREK[min(en_derin, len(BOLUMLER) - 1)]
            adaylar = [(maliyet(k, seviye[k] + 1), k) for k, v in hedef.items() if seviye[k] < v]
            if not adaylar:
                break
            fiyat, dal = min(adaylar)
            if fiyat > kredi:
                break
            kredi -= fiyat
            seviye[dal] += 1
    return ilk_varis, ucus, dakika

def main(n=2000):
    rng = random.Random(366)
    sonuc = [tek_oyun(rng) for _ in range(n)]
    print(f"{'Bölüm':24s} {'uçuş (medyan)':>14s} {'aralık %10–90':>15s}")
    satirlar = []
    for b in range(1, len(BOLUMLER) + 1):
        xs = sorted(s[0][b] for s in sonuc if b in s[0])
        med = statistics.median(xs); lo = xs[len(xs) // 10]; hi = xs[len(xs) * 9 // 10]
        ad = "Plüton'a iniş" if b == len(BOLUMLER) else "Varış: " + BOLUMLER[b]
        print(f"{ad:24s} {med:14.0f} {lo:>7d}–{hi:<7d}")
        satirlar.append((ad, med, lo, hi))
    dk = statistics.median(s[2] for s in sonuc)
    print(f"Toplam oyun süresi (medyan): {dk/60:.1f} saat, {statistics.median(s[1] for s in sonuc):.0f} uçuş")
    return satirlar, dk

if __name__ == "__main__":
    main()
