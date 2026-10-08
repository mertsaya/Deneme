# B0 · Gri kutu prototip şartnamesi

2026-10-08 (denetim düzeltmeleri işlendi) · Dayanak: `PLAN_B.md` 6.2, `ICERIK.md` Taslak 2, `oyun/KARARLAR.md`, `oyun/sim/ucus_sim.py` · Uygulayan: `uygulayici` · Ölçen: `oyun-testcisi`

**Amaç tek bir soruyu cevaplamak:** "Burrito Bison gibi hissettiriyor ve eğlenceli mi?" Görsel yok, basit şekiller var. Fizik ve sayılar simülasyondan gelir; B0'da ayar değil, his test edilir.

`~` işaretli sayılar tahmin, oyun testinde ilk ayarlanacaklar onlar. İşaretsiz sayılar sim'den gelir, değiştirilmeden önce sim'de ölçülür.

Sim'e yapılan atıflar satır numarasıyla değil **işlev adıyla** yapılır (sim değiştikçe satırlar kayar).

---

## 0. Kapsam

| Dahil | Hariç (B1 ve sonrası) |
|---|---|
| Rampa göstergesi ve kalkış | Rakip zeplini (yerine kalkış primi, §15 S1) |
| Uçuş fiziği: g_etkin, sürükleme, ses duvarı Cd tepesi, üst sönüm, sekme | Isı duvarı, ısı fiziği, tropopoz/Kármán/yörünge ödülleri |
| Dalış (koni yardımı, mükemmel sekme, boş dalış toparlanması) | Ölümcül nesne (kargo uçağı), zırh |
| 5 nesne: martı grubu, reklam balonu, reklam zeplini, uçurtma, yakıt dronu | Kalan 19 B1 nesnesi, nadir olaylar, kapsül |
| Yakıt dronu mini zamanlama oyunu (§7.4) | Diğer fırsatların mini oyunları |
| 1 kademe son şansı (alçakta ve yüksekte) | Kademe sayısı geliştirmesi, son ateşleme |
| Ses duvarı (kırılış + sinematik + ödül) | Diğer eşikler |
| Kara kutu (döküm, "seni durduran", çözen kart) | Rekor balonu, hayalet, grafik |
| 6 kartlık hangar | Diğer geliştirmeler, fırsatlar F2–F10 |
| Kayıt (sürümlü, güvenli varsayılan) | Yedek kodu |
| Ayarlar, duraklat, erişilebilirlik, ışığa duyarlılık | Renk körlüğü modu, satın alma kilidi, istatistik ekranı |
| Basit sentez sesler (§15 S4) | Müzik (ayarlarda müzik çubuğu da yok) |
| Test kancaları, botlar, toplu ölçüm | — |

**Kod kapsamı:** `Ucus` sınıfından yalnız B0'da çalışan dallar taşınır. **Taşınmayan yollar:** ısı/ısı kilidi, termal, jet, kargo/ölümcül, römorkör, zırh, kalkan, rakip zeplini, son ateşleme, fişek, konfeti, uzay bantları (Kármán/yörünge/kaçış). Bu dallar JS'te hiç yazılmaz (bayrakla kapatılmış ölü kod da değil).

**Deniz yok uyarlaması** (KARARLAR "her şey gökyüzünde"). Eski B0 listesindeki deniz nesnelerinin gökyüzü karşılıkları: **şamandıra → reklam zeplini** (iri, güvenilir trambolin; açılış "vay" sekmesini de o verir), **ağ → uçurtma ipi** (altından geçerken takılan fren, ağın yaptığı işi yapar).

### 0.1 Burrito Bison'dan ne alındı

| BB | B0'da | Karar | Neden |
|---|---|---|---|
| Fırlatma göstergesi, kritik bölge | Gidip gelen iğne, yeşil bölge (§3) | Al | İlk saniyede beceri ve heyecan |
| Normal jöleler: sekersin, yavaşlarsın | Balon, zeplin (trambolin), martı (fren) | Uyarla | Tema; sekme hızı artırmaz (mantık kuralı 1) |
| Polis jöleleri (yakalar, yavaşlatır) | Uçurtma ipi | Uyarla | Alçakta kalmanın bedeli |
| Rocket Slam | Dalış: 70° aşağı, koni yardımı, mükemmel sekme | Al | Tek dokunuşluk beceri. BB'de dalış dikine; bizde 70° çünkü roket ileri gidiyor, dikine dalış yatay hızı sıfırlar |
| Satın alınınca çıkan özel jöle (kendi mini oyunuyla) | Yakıt dronu + daralan halka (§7.4) | Al | Harcamanın dünyada görünür sonucu; KARARLAR: her fırsatın kendi mini zamanlama oyunu |
| Pasta duvarı | Ses duvarı (Cd tepesi + kırılış) | Uyarla | Gerçek fiziksel eşik; hasar biriktirmez |
| Yere değince sekme, uzun kalırsan son | Zemin yok; kademe son şansı | At / değiştir | KARARLAR: deniz/zemin yok; ilerleme bir hatayla kaybolmasın |
| Ringdeki rakip | B0'da yok | Ertele | Kapsam; ekonomisi kalkış primiyle korunur |
| Piñata kartları | Yok | Ertele | B1 |
| Dükkân | 6 kartlık hangar | Al | "Bir tur daha" çekimi |

---

## 1. Ekran ve kontrol

- **Cihaz:** Samsung Galaxy S24 Ultra, dikey, tarayıcı (Chrome / Samsung Internet). CSS görünüm ~384 × 832, DPR ~3,75. Güvenli alanlar `env(safe-area-inset-*)`.
- **Tam ekran ve dikey kilit:** ilk dokunuşta (kullanıcı hareketi gerektiği için) `document.documentElement.requestFullscreen()` ve ardından `screen.orientation.lock('portrait')` denenir; ikisi de başarısız olabilir, hata yutulur, oyun devam eder. Yatayda "Telefonu dik tut" kaplaması. Tam ekrandan çıkılırsa yeniden zorlanmaz; bir sonraki UÇ dokunuşunda bir kez daha denenir.
- **Tek dokunuş:** `pointerdown` (gecikmesiz), ekranın her yeri (arayüz düğmeleri hariç). Basılı tutma, kaydırma, çoklu dokunuş yok; aynı anda ikinci parmak yok sayılır. Sayfa kaydırma ve yakınlaştırma kapalı (`touch-action: none`, `user-select: none`).
- **Dokunuşun anlamı uçuşta:** yakıt dronu halkası etkinse (§7.4) dokunuş halkaya gider; değilse dalış (§6).
- **Dokunuş kuyruğu:** duraksama (hitstop) ya da ağır çekim sırasında gelen dokunuş bir sonraki fizik adımında uygulanır; kuyrukta en çok 1 dokunuş.
- **Arayüz yerleşimi** (onaylı konsept `oyun/konsept/oyun_ici_1.jpg` düzeni; B0'da gri):

| Yer | Öğe |
|---|---|
| Üst sol | Bu turun jetonu (jeton simgesi + sayı) |
| Üst orta | Mesafe (`mesafe_g`, km, 1 ondalık; §9.1) |
| Üst sağ | Duraklat düğmesi (56 × 56 dp) |
| Sağ kenar | Dikey irtifa çubuğu (km; B0'da 0–12 km ölçeği) |
| Alt sol | Hız göstergesi: yay + sayı. İç hız < 115 iken km/sa (= `hizGosterge(v)` × 3,6); ≥ 115 iken "Mach x,x" (= `hizGosterge(v)` / 343). **Ses duvarı çentiği iç hız 115'te** (kırılış eşiğiyle aynı) |
| Alt sağ | Dalış düğmesi (yuvarlak, 88 dp): dolum halkası + hak noktaları (kapasite 2). Görseldir, dokunuş ekranın her yerinde çalışır |
| Orta | İpucu yazıları, "MÜKEMMEL", "SON ŞANS", "SES DUVARI!", "TAM DOLUM!" |

---

## 2. Durum makinesi

```
ACILIS ─► HANGAR ◄──────────────┐
            │ UÇ                 │ HANGAR
            ▼                    │
          RAMPA ─► UCUS ─► BITIS ─► KARA_KUTU ─┐
            ▲                                   │ TEKRAR UÇ
            └───────────────────────────────────┘
RAMPA ve UCUS'tan: DURAKLAT (üst katman) ─► DEVAM (3-2-1) | YENİDEN BAŞLA | HANGAR | AYARLAR
HANGAR'dan: AYARLAR
```

| Durum | Süre | Çıkış |
|---|---|---|
| ACILIS | ≤ 5 s ilk yükleme | Kayıt okunur → HANGAR. İlk açılışta ne olacağı kullanıcı kararı bekliyor (§20 K-B) |
| RAMPA | 0,8–3,0 s | Dokunuş ya da 3,0 s → UCUS |
| UCUS | 15–65 s | Bitiş koşulu (§8) → BITIS |
| BITIS | 1,0 s komik son (dokunuşla atlanır) | → KARA_KUTU |
| KARA_KUTU | ≤ 4 s animasyon | TEKRAR UÇ → RAMPA (≤ 0,5 s) · HANGAR (ayrıntı §11) |

**Yeniden başlatma ≤ 3 s:** BITIS (1,0) + KARA_KUTU'da TEKRAR UÇ'a basılana kadar + RAMPA'ya geçiş ≤ 0,5 s. Tur nesneleri havuzdan yeniden kullanılır, sahne yeniden kurulmaz.

---

## 3. Rampa

| Değer | Sayı | Kaynak |
|---|---|---|
| Rampa ucu | x 0, y 60 | sim `rampa_y` |
| Kalkış açısı | 38° | sim |
| Kalkış hızı | 70 + 16 × Rampa gücü sv (B0'da en çok sv 6 → 166) | sim, B0 tavanı §12 |
| Kalite çarpanı | mükemmel ×1,30 · iyi ×1,0 · zayıf ×0,8 | sim |
| Otomatik kalkış | 3,0 s dokunulmazsa "iyi" | sim |
| Kalkış primi (B0) | v_kalkış × {mükemmel 1,0 · iyi 0,4 · zayıf 0} × 0,6 jeton | sim rakip vuruşu (§15 S1) |

**Gösterge** (yay biçimli, ekranın alt üçte birinde, genişlik %70):
- İğne konumu p ∈ [0, 1], **sabit hızlı gidiş-dönüş** (üçgen dalga), tam tur T = **2,0 s~** (gidiş 1,0 s). p 0'dan başlar, artar.
- Bölgeler: kırmızı (zayıf) [0, 0,25) · sarı (iyi) [0,25, 0,96 − b) · **yeşil (mükemmel) [0,96 − b, 0,96)** · sarı [0,96, 1]. b = 0,12 + 0,024 × Mükemmel bölge sv (0,12 → 0,24).
- Neden üçgen dalga: rastgele zamanda dokunan oyuncu yeşili tam b olasılıkla, kırmızıyı 0,25 olasılıkla bulur; bu, sim'deki "kötü" bot modeliyle aynı. Sinüs salınımında uçlarda bekleme olur, bölgeler adaletsizleşir.
- İlk yeşile varış 0,84 s (sim'deki iyi bot rampa süresi 0,8–1,1 s ile tutarlı). Yeşil pencere geçiş başına b / (1/s) = 120 ms (sv 5'te 240 ms).
- Geri bildirim: mükemmel → beyaz halka, "MÜKEMMEL KALKIŞ!", duraksama ve sarsıntı `HIS.mukemmel` (§14), titreşim ~20 ms. İyi → "İYİ". Zayıf → "ZAYIF", iğne kırmızı titrer.
- İlk turda ipucu: "Yeşilde dokun".

---

## 4. Uçuş fiziği

**Aktarım:** `ucus_sim.py` içindeki `Ucus` sınıfının **B0 dalları** (§0 kod kapsamı) JS'e aynı adlarla, aynı işlem sırasıyla aktarılır. Sayılar §16'daki üretilmiş yapılandırmadan okunur; kodda sayı yazılmaz.

- **Sabit adım** dt = 1/120 s, yarı örtük Euler (önce hız, sonra konum). Görüntü kare hızından bağımsız; görüntü iki fizik durumu arasında ara değerler (enterpolasyon).
- **Bir adımın sırası** (`Ucus.adim`): kamera hızı → (10 Hz) yönetmen (`yonet`), fırsat (`firsat_yonet`) ve garanti (`garanti`) → kuvvetler (yerçekimi, sürükleme, sönümler) → tümleştirme → dalış süresi → çarpışmalar (`carp`) → uçurtma ipi (`ip_kontrol`) → istatistik → eşikler → son şans, durma, yer, tavan.
- **Yerçekimi:** g_etkin = 30 × max(0, 1 − (|vx| / 600)²) (`g_etkin`).
- **Sürükleme:** a = 0,00012 × e^(−y/400) × Cd × v², hız vektörüne ters. Cd = Cd_ses(v) × 0,85^(ayrılan kademe) (B0'da Aerodinamik yok).
- **Cd_ses(v)** (`cd_ses`): v ≤ 85 → 1,0; 85–100 → 1,0 → 2,4; 100–115 → 2,4 → 1,1; v > 115 → 1,1 (doğrusal).
- **Üst sönüm:** v < 600 iken y > 300'de ek 7 × min(1, (y − 300) / 3.200) b/s² (hızın tersine). y > 2.900 ve vy > 0 → ek −6 b/s² dikey. (B0'da nadiren devreye girer; eşlik için var.)
- **Isı:** B0'da yok, kodu da taşınmaz. Rampa tavanı sv 6 olduğundan hız 250'yi yalnız kısa dalış anlarında aşar; sim'de bu durumda ısı kilidine varılmaz.
- **Hız tavanı yok.** Hız yalnız kayıtlı kaynaklarla artar (§18 K10).
- **Sayısal güvenlik:** v < 1e−6 iken sürükleme hesaplanmaz.

---

## 5. Çarpışma, sekme, yavaşlatma

- **Biçim:** daire–daire. Roket yarıçapı 4; nesne yarıçapı `r`. Görsel biçim çarpışma dairesinden en çok %15 taşabilir ("gördüğün çarpar").
- **Aday listesi:** 10 Hz'de, roketten |dx| < 0,15·|v| + 80 ve |dy| < aynı (uçurtma dikey sınırsız) olan nesneler.
- **Tekrar:** aynı nesne 2 s içinde ikinci kez etki ve ödül vermez.
- **Trambolin (balon, zeplin):**
  - **Üstten** = roket y ≥ nesne y ve vy < 0,35·|v|. Sonuç: |v'| = |v| × k_etkin, yön nesnenin sekme açısı (balon 50°, zeplin 45°). k_etkin = min(0,92, k + 0,012 × Sekme verimi sv).
  - Dalış süresi içindeyse **mükemmel sekme:** |v'| = |v| + min(0,10·|v|, 12); dalış biter.
  - **Yandan:** hız × (1 − yan kaybı); dalış iptal; göstergeye 0,13.
  - Her temas vuruş sayar; ömür dolunca nesne söner (balon 3 → patlar, zeplin 3 → söner, süzülerek iner).
- **Yavaşlatıcı (martı, uçurtma gövdesi):** hız × (1 − kayıp); martıda yön 2° yukarı döner; nesne etkisizleşir; göstergeye 0,13.
- **Uçurtma ipi:** ip uçurtmadan yere dikine iner. Roket bir adımda uçurtmanın x'ini geçerken uçurtmanın altındaysa (y < y_uçurtma − r) ipe takılır: hız × (1 − 0,15); ip kopar, uçurtma savrulur.
- **Yakıt dronu (fırsat):** temas → dalış göstergesi +1, göstergeye ayrıca +0,30; halka mini oyunu tutturulduysa +0,25 daha (§7.4). Dron bidonu bırakır, sallanarak uzaklaşır.
- **Ödül:** her etkili temasta nesne ödülü (§9).
- **İki taraf kuralı (gri kutuda da görünür):** balon/zeplin temas noktasında %15~ basılır ve 0,3 s~ yaylanır; martı grubu dağılır, 0,5 s sonra toparlanıp uçar; uçurtma takla atar; dron sallanır, bidon düşer.
- **Yandan çarpmada içinden geçme yok (yalnız görüntü):** fizikte roket yandan temastan sonra yoluna devam eder (sim aynen), daireler bir süre üst üste kalabilir. Görüntü bunu gizler: yandan vurulan nesne (trambolin yandan, martı, uçurtma gövdesi, dron) roketin hız yönünde ve roketten dışarı doğru itilir: temas anında nesnenin görsel konumuna, roketten nesneye bakan birim vektör yönünde ~(r_roket + r − d) kadar anında ayrılma, ardından roketin hız yönünde ~0,3 s boyunca ~0,6 × |v| ile başlayıp üstel sönen kayma eklenir. Böylece roket nesneyi sıyırıp geçiyormuş gibi görünür. Bu kayma yalnız görsel ofsettir; fizikteki nesne konumu (çarpışma, ikinci temas kontrolü, sim eşliği) değişmez. Kayma bitince görsel ofset ~0,5 s'de sıfıra döner ya da nesne söndüyse sönme animasyonu ofsetli yerinde oynar.

---

## 6. Dalış

| Değer | Sayı | Kaynak |
|---|---|---|
| Hak | Gösterge ≥ 1,0 → 1 dalış; kapasite 2 | sim |
| Başlangıç | 1,0 (her tur 1 dalışla başlar) | sim `gosterge_bas` |
| Dolum | trambolin üstten 0,08 · mükemmel 0,10 · diğer temas 0,13 · fırsat 0,30 (+0,25 halka tutunca) | sim |
| Hız | |v| + 14 + 4,0 × Dalış gücü sv (10 sv → +54) | sim |
| Yön | 70° aşağı; **koni yardımı:** 66–76° aşağı konide, menzil max(150, |v|) içinde, en yakın uygun trambolinin üst kenarına (y + 0,5r) nişan | sim `dalis_hedef` |
| Süre | 1,2 s (bu sürede üstten trambolin teması = mükemmel) | sim |
| Kural | Dalış sürerken ikinci dokunuş dalış yapmaz; hak yokken dokunuş "boş" titreşimi (düğme 80 ms~ sallanır, ses "tık"), etkisiz | sim `dokun` + PLAN |

- **Görsel:** roket burnu hız yönüne döner; 0,2 s~ alev patlaması; dalış süresince arkada beyaz çizgi. Mükemmel → şok halkası, "MÜKEMMEL!", `HIS.mukemmel`.
- **Hedef vurgusu:** kullanıcı kararı bekliyor (§20 K-A). Uygulayıcı vurguyu `?vurgu=0|1` ile açılıp kapanır kodlar.
- **Boş dalış toparlanması** (KARARLAR 8. oturum, onaylı; **her zaman açık**, `B0.toparlanma = true`; `?toparlanma=0` yalnız sim eşliği testi için kapatır): dokunuşta konide hedef yoksa dalış 0,4 s sürer, sonra yön dalış öncesine döner (−10°…+45° arasına kırpılır), |v| = 0,9 × dalış öncesi |v|. Sayılar (`bos_dalis`) sim bu kuralı içerdiğinde sim'den alınır; içermiyorsa §16'daki B0 değerleri (~) geçerli.
- İpucu: ilk turda gösterge ≥ 1 ve konide ilk kez hedef belirince 1,5 s "Dalış için dokun".

---

## 7. Dünya ve nesneler

### 7.1 B0 nesneleri

| Nesne | Sim adı | r | y | w | Etki | Ödül | Gri kutu görünümü |
|---|---|---|---|---|---|---|---|
| Martı grubu | `marti` | 13 | 25–180 | 3,0 | −%6, 2° yukarı | 20 | 3 beyaz üçgen, merkez çevresinde hafif dalgalanır |
| Reklam balonu | `balon` | 12 | 40–200 | 3,0 | Trambolin k 0,80, 50°, yan −%6, ömür 3 | 15 | Pembe küre, üstünde beyaz yay şeridi |
| Reklam zeplini | `zeplin` | 22 | 80–500 | 1,2 | Trambolin k 0,85, 45°, yan −%10, ömür 3 | 40 | Açık mavi tombul elipsoit (1,25 : 1), üstünde beyaz yay şeridi |
| Uçurtma | `ucurtma` | 7 | 40–220 | 1,5 | Gövde −%2; ip −%15 | 6 | Sarı baklava + yere inen ince çizgi |
| Yakıt dronu | `yakit` (fırsat) | 9 | rota üstü, y ≥ 30 | — | +1 dalış (+0,25 halka) | 20 | Sarı kutu + 4 küçük disk; çevresinde turkuaz halka (fırsat = daire + turkuaz) |

Trambolinlerin üstündeki beyaz yay şeridi "buraya düşülür" işaretidir (şekil kodu; renkten bağımsız).

### 7.2 Yerleşim (sim'le aynı mantık)

- **Yoğunluk yönetmeni** (10 Hz, `yonet`): ekranda her an ~7 nesne. Üretim bölgesi: görünür alan + önündeki bir ekran, üstte/altta yükseklik × 0,3, y ≥ 25; yeni nesneler **gerçek görünür alanın** dışına konur (ilk doldurma hariç; görünür alan tanımı §14 Kamera). Tür seçimi o yükseklikte açık türler arasında `w` ağırlığıyla. Arkada bir ekrandan fazla kalanlar havuza döner.
- **Açılış zeplini** (`kalkis`): kalkıştan 1,8 s sonraki rota noktasına (x + 4, y = max(65, y_rota − 11)) bir zeplin. "Vay" anını garanti eder.
- **Sekme garantisi** (`garanti`): **fiilen 0,3 s'de bir** (sim sayacı 0,25'ten başlar, 10 Hz döngüde 0,1 düşer, üçüncü adımda ≤ 0 olur; sayaç mantığı aynen taşınır). 6 s'lik pasif rotanın altında en az 15 b aşağıda bir trambolin yoksa, rotanın uzak yarısına (mümkünse ekran dışı) bir tane konur.
- **Yakıt dronu** (`firsat_yonet`): satın alındıysa ortalama 30 s / (1 + 0,25 × Sıklık sv) aralıkla (ilk: aralık × (0,3–1,0)), rotada 1,6–2,6 s ileriye, y sapması σ 12, y ≥ 30. Turda en çok 5.
- **Rastgele:** tüm dünya üretimi `?seed=` tohumlu tek kaynaktan (§17.3); çekim sırası sim'deki çağrı sırasıyla aynı. Botun rastgelesi ayrı kaynak (sim'deki gibi).
- **Yoğunluk farkı notu:** B0'da `parti` (parti balonu) yok; aynı yoğunlukta pay balon ve zepline kayar. Sim eşliği testinde `?tipler=` ile eklenir (§18 K8).
- **Liste temizliği:** sim etkisiz/geride kalan nesneleri liste süzerek atar. JS'te bu **sırayı koruyan yerinde sıkıştırma** ile yapılır (okuma/yazma indisi, kalanlar öne kayar, dizi boyu kısaltılır, atılan nesne havuza döner). Sıra korunur çünkü çarpışma ve hedef seçim sırası sim'le aynı olmalı; yeni dizi oluşturulmaz (§19 "uçuşta `new` yok").

### 7.3 Arka plan

Gök y ile koyulaşır: y 0 açık mavi → y 1.000 lacivert (onaylı minyatür kararı: mavi → lacivert). Yer y = 0'da düz yeşil şerit (yeryüzü dekoru tarla, KARARLAR 8. oturum; B0'da yalnız şerit). 3 katman paralaks bulut (z −50, −150, −400), oynanışa girmez.

### 7.4 Yakıt dronu mini oyunu (kullanıcı kararı: B0'a mini oyunla girer)

> **Öneri olarak işaretli:** aşağıdaki ayrıntılar (pencere süreleri, halka biçimi, sonuç metinleri) gri kutuda kullanıcıya gösterilir; beğenilmezse sayılar ve biçim ayarlanır. Değişmeyecek olanlar: tek dokunuş, başarıda +0,25 gösterge (sim `firsat_al`), rastgele sayı çekim sırası.

**Fikir:** dron yaklaşırken çevresindeki turkuaz halka daralır. Halka dronun gövdesine oturduğu anda dokunursan bidon tam dolar.

| Öğe | Değer |
|---|---|
| **Tetik (halka başlar)** | Dron etkin, roketin önünde (dx > 0) ve tahmini temas süresi τ = (dx − (r + 4)) / max(vx, 1) ≤ **0,8 s~**. Dron rotadan uzaksa da (|dy| büyük) halka çalışır; tutturmak temas olmadan bir şey vermez |
| **Halka** | Yarıçap = (r + 4) × (1 + 2 × τ / 0,8~) → 3 katından dronun çarpışma çemberine daralır. Gri kutuda turkuaz kalın çember, dronun kendi çemberi ince beyaz |
| **Başarı penceresi** | τ ≤ **0,25 s~** (halka ≤ ~1,6 katı) ile temastan sonraki **0,05 s~** arası. Halka bu aralıkta yeşile döner (şekil kodu: çember kalınlaşır) |
| **Süre** | Halka toplam ≤ 0,8 s~ görünür; dron roketin arkasına geçince (dx < −(r + 4)) ya da temas + 0,05 s~ sonra kaybolur |
| **Dokunuş** | Halka etkinken dokunuş **yalnız halkaya** gider, dalış yapmaz (sim `dokun` notu: "fırsat halkası varsa onu, yoksa dalış"). Dalış sürerken de halkaya dokunulabilir. Halka başına tek deneme: ilk dokunuş sonucu belirler |
| **Başarı** (pencerede dokunuş ve temas oldu) | Gösterge: +1 + 0,25 + 0,30 (sim sırasıyla: `gosterge = min(kap, gosterge + 1 + 0,25)`, sonra `gosterge_ekle(0,30)`); "TAM DOLUM!"; `HIS.firsat` + ek parıltı; sayaç `firsat_tut` +1 |
| **Erken dokunuş** (halka etkin, pencere dışında) | Deneme yanar; halka kırmızımsı griye döner, "ERKEN"; temas olursa normal ödül: +1 + 0,30 |
| **Dokunmadan temas** | Normal ödül: +1 + 0,30. Ceza yok |
| **Tutturdu ama temas yok** | Hiçbir şey (bidon alınmadı); dron sallanarak uzaklaşır |
| **İlk karşılaşma ipucu** | Kayıtta `ipucu.yakit` false ise halka ilk başladığında tek satır: **"Halka daralınca dokun: tam dolum!"** (1,5 s); gösterildikten sonra true yazılır. Aynı turda başka yeni kural ipucu gösterilmez (KARARLAR: turda en çok bir yeni kural) |

**Rastgele eşlik (zorunlu):** sim `firsat_al` içinde `firsat_tut()` dünya üretecinden (`s.rng`) **temas anında tam bir** `random()` çeker. JS de temas anında, aynı yerde (gösterge eklenmeden önce) dünya üretecinden bir sayı **her zaman** çeker:
- **Bot oynuyorsa** (`?bot=`, `?toplu`, `?kampanya`, `__oyun.tur`): sonuç = çekilen < `BOTLAR[bot].tut` (sim'le aynı). Görüntülü bot modunda bot, sonuç başarılıysa pencerede görünür bir dokunuş halkası çizer (yalnız görüntü).
- **İnsan oynuyorsa:** sayı çekilir ve atılır; sonuç insanın halka dokunuşundan gelir. Böylece insanın beceri sonucu ne olursa olsun dünya üretim dizisi (sonraki nesneler) bozulmaz.

**Bot tut oranlarıyla karşılaştırma (ölçüm, geçme şartı değil):** sim botları `tut` hic 0 · kötü 0,25 · orta 0,35 · iyi 0,50 · usta 1,0 varsayar. İnsan testinde gerçek tutturma oranı `firsat_tut / firsat` olarak kara kutu günlüğüne yazılır; 0,25–0,50 dışındaysa pencere (0,25 s~) ayarlanır.

---

## 8. Son şans ve bitiş

- **Kademe:** B0'da 1 son şans. Tetikler (sim `adim` sonu, sırasıyla):
  - **Alçakta:** y < 25 ve vy < 0, kademe > 0 → `kademe_ates('yer')`.
  - **Durma:** hız 2 s boyunca < 25 **ya da** y > 1.000 (tropopoz) iken yatay hız 2 s boyunca < 110 (`vx_dur`). Kademe varsa **her irtifada önce kademe ateşlenir** (`kademe_ates('durma')`); yoksa tur biter. (KARARLAR 8. oturum; eski "y < 300" şartı ve `?kademe_ust` seçeneği kaldırıldı.)
- **Sonuç** (`kademe_ates`): vx' = 0,9·vx + 15 + 6,5 × Kademe itkisi sv; vy' = 78 + 6,5 × sv; **y > 1.000 ise vy' × 0,5** (`kademe_ust_vy_kat`, ileri ağırlıklı); sürükleme × 0,85; dalış iptal; durma sayacı sıfırlanır.
- **His:** `HIS.son_sans` (duraksama + ağır çekim), "SON ŞANS" + kalan kademe simgesi; alt kademe (gri silindir) ayrılır, küçük paraşüt açılır, yere süzülür; roket kısalır.
- **Bitiş koşulları** (sim sırası):
  - `yer`: kademe yokken y ≤ 0.
  - `durma`: kademe yokken durma tetiği (yukarıda) 2 s sürdü.
  - `sure`: tur (rampa + uçuş) 65 s.
- **BITIS sahnesi (1,0 s):** içeriği kullanıcı kararı bekliyor (§20 K-C). Kesin olan: süre 1,0 s, dokunuşla atlanır, `HIS.bitis`, pilot kapsülde kalır (KARARLAR).

---

## 9. Ekonomi (B0)

| Kalem | Formül | Kaynak |
|---|---|---|
| Nesne ödülü | ödül × kombo × (1 + 0,10 × İzlenme sv; B0'da 0) × 0,10 × 2,4 | sim `odul` |
| Kombo | 3 s içinde art arda vuruş: ×(1 + 0,05 × n), tavan ×2,0; tüm çarpanlar en çok ×4 | sim |
| Mesafe | iç x / 1.000 × 70 | sim `km_odul` |
| Sponsor tabanı | 25 (tur doğal bitişle bittiyse) | sim |
| Kalkış primi | §3 (tur doğal bitişle bittiyse) | sim rakip vuruşu |
| Ses duvarı | İlk kırılış 300, sonrakiler 30 | sim `DUVARLAR` |

- **Elle bitirilen tur** (duraklat menüsünden YENİDEN BAŞLA / HANGAR, ya da yarım kalan tur `bekleyen`): yalnız **nesne + mesafe + ses duvarı** kazancı (o ana kadar kazanılmış olanlar) verilir; **sponsor tabanı ve kalkış primi verilmez.** Neden: rampadan hemen sonra çıkıp her seferinde taban + prim toplamak sömürüdür. Kara kutu dökümünde bu iki satır "—" olarak görünür.
- **Uçan sayılar jeton** (KARARLAR 8. oturum, onaylı): temas noktasından yükselen "+4" (yuvarlanmış), kombo ≥ ×1,2 iken yanında "×1,3".
- **Jeton sayacı** üst solda bu turun toplamını gösterir; mesafe ve taban kara kutuda eklenir.
- Tur 1 beklenen kazanç: iyi oyuncu ~170, dokunmayan ~120 (sim).

### 9.1 Mesafe: iki ölçü

| Ölçü | Tanım | Nerede |
|---|---|---|
| `mesafe_g` | Gösterge mesafesi: her adımda `hizGosterge(v) × (vx / v) × dt / 1000` toplanır (km; sim `adim`) | Üst orta sayaç, kara kutu "Mesafe" satırı, rekor (`rekor.mesafe_g`), kara kutu "YENİ!" |
| iç x | Fizik x (b) | Mesafe ödülü (`km_odul`), K3 beceri farkı ölçümü, sim eşliği |

---

## 10. Ses duvarı

- **Fizik:** Cd tepesi (§4) 85–115 arasında hızı yer. Kırılış: v ≥ 115 kesintisiz 0,3 s.
- **Gösterge:** hız yayında ses duvarı çentiği **iç hız 115'te** (kırılış eşiği). 85–115 arasında yay titrer, "SES DUVARI" etiketi belirir. 115 üstünde sayı "Mach x,x"e döner (§1).
- **İlk kırılış sinematiği:** `HIS.ses_ilk` (duraksama → ağır çekim) → roketin çevresinde beyaz şok konisi (gri kutuda yarı saydam koni) → tam ekran başlık "SES DUVARI!" + "+300". Işığa duyarlılık kurallarına uygun (§13.4): parlama yok, koni opak değil.
- **Sonraki kırılışlar:** `HIS.ses_sonra`, küçük koni, "+30".
- **Kayıt:** ilk kırılış turu saklanır (`duvar.ses`).
- **Kara kutu:** bu tur kırılmadıysa ilgili "seni durduran" kuralı (§11).

---

## 11. Kara kutu

**Zamanlama ve dokunuş:**
- Animasyon ≤ 4 s. Açıldıktan sonra **düğmeler 0,3 s~ kilitli** (uçuştan kalan dokunuş yanlışlıkla basmasın).
- Animasyon sürerken **düğme dışı dokunuş** animasyonu sona atlar (tüm sayılar son değerine).
- Animasyon sürerken **TEKRAR UÇ** (kilit bittiyse) animasyonu beklemeden hemen yeniden başlatır.

Düzen yukarıdan aşağı:

1. Başlık: "UÇUŞ RAPORU" · tur no.
2. Toplam jeton (0,8 s sayarak artar).
3. Döküm satırları: Nesneler (n vuruş) · Mesafe (`mesafe_g`, x,x km) · Kalkış primi · Sponsor tabanı · Ses duvarı (varsa). Elle bitirilen turda prim ve taban "—" (§9).
4. Rekorlar: en yüksek hız, mesafe (`mesafe_g`); yeni rekorsa "YENİ!".
5. **Seni durduran şey** (ilk uyan kural). Koşullar kesin; **metinler kullanıcı kararı bekliyor** (§20 K-C). Kod metinleri anahtardan okur:

| Sıra | Koşul | Metin anahtarı | Yer tutucular |
|---|---|---|---|
| 1 | Ses duvarı **bu tur** kırılmadı ve bu turun en yüksek hızı ≥ 85 | `durduran.ses` | {Δ} = (hizGosterge(115) − hizGosterge(max_v)) × 3,6, km/sa, tam sayı |
| 2 | Bitişte gösterge ≥ 1,0 | `durduran.dalis` | — |
| 3 | Bu tur ≥ 2 uçurtma ipi | `durduran.ip` | {n} |
| 4 | `durma` ve y > 1.000 | `durduran.yuksek` | — |
| 5 | `durma` | `durduran.durma` | — |
| 6 | `yer` | `durduran.yer` | — |
| 7 | `sure` | `durduran.sure` | — |

6. **Bunu çözen kart:** aday = B0 kartlarından maks olmayanlar; puan = değer / fiyat; değer sim `deger()` işlevinden (bot = "iyi"; son 3 turda hiç dalış yoksa bot = "hic", bu durumda kart Rampa gücünü önerir). Kart: ad, fiyat, "Şimdi alınabilir" ya da "{eksik} jeton (≈ {n} tur)", n = ⌈eksik / son 3 tur ortalaması⌉. Karta dokunmak hangarı o kart vurgulu açar.
7. Düğmeler: **TEKRAR UÇ** (büyük, birincil) · **HANGAR**.

---

## 12. Hangar (6 kart)

Konsept `oyun/konsept/hangar_1.jpg` düzeni: üstte toplam jeton, ortada roket (gri kutu), altta 2 × 3 kart, en altta büyük **UÇ** düğmesi, sol altta ayarlar dişlisi.

| # | Kart | Sim satırı | Sv | Fiyatlar (jeton) | Kartta görünen etki |
|---|---|---|---|---|---|
| 1 | Rampa gücü | `rampa` | **6** (B0 tavanı; sim 10) | 60 · 93 · 144 · 223 · 346 · 537 | Kalkış hızı (km/sa): 70 → 166 b/s |
| 2 | Mükemmel bölge | `bolge` | 5 | 80 · 124 · 192 · 298 · 462 | Yeşil bölge %12 → %24 |
| 3 | Sekme verimi | `verim` | 8 | 90 · 140 · 216 · 335 · 519 · 805 · 1.248 · 1.934 | Sekmede korunan hız %80 → %90 (balon) |
| 4 | Dalış gücü | `dalis` | 10 | 70 · 109 · 168 · 261 · 404 · 626 · 971 · 1.505 · 2.332 · 3.615 | Dalış itişi +14 → +54 |
| 5 | Kademe itkisi | `kademe_itki` | 8 | 200 · 310 · 481 · 745 · 1.154 · 1.789 · 2.773 · 4.299 | Son şans fırlatması: dikey 78 → 130, ileri +15 → +67 |
| 6 | Yakıt dronu | `yakit_ac` → `yakit_s` | 1 + 4 | 150 (aç) · 100 · 155 · 240 · 372 | Aç: "Yakıt dronları çıkar (+1 dalış; halkayı tuttur, tam dolum)". Sıklık: ortalama aralık 30 → 15 s |

- Fiyatlar JS'te hesaplanmaz: §16 betiği sim `fiyat()` çıktısını kart başına hazır liste olarak yazar (Python/JS yuvarlama farkı ortadan kalkar). Tablodaki sayılar bilgi amaçlı; fark varsa üretilen liste geçerli.
- Görünürlük: hepsi tur 1'den (B0 küçük olduğundan sim'deki tur 2 görünürlüğü kaldırıldı: `bolge`, `yakit_*`; ekonomi etkisi ölçülür).
- Kart durumu: alınabilir (canlı) · yetersiz (gri, eksik jeton yazılı) · MAKS. Seviye noktaları n / maks.
- Satın alma: tek dokunuş; jeton düşer, kart 120 ms~ ×1,15~ zıplar, roketin üstünde ilgili parça bir ton açılır, kayıt yazılır. Geri alma yok (B0).
- **Rampa tavanı gerekçesi:** sv 6'da mükemmel kalkış 166 × 1,3 = 216 b/s < 250: ısı B0'da yok, tavan bu yüzden.

---

## 13. Kayıt, ayarlar, duraklat, erişilebilirlik

### 13.1 Kayıt

- localStorage anahtarı `sdp_kayit`. Şema:

```json
{ "v": 1, "jeton": 0, "tur": 0,
  "sv": { "rampa": 0, "bolge": 0, "verim": 0, "dalis": 0, "kademe_itki": 0, "yakit_ac": 0, "yakit_s": 0 },
  "duvar": { "ses": null },
  "rekor": { "mesafe_g": 0, "max_v": 0, "max_y": 0 },
  "son": [], "son_dalis": [],
  "ipucu": { "rampa": false, "dalis": false, "sekme": false, "yakit": false },
  "ayar": { "efekt": 80, "titresim": true, "hareket_azalt": null, "isik": false, "yazi": 1.0, "kalite": "oto" },
  "bekleyen": null }
```

- `son`: son 3 tur kazancı; `son_dalis`: son 3 turun dalış sayısı (kara kutu kartı için).
- Yazma: her tur sonu (KARA_KUTU açılmadan önce), her satın alma, her ayar değişikliği.
- **Yarım kalan tur ve çift sayım önlemi:**
  - Sayfa gizlenince (`visibilitychange` → hidden, `pagehide`) o ana kadarki **elle bitirme kazancı** (§9: nesne + mesafe + ses duvarı) `bekleyen`e yazılır (jetona eklenmez).
  - Sayfa yeniden **görünür olunca** (aynı oturum, tur sürüyor) aynı yazımda `bekleyen = null` yazılır; tur kaldığı yerden duraklatılmış devam eder.
  - **Her tur sonu yazımında** jeton += tur kazancı ve `bekleyen = null` **aynı yazımda** yapılır (tek `setItem`).
  - Açılışta `bekleyen` doluysa (sayfa gizliyken öldürülmüş): jetona eklenir, "Yarım kalan uçuş: +X jeton" bildirimi, aynı yazımda `bekleyen = null`.
  - Böylece bir tur kazancı en çok bir kez sayılır; kesinti hiçbir şey kaybettirmez.
- **Bozuk kayıt:** JSON hatası ya da şema dışı değer → bozuk metin `sdp_kayit_bozuk` anahtarına taşınır, varsayılan kayıtla devam, "Kayıt okunamadı, yeni başlangıç" bildirimi. Çökme yok.
- **Sürüm taşıma:** `tasi(kayit)` işlevi `v`ye göre adım adım günceller (B0'da yalnız v1).
- `?kayit=0` → hiç okuma/yazma (testler).

### 13.2 Ayarlar

HANGAR'daki dişliden ve DURAKLAT menüsünden açılır.

| Ayar | Seçenekler | Varsayılan |
|---|---|---|
| Efekt sesi | 0–100 | 80 |
| Titreşim | Açık / kapalı | Açık |
| Hareket azaltma | Açık / kapalı | `prefers-reduced-motion` değeri |
| Işığa duyarlılık modu | Açık / kapalı | Kapalı |
| Yazı boyutu | Normal / Büyük / Çok büyük (×1,0 / ×1,2 / ×1,4) | Normal |
| Kalite | Otomatik / Düşük / Orta / Yüksek: piksel oranı = min(cihaz DPR, **1,0 / 1,5 / 2,0**). **Otomatik** 2,0 ile başlar; uçuşta 2 s boyunca kare hızı < 55 ise 1,5'e iner | Otomatik |
| Kaydı sıfırla | İki adımlı: "Kaydı sıfırla" → "Emin misin? Tüm jeton ve geliştirmeler silinir" → "Sil" / "Vazgeç" | — |

Müzik ayarı B0'da yok (müzik yok; B1'de eklenir).

### 13.3 Duraklat

- **Düğme:** üst sağ, 56 × 56 dp; dokunuşu dalış sayılmaz.
- **Otomatik:** `visibilitychange` (hidden), `pagehide`, `blur` → aynı karede duraklar (fizik adımı durur). **İstisna:** `?toplu`, `?kampanya` ve görüntüsüz `?t=` modlarında `blur` otomatik duraklatması kapalı (arka planda çalışan Playwright testleri durmasın).
- **Menü:** DEVAM · YENİDEN BAŞLA · HANGAR · AYARLAR. YENİDEN BAŞLA ve HANGAR turu **elle bitirme** kazancıyla bitirir (§9: taban ve kalkış primi yok).
- **Devam:** 3-2-1 sayımı (her biri 0,5 s); sayım sırasında dokunuşlar yok sayılır; RAMPA'da iğne de durur.

### 13.4 Erişilebilirlik ve ışığa duyarlılık

- Dokunma hedefleri ≥ 48 dp, aralarında ≥ 8 dp. Menüler HTML düğmeleri, `aria-label` Türkçe.
- **Şekil kodu (renkten bağımsız, her zaman açık):** trambolin = yuvarlak + üstte beyaz yay şeridi; fırsat = turkuaz daire halkası; yavaşlatıcı = köşeli biçim (üçgen martılar, baklava uçurtma). Dron halkasının başarı penceresi renk yanında kalınlıkla da belirtilir.
- Yazılarda 2 px koyu kontur; kontrast ≥ 4,5 : 1. Yazı boyutu ayarı tüm arayüzü ölçekler, taşma olmaz.
- **Hareket azaltma:** sarsıntı 0; tam ekran parlama yok; hız çizgileri %30; kamera geçişleri yumuşak. Ağır çekim (oynanışın parçası) kalır.
- **Işığa duyarlılık modu ve her zaman geçerli kurallar** (güvenlik sınırı, ayar değil): tam ekran flaş saniyede en çok 3 (genel sınırlayıcı); mükemmel sekme parlaması ekranın en çok %30'u ve < 100 ms; kırmızı-beyaz titreşim yok; ağır çekim parlaklık oynatmaz. Mod açıkken parlamalar tamamen kapanır, yerine kontur halkası.
- **Sessiz oynanabilir:** her ses olayının görsel karşılığı var.
- **Titreşim** (`navigator.vibrate`): hafif temas ~10 ms · mükemmel ~20 · tam dolum ~20 · son şans ~40 · ses duvarı ~[30, 40, 60]. Ayardan kapanır.

---

## 14. His ("juice") ve ses (gri kutu ölçeği)

BB tarzı: vuruşlar abartılı ve tok. **Bu bölümdeki tüm sayılar tahmindir (~).** Tabloda başlangıç değeri ve oyun testinde denenecek aralık var; önce aralığın orta-üstünden başlanır, "fazla" denirse aşağı inilir.

| An | Duraksama (ms) | Sarsıntı | Diğer |
|---|---|---|---|
| Hafif çarpma (martı, balon yandan, uçurtma) | ~40 (30–60) | ~0,15 (0,10–0,25) | Nesne ~%15 basılır, ~4–6 parçacık, "+N" |
| Trambolin sekmesi | ~60 (40–80) | ~0,25 (0,15–0,35) | Nesne basılıp yaylanır, ses perdesi kombo ile yükselir |
| Mükemmel sekme / mükemmel kalkış | ~90 (60–120) | ~0,40 (0,30–0,50) | Şok halkası, "MÜKEMMEL!" |
| Yakıt dronu (fırsat) | ~90 (60–120) | ~0,40 (0,30–0,50) | ~×0,4 (0,3–0,5) ağır çekim ~0,3 s (0,2–0,4), bidon roketin üstüne uçar; tam dolumda ek parıltı |
| Son şans | ~200 (150–250) | ~0,50 (0,40–0,70) | ~×0,3 (0,2–0,4) ağır çekim ~0,5 s (0,4–0,7) |
| Ses duvarı (ilk) | ~300 (250–400) | ~0,60 (0,50–0,80) | ~×0,2 (0,15–0,3) ağır çekim ~0,6 s (0,5–0,8) |
| Ses duvarı (sonraki) | ~120 (80–150) | ~0,30 (0,20–0,40) | — |
| Bitiş | ~120 (100–200) | ~0,80 (0,60–1,00) | §20 K-C sahnesi |

- **Sarsıntı:** genlik = değer × ekran genişliğinin ~%2'si, ~200 ms üstel sönüm. Hareket azaltmada 0.
- **Duraksama ve ağır çekim** fizik adım sayısını azaltır (gerçek zaman ile fizik zamanı ayrışır); belirlenimlilik bozulmaz. Botlar fizik zamanında karar verir.
- **Kamera:** oynanış dikdörtgeni sim'deki `ekran()` ile aynı: genişlik W = min(500, 150 + 0,5 × v_kamera), yükseklik 2,1 × W, sol kenar x − W/3, dikey merkez max(y, H/2 − 10). v_kamera = hızın 0,8 s zaman sabitli yumuşatılmışı. Perspektif kamera, dikey görüş açısı 50°.
  - **Genişlik her zaman W'ye oturur** (ileriyi görmek oynanışın kendisi); ekran oranı farkı yalnız **üst/altta** kalır, yan bant yok. Ekran 2,1'den uzunsa üstte/altta fazladan gök görünür; kısaysa (tarayıcı çubukları, tam ekran reddedildi) oynanış dikdörtgeninin üstü ve altı eşit kırpılır.
  - **Gerçek görünür alan** = W genişlik × (W × gerçek ekran oranı) yükseklik, aynı merkezle. Yönetmenin "görünen alanın dışına koy" kuralı ve ekrandaki nesne sayımı bu alana göre yapılır (nesneler gözün önünde belirmez).
  - **Görüntüsüz modlar** (`?toplu`, `?kampanya`, `__oyun.tur`) sim'in 2,1 oranını kullanır; sim eşliği bu modlarda ölçülür. Görüntülü oyunda gerçek oran kullanıldığı için tam eşlik beklenmez (eşlik zaten istatistiksel, §17.3).
- **Sesler** (Web Audio sentez, §15 S4; süre ve perdeler ~): sekme "boing" (sinüs 300 → 600 Hz, 120 ms; kombo başına +1 yarım ton) · martı "pof" (gürültü 60 ms) · ip "tınn" (testere 180 Hz, 150 ms) · dalış "vuuş" (bant geçiren gürültü süpürmesi 250 ms) · mükemmel "ding" (880 + 1.320 Hz, 200 ms) · dron halkası daralırken yükselen "vııın" (sinüs 400 → 800 Hz, halka süresince), tam dolum "şıkırt" (880 Hz + gürültü, 150 ms) · son şans "pat" + alçak gümbürtü · ses duvarı "BUM" (60 Hz sinüs + gürültü, 400 ms) · boş dokunuş "tık" · satın alma "çın". İlk dokunuşla `AudioContext` başlar.

---

## 15. Sorulacaklar (varsayılanlı)

Varsayılanlar yalnız uygulamanın beklememesi için; kullanıcı cevabıyla değişir. Varsayılansız bekleyen kararlar §20'de.

**S1. B0'da rakip zeplini.** (a) Gri kutu olarak dahil: rampanın yanında can çubuklu zeplin, mükemmel kalkış ona çarpar, hasar turlar arası birikir (R1: 700 can, nakavt 500). BB'nin ring rakibi hissi B0'da test edilir. (b) Hariç; ekonomi aynı formülle "kalkış primi" olarak korunur. **Varsayılan: (b)** (kapsam listesine sadık). Öneri: B0 sonrası ilk iş (a).

**S4. B0'da ses.** (a) §14'teki basit sentez efektler. (b) Tamamen sessiz (ses B3'te). **Varsayılan: (a).** BB hissinin yarısı ses; gri kutuda bile vuruşun hissedilmesi için gerekli.

Karara bağlananlar (artık soru değil): boş dalış toparlanması her zaman açık (§6), yüksekte kademe her zaman önce ateşlenir (§8), uçan sayılar jeton (§9), yakıt dronu mini oyunla (§7.4) — KARARLAR 8. oturum ve koordinatör bildirimi.

---

## 16. Yapılandırma (sim'den üretilir)

Sayılar elle kopyalanmaz. Küçük bir betik sim'den JSON üretir; sim değiştikçe yeniden koşulur.

**Betik:** `oyun/b0/araclar/ayar_uret.py` (≈ 60 satır, yalnız standart kütüphane).
1. `oyun/sim/ucus_sim.py`'yi modül olarak içe aktarır (ana işlevi çalıştırmaz).
2. Okuduğu nesneler ve süzme:

| Nesne | Ne alınır |
|---|---|
| `AYAR` | Tamamı (düz sayılar; B0'da kullanılmayan anahtarlar zararsız, süzme ayrışma riski doğurur). `kademe_ust_vy_kat` buradan gelir |
| `SONUM_ALT` | Tamamı |
| `DUVARLAR` | Yalnız `ses` |
| `TIPLER` | Yalnız `balon`, `parti`, `zeplin`, `marti`, `ucurtma` (`parti` yalnız eşlik testi için); **sim'deki anahtar sırası korunur** (tür seçimi sırası rastgele eşliği için önemli) |
| `FIRSATLAR` | Yalnız `yakit` |
| `GELISTIRME` | Yalnız B0 kart satırları: `rampa`, `bolge`, `verim`, `dalis`, `kademe_itki`, `yakit_ac`, `yakit_s` |
| `fiyat()` | Her B0 satırı için sv 0…maks−1 fiyat listesi → `fiyatlar` (JS fiyat hesaplamaz) |
| `BOTLAR`, `BOT_SIRA` | Tamamı |
| `HIC_SIFIR` | B0 satırlarına süzülmüş |
| `IRTIFA_TABLO` | Tamamı |
| `deger()` | İşlev; JS'e elle aktarılır (yalnız B0 kart dalları), birim testi aynı girdilerde sim çıktısıyla karşılaştırır |

3. Python demetleri → dizi, sözlükler sırası korunarak (`json.dumps(..., sort_keys=False)`), hesaplanmış ifadeler (ör. `_YK − 100`, `v_kacis`) değer olarak.
4. **`SABIT_EK`:** sim kodunun içine gömülü sayılar. Betiğin içinde elle tutulan küçük sözlük; her girdinin yanında sim işlev adı yorum olarak. Sim bunları sabite taşırsa betik doğrudan okur. B0 için gereken girdiler:
   - `ust_vy_oran: 0.35` (`carp`), `marti_donus_derece: 2` (`carp`)
   - `acilis_zeplin: { dx: 4, y_min: 65, r_kat: 0.5 }` (`kalkis`)
   - `cam_tau: 0.8` (`adim`), `yonet_ara: 0.1` (`adim`)
   - `yonet: { on_ekran: 1, dikey_pay: 0.3, y_min: 25, deneme: 8 }`, `temizlik: { arka_ekran: 1, dikey_ekran: 2.5, sonuk_sure: 0.5 }` (`yonet`)
   - `garanti_ara: 0.25` (`adim`; fiilen 0,3 s, §7.2), `rota_sure: 6.0`, `rota_adim: 0.1` (`rota`), `garanti_pay_kat: 0.6`, `garanti_y_min: 30`, `garanti_x0: 20` (`garanti`)
   - `firsat: { ilk: [0.3, 0.7], sonra: [0.7, 0.6], tau: [1.6, 1.0], y_sapma: 12, y_min: 30 }` (`firsat_yonet`)
   - `yakit: { tut_ek: 0.25, cift_sv: 4, ek_sv: 2, ek: 0.25 }` (`firsat_al`; B0'da `yakit_g` yok, yalnız `tut_ek` etkin)
   - `aday: [0.15, 80]` (`adim`)
   - `bot_karar_ara: 0.05`, `tohum_bot: [7919, 13]`, `tohum_tur: 1000`, `tohum_alici: [31, 7]` (bot/kampanya işlevleri)
5. **Çıktı:** `oyun/b0/ayar.json` ve `oyun/b0/index.html` içindeki `<script type="application/json" id="ayar">` bloğu (tek dosya yayın için gömülü). `--denetle` bayrağıyla yazmadan karşılaştırır, fark varsa çıkış kodu 1 (testçi her sim değişikliğinden sonra koşar; §18 K8'den önce).

**Elle yazılan, yalnız B0'a ait JS** (sim'de karşılığı yok):

```js
const B0 = {
  tipler: ['balon', 'zeplin', 'marti', 'ucurtma'],     // ?tipler= ile değişir (eşlik testi: + 'parti')
  firsatlar: ['yakit'],
  kartlar: [['rampa'], ['bolge'], ['verim'], ['dalis'], ['kademe_itki'], ['yakit_ac', 'yakit_s']],
  sv_tavan: { rampa: 6 },                              // ısı B0'da yok: mükemmel kalkış ≤ 216 b/s
  gorunur_tur: 1,                                      // B0'da tüm kartlar tur 1'den
  kademe_n: 0,                                         // 1 son şans
  rakip: false, kalkis_primi: true,                    // §15 S1 (b)
  duvarlar: ['ses'],
  vurgu: null,                                         // §20 K-A: kullanıcı kararı bekliyor; ?vurgu=0|1
  toparlanma: true,                                    // KARARLAR 8. oturum; ?toparlanma=0 yalnız eşlik testi
  bos_dalis: { sure: 0.4, kayip: 0.10, aci: [-10, 45] },   // sim'de varsa sim'den; yoksa bu (~)
};

const B0_ARAYUZ = {
  rampa_T: 2.0,                         // ~ iğne tam tur (s), üçgen dalga
  rampa_kirmizi: 0.25, rampa_yesil_ust: 0.96,
  bitis_sure: 1.0, kara_kutu_max: 4.0, kara_kutu_sayac: 0.8,
  kara_kutu_kilit: 0.3,                 // ~ düğme kilidi (s)
  devam_sayim: [3, 0.5],                // 3-2-1, her biri 0,5 s
  ipucu_sure: 1.5,
  dokunma_min_dp: 48, duraklat_dp: 56, dalis_dugme_dp: 88,
  sayi_yuksel: [40, 0.6],               // ~ uçan sayı: 40 px, 0,6 s
  parcacik_max: 200,
  piksel_orani: { dusuk: 1.0, orta: 1.5, yuksek: 2.0, oto_bas: 2.0, oto_alt: 1.5, oto_fps: 55, oto_sure: 2.0 },
  yan_kayma: { sure: 0.3, hiz_kat: 0.6, donus: 0.5 },  // ~ §5 yandan çarpma görsel kayması
};

const YAKIT_HALKA = {                   // §7.4, tamamı öneri (~)
  tau_bas: 0.8,                         // halka bu kadar s önce başlar
  kat_bas: 3.0,                         // halka başta (r+4)'ün 3 katı
  pencere: [0.25, 0.05],                // başarı: temastan 0,25 s önce … 0,05 s sonra
  ipucu: 'Halka daralınca dokun: tam dolum!',
};

const HIS = {   // [duraksama ms, sarsıntı, ağır çekim çarpanı, ağır çekim s] — hepsi ~ (aralıklar §14)
  hafif: [40, 0.15, 1, 0], sekme: [60, 0.25, 1, 0], mukemmel: [90, 0.40, 1, 0],
  firsat: [90, 0.40, 0.4, 0.3], son_sans: [200, 0.50, 0.3, 0.5],
  ses_ilk: [300, 0.60, 0.2, 0.6], ses_sonra: [120, 0.30, 1, 0], bitis: [120, 0.80, 1, 0],
  sarsinti_genlik: 0.02, sarsinti_sure: 0.2,         // ~ ekran genişliği oranı, s
  titresim: { hafif: 10, mukemmel: 20, tam_dolum: 20, son_sans: 40, ses: [30, 40, 60] },   // ~ ms
};

const GUVENLIK = { flas_max_hz: 3, parlama_alan_max: 0.30, parlama_ms_max: 100 };   // ayar değil, sınır

// gösterge eşlemeleri (sim hiz_gosterge ile aynı; tek yönlü)
const HIZ_P = Math.log(7900 / 343) / Math.log(6);              // ≈ 1,751
function hizGosterge(v) {                                       // iç b/s → m/s
  return v <= 600 ? 343 * (Math.max(v, 0) / 100) ** HIZ_P : 7900 * v / 600;
}
const kmsa = (v) => hizGosterge(v) * 3.6;                       // km/sa
const mach = (v) => hizGosterge(v) / 343;                       // yalnız v ≥ 115 iken gösterilir
```

**Kara kutu kartı değer tablosu:** sim `deger()` aktarılır; B0'da yalnız kart satırları sorgulanır.

---

## 17. Test kancaları

### 17.1 Adres parametreleri

| Parametre | Etki |
|---|---|
| `?seed=N` | Tur tohumu (yoksa rastgele; duraklat menüsünde yazılır) |
| `?bot=hic\|kotu\|orta\|iyi\|usta` | Bot oynar (rampa + dalış + dron halkası; sim `rampa_karar`, `bot_karar`, `gorunur_hedef`, `firsat_tut`). Botun dokunuşları ekranda kısa halkayla görünür |
| `?t=S` | Tur başından (rampa dahil) S saniye görüntüsüz sabit adımla ilerlet, dondur (ekran görüntüsü için). Bot yoksa rampa 3 s'de otomatik "iyi", uçuşta dokunuş yok |
| `?tur=N` | Kampanya tur numarası (açılış koşulları) |
| `?sv=rampa:3,dalis:2` | Geliştirme seviyeleri (kayda yazılmaz) |
| `?tipler=balon,parti,zeplin,marti,ucurtma` | Etkin nesne türleri |
| `?hiz=K` | Fizik hızı çarpanı (yalnız botla; karede K kat adım) |
| `?toplu=N` | Görüntüsüz N tur (tohum seed…seed+N−1, aynı sv), sonuçlar konsola JSON ve `__oyun.sonuclar` |
| `?kampanya=N` | Botla N turluk kampanya; alıcı sim `alisveris` (yalnız B0 kartları); çıktı sim `kampanya().turlar` biçiminde |
| `?kayit=0` | localStorage'a dokunma |
| `?vurgu=0\|1` | Dalış hedef vurgusu (§20 K-A) |
| `?toparlanma=0` | Boş dalış toparlanmasını kapatır (yalnız sim eşliği testi) |
| `?debug=1` | Çarpışma daireleri, dalış konisi, pasif rota, oynanış ve gerçek görünür dikdörtgen, dron halkası penceresi, enerji denetimi uyarıları, fps sayacı |

### 17.2 `window.__oyun`

```js
window.__oyun = {
  AYAR, TIPLER, GELISTIRME, B0,              // salt okunur kopyalar
  durum(),                                   // { asama, t, x, y, vx, vy, gosterge, kademe, kazanc, nesne_n, halka }
  adim(n),                                   // n fizik adımı ilerlet (duraklatılmışken)
  dokun(),                                   // oyuncu dokunuşu (true: etkili; halka etkinse halkaya gider)
  tur(seed, sv, bot, tur),                   // görüntüsüz tek tur → sonuc
  kampanya(seed, bot, n),                    // görüntüsüz kampanya → { ilk, en_uzun_yok, turlar }
  olaylar,                                   // son turun olay günlüğü [[t, ad, ...], ...] (sim 'log' ile aynı)
  sonuclar,                                  // ?toplu çıktısı
  kayit: { oku(), yaz(o), sifirla() },
};
```

`sonuc` anahtarları sim `Ucus.sonuc()` ile aynı: `sekme, mukemmel, temas, son_sans, dalis, max_v, max_y, kazanc, kazanc_nesne, vay_t, mesafe, mesafe_g, sure_ucus, sure_tur, bitis, duvar, temas_s, kademe_kalan, ekran_ort, ekran_az_oran, firsat, firsat_tut, kalite`.

### 17.3 Rastgele sayı üreteci

- **Basit tohumlu üreteç yeter:** ör. `sfc32` ya da `mulberry32` (32 bit tohum; `seed` tam sayısından türetilir). Python MT19937 uyumu **gerekmez**.
- `random()` ∈ [0, 1); `uniform(a, b)` = a + (b − a)·random(); `gauss(μ, σ)` = Box–Muller (bir çift üret, ikincisini sakla, Python'daki gibi önbellekli); `randrange(n)` = ⌊random() × n⌋.
- **Çekim sırası sim'le aynı:** sim'de bir `rng` çağrısı olan her yerde JS de aynı üreteçten bir çekim yapar (aynı sayıda, aynı sırada; ör. dron temasındaki `firsat_tut` çekimi, §7.4). Bu, iki yolu sayı olarak eşitlemez ama dağılımları ve olay sıklıklarını eşit tutar.
- Dünya üreteci ve bot üreteci ayrı (sim'deki tohum formülleriyle: `tohum_bot`, `tohum_tur`, `tohum_alici`).
- **Eşlik istatistikseldir** (§18 K8), tek tek turların aynı çıkması beklenmez. Belirlenimlilik (aynı tohum → aynı sonuç) yalnız JS içinde şarttır (K9).

---

## 18. Kabul ölçütleri

Ölçüm: `oyun-testcisi`, Playwright + Chromium (`?toplu`, `?kampanya`, `?kayit=0`) ve S24 Ultra'da elle. Bot ölçümleri 20 tohum, medyan ve ortalama birlikte (K8 hariç).

**Geçme şartı:** K1–K3, K7–K16. **K4–K6 bilgi amaçlıdır** (raporlanır, geçme şartı değil; ekonomi ayarı B1'de sim'le yapılır).

| # | Ölçüt | Hedef | Nasıl |
|---|---|---|---|
| K1 | "Vay" anı | Tur 1'de `vay_t` ≤ 5 s, iyi ve hiç botlarında turların ≥ %90'ı | `?toplu=20&bot=iyi` ve `hic` |
| K2 | Tur 1 süresi | Ortalama 16–30 s (sim: ~17–18 s); hiçbir tur 65 s'ye çarpmaz | Aynı |
| K3 | Beceri farkı | İç x ile: Tur 1: iyi mesafe ≥ hiç × 1,30. Aynı geliştirmelerle (iyi kampanyasının tur 5 seviyeleri, `?sv=`): iyi ≥ hiç × 1,60 | `?toplu` |
| K4 | Satın alma ritmi (bilgi) | `?kampanya=15`, iyi / orta / hiç: art arda alışverişsiz tur ≤ 3; ilk 5 turda her tur ≥ 1 alım | `__oyun.kampanya` |
| K5 | Ses duvarı (bilgi) | İlk kırılış medyanı: iyi **tur 2–3** (KARARLAR 8. oturum), hiç ≤ tur 8 | Kampanya |
| K6 | Tur süresi, B0 kampanyası (bilgi) | Tur 5–15 medyanı 20–40 s~; tavana çarpan ≤ %5 | Kampanya |
| K7 | Yeniden başlatma | TEKRAR UÇ'tan iğnenin hareketine ≤ 0,5 s; bitişten yeni rampaya ≤ 3 s; kara kutu animasyonu sürerken TEKRAR UÇ hemen başlatır | Playwright zaman damgası |
| K8 | Sim eşliği | `?tipler=balon,parti,zeplin,marti,ucurtma`, tur 1, geliştirmesiz, hiç/orta/iyi, **≥ 200 tohum** (JS `?toplu=200`, sim aynı koşullarda 200 tohumla `tur_oyna`). Ölçüler: süre, iç x mesafe, en yüksek hız, sekme sayısı, kazanç. **Her ölçü için geçer:** ortalamalar arası fark ≤ %10 **ya da** iki tarafın ortalamaya ait %95 güven aralıkları örtüşüyor. Sim boş dalış toparlanmasını içermiyorsa JS `?toparlanma=0` ile koşulur. Önce §16 betiği `--denetle` geçmeli | Testçi iki tabloyu yan yana koyar |
| K9 | Belirlenimlilik | Aynı `?seed&bot&sv` iki kez → aynı `sonuc` JSON'u; `?hiz=1` ile `?hiz=8` aynı | Playwright |
| K10 | Mantık denetimi | `?debug=1` ile 20 tur: her trambolin sekmesinde |v'| ≤ |v|·k_etkin (+ek_vy), mükemmelde ≤ |v| + 12, yavaşlatıcıda < |v|; her hız artışı kayıtlı kaynağa bağlı (rampa, dalış, kademe, mükemmel, yerçekimi); dron yalnız göstergeyi değiştirir; 0 uyarı | Konsol |
| K11 | Kare hızı | S24 Ultra, Otomatik kalite: ortalama ≥ 58, en düşük ≥ 50; ilk açılış < 5 s | Kullanıcının telefonu + `?debug=1` fps sayacı |
| K12 | Kararlılık | Konsolda 0 hata; `?bot=iyi&kampanya=50` çökmesiz; bellek artışı < 20 MB | Playwright |
| K13 | Kayıt | Hangarda sekme kapatılıp açılınca jeton ve sv aynı; uçuşta sekme gizlenince `bekleyen` yazılır, görünür olunca `null` olur; gizliyken sayfa kapatılırsa açılışta bir kez eklenir; hiçbir senaryoda bir tur iki kez sayılmaz; elle bitirilen turda taban ve prim yok; bozuk JSON → varsayılan, çökme yok | Playwright |
| K14 | Duraklat | Gizlenince aynı karede durur; devamda 3-2-1; sayım sırasındaki dokunuş dalış yapmaz; duraklat düğmesi dalış yapmaz; `?toplu`'da blur duraklatmaz | Playwright |
| K15 | Erişilebilirlik | Hareket azaltmada sarsıntı 0 ve parlama yok; tam ekran flaş ≤ 3/s; mükemmel parlaması ≤ %30 alan, < 100 ms; üç yazı boyutunda arayüz taşmıyor; tüm düğmeler ≥ 48 dp | Ekran görüntüsü kontak sayfası `oyun/b0/test/` |
| K16 | Senin kararın | Telefonda **10 dakika** serbest oyun, sonra 3 sabit soru (Evet / Kısmen / Hayır): **(1) Kalkış heyecanlı mı? (2) Vuruşlar tok mu? (3) Bir tur daha oynamak ister misin?** Ayrıca 10 dakikada **kendiliğinden kaç tur** oynandığı otomatik sayılır (kayıttaki `tur` farkı). Testten önce kullanıcıya uyarı: **"Bu gri kutu yalnız his testidir: görsel, müzik ve içerik yok; yalnız kalkış, vuruş ve 'bir tur daha' hissini değerlendir."** | Kullanıcı + sayaç |

**K16 tutmazsa B1'e geçilmez** (PLAN_B §14). İlk düzeltilecek kaldıraçlar (B0'da veriyle): rampa iğnesi periyodu, gösterge dolumu (0,08 / 0,13), sekme açıları, ekran yoğunluğu (7), dalış konisi genişliği, `HIS` değerleri, dron halkası penceresi.

---

## 19. Uygulama notları

- **Dosyalar:** `oyun/b0/index.html` tek dosya (yayın için); üretilmiş yapılandırma (§16) en üstte gömülü JSON bloğu, ardından elle yazılan B0 sabitleri. **Three.js r170 yerel dosya:** `oyun/b0/lib/three.module.min.js` (importmap bu yola bakar; CDN yok, çevrimdışı ve testte ağ beklemesi olmasın). Testler `oyun/b0/test/`, betik `oyun/b0/araclar/`.
- **Piksel oranı:** `renderer.setPixelRatio(min(devicePixelRatio, kalite))`; varsayılan tavan **2,0** (S24 Ultra'nın 3,75'i değil). Otomatik kalitede §13.2 kuralı.
- **Sıra önerisi:** (1) §16 betiği + RNG + fizik çekirdeği + `__oyun.tur` (görüntüsüz) → K8 ve K9 önce geçsin; (2) botlar + `?toplu` / `?kampanya`; (3) görüntü, kamera, arayüz; (4) rampa, hangar, kara kutu, kayıt; (5) dron halkası, his, ses, ayarlar, duraklat, erişilebilirlik.
- **Havuz:** nesneler, parçacıklar, uçan sayılar havuzdan; uçuşta `new` yok. Sim'deki liste süzmeleri (nesne temizliği, aday listesi) JS'te **sırayı koruyan yerinde sıkıştırma** ve önceden ayrılmış dizilerle yapılır (§7.2); `filter`/`map` gibi yeni dizi döndüren çağrılar fizik döngüsünde kullanılmaz.
- **Görüntü–fizik ayrımı:** görüntü fizik durumunu yalnız okur (yandan çarpma kayması gibi görsel ofsetler ayrı tutulur, §5).

---

## 20. Kullanıcı kararları (verildi, 2026-10-08)

Uygulayıcı bu kararları varsayılan olarak kurar; yine de kolay değişsin diye metinler anahtardan, vurgu adres parametresinden okunur.

- **K-A. Dalış hedef vurgusu: VAR.** `B0.vurgu = 1` (`?vurgu=0` yalnız eşlik testi ve karşılaştırma için).
- **K-B. İlk açılış: HANGARSIZ İLK TUR.** İlk açılışta doğrudan RAMPA; hangar ilk kara kutudan sonra görünür.
- **K-C. Bitiş sahnesi: KARIŞIK (c).** `yer`'de abartılı (kapsül zıplayıp yuvarlanır, pilot sersem el sallar, paraşüt dolanır); `durma`/`sure`'de sakin (burun düşer, paraşüt açılır).
- **K-C. "Seni durduran" metinleri: ÖĞRETİCİ (a)** (§11 anahtarlarındaki mevcut metinler).
