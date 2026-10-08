# Uçuş + ekonomi simülasyonu: rapor (3. ayar: S1–S9 + E1–E2)

2026-10-08 · `oyun/sim/ucus_sim.py` (saf Python) · Dayanak: PLAN_B §5.2–5.3 (S1–S9, D1–D7), KARARLAR.md (8. oturum dahil)

Çalıştırma (klasör `oyun/sim`): `python ucus_sim.py` (tam: 5 bot × 20 tohum × 60 tur, ~5,5 dk, `kampanya.json` yazar) · `ozet [n]` (ayar döngüsü + **hedef kontrol** listesi; ~2 dk/20 tohum, ~4 dk/40 tohum) · `tek 7 iyi` · `egri` · `esleme` · `kontrol` (geçiyor).

**Kapsam:** Ayar yalnız ilk 25 tur için. 26+ satırlar taslak. Para birimi jeton. Hedefler kodda tek yerde: `HEDEF` (S9 ile güncellendi). `ozet` artık tuttu/tutmadı listesini kendisi basar.

## 1. Uygulanan ayarlar

Her adımdan sonra `ozet 20` ile ölçüldü. Son kabul 40 tohumla yapıldı. "Öneri" sütunu PLAN_B §5.3'teki değer, "Son" sütunu koddaki değer. Farklıysa nedeni yazılı. Yaratıcı kurallara dokunulmadı. Değişen yalnız sayılar ve ölçüm.

| # | Düğme | Öneri | Son | Not |
|---|---|---|---|---|
| S1 | Durma (`v_dur`/`vx_dur`) olunca kademe **her irtifada** ateşlenir. Tropopoz üstünde `kademe_ust_vy_kat` | 0,5 | 0,5 | Uygulandı. Tur 25'te son şans artık kullanılıyor (iyi: ort. 1,9 kademe/tur) |
| S2 | Kazanç hedefi = **uçuş kazancı** (`kazanc_ucus`, duvar ve nakavt hariç), 3 tur kayan medyan, tohumlar arası medyan | – | – | `kayan_medyan()`. `ozet` toplam kazancı ayrı satırda verir |
| S3 | `bant_carpan` (y ≥ 1.000 · y ≥ 3.500), nesne ve km ödülüne uygulanır, `carpan_tavan` dışında. km ödülü bulunduğu bantta tümlenir | ×1,8 · ×3,0 | **×2,4 · ×4,3** | S4 ile birlikte ayarlandı (aşağıda) |
| S4 | `km_odul` · `nesne_prim` · `rakip_odul` | 55 · 2,0 · 0,45 | **75 · 2,8 · 0,20** | Öneri, geliri hedefin %50'sine düşürdü (tahmin −%20 idi). Orta/kotu ilerlemesi çöktü (orta yörünge yok, kotu ısı 45). Gelir, bant çarpanı geç döneme kaydırılarak geri alındı. `rakip_odul` tur 1 kazancının büyük payı olduğu için 0,2'ye indi |
| S5 | `isi_sure` · `isi_hiz` · Isı kalkanı görünür tur | 3 s · 3,0 · 8 | **2,5 s** · 3,0 · 8 | 3 s ile 40 tohumda iyi ısı **13**. 2,5 s → 12. Duvar tur 8–9'daki tropopozdan 2–4 tur sonra geliyor; kalkan "çözen geliştirme" |
| S6 | Boş dalış toparlanması: konide hedef yoksa dalış 0,4 s sürer, sonra burun eski yönüne (−10°…+45°) döner, `bos_dalis_kayip` | 0,4 s · 0,10 | 0,4 s · **0,0** | 0,10 ile **orta bot −%15** (aynı geliştirmeyle tek uçuş). Koninin hemen dışındaki hedefe dalışlar 0,4 s'den sonra da isabet ediyordu. 0 ile kotu +%17, orta kaybı yarıya iner. Aşağıda §4 |
| S7 | İyi yörünge > 27 → römorkör `firsat_guc_kat` | 4,5 → 5,5 | 5,5 | Uygulandı. Tek başına etkisi yok (29 → 29). 7,0 da denendi: orta 40 → 38, iyi değişmedi |
| S8 | Tavan > %10 → alçak bantta trambolin seyrelmesi: 30. s'den sonra her 10 s ×0,9, en az ×0,5 | y < 300 | **y < 1.000**, sekme garantisi de seyrelir | y < 300 hiç etki etmedi. Tavana çarpan turlar **bulut bandında** (300–1.000, vx 60–100, tepe ~600, yay başına 10–12 s). Garanti her 0,25 s trambolin koyduğu için seyrelme boşa gidiyordu; garanti de aynı olasılıkla atlanıyor. Etki küçük: iyi %18 → %14–17 |
| S9 | `HEDEF` güncellemesi (D1–D6) + `hedef_kontrol()` | – | – | Eşik turu **sansürlü medyan**: ulaşamayan kampanya "ulaşamadı" sayılır (eskiden yalnız ulaşanların medyanıydı; orta yörünge bu yüzden iyimser görünüyordu) |
| E1 | Boş dalışta y < `kademe_y` + 15 olunca hemen toparlan (`bos_dalis_yer`) | 15 | 15 | Koordinatör ekledi. Yere gömülen boş dalış kademe yakmasın |
| E2 | Nesneler üst üste doğmaz: d < r1 + r2 + 4 olan aday reddedilir (`dogus_pay`). Fırsat rotada kalır, çakışan eski nesne kalkar | 4 | 4 | Koordinatör ekledi. Ekran yoğunluğu 9,4 → 9,0 (kontrol 7–12 geçiyor) |

Ölçüm de değişti: `ozet` artık orta/iyi/usta için 40 tur, hic/kotu için 60 tur koşuyor (`OZET_TUR`). Önceden 25 turda kesildiği için Kármán ve yörünge medyanları eksik sayılıyordu.

## 2. Hedef tablosu (son kabul: `ozet 40`, son kod)

| Hedef | Ölçülen | | Öneri değerleriyle (S1–S8 yazıldığı gibi, 40 tohum) |
|---|---|---|---|
| iyi ses 2–3 | **4** | ✗ (sınırda; 20 tohumda 3) | 3 |
| iyi tropopoz 9–10 | 10 | ✓ | 10 |
| iyi ısı 11–12 | 12 | ✓ | 13 ✗ |
| iyi Kármán 17–19 | 17 | ✓ | 19 |
| iyi yörünge 24–27 | 27 | ✓ | 30 ✗ |
| usta yörünge ≤ 24 | 21 | ✓ | 25 ✗ |
| orta yörünge ≤ 34 | **40** (21/40 kampanya tur 40'a dek) | ✗ | ulaşamadı ✗ |
| kotu ısı ≤ 28 | **32** | ✗ | 45 ✗ |
| kotu Kármán ≤ 50 (≥ 15/20) | **5/40** | ✗ | 3/40 ✗ |
| iyi tur 15–25 medyan süre 45–55 s | 54 | ✓ | 54 |
| tavana çarpan ≤ %10 (her bot) | hic 4 · kotu 2 · **orta 13 · iyi 15 · usta 12** | ✗ | orta 13 · iyi 15 · usta 11 ✗ |
| uçuş kazancı t1 120 | **146** (+%22) | ✗ | 149 ✗ |
| t5 500 | **239** (−%52) | ✗ | 228 ✗ |
| t10 900 | **725** (−%19) | ✗ (sınırda; 40 tohumluk öbür koşu 885) | 493 ✗ |
| t15 1.600 | **1.291** (−%19) | ✗ (sınırda; öbür koşu 1.352) | 798 ✗ |
| t20 2.600 | 2.812 | ✓ | 1.289 ✗ |
| t25 4.000 | 4.097 | ✓ | 1.946 ✗ |
| beceri tur 1 iyi/hiç ≥ +%30 | +%55 | ✓ | +%44 |
| beceri tur 5 ≥ +%60 | +%152 | ✓ | +%150 |
| beceri tur 10 ≥ +%60 | +%233 | ✓ | +%151 |
| **Toplam** | **11/20** | | 7/20 |

Sınırda olanlar (ses, t10, t15) 40 tohumluk iki koşu arasında yer değiştiriyor. Ölçüm gürültüsü eşik turunda ±1, kazançta ±%10.

## 3. Tam koşu (`python ucus_sim.py`, 20 tohum, 60 tur; `kampanya.json`)

Eşiklerin ilk kırıldığı tur (medyan · %10–%90):

| Bot | Ses | Tropopoz | Isı | Kármán | Yörünge | Kaçış (taslak) |
|---|---|---|---|---|---|---|
| **hedef (iyi)** | 2–3 | 9–10 | 11–12 | 17–19 | 24–27 | (40) |
| hic | 6 | 27 · 20–32 | 28 · 22–35 | 45 · 33–53 | 53 (15/20) | 58 (9/20) |
| kotu | 7 | 30 · 25–42 | 35 · 25–48 | 52 (8/20) | — | — |
| orta | 4 | 15 · 9–19 | 19 · 15–28 | 31 · 25–39 | 42 · 36–51 | 50 (16/20) |
| iyi | 3 | 10 · 7–15 | 14 · 6–20 | 17 · 12–23 | 28 · 21–38 | 36 |
| usta | 3 | 9 | 9 | 14 | 21 | 29 |

Rakip nakavtı (hedef 7 · 14 · 22): iyi 6 · 13 · 20 · orta 8 · 16 · 27 · hic 14 · 29 · 44.

Tur süresi (ilk 25 tur): iyi tur 15–25 medyanı 53 s (%10–%90: 35–65), tavana çarpan orta %15 · iyi %17 · usta %10 · hic %2 · kotu %1.

Beceri farkı (aynı geliştirme, mesafe, bot/hiç − 1): tur 5 iyi +%186 · orta +%114 · kotu +%17. Tur 10 iyi +%227 · orta +%158 · kotu +%24. Tur 25 iyi +%116.

Dayanıklılık (alıcı %30 rastgele): alışverişsiz seri en çok 2, çıkmaz 0/20 (tüm botlar). İyi bot: Kármán 18, yörünge 26.

## 4. Kalan sorunlar ve bulgular

1. **Kazanç eğrisinin başı tutmuyor (tur 1: 146, tur 5: 239; hedef 120 / 500).** Tur 1 → 5 arası uçuş kazancı ×1,6 büyüyor, hedef ×4,2 istiyor. Erken dönemde gelir mesafeyle doğrusal; iyi bot tur 5'te tur 1'in ~2,5 katı yol alıyor, gelir çarpanı (izlenme) ise tur 10'a dek alınmıyor. Hiçbir doğrusal ödül düğmesi ikisini birden tutturamaz. Erken geliri yükseltmek erken eşikleri öne çekiyor: tur 5 ≈ 300 olan ayarda tropopoz 8, ses 2. Eşik hedefleri tur 5 ≈ 240 gelirle tutuyor. Yani **fiyatlar, tur 5 = 500 hedefinin varsaydığından ucuz.** Seçenekler (karar gerekir): (A) tur 1–5 hedefini 120 → 150, 500 → 250 yap (eğri tur 10'dan sonra tutuyor). (B) İlk 10 turun fiyatlarını ve duvar ödüllerini ~×2 yap ve gelir hedefini koru (ICERIK fiyat tablosu değişir). (C) Erken bir gelir geliştirmesi (izlenme) daha görünür/ucuz olsun (kara kutu kartı önerir).
2. **Kötü dokunan oyuncu (kotu) hâlâ hiç dokunmayandan yavaş** (ısı 32 vs 28; Kármán 5/40 vs hic 45). S6 uçuşta farkı kapattı: aynı geliştirmeyle kotu artık hic'ten +%8–24 ileri. Asıl neden **alışveriş**. Sim'de hic'e kara kutu kartı hep "Rampa gücü"nü öneriyor, kotu ise iyi bot gibi dalış geliştirmelerine (dalış, dolum, yakıt) para yatırıyor ama dalışları tutmuyor. Tanı: kotu yalnız hic'in alım değerleriyle oynatılınca **ısı 28 ✓, Kármán 44 (20/20) ✓.** Öneri (tasarım kararı, uygulanmadı): kara kutu kartı önerisini oyuncunun dalış isabet oranına bağla. Dalışları tutmayan oyuncuya rampa/aerodinamik/kademe önerilsin.
3. **Orta oyuncu yörüngeye geç ulaşıyor** (40; 21/40 kampanya tur 40'a dek). Bu, sansürlü medyanla ilk kez dürüstçe görünüyor; eski raporda "33 (11/20)" yalnız ulaşanların medyanıydı. Römorkör ×7 orta'yı yalnız 2 tur öne çekti. Engel orta'nın uzaydaki tepe hızı. Seçenekler: (A) orta hedefini ≤ 40'a gevşet (B1 kapsamı 25 tur olduğundan tipik oyuncu yörüngeyi B1'de görmez). (B) Yörünge koşulunu orta için kolaylaştıran bir yardım (yörünge göstergesi / uzayda dalış konisi genişler). İkisi de karar.
4. **Tavan oranı %12–17 (hedef ≤ %10).** Tavana çarpan turlar bulut bandında (300–1.000) yavaş, yüksek yaylar. vx 60–100 hızla 10–12 s'lik yaylar, fişek/konfeti ile yeniden besleniyor. `vx_dur` tropopoz altında geçerli değil. S8 (y < 1.000, garanti dahil) %18 → %14–17 düşürdü. Daha sert seyrelme (×0,8, en az ×0,3) ve alçak bant sönümü (`SONUM_ALT` ek 7 → 14 ya da y1 1.000) **denendi**. Tavanı düşürmedi, ilerlemeyi bozdu (iyi Kármán 17 → 25). Kalan kaldıraçlar kural değişikliği, karar gerekir: (A) `vx_dur` benzeri bir durma koşulu bulut bandında da (ör. vx < 80, 3 s; uçuşun 30. s'sinden sonra). (B) Tur başına fırsat sınırı 5 → 4 (kullanıcı onaylı sayı). (C) %15'i kabul et, tavan emniyet olarak kalsın.
5. **Koordinatörün B0 ölçümü (ses 4, ilk 5–15 turda %42 tavan) sim'le uyuşmuyor.** Sim'de iyi bot ses 3–4, tavan ilk 15 turda %10'un altında. B0'daki %42 büyük olasılıkla B0'a özgü bir fark (fırsat çıkışı, garanti, durma kuralı ya da `ayar_uret.py`'nin eski değerleri okuması). Ayarlar bu oturumda değişti (§1), `ayar_uret.py` yeniden koşulmalı.
6. Ölçüm gürültüsü: 20 tohumda eşik turu ±2, 40 tohumda ±1. Karar için 40 tohum kullanıldı.

## 5. PLAN_B §5'e işlenecekler

- §5 tablo: sürükleme satırına **irtifa bandı ödül çarpanı** (y ≥ 1.000 ×2,4 · y ≥ 3.500 ×4,3; nesne + km ödülü; ×4 çarpan tavanının dışında).
- Isı duvarı: **v ≥ 250, y < 1.000, kesintisiz 2,5 s**; ısı/s = (v − 250) × **3** × ρ(y) × (1 − 0,15·kalkan) − 25. Isı kalkanı görünür **tur 8**.
- Kademe: durma (v < 25 ya da tropopoz üstünde vx < 110, 2 s) olunca **her irtifada** kademe ateşlenir. Tropopoz üstünde vy × 0,5 (ileri ağırlıklı). Kademe yoksa tur biter.
- Dalış: **boş dalış** (konide hedef yok) 0,4 s sürer ya da y < 40'a inince biter. Burun dalış öncesi yöne döner (−10°…+45°), hız büyüklüğü dalış öncesiyle aynı (kayıp 0).
- Dünya yönetmeni: nesneler üst üste doğmaz (d < r1 + r2 + 4 reddedilir). Uçuşun 30. s'sinden sonra y < 1.000'de trambolin ağırlığı ve sekme garantisi her 10 s ×0,9 (en az ×0,5).
- Ekonomi (§7): km ödülü 75 jeton/km(iç), nesne primi ×2,8, rampa zeplin vuruşu hasar × 0,2 jeton. Römorkör güç çarpanı ×5,5.
- §5.1 hedef tablosu S9'a göre: eşikler ses 2–3 · tropopoz 9–10 · ısı 11–12 · Kármán 17–19 · yörünge iyi 24–27 / usta ≤ 24 / orta ≤ 34. Mesafe tur 25 bilgi satırı (sim: 69–84 km; D1'in tahmini 90–130 tutmadı). Tur 25 hız satırı kalkar. Kazanç = uçuş kazancı, 3 tur kayan medyan. Beceri farkı tur 1 ≥ +%30, tur 5/10 ≥ +%60.
- §5.1 sim sütunu §2 ve §3'teki sayılarla güncellenir. §5.2 zayıf oyuncu: hic ısı 28 ✓ / Kármán 45 ✓; kotu ısı 32 ✗ / Kármán 5/40 ✗ (neden §4.2).
- §5.3 sonuna: S4 tahmini (−%20) gerçekte −%35/−%50 idi. S6'nın 0,10 kaybı orta oyuncuyu cezalandırdı. S8 y < 300 bandı yanlış banttı. Karar bekleyenler §4.1–4.4.

## 6. Simüle edilmedi

Nadir olaylar, kapsül kartları, görevler, albüm, rüzgâr/dalga bulutu/fırtına, F5/F7/F8/F9, Süzülgen/Kancalı roket, hayalet, uçuşta rakip hasarı (yalnız rampa vuruşu), ölümcül nesneden kaçınan bot. Bot parametreleri (tepki, hata, mini oyun oranları, alışveriş değerleri) gerçek oyuncu verisiyle düzeltilmeli. Özellikle kotu botun alışverişi (§4.2).

## 7. Seyreltme ve geçit kuralı (2026-10-08, kullanıcı kararı; uygulayıcı)

Kullanıcı B0'ı telefonda denedi: "nesneler çok yoğun, bir şeye çarpmadan uçulmuyor".

- **Yoğunluk:** `ekran_hedef` 7 → **5** (~%30 seyrek). `kontrol` yoğunluk aralığı 7–12 → 5–9 oldu; ölçülen ortalama 6,9.
- **E3 geçit kuralı (`gecit`):** roketin pasif yoluna doğan aday (|y − rota_y| < r + r_roket), aynı sütunda üstünde ya da altında en az 2·(r_roket + `kacis_pay` 4) = 16 b boşluk bırakmıyorsa reddedilir. Alt sınır zemin. Rastgele çekim yok; çekim sırası değişmedi. `ekle` içinde, E2'den sonra uygulanıyor.
- **Ekonomi düzeltmesi:** daha az temas geliri düşürdü. `nesne_prim` 2,8 → **3,1** ile karşılandı (en az sapma). Ölçüm 20 tohumluk kampanya, tur 1'de 40 tohum:

| | Eski (7, ×2,8) | Yeni (5, ×2,8) | Yeni (5, ×3,1) |
|---|---|---|---|
| iyi: ses duvarı ilk tur (medyan) | 3 | 4 | **3** |
| iyi: tur 5 / 15 kazanç | 415 / 2.343 | 382 / 2.547 | 451 / 2.565 |
| hic: tur 5 / 15 kazanç | 160 / 404 | 119 / 426 | 139 / 402 |
| iyi: tropopoz ilk tur | 10,5 | 9 | 9 |
| iyi: 25 turda tavana çarpan | %18 | %13 | %15 |
| tur 1 süre (iyi / hic) | 17,3 / 16,2 s | 16,5 / 15,9 s | — |

- **Kalan sapma:** hic botunun tur 5 kazancı eskiden %13 düşük (139'a karşı 160); tur 15'te aynı. İyi botun tur 1 vay ≤ 5 s oranı 0,90'dan 0,97'ye çıktı (daha az martı/uçurtma freni).
