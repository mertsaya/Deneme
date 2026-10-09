# Son Durak: Plüton — İçerik Kitabı

Taslak 2 · 2026-10-08 · Dayanak: `PLAN_B.md` Taslak 6.2, `KARARLAR.md`, `oyun/sim/ucus_sim.py` · Durum: §10 soruları kullanıcı onayı bekliyor

**Taslak 2'de değişenler:** para birimi altın jeton; sayılar simülasyonla eşitlendi (`TIPLER`, `FIRSATLAR`, `GELISTIRME`, `AYAR`); Kármán y 3.500 = 100 km, tropopoz y 1.000; bilim balonu 40° + üst atmosfer sönümü; habitat ayrı sınıf "kayma yüzeyi"; `vx_dur`, `firsat_tur_max`; dalış gücü 14 → 54; evrensel ton (yerel kaplamalar, reklam yazıları, rakip karakterleri ve bilgi kartları değiştirildi); kalıntılar (kaya, rotor akımı, su sütunu, kıyı, kargo pilotu, uydu mini sapanı) çıkarıldı.

**Kapsam.** Her tabloda **Kapsam** sütunu var: **B1** = ilk 25 tur (sim'le ayarlı ya da ayarlanacak), **Sonra** = B1.5 ve sonrası, **taslak**. Tur 26+ takvimi taslak.

**Sayılar hakkında.** Birimler PLAN_B §5 ile aynı: hız b/s, ivme b/s², mesafe b (1 b ≈ 1 m iç birim), yükseklik y (b). v_yörünge 600, v_kaçış 849. **Ödül** sütunu izlenme puanıdır; jeton = ödül × kombo × izlenme çarpanı × 0,10 × 2,4 (sponsor primi). Örnek: balon 15 → 3,6 jeton (kombosuz). `~` işaretli sayılar tahmin, oyun testinde önce onlar ayarlanır. **Ağırlık (w)** = o yükseklikte açık türler arasında seçilme ağırlığı; toplam yoğunluk ekran başına ~7 nesne (yoğunluk yönetmeni).

**Burrito Bison notu.** BB karşılıkları oyunun genel yapısına dayanıyor; tek tek jöle adları "BB'de benzeri" diye yazıldı, birebir iddia değil. BB'den isim, görsel ya da metin alınmaz.

---

## 0. Genel kurallar (her nesne için geçerli)

| Kural | Değer (sim) |
|---|---|
| Çarpışma | Daire–daire: roket yarıçapı 4, nesne yarıçapı `r` |
| Çarpma yönü | **Üstten:** roket nesne merkezinin üstünde (y ≥ y_nesne) ve vy < 0,35·|v|. **Yandan:** diğer her temas |
| Trambolin sekmesi | Hız büyüklüğü × k_etkin (k + 0,012 × Sekme verimi sv, tavan 0,92); yön nesnenin **sekme açısına** döner (40–55°). Her zaman k < 1 |
| Kayma yüzeyi | Trambolinle aynı fizik, sekme açısı 15° (roket yüzeyde kayıp ileri fırlar). Yalnız habitat |
| Yandan temas | Hız × (1 − yan kaybı); dalış iptal |
| Yavaşlatıcı | Hız × (1 − kayıp × (1 − 0,08 × Burun konisi sv)); nesne etkisizleşir |
| Aynı nesneyle tekrar | 2 s içinde ikinci etki ve ödül yok |
| Ömür | Trambolin `omur` vuruşta söner/patlar (patlamış nesne etki vermez) |
| Kombo | 3 s içinde art arda vuruş: her vuruş +0,05, tavan ×2,0 (Kombo tavanı ile ×3,0); tüm çarpanların çarpımı en çok ×4 |
| Mükemmel sekme | Dalış süresi (1,2 s) içinde üstten trambolin teması: |v| + min(%10, 12 b/s). Enerji kaynağı dalış yakıtı |
| Dalış göstergesi | Trambolin 0,08 · diğer temas 0,13 · mükemmel 0,10 · fırsat 0,30 (+%10/sv Gösterge dolum). 1,0 = 1 dalış; tur 1,0 ile başlar |
| Sekme garantisi | Pasif rotanın altında (en az 15 b), y ≥ 25, her an en az 1 trambolin; 0,25 s'de bir denetlenir, yoksa rotanın uzak yarısına (ekran dışı) konur |
| Açılış zeplini | Kalkıştan 1,8 s sonraki rota noktasına bir reklam zeplini konur ("vay" garantisi) |
| Fırsat aralığı | Tür başına ortalama 30 s / (1 + 0,25 × Sıklık sv); türler arası ≥ 6 s; turda en çok 5 (römorkör hariç); rotada 1,6–2,6 s ileriye konur |
| Ölümcül aralığı | ~22 s'de bir (×0,8–1,2), yalnız roket y 200–750 iken; rotaya konur; uyarı 1,5 s önce |
| Rampa | Rampa platformu y = 60; 38° kalkış |

---

## 1. Dünya bölümü nesne kataloğu

Bantlar: **A** alçak hava (25–250) · **B** bulutlar (250–1.000) · **Ü** üst atmosfer (1.000–3.500) · **U** uzay (3.500+, Kármán).

### 1.1 Sekme nesneleri (trambolin)

| # | Ad | Görünüş | y aralığı · w | k · açı · yan · ömür | Nesneye ne olur | Ödül | Açılış | Kapsam | BB karşılığı |
|---|---|---|---|---|---|---|---|---|---|
| S1 | Şişme reklam balonu | Yuvarlak, gülen yüzlü, dondurma reklamlı dev balon | 40–200 · 3,0 | 0,80 · 50° · %6 · 3 | Çöker, sallanır; 3. vuruşta patlar, konfeti | 15 | Tur 1 | **B1** | Normal jöle |
| S2 | Parti balonu salkımı | 20 renkli balon, kurdeleli hediye kutusu | 30–150 · 2,0 | 0,70 · 42° · %2 · 2 | Her vuruşta 6–8 balon patlar; 2. vuruşta biter, kutu paraşütle iner | 10 | Tur 1 | **B1** | Küçük jöle |
| S3 | Reklam zeplini | Dev, tombul, çizgili zeplin; yanında patlamış mısır kovası resmi ve "PATLAMIŞ MISIR" yazısı (öneri, §10); insansız | 80–500 · 1,2 | 0,85 · 45° · %10 · 3 | Zarf 25 b çöker, dalgalanır; 3. vuruşta söner, yamalı zarf süzülerek iner | 40 | Tur 1 | **B1** | İri jöle |
| S4 | Yük dronu | Dört pervaneli kutu dron, üstünde şişme kırmızı yastık; insansız | 60–450 · 0,6 | 0,80 · 55° · %25 · 1 · **+15 vy** | Üstten: aşağı basılır, batarya ışığı kırmızıya döner, alçalıp ayrılır. Yandan: pervaneleri savrulur, gövde paraşütle iner | 60 | Tur 2 | **B1** | Zıplatan özel jöle |
| S5 | Sıcak hava balonu | Kırmızı-beyaz dilimli, otomatik brülörlü reklam balonu; insansız | 250–950 · 1,0 | 0,85 · 40° · %8 · 3 | Zarf çöker; brülör korkuyla alev püskürtür; balon yavaşça döner | 30 | Tur 9 | **B1** | İri jöle |
| S6 | Kargo paraşütü kubbesi | Kargo uçağının attığı paletlerin turuncu paraşütleri, 3–5'li | A, B · yalnız kargo uçağı (X1) çarpışmasından sonra | ~0,75 · 45° · %2 · 1 | Kubbe çöker; palet yedek paraşütle iner | 25 | Tur 6 | **B1** (sim'de yok) | — |
| S7 | Bilim balonu | Dev, ince, saydam balon; altında alet kutusu | 800–3.400 · 1,2 | 0,85 · **40°** · %3 · 3 | İnce zarf dalgalanır, alet kutusu sallanır | 30 | Tropopoz eşiği | **B1** | — |
| S8 | Şişme habitat modülü | Kumaş görünümlü, beyaz, tombul uzay modülü; içinde sallanan test mankeni. **Kayma yüzeyi:** geniş, düz üst yüzey (görsel tasarım kullanıcı onayına) | 3.500–9.000 · 0,8 | 0,90 · **15°** · %5 · 3 | Esner, yavaşça döner; manken pencereye yapışır | 60 | Kármán | **B1** | — |
| S9 | Rakip zeplini (uçuşta) | Sıradaki rakibin renklerinde yamalı zeplin | A, B · turda %30, en çok 1 | 0,85 · 45° · %10 · 3 | Rakibe +25 hasar (× Zeplin hasarı); kaptan pencereden yumruk sallar | 50 | Rakip 1 | **B1** (sim'de yok) | Ringdeki rakip |

**Üst atmosfer sönümü (bilim balonu 40° kararıyla birlikte):** y > 2.900'de yükselirken ek −6 b/s² dikey sönüm. 40°'lik sekmenin verdiği fazla irtifa böylece kesilir, roket Kármán'ı hızla değil "basamakla" geçemez.

### 1.2 Yavaşlatıcılar

| # | Ad | Görünüş | y aralığı · w | Rokete etkisi | Nesneye ne olur | Ödül | Açılış | Kapsam | BB karşılığı |
|---|---|---|---|---|---|---|---|---|---|
| Y1 | Martı grubu | 2–3 tombul, şaşkın bakışlı martı, tek çarpışma dairesi (r 13) | 25–180 · 3,0 | −%6; yön 2° yukarı döner (büyüklük değişmez) | Sersemler, tüyleri uçar, takla atar, toparlanıp uçar | 20 | Tur 1 | **B1** | Normal jöle |
| Y2 | Uçurtma | Baklava biçimli, kuyruklu, yere ince ipiyle bağlı | 40–220 · 1,5 | Gövde −%2. **İp:** roket uçurtmanın altından geçerse ipe takılır, −%15 (× (1 − 0,2 × İp kesici)) | İp kopar, uçurtma savrulup süzülür | 6 | Tur 1 | **B1** | Engelleyici jöle |
| Y3 | Afiş çeken uçak | Uzaktan kumandalı küçük pervaneli uçak, arkasında "BÜYÜK İNDİRİM!" afişi (öneri, §10) | 60–200 · 0,4 | −%35 | Afiş yırtılır; uçak yalpalayıp yoluna devam eder | 25 | Tur 4 | **B1** | Polis jöleleri |
| Y4 | Radyosonde | Küçük beyaz meteoroloji balonu, altında kutu | 50–700 · 1,0 | −%2 | Balon patlar, kutu küçük paraşütle iner | 8 | Tur 5 | **B1** | — |
| Y5 | Sığırcık bulutu | Şekil değiştiren dev kuş bulutu (~300 kuş) | A · ~0,25 | İçinden geçerken her 0,1 s −%1 | Kuşlar roket biçiminde boşluk açar | 2/kuş | Tur 16 | Sonra | — |
| Y6 | Göktaşı tozu izi | Gökte ince, parıltılı turuncu çizgi | 1.000–3.400 · 0,8 | −%5 | Kıvılcım saçılır, iz dağılır | 20 | Tropopoz | **B1** | — |
| Y7 | Gece parlayan bulut | Elektrik mavisi ince buz bulutu şeridi | Ü · ~0,5 | −%3, ısı −20 | Roket izinde aralanır | 15 | Tropopoz | Sonra | — |
| Y8 | Volkanik kül bulutu | Gri, kabarık, kıvılcımlı bulut | B · ~0,15 | −%6; 2 s dalış göstergesi dolmaz | Arkada girdap | 20 | Tur 15 | Sonra | — |
| Y9 | Uydu | Altın folyolu kutu, iki mavi güneş paneli; insansız | 3.600–9.000 · 1,0 | −%12 | Panel fırıldak gibi döner, bazen kopar; gövde yörüngeden sapar | 50 | Kármán | **B1** | — |
| Y10 | Uzay çöpü | Somun, eldiven, boya pulu, kırık panel | 3.500–9.000 · 2,0 | −%8 | Parça ikiye bölünür, ayrı yönlere savrulur | 15 | Kármán | **B1** | — |

### 1.3 Hızlandırıcılar ve fırsatlar

Satın alınınca dünyada çıkar (§3). Güç = (taban + güç sv × artış) × sim güç çarpanı (`firsat_guc_kat`).

| # | Ad | Görünüş | Bant | Rokete etkisi (sv0) | Nesneye ne olur | Enerji kaynağı | Ödül | Kapsam | BB karşılığı |
|---|---|---|---|---|---|---|---|---|---|
| H1 | Havai fişek roketi | Çizgili, kocaman, fitili tüten fişek | Rota üstü | Tutunursun: 1,2 s boyunca 35° yönünde toplam 60 × 2,8 = 168 b/s itiş | Yakıtı bitince havada çiçek gösterisi | Barut | 40 | **B1** | Roketli jöle |
| H2 | Konfeti topu dronu | Dronun altında yıldız ağızlı pembe top | Rota üstü | 30° yönünde 45 × 2,8 = 126 b/s (mini oyunda ×1,2 ya da ×0,7) | Geri tepmeyle dron 30 b geriye savrulur, konfeti yağar | Basınçlı gaz tüpü | 35 | **B1** | Patlayan jöle |
| H3 | Sapan dronu | İki dron arasında gerili dev lastik | A, B | giriş × 0,9 + 70 | Dronlar içe çekilir, sallanır | Gerili lastik | 50 | Sonra | Fırlatıcı jöle |
| H4 | Tanker dronu | Göbekli, gri, hortumlu dev dron | B | Dalış hakları dolar, +50 | "Boş" lambası yanar, uzaklaşır | Tanker yakıtı | 80 | Sonra | — |
| H5 | Su roketleri | Yerden yükselen 3'lü pet şişe roket | A | Alttan çarparsa vy +25 | Takla atar, minik paraşüt | Basınçlı hava | 15 | Sonra | — |
| H6 | Römorkör | Turuncu, kepçe burunlu, mıknatıs kollu insansız araç | y ≥ 1.500 | Kenetlenir, 40 × 4,5 = 180 b/s itiş, 10° (mini oyunda 0°) | Yakıtı biter, kolunu açıp el sallar | Römorkörün yakıtı | 120 | **B1** | — |

### 1.4 Toplanabilirler

| # | Ad | Görünüş | Bant | Rokete etkisi | Nesneye ne olur | Ödül | Açılış | Kapsam |
|---|---|---|---|---|---|---|---|---|
| T1 | Yakıt dronu | Sarı bidon taşıyan küçük dron (r 9) | Rota üstü | +1 dalış (Güç sv2: +0,25 gösterge; sv4: +2 dalış); mini oyunda +0,25 | Bidonu bırakır, sallanarak uzaklaşır | 20 | Satın al (F1) | **B1** |
| T2 | Altın martı | Güneş gözlüklü, parıltılı martı | A · ~0,05 | Martı gibi | Altın simli konfeti döker | 150 | Tur 7 | Sonra |
| T3 | Yayın dronu | Tek kameralı, "CANLI" ışıklı dron | A, B, Ü | Fizik yok; izlenme ×2, 5 s | Kamera seni takip eder | Çarpan | Satın al (F9) | Sonra |
| T4 | Kargo kapsülü | Paraşütlü, çizgili, "KIRILIR" etiketli kapsül (piñata) | Her bant · turda %35 | −%4 | Açılır, 3 kart fırlar (üçü de kazanılır) | 3 kart (§4.6) | Tur 3 | **B1** (sim'de yok) |
| T5 | Rakip tanıtım balonu | Sıradaki rakibin yüzü basılı küçük balon, 3'lü | A, B | Üstten k 0,7 | Patlar, rakip yüzü "aaa!" | 10 + rakibe hasar | Rakip 1 | Sonra |

### 1.5 Tehlikeler (seyrek, uyarılı, adil)

**Kural (KARARLAR):** Ölümcül çarpışma turu bitirmez, bir kademe kaybettirir (çarpan kademe parçalanır, üstteki fırlar). Son kademedeysen tur biter. Uyarı ≥ 1,2 s (sim 1,5 s). Zırh varsa önce zırh kullanılır (turda 1).

| # | Ad | Görünüş | Bant | Uyarı | Rokete etkisi | Nesneye ne olur | Ödül | Açılış | Kapsam |
|---|---|---|---|---|---|---|---|---|---|
| X1 | Kargo uçağı | Kocaman, tombul, "HIZLI KARGO" yazılı insansız uçak (r 22, kanat ±40) | 300–600 | Kenar oku + motor uğultusu 1,5 s önce | Gövde: kademe kaybı. Kanat ucu (|dx| < 40, |dy| < 4): −%30 | Gövde ikiye ayrılır, kanatlar savrulur, 3–5 kargo paraşütü (S6) açılır | 200 | Tur 6 | **B1** |
| X2 | Sondaj roketi | İnce beyaz, dikine yükselen küçük roket | A, B | Duman sütunu + kesişme çizgisi | −%25, vy +20 | Takla, paraşüt | 60 | Tur 11 | Sonra |
| X3 | Ölü üst kademe | Paslı, dönen dev silindir | U | Kırmızı üçgen + yörünge çizgisi 2 s | Gövde: kademe kaybı. Sürtme −%25 | 4 parça çöp saçar | 250 | Tur 24 | Sonra |

### 1.6 Çevresel bantlar (fırsat olarak satın alınır)

| # | Ad | Görünüş | Konum | Rokete etkisi (sv0) | Enerji kaynağı | Ödül | Kapsam |
|---|---|---|---|---|---|---|---|
| C1 | Termal sütun | Titreşen sıcak hava sütunu, içinde dönen yapraklar ve 2–4 leylek | y 25–250, 120 b genişlik; roket y ≤ 300 iken çıkar | İçindeyken +8 b/s² yukarı, turda en çok 3 s | Güneşin ısıttığı yer | 3/s | **B1** |
| C2 | Jet akımı | Gök boyunca akan beyaz çizgili rüzgâr nehri | y 400–650, 60 b kalınlık, 1.500 b uzunluk; roket y 250–800 iken çıkar | İleri ivme = 12 × 3,5 × (1 − v / V), V = 180 b/s; v ≥ V ise 0 | Atmosferin rüzgârı | 5/s | **B1** |
| C3 | Dalga bulutu | Üst üste merceksi bulutlar | B | Önde +14 b/s², arkada −6 | Dağ dalgası rüzgârı | 4/s | Sonra |
| C4 | Rüzgâr tabakası | Yatay ince bulut çizgileri | A, B | Kuyruk +4 / karşı −6 b/s² | Rüzgâr | 0 | Sonra |
| C5 | Fırtına hücresi | Örs tepeli dev kara bulut | B | Merkez +20, kenar −15 b/s²; yıldırım 0,8 s dalış kilidi | Sıcak nemli hava | 25 | Sonra |

**B1 sayımı:** trambolin 8 (S1–S7, S9) + kayma yüzeyi 1 (S8) + yavaşlatıcı 7 (Y1–Y4, Y6, Y9, Y10) + fırsat 4 (H1, H2, H6, T1) + bant 2 (C1, C2) + kapsül 1 (T4) + tehlike 1 (X1) = **24**. Kalan 14 nesne **Sonra**.

### 1.7 İlk turun senaryosu (tohum sabit, "vay" ≤ 5 s)

| Zaman | Olay |
|---|---|
| 0,0 s | Gösterge iğnesi gidip gelir. İpucu: "Yeşilde dokun" |
| ~1,0 s | Mükemmel kalkış (70 × 1,30 = 91 b/s): roket rakip zeplininin gondoluna değer, R1 kaptanının şapkası uçar, +91 hasar |
| ~2,5 s | Martı grubuna dalış: tüy patlaması, "+5" jeton sayıları, kombo |
| ~3–4 s | **"Vay" anı:** açılış zepliniyle ilk sekme; roket ekranın üstüne fırlar, zeplin dalgalanır. İpucu: "Dalış için dokun" |
| 6–12 s | Balon zinciri, uçurtma ipi, ilk dalış, ilk mükemmel sekme |
| ~12 s | Hız düşer, y < 25: **SON ŞANS**, boş kademe paraşütle ayrılır, roket yukarı fırlar |
| ~18 s | Pilot kapsülde paraşütle iner, kamyonet gelir. Kara kutu: ~120–170 jeton, "Rampa gücü 60 jeton" kartı |

---

## 2. Nadir olaylar

**Kural:** turda en fazla bir nadir olay. Her turun başında zar: taban **%25**. **Acıma sayacı:** 4 tur üst üste çıkmadıysa sonraki turda garanti. Olay roketin önünde 1,5 km'de kurulur, 2 s önceden kenar ışığıyla duyurulur ("SICAK HABER!"). Sim'de yok; B1'de eklendikten sonra sim'e eklenmeli.

**B1 (5 olay, KARARLAR'daki komik ve tuhaf set):**

| # | Olay | Ne görürsün | Oynanış | Koşul · ağırlık | İlk kez garanti | Ödül | Mantık gerekçesi |
|---|---|---|---|---|---|---|---|
| U1 | Dev şişme kedi | Bağlarından kopmuş 60 b'lik şişme dev kedi, ayaklarından 6 halat sarkıyor | Sırtında 5 sekmeye kadar: k 0,9, 45°; her sekmede "miyav", kulaklar sallanır. Halatlar −%10 | A, B · 10 | Tur 5 | 5 × 100 + 500 | Festivalden kopmuş, insansız; sonra dronlar halatlarından çekip götürür |
| U4 | Uçan daire şakası | Parlayan, dönen disk; içinde yeşil kostümlü manken | Üstü trambolin (k 0,9) × 3; 3. vuruşta söner, "UFO DEĞİL, KAMPANYA!" afişi çıkar | B · 6 | Tur 14 | 800 + kart | Rakip ajansın disk biçimli zeplini (sahte uzaylı = rakip zeplini) |
| U5 | Leylek termalleri | Termal sütunlarda döne döne yükselen 40 leylek | 3 termal yan yana, her biri +12 b/s² (turda en çok 3 s); leyleğe çarparsan sersemler (−%2) | A, B · 8 | Tur 9 | 400; hiç çarpmazsan +400 | Leylekler termallerle süzülür; termalin varlığını leylekler gösterir |
| U9 | Meteor şok dalgası | 12 göktaşı izi gökyüzünü çizer, sonunda dev ateş topu | Ateş topu arkadan yetişir (1,5 s uyarı): şok dalgası **+80** ileri | Ü · 6 | Tur 20 | 900 + kart | Göktaşı roketten çok hızlı; şok dalgası onun kinetik enerjisinden pay |
| U12 | Kayıp balina zeplini | Mavi, kuyruğunu sallayan balina biçimli eski zeplin, "1. Hava Festivali" yazılı | 7 sekmeye kadar sırtında; kuyruk sekme yönünü 10° ileri çevirir (hız artmaz) | B · 3 | — (tur 10'dan sonra rastgele) | 7 × 120 + kaplama parçası | Eski festival zeplini; kuyruk yön çevirir, enerji eklemez |

**Sonra (taslak):** U2 Hava gösteri filosu (rüzgâr gölgesi −%60 sürükleme, 4 s) · U3 Gökyüzü fenerleri (en çok 120 fener, kombo) · U6 Güneş tutulması (izlenme ×2, 10 s) · U7 Rakip roket yarışı (8 s, eşit kütle çarpışması) · U8 Güneş enerjili dev kanat (3 sekme, k 0,85) · U10 Kutup ışıkları (izlenme ×2, uydular kayar) · U11 Uzay istasyonu (+2 dalış, robot kol bidon fırlatır).

---

## 3. Satın alınabilir fırsat nesneleri

Her fırsatın üç çizgisi var: **Aç** (tek), **Sıklık** (4 sv: ortalama aralık 30 s → 15 s), **Güç** (5 sv). Fiyat = taban × 1,55^sv. Fırsata çarpınca 90 ms duraksama ve ×0,4 ağır çekim (0,3 s). **Her fırsatın kendi mini zamanlama oyunu var** (KARARLAR); turkuaz **dokunma halkası** içindeyken dokunuş dalış yerine o nesnenin eylemini yapar. Her yeni mini oyun ilk karşılaşmada tek satır ipucuyla gelir, turda en çok bir yeni kural. Sim bunu bot başına "tutturma olasılığı" ile modelliyor (hiç %0 · kötü %25 · orta %35 · iyi %50 · usta %100).

**B1 (6 fırsat):**

| # | Fırsat | Aç · görünür | Sıklık taban | Güç taban · formül | Mini oyun (tek dokunuş) | Dokunmazsan |
|---|---|---|---|---|---|---|
| F1 | Yakıt dronu (T1) | 150 · tur 2 | 100 | 120 · sv0 +1 dalış; sv2 +0,25 gösterge; sv4 +2 dalış | Bidon düşerken dalışla yakala: +0,25 gösterge | Normal etki |
| F2 | Havai fişek (H1) | 300 · tur 3 | 150 | 160 · (60 + 10·sv) × 2,8 b/s, süre 1,2 + 0,1·sv s | **Erken patlat:** son %25'lik yeşil pencerede dokun → kalan itki ×1,25 (toplam ≈ ×1,19) | Tam itki, bonus yok |
| F3 | Konfeti topu dronu (H2) | 450 · tur 6 | 180 | 200 · (45 + 10·sv) × 2,8 b/s | **Nişan:** top 10°–60° arası sallanır (0,8 s); 25°–35° "mükemmel" = ×1,2 | 0,8 s sonra 30°'de ×0,7 |
| F4 | Termal sütun (C1) | 400 · tur 8 | 150 | 170 · 8 + 1,6·sv b/s², 3 s | Sütunun tepesine yakın çık, sonra dal | — (bant) |
| F6 | Jet akımı (C2) | 1.200 · tur 11 | 300 | 350 · ivme (12 + 1,2·sv) × 3,5 × (1 − v/V), V = 180 + 24·sv | 60 b kalınlıktaki akımda kalmak için sekme ve dalışı zamanla | — (bant) |
| F10 | Römorkör (H6) | 5.000 · tur 21 | 800 | 900 · (40 + 8·sv) × 4,5 b/s; yalnız y ≥ 1.500 | **Yön seç:** itme oku 0°–40° arası sallanır, dokunduğun yönde iter | 0,8 s sonra 10°'de iter |

**Sonra (taslak):** F5 Sapan dronu (900, tur 12) · F7 Tanker dronu (2.000, tur 15) · F8 Dalga bulutu (1.500, tur 13) · F9 Yayın dronu (600, tur 9). Mini oyunları Taslak 1'deki gibi (bırak, bağlan, poz ver).

---

## 4. Süreklilik sistemleri

### 4.1 Rakip ajanslar (rampadaki zeplin)

**Hasar:** H = v_kalkış × kalite × (1 + 0,15 × Zeplin hasarı sv). Kalite: mükemmel 1,0 · iyi 0,4 · zayıf 0. Rampa vuruşu ayrıca hasar × 0,6 jeton verir. Uçuşta (B1, sim'de yok): rakip zeplini (S9) +25. Hasar turlar arası birikir, her %20'de bir yama. Nakavt: zeplin söner, fırıldak gibi uçup gider, kaptan paraşütle iner ve yumruk sallar.

**Ton:** evrensel çizgi film arketipleri, yerel gönderme yok. **Adlar ve karakter biçimi §10 S1'de soruluyor;** aşağıda yalnız rol, zeplin ve kişilik var.

| # | Rol · ajans | Zeplin | Kişilik (tek replik, ad onayından sonra yazılır) | Can (sim) | Nakavt ödülü | Hedef nakavt | Kapsam |
|---|---|---|---|---|---|---|---|
| R1 | Balon turizmcisi · balon turları şirketi | Pembe-beyaz çizgili, püsküllü | Kendini beğenmiş gösteriş meraklısı | 700 | 500 + Konfeti topu dronu bedava açılır | Tur 7 | **B1** |
| R2 | Kargocu · hızlı kargo şirketi | Koli bantlı kahverengi | Telaşlı, her şeye etiket yapıştırır | 1.100 | 1.500 | Tur 14 | **B1** |
| R3 | Dalgın bilimci · meteoroloji enstitüsü | Beyaz, anten dolu, fırıldaklı | Sürekli hesap yapar, hep yanılır | 1.800 | 4.000 | Tur 22 | **B1** |
| R4 | Reklamcı · telekom şirketi | Gümüş, çanak antenli, ışıklı | Hızlı konuşur, cümle bitirmez | 3.200 | 8.000 | Tur ~30 | Sonra |
| R5 | Kibirli milyarder · uzay holdingi | Siyah-altın dev zeplin | Tepeden bakar; yenilince ilk kez gülümser | 5.200 | 15.000 | Tur ~39 | Sonra |

Her rakip ilk gelişinde 2 s'lik giriş sahnesi (atlanabilir), her mükemmel kalkışta tepki animasyonu, nakavtta 3 s sahne. Sim nakavt (iyi): 6 · 12 · 19.

### 4.2 Eşikler ve bölgeler

**İlk kırılış** büyük ödül ve sinematik (300 ms duraksama, ×0,2 ağır çekim); sonrakilerde ödülün %10'u.

| Eşik | Koşul (sim) | Göstergede | Sinematik | İlk ödül | Açtıkları | Hedef ilk kırılış (iyi) | Kapsam |
|---|---|---|---|---|---|---|---|
| Ses duvarı | v ≥ 115, 0,3 s (Cd tepesi v 100'de) | Mach 1,3 | Şok konisi, "BUM", arka planda tarlada inek şaşırır | 300 | Bölge 2 | 2–3 | **B1** |
| Tropopoz | y ≥ 1.000 | 12 km | Bulutlar aşağıda kalır, gök bir ton koyulaşır | 600 | Bilim balonu, göktaşı tozu | 9–10 | **B1** |
| Isı duvarı | v ≥ 250, y < 1.000, ısı kilidi yokken 2 s | Mach 5 | Burun kızarır, plazma halesi, soğuma buharı | 1.500 | Bölge 3 | 11–12 | **B1** |
| Kármán çizgisi | y ≥ 3.500 | **100 km** | Gök siyaha döner, sesler bir anlığına kesilir | 3.000 | Uydu, çöp, habitat | 17–19 | **B1** |
| Yörünge hızı | v ≥ 600, y ≥ 3.500, 1 s | 7,9 km/s | Roket süzülür, ufuk kavislenir, yıldızlar yanar; telsiz: "Yörüngedeyiz!" | 6.000 | Bölge 4 | 24–27 | **B1** |
| Kaçış hızı | v ≥ 849, y ≥ 3.500, 1 s (tur biter) | 11,2 km/s | Dünya küçülür, Ay büyür; 3 s geçiş | 15.000 | Ay bölümü | ~40 | Sonra |

Hedef turlar PLAN_B §5.3 S9 önerisine göre (onay bekliyor). Şu anki sim (iyi): 2 · 8 · 9 · 17 · 31.

**Bölgelerin kimliği** (anlık hıza göre):

| Bölge | Hız | Gök ve görünüş | Müzik katmanı | Baskın nesneler |
|---|---|---|---|---|
| 1 · Sabah Göğü | 0–100 | Açık mavi, pamuk bulutlar, aşağıda yeryüzü dekoru (PLAN_B §16 S6) | Akustik ritim + el çırpma | Martı, balon, uçurtma, zeplin |
| 2 · Bulut Denizi | 100–250 | Bulutların üstü, altın güneş, gölgenin çevresinde gökkuşağı halkası | + Synth bas | Sıcak hava balonu, kargo uçağı, jet akımı |
| 3 · Lacivert Tavan | 250–600 | Lacivertten siyaha, ufuk kavisli, ince mavi atmosfer çizgisi | + Koro pad | Bilim balonu, göktaşı tozu |
| 4 · Sessiz Yörünge | 600–849 | Siyah, yıldızlar, altta mavi Dünya | Katmanlar düşer, piyano; efektler telsiz sesine döner | Uydu, çöp, habitat, römorkör |

### 4.3 Görevler (36 görev, 12 set) — kapsam §10 S4

Aynı anda 3 görev görünür. Set bitince rütbe artar, kalıcı +%2 izlenme. Ceza ya da zaman sınırı yok. Ödüller jeton.

| Set · rütbe | Görev 1 | Görev 2 | Görev 3 | Ödül (her biri) |
|---|---|---|---|---|
| 1 · Stajyer | Mükemmel kalkış yap | 5 balondan sek (toplam) | 1 km uç | 50 |
| 2 · Çaylak Pilot | Tek turda 10 martı grubunu sersemlet | Bir dalışı mükemmel sekmeyle bitir | Son şanstan sonra 500 b daha uç | 80 |
| 3 · Pilot | Ses duvarını kır | Bir zeplini söndür (3 vuruş) | ×1,5 komboya ulaş | 150 |
| 4 · Kıdemli Pilot | Uçurtma ipine ve afişe takılmadan 3 km uç | Kargo kapsülü aç | 3 mükemmel sekme art arda | 250 |
| 5 · Gösteri Pilotu | Havai fişekte "erken patlat" bonusu al | 1. rakibi nakavt et | Tek turda 30 s havada kal | 400 |
| 6 · Kargo Avcısı | Kargo uçağının 60 b yakınından çarpmadan geç | 3 radyosonde patlat | Tek turda 2 farklı fırsat kullan | 600 |
| 7 · Hız Avcısı | Isı duvarını kır | Jet akımında 3 s kesintisiz kal | ×2 komboya ulaş | 900 |
| 8 · Bulut Ustası | Tropopozu geç | Bir nadir olay gör | Konfeti topunu "mükemmel" açıda ateşle | 1.300 |
| 9 · Fırtına Kovalayan | 2. rakibi nakavt et | Hiç dalış kullanmadan 4 km uç | 2 son şansı da kullan, sonra 1 km daha uç | 1.800 |
| 10 · Astronot Adayı | Kármán çizgisini geç | Bir uydu panelini döndür | Bir habitattan kay | 2.500 |
| 11 · Astronot | Yörünge hızına ulaş | Römorkörle kenetlen | ×3 komboya ulaş | 3.500 |
| 12 · Kaşif | 5. rakibi nakavt et | Kaçış hızına ulaş | 20 bilgi kartı topla | 5.000 (taslak) |

### 4.4 Koleksiyon: bilgi kartları (30 kart, 6 albüm) — kapsam §10 S4

Kartlar kapsülden, nadir olaylardan, rakip nakavtlarından ve set ödüllerinden gelir. Albüm tamamlanınca 1.000 × albüm no jeton ve bir kaplama. **[D]** = yayından önce doğrulanmalı. Yerel kartlar evrensel karşılıklarıyla değiştirildi.

| Albüm | Kartlar |
|---|---|
| 1 · Alçak hava | Ses deniz seviyesinde ~343 m/s, ~1.235 km/sa (20 °C) **[D]** · Leylekler göçte kanat çırpmadan termallerle yükselir **[D]** · Sığırcık sürülerinde her kuş en yakın ~7 komşusunu izler **[D]** · Meteoroloji balonları dünyada günde iki kez yüzlerce istasyondan aynı saatte bırakılır **[D sayı]** · Uçurtmalar binlerce yıldır kullanılıyor; ilk kullanım Çin'de **[D]** |
| 2 · Ses duvarı | İlk ses duvarı aşan uçuş: Bell X-1, 14 Ekim 1947 **[D]** · Ses duvarında sürükleme birden artar · Concorde ~Mach 2 ile yolcu taşıdı **[D]** · Sonik patlama uçağın arkasından sürüklenen bir koni · Buhar diski yoğuşmadan oluşur, her zaman Mach 1'de değildir **[D]** |
| 3 · Bulutlar ve hava | Jet akımları ~9–12 km'de, saatte yüzlerce km'ye çıkabilir **[D]** · Merceksi bulutlar dağ dalgalarında oluşur · Fırtına bulutunun tepesi tropopoza dayanınca örs biçimi alır · 2010 kül bulutu Avrupa hava trafiğini günlerce durdurdu **[D]** · Gökkuşağı halkası uçak gölgesinin çevresinde görünür |
| 4 · Lacivert tavan | Gece parlayan bulutlar ~76–85 km'de **[D]** · Göktaşlarının çoğu ~80–100 km'de yanar **[D]** · Kırmızı cinler fırtınaların üstünde çakan kısa ışıklar **[D]** · X-15 roket uçağı Mach 6,7'ye ulaştı (1967) **[D]** · Stratosfer atlayışı rekorları 2012 ve 2014 **[D irtifa]** |
| 5 · Kármán ve yörünge | Kármán çizgisi 100 km, uzayın yaygın kabul gören sınırı **[D: bazı kurumlarda 80 km]** · Alçak yörünge hızı ~7,8–7,9 km/s **[D]** · ISS ~400 km'de, ~90 dakikada bir tur atar **[D]** · Yörüngede olmak "sürekli düşüp ıskalamak"tır · İzlenen uzay çöpü sayısı on binlerce **[D]** · Kessler etkisi: çarpışmaların zincirleme çöp üretmesi |
| 6 · İnsanlar ve kilometre taşları | Sputnik 1, 4 Ekim 1957 **[D]** · Yuri Gagarin, ilk insanlı uzay uçuşu, 12 Nisan 1961 **[D]** · Valentina Tereşkova, uzaya çıkan ilk kadın, 16 Haziran 1963 **[D]** · Apollo 11, Ay'a ilk insanlı iniş, 20 Temmuz 1969 **[D]** · Kaçış hızı ~11,2 km/s ≈ yörünge hızının √2 katı **[D]** · İlk yörünge roketi kademesinin geri inişi: Aralık 2015 **[D]** |

### 4.5 Roketler ve kaplamalar — Sonra (B4)

| Roket | Açılış | Özel güç | Bedel |
|---|---|---|---|
| Kıvılcım | Baştan | Dengeli | — |
| Süzülgen | Tur ~18 · 6.000 | Dalış hakkı yokken dokun: kanatlar 1,2 s açılır, g_etkin × 0,35, Cd × 1,3; bekleme 5 s | Dalış gücü −%15 |
| Kancalı | Tur ~28 · 25.000 | 140 b menzildeki trambolinlere kanca: 0,6 s sarkaç, hız %95 korunur; 1 dalış harcar | Mükemmel sekme bonusu yok |

**Kaplamalar (görsel, güç vermez), 12 adet (öneri, §10 S3):** Karpuz · Donut · Gökkuşağı · Dondurma külahı · Şeker bastonu · Retro Sputnik · Leylek · Milyarder (R5 nakavtı) · Konfeti · Kargo kolisi · Altın martı · Galaksi.

### 4.6 Kargo kapsülü kartları (B1)

Kapsül açılınca 3 kart fırlar, **üçü de kazanılır** (KARARLAR). "Tek tur" kartları bir sonraki turda geçerli, rokette görünür parça olarak durur.

| Tür | Kart | Etki | Ağırlık |
|---|---|---|---|
| Para | Bahşiş · Sponsor çeki · Büyük ikramiye | Son 5 tur ortalama kazancının %20 · %50 · %120'si | 25 · 12 · 3 |
| Tek tur güç | Ek yakıt tankı | Başlangıçta +1 dalış | 8 |
| | Turbo rampa | Kalkış +20 b/s | 8 |
| | Yedek kademe | +1 son şans | 5 |
| | Kombo mıknatısı | Kombo süresi +2 s | 6 |
| | Tampon | İlk yavaşlatıcının kaybı %0 | 6 |
| | Fırsat yağmuru | Fırsat aralığı ×0,5 (tur sınırı 5 değişmez) | 5 |
| İndirim | Kupon | Bir geliştirmede %25 indirim | 8 |
| Rakip | Gizli dosya | Sonraki kalkışta rakibe +%50 hasar | 5 |
| Koleksiyon (meta kapsamına bağlı) | Bilgi kartı · Kaplama parçası | Albüme kart · kaplamaya parça | 10 · 8 |
| Nadir | Altın kapsül | Sonraki kapsülde bir kart Büyük ikramiye | 1 |

Meta sistemler B1 dışındaysa koleksiyon kartlarının ağırlığı Para kartlarına eklenir.

### 4.7 Günlük ve oturum hedefleri — kapsam §10 S4

| Sistem | Kural |
|---|---|
| Günlük hedefler | Her gün 3 küçük hedef; ödül son 5 tur ortalama kazancının %50'si; yapılmayanlar silinmez, en çok 9 birikir |
| Günün tohumu | Herkes aynı gün aynı tohumla; yalnız kendi geçmişinle karşılaştırma |
| Günün yıldızı | Bir nesne türü ×2 ödül |
| Isınma | Oturumun ilk turunda dalış göstergesi 1,5 ile başlar |
| Kesinti | Yarıda bırakmak hiçbir şey kaybettirmez |

### 4.8 Rekorlar ve hayalet

| Öğe | Kural | Kapsam |
|---|---|---|
| Rekorlar | En uzak mesafe · en yüksek hız · en yüksek irtifa · en büyük kombo · en çok sekme | **B1** |
| Rekor balonu | En uzak mesafende bayraklı işaret balonu ("REKOR 4,2 km"); geçince patlar, "YENİ REKOR!" | **B1** |
| Hayalet | En iyi turun izi yarı saydam silüet; geçince +%10 kazanç (turda 1) | §10 S4 |
| Kara kutu karşılaştırması | Bu tur ve en iyi tur hız-mesafe eğrisi | **B1** |

---

## 5. İlerleme takvimi

Hedef: her 2–4 turda bir yenilik. Uçuş kazancı hedefleri (3 tur kayan medyan, tek seferlikler hariç; PLAN_B §5.3 S2): tur 1: 120 · 5: 500 · 10: 900 · 15: 1.600 · 20: 2.600 · 25: 4.000.

### 5.1 B1: ilk 25 tur

Eşik turları "iyi" oyuncu için hedeftir (PLAN_B §5.3 S9); "görünür" sim'deki `GELISTIRME` görünürlük turu.

| Tur | Yeni nesne / olay | Hangar (görünür) | Rakip / eşik |
|---|---|---|---|
| 1 | Martı, reklam balonu, parti balonu, uçurtma, reklam zeplini | Rampa gücü, Sekme verimi, Kademe itkisi, Dalış gücü, İzlenme çarpanı | R1 gelir |
| 2 | Yük dronu | Mükemmel bölge, Gösterge dolum, **F1 Yakıt dronu** | (Ses duvarı 2–3) |
| 3 | Kargo kapsülü | **F2 Havai fişek** | **Ses duvarı** → Bölge 2 |
| 4 | Afiş çeken uçak | İp kesici, Aerodinamik | |
| 5 | Radyosonde · **U1 Dev şişme kedi** (garanti) | Burun konisi | |
| 6 | Kargo uçağı + kargo paraşütleri | **F3 Konfeti topu**, Zırh | |
| 7 | — | Zeplin hasarı | **R1 nakavt** → R2 |
| 8 | — | **F4 Termal sütun**, Isı kalkanı (öneri; sim: tur 10) | |
| 9 | Sıcak hava balonu · **U5 Leylek termalleri** (garanti) | Kombo süresi | (Tropopoz 9–10) |
| 10 | Bilim balonu, göktaşı tozu (tropopozla açılır) · U12 rastgele havuza girer | | **Tropopoz** |
| 11 | — | **F6 Jet akımı** | |
| 12 | — | Kademe sayısı (2 son şans) | **Isı duvarı** (11–12) → Bölge 3 |
| 14 | **U4 Uçan daire şakası** (garanti) | Mükemmel bonusu | **R2 nakavt** → R3 |
| 18 | Uydu, uzay çöpü, habitat (Kármán'la açılır) | | **Kármán çizgisi** (17–19) |
| 20 | **U9 Meteor şok dalgası** (garanti) | Kombo tavanı | |
| 21 | — | **F10 Römorkör** | |
| 22 | — | | **R3 nakavt** → R4 gelir |
| 23 | — | Dalış kapasitesi (3 dalış) | |
| 24 | — | Son ateşleme | |
| 25 | — | | **Yörünge hızı** (24–27) → Bölge 4 |

En uzun yeniliksiz aralık: 14 → 18 (3 tur). Takvimdeki görev setleri, albüm, günlük hedefler ve hayalet §10 S4 cevabına göre eklenir.

### 5.2 Tur 26–60 (taslak)

| Tur | Yeni nesne / olay | Hangar | Rakip / eşik |
|---|---|---|---|
| 26 | U10 Kutup ışıkları | Kademe sayısı (3 son şans) | |
| 27 | U11 Uzay istasyonu | Dalış kapasitesi (4 dalış) | |
| 28 | Ölü üst kademe | Kancalı roket | |
| 30 | — | | R4 nakavt → R5 |
| 31–39 | Nadir olay şansı %35+; R5'in altın reklam uydusu | Üst seviyeler | Ara rekor bayrakları (hız 700, 750, 800; ilk kez 1.000 jeton) |
| 39 | — | | R5 nakavt → Ay üssü |
| 40 | Kaçış sahnesi | | **Kaçış hızı** → Ay bölümü |
| 41–60 | Ay içeriği (§7) | Ay geliştirmeleri | Ay rakipleri, krater sırtları, Ay kaçışı (~62–65) |

Sonra listesindeki nesneler (Y5, Y7, Y8, H3–H5, T2, T3, T5, X2, X3, C3–C5) ve fırsatlar (F5, F7, F8, F9) B1.5'te 26–40 arasına yayılır.

---

## 6. Hangar geliştirme ağacı

Fiyat = taban × 1,55^(mevcut seviye); sabit listeler aynen. Değerler sim `GELISTIRME` ile birebir.

| Sekme | Geliştirme | Sv | Taban | Etki / seviye | Görünür | Kapsam |
|---|---|---|---|---|---|---|
| **Rampa** | Rampa gücü | 10 | 60 | Kalkış +16 b/s (70 → 230) | 1 | **B1** |
| | Mükemmel bölge | 5 | 80 | Yeşil bölge %12 → %24 (+2,4 puan) | 2 | **B1** |
| | Mükemmel bonusu | 5 | 200 | Mükemmel kalkış ×1,30 → ×1,55 (+0,05) | 14 | **B1** |
| | Zeplin hasarı | 8 | 120 | Rakibe hasar +%15 | 7 | **B1** |
| **Gövde** | Sekme verimi | 8 | 90 | k +0,012 (tavan 0,92) | 1 | **B1** |
| | Aerodinamik | 8 | 150 | Cd −%5 | 4 | **B1** |
| | Burun konisi | 6 | 120 | Yavaşlatıcı kaybı −%8 göreli | 5 | **B1** |
| | İp kesici | 4 | 100 | Uçurtma ipi freni −%20 göreli (%15 → %3) | 4 | **B1** |
| | Isı kalkanı | 6 | 1.500 | Isınma −%15 | 10 (öneri 8) | **B1** |
| | Zırh | 3 | 2.500 | Turda 1 ölümcül çarpmayı kademe harcamadan atlatır; hız kaybı %60 / %45 / %30 | 6 | **B1** |
| **Kademeler** | Kademe sayısı | 2 | 600 / 6.000 | Son şans 1 → 2 → 3 | 12 | **B1** |
| | Kademe itkisi | 8 | 200 | +6,5 b/s dikey ve yatay (vy 78 → 130; vx +15 → +67) | 1 | **B1** |
| | Kademe yakıtı | 5 | 300 | Ateşleme 0,8 → 1,4 s | 16 | Sonra |
| | Hurda satışı | 5 | 150 | Paraşütle inen kademe başına +20 jeton | 19 | Sonra |
| **Motor** | Dalış gücü | 10 | 70 | +14 → +54 b/s (+4,0) | 1 | **B1** |
| | Gösterge dolum | 8 | 90 | Dolum +%10 | 2 | **B1** |
| | Dalış kapasitesi | 2 | 900 / 7.000 | 2 → 3 → 4 dalış | 23 | **B1** |
| | Son ateşleme | 4 | 400 | +19,5 b/s / sv (|vx| < 30, kademe yokken, turda 1) | 24 | **B1** |
| **Fırsatlar** | F1, F2, F3, F4, F6, F10 | Aç + 4 + 5 | §3 | §3 | §3 | **B1** |
| | F5, F7, F8, F9 | | | | | Sonra |
| **Yayın** | İzlenme çarpanı | 10 | 150 | +%10 | 1 | **B1** |
| | Kombo süresi | 5 | 120 | 3 → 5,5 s (+0,5) | 9 | **B1** |
| | Kombo tavanı | 3 | 1.000 | ×2,0 → ×3,0 (+0,33) | 20 | **B1** |
| | Kapsül sıklığı | 5 | 300 | Turda %35 → %60 | 22 | Sonra |
| | Sansasyon | 5 | 500 | Nadir olay şansı %25 → %50 | 17 | Sonra |
| **Roketler** | Süzülgen · Kancalı | — | 6.000 · 25.000 | §4.5 | 18 · 28 | Sonra |

B1: 19 geliştirme + 6 fırsat × 3 çizgi = **37 satın alma çizgisi**.

---

## 7. Diğer bölümler: içerik iskeleti (taslak)

Her bölümde tur sonu "yüzeye kademesiz değmek". Ayrıntılar Dünya bölümü eğlenceli bulunduktan sonra.

| Bölüm | Nesneler (tek satır davranış) | İmza nadir olay | Rakip / eşik fikri |
|---|---|---|---|
| **2 · Ay** | Hava yastığı topu: trambolin k 0,9 (sürükleme yok) · Kargo inici: iticileri seni yukarı iter (onun yakıtı) · Kütle sürücüsü kovası: +60 (güneş enerjisi) · Eski kademe hurdası: −%15 · Regolit tozu: −%3, görüş kısalır · Buz kütlesi: sert trambolin k 0,7 · Madenci dronu: −%10, cevher saçar (jeton) · Lazer yansıtıcı: kart · İşaret fişeği | **Ay geçidi istasyonu:** robot kol seni yakalayıp döndürür ve fırlatır (enerji korunur, yön değişir) | Robot kepçeli madenci kulesi · Krater sırtları, Ay kaçışı |
| **3 · Mars** | Toz hortumu: +12 b/s² · Mars helikopteri: k 0,7 · Paraşütlü iniş kapsülü · Hava yastıklı iniş topu: k 0,85 · CO₂ gayzeri: +30 · Kum fırtınası: −4 b/s² · Kum bulutu: −%4 · Phobos sapanı: +30 · Deimos: kart | **Küresel toz fırtınası:** 15 s, izlenme ×3 | Uçan daire şakasının sahibi turizm şirketi · Olympus Mons, Mars kaçışı |
| **4 · Asteroit Kuşağı** | Moloz yığını asteroit: k 0,8 · Metal asteroit: ölümcül, uyarılı · Kuyruklu yıldız gaz jeti: +40 · Madenci gemisi: −%20 · Toz halkası: −%2 · İkili asteroit · Buzlu asteroit · Cüce gezegen sapanı: +50 | **Çarpma testi:** moloz dalgasında sörf | Madenci kartel · Kirkwood boşlukları |
| **5 · Jüpiter** | Konveksiyon kulesi: +25 b/s² · Amonyak bulutu: −%3 · Büyük Kırmızı Leke · Io volkan sütunu: +70 · Radyasyon kuşağı · Europa buz kırığı: k 0,75 · Jüpiter sapanı: +150 | **Kuyruklu yıldız çarpması:** şok dalgası +100 | Gaz toplayıcı · Radyasyon kuşağı |
| **6 · Satürn** | Halka buzu: k 0,8 · Halka tozu: −%2 · Halka boşluğu · Enceladus gayzeri: +50 · Çoban uydu · Titan pusu: sürükleme ×3 · Altıgen fırtına · Halka dalgası | **Büyük Beyaz Leke:** 20 s kuyruk rüzgârı | Lüks gemi turları · Halka düzlemi |
| **7 · Uranüs–Neptün** | Metan buz bulutu: k 0,75 · Süpersonik rüzgâr: +8 b/s² **[D]** · Karanlık leke: −15 · Triton gayzeri: +40 · Yan yatık halka · Elmas yağmuru (kartta "tahmin" diye) **[D]** · Karanlık: görüş 120 b | **Büyük karanlık leke:** 15 s girdap | Buzul lojistik · Görüş eşiği |
| **8 · Plüton** | Azot buzu ovası: k 0,85 · Su buzu dağları: uyarılı · Metan karı: −%3 · Mavi pus · Charon sapanı: +40 · Kuiper nesnesi: trambolin | **Kalp:** final iniş mini oyunu | Rakip yok: final |

---

## 8. Mantık denetimi

### 8.1 Her hızlandırıcının enerji kaynağı (B1)

| Hızlandırıcı | Kazanç (sim) | Kaynak (görünür) | Sınır |
|---|---|---|---|
| Rampa | 70–230 × kalite | Rampanın itici sistemi | Turda 1 |
| Dalış | +14–54 | Roketin yakıtı (dalış hakkı) | Hak sayısı |
| Mükemmel sekme | +%10 | Dalışın yakıtı | En çok +12 b/s |
| Kademe ayırma | vy 78–130, vx +15–67 | Her kademenin kendi motoru | Kademe sayısı (1–3) |
| Son ateşleme | +19,5–78 | Yedek yakıt | Turda 1 |
| Yük dronu (S4) | +15 vy | Dronun bataryası (gösterge düşer) | Dron başına 1 (ömür 1) |
| H1 Havai fişek | (60–110) × 2,8 | Barut | Turda ≤ 5 fırsat, türler arası ≥ 6 s |
| H2 Konfeti topu | (45–95) × 2,8 × 0,7–1,2 | Basınçlı gaz tüpü | Aynı |
| H6 Römorkör | (40–80) × 4,5 | Römorkör yakıtı | y ≥ 1.500; tur sınırından muaf, aralık kuralına bağlı |
| C1 Termal | +8–16 b/s² yukarı | Güneşin ısıttığı yer | 3 s; yatay hız vermez |
| C2 Jet akımı | (12–18) × 3,5 × (1 − v/V) | Rüzgâr | v ≥ V iken 0 |
| U5 Leylek termalleri | +12 b/s² | Termaller | 3 s |
| U9 Şok dalgası | +80 | Göktaşının kinetik enerjisi | Turda 1 |
| Trambolin, kayma yüzeyi | 0 (yalnız yön) | — | k < 1 |
| U12 Balina | 0 (yön 10°) | — | Hız artmaz |

**Kod testi:** her çarpışma olayında giden hız büyüklüğü denetlenir (trambolin ≤ giriş × k_etkin + ek_vy; mükemmel ≤ giriş + 12; yavaşlatıcı < giriş); her itki bir kaynak kimliğine bağlanır, bağlanmayan artış testte hata verir.

### 8.2 Her çarpışmanın iki tarafı (B1)

| Çarpışma | Roket | Nesne |
|---|---|---|
| Martı grubu | −%6, 2° yukarı | Sersem, tüy, toparlanır |
| Balon, parti balonu | Trambolin | Çöker, patlar |
| Zeplin, sıcak hava balonu, rakip zeplini | Trambolin / yandan fren | Çöker, dalgalanır, söner; rakip yama alır |
| Yük dronu | Trambolin + 15 vy | Basılır, batarya düşer / parçalanır, paraşüt |
| Uçurtma, afiş | Fren | İp kopar, afiş yırtılır, uçak yalpalar |
| Radyosonde, kapsül | Küçük fren | Patlar / açılır, paraşüt |
| Kargo uçağı | Kademe kaybı ya da −%30 | Parçalanır, kargo paraşütleri |
| Uydu, çöp | Fren | Panel döner, bölünür, saçılır |
| Fişek, konfeti, römorkör | Hızlanır | Yakıtı/şarjı biter, geri tepme, uzaklaşır |
| Habitat, bilim balonu | Kayma / trambolin | Esner, manken/kutu sallanır |

### 8.3 Sömürü döngüsü sınırları

| Risk | Sınır |
|---|---|
| Sonsuz balon sekmesi | k < 1; aynı nesne 2 s içinde etki vermez; ömür 1–3 vuruş |
| Yüksekte asılı kalma | Tropopoz üstünde yatay hız 2 s < 110 → tur biter (`vx_dur`; PLAN_B §16 S1 önerisi: önce kademe) |
| Basamak gibi bilim balonu | y > 2.900'de yükselirken −6 b/s²; v < 600 iken y 300–3.500 ek sürükleme 0–7 b/s² |
| Uzun uçuşun kendini fırsatla beslemesi | Turda en çok 5 fırsat (römorkör hariç); türler arası ≥ 6 s |
| Dalış zinciri | Gösterge dolumu düşük (trambolin 0,08); hak sınırlı; bonus en çok +12 |
| Jet akımıyla sınırsız hızlanma | v ≥ V iken ivme 0 |
| Termalde asılı kalma | En çok 3 s, yatay hız vermez |
| Rakibe sonsuz hasar | Rampada turda 1; uçuşta S9 turda en çok 1 |
| Tur süresi | 65 s emniyet tavanı (turların ≤ %10'u çarpmalı) |

### 8.4 PLAN_B ile tutarsızlıklar

Taslak 1'deki 7 düzeltme (uydu mini sapanı, rotor akımı, kargo pilotu, su sütunu, Ay gazı, rampa yüksekliği, istasyon bidonları) PLAN_B 6.2'ye işlendi. Açık kalan tutarsızlık yok; römorkörün atmosferde (y 1.500, ~30 km) çıkması §10 S5'te.

---

## 9. Kararlaştırılanlar (KARARLAR.md)

Kapsül kartlarının üçü de kazanılır · her fırsatın kendi mini oyunu · B1 = ilk 25 tur (~24 nesne, 5 nadir olay, 6 fırsat) · evrensel ton · altın jeton · bilim balonu 40°, habitat 15° kayma yüzeyi · `vx_dur`, `firsat_tur_max`, dalış 14 → 54 · zayıf oyuncu dokunmadan da ilerler (ısı ~25, Kármán ~45).

---

## 10. Sorulacaklar (kullanıcıya)

**S1. Rakip karakterleri** (evrensel ton kararıyla Taslak 1'deki "komik Türk karakterleri" kalktı).
(a) Hayvan maskotlar: R1 kibirli tavus kuşu (balon turları), R2 telaşlı sincap (kargo), R3 dalgın baykuş (meteoroloji), R4 geveze papağan (telekom), R5 monokllü kedi (uzay holdingi). (b) Uluslararası çizgi film insan karikatürleri (kaptan, kargo müdiresi, profesör, reklamcı, baron), bıyık vb. yerel göstergeler olmadan. (c) Taslak 1'deki adlar kalır (Pofuduk, Koli, Pervane, Sinyal, Vakum), yalnız görünüş evrenselleşir. **Öneri: (a).** Küçük ekranda bir bakışta okunur, kültürden bağımsız, pilot maskotla tür olarak ayrışır. Adlar ve replikler seçimden sonra yazılır.

**S2. Dünyadaki reklam yazıları.** (a) Kısa Türkçe yazılar: zeplinde "PATLAMIŞ MISIR", afişte "BÜYÜK İNDİRİM!". (b) Yalnız simgeler (mısır kovası, yüzde işareti), yazı yok. **Öneri: (a).** Mizahı yazı taşıyor; yazılar kodla konur, dil dosyasından değişir.

**S3. Kaplama listesi** (Simit, Nazar boncuğu, Çay bardağı, Lokum çıktı): Donut, Gökkuşağı, Dondurma külahı, Şeker bastonu önerildi. (a) Onayla. (b) Başka tema (ör. uzay hayvanları). Kaplamalar B1 dışında olduğundan acil değil.

**S4. Meta sistemlerin B1 kapsamı** (görevler, bilgi kartı albümü, günlük hedefler, günün tohumu, hayalet, kaplamalar). (a) Hepsi B1 sonrası; B1 = çekirdek döngü + 25 tur içerik + rekorlar. (b) Görev setleri 1–11 B1'de, gerisi sonra. (c) Hepsi B1'de. **Öneri: (a).** Önce eğlence kanıtlanır; görevler BB'de de ikinci katman.

**S5. Römorkör atmosferde mi?** Sim'de römorkör y ≥ 1.500'de (~30 km) çıkıyor, yani Kármán'ın (100 km) altında. Yörünge turunu bu ayarlıyor. (a) Kalsın; adı "Yüksek irtifa römorkörü", görünüşü balonla asılı itici. (b) Yalnız uzayda (y ≥ 3.500) çıksın; sim'de `romorkor_y` 3.500 olur, yörünge muhtemelen 2–4 tur gecikir ve yeniden ayar gerekir. **Öneri: (a).**
