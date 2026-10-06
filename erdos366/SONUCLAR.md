# Erdős #366 arama sonuçları

Her satır: X sınırına kadar tüm 3-dolu m için m-1 ve m+1'in güçlü olup olmadığı test edildi (`sieve`, 4 çekirdek).

| X | 3-dolu sayı | süre | #366 yönü (n 2-dolu, n+1 3-dolu) | ters yön | ardışık iki 3-dolu |
|---|---|---|---|---|---|
| 10^22 | 98 566 055 | 12 s | yok | (8,9), (12167,12168) | yok |
| 10^24 | 460 160 083 | 64 s | yok | (8,9), (12167,12168) | yok |
| 10^26 | 2 144 335 391 | 432 s | yok | (8,9), (12167,12168) | yok |

Doğrulama: `python3 verify.py out_*.txt` (sympy ile tam çarpanlara ayırma).
10^22 sonucu OEIS A060355 b-dosyasıyla (Donovan Johnson, terimler < 10^22) tutarlı.
Elek yolu ile deneme bölmesi yolu 10^12, 10^18 ve 10^20'de tüm ara sayaçlarda birebir aynı.

## Sezgisel hesap: neden aramaya devam etmiyoruz
X'e kadar ~4,66·X^(1/3) tane 3-dolu sayı var. x civarında bir sayının güçlü olma olasılığı ~(ζ(3/2)/ζ(3))/(2√x) ≈ 1,09/√x.
Bunlar çarpılıp toplanınca Y'den büyük çözümlerin beklenen sayısı ≈ 10·Y^(-1/6) çıkıyor:
10^22'nin ötesinde ≈ 0,002, 10^26'nın ötesinde ≈ 0,0005. Büyük arama neredeyse kesin boşa çıkar, bu yüzden 10^26'da durduk.
