# Uçuş + ekonomi simülasyonu: rapor (2. ayar)

2026-10-08 · `oyun/sim/ucus_sim.py` (saf Python) · Dayanak: PLAN_B §5, ICERIK §5, KARARLAR.md (8. oturum dahil)

Çalıştırma (klasör `oyun/sim`): `python ucus_sim.py` (tam: 5 bot × 20 tohum × 60 tur, ~80 s, `kampanya.json` yazar) · `ozet [n]` (ayar döngüsü, ilk 25 tur) · `tek 7 iyi` · `egri` · `esleme` · `kontrol` (geçiyor).

**Kapsam:** Ayar yalnız **ilk 25 tur** için yapıldı. Tablolarda 26+ satırlar **taslak**. Para birimi **jeton**. Hedefler kodda tek yerde: `HEDEF`.

## 1. Ne değişti

| Kalem | Eski | Yeni | Neden |
|---|---|---|---|
| Botlar | hic, kotu (rastgele dokunur), iyi, usta | **hic, kotu, orta, iyi, usta**, tek tablo `BOTLAR` | §2 |
| Botların görüşü | iyi/usta oyunun koni yardımını kâhin gibi kullanıyordu (400 b ileri) | Yalnız **ekranda görünen** nesneler (ileri bakış ≤ ekranın 2/3'ü) | Görev 1 |
| Tur tavanı | 85 s uçuş + rampa | **65 s tur** (yalnız emniyet) | Görev 2 |
| Yörünge sönümü | 14 b/s² | **22 b/s²** (`sonum_yorunge` ayrı düğme, şimdilik 22) | Görev 2 |
| v < 600 ek sürükleme | yok | y 300→3500 arası 0→**7 b/s²** (`SONUM_ALT`) | Görev 2 |
| Yüksekte asılı kalma | yok | Tropopoz üstünde **yatay hız 2 s boyunca < 110** → tur biter (`vx_dur`) | Uzun turların asıl nedeni, §6.1 |
| Turda fırsat sayısı | sınırsız | **en çok 5** (römorkör muaf) (`firsat_tur_max`) | Uzun uçuş kendini fırsatla beslemesin |
| Gösterge dolumu / temas | trambolin 0,25 · diğer 0,20 | **0,08 · 0,13** | Dalış zinciri sonsuza dek sürmesin |
| Saniye başına ödeme | 2,5 jeton/s | **0** | Görev 2. Yerine: km ödülü 50→**70**, nesne ödülüne `nesne_prim` **×2,4** (izlenme→jeton çevrimi `odul_kat`=0,10 **dokunulmadı**) |
| Rampa üst sınırı | 190 (12/sv) | **230** (16/sv) | Görev 3 |
| Son ateşleme, kademe itkisi | 15/sv · 5/sv | **19,5/sv · 6,5/sv** (+%30) | Görev 3 |
| Kármán eşiği | y 3000 | **y 3500**; irtifa eşlemesi 3500 b = 100 km; uzay bantları Kármán'dan türer | Görev 4 |
| Bilim balonu sekme açısı | 30° | **40°** + y > 2900'de yükselirken **6 b/s²** ek dikey sönüm (`ust_sonum`) | KARARLAR 8. oturum |
| Habitat | trambolin, 15° | 15°, **ayrı sınıf "kayma yüzeyi"** (`kayma=True`; `kontrol` 40–55° kuralından muaf tutar) | KARARLAR 8. oturum |
| Fırsat güçleri | ICERIK değerleri | ICERIK × **fişek 2,8 · konfeti 2,8 · jet 3,5 · römorkör 4,5** (`firsat_guc_kat`) | Görev 4 |
| Dalış itkisi | 14 + 2,2/sv | 14 + **4,0/sv** | Geç oyun hızı (yörünge) |
| Dalış konisi | 60–80° | **66–76°** | Geniş konide tepki süresi önemsizdi (usta ≈ iyi), §3 |
| Isı duvarı süresi | 250 üstünde 1 s | **2 s** | Tek fişek patlamasıyla kırılmasın |
| Alıcı bot | römörkörü hiç almıyordu | Römorkör değeri "romorkor_y'ye çıkabiliyor musun"a bağlı; `rastgele` seçeneği (dayanıklılık) | |

Değişmeyen: duvar ödülleri, fiyatlar, seviye sayıları, rakip canları, izlenme→jeton çevrimi, ekran yoğunluğu.

## 2. Botlar (`BOTLAR`)

| Bot | Tepki s | Hedef tahmini hatası | Öngörü | Mükemmel kalkış | Mini oyun | Not |
|---|---|---|---|---|---|---|
| hic | – | – | – | hep "iyi" (3 s bekler) | %0 | Uçuşta hiç dokunmaz |
| kotu | 0,40–0,70 | ±%50 | 0,2 | ≈ bölge (%12–24), %25 zayıf | %25 | + saniyede 0,15 amaçsız dokunuş |
| **orta** | 0,25–0,40 | ±%25 | 0,7 | %50–60 | %35 | Yeni |
| iyi | 0,18–0,30 | ±%10 | 0,8 | %80–95 | %50 | Eskiden 0–0,15 s ve ekran dışını görüyordu |
| usta | 0–0,05 | 0 | 1,0 | %97 | %100 | |

`kotu` yeniden tanımlandı: eski rastgele dokunan kotu, hiç dokunmayandan **daha kötüydü** (tur 10'da −%40); yani "kötü oyuncu" modeli değil, cezaydı. Yenisi hedefe dokunmaya çalışıyor ama geç ve hatalı.

## 3. Hedef ve sonuç (iyi bot, 20 tohum, tek birim)

Birimler: iç birim **b**, **b/s** (yalnız kodda). Göstergede: mesafe **km** (gösterge hızının yatay bileşeninin tümlevi, `mesafe_g`), irtifa **km** (`irtifa_km`), hız Mach / km/s. Eski rapordaki "iç b · gösterge km" karışık sütunu ve "hedefi simülasyona göre değiştir" önerisi kaldırıldı: hedefler PLAN_B §5 / ICERIK §5'ten, sim onlara ayarlanır.

| Tur | Ölçüt | Hedef | Ölçülen | |
|---|---|---|---|---|
| 1 | süre · mesafe · kazanç | 18 s · 1,2 km · 120 | 18 s · 1,7 km · 171 | mesafe ve kazanç biraz yüksek |
| 3 | süre · mesafe · en yüksek hız | 30 s · 4 km · Mach 1+ | 27 s · 3,8 km · Mach 1,9 | ✓ |
| 5 | kazanç | 400 | 701 | yüksek |
| 10 | süre · mesafe · hız · kazanç | 50 s · 25 km · 260 b/s · 900 | 45 s · 22,5 km · 256 b/s · 932 | ✓ |
| 15 | kazanç | 1.600 | 1.031 | düşük |
| 15–25 | tur süresi medyanı | 45–55 s | 46 s | ✓ |
| 20 | kazanç | 2.600 | 2.283 | ✓ (±%15) |
| 25 | mesafe · hız · kazanç | 150 km · 600 b/s · 4.000 | 67 km · 426 b/s · 1.815 | **düşük** |

Tur 25 süresi PLAN_B'de 75 s yazıyor; bu görevde 45–55 s istendiği için o kullanıldı (PLAN_B güncellenmeli).

## 4. Eşiklerin ilk kırıldığı tur (medyan · %10–%90, 20 tohum)

| Bot | Ses | Tropopoz | Isı | Kármán | Yörünge | Kaçış (taslak) |
|---|---|---|---|---|---|---|
| **hedef (iyi)** | 3 | 10 | 12 | 18–19 | 25 | (40) |
| hic | 6 | 28 | 28 | 47 · 37–55 | 54 (5/20) | — |
| kotu | 7 | 30 (19/20) | 30 (19/20) | 38 (7/20) | — | — |
| orta | 3 | 12 | 12 | 23 · 13–37 | 37 (19/20) | 51 (13/20) |
| iyi | 2 | 8 | 9 | **17** · 11–24 | **31** · 20–37 | 43 |
| usta | 2 | 8 | 8 | **13** · 10–18 | **25** · 21–30 | 32 |

Rakip nakavtı (medyan, hedef 7 · 14 · 22): iyi 6 · 12 · 19 · usta 5 · 12 · 19 · orta 7 · 16 · 26 · hic 14 · 30 · 46.

İyi ile usta farkı: Kármán **4 tur** ✓, yörünge **6 tur** ✓. Uyarı: kampanya başına sapma büyük. Aynı ayarla iki ölçümde iyi botun yörünge medyanı 26 ve 31 çıktı (20 tohumda ±3 tur oynuyor).

## 5. Tur süresi (ilk 25 tur)

| Bot | Tur 15–25 medyan | %10–%90 | Tavana (65 s) çarpan |
|---|---|---|---|
| hic | 30 s | 17–58 | %3 |
| kotu | 20 s | 10–53 | %3 |
| orta | 52 s | 27–65 | **%17** |
| iyi | 46 s | 23–65 | **%13** |
| usta | 44 s | 21–60 | %10 |

Medyan hedefte. Tavana çarpma orta ve iyi botta %10'un üstünde (§7).

## 6. Beceri farkı (aynı geliştirmeler: iyi botun o turdaki seviyeleri, 60 uçuş)

| Tur | kotu | orta | iyi | usta |
|---|---|---|---|---|
| 1 (geliştirmesiz) | +%13 | +%33 | +%44 | +%41 |
| 5 | −%15 | +%106 | +%150 | +%185 |
| 10 | +%17 | **+%153** | +%232 | +%243 |
| 25 | +%20 | +%64 | +%89 | +%83 |

Orta botun tur 10 hedefi (+%150–300) bu ölçümde sınırda tutuyor. 20 tohumlu `ozet` ölçümünde ise +%123 çıktı. Tur 1'de iyi/hic +%44; eski hedef ≥ %60'tı. Bunun nedeni iyi botun artık gerçekçi tepki süresiyle oynaması.

## 7. Zayıf oyuncu tabanı

| Hedef | Sonuç |
|---|---|
| kotu: ısı duvarı ~tur 25 | Medyan **30** (19/20). Hedefe yakın, tutmadı |
| kotu: Kármán ~tur 45 | 60 turda yalnız **7/20** kırabildi (medyan 38). **Tutmadı** |
| hic: tüm geliştirmeler maksta tropopoz | Ortalama tepe irtifa 1.584 b, **6/10** tur tropopozu geçiyor ✓ |
| hic kampanyası (bilgi) | Tropopoz 28, ısı 28, Kármán 47 |

Kaldıraçlar: rampa 230, +%30 pasif geliştirmeler, kotu bot modeli (§2). Kotu botun Kármán'a ulaşması için ek kaldıraç gerekiyor: tur başına sabit sponsor ödemesini (`taban_odul` 25) artırmak ya da dokunuş istemeyen bir "otomatik dalış" geliştirmesi eklemek. İkisi de tasarım kararı.

## 8. Dayanıklılık: alıcı %30 olasılıkla rastgele satın alır

| Bot | Kármán | Yörünge | Alışverişsiz seri maks (ilk 25 · 60 tur) | Çıkmaz |
|---|---|---|---|---|
| hic | 48 (18/20) | 54 (3/20) | 2 · 2 | 0/20 |
| kotu | 54 (7/20) | — | 2 · 2 | 0/20 |
| orta | 27 | 44 | 1 · 2 | 0/20 |
| iyi | 17 | 32 | 1 · 3 | 0/20 |
| usta | 13 | 28 | 1 · 2 | 0/20 |

"Alışverişsiz seri ≤ 3" ve "çıkmaz yok" hâlâ geçiyor. Çıkmaz: ilk 25 turda art arda 5 tur ne alım ne yeni eşik ne rakip nakavtı olması. Açgözlü alıcıyla seri en çok 2.

## 9. Açık sorunlar ve seçenekler

1. **Uzun turun asıl nedeni yörünge değil, sürekli beslenen zincirlerdi.** İki yer var. (a) Üst atmosferde (1000–3500) yoğunluk ≈ 0 olduğu için kayıp yok, bilim balonu basamak gibi çalışıyor. (b) Fırsatlar zamana bağlı çıktığı için uzun uçuş daha çok fırsat topluyor. Görevdeki iki kaldıraç (sönüm 22, v < 600 ek sürükleme) tek başına süreyi değiştirmedi: tavansız ölçümde medyan 70–90 s, p90 120–200 s kaldı. Süreyi asıl üç yeni kural düşürdü: `vx_dur`, `firsat_tur_max` ve düşük gösterge dolumu. Bunlar oynanış kuralıdır, **onay gerekir**. Kalan sorun: tavana çarpanların çoğu alçakta (y < 1000) yavaş sekme zincirleri, orta botta %17, iyide %13. Denenip işe yaramayanlar: düz/doğrusal ek sürükleme (erken turları öldürüyor), alçakta yatay hız eşiği (tur 1 süresini 9–13 s'ye düşürüyor), yavaşken sekme garantisini kapatmak, gösterge dolumunu hıza bağlamak, sekme kaybını artırmak. Seçenekler: (A) %13–17'yi kabul et, tavan emniyet olarak kalsın. (B) Fırsat çıkışını süre yerine mesafeye bağla (denenmedi). (C) Alçak bantta (y < 300) trambolin yoğunluğu uçuş ilerledikçe seyrelsin (denenmedi).
2. **Yörünge ~tur 25.** Yalnız fırsat gücüyle olmadı. Römorkörü ×7 güçlendirmek, ucuzlatmak (2.500), erken açmak (tur 18), uçuşta garanti çıkarmak (`romorkor_garanti`, kapalı) ya da yörünge hızında sönümü sıfırlamak iyi botun yörünge turunu değiştirmedi (33–37). Asıl engel iyi botun tur 22–25'teki tepe hızı (~430). Sonuçta dalış itkisini 2,2'den 4,0/sv'ye çıkardım: yörünge 26–31 oldu. ICERIK'teki "dalış 14 → 36" artık **14 → 54**; onay gerekir. Diğer seçenekler: (A) "Bölge 4 / yörünge" takvimini tur ~30'a kaydır. (B) Yörünge koşulunu "v ≥ 600, 1 s" yerine 0,5 s yap (`duvar_sure`). Denedim, etkisi küçük.
3. **Erken eşikler 1–3 tur erken** (iyi: ses 2/3, tropopoz 8/10, ısı 9/12, Kármán 17/18–19). Erken kazanç yüksek (tur 5: 701, hedef 400), geç kazanç düşük (tur 25: 1.815, hedef 4.000). Eğri fazla düz. Sonraki ayarın konusu: erken rampa vuruşu ödülü (`rakip_odul`) ile km ödülü düşürülsün, geç dönemde izlenme/kombo çarpanı güçlensin.
4. **Ölçüm gürültüsü büyük.** Tek tohumda kampanyalar ±5 tur oynuyor. Beceri farkı ortalama mesafeyle ölçülüyor ve uç değerlere duyarlı. Karar verirken 20+ tohum ve medyan kullanılmalı (`ana` artık beceri farkını 60 uçuşla ölçüyor).
5. **Tasarım dokümanlarına işlenecekler:** PLAN_B §5 hedef tablosu (tur 25 süresi 75 → 45–55 s), Kármán 3.500 b = 100 km, bantlar (üst atmosfer 1.000–3.500, yörünge 3.500+), ısı duvarı 2 s, dalış konisi 66–76°, fırsat güç çarpanları, habitat "kayma yüzeyi" sınıfı, ₺ → jeton.

## 10. Eksik sistemler ve ışığa duyarlılık

Kapsam kararına göre B0/B1'e yalnız şunlar giriyor: **ayarlar** (müzik/efekt ayrı, titreşim, hareket azaltma, ışığa duyarlılık modu, yazı boyutu, kalite kademesi, kaydı sıfırla), **duraklat** (düğme + arka plana geçişte otomatik; devam/yeniden başla/hangar/ayarlar; dönüşte 3-2-1) ve **erişilebilirlik**. Renk körlüğü modu, yedek kodu, satın alma kilidi ve istatistik ekranı B1'den sonra. Kayıt şeması (`v` sürümü, güvenli varsayılan) yine gerekli.

Işığa duyarlılık: tam ekran flaş saniyede 3'ten sık olmaz. Mükemmel sekme parlaması ekranın en çok %30'u, < 100 ms. Kırmızı-beyaz titreşim olmaz. Duvar ağır çekimi parlaklık oynatmaz. `prefers-reduced-motion` okunur. Uyarılar renkten ayrı olarak şekille de ayırt edilir.

## 11. Simüle edilmedi

Nadir olaylar, kapsül kartları, görevler, albüm, rüzgâr/dalga bulutu/fırtına, F5/F7/F8/F9, Süzülgen/Kancalı roket, hayalet, uçuşta rakip hasarı (yalnız rampa vuruşu sayılıyor), ölümcül nesneden kaçınan bot. Bot parametreleri (tepki, hata, mini oyun oranları) gerçek oyuncu verisiyle düzeltilmeli.
