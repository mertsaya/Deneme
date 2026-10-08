# Son Durak: Plüton — İçerik Kitabı

Taslak 1 · 2026-10-08 · Dayanak: `PLAN_B.md` Taslak 6.1 · Durum: kullanıcı onayı bekliyor

Bu kitap, Dünya bölümünün bütün içeriğini (nesneler, nadir olaylar, fırsat nesneleri, rakipler, duvarlar, görevler, koleksiyon, hangar, ilerleme takvimi) uygulayıcının doğrudan koda dökebileceği sayılarla tanımlar. Diğer bölümler için yalnızca iskelet var.

**Sayılar hakkında.** Birimler PLAN_B §5 ile aynı: hız b/s, ivme b/s², mesafe b (1 b ≈ 1 m, 1 km = 1.000 b), yükseklik y (b). v_yörünge = 600, v_kaçış = 849. Para ₺ (1 izlenme = 1 ₺, kombo ve Yayın çarpanından önce). **Bütün sayılar ilk ayardır.** `~` işaretli olanlar tahmin; oyun testinde ilk oynanacak olanlar onlar. Sıklık "adet / km, nesnenin bandında" demek.

**Burrito Bison notu.** BB karşılıkları oyunun genel yapısına dayanıyor (fırlatma göstergesi, normal ve özel jöleler, roket dalışı, pasta duvarları, rakipler, piñata kartları). Tek tek jöle adlarını ve görev setlerinin tam biçimini web'de doğrulayamadım; o satırlar "BB'de benzeri" diye yazıldı, birebir iddia değil. Telif: BB'den isim, görsel ya da metin alınmaz (PLAN_B §11).

---

## 0. Genel kurallar (her nesne için geçerli)

| Kural | Değer |
|---|---|
| Çarpma yönü | **Üstten:** roket aşağı iniyor (vy < 0) ve nesnenin üst yarısına değiyor. **Yandan:** diğer her temas |
| Trambolin sekmesi | vy' = −k × vy (k nesneye göre 0,6–0,9; her zaman < 1). vx' = vx × (1 − yatay kayıp) |
| "−%X hız" | Hız vektörünün büyüklüğü %X azalır, yön değişmez (aksi yazılmadıkça) |
| Aynı nesneyle tekrar | Aynı nesne 2 s içinde ikinci kez etki ve ödül vermez (PLAN §3 kural 8) |
| Kombo | 3 s içinde art arda vuruş: ×1,1'den başlar, her vuruş +0,1, tavan ×3 (geliştirmeyle ×5) |
| Mükemmel sekme | Dalış bir trambolin nesnesine değerek biterse: o sekmede yatay kayıp yok, üstüne +%10 (en çok +25 b/s). Enerji kaynağı: dalış ateşlemesinin yakıtı |
| Sekme garantisi | Dalış menzilinde (roketin 250 b önü, 40–200 b altı) her an en az 1 trambolin nesnesi. Oluşturma anında test edilir |
| Hızlandırıcı arası | İki hızlandırıcı arasında en az 400 b (zincirleme sömürüyü keser) |
| Ölümcül arası | İki ölümcül nesne arasında en az 2 km; ölümcülün 300 b yakınında fren nesnesi yok; uyarı ≥ 1,2 s |
| Rampa | Kıyıdaki kayalık burnun tepesinde, **y = 60** (öneri; PLAN'da belirtilmemiş). 70 b/s, 38° kalkışla tepe ≈ y 91 |

**Sıklık sınıfları:** Yaygın 2–4/km · Ara 0,6–1,5/km · Seyrek 0,15–0,5/km · Nadir ≤ 0,1/km ya da tur başına olasılık.

**Yoğunluk bütçesi (ilk ayar):** Alçak bantta toplam ~12 nesne/km, bulutlarda ~9, üst atmosferde ~6, yörüngede ~5. Fırsat nesneleri bu bütçenin dışında, kendi sıklıklarıyla eklenir.

---

## 1. Dünya bölümü nesne kataloğu (38 nesne)

Bantlar: **A** alçak hava (25–250) · **B** bulutlar (250–700) · **Ü** üst atmosfer (700–1.500) · **Y** yörünge (1.500+).

### 1.1 Sekme nesneleri (trambolin) — 9

| # | Ad | Görünüş | Bant · sıklık | Rokete etkisi | Nesneye ne olur | Ödül | Açılış | Mantık gerekçesi | BB karşılığı |
|---|---|---|---|---|---|---|---|---|---|
| S1 | Şişme reklam balonu | Yuvarlak, gülen yüzlü, üstünde dondurma reklamı olan dev balon | A (40–200) · 3,0/km | Üstten: k 0,8, yatay −%2. Yandan: −%6 | 12 b çöker, sallanır; 3. vuruşta patlar, konfeti saçar (patlamış balon etki vermez) | 15 | Baştan | Hava dolu esnek zarf enerjiyi geri verir ama bir kısmını ısıya ve sallanmaya harcar | Normal jöle |
| S2 | Parti balonu salkımı | 20 renkli balon, ipinin ucunda kurdeleli hediye kutusu | A (30–150) · 2,0/km | Üstten: k 0,6, yatay −%1. Yandan: −%2 | Her vuruşta 6–8 balon patlar; 2. vuruşta salkım biter, kutu küçük paraşütle iner | 10 + kutudan 5–20 | Baştan | Küçük balonların kaldırma ve esnekliği az, bu yüzden zayıf trambolin | Küçük jöle |
| S3 | Reklam zeplini | Dev, tombul, yanında "SICAK SİMİT" yazan çizgili zeplin; insansız | A, B (80–500) · 1,2/km | Üstten: k 0,85, yatay −%3. Yandan: −%10 | Zarf 25 b çöker ve dalgalanır; 3. vuruşta söner, yamalı zarf yavaşça süzülerek iner | 40 | Baştan | Büyük, gergin zarf en iyi trambolin; yandan çarpınca kütlesi roketi frenler | İri jöle |
| S4 | Yük dronu | Dört pervaneli kutu dron, üstünde şişme kırmızı yastık; insansız | A, B (60–450) · 0,6/km | Üstten: k 0,8, yatay −%5, **+15 vy** (dron 0,3 s tam güç verir). Gövdeye yandan: −%25 | Üstten: 20 b aşağı basılır, batarya ışığı kırmızıya döner, yavaşça alçalıp ayrılır. Yandan: pervaneleri savrulur, gövde paraşütle iner | 60 | Tur 2 | +15 vy'nin kaynağı dronun bataryası, görünür batarya göstergesi düşer. (PLAN'daki "rotor akımı yukarı iter" düzeltildi: rotor akımı aşağı eser) | BB'de benzeri: zıplatan özel jöle |
| S5 | Sıcak hava balonu | Kırmızı-beyaz dilimli, sepetinde kum torbaları olan otomatik brülörlü reklam balonu; insansız | B (250–600) · 0,8/km | Zarf üstten: k 0,85, yatay −%2. Zarfa yandan: −%8. Sepete: −%15 | Zarf 20 b çöker; brülör korkuyla alev püskürtür (görsel); balon yavaşça döner. Sepete çarpılırsa kum torbası düşer | 30 | Tur 9 | Kumaş zarf esner; sepet sert, onun için fren büyük | İri jöle |
| S6 | Kargo paraşütü kubbesi | Kargo uçağının attığı paletlerin turuncu paraşütleri, 3–5'li grup | A, B · yalnız kargo uçağı (X1) geçtikten sonra | Üstten: k 0,75, yatay −%2 | Kubbe çöker; palet yedek paraşütle iner | 25 | Tur 6 | Gergin kumaş; tehlikenin hemen arkasından gelen ödül (tehlike–fırsat ikilisi) | — |
| S7 | Bilim balonu | Dev, ince, saydam stratosfer balonu; altında alet kutusu | Ü (700–1.400) · 1,0/km | Üstten: k 0,85, yatay −%1. Yandan: −%3 | İnce zarf dalgalanır, alet kutusu sallanır | 30 + %10 kart parçası | Tropopoz eşiği (y 700) sonrası | Yüksekte hava ince, yatay sürtünme az | — |
| S8 | Şişme habitat modülü | Kumaş görünümlü, beyaz, tombul uzay modülü; içinde sallanan test mankeni | Y (1.500–2.200) · 0,5/km | Üstten: k 0,9, yatay −%2 | Esner, yavaşça döner; manken pencereye yapışır | 60 | Kármán çizgisi (y 1.500) sonrası | Gerçek şişme modüllerden esinli; g_etkin ≈ 0 olduğu için k yüksek ama yine < 1 | — |
| S9 | Rakip zeplini (uçuşta) | Sıradaki rakibin renklerinde, yamalı zeplin | A, B · tur başına %30, en çok 1 | Üstten: k 0,85, yatay −%3. Yandan: −%10 | Rakibe **+25 hasar** (×zeplin hasarı geliştirmesi); kaptan pencereden yumruk sallar | 50 | Rakip 1'den itibaren | Rampadaki zeplinin aynısı; hasarı turlar arası taşınır | Ringdeki rakip |

### 1.2 Yavaşlatıcılar — 10

| # | Ad | Görünüş | Bant · sıklık | Rokete etkisi | Nesneye ne olur | Ödül | Açılış | Mantık gerekçesi | BB karşılığı |
|---|---|---|---|---|---|---|---|---|---|
| Y1 | Martı sürüsü | 5–9 tombul, şaşkın bakışlı martı | A (25–180) · 3,0/km | Martı başına −%3; yön 2° yukarı döner (toplam hız artmaz) | Sersemler, tüyleri uçar, takla atar, toparlanıp uçar | 10 / martı | Baştan | Hafif nesne savrulur, roket az yavaşlar | Normal jöle |
| Y2 | Uçurtma | Baklava biçimli, kuyruklu, yerden ince ipiyle bağlı | A (40–220) · 1,5/km | Gövde: −%2. İp: −%15 (0,3 s takılma) | İp kopar, uçurtma savrulup süzülür | 6 | Baştan | Gergin ip kopana kadar roketi geri tutar | Engelleyici jöle |
| Y3 | Afiş çeken uçak | Uzaktan kumandalı küçük pervaneli uçak, arkasında "BAYRAMDA KAMPANYA" afişi | A (60–200) · 0,4/km | Afiş: −%35 (0,5 s sürüklenir). Gövde: −%12 | Afiş yırtılır; uçak yalpalayıp yoluna devam eder | 25 | Tur 4 | Afiş geniş kumaş, sürtünme büyük; uçak hafif, savrulur | Polis jöleleri |
| Y4 | Radyosonde | Küçük beyaz meteoroloji balonu, altında sallanan kutu | A, B (50–700) · 1,0/km | −%2 | Balon patlar, kutu küçük paraşütle iner | 8 + **%15 bilgi kartı parçası** | Tur 5 | Hafif; gerçek hava gözlem balonu, veri kutusu bilgi kartı taşır | — |
| Y5 | Sığırcık bulutu | Şekil değiştiren dev kara kuş bulutu (~300 kuş) | A (80–250) · 0,25/km | İçinden geçerken her 0,1 s −%1 (ortalama toplam −%12) | Kuşlar ikiye ayrılıp roket biçiminde boşluk açar, sonra yeniden birleşir | 2 / kuş (kombo doldurur) | Tur 16 | Çok sayıda hafif nesne, toplamda belirgin fren; kuşlara çarpma yok, kaçışıyorlar | — |
| Y6 | Göktaşı tozu izi | Gökte ince, parıltılı turuncu çizgi | Ü (900–1.500) · 0,8/km | −%5, ısı +5 | Kıvılcım saçılır, iz dağılır | 20 | Tropopoz sonrası | Toz parçacıkları sürtünme ve ısı yaratır | — |
| Y7 | Gece parlayan bulut | Elektrik mavisi, dalgalı, ince buz bulutu şeridi | Ü (1.100–1.400) · şerit, 0,5/km | −%3, **ısı −20** | Bulut roket izinde aralanır | 15 | Tropopoz sonrası | Buz kristali hafif frenler ama soğutur; ısı yönetimi için tercih edilen fren | — |
| Y8 | Volkanik kül bulutu | Gri, kabarık, içinde kıvılcımlar olan bulut | B (300–650) · 0,15/km | −%6; içinde ve 2 s sonrasına kadar dalış göstergesi dolmaz | Bulut roketin arkasında girdap yapar | 20 | Tur 15 | Kül motoru tıkar; görünür ve önceden belli, kaçınılabilir | — |
| Y9 | Uydu | Altın folyolu kutu, iki mavi güneş paneli; insansız | Y (1.600–2.400) · 1,0/km | Panel sürtme: −%4. Gövde: −%20 | Panel fırıldak gibi döner, bazen kopup sürüklenir; gövde yörüngeden sapar | 50 | Kármán sonrası | **PLAN'daki "uydu mini sapanı" kaldırıldı:** uydunun kütlesi rokete hız veremez. Hız kaynağı rolünü fırsat nesnesi Uzay römorkörü (F10) aldı | — |
| Y10 | Uzay çöpü | Somun, eldiven, boya pulu, kırık panel parçası | Y (1.500–3.000) · 2,0/km | −%8 | Çarpılan parça ikiye bölünür, parçalar ayrı yönlere savrulur (bunlara çarpmak −%3) | 15 | Kármán sonrası | Momentum paylaşılır: roket frenlenir, parça hızlanıp dağılır | — |

### 1.3 Hızlandırıcılar — 6 (+ 3 bant, §1.6)

Fırsat nesneleri (satın alınınca çıkar) §3'te ayrıntılı. Burada dünyadaki davranışları.

| # | Ad | Görünüş | Bant · sıklık | Rokete etkisi | Nesneye ne olur | Enerji kaynağı | Ödül | Açılış | BB karşılığı |
|---|---|---|---|---|---|---|---|---|---|
| H1 | Havai fişek roketi | Çizgili, kocaman, fitili tüten çubuklu fişek | A, B · §3 | Tutunursun: 1,2 s yukarı-ileri (35°) itiş, toplam +60 | Yakıtı bitince havada patlayıp çiçek gösterisi yapar | Fişeğin barutu | 40 | Satın al (F2) | Roketli özel jöle |
| H2 | Konfeti topu dronu | Dronun altında asılı, ağzı yıldız şeklinde pembe top | A, B · §3 | Top döner, dokunuşla ateşler: +45, seçilen açıda | Geri tepmeyle dron 30 b geriye savrulur, konfeti yağar | Topun basınçlı gaz tüpü | 35 | Satın al (F3) | Bombalı/patlayan özel jöle |
| H3 | Sapan dronu | İki dron arasında gerili dev yeşil lastik | A, B · §3 | Lastiğe girersin, gerilir, dokunuşla bırakır: giriş hızı × 0,9 + 70 | Dronlar içe doğru çekilir, sonra sallanarak toparlanır | Dronların önceden gerdiği lastik (gerginlik görünür: dronlar eğik, lastik titrek) | 50 | Satın al (F5) | BB'de benzeri: fırlatıcı özel jöle |
| H4 | Tanker dronu | Göbekli, gri, arkasından uzun hortum sarkan dev dron | B · §3 | Hortuma bağlanırsın: dalış hakları dolar, motor 1,0 s ateşler +50 | Tanker yakıt göstergesi düşer, "boş" lambası yanar, uzaklaşır | Tankerin yakıtı, roketin kendi motorunda yanar | 80 | Satın al (F7) | — |
| H5 | Su roketleri | Okul bilim fuarı: yerden yükselen 3'lü pet şişe roket grubu | A (25–200, yukarı doğru gider) · 0,5/km | Alttan çarparsa vy +25 (yatay değişmez). Üstten çarparsa −%3 | Şişe takla atar, su püskürtür, minik paraşütü açılır | Şişedeki basınçlı hava ve su | 15 | Tur 3 | — |
| H6 | Uzay römorkörü | Turuncu, kepçe burunlu, mıknatıs kollu küçük insansız uzay aracı | Y · §3 | Kenetlenir, 2 s iter: +40, yönü dokunuşla seçilir | Yakıtı biter, römorkör geri döner, el sallar gibi kolunu açar | Römorkörün yakıtı | 120 | Satın al (F10) | — |

### 1.4 Toplanabilirler — 5

| # | Ad | Görünüş | Bant · sıklık | Rokete etkisi | Nesneye ne olur | Ödül | Açılış | Mantık gerekçesi | BB karşılığı |
|---|---|---|---|---|---|---|---|---|---|
| T1 | Yakıt dronu | Sarı bidon taşıyan küçük dron | A, B · §3 | +1 dalış hakkı | Bidonu bırakır, sallanarak uzaklaşır | 20 | Satın al (F1) | Dalış = yakıt; bidon yakıt | Ek dalış veren özel jöle |
| T2 | Altın martı | Sponsor yelekli, güneş gözlüklü, parıltılı martı | A · 0,05/km | −%3 (normal martı gibi) | Sersemler, yeleğinden altın simli konfeti dökülür | **150** | Tur 7 | Sponsorun maskotu; ödül sponsor parası, fizik normal martıyla aynı | Nadir altın jöle (BB'de benzeri) |
| T3 | Yayın dronu | Kocaman tek kameralı, kırmızı "CANLI" ışıklı dron | A, B, Ü · §3 | Fizik etkisi yok; "poz ver" → izlenme ×2, 5 s | Kamera dönüp seni takip eder | Çarpan | Satın al (F9) | Kamera = izlenme. Çarpışma yok, yanından geçilir (kural 4: görünür sebep) | — |
| T4 | Kargo kapsülü | Paraşütlü, çizgili, "KIRILIR" etiketli kapsül (piñata) | Her bant · tur başına %35 | −%4 | Açılır, 3 kart fırlar, kapsül paraşütle iner | 3 kart (§4.6) | Tur 3 | Hafif kapsül; içi sponsor hediyesi | Piñata |
| T5 | Rakip tanıtım balonu | Sıradaki rakibin yüzü basılı küçük balon, 3'lü | A, B · 0,4/km (rakip olduğu sürece) | Üstten: k 0,7 (küçük trambolin) | Patlar, rakip yüz ifadesi "aaa!" | 10 + **rakibe hasar** (§4.1) | Rakip 1'den itibaren | Rakibin reklamını patlatmak onu küçük düşürür; hasar mizahi | — |

### 1.5 Tehlikeler (seyrek, uyarılı, adil) — 3

| # | Ad | Görünüş | Bant · sıklık | Uyarı | Rokete etkisi | Nesneye ne olur | Ödül | Açılış | Mantık gerekçesi |
|---|---|---|---|---|---|---|---|---|---|
| X1 | Kargo uçağı | Kocaman, tombul, "HIZLI KARGO" yazılı insansız kargo uçağı | B (300–600) · 0,12/km | Kenar oku + motor uğultusu 1,5 s önce | Gövdeye çarpma: **patlama, tur sonu** (Zırh varsa atlatılır). Kanat ucu: −%30. Arkasından 150 b içinde geçmek: 3 s **sürükleme −%50** (rüzgâr gölgesi) | Çarpmada: gövde ikiye ayrılır, kanatlar savrulur, yakıt tankı gecikmeli patlar, 3–5 kargo paraşütü (S6) açılır | 200 | Tur 6 | Ağır nesne her iki tarafı da parçalar; insansız olduğu için kimse yaralanmaz. Rüzgâr gölgesi enerji vermez, yalnızca kaybı azaltır |
| X2 | Sondaj roketi | İnce, beyaz, burnunda "METEOROLOJİ" yazan, dikine yükselen küçük roket | A, B · 0,15/km | Yerden duman sütunu + kesişme çizgisi 1,5 s önce | −%25, **vy +20** (onun motoru seni yukarı iter) | Takla atar, motoru söner, paraşütü açılır | 60 | Tur 11 | İki roketin çarpışması: ikisi de sapar. Yukarı itme onun yakıtından |
| X3 | Ölü üst kademe | Dev, paslı, yavaşça kendi etrafında dönen silindir | Y · 0,1/km | Kırmızı üçgen işaret + yörünge çizgisi 2 s önce | Gövdeye çarpma: **patlama, tur sonu** (Zırh atlatır). Sürtme: −%25 | Çarpılınca yörüngesinden sapar, 4 parça çöp (Y10) saçar | 250 | Tur 24 | Ağır, sabit gibi davranan kütle; her çarpma yeni çöp üretir (iki taraf) |

### 1.6 Çevresel bantlar — 5

| # | Ad | Görünüş | Bant · sıklık | Rokete etkisi | Nesneye ne olur | Enerji kaynağı | Ödül | Açılış | Mantık gerekçesi |
|---|---|---|---|---|---|---|---|---|---|
| C1 | Termal sütun | Titreşen sıcak hava sütunu, içinde döne döne yükselen yapraklar ve 2–4 leylek | A (25–250), 120 b genişlik · §3 | İçindeyken +8 b/s² yukarı | Leylekler kanat çırpmadan yükselir | Güneşin ısıttığı kara | 3/s | Satın al (F4) | Sütun sonlu, en çok 3 s kalınabilir (üstünden çıkarsın); yatay hız vermez |
| C2 | Jet akımı | Gök boyunca akan, beyaz çizgili rüzgâr nehri | B (400–650), 60 b kalınlık, 1,5 km uzunluk · §3 | İleri ivme = 12 × (1 − v / V_rüzgâr), V_rüzgâr 180 b/s; v ≥ V ise etki yok | Çizgiler roket etrafında kıvrılır | Atmosferin rüzgâr enerjisi | 5/s | Satın al (F6) | **Rüzgâr seni kendi hızından hızlı itemez**: formül bunu garanti eder |
| C3 | Dalga bulutu | Üst üste dizilmiş uçan daire biçimli düz bulutlar (merceksi) | B (300–650) · §3 | Bulutun önünde (rüzgâr üstü) +14 b/s² yukarı, arkasında −6 b/s² | Bulut dalgalanır | Dağ üstünden aşan rüzgârın dalgası | 4/s | Satın al (F8) | Gerçek planör tekniği; ön tarafı fırsat, arka tarafı bedel |
| C4 | Rüzgâr tabakası | Yatay akan ince bulut çizgileri; ok yönü rüzgârın yönü | A, B · 0,6/km (%60 karşı, %40 kuyruk) | Kuyruk: +4 b/s² ileri (V_rüzgâr 120 sınırı, C2 formülü). Karşı: −6 b/s² | — | Rüzgâr | 0 | Ses duvarı sonrası | Görünür çizgiler önceden yönü söyler; karşı rüzgâr bilinçli bir fren |
| C5 | Fırtına hücresi | Örs tepeli dev kara bulut, içi çakan | B (250–700) · 0,2/km | Merkezde yukarı akım +20 b/s²; kenarlarda aşağı akım −15 b/s². Yıldırım (bulutta en çok 1): 0,8 s dalış kilidi | Bulut çakar, gök gürler | Bulutun içindeki sıcak nemli hava | 25 (yıldırım: 40) | Tur 8 | Gerçek fırtına bulutunun dikey akımları; risk (kenar) + fırsat (merkez). Yıldırım 0,6 s önce bulut içi parlamayla uyarır |

**Toplam:** 9 sekme + 10 yavaşlatıcı + 6 hızlandırıcı + 5 toplanabilir + 3 tehlike + 5 çevresel bant = **38**.

### 1.7 İlk turun senaryosu (tohum sabit, "vay" ≤ 5 s)

| Zaman | Olay |
|---|---|
| 0,0 s | Geri sayım biter, gösterge iğnesi sarkaç gibi gidip gelir. İpucu: "Yeşilde dokun" |
| ~1,0 s | Mükemmel kalkış: roket rakip zeplininin gondoluna çarpar, kaptan Pofuduk'un şapkası uçar, +91 hasar |
| 2,5 s | 7 martılık sürüye dalış: tüy patlaması, 7 × "+10" sayısı, kombo ×1,7 |
| 4,0 s | **"Vay" anı:** dev reklam zepliniyle ilk sekme; roket ekranın üstüne kadar fırlar, zeplin dalgalanır. İpucu: "Dalış için dokun" (gösterge yarı doldu) |
| 6–10 s | Balon zinciri, uçurtma ipi, ilk dalış ve ilk mükemmel sekme |
| ~12 s | Hız düşer, y < 25: **SON ŞANS**, boş kademe paraşütle ayrılır, roket 50° yukarı fırlar |
| ~18 s | Kapsül paraşütle tarlaya iner, kamyonet gelir. Kara kutu: ~120 ₺, "Rampa gücü 60 ₺" kartı |

---

## 2. Nadir (unique) olaylar — 12

**Kural:** bir turda en fazla bir nadir olay. Her turun başında olasılık zarı: taban **%25**, "Sansasyon" geliştirmesiyle +%5/sv (en çok %50). **Acıma sayacı:** 4 tur üst üste nadir olay çıkmadıysa sonraki turda garanti. Hangi olayın seçileceği, koşulu sağlananlar arasında ağırlığa göre. İlk kez görülen her olay bir bilgi kartı ve "Nadir Albüm"e bir sayfa verir. Olay, roketin o anki bandına göre önünde 1,5 km mesafede kurulur ve 2 s önceden kenar ışığıyla duyurulur ("SICAK HABER!").

| # | Olay | Ne görürsün | Oynanış | Koşul · ağırlık | İlk kez garanti | Ödül | Mantık gerekçesi |
|---|---|---|---|---|---|---|---|
| U1 | Dev geçit töreni balonu | Bağlarından kopmuş 60 b'lik şişme dev kedi "Pamuk", ayaklarından sarkan 6 halat | Sırtında 5 sekmeye kadar: k 0,9, yatay kayıp yok; her sekmede kedi "miyav" der, kulakları sallanır. Halatlar: −%10 | A, B · 10 | Tur 5 | 5 × 100 + 500 | Festivalden kopmuş, insansız. Sonra itfaiye dronları gelip halatlarından çeker (görünür son) |
| U2 | Hava gösteri filosu | 7 insansız akrobasi dronu V düzeninde, arkalarında kırmızı-beyaz duman | Arkalarındaki koridorda 4 s **sürükleme −%60**; ortasından geçersen dronlar ikiye açılıp duman kalbi çizer | A, B · 10 | Tur 7 | 600 + ×1,5 izlenme 6 s | Rüzgâr gölgesi enerji vermez, yalnızca kaybı azaltır |
| U3 | Gökyüzü fenerleri | Yüzlerce turuncu dilek feneri, alttan yükselen ışık nehri | Her fener −%0,3, +3 ödül; kombo zamanlayıcı fenerlerde durmaz → dev kombo | A · 8 | Tur 10 | ~150–400 | Hafif kâğıt fenerler, sıcak hava; toplam fren küçük. Sömürü sınırı: en çok 120 fener |
| U4 | Uçan daire şakası | Parlayan, dönen, ışıklı disk; içinde yeşil kostümlü manken | Disk üstü trambolin (k 0,9) × 3; 3. vuruşta söner, içinden "UFO DEĞİL, KAMPANYA!" afişi çıkar | B · 6 | Tur 14 | 800 + kart | Rakip ajansın reklam dublörü: disk biçimli zeplin. Mantık: aslında S3'ün kostümlüsü |
| U5 | Leylek göçü | Termal sütunlarda döne döne yükselen 40 leylek, dev sarmal | 3 termal yan yana, her biri +12 b/s²; leyleklere çarpmamak için ortadan geç, çarparsan leylek sersemler (−%2) | A, B · 8 (yalnız ilkbahar ve sonbahar aylarında ağırlık ×2, cihaz tarihine göre) | Tur 12 | 400; hiç leyleğe çarpmazsan +400 | Gerçek: leylekler termallerle süzülür; termal varlığını leylekler gösterir |
| U6 | Güneş tutulması | Gök 10 s kararır, Ay'ın gölgesi akar, yıldızlar ve Güneş tacı görünür | Fizik değişmez; izlenme ×2, 10 s | Her bant · 4 | Tur 18 | ×2 çarpan + kart | Herkes gökyüzüne bakıyor, yayın patlıyor |
| U7 | Rakip roket yarışı | Sıradaki rakibin insansız yarış roketi yanına gelir, kaptan ekrandan dil çıkarır | 8 s yarış; sonunda öndeysen kazanırsın. Birbirinize değerseniz eşit kütle: hız farkı paylaşılır (ikiniz de seker) | B, Ü · 8 | Tur 16 | Kazanırsan 1.000 + rakibe 150 hasar | İkisi de kendi yakıtıyla uçuyor; çarpışma momentumu paylaşır |
| U8 | Güneş enerjili dev kanat | 80 b kanat açıklığı, ince, kibrit çöpü gibi güneş uçağı; insansız | Kanadın üstünde "kanat sörfü": 3 ardışık sekme, k 0,85, yatay −%1 | Ü · 6 | Tur 20 | 3 × 120 + kart | Gerçek yüksek irtifa güneş uçaklarından; kanat esnek, yavaş uçar, sekince salınır |
| U9 | Meteor yağmuru | 12 göktaşı izi gökyüzünü çizer, sonunda dev bir ateş topu | Ateş topu arkadan yetişir (1,5 s uyarı): şok dalgası **+80** ileri, ısı +20. Küçük izler Y6 gibi | Ü · 6 | Tur 22 | 900 + kart | Göktaşı rokettan çok daha hızlı; şok dalgası onun kinetik enerjisinden pay |
| U10 | Kuzey ışıkları fırtınası | Gök yeşil-mor perdelerle dalgalanır | İzlenme ×2, 8 s; uydular 8 s kontrol kaybeder (yörüngede sürüklenir, yerleri değişir) | Ü, Y · 5 | Tur 26 | ×2 + kart | Güneş fırtınası: gerçek, uyduları etkiler |
| U11 | Uzay istasyonu | Panelleri ışıldayan dev istasyon, pencereden el sallayan astronot | Yanından 200 b'den yakın geçersen robot kol 2 yakıt bidonu fırlatır: **+2 dalış hakkı**. Gövdeye çarpmak: −%40 (patlama yok, istasyon kalkanı çöker) | Y · 10 | Tur 25 | 1.500 + kart + "Selfi" rozeti | Dalış hakkının kaynağı istasyonun yakıt bidonu |
| U12 | Kayıp balina zeplini | Mavi, kuyruğunu sallayan dev balina biçimli eski zeplin, üstünde "1. Hava Festivali" yazısı | 7 sekmeye kadar sırtında; kuyruk sallaması sekme yönünü 10° ileri çevirir (hız artmaz) | B · 3 | — (tamamen rastgele) | 7 × 120 + kaplama parçası | Eski festival zeplini; kuyruk yön çevirir, enerji eklemez |

---

## 3. Satın alınabilir fırsat nesneleri — 10

Her fırsatın üç çizgisi var: **Aç** (tek seferlik), **Sıklık** (4 sv), **Güç** (5 sv). Fiyat = taban × 1,55^seviye (PLAN §7). Fırsat nesnesine çarpınca 90 ms duraksama ve ×0,4 ağır çekim (0,3 s); etkileşimli olanlarda **dokunma halkası** belirir: halka içindeyken dokunuş dalış yerine o nesnenin eylemini yapar (renk: turkuaz daire, PLAN §11 renk körlüğü kuralı).

| # | Fırsat | Aç | Sıklık (0 → 4 sv) · taban | Güç (0 → 5 sv) · taban | Oyuncunun hareketi (tek dokunuş) | Dokunmazsan |
|---|---|---|---|---|---|---|
| F1 | Yakıt dronu (T1) | 150 ₺ · Tur 2 | 0,3 → 0,9/km (+0,15) · 100 | sv0: +1 dalış; sv2: +1 ve gösterge +%25; sv4: +2; sv5: +2 ve gösterge +%50 · 120 | Yok, çarpman yeter. Bidon düşerken dalışla yakalarsan +%25 gösterge | — |
| F2 | Havai fişek roketi (H1) | 300 ₺ · Tur 3 | 0,2 → 0,6/km (+0,1) · 150 | +60 → +110 (+10/sv), süre 1,2 → 1,7 s · 160 | **Erken patlat:** tutunurken dokun. Son %25'lik yeşil pencerede dokunursan kalan itki tek seferde ×1,25 verilir ve fişek arkanda çiçek açar. Erken (yeşil öncesi) dokunursan kalan itki ×0,8 | Fişek kendi bitince bırakır (tam itki, bonus yok) |
| F3 | Konfeti topu dronu (H2) | 450 ₺ · Tur 6 | 0,2 → 0,6/km · 180 | +45 → +95 (+10/sv) · 200 | **Nişan:** top 10°–60° arası sarkaç gibi döner (dönem 0,8 s); dokunduğun açıda ateşler. 25°–35° "mükemmel" = ×1,2 | 0,8 s sonra 30°'de ×0,7 güçle ateşler |
| F4 | Termal sütun (C1) | 400 ₺ · Tur 8 | 0,3 → 0,9/km · 150 | +8 → +16 b/s² (+1,6/sv), en çok kalma 3 → 4 s · 170 | Yok (bant). Sütunda dalış yapmak sütundan çıkarır; doğru an: tepeye yakın çık, sonra dal | — |
| F5 | Sapan dronu (H3) | 900 ₺ · Tur 12 | 0,15 → 0,45/km · 250 | +70 → +120 (+10/sv) · 300 | **Bırak:** lastik 0,6 s gerilir, gerginlik göstergesi dolar; tam dolduğu 0,15 s'lik pencerede dokun = tam güç. Erken: +%55 güç | Lastik 0,6 s sonra kendiliğinden bırakır: +20 ve giriş hızı × 0,9 |
| F6 | Jet akımı (C2) | 1.200 ₺ · Tur 11 | Tur başına 1 → 3 akım (+0,5) · 300 | V_rüzgâr 180 → 300 (+24/sv), ivme katsayısı 12 → 18 · 350 | Bantta kalmak: 60 b kalınlıktaki akımdan düşmemek için sekme ve dalışları zamanla | — |
| F7 | Tanker dronu (H4) | 2.000 ₺ · Tur 15 | 0,1 → 0,3/km · 400 | +50 → +100 (+10/sv), ateşleme 1,0 → 1,5 s · 450 | **Bağlan:** hortum ucu sallanır; uç 40 b halkasına girdiğinde dokun → kenetlenir. Iskalarsan dokunuş normal dalış olur | Halkadan geçip gidersin, etki yok |
| F8 | Dalga bulutu (C3) | 1.500 ₺ · Tur 13 | 0,3 → 0,8/km · 300 | +14 → +24 b/s² (+2/sv) · 320 | Yok (bant). Ön tarafta kal, arka tarafa düşme | — |
| F9 | Yayın dronu (T3) | 600 ₺ · Tur 9 | 0,3 → 0,9/km · 150 | Çarpan ×2 → ×3 (+0,2/sv), süre 5 → 8 s · 200 | **Poz ver:** kamera halkasındayken dokun → roket takla atar, kamera flaşı | Geçip gidersin, ×1,3 küçük çarpan |
| F10 | Uzay römorkörü (H6) | 5.000 ₺ · Tur 21 | 0,15 → 0,45/km · 800 | +40 → +80 (+8/sv), itiş süresi 2 → 3 s · 900 | **Yön seç:** kenetlenince itme oku 0°–40° arası sarkaç gibi döner; dokunduğun yönde iter (alçalmak ya da yükselmek senin kararın) | 0,8 s sonra 10°'de iter |

**Fırsatların toplam maliyeti (aç + tam seviye):** ≈ 92.000 ₺ (~). Dünya bölümünde oyuncunun yaklaşık yarısını tam seviyeye çıkarması beklenir; gerisi Ay bölümünde de çalışır (ortak fırsatlar).

---

## 4. Süreklilik sistemleri

### 4.1 Rakip ajanslar (rampadaki zeplin)

**Hasar formülü:** H = v_kalkış × kalite × (1 + 0,15 × Zeplin hasarı sv). Kalite: mükemmel 1,0 · iyi 0,4 · zayıf 0. Uçuşta: rakip zeplini (S9) +25, tanıtım balonu (T5) +15, rakip yarışı (U7) +150, "zayıflık" nesnesi (aşağıda). Hasar turlar arası birikir, zeplinde yama sayısıyla görünür (her %20'de bir yama, PLAN §3 kural 5). Nakavt: zeplin söner, fırıldak gibi uçup gider, kaptan paraşütle iner ve yumruk sallar; sıradaki rakip bir sonraki turda gelir.

| # | Rakip | Ajans · zeplin | Kişilik (tek replik) | Can | Zayıflığı (uçuşta, ek hasar) | Nakavt ödülü | Beklenen nakavt |
|---|---|---|---|---|---|---|---|
| R1 | Kaptan Pofuduk | Pofuduk Balon Turları · pembe-beyaz çizgili, püsküllü | Kendini beğenmiş, kalın bıyıklı balon turizmcisi. "Bıyığıma dokunma!" | 450 | Pembe tanıtım balonları: +15 (×1,5 bu rakipte) | 500 ₺ + Konfeti topu dronu bedava açılır | Tur 6–7 |
| R2 | Madam Koli | Hızlı Kargo Havayolları · koli bantlı kahverengi zeplin | Telaşlı, her şeye etiket yapıştırır. "Bu zeplin İADE!" | 1.600 | Kargo paletleri (S6): +30 | 1.500 ₺ + Kapsül sıklığı +1 sv bedava | Tur 13–14 |
| R3 | Profesör Pervane | Pervane Meteoroloji Enstitüsü · beyaz, anten dolu, dönen fırıldaklı zeplin | Dalgın bilim insanı, sürekli hesap yapar. "Hesaplarıma göre... AH!" | 3.500 | Radyosonde (Y4): +40 | 4.000 ₺ + Dalga bulutu bedava açılır + 3 bilgi kartı | Tur 21–22 |
| R4 | Bayan Sinyal | Şimşek Telekom · gümüş, çanak antenli, yanıp sönen ışıklı zeplin | Hızlı konuşan reklamcı, cümle bitirmez. "Kampanyamız şu an ŞU AN—" | 6.000 | Uydular (Y9): +60 | 8.000 ₺ + Uzay römorkörü %50 indirim + kaplama | Tur 29–30 |
| R5 | Baron Vakum | Vakum Uzay Holding · siyah-altın, monokl gözlü dev zeplin "Kibir" | Tepeden bakan milyarder; yenilince ilk kez gülümser. "Uzay benim... galiba değil." | 10.000 | Kendi altın reklam uydusu (her turda 1, Y bandında): +200 | 15.000 ₺ + Ay üssü kurulumu bedava + "Baron" kaplaması | Tur 38–39 |

Her rakip ilk gelişinde 2 s'lik giriş sahnesi (atlanabilir), her mükemmel kalkışta tepki animasyonu (şapka, monokl, bıyık uçar), nakavtta 3 s sahne.

### 4.2 Hız duvarları, eşikler ve bölgeler

Burrito Bison'un pasta duvarları gibi, ama gerçek eşikler: 3 hız duvarı + 2 irtifa eşiği + kaçış. **İlk kırılış** büyük ödül ve sinematik (PLAN §9: 300 ms duraksama, ×0,2 ağır çekim); sonraki kırılışlarda ödülün %10'u.

| Eşik | Koşul | Sinematik | İlk ödül | Sonraki | Açtıkları | Beklenen ilk kırılış |
|---|---|---|---|---|---|---|
| Ses duvarı | v 100 → 115'i geç (Cd tepesi) | Şok konisi, "BUM", camlar titrer (arka planda tarlada inek şaşırır) | 300 ₺ | 30 | Bölge 2, rüzgâr tabakası | Tur 3 |
| Tropopoz eşiği | y ≥ 700 | Bulutlar aşağıda kalır, gök bir ton koyulaşır | 600 ₺ | 60 | Üst atmosfer nesneleri | Tur 9–10 |
| Isı duvarı | v ≥ 260 ve ısı < 100'ken 1 s | Burun kızarır, plazma halesi, sonra soğuma buharı | 1.500 ₺ | 150 | Bölge 3 | Tur 10–12 |
| Kármán çizgisi | y ≥ 1.500 | Gök siyaha döner, sesler bir anlığına kesilir | 3.000 ₺ | 300 | Yörünge nesneleri | Tur 18–19 |
| Yörünge hızı | v ≥ 600 | Roket süzülür, ufuk kavislenir, yıldızlar yanar; telsiz: "Yörüngedeyiz!" | 6.000 ₺ | 600 | Bölge 4, uzay istasyonu | Tur 25 |
| Kaçış hızı | v ≥ 849 | Dünya küçülür, Ay büyür; 3 s geçiş sahnesi | 15.000 ₺ | — | Ay bölümü | Tur 40 |

**Bölgelerin kimliği** (hızla değişir; PLAN §5 ile tutarlı):

| Bölge | Hız | Gök ve görünüş | Müzik katmanı | Ortam olayı | Baskın nesneler |
|---|---|---|---|---|---|
| 1 · Sabah Kıyısı | 0–100 | Açık mavi, pamuk bulutlar, aşağıda kıyı, tarlalar, deniz feneri | Akustik ritim + el çırpma | Balon festivali (S1, S2 yoğun) | Martı, balon, uçurtma, zeplin |
| 2 · Bulut Denizi | 100–250 | Bulutların üstü, altın güneş, bulut üstünde gölgenin etrafında gökkuşağı halkası | + Synth bas | Bulut tepelerinde sıcak hava balonları | Sıcak hava balonu, kargo uçağı, jet akımı, fırtına |
| 3 · Lacivert Tavan | 250–600 | Lacivertten siyaha, ufuk kavisli, ince mavi atmosfer çizgisi | + Koro pad | Gece parlayan bulutlar, göktaşı izleri | Bilim balonu, göktaşı izi, sondaj roketi |
| 4 · Sessiz Yörünge | 600–849 | Siyah, yıldızlar, altta mavi Dünya | Bütün katmanlar düşer, piyano; efektler telsiz sesine döner (uzayda ses yok şakası) | Gün doğumu çizgisi geçer | Uydu, çöp, habitat, römorkör, ölü kademe |

### 4.3 Görevler (36 görev, 12 set)

Aynı anda 3 görev (bir set) görünür. Set bitince **rütbe** artar ve kalıcı **+%2 izlenme** (12 set: +%24). Görev tek tek tamamlanır, ilerleme turlar arası saklanır ("tek turda" yazanlar hariç). Hiçbir görev ceza ya da zaman sınırı içermez.

| Set · rütbe | Görev 1 | Görev 2 | Görev 3 | Görev ödülü (her biri) |
|---|---|---|---|---|
| 1 · Stajyer | Mükemmel kalkış yap | 5 balondan sek (toplam) | 1 km uç | 50 ₺ |
| 2 · Çaylak Pilot | Tek turda 10 martı sersemlet | Bir dalışı mükemmel sekmeyle bitir | Son şanstan sonra 500 b daha uç | 80 ₺ |
| 3 · Pilot | Ses duvarını kır | Bir zeplini söndür (3 vuruş) | ×1,5 komboya ulaş | 150 ₺ |
| 4 · Kıdemli Pilot | Uçurtma ipine ve afişe takılmadan 3 km uç | Kargo kapsülü aç | 3 mükemmel sekme art arda | 250 ₺ |
| 5 · Gösteri Pilotu | Havai fişekte "erken patlat" bonusu al | Kaptan Pofuduk'u nakavt et | Tek turda 30 s havada kal | 400 ₺ |
| 6 · Kargo Avcısı | Kargo uçağının 60 b yakınından çarpmadan geç | 3 radyosonde patlat (toplam) | Tek turda 2 farklı fırsat nesnesi kullan | 600 ₺ |
| 7 · Hız Avcısı | Isı duvarını kır | Jet akımında 3 s kesintisiz kal | ×2 komboya ulaş | 900 ₺ |
| 8 · Bulut Ustası | Tropopoz eşiğini geç | Bir nadir olay gör | Konfeti topunu "mükemmel" açıda ateşle | 1.300 ₺ |
| 9 · Fırtına Kovalayan | Madam Koli'yi nakavt et | Hiç dalış kullanmadan 4 km uç | 3 son şansı da kullan, sonra 1 km daha uç | 1.800 ₺ |
| 10 · Astronot Adayı | Kármán çizgisini geç | Bir uydu panelini döndür | Hayaletini geç | 2.500 ₺ |
| 11 · Astronot | Yörünge hızına ulaş | Uzay istasyonundan yakıt al | ×3 komboya ulaş | 3.500 ₺ |
| 12 · Kaşif | Baron Vakum'u nakavt et | Kaçış hızına ulaş | 20 bilgi kartı topla | 5.000 ₺ |

### 4.4 Koleksiyon: bilgi kartları (30 kart, 6 albüm)

Kartlar kapsülden (T4), radyosonde parçalarından (Y4: 5 parça = 1 kart), nadir olaylardan, rakip nakavtlarından ve set ödüllerinden gelir. Albüm tamamlanınca: 1.000 × albüm no ₺ ve bir kaplama. **[D]** = yayından önce doğrulanmalı (PLAN §11 "Gerçek bilgi").

| Albüm | Kartlar |
|---|---|
| 1 · Kıyı ve alçak hava | Ses deniz seviyesinde ~343 m/s, ~1.235 km/sa (20 °C) **[D]** · Leylekler göçte kanat çırpmadan termallerle yükselir; İstanbul Boğazı büyük bir göç yolu **[D sayı verilecekse]** · Sığırcık sürülerindeki her kuş en yakın ~7 komşusunu izler **[D]** · Meteoroloji balonları dünyada günde iki kez yüzlerce istasyondan aynı saatte bırakılır **[D sayı]** · Uçurtmalar binlerce yıldır kullanılıyor; ilk kullanım Çin'de **[D]** |
| 2 · Ses duvarı | İlk ses duvarı aşan uçuş: Chuck Yeager, Bell X-1, 14 Ekim 1947 **[D]** · Ses duvarında sürükleme birden artar (transonik sürükleme tepesi) · Concorde ~Mach 2 ile yolcu taşıdı **[D]** · Sonik patlama tek bir "bum" değil, uçağın arkasından sürüklenen bir koni · Bulut konisi (buhar diski) yoğuşmadan oluşur; her zaman Mach 1'de değildir **[D]** |
| 3 · Bulutlar ve hava | Jet akımları ~9–12 km'de, saatte yüzlerce km'ye çıkabilir **[D]** · Merceksi bulutlar dağ dalgalarında oluşur; planörler bunlarla yükselir · Fırtına bulutlarının tepesi tropopoza dayanınca örs biçimi alır · 2010 İzlanda kül bulutu Avrupa hava trafiğini günlerce durdurdu **[D]** · Gökkuşağı halkası (glory) uçağın gölgesinin çevresinde görünür |
| 4 · Lacivert tavan | Gece parlayan bulutlar ~76–85 km'de, Dünya'nın en yüksek bulutları **[D]** · Göktaşlarının çoğu ~80–100 km'de yanar **[D]** · Kırmızı cinler fırtınaların üstünde 50–90 km'de çakan kısa ışıklar **[D]** · X-15 roket uçağı Mach 6,7'ye ulaştı (1967) **[D]** · Stratosfer atlayışları: Baumgartner 2012, Eustace 2014 rekorları **[D irtifa]** |
| 5 · Kármán ve yörünge | Kármán çizgisi 100 km, uzayın yaygın kabul gören sınırı **[D: ABD bazı kurumlarda 80 km]** · Alçak yörünge hızı ~7,8–7,9 km/s **[D]** · ISS ~400 km'de, ~90 dakikada bir tur atar **[D]** · Yörüngede olmak "sürekli düşüp ıskalamak"tır · İzlenen uzay çöpü sayısı on binlerce **[D güncel sayı]** · Kessler etkisi: çarpışmaların zincirleme çöp üretmesi |
| 6 · İnsanlar ve kilometre taşları | Sputnik 1, 4 Ekim 1957 **[D]** · Yuri Gagarin, ilk insanlı uzay uçuşu, 12 Nisan 1961 **[D]** · Alper Gezeravcı, ilk Türk astronot, 2024, ISS **[D]** · Türksat 6A, Türkiye'nin yerli haberleşme uydusu, 2024 **[D]** · Kaçış hızı ~11,2 km/s = yörünge hızının ~√2 katı **[D]** · Yeniden kullanılan ilk yörünge roketi kademesi inişi: Aralık 2015 **[D]** |

(Albümler 5 + 5 + 5 + 5 + 6 + 6 = 32 aday kart. Doğrulamada en zayıf 2 kart çıkarılır, 30 kalır.)

### 4.5 Roketler ve kaplamalar

| Roket | Açılış | Özel güç (tek dokunuş) | Bedel | Mantık |
|---|---|---|---|---|
| Kıvılcım | Baştan | Dengeli. Mükemmel sekme +%10 (standart) | — | — |
| Süzülgen | Tur 18 · 6.000 ₺ | Dalış hakkı **yokken** dokun: katlanır kanatlar 1,2 s açılır, g_etkin × 0,35, Cd × 1,3. Bekleme 5 s | Dalış gücü −%15 | Kanat kaldırma kuvveti düşüşü yavaşlatır ama sürükleme artar: enerji kazanılmaz, irtifa için hız harcanır |
| Kancalı | Tur 28 · 25.000 ₺ ya da Set 10 | Dokun = dalış yerine 140 b menzildeki en yakın trambolin nesnesine kanca: 0,6 s sarkaç, hız büyüklüğü %95 korunur, yön yukarı-ileri döner. 1 dalış hakkı harcar | Mükemmel sekme bonusu yok | Sarkaç enerjiyi korur (kayıplı); nesne de rokete doğru çekilip sallanır (iki taraf) |

**Kaplamalar (görsel, güç vermez), 12 adet:** Karpuz · Simit · Nazar boncuğu · Çay bardağı · Lokum · Retro Sputnik · Leylek · Baron (R5 nakavtı) · Konfeti · Kargo kolisi · Altın martı · Galaksi. Edinme: 4 kaplama parçası (kapsül), albüm tamamlama, rakip nakavtı, set ödülleri. Her roket her kaplamayı giyebilir.

### 4.6 Kargo kapsülü kartları

Kapsül açılınca 3 kart fırlar, üçü de kazanılır (bkz. Açık karar 2). "Tek tur" kartları **bir sonraki turda** geçerli ve rokette görünür parça olarak durur (kural 5).

| Tür | Kart | Etki | Ağırlık |
|---|---|---|---|
| Para | Bahşiş · Sponsor çeki · Büyük ikramiye | Son 5 tur ortalama kazancının %20 · %50 · %120'si | 25 · 12 · 3 |
| Tek tur güç | Ek yakıt tankı | Başlangıçta +1 dalış hakkı (tank gövdede görünür) | 8 |
| | Turbo rampa | Kalkış +20 b/s (rampada ek itici görünür) | 8 |
| | Yedek kademe | +1 son şans (ek kademe görünür) | 5 |
| | Kombo mıknatısı | Kombo süresi +2 s (yayın anteni) | 6 |
| | Tampon | İlk fren nesnesinin kaybı %0; tampon kırılır | 6 |
| | Fırsat yağmuru | Fırsat nesnesi sıklığı ×2 | 5 |
| İndirim | Kupon | Bir geliştirmede %25 indirim (tek kullanım) | 8 |
| Koleksiyon | Bilgi kartı · Kaplama parçası | Albüme kart · kaplamaya parça | 10 · 8 |
| Rakip | Gizli dosya | Sonraki kalkışta rakibe +%50 hasar | 5 |
| Nadir | Altın kapsül | Sonraki kapsülde 3 kartın biri Büyük ikramiye | 1 |

### 4.7 Günlük ve oturum hedefleri (reklamsız, cezasız)

| Sistem | Kural |
|---|---|
| Günlük hedefler | Her gün 3 küçük hedef (görev havuzundan, oyuncunun seviyesine uygun). Ödül: her biri son 5 tur ortalama kazancının %50'si. **Yapılmayanlar silinmez,** en çok 9 hedef (3 gün) birikir. Seri yok, kayıp yok |
| Günün tohumu | Ana menüde "Günün uçuşu": herkesin aynı gün aynı tohumla oynadığı tur. Kendi önceki günlerinle karşılaştırılır (çevrimiçi sıralama yok) |
| Günün yıldızı | Her gün bir nesne türü ×2 ödül verir (ör. "Bugün martılar ×2") |
| Isınma | Oturumun ilk turunda dalış göstergesi yarı dolu başlar (yalnız ödül, eksiğe ceza yok) |
| Kesinti | Oturumu yarıda bırakmak hiçbir şey kaybettirmez; tur kazancı her durumda tam alınır |

### 4.8 Rekorlar ve hayalet

| Öğe | Kural |
|---|---|
| Rekorlar | En uzak mesafe · en yüksek hız · en yüksek irtifa · en büyük kombo · en çok sekme · en uzun uçuş süresi |
| Rekor balonu | En uzak mesafende dünyada ajansının bayraklı işaret balonu durur ("REKOR 4,2 km"). Trambolin değil, geçince patlar ve "YENİ REKOR!" (kural 5: kalıcılığın görünür sebebi) |
| Hayalet | En iyi turun (x, y) izi 10 Hz kaydedilir, yarı saydam mavi roket silueti olarak aynı zamanlamayla uçar. Geçtiğin an "Hayaletini geçtin!" ve tur sonunda +%10 kazanç (tur başına 1 kez). Ayarlardan kapatılabilir |
| Kara kutu karşılaştırması | Tur sonunda rekor grafiği: bu tur (turuncu) ve en iyi tur (mavi) hız-mesafe eğrisi |

---

## 5. İlerleme takvimi (ilk 60 tur)

Hedef: her 2–4 turda bir yenilik. Tur kazancı hedefleri (~, ekonomi simülasyonuyla doğrulanacak): Tur 1: 120 · 5: 400 · 10: 900 · 15: 1.600 · 20: 2.600 · 25: 4.000 · 30: 5.500 · 40: 9.000 · 50: 12.000.

| Tur | Yeni nesne / olay | Hangar | Rakip / duvar | Görev / sistem |
|---|---|---|---|---|
| 1 | Martı, reklam balonu, parti balonu, uçurtma, reklam zeplini | Rampa gücü, Dalış gücü, Sekme verimi, Kademe itkisi, İzlenme çarpanı | R1 Kaptan Pofuduk gelir | Set 1 |
| 2 | Yük dronu | Gösterge dolum hızı, Mükemmel bölge; **F1 Yakıt dronu** dükkânda | | |
| 3 | Su roketleri, kargo kapsülü | **F2 Havai fişek** | **Ses duvarı** → Bölge 2, rüzgâr tabakası | Kapsül kartları |
| 4 | Afiş çeken uçak | İp kesici, Aerodinamik | | Set 2 |
| 5 | Radyosonde | Burun konisi | | Koleksiyon albümü açılır; **U1 Dev balon** (garanti ilk nadir) |
| 6 | Kargo uçağı + kargo paraşütleri | **F3 Konfeti topu**, Zırh görünür | | Set 3 |
| 7 | Altın martı | Zeplin hasarı | **R1 nakavt** → R2 Madam Koli | **U2 Hava gösterisi** |
| 8 | Fırtına hücresi | **F4 Termal sütun** | | Günlük hedefler açılır |
| 9 | Sıcak hava balonu | **F9 Yayın dronu**, Kombo süresi | | Set 4 |
| 10 | — | Isı kalkanı | **Tropopoz eşiği**; Isı duvarı ilk karşılaşma | **U3 Fenerler**; hayalet açılır |
| 11 | Sondaj roketi | **F6 Jet akımı** | | Set 5 |
| 12 | — | **F5 Sapan dronu**, Kademe sayısı sv1 (2 son şans) | **Isı duvarı** → Bölge 3 | **U5 Leylek göçü** |
| 13 | Bilim balonu, göktaşı izi, gece parlayan bulut | **F8 Dalga bulutu** | | Set 6 |
| 14 | Uçan daire şakası (U4) | Mükemmel bonusu | **R2 nakavt** → R3 Profesör Pervane | |
| 15 | Volkanik kül | **F7 Tanker dronu** | | Set 7 |
| 16 | Sığırcık bulutu | Kademe yakıtı | | **U7 Rakip yarışı** |
| 17 | — | Sansasyon (nadir olay şansı) | | Set 8 |
| 18 | U6 Güneş tutulması | **Süzülgen roket** | | Kaplamalar açılır |
| 19 | Uydu, uzay çöpü | Hurda satışı | **Kármán çizgisi** | |
| 20 | U8 Dev güneş kanadı | Kombo tavanı | | Set 9 |
| 21 | Şişme habitat modülü | **F10 Uzay römorkörü** | | |
| 22 | U9 Meteor yağmuru | Kapsül sıklığı | **R3 nakavt** → R4 Bayan Sinyal | |
| 23 | — | Dalış kapasitesi sv1 (3 dalış) | | Set 10 |
| 24 | Ölü üst kademe | Son ateşleme | | |
| 25 | Uzay istasyonu (U11) | | **Yörünge hızı** → Bölge 4 | |
| 26 | U10 Kuzey ışıkları | Kademe sayısı sv2 (3 son şans) | | Set 11 |
| 27 | — | Dalış kapasitesi sv2 (4 dalış) | | Albüm 5 kartları |
| 28 | — | **Kancalı roket** | | |
| 30 | — | | **R4 nakavt** → R5 Baron Vakum | Set 12 |
| 31–39 | Her turda nadir olay şansı %35+; Baron'un altın uydusu her turda | Kalan geliştirmelerin üst seviyeleri; her 2 turda bir fırsat üst seviyesi | Kaçış hazırlığı: hız 700, 750, 800 ara rekor bayrakları (her biri 1.000 ₺ ilk kez) | Rekor ve albüm tamamlama |
| 39 | — | | **R5 nakavt** → Ay üssü hazır | |
| 40 | Kaçış sahnesi | | **Kaçış hızı** → **Ay bölümü** | |
| 41 | Ay: iniş hava yastığı topu, kargo inici | Ay sekmesi: "Vakum gövde" (sürükleme yok, Aerodinamik yerine) | Ay rakibi 1 | Ay görev setleri |
| 43 | Ay: kütle sürücüsü kovası | Ay fırsatı: kütle sürücüsü | | |
| 45 | Ay: eski kademe hurdası, regolit tozu | | Ay eşiği: Krater sırtı 1 | |
| 47 | Ay: buz kütlesi | | | Ay albümü |
| 49 | Ay nadir olayı: Ay geçidi istasyonu | | Ay rakibi 1 nakavt → 2 | |
| 52 | Ay: Ay madenci dronu | Ay fırsatı: madenci dronu | | |
| 55 | Ay: lazer yansıtıcı (kart) | | Krater sırtı 2 | |
| 58 | — | | Ay rakibi 2 nakavt | |
| 60 | Ay kaçışına hazırlık | | Ay kaçış hızı → Mars (~tur 62–65) | |

Uzun boşluk denetimi: Dünya'da en uzun "yeni şeysiz" aralık 2 tur (28→30, 31–39 arası her turda geliştirme + ara rekor bayrakları). 41–60'ta en çok 3 tur.

---

## 6. Hangar geliştirme ağacı (tam liste)

Fiyat = taban × 1,55^(mevcut seviye). "Görünür" = hangarda belirdiği tur (o turdan önce gizli, dükkân yavaş açılır). Toplam tahmini maliyet ≈ 280.000 ₺; Dünya'da (40 tur, toplam kazanç ~150.000 ₺) yaklaşık %55'i alınır, gerisi Ay'da da işe yarar (~).

| Sekme | Geliştirme | Sv | Taban | Etki / seviye | Görünür |
|---|---|---|---|---|---|
| **Rampa** | Rampa gücü | 10 | 60 | Kalkış +12 b/s (70 → 190) | 1 |
| | Mükemmel bölge | 5 | 80 | Yeşil bölge %12 → %24 (+2,4 puan) | 2 |
| | Mükemmel bonusu | 5 | 200 | +%30 → +%55 (+5 puan) | 14 |
| | Zeplin hasarı | 8 | 120 | Rakibe hasar +%15 | 7 |
| **Gövde** | Sekme verimi | 8 | 90 | Trambolin k +0,01 (0,80 → 0,88), yatay kayıp −%8 göreli | 1 |
| | Aerodinamik | 8 | 150 | Cd −%5 (en çok −%40) | 4 |
| | Burun konisi | 6 | 120 | Yavaşlatıcı kaybı −%8 göreli | 5 |
| | İp kesici | 4 | 100 | İp ve afiş freni %35 → %7 (−7 puan) | 4 |
| | Isı kalkanı | 6 | 1.500 | Isı birikimi −%15 | 10 |
| | Zırh | 3 | 2.500 | Ölümcül çarpmayı atlatır: sv1 −%60 kayıp, sv2 −%45, sv3 −%30 ve turda 2 kez | 6 |
| **Kademeler** | Kademe sayısı | 2 | 600 / 6.000 (sabit) | Son şans 1 → 2 → 3 | 12 |
| | Kademe itkisi | 8 | 200 | 40 → 90 b/s (+6,25) | 1 |
| | Kademe yakıtı | 5 | 300 | Ateşleme 0,8 → 1,4 s (+0,12) | 16 |
| | Hurda satışı | 5 | 150 | Paraşütle inen boş kademe başına +20 ₺ (gerçek kademe geri kazanımı) | 19 |
| **Motor** | Dalış gücü | 10 | 70 | +18 → +40 b/s (+2,2) | 1 |
| | Gösterge dolum | 8 | 90 | Dolum +%10 | 2 |
| | Dalış kapasitesi | 2 | 900 / 7.000 (sabit) | 2 → 3 → 4 dalış | 23 |
| | Son ateşleme | 4 | 400 | Yatay hız < 30 ve kademe yokken 1 kez otomatik ateşleme: +15 b/s / sv | 24 |
| **Fırsatlar** | F1–F10 | Aç + 4 + 5 | §3 | §3 | §5 takvimi |
| **Yayın** | İzlenme çarpanı | 10 | 150 | +%10 | 1 |
| | Kombo süresi | 5 | 120 | 3 → 5,5 s (+0,5) | 9 |
| | Kombo tavanı | 3 | 1.000 | ×3 → ×5 (+0,67) | 20 |
| | Kapsül sıklığı | 5 | 300 | Tur başına %35 → %60 (+5 puan) | 22 |
| | Sansasyon | 5 | 500 | Nadir olay şansı %25 → %50 (+5 puan) | 17 |
| **Roketler** | Süzülgen · Kancalı | — | 6.000 · 25.000 | §4.5 | 18 · 28 |

Toplam: 23 geliştirme + 10 fırsat (her biri 3 çizgi) + 2 roket = **63 satın alma çizgisi**.

---

## 7. Diğer bölümler: içerik iskeleti

Her bölümün kendi "zemini" yok kuralı Dünya için geçerli; diğer bölümlerde de tur sonu "yüzeye kademesiz değmek". Ayrıntılar Dünya bölümü eğlenceli bulunduktan sonra.

| Bölüm | Nesneler (tek satır davranış) | İmza nadir olay | Rakip / duvar fikri |
|---|---|---|---|
| **2 · Ay** | Hava yastığı topu: trambolin k 0,9 (sürükleme yok) · Kargo inici: iticileri seni yukarı iter (onun yakıtı) · Kütle sürücüsü kovası: elektromanyetik raya bin, +60 (güneş enerjisi) · Eski kademe hurdası: −%15, döner · Regolit tozu bulutu: −%3, görüş kısalır · Buz kütlesi (krater gölgesi): sert trambolin k 0,7, kırılır · Madenci dronu: yük taşır, çarpınca −%10, cevher saçar (₺) · Lazer yansıtıcı: kart · Yörünge hurdası: −%8 · Ay rover'ının antenli işaret balonu yok (hava yok): yerine işaret fişeği | **Ay geçidi istasyonu:** robot kol seni yakalayıp 360° döndürür ve fırlatır (sarkaç, enerji korunur, yön değişir) | Rakip: "Gölge Madencilik" robot kepçeli kule. Duvar: Krater sırtları (yükseklik eşikleri), Ay kaçışı. **Not:** PLAN'daki "kraterden fışkıran gaz" Ay'da kaynaksız; kütle sürücüsüyle değiştirildi |
| **3 · Mars** | Toz hortumu: termal gibi yukarı +12 b/s² (güneş ısısı) · Mars helikopteri: küçük yük dronu, k 0,7 · Paraşütlü iniş kapsülü: kubbe trambolin · Hava yastıklı iniş topu: k 0,85 · CO₂ gayzeri (kutup): yukarı itiş +30 (güneşle ısınan gaz) · Kum fırtınası bandı: −4 b/s², görüş 60 b · Kum bulutu: −%4 · Phobos sapanı: +30 (küçük kütle, küçük sapan) · Deimos: uzak, kart · Terk edilmiş paraşüt kılıfı: −%2 | **Küresel toz fırtınası:** gök kızıllaşır 15 s, her şey yavaşlar ama izlenme ×3 | Rakip: "Kızıl Turizm" (uçan daire şakasının sahibi, U4 bağlantısı). Duvar: Olympus Mons (irtifa eşiği), Mars kaçışı |
| **4 · Asteroit Kuşağı** | Moloz yığını asteroit: yumuşak, top havuzu gibi trambolin k 0,8 · Metal asteroit: sabit, ölümcül, uyarılı · Kuyruklu yıldız gaz jeti: +40 (güneşle süblimleşme) · Madenci gemisi: yandan −%20 · Toz halkası: −%2 · İkili asteroit: ikisi birbirinin etrafında döner, zamanlama · Buzlu asteroit: kırılır, parçalar saçılır · Cüce gezegen yakın geçişi: sapan +50 | **Çarpma testi:** bir sonda asteroide çarpar, saçılan moloz dalgasında sörf | Rakip: "Kaya Kartel" madenci. Duvar: Kirkwood boşlukları (nesnesiz uzun bölgeler) |
| **5 · Jüpiter** | Konveksiyon kulesi: yukarı akım +25 b/s² · Amonyak bulut şeridi: −%3 · Büyük Kırmızı Leke: dairesel rüzgâr bandı, dışında ileri, içinde geri · Io volkan sütunu: +70 (gelgit ısısı) · Radyasyon kuşağı: dalış göstergesi dolmaz · Europa buz kırığı: trambolin k 0,75 · Küçük uydu kayası: −%10 · Kayan sonda: kart · Jüpiter sapanı: +150 (dev kütle) | **Kuyruklu yıldız çarpması:** parçalar Jüpiter'e dalar, dev ateş topları arkadan şok dalgası (+100) | Rakip: "Dev Enerji" gaz toplayıcı. Duvar: radyasyon kuşağı geçişi |
| **6 · Satürn** | Halka buzu topağı: trambolin k 0,8 · Halka tozu: −%2 · Halka boşluğu: nesnesiz, sekme yok (risk) · Enceladus gayzeri: +50 (gelgit ısısı) · Çoban uydu: halka parçalarını iter, yön değiştirir · Titan pusu: yoğun hava, sürükleme ×3, paraşüt fırsatı · Altıgen fırtına şeridi: kuyruk rüzgârı · Halka dalgası: dalga bulutu gibi | **Büyük Beyaz Leke fırtınası:** gezegen çapında fırtına, 20 s güçlü kuyruk rüzgârı | Rakip: "Halka Lüks Gemi Turları". Duvar: halka düzlemi geçişi |
| **7 · Uranüs–Neptün** | Metan buz bulutu: trambolin k 0,75 · Süpersonik rüzgâr bandı: +8 b/s² (gerçekte Güneş Sistemi'nin en hızlı rüzgârları **[D]**) · Karanlık leke girdabı: aşağı akım −15 · Triton azot gayzeri: +40 · Yan yatık halka: çapraz geçiş · Elmas yağmuru (varsayım, kartta "bilim insanlarının tahmini" diye yazılır **[D]**) · Uzak sonda: kart · Karanlık: görüş 120 b | **Neptün'ün büyük karanlık lekesi:** 15 s dev girdap, içinde dönerek hız korunur | Rakip: "Buzul Lojistik". Duvar: görüş eşiği (fener geliştirmesi gerekir) |
| **8 · Plüton** | Azot buzu ovası: kaygan trambolin k 0,85, yatay kayıp yok · Su buzu dağları: sabit, uyarılı · Metan karı: −%3 · Mavi pus katmanları: −%1, görsel · Charon sapanı: +40 · Azot buzulu akıntısı: yavaş kuyruk rüzgârı · Kuiper nesnesi: kardan adam biçimli kaya, trambolin · Uzak sonda selamı: kart | **Kalp:** Plüton'un kalp biçimli ovası görünür; final iniş mini oyunu (Tombaugh Regio) | Rakip yok: final. Son duvar: "Zafer" iniş hızı eşiği; sonrası zaman yarışı |

---

## 8. Mantık denetimi tablosu

### 8.1 Her hızlandırıcının enerji kaynağı

| Hızlandırıcı | Kazanç | Kaynak (görünür) | Sınır |
|---|---|---|---|
| Rampa | 70–190 | Rampanın itici sistemi | Turda 1 |
| Dalış | +18–40 | Roketin yakıtı (dalış hakkı = yakıt dozu) | Hak sayısı |
| Mükemmel sekme | +%10 | Dalışın yakıtı (sekme anına aktarılır) | En çok +25 b/s |
| Kademe ayırma | +40–90 | Her kademenin kendi motoru | Kademe sayısı (1–3) |
| Son ateşleme | +15–60 | Yedek yakıt | Turda 1 |
| Yük dronu (S4) | +15 vy | Dronun bataryası (gösterge düşer) | Dron başına 1 |
| H1 Havai fişek | +60–110 | Barut | 400 b arası |
| H2 Konfeti topu | +45–95 | Basınçlı gaz tüpü | 400 b arası |
| H3 Sapan dronu | +70–120 | Dronların gerdiği lastik | Giriş hızı × 0,9 (lastik de kayıp yaşatır) |
| H4 Tanker | +50–100 | Tanker yakıtı, roketin motorunda | Tanker başına 1, sonra "boş" |
| H5 Su roketi | +25 vy | Basınçlı hava | Yalnız alttan çarpmada |
| H6 Römorkör | +40–80 | Römorkör yakıtı | Römorkör başına 1 |
| C1 Termal | +8–16 b/s² yukarı | Güneşin ısıttığı kara | 3–4 s; yatay hız vermez |
| C2 Jet akımı | 12 × (1 − v/V) | Rüzgâr | v ≥ V_rüzgâr iken 0 |
| C3 Dalga bulutu | +14–24 b/s² yukarı | Dağ dalgası rüzgârı | Arka tarafta −6 |
| C4 Kuyruk rüzgârı | +4 b/s² | Rüzgâr | V 120 |
| C5 Fırtına merkezi | +20 b/s² yukarı | Sıcak nemli havanın yükselmesi | Kenarda −15, yıldırım |
| X2 Sondaj roketi | +20 vy | Onun motoru | Bedeli −%25 |
| U9 Ateş topu | +80 | Göktaşının kinetik enerjisi | Turda 1 (nadir) |
| U11 İstasyon | +2 dalış | İstasyonun yakıt bidonları | Turda 1 |
| Trambolinler | 0 (yalnız yön) | — | k < 1 her zaman |
| Kancalı, U12 balina | 0 (yalnız yön) | — | %95 korunur / %100'ü aşmaz |
| Rüzgâr gölgesi (X1, U2) | 0 (kayıp azalır) | — | 3–4 s |

**Kod testi:** her hız artışı yukarıdaki kaynak kimliklerinden birine bağlanır; bağlanmayan artış testte hata verir (PLAN §3 kural 1).

### 8.2 Her çarpışmanın iki tarafı

| Çarpışma | Roket | Nesne |
|---|---|---|
| Martı, sığırcık | −%3 / −%1 | Sersem, tüy, toparlanır / kaçışır |
| Balon, parti balonu | Trambolin | Çöker, patlar |
| Zeplin, sıcak hava balonu, rakip zeplini | Trambolin / fren | Çöker, dalgalanır, söner; rakip yama alır |
| Yük dronu | Trambolin + 15 | Basılır, batarya düşer / parçalanır, paraşüt |
| Uçurtma, afiş | Fren | İp kopar, afiş yırtılır, uçak yalpalar |
| Radyosonde, kapsül | Küçük fren | Patlar / açılır, paraşüt |
| Kargo uçağı | Patlama ya da −%30 | Parçalanır, kargo paraşütleri |
| Sondaj roketi | −%25, +20 vy | Takla, paraşüt |
| Uydu, çöp, ölü kademe | Fren ya da patlama | Panel döner, bölünür, saçılır |
| Fişek, konfeti, sapan, tanker, römorkör | Hızlanır | Yakıtı/şarjı biter, geri tepme, uzaklaşır |
| Habitat, bilim balonu | Trambolin | Esner, manken/kutu sallanır |
| Kancalı roket kancası | Yön değişir | Nesne rokete doğru çekilir, sallanır |

### 8.3 Sömürü döngüsü riskleri

| Risk | Sınır |
|---|---|
| Sonsuz balon sekmesi | k < 1 ve yatay kayıp; aynı nesne 2 s içinde etki vermez; balon 3. vuruşta patlar |
| Termalde asılı kalma | En çok 3–4 s, sonra sütun dağılır (görsel); yatay hız vermez, sürükleme yatayı eritir |
| Jet akımıyla sınırsız hızlanma | v ≥ V_rüzgâr iken ivme 0 |
| Hızlandırıcı zinciri | İki hızlandırıcı arası ≥ 400 b; fırsat sıklığı tavanı 0,9/km |
| Fener ve sığırcıkla kombo çiftliği | Fener en çok 120; sığırcık kuş başına ödül tur başına en çok 100 kuş |
| Rakibe sonsuz hasar | Rampada turda 1; uçuşta S9 turda en çok 1, T5 sıklığı sabit |
| Hayalet geçme | Tur başına 1 bonus, yalnız yeni rekorda |
| Kademe hurda satışı | Turda en çok 3 kademe; ayırma yalnız y < 25'te tetiklenir, oyuncu isteyerek çoğaltamaz |
| Günlük hedef biriktirme | En çok 9 bekleyen hedef |
| Günün tohumunu ezberleme | Kazanç normal tur kadar; ek ödül yok |
| Mükemmel sekme + dalış döngüsü | Dalış hakkı sınırlı, bonus en çok +25 b/s |

### 8.4 PLAN_B ile tutarsızlıklar (bu kitapta düzeltildi, onay gerekli)

| PLAN_B yeri | Sorun | Bu kitaptaki çözüm |
|---|---|---|
| §6 Uydu "mini sapan +25" | Uydunun kütlesi rokete hız veremez (kural 1) | Uydu yavaşlatıcı (Y9); hız rolü Uzay römorkörüne (F10) |
| §6 Dron-helikopter "rotor akımı yukarı iter" | Rotor akımı aşağı eser | Yük dronu: üstünde şişme yastık + 0,3 s motor itişi (batarya) |
| §3 kural 3 "Kargo pilotu paraşütle atlar" | §6 kargo uçağı "insansız" | İnsansız, pilot yok; kargo paraşütleri açılır |
| §9 "su sütunu" | Deniz kaldırıldı (6.1) | Yere iniş: toz bulutu, paraşüt |
| §8 Ay "kraterden fışkıran gaz" | Ay'da gaz kaynağı yok | Kütle sürücüsü kovası (güneş enerjisi) |
| §5 rampa yüksekliği | Belirtilmemiş; 70 b/s 38° ile tepe ~31 b, alçak bant altı 25 | Rampa y = 60 önerisi |
| §6 Uzay istasyonu "+2 dalış" | Kaynak yazılı değil | Robot kolun fırlattığı yakıt bidonları |

---

## 9. Açık kararlar (kullanıcıya sorulacak)

1. **PLAN_B'deki 7 mantık düzeltmesi (§8.4).** (a) Hepsini onayla ve PLAN_B'yi güncelle, (b) tek tek konuşalım. **Öneri: (a).**
2. **Kargo kapsülü kartları.** (a) 3 kartın üçü de kazanılır (cömert, sade), (b) 3 ters karttan birini seçersin (Burrito Bison'daki sürpriz hissi, bir dokunuş fazla). **Öneri: (a);** (b) hangarda değil tur sonunda 2 s eklediği için akışı yavaşlatır.
3. **Fırsat nesnelerindeki dokunuş.** (a) Turkuaz halka içindeyken dokunuş nesnenin eylemini yapar (nişan, bırak, bağlan), dışında dalış; (b) fırsatlar tamamen otomatik, dokunuş her zaman dalış. **Öneri: (a);** Burrito Bison'un özel jölelerindeki "doğru anda dokun" hissini verir, tek dokunuş kuralını bozmaz.
4. **Rakiplerin tonu.** (a) Komik Türk karakterleri (Kaptan Pofuduk, Madam Koli, Profesör Pervane, Bayan Sinyal, Baron Vakum), (b) uluslararası/İngilizce esinli adlar, (c) hayvan maskotlar. **Öneri: (a).**
5. **B1 kapsamı.** (a) Bu kitaptaki 38 nesne, 12 nadir olay, 10 fırsatın hepsi B1'de; (b) B1 = ilk 25 tura yetecek ~24 nesne + 5 nadir olay + 6 fırsat, kalanı B1.5. **Öneri: (b);** önce eğlenceyi kanıtlar, B0 zaten 5 nesneyle başlıyor.
