# Son Durak: Plüton — Plan B (Burrito Bison mantığı)

Taslak 6 · 2026-10-08 · Durum: kullanıcı onayı bekliyor

Bu plan, Taslak 5'teki fikri (Dünya'dan Plüton'a, her denemeden sonra geliştirme) korur, oynanışı ise baştan Burrito Bison mantığına göre kurar. A0'daki gerçekçi uçuş simülasyonu bırakılır.

---

## 0. Kuzey yıldızı ve kalite çıtası

**Tek cümle:** Rampadan fırlatılan çizgi film roketi, denizin üstünde sekerek, çarptığı şeylerden hız kaparak ve doğru anda dokunarak momentumunu korur. Yeterince hızlanırsa yörüngeye, sonra Ay'a, en sonunda Plüton'a "düşer".

**4,5 yıldız ne demek?** Mağazada 4,5 ve üstü alan arcade fırlatma oyunlarının (Burrito Bison: Launcha Libre, Learn to Fly 3, Earn to Die 2) ortak özellikleri. Her biri ölçülebilir bir kabul ölçütüne dönüştü (§12):

1. İlk 5 saniyede "vay" anı, ilk 30 saniyede kural öğrenilmiş.
2. Bir tur 20–90 saniye, yeniden başlatma 3 saniyenin altında.
3. Her 1–3 turda bir satın alma, her 2–4 turda yeni bir şey (nesne, bölge, rakip).
4. Her vuruş hissedilir: duraksama, sarsıntı, ses, parçacık, sayı.
5. Haksız son yok: oyuncu her zaman neden durduğunu görür ve bir sonrakinde neyi değiştireceğini bilir.
6. Takılma yok: kare hızı 60, ilk açılış 5 saniyenin altında, kayıt kaybı yok.
7. Mantık hatası yok: her etkinin görünür bir sebebi var (§3).

---

## 1. Burrito Bison'un anatomisi ve bizim karşılığımız

Kaynaklar: oyunun resmî sitesi, rehberler ve incelemeler (§15). "Al" birebir alınan mekaniği, "uyarla" temaya çevrilen mekaniği, "at" bilerek dışarıda bırakılanı gösteriyor.

| Burrito Bison | Ne işe yarıyor | Bizde | Karar |
|---|---|---|---|
| Ringden sapanla fırlatma, zamanlama göstergesi, kritik vuruş | İlk saniyede beceri ve heyecan | **Rampa fırlatması:** gösterge iğnesi yeşil bölgedeyken dokun → mükemmel kalkış (+%30 hız) | Al |
| Ringdeki rakip: canı var, her fırlatmada hasar alır, nakavt olunca büyük ödül, sıradaki rakip gelir | Her turda küçük, uzun vadede büyük hedef | **Rakip ajansın zeplini:** rampanın yanında asılı durur, mükemmel kalkış onun gondoluna çarpar; yamalı zeplin turlar arasında hasarını taşır, nakavt olunca söner ve uçup gider, sıradaki rakip gelir (5 rakip) | Uyarla |
| Normal jöle ayılar: üstlerine düşünce sekersin ama yavaşlarsın, para verirler | Sürekli küçük karar ve ödül | **Martılar, şişme reklam balonları, şamandıralar:** çarpınca küçük hız kaybı, izlenme puanı | Uyarla |
| Yere değmek seni çok yavaşlatır, uzun süre yerde kalırsan tur biter | Havada kalma baskısı | **Su sekmesi:** sığ açıyla suya değersen taş gibi sekersin ama hız kaybedersin; dik açıyla suya girersen batarsın ve tur biter | Uyarla (gerçek fizik) |
| Roket dalışı (Rocket Slam): gösterge dolunca 2 kullanım (yarısında 1); aşağı dalıp ayıya çarpınca yüksek sekersin | Tek dokunuşluk beceri | **Dalış ateşlemesi:** aynı kural. Dokun → roket burnunu 22° aşağı verir ve kısa ateşler; bir nesneye ya da suya değdiği anda dev sekme | Al |
| Özel jöleler satın alınınca oyunda çıkmaya başlar (roketli, bombalı, balonlu, ek dalış veren…) | Para harcamanın görünür sonucu, çeşitlilik | **Fırsat nesneleri:** havai fişek mavnası, eski deniz mayını, yakıt dronu, jet akımı… satın alınınca dünyada belirmeye başlar, yükseltildikçe güçlenir | Al |
| Polis jöleleri yerde devriye gezer, seni yakalayıp yavaşlatır | Yerden uzak durma nedeni | **Balıkçı ağları ve sahil güvenlik botu:** ağa sekersen ağır fren | Uyarla |
| Pasta duvarları: bölgeleri ayırır, kırmak için hız ve güç gerekir, hasar birikir | Orta vadeli büyük hedef, "bu tur kırdım!" anı | **Hız duvarları:** Ses duvarı (Mach 1), Isı duvarı (Mach 5), Yörünge hızı, Kaçış hızı. Gerçek eşikler, her biri sinematik bir an (§4) | Uyarla (gerçek fizik) |
| Piñata kartları (para, geçici güç, indirim) | Sürpriz ödül | **Kargo kapsülü:** uçuşta nadir çıkan paraşütlü kapsül, çarpınca 3 kart | Uyarla (reklamsız) |
| 3 karakter, her birinin özel gücü | Yeniden oynanabilirlik | **3 roket:** Kıvılcım (başlangıç), Süzülgen (kısa süzülme), Kancalı (uydulara kanca) | Al (Faz 4) |
| Tur sonu para dökümü, yükseltme dükkânı | "Bir tur daha" çekimi | **Kara kutu + Hangar:** neden durduğun, dökümü ve "bunu çözen geliştirme" kartı | Al + bizim kara kutumuz |
| Reklam izle → ödül, uygulama içi satın alma | Para kazanma | — | **At:** kişisel oyun, reklam yok; ekonomi buna göre ayarlanır |
| Sonu olmayan oyun sonu (eleştiri) | — | Plüton'a iniş = gerçek bir son + sonrası için zaman yarışı | **Düzelt** |

---

## 2. Çekirdek fikir: Burrito Bison'un döngüsü = gerçek yörünge fiziği

Gerçekte roket uzaya **yukarı çıkarak değil, yatayda hızlanarak** gider. Yatay hız arttıkça Dünya'nın eğriliği yüzünden "düşüşü ıskalarsın". Etkin yerçekimi:

> **g_etkin = g × (1 − (v / v_yörünge)²)**

- Yavaşsan yerçekimi tam çeker → denize düşersin.
- Hızlandıkça yerçekimi zayıflar → yaylar uzar, daha yüksekte süzülürsün.
- v = v_yörünge olunca g_etkin = 0 → **yörüngedesin**, süzülürsün.
- v = √2 × v_yörünge olunca kaçarsın → **Ay bölümü**. (Gerçek kaçış hızı da yörünge hızının √2 katı: 11,2 ≈ 1,41 × 7,9 km/s.)

Burrito Bison'daki "hızını koru, yere düşme" kuralı burada fiziğin kendisi oluyor. Formül gerçek, ölçek oyun için küçültülmüş: Dünya'nın yarıçapı "çizgi film" boyunda. Bu tek kural ilerlemeyi de tanımlıyor: hızlandıkça gökyüzü kararıyor, deniz kavisleniyor, yıldızlar çıkıyor.

---

## 3. Mantık kuralları (değişmez)

Her tasarım kararı bunlara göre denetlenir. Denetçi ajan her teslimatta bu listeyle kontrol eder.

1. **Enerji kaynaksız artmaz.** Hız ancak şunlardan gelir: rampa, motor ateşlemesi (yakıt), patlama (mayın, havai fişek), jet akımı, sapan (kütle çekimi). Balon ve sekme hızı **artırmaz**, yalnızca yönü yukarı çevirir ve bir kısmını kaybettirir. Kodda otomatik test: her hız artışı kayıtlı bir kaynağa bağlanmalı.
2. **Her çarpışmanın iki tarafı var.** Her nesnenin bir kütle sınıfı ve kendi tepkisi var (§6 tablosu). Hafif nesne savrulur, roket biraz yavaşlar. Ağır nesne parçalanır, roket çok yavaşlar ya da patlar. Sabit nesne (kaya) roketi durdurur.
3. **Şiddet yok, kimse ölmez.** Kuşlar sersemler, tüyleri uçar, toparlanıp uçar. Uçaklarda insan yok: kargo uçağı ve insansız dronlar. Kargo pilotu paraşütle atlar. Zeplindeki rakip kaptan her seferinde paraşütle iner ve yumruk sallar.
4. **Görünmeyen şey etkilemez.** Her etki önce görünür (uyarı, iz, gölge, kenar oku). Ekran dışından gelen her tehlike en az 1,2 saniye önce işaretlenir.
5. **Turlar arası kalıcılık bir sebebe dayanır.** Zeplinin hasarı yamalarla görünür. Kırılan hız duvarının rekoru bayrakla işaretlenir. Satın alınanlar roketin üstünde görünür.
6. **Kaçınılmaz ceza yok.** Oyuncuyu yalnızca kendi yavaşlığı ya da gördüğü bir tehlike durdurur. Ölümcül nesneler (kaya, kargo uçağı) seyrek, iri ve önceden uyarılı.
7. **Sayılar yalan söylemez.** Göstergedeki hız oyunun iç hızından tek yönlü bir eşlemeyle hesaplanır. Duvarların etiketi (Mach 1 = 1.235 km/sa) her zaman göstergeyle tutarlı.
8. **Sömürü döngüsü yok.** Balon zinciri ve sonsuz sekme gibi döngüler sınırlı: aynı nesne 2 saniye içinde ikinci kez etki vermez, sekme her seferinde enerji kaybettirir.

---

## 4. Tur akışı

```
HANGAR ──Kalk──► RAMPA (zamanlama) ──► UÇUŞ (sekme, çarpma, dalış) ──► DURUŞ ──► KARA KUTU ──► HANGAR
   ▲                                                                                          │
   └──────────────────────────── 3 saniyeden kısa ─────────────────────────────────────────┘
```

**Rampa (2–3 s).** Geri sayım biter, gösterge iğnesi sarkaç gibi gidip gelir. Dokunduğun an gücü belirler: yeşil = mükemmel (+%30 hız ve zeplin vuruşu), sarı = iyi, kırmızı = zayıf. Dokunmazsan 3 saniye sonra otomatik "iyi" kalkış.

**Uçuş.** Roket yay çizerek denizin üstüne iner, seker, nesnelere çarpar. Oyuncunun tek eylemi **dalış ateşlemesi**:
- Dalış göstergesi çarpma ve sekmelerle dolar. Yarısında 1, tamamında 2 dalış hakkı (ilk roket için, geliştirmeyle 3–4).
- Dokun → roket burnunu 22° aşağı verir ve 0,35 s ateşler: +18 hız (geliştirmeyle +40).
- Dalış bir nesneye ya da suya değerek biterse **mükemmel sekme**: o sekmede hız kaybı yok, üstüne +%10.
- Hak yokken dokunmak hiçbir şey yapmaz, gösterge kısa bir "boş" titreşimi verir.

**Duruş.** Hız düştükçe yaylar kısalır, düşüş dikleşir. Suya 35°'den dik girersen roket batar, tur biter. Komik bir son: roket şamandıra gibi su yüzüne çıkar, ajansın römorkörü çekip götürür. Seyrek ölümcül nesneye çarparsan da patlarsın: ateş topu, saçılan parçalar, kaptan paraşütle atlar. İki durumda da kazanç tam alınır, ceza yok. Burrito Bison'daki gibi.

**Kara kutu (tur sonu, en fazla 4 s).** Mesafe, en yüksek hız, kırılan duvarlar, izlenme dökümü. "Seni durduran şey" (ör. "Ses duvarının 40 km/sa altında kaldın") ve bunu çözen geliştirme kartı (fiyatı ve kaç tur kaldığı). Büyük "Tekrar uç" ve "Hangar" düğmeleri.

**Hangar.** 5 sekme (§7). Satın alma anında roketin üstünde parça yerine oturur, kısa bir test ateşlemesi yapılır.

---

## 5. Uçuş fiziği (oyun birimleri, ilk ayar)

Tüm sayılar tek bir yapılandırma nesnesinde durur. Denge, kod değil veri değişikliğiyle yapılır.

| Büyüklük | Değer | Not |
|---|---|---|
| Dünya düzlemi | x ileri, y yükseklik (deniz = 0) | Yandan 2.5B |
| Taban yerçekimi g | 30 b/s² | Oyun hissi için güçlü; gerçek oran g_etkin formülüyle |
| v_yörünge | 600 b/s | g_etkin = 0 |
| v_kaçış | 849 b/s (= 600 × √2) | Ay bölümüne geçiş |
| Hava yoğunluğu ρ(y) | e^(−y / 400) | Alçakta fren güçlü, yüksekte zayıf |
| Sürükleme | a = −0,00012 × ρ × Cd(M) × v² | |
| Ses duvarı Cd(M) | 1 → 2,4 → 1,1 (v 85→100→115) | Gerçekteki transonik sürükleme tepesi. Hızın yetmezse "duvara" takılırsın |
| Isı duvarı | v > 250 ve y < 300 iken ısı birikir | Isı kalkanı alınana ya da daha yükseğe çıkılana kadar hız sınırlanır |
| Sekme koşulu | açı < 35° ve v > 25 | Değilse batma |
| Sekme kaybı | %14 (geliştirmeyle %4'e kadar) | Dikey hız × 0,55 (geliştirmeyle 0,75) |
| Rampa çıkış hızı | 70 b/s, 38° | Geliştirmeyle 190'a kadar |
| Göstergede hız | 0–100 → 0–1.235 km/sa (Mach 1), 100–250 → Mach 1–5, 250–600 → Mach 5–23 (7,9 km/s), 600–849 → 7,9–11,2 km/s | Tek yönlü eşleme (kural 7) |

**Kamera.** Roketi ekranın sol üçte birinde tutar. Hızla birlikte geri çekilir (FOV 50° → 65°). Yüksekte deniz ve kavis kadraja girer. Duvar geçişlerinde 0,6 s ağır çekim ve yakın çekim.

**Hedef tur profilleri** (ekonomi simülasyonuyla doğrulanacak):

| Tur | Süre | Mesafe | En yüksek hız | Olay |
|---|---|---|---|---|
| 1 | 18 s | 1,2 km | 70 | Martılar, ilk sekmeler |
| 3 | 30 s | 4 km | 110 | Ses duvarı ilk kez kırılır |
| 10 | 50 s | 25 km | 260 | Isı duvarı |
| 25 | 75 s | 150 km | 600 | Yörünge: süzülme, yıldızlar |
| 40 | 90 s | — | 849 | Kaçış: Ay bölümü açılır |

---

## 6. Dünya bölümü: nesneler

Bantlar: **Deniz** (y 0–40), **Alçak hava** (40–250), **Bulutlar** (250–700), **Üst atmosfer** (700–1.500), **Yörünge** (g_etkin ≈ 0, 1.500+). Hız arttıkça roket doğal olarak üst bantlara çıkar.

| Nesne | Bant | Sıklık | Rokete etkisi | Nesneye ne olur | Ödül | Açılış |
|---|---|---|---|---|---|---|
| Martı sürüsü | Deniz, alçak | Yaygın | −%3 hız, hafif yukarı itiş | Sersemler, tüyleri uçar, takla atıp toparlanır | +10 izlenme | Baştan |
| Şişme reklam balonu | Alçak | Yaygın | Üstten: dikey hızı tersler (trambolin), yatay −%2. Yandan: −%6 | Esner, sallanır, 3. vuruşta patlar | +15 | Baştan |
| Şamandıra | Deniz | Yaygın | Sekme gibi davranır, kayıp %8 (sudan iyi) | Batıp çıkar, çanı çalar | +8 | Baştan |
| Balıkçı ağı | Deniz | Seyrek | Sekme kaybı %45 | Ağ yırtılır, balıklar kaçar | +5 | Baştan (fren) |
| Sahil güvenlik botu | Deniz | Seyrek | Yaklaşırsan ağ fırlatır (1 s uyarı) | Ağ boşa giderse bot döner | — | Tur 4'ten |
| **Yakıt dronu** | Alçak, bulut | Seyrek | +1 dalış hakkı | Bidonu bırakır, dron sallanarak uzaklaşır | +20 | Satın al |
| **Havai fişek mavnası** | Deniz | Seyrek | Üstüne düşersen 1,2 s fişekle yukarı-ileri itilirsin (+60 hız) | Fişekler bitince mavna is içinde kalır | +40 | Satın al |
| **Eski deniz mayını** | Deniz | Seyrek | Patlama ileri iter (+45 hız) | Patlar, su sütunu | +35 | Satın al |
| **Jet akımı** | Bulut | Bant | İçinde kaldıkça +12 hız/s | — (rüzgâr) | +5/s | Satın al |
| Fırtına bulutu | Bulut | Seyrek | Yıldırım: 0,8 s dalış kilidi | Bulut çakar, gök gürler | +25 | Tur 8'den |
| Kargo uçağı (insansız) | Bulut | Nadir | Gövdeye çarpmak: patlama, tur sonu. Kanat ucuna sürtmek: −%30 | Parçalanır, kargo paraşütleri açılır | +200 | Tur 6'dan |
| Kaya adacık | Deniz | Nadir | Çarpma: patlama, tur sonu (2 s önce ufukta) | — | — | Tur 5'ten |
| Hava balonu (bilim) | Üst atmosfer | Yaygın | Trambolin, dikey tersler, yatay −%2 | Gondol sallanır | +30 | Bölge |
| Göktaşı izi | Üst atmosfer | Seyrek | −%5, ısı +5 | Kıvılcım | +20 | Bölge |
| Uydu | Yörünge | Yaygın | Yandan sürtme = **mini sapan** (+25 hız). Gövdeye çarpma: −%20 | Paneli döner, kopabilir | +50 | Bölge |
| Uzay çöpü | Yörünge | Yaygın | −%8 | Parçalara ayrılır (çarpılan bölünür) | +15 | Bölge |
| Uzay istasyonu | Yörünge | Nadir | Yanından geçerken +2 dalış hakkı | Astronot el sallar | +150 | Bölge |
| **Kargo kapsülü** (piñata) | Her bant | Nadir | Çarpınca 3 kart: para, tek tur güç, indirim | Paraşütle düşer, açılır | Kart | Tur 3'ten |
| Rakip zeplini | Rampa yanı | Her tur | Mükemmel kalkış gondola çarpar | Can kaybeder, yamalanır; nakavt olunca söner ve uçup gider | Nakavt: +500 | Baştan |

Kalın yazılanlar Burrito Bison'un özel jöleleri gibi satın alınınca dünyada belirmeye başlar ve yükseltildikçe güçlenir.

**Yerleşim.** Dünya sonsuz akan bir şerit. Nesneler mesafe aralığına, banda ve sıklığa göre tohumlu rastgele yerleşir (§10). İki ölümcül nesne arasında en az 2 km var. Ölümcül nesnenin 300 m yakınına fren nesnesi konmaz. Her 600 m'de en az bir sekme ya da itki fırsatı var. Rotada "kaçınılmaz ölüm" diziliminin olmadığı oluşturma anında test edilir.

---

## 7. Ekonomi ve hangar

**Tek para birimi: İzlenme → Sponsor parası (₺).** Taslak 5'teki "canlı yayın" estetiğiyle tutarlı: uçuşu milyonlar izliyor, her çılgın an izlenmeyi artırıyor, tur sonunda sponsorlar izlenmeye göre ödüyor. Kombo çarpanı: 3 saniye içinde art arda vuruşlar ×1,1'den başlayıp en çok ×3'e çıkar.

Tur kazancı = Σ(nesne izlenmesi × kombo) + mesafe (km başına 4) + duvar ödülleri + zeplin vuruşu.

**Hangar sekmeleri** (her geliştirme 5–10 kademe; fiyat = taban × 1,55^kademe):

| Sekme | Geliştirmeler |
|---|---|
| Rampa | Rampa gücü · Mükemmel bölge genişliği · Zeplin hasarı |
| Gövde | Sekme verimi · Aerodinamik (Cd −) · Ağ kesici · Isı kalkanı (Isı duvarı için) · Kaya zırhı (bir ölümcül çarpmayı −%60 kayıpla atlatır) |
| Motor | Dalış gücü · Gösterge dolum hızı · Dalış kapasitesi (2→4) · Son ateşleme (hız bitince otomatik tek ateşleme) |
| Fırsatlar | Yakıt dronu · Havai fişek mavnası · Deniz mayını · Jet akımı. Her biri aç + sıklık + güç |
| Yayın | İzlenme çarpanı · Kombo süresi · Kargo kapsülü sıklığı |

İlk tur ≈ 120 ₺. İlk geliştirmeler 60–150 ₺. İlk 10 turda her turdan sonra en az bir satın alma yapılabilir. Plüton'a kadar hedef yaklaşık 6–8 saat. **Kodlamadan önce `oyun/ekonomi_b.py` simülasyonu** yazılır: "ortalama oyuncu" botu turları oynar ve her bölüme kaç turda varıldığını, en uzun "satın alamadan geçen tur" dizisini ve hiçbir geliştirmenin işe yaramaz kalmadığını ölçer. Kabul: art arda en fazla 3 tur satın alamadan geçer. Hiçbir duvar 8 turdan fazla oyuncuyu durdurmaz.

---

## 8. Bölümler (Taslak 5'in rotası korunur)

Her bölüm kendi "dünyası": kendi zemini (sekme yüzeyi), yerçekimi, nesneleri ve hız duvarlarıyla. Kaçış hızı bir sonraki bölümü açar. Varılan bölümde bir **üs** kurulur ve sonraki turlar oradan kalkar (Taslak 5'teki checkpoint).

| # | Bölüm | Sekme yüzeyi | Özel kural | Duvarlar |
|---|---|---|---|---|
| 1 | Dünya (Akdeniz) | Deniz | Hava yoğun, ses ve ısı duvarı | Ses · Isı · Yörünge · Kaçış |
| 2 | Ay | Regolit (toz bulutu kalkar, kayıp fazla) | Zayıf yerçekimi, hava yok (sürükleme yok, ama sekme kaybı büyük) | Krater sırtları · Kaçış |
| 3 | Mars | Kum tepeleri ve ince atmosfer | Toz fırtınası, Phobos sapanı | Olympus Mons · Kaçış |
| 4 | Asteroit Kuşağı | Asteroitler (her biri küçük bir zemin) | Kayadan kayaya sekme | Kirkwood boşlukları |
| 5 | Jüpiter | Bulut tepeleri | Dev yerçekimi, en büyük sapan | Radyasyon kuşağı |
| 6 | Satürn | Halka buzları | Halka boşlukları | Halka geçişi |
| 7 | Uranüs–Neptün | Buz bulutları | Karanlık, görüş kısa | Rüzgârlar |
| 8 | Plüton | Azot buzu ovası | Final: Tombaugh Regio'ya iniş mini oyunu | Zafer |

Taslak 5'teki 10 bölüm 8'e indi. Troposfer, Kármán ve Yörünge artık Dünya bölümünün iç bantları. Bölümlerin ayrıntılı tasarımı, Dünya bölümü bitip oyunun "eğlenceli" olduğu kanıtlandıktan sonra yapılır.

---

## 9. His ("juice") listesi

| An | Duraksama | Sarsıntı | Diğer |
|---|---|---|---|
| Hafif çarpma (martı, balon) | 40 ms | 0,15 | Squash %15, tüy ya da konfeti, "pof", +izlenme sayısı uçar |
| Mükemmel sekme | 60 ms | 0,25 | Su halkası, beyaz parlama, "MÜKEMMEL", ses perdesi yükselir |
| Fırsat nesnesi | 90 ms | 0,4 | Özel efekt (fişek, patlama), kısa ağır çekim (×0,4, 0,3 s) |
| Duvar kırılışı | 300 ms | 0,6 | Ağır çekim ×0,2, 0,6 s; şok konisi; tam ekran başlık; müzik katmanı açılır |
| Patlama / batma | 120 ms | 0,8 | Ateş topu ya da su sütunu, parçalar, kaptan paraşütle atlar |

Hız çizgileri, kamera geri çekilmesi ve rüzgâr sesi hızla orantılı. Müzik hızla katman kazanır. Dokunmatik titreşim vuruşun gücüne göre (hareket azaltma ayarıyla kapanır).

---

## 10. Teknik mimari

- **Platform:** Tarayıcı, Three.js r170, tek sayfa + varlık dosyaları; claude.ai Artifact olarak telefondan link. A0'daki altyapı yeniden kullanılır: yayın kısıtları, base64 GLB, uyarlanabilir çözünürlük, test kancaları.
- **Katmanlar:** `ayar` (tüm sayılar) · `dunya` (tohumlu nesne üretimi, bant ve şerit yönetimi) · `fizik` (sabit 120 Hz adım; çarpışmalar daire/kapsül, 2B) · `durum` (rampa → uçuş → duruş → kara kutu → hangar durum makinesi) · `goruntu` (Three.js, kamera, efektler) · `ses` (Web Audio) · `arayuz` · `kayit`.
- **Fizik 2B, görüntü 3B.** Oynanış düzlemde (x, y). Modeller ve derinlik katmanları (arka plan adaları, bulutlar, ufuk) 3B.
- **Belirlenimlilik:** `?seed=` ile aynı tur tekrar üretilir; test botu ve hata ayıklama için şart.
- **Test kancaları:** `?t=`, `?seed=`, `?bot=iyi|kotu|yok` (otomatik oyuncu), `window.__oyun`.
- **Kayıt:** localStorage + Ayarlar'da yedek kodu. Her tur sonu ve her satın alma sonrası otomatik kayıt. Sürüm numaralı kayıt şeması, eski kayıt yeni sürüme taşınır.
- **Performans:** 60 fps. Nesneler örneklemeyle çizilir, havuzlanır (çöp üretmez). Ekranda en fazla ~150 nesne ve 2.000 parçacık. 3 kalite kademesi.

---

## 11. Gözden kaçmasın listesi

| Konu | Karar |
|---|---|
| Kesinti | Arka plana geçince ya da arama gelince otomatik duraklar. Dönüşte "devam" için dokun |
| Ekran | Dikey kilit; çentik ve alt çubuk için güvenli alan; tek elle oynanır (dokunma ekranın her yerinde) |
| İlk açılış | 5 s altında; ilk tur 3 ipucu: "Yeşilde dokun", "Dalış için dokun", "Sığ açıyla sekersin" |
| Ses | İlk dokunuşla başlar; müzik ve efekt ayrı ayrı ayarlanır; sessiz modda da oynanabilir (görsel ipuçları yeterli) |
| Erişilebilirlik | Hareket azaltma (sarsıntı ve flaş kapalı), renk körlüğü (tehlike = üçgen + kırmızı, fırsat = daire + turkuaz), yazı boyutu |
| Haksızlık | Ölümcül nesne uyarısı ≥ 1,2 s; ölümcül dizilim testi; sömürü döngüsü sınırları (kural 8) |
| Takılma | Para sıfırken bile tur kazancı > 0; her zaman alınabilecek bir geliştirme var |
| Ekonomi | Simülasyonla kabul ölçütleri (§7) |
| Kayıt kaybı | Yedek kodu, kayıt şeması sürümü, bozuk kayıtta güvenli varsayılan |
| Telif | Burrito Bison'dan isim, görsel, ses ya da metin kopyalanmaz; yalnızca mekanik fikirler (oyun mekaniği telif konusu değildir). "Jöle ayı" gibi markalaşmış öğeler yok |
| Gerçek bilgi | Bilgi kartlarındaki her gerçek not yayından önce doğrulanır (Taslak 5 kuralı) |
| Dil | Tüm metinler dil dosyasında, Türkçe |
| Oyun sonu | Plüton'a iniş final sinematiği; sonrası zaman yarışı ve rekorlar |

---

## 12. Kabul ölçütleri ("4,5 yıldız" testi)

Her fazın sonunda oyun testçisi ajan ölçer, denetçi onaylar, sonra sen telefonda oynarsın.

| Ölçüt | Hedef | Nasıl ölçülür |
|---|---|---|
| İlk "vay" anı | ≤ 5 s | Test botu + ekran görüntüsü zaman damgası |
| Beceri farkı | İyi zamanlayan bot, hiç dokunmayan bottan ≥ %60 daha uzağa gider | Aynı tohumla 20'şer tur |
| Tur süresi | 18–90 s | Bot ortalaması |
| Yeniden başlatma | ≤ 3 s | Ölçüm |
| Satın alma ritmi | Art arda ≤ 3 tur alışverişsiz | Ekonomi simülasyonu |
| Yenilik ritmi | Her 2–4 turda yeni nesne, bölge ya da rakip | Simülasyon |
| Kare hızı | Ortalama ≥ 58, en düşük ≥ 50 (S24 Ultra) | Senin telefon testin |
| Hata | Konsolda 0 hata, 30 dakikalık bot oyununda çökme yok | Testçi |
| Mantık | §3'teki 8 kuralın her biri için otomatik ya da elle kontrol | Denetçi kontrol listesi |
| Senin kararın | "Burrito Bison'a yakın ve eğlenceli" | Her fazın sonunda sen |

---

## 13. Ekip ve iş akışı

| Ajan | Görevi |
|---|---|
| Ben (yönetmen) | İşi böler, ajanları çalıştırır, sonuçları birleştirir, sana sunar, commit atar |
| `oyun-tasarimci` | Faz şartnameleri, sayılar, ekonomi simülasyonu |
| `uygulayici` | Kod |
| `gorsel-sanatci` | Tarz kareleri (seçenekli), modeller, efektler |
| `ses-tasarimci` | Efektler ve müzik |
| `oyun-testcisi` | Bot oyunları, ölçümler, ekran görüntüsü kontak sayfası, "eğlenceli mi" raporu |
| `denetci` | Her plan ve teslimattan önce: kullanıcının istekleri, mantık kuralları, kapsam kayması |

**Her fazın döngüsü:** tasarımcı şartname yazar → denetçi inceler → ben sana sorulacak kararları sorarım → uygulayıcı kodlar → testçi ölçer → uygulayıcı düzeltir → denetçi onaylar → sen telefonda oynarsın → geri bildirim listesi.

---

## 14. Fazlar

| Faz | İçerik | Bitiş ölçütü |
|---|---|---|
| **B0 · Gri kutu** | Basit şekillerle: rampa göstergesi, uçuş fiziği (g_etkin, sürükleme, sekme), dalış, 5 nesne (martı, balon, şamandıra, ağ, yakıt dronu), ses duvarı, kara kutu, 6 geliştirmelik hangar, kayıt | Kabul ölçütlerinden beceri farkı, tur süresi ve satın alma ritmi tutuyor. Sen "eğlenceli" diyorsun. **Eğlenceli değilse sonraki faza geçilmez.** |
| B1 · Dünya bölümü tam | Tüm nesneler (§6), 4 duvar, zeplin rakipleri, kargo kapsülü, 25+ geliştirme, ekonomi simülasyonu | Dünya bölümü baştan sona oynanıyor (~1,5–2 saat) |
| B2 · Görünüm | Tarz kareleri (3 seçenek) → senin seçimin → modeller, animasyon, efektler, arayüz | Telefonda 60 fps, senin onayın |
| B3 · Ses | Efektler, müzik, hızla değişen katmanlar | Senin onayın |
| B4 · Cila | İlk açılış, ipuçları, erişilebilirlik, 3 roket, denge | §12'nin tamamı |
| B5+ · Bölümler | Ay → Mars → … → Plüton | Her bölüm için aynı döngü |

**Tahmin:** B0 1–2 oturum. B1 2–3. B2 3–4. B3 1–2. B4 2. Dünya bölümü toplam 9–13 oturum. Sonraki bölümler her biri 2–3 oturum.

---

## 15. Kaynaklar

- [Burrito Bison: Launcha Libre resmî sitesi](https://www.burrito-bison.com/)
- [TalkAndroid rehberi: roket dalışı göstergesi, zamanlama, öncelikli geliştirmeler](https://www.talkandroid.com/burrito-bison-launcha-libre-tips-hints-strategies/)
- [GameGrin incelemesi: rakipler, piñatalar, ilerleme, eleştiriler](https://www.gamegrin.com/mobile/burrito-bison-launcha-libre-review/)
- [GameSkinny: özel jöleler rehberi](https://www.gameskinny.com/tips/burrito-bison-launcha-libre-special-gummies-guide-with-tips/)
- [Gamezebo incelemesi: pasta duvarları, rakipler](https://www.gamezebo.com/the-best/burrito-bison-launcha-libre-review-mucha-diversion/)
- Taslak 5: `oyun/tasarim.html` (rota, engel aileleri, kara kutu, hangar fikri)
