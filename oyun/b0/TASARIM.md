# B0 · Gri kutu prototip şartnamesi

2026-10-08 · Dayanak: `PLAN_B.md` 6.2, `ICERIK.md` Taslak 2, `KARARLAR.md`, `oyun/sim/ucus_sim.py` · Uygulayan: `uygulayici` · Ölçen: `oyun-testcisi`

**Amaç tek bir soruyu cevaplamak:** "Burrito Bison gibi hissettiriyor ve eğlenceli mi?" Görsel yok, basit şekiller var. Fizik ve sayılar simülasyonla birebir; B0'da ayar değil, his test edilir.

`~` işaretli sayılar tahmin, oyun testinde ilk ayarlanacaklar onlar. İşaretsiz sayılar sim'den gelir, değiştirilmeden önce sim'de ölçülür.

---

## 0. Kapsam

| Dahil | Hariç (B1 ve sonrası) |
|---|---|
| Rampa göstergesi ve kalkış | Rakip zeplini (yerine kalkış primi, §15 S1) |
| Uçuş fiziği: g_etkin, sürükleme, ses duvarı Cd tepesi, üst sönüm, sekme | Isı duvarı, ısı fiziği, tropopoz/Kármán/yörünge ödülleri |
| Dalış (koni yardımı, mükemmel sekme) | Ölümcül nesne (kargo uçağı), zırh |
| 5 nesne: martı grubu, reklam balonu, reklam zeplini, uçurtma, yakıt dronu | Kalan 19 B1 nesnesi, nadir olaylar, kapsül |
| 1 kademe son şansı | Kademe sayısı geliştirmesi, son ateşleme |
| Ses duvarı (kırılış + sinematik + ödül) | Diğer eşikler |
| Kara kutu (döküm, "seni durduran", çözen kart) | Rekor balonu, hayalet, grafik |
| 6 kartlık hangar | Diğer geliştirmeler, fırsatlar F2–F10 |
| Kayıt (sürümlü, güvenli varsayılan) | Yedek kodu |
| Ayarlar, duraklat, erişilebilirlik, ışığa duyarlılık | Renk körlüğü modu, satın alma kilidi, istatistik ekranı |
| Basit sentez sesler (§15 S4) | Müzik |
| Test kancaları, botlar, toplu ölçüm | — |

**Deniz yok uyarlaması** (KARARLAR "her şey gökyüzünde"). Eski B0 listesindeki deniz nesnelerinin gökyüzü karşılıkları: **şamandıra → reklam zeplini** (iri, güvenilir trambolin; açılış "vay" sekmesini de o verir), **ağ → uçurtma ipi** (altından geçerken takılan fren, ağın yaptığı işi yapar).

### 0.1 Burrito Bison'dan ne alındı

| BB | B0'da | Karar | Neden |
|---|---|---|---|
| Fırlatma göstergesi, kritik bölge | Gidip gelen iğne, yeşil bölge (§3) | Al | İlk saniyede beceri ve heyecan |
| Normal jöleler: sekersin, yavaşlarsın | Balon, zeplin (trambolin), martı (fren) | Uyarla | Tema; sekme hızı artırmaz (mantık kuralı 1) |
| Polis jöleleri (yakalar, yavaşlatır) | Uçurtma ipi | Uyarla | Alçakta kalmanın bedeli |
| Rocket Slam | Dalış: 70° aşağı, koni yardımı, mükemmel sekme | Al | Tek dokunuşluk beceri. BB'de dalış dikine; bizde 70° çünkü roket ileri gidiyor, dikine dalış yatay hızı sıfırlar |
| Satın alınınca çıkan özel jöle | Yakıt dronu | Al | Harcamanın dünyada görünür sonucu |
| Pasta duvarı | Ses duvarı (Cd tepesi + kırılış) | Uyarla | Gerçek fiziksel eşik; hasar biriktirmez |
| Yere değince sekme, uzun kalırsan son | Zemin yok; kademe son şansı | At / değiştir | KARARLAR: deniz/zemin yok; ilerleme bir hatayla kaybolmasın |
| Ringdeki rakip | B0'da yok | Ertele | Kapsam; ekonomisi kalkış primiyle korunur |
| Piñata kartları | Yok | Ertele | B1 |
| Dükkân | 6 kartlık hangar | Al | "Bir tur daha" çekimi |

---

## 1. Ekran ve kontrol

- **Cihaz:** Samsung Galaxy S24 Ultra, dikey, tarayıcı (Chrome / Samsung Internet). CSS görünüm ~384 × 832, DPR ~3,75. Güvenli alanlar `env(safe-area-inset-*)`.
- **Dikey kilit:** `screen.orientation.lock('portrait')` denenir; yatayda "Telefonu dik tut" kaplaması.
- **Tek dokunuş:** `pointerdown` (gecikmesiz), ekranın her yeri (arayüz düğmeleri hariç). Basılı tutma, kaydırma, çoklu dokunuş yok; aynı anda ikinci parmak yok sayılır. Sayfa kaydırma ve yakınlaştırma kapalı (`touch-action: none`, `user-select: none`).
- **Dokunuş kuyruğu:** duraksama (hitstop) ya da ağır çekim sırasında gelen dokunuş bir sonraki fizik adımında uygulanır; kuyrukta en çok 1 dokunuş.
- **Arayüz yerleşimi** (onaylı konsept `oyun/konsept/oyun_ici_1.jpg` düzeni; B0'da gri):

| Yer | Öğe |
|---|---|
| Üst sol | Bu turun jetonu (jeton simgesi + sayı) |
| Üst orta | Mesafe (km, 1 ondalık) |
| Üst sağ | Duraklat düğmesi (56 × 56 dp) |
| Sağ kenar | Dikey irtifa çubuğu (km; B0'da 0–12 km ölçeği) |
| Alt sol | Hız göstergesi: yay + sayı (km/sa; ≥ Mach 1'de "Mach 1,2"); Mach 1 çentiği |
| Alt sağ | Dalış düğmesi (yuvarlak, 88 dp): dolum halkası + hak noktaları (kapasite 2). Görseldir, dokunuş ekranın her yerinde çalışır |
| Orta | İpucu yazıları, "MÜKEMMEL", "SON ŞANS", "SES DUVARI!" |

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
| ACILIS | ≤ 5 s ilk yükleme | Kayıt okunur → HANGAR (ilk açılışta doğrudan RAMPA: ilk tur hangarsız başlar) |
| RAMPA | 0,8–3,0 s | Dokunuş ya da 3,0 s → UCUS |
| UCUS | 15–65 s | Bitiş koşulu (§8) → BITIS |
| BITIS | 1,0 s komik son (dokunuşla atlanır) | → KARA_KUTU |
| KARA_KUTU | ≤ 4 s animasyon (dokunuşla atlanır) | TEKRAR UÇ → RAMPA (≤ 0,5 s) · HANGAR |

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
- Geri bildirim: mükemmel → beyaz halka, "MÜKEMMEL KALKIŞ!", 60 ms duraksama, titreşim 20 ms. İyi → "İYİ". Zayıf → "ZAYIF", iğne kırmızı titrer.
- İlk turda ipucu: "Yeşilde dokun".

---

## 4. Uçuş fiziği

**Birebir aktarım:** `ucus_sim.py` içindeki `Ucus` sınıfı (satır 201–824) JS'e aynı adlarla, aynı işlem sırasıyla aktarılır. Sayılar §13'teki yapılandırmadan okunur; kodda sayı yazılmaz.

- **Sabit adım** dt = 1/120 s, yarı örtük Euler (önce hız, sonra konum). Görüntü kare hızından bağımsız; görüntü iki fizik durumu arasında ara değerler (enterpolasyon).
- **Bir adımın sırası** (`Ucus.adim`, satır 649–807): kamera hızı → (10 Hz) yönetmen, fırsat ve garanti → kuvvetler (yerçekimi, sürükleme, sönümler) → tümleştirme → dalış süresi → çarpışmalar → uçurtma ipi → istatistik → eşikler → son şans, durma, yer, tavan.
- **Yerçekimi:** g_etkin = 30 × max(0, 1 − (|vx| / 600)²).
- **Sürükleme:** a = 0,00012 × e^(−y/400) × Cd × v², hız vektörüne ters. Cd = Cd_ses(v) × 0,85^(ayrılan kademe) (B0'da Aerodinamik yok).
- **Cd_ses(v):** v ≤ 85 → 1,0; 85–100 → 1,0 → 2,4; 100–115 → 2,4 → 1,1; v > 115 → 1,1 (doğrusal).
- **Üst sönüm:** v < 600 iken y > 300'de ek 7 × min(1, (y − 300) / 3.200) b/s² (hızın tersine). y > 2.900 ve vy > 0 → ek −6 b/s² dikey. (B0'da nadiren devreye girer; eşlik için var.)
- **Isı:** B0'da yok. Rampa tavanı sv 6 olduğundan hız 250'yi yalnız kısa dalış anlarında aşar; sim'de bu durumda ısı kilidine varılmaz.
- **Hız tavanı yok.** Hız yalnız kayıtlı kaynaklarla artar (§11 denetimi).
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
- **Yakıt dronu (fırsat):** temas → dalış göstergesi +1 (yakıt Güç geliştirmesi B0'da yok), göstergeye ayrıca +0,30; dron bidonu bırakır, sallanarak uzaklaşır.
- **Ödül:** her etkili temasta nesne ödülü (§9).
- **İki taraf kuralı (gri kutuda da görünür):** balon/zeplin temas noktasında %15 basılır ve 0,3 s yaylanır; martı grubu dağılır, 0,5 s sonra toparlanıp uçar; uçurtma takla atar; dron sallanır, bidon düşer.

---

## 6. Dalış

| Değer | Sayı | Kaynak |
|---|---|---|
| Hak | Gösterge ≥ 1,0 → 1 dalış; kapasite 2 | sim |
| Başlangıç | 1,0 (her tur 1 dalışla başlar) | sim `gosterge_bas` |
| Dolum | trambolin üstten 0,08 · mükemmel 0,10 · diğer temas 0,13 · fırsat 0,30 | sim |
| Hız | |v| + 14 + 4,0 × Dalış gücü sv (10 sv → +54) | sim |
| Yön | 70° aşağı; **koni yardımı:** 66–76° aşağı konide, menzil max(150, |v|) içinde, en yakın uygun trambolinin üst kenarına (y + 0,5r) nişan | sim `dalis_hedef` |
| Süre | 1,2 s (bu sürede üstten trambolin teması = mükemmel) | sim |
| Kural | Dalış sürerken ikinci dokunuş yok sayılır; hak yokken dokunuş "boş" titreşimi (düğme 80 ms sallanır, ses "tık"), etkisiz | sim + PLAN |

- **Görsel:** roket burnu hız yönüne döner; 0,2 s alev patlaması; dalış süresince arkada beyaz çizgi. Mükemmel → şok halkası, "MÜKEMMEL!", 60 ms duraksama.
- **Hedef vurgusu** (§15 S2, varsayılan açık, `?vurgu=0` kapatır): koni içinde geçerli hedef varken o trambolinin üstünde ince beyaz yay belirir. Oyuncu "şimdi dokunursam oraya dalarım"ı görür.
- **Boş dalış toparlanması** (PLAN_B §16 S3; varsayılan **kapalı**, `?toparlanma=1` açar): dokunuşta konide hedef yoksa dalış 0,4 s sürer, sonra yön dalış öncesine döner (−10°…+45° arası), |v| = 0,9 × dalış öncesi.
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
| Yakıt dronu | `yakit` (fırsat) | 9 | rota üstü, y ≥ 30 | — | +1 dalış | 20 | Sarı kutu + 4 küçük disk; çevresinde turkuaz halka (fırsat = daire + turkuaz) |

Trambolinlerin üstündeki beyaz yay şeridi "buraya düşülür" işaretidir (şekil kodu; renkten bağımsız).

### 7.2 Yerleşim (sim'le birebir)

- **Yoğunluk yönetmeni** (10 Hz, `yonet`): ekranda her an ~7 nesne. Üretim bölgesi: ekran + önündeki bir ekran, üstte/altta yükseklik × 0,3, y ≥ 25; yeni nesneler görünen alanın dışına konur (ilk doldurma hariç). Tür seçimi o yükseklikte açık türler arasında `w` ağırlığıyla. Arkada bir ekrandan fazla kalanlar havuza döner.
- **Açılış zeplini:** kalkıştan 1,8 s sonraki rota noktasına (x + 4, y = max(65, y_rota − 11)) bir zeplin. "Vay" anını garanti eder.
- **Sekme garantisi** (0,25 s'de bir, `garanti`): 6 s'lik pasif rotanın altında en az 15 b aşağıda bir trambolin yoksa, rotanın uzak yarısına (mümkünse ekran dışı) bir tane konur.
- **Yakıt dronu** (`firsat_yonet`): satın alındıysa ortalama 30 s / (1 + 0,25 × Sıklık sv) aralıkla (ilk: aralık × (0,3–1,0)), rotada 1,6–2,6 s ileriye, y sapması σ 12, y ≥ 30. Turda en çok 5.
- **Rastgele:** tüm üretim `?seed=` tohumlu tek kaynaktan (§14.3). Botun rastgelesi ayrı kaynak (sim'deki gibi).
- **Yoğunluk farkı notu:** B0'da `parti` (parti balonu) yok; aynı yoğunlukta pay balon ve zepline kayar. Sim eşliği testinde `?tipler=` ile eklenir (§14).

### 7.3 Arka plan

Gök y ile koyulaşır: y 0 açık mavi → y 1.000 lacivert (onaylı minyatür kararı: mavi → lacivert). Yer y = 0'da düz yeşil şerit (yeryüzü dekoru kararı PLAN_B §16 S6; B0'da yalnız şerit). 3 katman paralaks bulut (z −50, −150, −400), oynanışa girmez.

---

## 8. Son şans ve bitiş

- **Kademe:** B0'da 1 son şans. Tetik: y < 25 ve vy < 0, kademe > 0. Ayrıca hız 2 s boyunca < 25 ve y < 300.
- **Sonuç:** vx' = 0,9·vx + 15 + 6,5 × Kademe itkisi sv; vy' = 78 + 6,5 × sv; sürükleme × 0,85; dalış iptal.
- **His:** 200 ms duraksama, 0,5 s ×0,3 ağır çekim, "SON ŞANS" + kalan kademe simgesi; alt kademe (gri silindir) ayrılır, küçük paraşüt açılır, yere süzülür; roket kısalır.
- **Bitiş koşulları** (sim sırası):
  - `yer`: kademe yokken y ≤ 0.
  - `durma`: hız 2 s boyunca < 25 (kademe yok ya da y ≥ 300), ya da y > 1.000'de yatay hız 2 s boyunca < 110 (`vx_dur`; §15 S6).
  - `sure`: tur (rampa + uçuş) 65 s.
- **BITIS sahnesi (1,0 s):** `yer` → toz bulutu, kapsül paraşütle konar. `durma`/`sure` → roket burnu düşer, paraşüt açılır. Pilot kapsülde kalır.

---

## 9. Ekonomi (B0)

| Kalem | Formül | Kaynak |
|---|---|---|
| Nesne ödülü | ödül × kombo × (1 + 0,10 × İzlenme sv; B0'da 0) × 0,10 × 2,4 | sim `odul` |
| Kombo | 3 s içinde art arda vuruş: ×(1 + 0,05 × n), tavan ×2,0; tüm çarpanlar en çok ×4 | sim |
| Mesafe | iç x / 1.000 × 70 | sim `km_odul` |
| Sponsor tabanı | 25 (her tur) | sim |
| Kalkış primi | §3 | sim rakip vuruşu |
| Ses duvarı | İlk kırılış 300, sonrakiler 30 | sim `DUVARLAR` |

- **Uçan sayılar jeton** (§15 S5): temas noktasından yükselen "+4" (yuvarlanmış), kombo ≥ ×1,2 iken yanında "×1,3".
- **Jeton sayacı** üst solda bu turun toplamını gösterir; mesafe ve taban kara kutuda eklenir.
- Tur 1 beklenen kazanç: iyi oyuncu ~170, dokunmayan ~120 (sim).

---

## 10. Ses duvarı

- **Fizik:** Cd tepesi (§4) 85–115 arasında hızı yer. Kırılış: v ≥ 115 kesintisiz 0,3 s.
- **Gösterge:** hız yayında Mach 1 çentiği (iç hız 100); 85–115 arasında yay titrer, "SES DUVARI" etiketi belirir.
- **İlk kırılış sinematiği:** 300 ms duraksama → 0,6 s ×0,2 ağır çekim → roketin çevresinde beyaz şok konisi (gri kutuda yarı saydam koni) → tam ekran başlık "SES DUVARI!" + "+300". Işığa duyarlılık kurallarına uygun (§13.4): parlama yok, koni opak değil.
- **Sonraki kırılışlar:** 120 ms duraksama, küçük koni, "+30".
- **Kayıt:** ilk kırılış turu saklanır (`duvar.ses`).
- **Kara kutu:** kırılmadıysa "Ses duvarına X km/sa kaldı" (§11).

---

## 11. Kara kutu

Animasyon ≤ 4 s, dokunuş atlatır. Düzen yukarıdan aşağı:

1. Başlık: "UÇUŞ RAPORU" · tur no.
2. Toplam jeton (0,8 s sayarak artar).
3. Döküm satırları: Nesneler (n vuruş) · Mesafe (x,x km) · Kalkış primi · Sponsor tabanı · Ses duvarı (varsa).
4. Rekorlar: en yüksek hız, mesafe; yeni rekorsa "YENİ!".
5. **Seni durduran şey** (ilk uyan kural):

| Sıra | Koşul | Metin |
|---|---|---|
| 1 | Ses duvarı hiç kırılmadı ve en yüksek hız ≥ 85 | "Ses duvarına {Δ} km/sa kaldı" (Δ = gösterge(115) − gösterge(max_v), km/sa) |
| 2 | Bitişte gösterge ≥ 1,0 | "Dalış hakkın vardı: dokunup dal" |
| 3 | Bu tur ≥ 2 uçurtma ipi | "Uçurtma ipleri seni {n} kez frenledi" |
| 4 | `durma` ve y > 1.000 | "Çok yükseldin ama ileri hızın bitti" |
| 5 | `durma` | "Hızın tükendi" |
| 6 | `yer` | "Son kademen de bitti" |
| 7 | `sure` | "Uçuş süresi doldu" |

6. **Bunu çözen kart:** aday = B0 kartlarından maks olmayanlar; puan = değer / fiyat; değer sim'deki `deger()` tablosundan (bot = "iyi"; son 3 turda hiç dalış yoksa bot = "hic", bu durumda kart Rampa gücünü önerir). Kart: ad, fiyat, "Şimdi alınabilir" ya da "{eksik} jeton (≈ {n} tur)", n = ⌈eksik / son 3 tur ortalaması⌉. Karta dokunmak hangarı o kart vurgulu açar.
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
| 6 | Yakıt dronu | `yakit_ac` → `yakit_s` | 1 + 4 | 150 (aç) · 100 · 155 · 240 · 372 | Aç: "Yakıt dronları çıkar (+1 dalış)". Sıklık: ortalama aralık 30 → 15 s |

- Fiyat = round(taban × 1,55^sv); Yakıt dronu açma fiyatı sabit 150 (sim'deki gibi ayrı satırlar, kartta tek kart). Tablodaki fiyatlar elle hesaplandı; yarım değerlerde (ör. 109, 481) kayan nokta yuvarlaması belirleyici olduğundan birim testi listeyi sim'in `fiyat()` çıktısıyla karşılaştırır, fark varsa sim kazanır.
- Görünürlük: hepsi tur 1'den (B0 küçük olduğundan sim'deki tur 2 görünürlüğü kaldırıldı: `bolge`, `yakit_*`; ekonomi etkisi ölçülür).
- Kart durumu: alınabilir (canlı) · yetersiz (gri, eksik jeton yazılı) · MAKS. Seviye noktaları n / maks.
- Satın alma: tek dokunuş; jeton düşer, kart 120 ms ×1,15 zıplar, roketin üstünde ilgili parça bir ton açılır, kayıt yazılır. Geri alma yok (B0).
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
  "ayar": { "efekt": 80, "muzik": 60, "titresim": true, "hareket_azalt": null, "isik": false, "yazi": 1.0, "kalite": "oto" },
  "bekleyen": null }
```

- `son`: son 3 tur kazancı; `son_dalis`: son 3 turun dalış sayısı (kara kutu kartı için).
- Yazma: her tur sonu (KARA_KUTU açılmadan önce), her satın alma, her ayar değişikliği.
- **Yarım kalan tur:** sayfa gizlenince (`visibilitychange` → hidden, `pagehide`) o ana kadarki tur kazancı `bekleyen`e yazılır. Açılışta `bekleyen` varsa jetona eklenir, "Yarım kalan uçuş: +X jeton" bildirimi, `bekleyen` silinir. Kesinti hiçbir şey kaybettirmez.
- **Bozuk kayıt:** JSON hatası ya da şema dışı değer → bozuk metin `sdp_kayit_bozuk` anahtarına taşınır, varsayılan kayıtla devam, "Kayıt okunamadı, yeni başlangıç" bildirimi. Çökme yok.
- **Sürüm taşıma:** `tasi(kayit)` fonksiyonu `v`ye göre adım adım günceller (B0'da yalnız v1).
- `?kayit=0` → hiç okuma/yazma (testler).

### 13.2 Ayarlar

HANGAR'daki dişliden ve DURAKLAT menüsünden açılır.

| Ayar | Seçenekler | Varsayılan |
|---|---|---|
| Efekt sesi | 0–100 | 80 |
| Müzik | 0–100 (B0'da müzik yok; çubuk görünür, "yakında" notu) | 60 |
| Titreşim | Açık / kapalı | Açık |
| Hareket azaltma | Açık / kapalı | `prefers-reduced-motion` değeri |
| Işığa duyarlılık modu | Açık / kapalı | Kapalı |
| Yazı boyutu | Normal / Büyük / Çok büyük (×1,0 / ×1,2 / ×1,4) | Normal |
| Kalite | Otomatik / Düşük / Orta / Yüksek (çözünürlük çarpanı 1,0 / 1,5 / 2,0 / cihaz) | Otomatik |
| Kaydı sıfırla | İki adımlı: "Kaydı sıfırla" → "Emin misin? Tüm jeton ve geliştirmeler silinir" → "Sil" / "Vazgeç" | — |

### 13.3 Duraklat

- **Düğme:** üst sağ, 56 × 56 dp; dokunuşu dalış sayılmaz.
- **Otomatik:** `visibilitychange` (hidden), `pagehide`, `blur` → aynı karede duraklar (fizik adımı durur).
- **Menü:** DEVAM · YENİDEN BAŞLA · HANGAR · AYARLAR. YENİDEN BAŞLA ve HANGAR turu o ana kadarki kazançla bitirir (kazanç her zaman tam alınır; sömürü yok çünkü kazanç negatif olamaz).
- **Devam:** 3-2-1 sayımı (her biri 0,5 s); sayım sırasında dokunuşlar yok sayılır; RAMPA'da iğne de durur.

### 13.4 Erişilebilirlik ve ışığa duyarlılık

- Dokunma hedefleri ≥ 48 dp, aralarında ≥ 8 dp. Menüler HTML düğmeleri, `aria-label` Türkçe.
- **Şekil kodu (renkten bağımsız, her zaman açık):** trambolin = yuvarlak + üstte beyaz yay şeridi; fırsat = turkuaz daire halkası; yavaşlatıcı = köşeli biçim (üçgen martılar, baklava uçurtma).
- Yazılarda 2 px koyu kontur; kontrast ≥ 4,5 : 1. Yazı boyutu ayarı tüm arayüzü ölçekler, taşma olmaz.
- **Hareket azaltma:** sarsıntı 0; tam ekran parlama yok; hız çizgileri %30; kamera geçişleri yumuşak. Ağır çekim (oynanışın parçası) kalır.
- **Işığa duyarlılık modu ve her zaman geçerli kurallar:** tam ekran flaş saniyede en çok 3 (genel sınırlayıcı); mükemmel sekme parlaması ekranın en çok %30'u ve < 100 ms; kırmızı-beyaz titreşim yok; ağır çekim parlaklık oynatmaz. Mod açıkken parlamalar tamamen kapanır, yerine kontur halkası.
- **Sessiz oynanabilir:** her ses olayının görsel karşılığı var.
- **Titreşim** (`navigator.vibrate`): hafif temas 10 ms · mükemmel 20 · son şans 40 · ses duvarı [30, 40, 60]. Ayardan kapanır.

---

## 14. His ("juice") ve ses (gri kutu ölçeği)

| An | Duraksama | Sarsıntı | Diğer |
|---|---|---|---|
| Hafif çarpma (martı, balon yandan) | 40 ms | 0,15 | Nesne %15 basılır, 4–6 parçacık, "+N" |
| Trambolin sekmesi | 40 ms | 0,15 | Nesne basılıp yaylanır, ses perdesi kombo ile yükselir |
| Mükemmel sekme | 60 ms | 0,25 | Şok halkası, "MÜKEMMEL!" |
| Yakıt dronu | 90 ms | 0,4 | ×0,4 ağır çekim 0,3 s, bidon roketin üstüne uçar |
| Son şans | 200 ms | 0,5 | ×0,3 ağır çekim 0,5 s |
| Ses duvarı (ilk) | 300 ms | 0,6 | ×0,2 ağır çekim 0,6 s |
| Bitiş | 120 ms | 0,8 | Toz ya da paraşüt |

- **Sarsıntı:** genlik = değer × ekran genişliğinin %2'si, 200 ms üstel sönüm. Hareket azaltmada 0.
- **Duraksama ve ağır çekim** fizik adım sayısını azaltır (gerçek zaman ile fizik zamanı ayrışır); belirlenimlilik bozulmaz. Botlar fizik zamanında karar verir.
- **Kamera:** görünen dünya dikdörtgeni sim'deki `ekran()` ile aynı: genişlik W = min(500, 150 + 0,5 × v_kamera), yükseklik 2,1 × W, sol kenar x − W/3, dikey merkez max(y, H/2 − 10). v_kamera = hızın 0,8 s zaman sabitli yumuşatılmışı. Perspektif kamera, dikey görüş açısı 50°, uzaklık bu dikdörtgeni z = 0 düzleminde tam gösterecek şekilde hesaplanır. Ekran oranı 2,1'den uzunsa fazlalık üst/alt dekor, kısaysa yan dekor; oynanış dikdörtgeni değişmez (botların gördüğü alan = oyuncunun gördüğü alan).
- **Sesler** (Web Audio sentez, §15 S4): sekme "boing" (sinüs 300 → 600 Hz, 120 ms; kombo başına +1 yarım ton) · martı "pof" (gürültü 60 ms) · ip "tınn" (testere 180 Hz, 150 ms) · dalış "vuuş" (bant geçiren gürültü süpürmesi 250 ms) · mükemmel "ding" (880 + 1.320 Hz, 200 ms) · son şans "pat" + alçak gümbürtü · ses duvarı "BUM" (60 Hz sinüs + gürültü, 400 ms) · boş dokunuş "tık" · satın alma "çın". İlk dokunuşla `AudioContext` başlar.

---

## 15. Sorulacaklar

Varsayılanlar yalnız uygulamanın beklememesi için; kullanıcı cevabıyla değişir.

**S1. B0'da rakip zeplini.** (a) Gri kutu olarak dahil: rampanın yanında can çubuklu zeplin, mükemmel kalkış ona çarpar, hasar turlar arası birikir (R1: 700 can, nakavt 500). BB'nin ring rakibi hissi B0'da test edilir. (b) Hariç; ekonomi aynı formülle "kalkış primi" olarak korunur. **Varsayılan: (b)** (kapsam listesine sadık). Öneri: B0 sonrası ilk iş (a).

**S2. Dalış hedef vurgusu** (koni içindeki trambolinin üstünde beyaz yay). (a) Yok: oyuncu hedefi kendisi kestirir (sim botlarına en yakın). (b) Var: öğrenmeyi hızlandırır, zayıf oyuncuyu destekler. **Varsayılan: (b),** `?vurgu=0` ile A/B testi.

**S3. Boş dalış toparlanması** (PLAN_B §16 S3). **Varsayılan: kapalı** (sim eşliği), `?toparlanma=1` ile denenir. Kullanıcı (b) derse varsayılan açık olur.

**S4. B0'da ses.** (a) §14'teki basit sentez efektler. (b) Tamamen sessiz (ses B3'te). **Varsayılan: (a).** BB hissinin yarısı ses; gri kutuda bile vuruşun hissedilmesi için gerekli.

**S5. Uçan sayılar** (PLAN_B §16 S4). **Varsayılan: jeton.**

**S6. Yüksekte asılı kalınca kademe** (PLAN_B §16 S1). **Varsayılan:** onaylı kural (tur biter). `?kademe_ust=1` öneriyi açar: kademe varsa önce ileri doğru ateşlenir (vy' = 0,5 × (78 + 6,5·sv)). B0'da y > 1.000'e nadiren çıkıldığı için etkisi küçük.

---

## 16. Yapılandırma nesnesi (JS)

Sim'deki `AYAR`, `DUVARLAR`, `RAKIPLER`, `TIPLER`, `FIRSATLAR`, `KARGO`, `GELISTIRME`, `BOTLAR` birebir; anahtar sırası Python'daki gibi (tür seçimi sırası rastgele sayı eşliği için önemli). Python demetleri diziye çevrildi. `SABIT_EK`, sim kodunun içine gömülü sayıları tek yere toplar. `B0` ve `B0_ARAYUZ` yalnız bu faza ait. Sim değiştikçe bu blok sim'den yeniden üretilir; elle ayrışmaz.

```js
// ===== sim ile birebir (oyun/sim/ucus_sim.py, 2. ayar) =====
const SONUM_ALT = { y0: 300.0, y1: 3500.0, ek: 7.0 };

const AYAR = {
  dt: 1 / 120,
  g: 30.0,
  v_yorunge: 600.0,
  v_kacis: 600.0 * Math.SQRT2,
  g_yatay: true,
  rho_olcek: 400.0,
  c_suruk: 0.00012,
  cd_ses: [[85, 1.0], [100, 2.4], [115, 1.1]],
  ses_v: 115.0, ses_sure: 0.3, isi_duvar_v: 250.0, duvar_sure: 1.0, isi_sure: 2.0,
  uzay_kosul: true,
  isi_v: 250.0, isi_y: 1000.0,
  isi_hiz: 2.0,
  isi_sogu: 25.0,
  isi_cd: 2.5,
  y_karman: 3500.0, y_tropopoz: 1000.0,
  sonum: 22.0,
  sonum_yorunge: 22.0,
  sonum_alt: SONUM_ALT,
  ust_sonum: [2900.0, 6.0],
  v_dur: 25.0, dur_sure: 2.0,
  vx_dur: 110.0,
  tur_tavan: 65.0,
  r_roket: 4.0,
  rampa_y: 60.0, rampa_aci: 38.0, rampa_v: 70.0, rampa_v_sv: 16.0,
  rampa_oto: 3.0,
  kalite: { mukemmel: 1.30, iyi: 1.0, zayif: 0.80 },
  mukemmel_bolge: 0.12, mukemmel_bolge_sv: 0.024,
  mukemmel_bonus_sv: 0.05,
  acilis_sekme_dt: 1.8,
  k_tavan: 0.92, k_sv: 0.012,
  tekrar_sure: 2.0,
  dalis_aci: 70.0, dalis_koni: [66.0, 76.0], dalis_menzil: 150.0, dalis_menzil_k: 1.0,
  dalis_itki: 14.0, dalis_itki_sv: 4.0, dalis_sure: 1.2,
  dalis_kap: 2, gosterge_bas: 1.0,
  gosterge_tr: 0.08, gosterge_diger: 0.13, gosterge_m: 0.10,
  gosterge_firsat: 0.30, gosterge_sv: 0.10,
  mukemmel_sekme: 0.10, mukemmel_sekme_tavan: 12.0,
  kademe_y: 25.0, kademe_vy: 78.0, kademe_vy_sv: 6.5, kademe_vx: 15.0, kademe_vx_sv: 6.5, kademe_x_kayip: 0.9,
  kademe_cd: 0.85,
  son_ates: 19.5,
  ekran_w0: 150.0, ekran_wk: 0.5, ekran_wmax: 500.0, ekran_oran: 2.1,
  ekran_hedef: 7,
  romorkor_garanti: false,
  romorkor_y: 1500.0,
  garanti_pay: 25.0,
  firsat_ara: 30.0, firsat_ara_sv: 0.25, firsat_min: 6.0,
  firsat_tur_max: 5,
  firsat_tur_muaf: ['romorkor'],
  olumcul_ara: 22.0, olumcul_uyari: 1.5, olumcul_rota: true,
  kombo_sure: 3.0, kombo_sure_sv: 0.5, kombo_adim: 0.05, kombo_tavan: 2.0, kombo_tavan_sv: 0.33,
  carpan_tavan: 4.0,
  izlenme_sv: 0.10,
  odul_kat: 0.10,
  nesne_prim: 2.4,
  rakip_odul: 0.6,
  km_odul: 70.0,
  taban_odul: 25.0, sure_odul: 0.0,
  firsat_guc_kat: { fisek: 2.8, konfeti: 2.8, jet: 3.5, romorkor: 4.5 },
  fiyat_us: 1.55,
  ayar_tur: 25,
};

const DUVARLAR = { ses: 300, tropopoz: 600, isi: 1500, karman: 3000, yorunge: 6000, kacis: 15000 };   // ilk ödül; sonraki ×0,1
const RAKIPLER = [[700, 500], [1100, 1500], [1800, 4000], [3200, 8000], [5200, 15000]];          // [can, nakavt ödülü]

const _YK = AYAR.y_karman;
const TIPLER = {
  balon:   { sinif: 'tr', r: 12, ymin: 40,   ymax: 200,  w: 3.0, k: 0.80, aci: 50, yan: 0.06, odul: 15, omur: 3, acilis: 1 },
  parti:   { sinif: 'tr', r: 10, ymin: 30,   ymax: 150,  w: 2.0, k: 0.70, aci: 42, yan: 0.02, odul: 10, omur: 2, acilis: 1 },
  zeplin:  { sinif: 'tr', r: 22, ymin: 80,   ymax: 500,  w: 1.2, k: 0.85, aci: 45, yan: 0.10, odul: 40, omur: 3, acilis: 1 },
  dron:    { sinif: 'tr', r: 11, ymin: 60,   ymax: 450,  w: 0.6, k: 0.80, aci: 55, yan: 0.25, odul: 60, omur: 1, acilis: 2, ek_vy: 15 },
  sicak:   { sinif: 'tr', r: 20, ymin: 250,  ymax: 950,  w: 1.0, k: 0.85, aci: 40, yan: 0.08, odul: 30, omur: 3, acilis: 9 },
  bilim:   { sinif: 'tr', r: 26, ymin: 800,  ymax: _YK - 100, w: 1.2, k: 0.85, aci: 40, yan: 0.03, odul: 30, omur: 3, acilis: 'tropopoz' },
  habitat: { sinif: 'tr', kayma: true, r: 26, ymin: _YK, ymax: 9000, w: 0.8, k: 0.90, aci: 15, yan: 0.05, odul: 60, omur: 3, acilis: 'karman' },
  marti:   { sinif: 'yv', r: 13, ymin: 25,   ymax: 180,  w: 3.0, kayip: 0.06, odul: 20, acilis: 1 },
  ucurtma: { sinif: 'yv', r: 7,  ymin: 40,   ymax: 220,  w: 1.5, kayip: 0.02, ip: 0.15, odul: 6, acilis: 1 },
  afis:    { sinif: 'yv', r: 14, ymin: 60,   ymax: 200,  w: 0.4, kayip: 0.35, odul: 25, acilis: 4, ip_tip: true },
  sonde:   { sinif: 'yv', r: 6,  ymin: 50,   ymax: 700,  w: 1.0, kayip: 0.02, odul: 8, acilis: 5 },
  goktasi: { sinif: 'yv', r: 12, ymin: 1000, ymax: _YK - 100, w: 0.8, kayip: 0.05, odul: 20, acilis: 'tropopoz' },
  uydu:    { sinif: 'yv', r: 10, ymin: _YK + 100, ymax: 9000, w: 1.0, kayip: 0.12, odul: 50, acilis: 'karman' },
  cop:     { sinif: 'yv', r: 6,  ymin: _YK, ymax: 9000, w: 2.0, kayip: 0.08, odul: 15, acilis: 'karman' },
};

const FIRSATLAR = {
  yakit:    { r: 9,  odul: 20,  guc: 1,  guc_sv: 0.25, f: 'F1' },
  fisek:    { r: 10, odul: 40,  guc: 60, guc_sv: 10, aci: 35, sure: 1.2, f: 'F2' },
  konfeti:  { r: 10, odul: 35,  guc: 45, guc_sv: 10, f: 'F3' },
  termal:   { r: 60, odul: 3,   guc: 8,  guc_sv: 1.6, sure: 3.0, f: 'F4' },
  jet:      { r: 30, odul: 5,   guc: 12, guc_sv: 1.2, V: 180, V_sv: 24, uzun: 1500, f: 'F6' },
  romorkor: { r: 12, odul: 120, guc: 40, guc_sv: 8, f: 'F10' },
};
const KARGO = { r: 22, kanat: 40, odul: 200, kanat_kayip: 0.30, ymin: 300, ymax: 600, acilis: 6 };

// ad: [en çok sv, taban fiyat | sabit liste, görünür tur]
const GELISTIRME = {
  rampa: [10, 60, 1], bolge: [5, 80, 2], m_bonus: [5, 200, 14], zeplin_h: [8, 120, 7],
  verim: [8, 90, 1], aero: [8, 150, 4], burun: [6, 120, 5], ip: [4, 100, 4],
  kalkan: [6, 1500, 10], zirh: [3, 2500, 6],
  kademe_n: [2, [600, 6000], 12], kademe_itki: [8, 200, 1],
  dalis: [10, 70, 1], dolum: [8, 90, 2], kapasite: [2, [900, 7000], 23], son_ates: [4, 400, 24],
  izlenme: [10, 150, 1], kombo_s: [5, 120, 9], kombo_t: [3, 1000, 20],
  yakit_ac: [1, [150], 2], yakit_s: [4, 100, 2], yakit_g: [5, 120, 2],
  fisek_ac: [1, [300], 3], fisek_s: [4, 150, 3], fisek_g: [5, 160, 3],
  konfeti_ac: [1, [450], 6], konfeti_s: [4, 180, 6], konfeti_g: [5, 200, 6],
  termal_ac: [1, [400], 8], termal_s: [4, 150, 8], termal_g: [5, 170, 8],
  jet_ac: [1, [1200], 11], jet_s: [4, 300, 11], jet_g: [5, 350, 11],
  romorkor_ac: [1, [5000], 21], romorkor_s: [4, 800, 21], romorkor_g: [5, 900, 21],
};
function fiyat(ad, sv) {
  const [mx, taban] = GELISTIRME[ad];
  if (sv >= mx) return null;
  return Array.isArray(taban) ? taban[sv] : Math.round(taban * AYAR.fiyat_us ** sv);
  // Not: Python round() yarımlarda çifte yuvarlar; JS Math.round yukarı. Fiyatlar tam sayı .5'e
  // düşmediği sürece fark yok; birim testi B0 fiyat listesini (§12) karşılaştırır.
}

const BOTLAR = {
  hic:  { tut: 0.0 },
  kotu: { tepki: [0.40, 0.70], gurultu: 0.50, ongoru: 0.2, tut: 0.25, vazgec: 0.3, rampa_t: [0.4, 2.0], zayif: 0.25, rastgele_s: 0.15 },
  orta: { tepki: [0.25, 0.40], gurultu: 0.25, ongoru: 0.7, mukemmel: [0.50, 0.60], tut: 0.35, vazgec: 0.5, rampa_t: [0.6, 1.4] },
  iyi:  { tepki: [0.18, 0.30], gurultu: 0.10, ongoru: 0.8, mukemmel: [0.80, 0.95], tut: 0.50, vazgec: 0.8, rampa_t: [0.8, 1.1] },
  usta: { tepki: [0.00, 0.05], gurultu: 0.0,  ongoru: 1.0, mukemmel: [0.97, 0.97], tut: 1.00, vazgec: 1.0, rampa_t: [0.8, 1.1] },
};
const BOT_SIRA = ['hic', 'kotu', 'orta', 'iyi', 'usta'];
const HIC_SIFIR = ['dalis', 'dolum', 'kapasite', 'bolge', 'm_bonus', 'yakit_ac', 'yakit_s', 'yakit_g', 'son_ates'];

// gösterge eşlemeleri (tek yönlü)
const HIZ_P = Math.log(7900 / 343) / Math.log(6);              // ≈ 1,751
function hizGosterge(v) {                                       // iç b/s → m/s
  return v <= 600 ? 343 * (Math.max(v, 0) / 100) ** HIZ_P : 7900 * v / 600;
}
const IRTIFA_TABLO = [[0, 0], [25, 0.2], [300, 2], [1000, 12], [_YK, 100], [_YK + 3000, 400]];   // [b, km]; üstü 0,1 km/b

// sim kodunun içine gömülü sayılar (ucus_sim.py; JS'te tek yerde)
const SABIT_EK = {
  ust_vy_oran: 0.35,                 // carp(): üstten sayılma vy < 0,35·|v|
  marti_donus_derece: 2,
  burun_sv: 0.08, aero_sv: 0.05, kalkan_sv: 0.15, zeplin_h_sv: 0.15, ip_sv: 0.20,
  zirh: [0.60, 0.15],                // kayıp = 0,60 − 0,15·(sv − 1), turda 1
  rakip_kalite: { mukemmel: 1.0, iyi: 0.4, zayif: 0.0 },
  acilis_zeplin: { dx: 4, y_min: 65.0, r_kat: 0.5 },
  isi_kilit: 100, isi_coz: 70, isi_max: 120,
  cam_tau: 0.8,                      // cam_v += (v − cam_v)·min(1, dt/0,8)
  yonet_ara: 0.1,                    // 10 Hz yönetmen
  yonet: { on_ekran: 1, dikey_pay: 0.3, y_min: 25.0, deneme: 8 },
  temizlik: { arka_ekran: 1, dikey_ekran: 2.5, sonuk_sure: 0.5 },
  garanti_ara: 0.25, rota_sure: 6.0, rota_adim: 0.1, garanti_pay_kat: 0.6, garanti_y_min: 30, garanti_x0: 20,
  firsat: { ilk: [0.3, 0.7], sonra: [0.7, 0.6], tau: [1.6, 1.0], y_sapma: 12, y_min: 30.0,
            termal_y: 140, termal_roket_ymax: 300, jet_y: [400, 650], jet_roket_y: [250, 800] },
  olumcul: { ilk: [0.5, 1.0], sonra: [0.8, 0.4], roket_y: [200, 750], tau_ek: [0.5, 1.0], y_sapma: 25, kanat_dy: 4 },
  aday: [0.15, 80],                  // yarıçap = |v|·0,15 + 80
  son_ates_vx: 30, son_ates_vy: [0.5, 20],
  kademe_durma_ymax: 300,
  konfeti_aci: 30, konfeti_tut: [1.2, 0.7], fisek_tut: 1.19, romorkor_aci: [0, 10],
  yakit: { cift_sv: 4, ek_sv: 2, ek: 0.25, tut_ek: 0.25 },
  bot_karar_ara: 0.05,
  tohum_bot: [7919, 13],             // bot rastgelesi: Random(seed·7919 + 13)
  tohum_tur: 1000,                   // kampanya turu tohumu: seed·1000 + tur
  tohum_alici: [31, 7],              // alıcı: Random(seed·31 + 7)
};

// ===== yalnız B0 =====
const B0 = {
  tipler: ['balon', 'zeplin', 'marti', 'ucurtma'],     // ?tipler= ile değişir (eşlik testi: + 'parti')
  firsatlar: ['yakit'],
  kartlar: [['rampa'], ['bolge'], ['verim'], ['dalis'], ['kademe_itki'], ['yakit_ac', 'yakit_s']],
  sv_tavan: { rampa: 6 },                              // ısı B0'da yok: mükemmel kalkış ≤ 216 b/s
  gorunur_tur: 1,                                      // B0'da tüm kartlar tur 1'den
  kademe_n: 0,                                         // 1 son şans
  rakip: false, kalkis_primi: true,                    // §15 S1 (b)
  olumcul: false, isi: false,
  duvarlar: ['ses'],
  vurgu: true, toparlanma: false, kademe_ust: false,   // §15 S2, S3, S6
  bos_dalis: { sure: 0.4, kayip: 0.10, aci: [-10, 45] },   // toparlanma açıkken (~)
  kademe_ust_vy_kat: 0.5,                              // kademe_ust açıkken (~)
};

const B0_ARAYUZ = {
  rampa_T: 2.0,                         // ~ iğne tam tur (s), üçgen dalga
  rampa_kirmizi: 0.25, rampa_yesil_ust: 0.96,
  bitis_sure: 1.0, kara_kutu_max: 4.0, kara_kutu_sayac: 0.8,
  devam_sayim: [3, 0.5],                // 3-2-1, her biri 0,5 s
  ipucu_sure: 1.5,
  dokunma_min_dp: 48, duraklat_dp: 56, dalis_dugme_dp: 88,
  sayi_yuksel: [40, 0.6],               // ~ uçan sayı: 40 px, 0,6 s
  parcacik_max: 200,
};

const HIS = {   // [duraksama ms, sarsıntı, ağır çekim çarpanı, ağır çekim s]
  hafif: [40, 0.15, 1, 0], sekme: [40, 0.15, 1, 0], mukemmel: [60, 0.25, 1, 0],
  firsat: [90, 0.4, 0.4, 0.3], son_sans: [200, 0.5, 0.3, 0.5],
  ses_ilk: [300, 0.6, 0.2, 0.6], ses_sonra: [120, 0.3, 1, 0], bitis: [120, 0.8, 1, 0],
  sarsinti_genlik: 0.02, sarsinti_sure: 0.2,         // ekran genişliği oranı, s
  flas_max_hz: 3, parlama_alan_max: 0.30, parlama_ms_max: 100,
  titresim: { hafif: 10, mukemmel: 20, son_sans: 40, ses: [30, 40, 60] },
};
```

**Kara kutu kartı değer tablosu:** sim `deger()` (satır 940–970) aynen aktarılır; B0'da yalnız kart satırları sorgulanır.

---

## 17. Test kancaları

### 17.1 Adres parametreleri

| Parametre | Etki |
|---|---|
| `?seed=N` | Tur tohumu (yoksa rastgele; duraklat menüsünde yazılır) |
| `?bot=hic\|kotu\|orta\|iyi\|usta` | Bot oynar (rampa + dalış, sim `rampa_karar`, `bot_karar`, `gorunur_hedef` birebir). Botun dokunuşları ekranda kısa halkayla görünür |
| `?t=S` | Tur başından (rampa dahil) S saniye görüntüsüz sabit adımla ilerlet, dondur (ekran görüntüsü için). Bot yoksa rampa 3 s'de otomatik "iyi", uçuşta dokunuş yok |
| `?tur=N` | Kampanya tur numarası (açılış koşulları) |
| `?sv=rampa:3,dalis:2` | Geliştirme seviyeleri (kayda yazılmaz) |
| `?tipler=balon,parti,zeplin,marti,ucurtma` | Etkin nesne türleri |
| `?hiz=K` | Fizik hızı çarpanı (yalnız botla; karede K kat adım) |
| `?toplu=N` | Görüntüsüz N tur (tohum seed…seed+N−1, aynı sv), sonuçlar konsola JSON ve `__oyun.sonuclar` |
| `?kampanya=N` | Botla N turluk kampanya; alıcı sim `alisveris` (yalnız B0 kartları); çıktı sim `kampanya().turlar` biçiminde |
| `?kayit=0` | localStorage'a dokunma |
| `?vurgu=0\|1` · `?toparlanma=0\|1` · `?kademe_ust=0\|1` | §15 seçenekleri |
| `?debug=1` | Çarpışma daireleri, dalış konisi, pasif rota, ekran dikdörtgeni, enerji denetimi uyarıları |

### 17.2 `window.__oyun`

```js
window.__oyun = {
  AYAR, TIPLER, GELISTIRME, B0,              // salt okunur kopyalar
  durum(),                                   // { asama, t, x, y, vx, vy, gosterge, kademe, kazanc, nesne_n }
  adim(n),                                   // n fizik adımı ilerlet (duraklatılmışken)
  dokun(),                                   // oyuncu dokunuşu (true: etkili)
  tur(seed, sv, bot, tur),                   // görüntüsüz tek tur → sonuc
  kampanya(seed, bot, n),                    // görüntüsüz kampanya → { ilk, en_uzun_yok, turlar }
  olaylar,                                   // son turun olay günlüğü [[t, ad, ...], ...] (sim 'log' ile aynı)
  sonuclar,                                  // ?toplu çıktısı
  kayit: { oku(), yaz(o), sifirla() },
};
```

`sonuc` anahtarları sim `Ucus.sonuc()` ile aynı: `sekme, mukemmel, temas, son_sans, dalis, max_v, max_y, kazanc, kazanc_nesne, vay_t, mesafe, mesafe_g, sure_ucus, sure_tur, bitis, duvar, temas_s, kademe_kalan, ekran_ort, ekran_az_oran, firsat, firsat_tut, kalite`.

### 17.3 Rastgele sayı üreteci

Python `random.Random` ile uyumlu MT19937 önerilir: int tohum → `init_by_array` (|tohum|'un 32 bit parçaları); `random()` = (a >> 5, b >> 6) ile 53 bit; `uniform(a, b)` = a + (b − a)·random(); `gauss` = Python'un Box–Muller'ı (`gauss_next` önbelleğiyle); `randrange(n)` = `getrandbits(bit_uzunluğu(n))` reddetmeli. Böylece aynı tohumda ilk olaylar sim'le aynı çıkar. Kayan nokta farkları (exp, hypot) zamanla yolu ayırabilir; **eşlik istatistikseldir** (§18 K8), tam eşlik şart değil.

---

## 18. Kabul ölçütleri

Ölçüm: `oyun-testcisi`, Playwright + Chromium (`?toplu`, `?kampanya`, `?kayit=0`) ve S24 Ultra'da elle. Bot ölçümleri 20 tohum, medyan ve ortalama birlikte.

| # | Ölçüt | Hedef | Nasıl |
|---|---|---|---|
| K1 | "Vay" anı | Tur 1'de `vay_t` ≤ 5 s, iyi ve hiç botlarında turların ≥ %90'ı | `?toplu=20&bot=iyi` ve `hic` |
| K2 | Tur 1 süresi | Ortalama 16–30 s (sim: ~17–18 s); hiçbir tur 65 s'ye çarpmaz | Aynı |
| K3 | Beceri farkı | Tur 1: iyi mesafe ≥ hiç × 1,30. Aynı geliştirmelerle (iyi kampanyasının tur 5 seviyeleri, `?sv=`): iyi ≥ hiç × 1,60 | `?toplu` |
| K4 | Satın alma ritmi | `?kampanya=15`, iyi / orta / hiç: art arda alışverişsiz tur ≤ 3; ilk 5 turda her tur ≥ 1 alım | `__oyun.kampanya` |
| K5 | Ses duvarı | İlk kırılış medyanı: iyi tur 2–4, hiç ≤ tur 8 | Kampanya |
| K6 | Tur süresi (B0 kampanyası) | Tur 5–15 medyanı 20–40 s~; tavana çarpan ≤ %5 | Kampanya |
| K7 | Yeniden başlatma | TEKRAR UÇ'tan iğnenin hareketine ≤ 0,5 s; bitişten yeni rampaya ≤ 3 s | Playwright zaman damgası |
| K8 | Sim eşliği | `?tipler=balon,parti,zeplin,marti,ucurtma`, tur 1, geliştirmesiz, 20 tohum, hiç/orta/iyi: ortalama süre, mesafe, en yüksek hız, sekme sayısı ve kazanç `python ucus_sim.py` tam çıktısındaki "Tur 1, geliştirmesiz" tablosundan en çok ±%10 sapar | Testçi iki tabloyu yan yana koyar |
| K9 | Belirlenimlilik | Aynı `?seed&bot&sv` iki kez → aynı `sonuc` JSON'u; `?hiz=1` ile `?hiz=8` aynı | Playwright |
| K10 | Mantık denetimi | `?debug=1` ile 20 tur: her trambolin sekmesinde |v'| ≤ |v|·k_etkin (+ek_vy), mükemmelde ≤ |v| + 12, yavaşlatıcıda < |v|; her hız artışı kayıtlı kaynağa bağlı (rampa, dalış, kademe, mükemmel, fırsat, yerçekimi); 0 uyarı | Konsol |
| K11 | Kare hızı | S24 Ultra: ortalama ≥ 58, en düşük ≥ 50; ilk açılış < 5 s | Kullanıcının telefonu + `?debug=1` fps sayacı |
| K12 | Kararlılık | Konsolda 0 hata; `?bot=iyi&kampanya=200` (~30 dk) çökmesiz; bellek artışı < 20 MB | Playwright |
| K13 | Kayıt | Hangarda sekme kapatılıp açılınca jeton ve sv aynı; uçuşta sekme gizlenince `bekleyen` yazılır ve açılışta eklenir; bozuk JSON → varsayılan, çökme yok | Playwright |
| K14 | Duraklat | Gizlenince aynı karede durur; devamda 3-2-1; sayım sırasındaki dokunuş dalış yapmaz; duraklat düğmesi dalış yapmaz | Playwright |
| K15 | Erişilebilirlik | Hareket azaltmada sarsıntı 0 ve parlama yok; tam ekran flaş ≤ 3/s; mükemmel parlaması ≤ %30 alan, < 100 ms; üç yazı boyutunda arayüz taşmıyor; tüm düğmeler ≥ 48 dp | Ekran görüntüsü kontak sayfası `oyun/b0/test/` |
| K16 | Senin kararın | "Burrito Bison'a yakın ve eğlenceli" | Telefonda 10–15 dk oyun |

**K16 tutmazsa B1'e geçilmez** (PLAN_B §14). İlk düzeltilecek kaldıraçlar (B0'da veriyle): rampa iğnesi periyodu, gösterge dolumu (0,08 / 0,13), sekme açıları, ekran yoğunluğu (7), dalış konisi genişliği.

---

## 19. Uygulama notları

- **Dosyalar:** `oyun/b0/index.html` tek dosya (yayın için); yapılandırma (§16) ayrı bir `<script>` bloğunda en üstte. Three.js r170 A0'daki gibi importmap ile. Testler `oyun/b0/test/`.
- **Sıra önerisi:** (1) yapılandırma + RNG + fizik çekirdeği + `__oyun.tur` (görüntüsüz) → K8 ve K9 önce geçsin; (2) botlar + `?toplu` / `?kampanya`; (3) görüntü, kamera, arayüz; (4) rampa, hangar, kara kutu, kayıt; (5) his, ses, ayarlar, duraklat, erişilebilirlik.
- **Havuz:** nesneler, parçacıklar, uçan sayılar havuzdan; uçuşta `new` yok.
- **Görüntü–fizik ayrımı:** görüntü fizik durumunu yalnız okur.
