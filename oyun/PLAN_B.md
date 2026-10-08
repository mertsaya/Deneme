# Son Durak: Plüton — Plan B (Burrito Bison mantığı)

Taslak 6.2 · 2026-10-08 · Durum: kullanıcı onayı bekliyor (yalnız §5.3 önerileri ve §16 soruları; geri kalanı KARARLAR.md'ye dayanıyor)

**6.2'de değişenler**
- **Para birimi altın jeton** (₺ kaldırıldı, evrensel ton).
- **Simülasyon değerleri işlendi** (`oyun/sim/ucus_sim.py`, RAPOR §9.5): Kármán y 3.500 = 100 km, tropopoz y 1.000 = 12 km, bantlar yeniden; ısı duvarı 2 s; dalış konisi 66–76°; dalış gücü 14 → 54; fırsat güç çarpanları; bilim balonu 40° + üst atmosfer sönümü; habitat ayrı sınıf "kayma yüzeyi" (15°); `vx_dur` ve `firsat_tur_max` kuralları (kullanıcı onaylı).
- **Kalıntılar çıkarıldı:** kaya, rotor akımı, su sütunu, kıyı, kargo pilotu paraşütü (kargo uçağı insansız), uydu mini sapanı.
- **Ölümcül çarpışma** artık turu bitirmez, bir kademe kaybettirir (KARARLAR).
- **Kapsam:** B1 = ilk 25 tur. Bu plandaki 26+ tur bilgileri **taslak**.
- **Yeni §5.3:** simülasyonun tutmayan hedefleri için değerlendirme ve ayar listesi (onay bekliyor).
- **Evrensel ton:** yerel göndermeler kaldırıldı (ayrıntı ICERIK.md).

Bu plan, Taslak 5'teki fikri (Dünya'dan Plüton'a, her denemeden sonra geliştirme) korur, oynanışı Burrito Bison mantığına göre kurar. A0'daki gerçekçi uçuş simülasyonu bırakıldı.

---

## 0. Kuzey yıldızı ve kalite çıtası

**Tek cümle:** Rampadan fırlatılan çizgi film roketi, gökyüzündeki zeplinlerden ve balonlardan sekerek, çarptığı şeylerden hız kaparak ve doğru anda dokunarak momentumunu korur. Yere düşmek üzereyken boş kademesini atıp kaldığı yerden yeniden fırlar. Yeterince hızlanırsa yörüngeye, sonra Ay'a, en sonunda Plüton'a "düşer".

**4,5 yıldız ne demek?** Mağazada 4,5 ve üstü alan arcade fırlatma oyunlarının (Burrito Bison: Launcha Libre, Learn to Fly 3, Earn to Die 2) ortak özellikleri. Her biri ölçülebilir bir kabul ölçütüne dönüştü (§12):

1. İlk 5 saniyede "vay" anı, ilk 30 saniyede kural öğrenilmiş.
2. Bir tur 18–65 saniye, yeniden başlatma 3 saniyenin altında.
3. Her 1–3 turda bir satın alma, her 2–4 turda yeni bir şey (nesne, bölge, rakip).
4. Her vuruş hissedilir: duraksama, sarsıntı, ses, parçacık, sayı.
5. Haksız son yok: oyuncu her zaman neden durduğunu görür ve bir sonrakinde neyi değiştireceğini bilir.
6. Takılma yok: kare hızı 60, ilk açılış 5 saniyenin altında, kayıt kaybı yok.
7. Mantık hatası yok: her etkinin görünür bir sebebi var (§3).

---

## 1. Burrito Bison'un anatomisi ve bizim karşılığımız

"Al" birebir alınan mekaniği, "uyarla" temaya çevrilen mekaniği, "at" bilerek dışarıda bırakılanı gösteriyor.

| Burrito Bison | Ne işe yarıyor | Bizde | Karar |
|---|---|---|---|
| Ringden sapanla fırlatma, zamanlama göstergesi, kritik vuruş | İlk saniyede beceri ve heyecan | **Rampa fırlatması:** gösterge iğnesi yeşil bölgedeyken dokun → mükemmel kalkış (×1,30 hız ve rakip zeplinine vuruş) | Al |
| Ringdeki rakip: canı var, her fırlatmada hasar alır, nakavt olunca büyük ödül | Her turda küçük, uzun vadede büyük hedef | **Rakip ajansın zeplini:** rampanın yanında asılı durur, mükemmel kalkış gondoluna çarpar; hasar turlar arası taşınır, yamalarla görünür; nakavt olunca söner, sıradaki rakip gelir (5 rakip) | Uyarla |
| Normal jöle ayılar: üstlerine düşünce sekersin, yavaşlarsın, para verirler | Sürekli küçük karar ve ödül | **Martılar, uçurtmalar, şişme reklam balonları:** çarpınca küçük hız kaybı, jeton | Uyarla |
| Yere değmek seni yavaşlatır, uzun süre yerde kalırsan tur biter | Havada kalma baskısı | **Gökyüzü zemini:** zemin yok; havadaki esnek nesneler (zeplin, balon, yük dronu, bilim balonu) trambolin işi görür | Uyarla |
| — | İlerlemenin bir hatayla kaybolmaması | **Kademe son şansı:** yere düşmek üzereyken en alt kademe otomatik ayrılır, üstteki kademe olduğu yerden yukarı-ileri ateşlenir. Başta 1, geliştirmeyle 3. Atılan kademe paraşütle iner | Yeni |
| Roket dalışı (Rocket Slam): gösterge dolunca kullanım; aşağı dalıp ayıya çarpınca yüksek sekersin | Tek dokunuşluk beceri | **Dalış ateşlemesi:** dokun → roket 70° aşağı ateşler (koni yardımı 66–76°), bir trambolinin üstüne değerse mükemmel sekme | Al |
| Özel jöleler satın alınınca oyunda çıkmaya başlar | Para harcamanın görünür sonucu | **Fırsat nesneleri:** yakıt dronu, havai fişek, konfeti topu, termal sütun, jet akımı, uzay römorkörü; her birinin kendi mini zamanlama oyunu (KARARLAR) | Al |
| Polis jöleleri seni yakalayıp yavaşlatır | Alçakta kalmanın bedeli | **Afiş çeken uçaklar ve uçurtma ipleri:** alçak bantta, takılırsan ağır fren | Uyarla |
| Pasta duvarları: bölgeleri ayırır, kırmak için hız gerekir | Orta vadeli hedef | **Eşikler:** Ses duvarı, tropopoz, ısı duvarı, Kármán çizgisi, yörünge hızı, kaçış hızı. Hasar biriktirmez, gerçek fiziksel eşiktir | Uyarla |
| Piñata kartları | Sürpriz ödül | **Kargo kapsülü:** çarpınca 3 kart, üçü de kazanılır (KARARLAR) | Uyarla (reklamsız) |
| 3 karakter | Yeniden oynanabilirlik | 3 roket (B4) | Al (sonra) |
| Tur sonu para dökümü, dükkân | "Bir tur daha" | **Kara kutu + Hangar** | Al |
| Reklam, uygulama içi satın alma | Para kazanma | — | **At** |
| Sonu olmayan oyun | — | Plüton'a iniş = gerçek son | **Düzelt** |

---

## 2. Çekirdek fikir: Burrito Bison'un döngüsü = gerçek yörünge fiziği

Gerçekte roket uzaya **yukarı çıkarak değil, yatayda hızlanarak** gider. Etkin yerçekimi:

> **g_etkin = g × max(0, 1 − (vx / v_yörünge)²)** — vx: yatay hız

- Yavaşsan yerçekimi tam çeker → yere düşersin.
- Yatay hız arttıkça yerçekimi zayıflar → yaylar uzar.
- vx = v_yörünge olunca g_etkin = 0 → **yörüngedesin**.
- v = √2 × v_yörünge → **kaçış**, Ay bölümü.

Formülde yatay hız kullanılır: dikine fırlayarak yerçekimi "kapatılamaz" (fiziksel olarak doğru ve sömürüyü önler).

---

## 3. Mantık kuralları (değişmez)

1. **Enerji kaynaksız artmaz.** Hız ancak şunlardan gelir: rampa, dalış (yakıt), kademe ateşlemesi, son ateşleme, yük dronunun bataryası, fırsat nesneleri (fişek barutu, konfeti tüpü, römorkör yakıtı), termal sütun ve jet akımı (atmosfer), sonraki bölümlerde kütle çekimi sapanı. Sekme hızı **artırmaz** (|v| × k, k < 1); yalnız yön değiştirir. Kodda otomatik test (§12).
2. **Her çarpışmanın iki tarafı var.** Hafif nesne savrulur, roket biraz yavaşlar. Ağır nesne (kargo uçağı) parçalanır, roket bir kademesini kaybeder.
3. **Şiddet yok, kimse ölmez.** Kuşlar sersemler, toparlanıp uçar. Uçaklar ve dronlar insansız; kargo paletleri paraşütle iner. Rakip kaptan her nakavtta paraşütle iner ve yumruk sallar. Pilot maskot son şansta kapsülde kalır.
4. **Görünmeyen şey etkilemez.** Ekran dışından gelen her tehlike en az 1,2 s önce işaretlenir (sim: 1,5 s).
5. **Turlar arası kalıcılık bir sebebe dayanır.** Zeplin hasarı yamalarla, rekor bayrakla, satın alınanlar roketin üstünde görünür.
6. **Kaçınılmaz ceza yok.** Ölümcül nesne (kargo uçağı) seyrek, iri, önceden uyarılı; çarpmak turu bitirmez, kademe kaybettirir.
7. **Sayılar yalan söylemez.** Göstergedeki hız ve irtifa iç değerlerden tek yönlü eşlemeyle hesaplanır (§5).
8. **Sömürü döngüsü yok.** Aynı nesne 2 s içinde ikinci kez etki vermez; sekme her seferinde enerji kaybettirir; turda en çok 5 fırsat nesnesi (römorkör hariç); tropopoz üstünde yavaş asılı kalmak turu bitirir (`vx_dur`).

---

## 4. Tur akışı

```
HANGAR ──Kalk──► RAMPA (zamanlama) ──► UÇUŞ (sekme, çarpma, dalış) ──► DURUŞ ──► KARA KUTU ──► HANGAR
   ▲                                                                                          │
   └──────────────────────────── 3 saniyeden kısa ─────────────────────────────────────────┘
```

**Rampa (1–3 s).** Gösterge iğnesi gidip gelir. Dokunduğun an gücü belirler: yeşil = mükemmel (×1,30 hız, rakip zeplinine tam vuruş), sarı = iyi (×1,0), kırmızı = zayıf (×0,8). Dokunmazsan 3 s sonra otomatik "iyi".

**Uçuş.** Roket yay çizer, gökyüzündeki nesnelere çarpar, onlardan seker. Tek eylem **dalış**:
- Dalış göstergesi temaslarla dolar. Tur 1 dalış hakkıyla başlar, kapasite 2 (geliştirmeyle 4).
- Dokun → roket 70° aşağı yönelir, hızına 14 b/s eklenir (geliştirmeyle 54). 66–76° konide menzilde trambolin varsa ona nişan alınır.
- Dalış 1,2 s içinde bir trambolinin üstüne değerse **mükemmel sekme**: kayıp yok, üstüne +%10 (en çok +12 b/s).
- Hak yokken dokunmak bir şey yapmaz, gösterge kısa bir "boş" titreşimi verir.

**Son şans (kademe ayırma).** Roket y 25'in altına düşerken kademe varsa en alt kademe otomatik ayrılır; üstteki kademe ateşlenir (vx' = 0,9·vx + 15 + 6,5·sv, vy' = 78 + 6,5·sv). Roket her ayrılmada küçülür (sürükleme ×0,85). Boş kademe paraşütle iner. Aynı şey hız 2 s boyunca 25'in altında kalınca (y < 300 iken) ve ölümcül çarpışmada da olur.

**Duruş.** Tur şu durumlarda biter: kademesiz yere değmek; hız 2 s < 25 (kademe yok ya da y ≥ 300); **tropopoz üstünde yatay hız 2 s < 110** (`vx_dur`, kullanıcı onaylı; §5.3'te değişiklik önerisi var); son kademedeyken ölümcül çarpışma; 65 s emniyet tavanı. Komik son: pilot kapsülde paraşütle iner, ajansın kamyoneti toplar. Kazanç her durumda tam alınır.

**Kara kutu (en fazla 4 s).** Mesafe, en yüksek hız, irtifa, kırılan eşikler, jeton dökümü. "Seni durduran şey" ve bunu çözen geliştirme kartı (fiyatı, kaç tur kaldığı). "Tekrar uç" ve "Hangar".

**Hangar.** Sekmeler (§7). Satın alınca parça roketin üstüne oturur.

---

## 5. Uçuş fiziği (oyun birimleri; simülasyonla ayarlı)

Tüm sayılar tek yapılandırma nesnesinde (`AYAR`, `TIPLER`, `FIRSATLAR`, `GELISTIRME`; kaynak `oyun/sim/ucus_sim.py`). Denge veri değişikliğiyle yapılır. Birimler: b (≈ m), b/s, b/s²; sabit adım 1/120 s.

| Büyüklük | Değer |
|---|---|
| Dünya düzlemi | x ileri, y yükseklik (yer = 0) |
| Taban yerçekimi g | 30 b/s² |
| v_yörünge · v_kaçış | 600 · 849 b/s |
| Hava yoğunluğu ρ(y) | e^(−y / 400) |
| Sürükleme | a = 0,00012 × ρ × Cd × v². Cd = Cd_ses(v) × 0,85^(ayrılan kademe) × (1 − 0,05·Aerodinamik) × (ısı kilidinde 2,5) |
| Ses duvarı | Cd_ses: 1,0 → 2,4 → 1,1 (v 85 → 100 → 115, doğrusal). Kırılış: v ≥ 115, 0,3 s |
| Isı | ısı/s = max(0, v − 250) × 2 × ρ(y) × (1 − 0,15·Isı kalkanı) − 25; 0–120 arası. ≥ 100 → kilit (Cd × 2,5), < 70 → çözülür |
| Isı duvarı | v ≥ 250, y < 1.000, kilitsiz, kesintisiz 2 s |
| Üst atmosfer sönümü | v < 600 iken y 300 → 3.500 arasında ek sürükleme 0 → 7 b/s² (doğrusal); y ≥ 3.500 ve v < 849: +22 b/s²; y > 2.900 ve yükselirken ek −6 b/s² dikey |
| Sekme (trambolin, üstten) | Hız büyüklüğü × k_etkin (k + 0,012·Sekme verimi, tavan 0,92), yön nesnenin **sekme açısına** (40–55°; kayma yüzeyi 15°) döner; yük dronu +15 vy ekler. "Üstten" = roket nesne merkezinin üstünde ve vy < 0,35·|v| |
| Yandan temas | Hız × (1 − yan kaybı) |
| Mükemmel sekme | Dalış süresi içinde (1,2 s) üstten temas: |v| + min(%10, 12 b/s) |
| Kademe ayırma | §4. Başta 1 son şans, geliştirmeyle 3 |
| Son ateşleme | Kademe yokken y < 25'e düşerken ve |vx| < 30: vx += 19,5 × sv, vy = 0,5·|vy| + 20; turda 1 |
| Rampa | y 60, 38°; 70 + 16/sv b/s (10 sv → 230). Mükemmel ×1,30 (+0,05/sv Mükemmel bonusu), iyi ×1,0, zayıf ×0,8 |
| Dalış | §4; menzil max(150, v) b |
| Dalış göstergesi | Dolum: trambolin 0,08 · diğer temas 0,13 · mükemmel sekme 0,10 · fırsat 0,30 (+%10/sv Gösterge dolum); başlangıç 1,0; 1,0 = 1 dalış |
| Göstergede hız | m/s = 343 × (v/100)^1,751 (v ≤ 600; 100 → Mach 1, 250 → Mach 5,0, 600 → 7,9 km/s); v > 600: 7.900 × v/600 (849 → 11,2 km/s) |
| Göstergede irtifa | Parçalı doğrusal: 25 b → 0,2 km · 300 → 2 · 1.000 → 12 · 3.500 → **100 (Kármán)** · 6.500 → 400; üstü 0,1 km/b |
| Göstergede mesafe | Gösterge hızının yatay bileşeninin tümlevi (km) |
| Ekran (dikey) | Genişlik W = min(500, 150 + 0,5 × v_kamera) b, yükseklik 2,1 × W; roket sol üçte birde; ekranda her an ~7 nesne |

**Bantlar:** Alçak hava 25–250 · Bulutlar 250–1.000 · Üst atmosfer 1.000–3.500 · Uzay 3.500+ (Kármán). Uzay nesneleri Kármán'ın üstünde, atmosfer nesneleri altında (sim `kontrol` testi).

**Eşikler:** Ses (v 115) · Tropopoz (y 1.000 = 12 km) · Isı (v 250, 2 s) · Kármán (y 3.500 = 100 km) · Yörünge (v 600, y ≥ 3.500, 1 s) · Kaçış (v 849, y ≥ 3.500, 1 s; tur biter, Ay açılır — taslak).

**Kamera.** Roket sol üçte birde; hızla geri çekilir (yukarıdaki W formülü). Eşik geçişlerinde 0,6 s ağır çekim.

### 5.1 Hedef tur profilleri (iyi bot) ve simülasyon sonucu

| Tur | Ölçüt | Hedef (6.1) | Sim (iyi, 20 tohum) | Durum |
|---|---|---|---|---|
| 1 | süre · mesafe · kazanç | 18 s · 1,2 km · 120 | 18 s · 1,7 km · 171 | biraz yüksek |
| 3 | süre · mesafe · hız | 30 s · 4 km · Mach 1+ | 27 s · 3,8 km · Mach 1,9 | ✓ |
| 5 | kazanç | 400 | 701 | yüksek |
| 10 | süre · mesafe · hız · kazanç | 50 s · 25 km · 260 · 900 | 45 s · 22,5 km · 256 · 932 | ✓ |
| 15 | kazanç | 1.600 | 1.031 | düşük |
| 15–25 | tur süresi medyanı | 45–55 s (75 s'nin yerine) | 46 s | ✓ |
| 20 | kazanç | 2.600 | 2.283 | ✓ |
| 25 | mesafe · hız · kazanç | 150 km · 600 · 4.000 | 67 km · 426 · 1.815 | düşük |
| 40 | hız (taslak) | 849 (kaçış) | iyi 43, usta 32 | taslak |

Eşiklerin ilk kırıldığı tur (medyan; hedef → iyi / orta / usta): ses 3 → 2/3/2 · tropopoz 10 → 8/12/8 · ısı 12 → 9/12/8 · Kármán 18–19 → 17/23/13 · yörünge 25 → 31/37/25. Rakip nakavtı hedef 7 · 14 · 22 → iyi 6 · 12 · 19.

### 5.2 Zayıf oyuncu tabanı (KARARLAR 8. oturum)

Dokunmayan ya da kötü dokunan oyuncu geliştirmelerle yavaş ama ilerler: ısı duvarı ~tur 25, Kármán ~tur 45. Sim: hiç dokunmayan Kármán 47 ✓; kötü dokunan ısı 30 (19/20), Kármán yalnız 7/20 kampanyada ✗ (§5.3).

### 5.3 Simülasyon değerlendirmesi: hedef mi, sim mi düzeltilmeli? (öneri, onay bekliyor)

Ölçüt: hedef, oyuncunun yaşayacağı bir şeyi koruyorsa (yenilik ritmi, satın alma ritmi, kullanıcı kararı) **sim** düzeltilir; hedef, artık geçersiz bir varsayıma ya da türetilmiş bir sayıya dayanıyorsa **hedef** düzeltilir. Sim'e dokunulmadı; aşağıdaki liste uygulanacak ayar değişiklikleridir. Bütün etki tahminleri **tahmindir**, her adımdan sonra `python ucus_sim.py ozet 20` ile ölçülür.

**Kanıt (kampanya.json, iyi bot, tur 25, 20 tohum):** 20 turun 19'u "durma" ile bitiyor ve 19'unda son şans **hiç kullanılmamış**. 7 tur ≤ 27 s sürüyor, tepe irtifası 1.000–1.520 b (tropopozun hemen üstü), ortalama kazanç 770; kalan 13 turun ortalaması 2.377. Yani bu turlar `vx_dur` kuralıyla, roketin elinde kademe varken bitiyor. Tur 12'de alınan "Kademe sayısı" bu dönemde işe yaramıyor. Bu, "hiçbir geliştirme işe yaramaz kalmaz" ilkesine ve KARARLAR'daki son şans kuralının amacına ("ilerleme bir hatayla kaybolmasın") ters.

| # | Sorun | Karar | Gerekçe |
|---|---|---|---|
| D1 | Tur 25 mesafesi 67 km, hedef 150 | **Hedef düzelir:** mesafe ayar hedefi olmaktan çıkar, bilgi satırı olur (tur 25 ≈ 90–130 km) | 150 km, 75 s'lik tur varsayımıyla yazılmıştı; süre 45–55 s'ye indi. Mesafe gösterge hızının tümlevi, yani hızdan türer; hız tutarsa mesafe kendiliğinden gelir |
| D2 | Tur 25 hızı 426, yörünge iyi 31 (hedef 25) | **Hedef korunur, ölçüt düzelir, sim düzelir.** Ölçüt "tur 25 ortalama en yüksek hız 600" yerine "yörünge ilk kırılışı medyanı: usta ≤ 24, iyi 24–27, orta ≤ 34". Sim: S1, S3 | Yörünge, B1 kapsamının (ilk 25 tur) finali; tur 25'ten sonra yeni içerik yok, oyuncu yörüngeyi B1 içinde görmeli. Ortalama tepe hızı uç değerlere duyarlı; eşik turu oyuncunun yaşadığı şey |
| D3 | Kazanç eğrisi düz (tur 5: 701/400, tur 25: 1.815/4.000) | **Hedefin şekli doğru, sim düzelir; ölçüm düzelir.** Tur 5 hedefi 400 → 500 | Fiyatlar seviye başına ×1,55 büyüyor; gelir de geometrik büyümezse tur başına alım sayısı düşer, son turlar öğütmeye döner. Hedef eğri tur başına ≈ ×1,15, doğru şekil. Ölçüm: sim kazancı ilk duvar ve nakavt ödüllerini (300–6.000) içeriyor, tur bazında gürültülü; hedef "uçuş kazancı" (`kazanc_ucus`) ile 3 tur kayan medyan üzerinden ölçülmeli. Tur 5'te biraz cömertlik BB'nin ilk saatine uygun (ilk turlarda turda 2–4 alım) |
| D4 | Kötü dokunan oyuncu Kármán'a ulaşamıyor (7/20) | **Hedef korunur** (kullanıcı kararı), **sim düzelir** (S1, S6) | Asıl bulgu: kötü dokunan, **hiç dokunmayandan kötü** (hiç: Kármán 47; kötü: 7/20). Boş bir dalış (konide hedef yokken) roketi 70° aşağı çevirir; yatay hızın ~%66'sı gider (cos 70° = 0,34). Oyun yanlış dokunuşu dokunmamaktan ağır cezalandırıyor. BB'de boş bir dalış yere çarpıp seker, küçük bir kayıptır. Gerçek zayıf oyuncu boşa dokunur; tasarım bunu affetmeli, ödüllendirmemeli |
| D5 | Erken eşikler 1–3 tur erken (ses 2, tropopoz 8, ısı 9) | **Ses: hedef düzelir (2–3). Tropopoz ve ısı: sim düzelir** (S4, S5) | Ses duvarının tur 2'de gelmesi iyi bir "vay" (BB'de ilk duvar ilk birkaç turda). Ama ısı duvarı tropopozla aynı turda kırılıyor: duvar değil, hız kontrolü. Isı kalkanı tur 10'da görünür olduğundan duvar kalkan gerekmeden kırılıyor, kalkan işe yaramaz kalıyor. Duvar 2–3 tur durdurmalı ve "çözen geliştirme" kartı o anda var olmalı |
| D6 | Beceri farkı tur 1: +%44 (hedef ≥ %60) | **Hedef düzelir:** tur 1 ≥ +%30; aynı geliştirmelerle tur 5 ve 10 ≥ +%60 (sim: +%150 / +%232 ✓) | Tur 1'de 1 dalış hakkı var ve gösterge yavaş doluyor; ilk tur doğal olarak fırlatma ağırlıklı (BB'de de öyle). Botlar artık gerçekçi tepki süresiyle oynuyor |
| D7 | Tavana (65 s) çarpan tur: orta %17, iyi %13 | **Sim ölçülür, gerekirse düzelir** (S8) | S1 turları uzatacağı için önce S1'in etkisi ölçülmeli |

**Ayar değişiklikleri listesi (sim'e bu sırayla uygulanır; her adımdan sonra 20 tohum ölçümü):**

| # | Değişiklik | Yeni değer | Beklenen etki (tahmin) | Onay |
|---|---|---|---|---|
| S1 | `vx_dur` ya da yüksekte durma koşulu sağlanınca, kademe varsa **her irtifada** kademe ateşlenir (şu an yalnız y < 300). Tropopoz üstünde ateşleme yönü ileri ağırlıklı: vx' = 0,9·vx + 15 + 6,5·sv, vy' = 0,5 × (78 + 6,5·sv). Yeni düğme `kademe_ust_vy_kat = 0,5` | Kademe yoksa tur yine biter | İyi bot tur 25 kazancı +%25–30 (7 kısa tur toparlanır), tur 15–25 medyan süresi +3–6 s, son şans geç dönemde kullanılır | **Gerekli** (onaylı kuralı değiştirir, §16 S1) |
| S2 | Ölçüm: `HEDEF['kazanc']` uçuş kazancına (`kazanc_ucus`) ve 3 tur kayan medyana bağlanır; tek seferlikler (duvar + nakavt) ayrı satır | Uçuş kazancı hedefi: 1: 120 · 5: 500 · 10: 900 · 15: 1.600 · 20: 2.600 · 25: 4.000 (±%15) | Ölçüm gürültüsü azalır | Hayır (ölçüm) |
| S3 | Geç dönem gelir kaldıracı: irtifa bandı çarpanı nesne ve km ödülüne; `carpan_tavan` (×4) dışında uygulanır | `bant_carpan`: y < 1.000 → ×1,0 · 1.000–3.500 → ×1,8 · ≥ 3.500 → ×3,0 | Tur 15 ≈ +%30, tur 25 ≈ +%50–60 | **Gerekli** (§16 S2, seçenekli) |
| S4 | Erken gelir kesintisi | `km_odul` 70 → 55 · `nesne_prim` 2,4 → 2,0 · `rakip_odul` 0,6 → 0,45 | Tur 1–10 kazancı −%20 (tur 1 ≈ 135, tur 5 ≈ 560); S3 ile birlikte tur 25 ≈ 3.400–4.000; tropopoz +1 tur | Hayır (ayar) |
| S5 | Isı duvarı gerçek duvar olsun | `isi_sure` 2 → 3 s · `isi_hiz` 2,0 → 3,0 · Isı kalkanı görünür tur 10 → 8 | Isı iyi 9 → 11–12; kalkan "çözen geliştirme" olur | Hayır (ayar) |
| S6 | Boş dalış toparlanması: dokunuş anında konide hedef yoksa dalış 0,4 s sürer, sonra burun dalış öncesi yöne döner (−10° ile +45° arası sınırlı), hız büyüklüğü = 0,9 × dalış öncesi. Yeni düğmeler `bos_dalis_sure = 0,4`, `bos_dalis_kayip = 0,10` | Hedefli dalış değişmez | Kötü bot ≥ hiç; kötü Kármán ~45–50 (≥ 15/20 kampanya); iyi/usta farkı az değişir (onlar hedefli dalıyor) | **Gerekli** (his değişir, §16 S3) |
| S7 | Yörünge ince ayarı (S1–S5'ten sonra) | İyi yörünge medyanı > 27 ise `firsat_guc_kat.romorkor` 4,5 → 5,5; < 23 ise uzay bant çarpanı 3,0 → 2,5 | Yörünge iyi 24–27 | Hayır |
| S8 | Tavan oranı S1'den sonra > %10 ise: y < 300 bandında trambolin ağırlığı uçuşun 30. saniyesinden sonra her 10 s'de ×0,9 (en az ×0,5) | — | Tavana çarpan ≤ %10 | Hayır |
| S9 | `HEDEF` güncellemesi | esik: ses 2–3, tropopoz 9–10, ısı 11–12, Kármán 17–19, yörünge 24–27 · mesafe tur 25 kaldırılır · hız tur 25 kaldırılır (D2 ölçütü) · kazanç S2 · beceri: tur 1 ≥ +%30, tur 5/10 ≥ +%60 · zayıf: kötü ısı ≤ 28, Kármán ≤ 50 (≥ 15/20) · orta (tipik oyuncu): yörünge ≤ 34 | — | D1–D6 onayıyla |

Ölçüm notu: tek tohumda kampanyalar ±5 tur oynuyor; karar için en az 20 tohum ve medyan, son kabul için 40 tohum.

---

## 6. Dünya bölümü: B1 nesneleri (ilk 25 tur)

Ayrıntı, sayılar ve görünüş: `ICERIK.md` §1. Sim değerleri (`TIPLER`) esastır.

| Sınıf | Nesneler | Not |
|---|---|---|
| Trambolin | Reklam balonu, parti balonu, reklam zeplini, yük dronu, sıcak hava balonu, kargo paraşütü, bilim balonu (40°), rakip zeplini | Sekme açısı 40–55° |
| Kayma yüzeyi | Şişme habitat modülü (15°) | Ayrı sınıf: fizik trambolinle aynı, sığ açı; görsel tasarım kullanıcı onayına |
| Yavaşlatıcı | Martı, uçurtma (ip), afiş çeken uçak, radyosonde, göktaşı tozu izi, uydu, uzay çöpü | Uydu hız vermez (mini sapan kaldırıldı) |
| Fırsat | Yakıt dronu, havai fişek, konfeti topu dronu, termal sütun, jet akımı, uzay römorkörü | Satın alınınca çıkar; turda en çok 5 (römorkör hariç) |
| Toplanabilir | Kargo kapsülü | Tur 3'ten, 3 kart |
| Tehlike | Kargo uçağı (insansız) | Tur 6'dan; gövde = kademe kaybı, kanat ucu −%30 |
| Nadir olay (5) | Dev şişme kedi, uçan daire şakası (rakip dublörü), leylek termalleri, meteor şok dalgası, kayıp balina zeplini | Turda en çok 1 |

**Yerleşim.** Nesneler ekran başına yoğunlukla (her an ~7) ve bant ağırlıklarıyla tohumlu üretilir. Dalış menzilinde (pasif rotanın en az 15 b altında) her an en az bir trambolin bulunur (0,25 s'de bir denetlenir, eksikse ekran dışına konur). Fırsatlar zamana bağlı (ortalama aralık 30 s / (1 + 0,25·sıklık sv), türler arası ≥ 6 s). Kargo uçağı ~22 s'de bir, yalnız y 200–750 arasındayken, rotaya, 1,5 s uyarıyla.

---

## 7. Ekonomi ve hangar

**Tek para birimi: altın jeton.** Uçuşu izleyenler arttıkça sponsorlar jeton öder. Ekranda uçan sayılar jeton (§16 S4).

Tur kazancı = Σ(nesne ödülü × kombo × izlenme çarpanı) × 0,10 × 2,4 + iç km × 70 + 25 (sponsor tabanı) + rakip hasarı × 0,6 + eşik ödülleri (ilk kez tam, sonra %10) + rakip nakavt ödülü.
- Kombo: 3 s içinde art arda vuruş, her vuruş +0,05, tavan ×2,0 (Kombo tavanı ile ×3,0). Tüm çarpanların çarpımı en çok ×4.
- Eşik ödülleri: ses 300 · tropopoz 600 · ısı 1.500 · Kármán 3.000 · yörünge 6.000 · kaçış 15.000.
- Rakipler (can / nakavt): 700/500 · 1.100/1.500 · 1.800/4.000 · 3.200/8.000 (taslak) · 5.200/15.000 (taslak).
- Fiyat = taban × 1,55^seviye.

**Hangar sekmeleri (B1, sim'deki satırlar):**

| Sekme | Geliştirmeler |
|---|---|
| Rampa | Rampa gücü · Mükemmel bölge · Mükemmel bonusu · Zeplin hasarı |
| Gövde | Sekme verimi · Aerodinamik · Burun konisi · İp kesici · Isı kalkanı · Zırh |
| Kademeler | Kademe sayısı (1 → 3 son şans) · Kademe itkisi |
| Motor | Dalış gücü · Gösterge dolum · Dalış kapasitesi (2 → 4) · Son ateşleme |
| Fırsatlar | Yakıt dronu · Havai fişek · Konfeti topu · Termal sütun · Jet akımı · Uzay römorkörü (her biri aç + sıklık + güç) |
| Yayın | İzlenme çarpanı · Kombo süresi · Kombo tavanı |

İlk tur ≈ 120–170 jeton; ilk geliştirmeler 60–200 jeton. Simülasyon: `oyun/sim/ucus_sim.py` (5 bot, 20 tohum). Kabul: art arda en çok 3 tur alışverişsiz (sim: iyi 1, hiç 2 ✓), ilk 25 turda çıkmaz yok (✓).

---

## 8. Bölümler (Taslak 5'in rotası; 2–8 taslak)

| # | Bölüm | Sekme nesneleri | Özel kural | Eşikler |
|---|---|---|---|---|
| 1 | Dünya | Zeplin, balon, yük dronu, bilim balonu, habitat | Hava yoğun, ses ve ısı duvarı | Ses · Tropopoz · Isı · Kármán · Yörünge · Kaçış |
| 2 | Ay | Hava yastığı topları, yörünge hurdaları | Zayıf yerçekimi, hava yok | Krater sırtları · Kaçış |
| 3 | Mars | Toz hortumları, kum bulutları | Toz fırtınası, Phobos sapanı | Olympus Mons · Kaçış |
| 4 | Asteroit Kuşağı | Moloz yığını asteroitler | Asteroitten asteroide sekme | Kirkwood boşlukları |
| 5 | Jüpiter | Bulut tepeleri | Dev yerçekimi, en büyük sapan | Radyasyon kuşağı |
| 6 | Satürn | Halka buzları | Halka boşlukları | Halka geçişi |
| 7 | Uranüs–Neptün | Buz bulutları | Karanlık, görüş kısa | Rüzgârlar |
| 8 | Plüton | Azot buzu ovası | Final iniş mini oyunu | Zafer |

Bölümlerin ayrıntılı tasarımı, Dünya bölümü eğlenceli bulunduktan sonra.

---

## 9. His ("juice") listesi

| An | Duraksama | Sarsıntı | Diğer |
|---|---|---|---|
| Hafif çarpma (martı, balon) | 40 ms | 0,15 | Squash %15, tüy ya da konfeti, "pof", +jeton sayısı uçar |
| Mükemmel sekme | 60 ms | 0,25 | Şok halkası, parlama (ekranın en çok %30'u, < 100 ms), "MÜKEMMEL", ses perdesi yükselir |
| Fırsat nesnesi | 90 ms | 0,4 | Özel efekt, kısa ağır çekim (×0,4, 0,3 s) |
| Kademe ayırma (son şans) | 200 ms | 0,5 | Ağır çekim ×0,3, 0,5 s; boş kademe paraşütle düşer; "SON ŞANS" |
| Eşik kırılışı | 300 ms | 0,6 | Ağır çekim ×0,2, 0,6 s; şok konisi; tam ekran başlık; müzik katmanı açılır |
| Ölümcül çarpışma / yere iniş | 120 ms | 0,8 | Ateş topu ya da toz bulutu, parçalar; pilot kapsülde paraşütle iner |

**Işığa duyarlılık:** tam ekran flaş saniyede 3'ten sık olmaz; kırmızı-beyaz titreşim yok; ağır çekim parlaklık oynatmaz; `prefers-reduced-motion` okunur; uyarılar renkten ayrı şekille de ayırt edilir. Hareket azaltma ayarı sarsıntıyı ve flaşı kapatır.

---

## 10. Teknik mimari

- **Platform:** Tarayıcı, Three.js r170, tek sayfa; telefondan artifact bağlantısı. A0 altyapısı (yayın kısıtları, base64 GLB, uyarlanabilir çözünürlük, test kancaları) yeniden kullanılır.
- **Katmanlar:** `ayar` · `dunya` (tohumlu üretim, yoğunluk yönetmeni) · `fizik` (sabit 120 Hz, 2B daire çarpışma) · `durum` (rampa → uçuş → duruş → kara kutu → hangar) · `goruntu` · `ses` · `arayuz` · `kayit`.
- **Fizik 2B, görüntü 3B.** Oynanış düzlemde (x, y).
- **Sim eşliği:** JS fizik çekirdeği `ucus_sim.py`'nin `Ucus` sınıfının birebir aktarımı; botlar (`BOTLAR`) da aynı.
- **Belirlenimlilik:** `?seed=` ile aynı tur tekrar üretilir.
- **Test kancaları:** `?t=`, `?seed=`, `?bot=hic|kotu|orta|iyi|usta`, `?toplu=`, `window.__oyun` (ayrıntı `oyun/b0/TASARIM.md`).
- **Kayıt:** localStorage, sürüm numaralı şema, bozuk kayıtta güvenli varsayılan. Yedek kodu B1 sonrası.
- **Performans:** 60 fps; nesneler havuzlanır; ekranda en çok ~150 nesne, 2.000 parçacık; 3 kalite kademesi.

---

## 11. Gözden kaçmasın listesi

| Konu | Karar |
|---|---|
| Kesinti | Arka plana geçince otomatik duraklar; dönüşte 3-2-1 |
| Ekran | Dikey kilit; güvenli alan; tek elle; dokunma ekranın her yerinde (düğmeler hariç) |
| İlk açılış | 5 s altında; ilk tur 3 ipucu: "Yeşilde dokun", "Dalış için dokun", "Balonun üstüne düş" |
| Ses | İlk dokunuşla başlar; müzik ve efekt ayrı; sessiz oynanabilir |
| Erişilebilirlik (B0/B1) | Ayarlar, duraklat, hareket azaltma, ışığa duyarlılık, yazı boyutu; şekil kodlaması her zaman açık (tehlike = üçgen, fırsat = daire). Renk körlüğü modu B1 sonrası |
| B1 sonrası | Renk körlüğü modu, yedek kodu ver/al, satın alma kilidi, istatistik ekranı (KARARLAR) |
| Haksızlık | Ölümcül uyarısı ≥ 1,2 s; sömürü sınırları (kural 8) |
| Takılma | Para sıfırken bile tur kazancı > 0 (taban 25); her zaman alınabilecek bir geliştirme var |
| Telif | BB'den isim, görsel, ses, metin alınmaz; yalnız mekanik fikirler |
| Gerçek bilgi | Bilgi kartlarındaki her not yayından önce doğrulanır |
| Ton | Evrensel çizgi film; yerel gönderme yok (KARARLAR) |
| Dil | Tüm metinler dil dosyasında, Türkçe |

---

## 12. Kabul ölçütleri ("4,5 yıldız" testi)

| Ölçüt | Hedef | Nasıl ölçülür |
|---|---|---|
| İlk "vay" anı | ≤ 5 s, turların ≥ %90'ında | Bot + `vay_t` |
| Beceri farkı | Tur 1: iyi ≥ hiç + %30; aynı geliştirmelerle tur 5 ve 10: ≥ + %60 | Aynı tohumla 20'şer tur |
| Tur süresi | Tur 1: 16–30 s; tur 15–25 medyanı 45–55 s; tavana çarpan ≤ %10 | Bot |
| Yeniden başlatma | ≤ 3 s | Ölçüm |
| Satın alma ritmi | Art arda ≤ 3 tur alışverişsiz | Sim + JS kampanyası |
| Yenilik ritmi | Her 2–4 turda yeni nesne, bölge ya da rakip | ICERIK §5 |
| Kare hızı | Ortalama ≥ 58, en düşük ≥ 50 (S24 Ultra) | Senin telefon testin |
| Hata | Konsolda 0 hata, 30 dk bot oyununda çökme yok | Testçi |
| Mantık | §3'teki 8 kural: otomatik çarpışma denetimi + elle kontrol | Denetçi |
| Senin kararın | "Burrito Bison'a yakın ve eğlenceli" | Her fazın sonunda |

---

## 13. Ekip ve iş akışı

| Ajan | Görevi |
|---|---|
| Yönetmen (ana oturum) | İşi böler, ajanları çalıştırır, sonuçları sana sunar, commit atar |
| `oyun-tasarimci` | Şartnameler, sayılar, ekonomi |
| `uygulayici` | Kod |
| `gorsel-sanatci` | Tarz kareleri, modeller, efektler |
| `ses-tasarimci` | Efektler ve müzik |
| `oyun-testcisi` | Bot oyunları, ölçümler, ekran görüntüleri |
| `denetci` | Her plan ve teslimattan önce: kullanıcı istekleri, mantık kuralları, kapsam |

---

## 14. Fazlar

| Faz | İçerik | Bitiş ölçütü |
|---|---|---|
| **B0 · Gri kutu** | Şartname: `oyun/b0/TASARIM.md`. Rampa göstergesi, uçuş fiziği, dalış, 5 nesne (martı, reklam balonu, reklam zeplini, uçurtma, yakıt dronu), 1 son şans, ses duvarı, kara kutu, 6 kartlık hangar, kayıt, ayarlar/duraklat/erişilebilirlik | B0 kabul ölçütleri tutuyor; sen "eğlenceli" diyorsun. **Eğlenceli değilse sonraki faza geçilmez** |
| B1 · Dünya, ilk 25 tur | ~24 nesne, 5 nadir olay, 6 fırsat, 3 rakip, eşikler (ses → yörünge), hangar (§7), sim eşliği | İlk 25 tur baştan sona oynanıyor |
| B2 · Görünüm | Onaylı konsept yönünde (`oyun/konsept/`) modeller, animasyon, efektler, arayüz | Telefonda 60 fps, senin onayın |
| B3 · Ses | Efektler, hızla katman kazanan müzik | Senin onayın |
| B4 · Cila | İlk açılış, ipuçları, 3 roket, denge | §12'nin tamamı |
| B1.5 · Dünya tamamı | Tur 26–40 içeriği (taslak), kaçış | Dünya bölümü bitiyor |
| B5+ · Bölümler | Ay → … → Plüton | Her bölüm için aynı döngü |

---

## 15. Kaynaklar

- [Burrito Bison: Launcha Libre resmî sitesi](https://www.burrito-bison.com/)
- [TalkAndroid rehberi](https://www.talkandroid.com/burrito-bison-launcha-libre-tips-hints-strategies/)
- [GameGrin incelemesi](https://www.gamegrin.com/mobile/burrito-bison-launcha-libre-review/)
- [GameSkinny: özel jöleler](https://www.gameskinny.com/tips/burrito-bison-launcha-libre-special-gummies-guide-with-tips/)
- [Gamezebo incelemesi](https://www.gamezebo.com/the-best/burrito-bison-launcha-libre-review-mucha-diversion/)
- Simülasyon: `oyun/sim/ucus_sim.py`, `oyun/sim/RAPOR.md`
- Taslak 5: `oyun/tasarim.html`

---

## 16. Sorulacaklar (kullanıcıya)

**S1. Yüksekte asılı kalınca kademe.** Onaylı kural: tropopoz üstünde yatay hız 2 s < 110 → tur biter. Sim'de bu, roketin elinde kademe varken oluyor (tur 25'te iyi botun 20 turunun 19'u; §5.3).
(a) Kural kalır, tur biter. (b) Kademe varsa önce kademe ileri doğru ateşlenir, kademe yoksa tur biter. **Öneri: (b).** Son şans kuralının amacıyla tutarlı, kademe geliştirmesini işe yarar kılar.

**S2. Geç dönem gelir kaldıracı** (§5.3 S3).
(a) İrtifa bandı çarpanı: üst atmosfer ×1,8, uzay ×3; ekranda "İZLENME ×1,8" (yüksek irtifa görüntüsü daha çok izlenir). (b) Hız primi: nesne ödülü × (1 + v/250). (c) Çarpan yok; fiyat artışı 1,55 → 1,45 (geç geliştirmeler ucuzlar). **Öneri: (a).** BB'de de ileri bölgeler daha çok kazandırır; eşik geçmenin kalıcı bir değeri olur.

**S3. Boş dalış toparlanması** (§5.3 S6). Konide hedef yokken dalış:
(a) Bugünkü gibi 70° aşağı, 1,2 s. (b) 0,4 s sonra burun kalkar, hızın %10'u gider. (c) Hedef yokken dalış hiç tetiklenmez (boş titreşim). **Öneri: (b).** Hata cezalı ama yıkıcı değil. (c) dokunuşu "bozuk" hissettirir.

**S4. Ekranda uçan sayılar.** (a) Doğrudan jeton (konseptteki jeton sayacıyla tutarlı). (b) İzlenme, tur sonunda jetona çevrilir. **Öneri: (a).**

**S5. Hedef değişiklikleri** (§5.3 D1, D2, D3, D5, D6): mesafe hedefini kaldırmak, yörüngeyi "iyi 24–27 / orta ≤ 34" bandıyla ölçmek, tur 5 kazancı 500, ses duvarı tur 2–3, beceri farkı ölçütü. (a) Hepsini onayla. (b) Tek tek konuşalım.

**S6. Yeryüzü dekoru** (deniz yok kuralıyla; konsept görselde uzakta kıyı görünüyor). (a) Tarlalar, tepeler, küçük kasaba. (b) Uzakta kıyı şeridi, yalnız dekor, oynanışa girmez. **Öneri: (a).** "Deniz yok" kararını görselde de net tutar.

Rakip karakterleri, reklam yazıları, kaplamalar ve meta sistemlerin kapsamı için sorular: `ICERIK.md` §10.
