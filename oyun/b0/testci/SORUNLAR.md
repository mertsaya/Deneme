# B0 playtest sorun listesi

Tarih-saat: 2026-10-08 20:02 – 20:40 (UTC). `oyun/b0/index.html` bu sürede iki kez değişti (20:18'de güncellendi); bot ve kabul sayıları 20:38 koşusundan, canlı senaryolar 20:10 – 20:35 arası koşulardan. Oyun kodu değiştirilmedi, commit atılmadı.

Yöntem: Playwright + Chromium (swiftshader, headless, 384x832 DPR2 mobil), betikler `oyun/b0/testci/senaryo_*.py`, ham veri `testci/cikti/senaryo_*.json`, görüntüler `testci/cikti/senaryo/` ve `testci/cikti/kontak.png`.

Sınır: "his" ölçülemez. Hit-stop, sarsıntı, ses, titreşim headless ortamda duyulmaz/hissedilmez; yalnız aşağıdaki ölçülebilir göstergeler raporlanır. Gerçek telefonda K16 gerekir.

## Ölçülebilir his göstergeleri

| Gösterge | Sonuç |
|---|---|
| Rampa dokunuşu - tepki (pointerdown -> sonraki kare, fizik durumu değişti) | 2 ms (aynı kare) |
| Dalış dokunuşu -> gösterge/hız değişimi | 18 ms (1 kare) |
| TEKRAR UÇ tıklaması -> RAMPA | 0,19 s (kabul.py 0,29-0,44 s) |
| Ölü zaman (tur bitişi -> yeni rampa) | BITIS 1,0 s + kara kutu (en az 0,3 s kilit) + 0,2 s = en kısa ~1,5-1,8 s; sınır 3 s içinde |
| Tur süresi dağılımı, tur 1 (20 tohum) | iyi ort 16,5 (min 11,5 / maks 24,6) · orta 15,6 (9,3 / 24,9) · kötü 15,3 (9,2 / 25,0) · hiç 15,9 (12,5 / 20,2) s |
| İlk 5 s günlük olayı (sekme/dalış/son şans) | iyi 2,8 · orta 3,1 · kötü 2,9 · hiç 1,9 (min 1). İlk olay ~1,5-2,1 s |
| Tur başına sekme / mükemmel / dalış (ort.) | iyi 2,7 / 0,80 / 1,1 · orta 2,6 / 0,65 / 1,1 · kötü 2,5 / 0,45 / 1,1 · hiç 2,2 / 0 / 0 |
| "Vay" anı (`vay_t`) | iyi 2,6 s · hiç 4,5 s; <=5 s oranı iyi %90, hiç %100 |
| Tur 1 en yüksek hız | ~87-94 iç hız (~1.000-1.120 km/sa); ses duvarı (115) tur 1'de hiç kırılmıyor (kampanya medyanı iyi tur 3-4, hiç tur 6) |
| Bot beceri farkı, tur 1 | mesafe iyi/hiç 1,53x (K3: 1,63x), kazanç 121 / 97 jeton (+%25), tur süresi aynı |
| Elle rampa (yeşilde dokun) vs dokunmayan, 3 tur | 401 vs 300 jeton (n=3, gürültülü); spam 249 jeton |
| Kampanya, 15 tur | hiç botu tur süresi 13 -> 16-27 s, iyi botu tur 11'den itibaren 53-61 s |
| fps (headless swiftshader) | ort 57-60; 5 dk koşuda 20 sn pencerelerinin hepsi ort >=58, p99 <=33 ms, en uzun kare 100 ms |
| Tek seferlik takılma | tek kare 150-283 ms, min anlık fps 6-12 (tur başı/geçişler; swiftshader'a bağlı olabilir) |
| 5 dk bellek | JS heap 3,7-4,6 MB sabit, dinleyici 62 sabit, DOM düğümü 335-759 salınıyor ama büyümüyor; kalite oto 2,0 -> 1,5 (82. s) sonra kararlı; 15 tur, konsol hatası 0 |
| Konsol hatası (tüm senaryolar) | 0 |

Hazır betikler: calistir.py OK (fps 58,6, hata 0); bot_tur.py 20 tur x 4 bot hepsi bitiş `yer`, 65 s tavanına çarpan 0; kontak.py 7/8 kare (ses duvarı karesi yok: tur 1'de kırılmıyor); kabul.py --hizli K1-K3, K7-K10, K12-K15 GEÇTİ, K4-K6 BİLGİ (K5: iyi 4. turda, hedef 2-3; K6: iyi t5-15 medyan 53 s, hedef 20-40), K11 ve K16 elle.

## Sorunlar

### 1. [önemli] 360x780 + yazı "Çok büyük" (x1,4): kara kutuda ana düğme TEKRAR UÇ ekran dışına taşıyor ve iki satıra bölünüyor
- Yeniden üretme: kayıtta `ayar.yazi = 1.4`, 360x780 görünüm, bir tur bitir.
- Beklenen: TEKRAR UÇ tamamı görünür, tek satır (TASARIM §13.4 "taşma olmaz").
- Gerçek: kkTekrar/kkHangar alt kenarı 805 px > 780 (`DISARI kkTekrar 166,697,344,805`); "TEKRAR / UÇ" iki satır, alt yarısı kesik. `kabul.py` K15 bunu yakalamıyor (384x832'de ölçüyor). 384x832 ve 412x915'te sorun yok.
- Görüntü: `testci/cikti/senaryo/g_360x780_kk_y1.4.png`, özet `g_sheet2.png`.
- Öneri: ekranda kaydırma yerine düğme çubuğunu `position: sticky; bottom` yap, kart/döküm alanını kaydır; 1,4'te "Seni durduran" metnini kısalt.

### 2. [önemli] 360x780 + x1,4: Ayarlar'da "Açık/Kapalı" düğmeleri üst üste biniyor
- Yeniden üretme: aynı koşul, Ayarlar ekranı (hangar dişlisi).
- Beklenen: etiket ve düğmeler çakışmaz. Gerçek: "Hareket azaltma" ve "Işığa duyarlılık" satırlarında "Kapalı" ile "Açık" düğmeleri birbirinin üstüne biniyor, metin okunmuyor. Erişilebilirlik ayarının kendisi erişilemez oluyor.
- Görüntü: `g_360x780_ayar_y1.4.png`.
- Öneri: ayar satırlarını dar/büyük yazıda etiket üstte, düğmeler altta tek sütun yap (384'te zaten sarıyor, 360'ta taşıyor).

### 3. [önemli, tasarım/denge] Geliştirmeler kötü/orta oyuncuda hissedilmiyor, iyi oyuncuda tavana gidiyor
- Yeniden üretme: `python3 bot_tur.py --kampanya 15` (kampanya medyanları) ve elle kampanya (aşağıdaki tur süreleri).
- Gerçek: hiç botu 15 turda 13 s -> 16-27 s, kazanç 95 -> ~224 jeton; ses duvarı ilk kırılış tur 6. İyi botu tur 9-15'te 53-61 s (65 s tavanına çok yakın), kazanç 600-760. Yani "tekrar oynama sebebi" beceriyle ayrışıyor ama zayıf oyuncu için görünür ilerleme yok. Tur 1'de dokunmayan ile iyi oyuncunun tur süresi aynı (~16 s), fark yalnız mesafe/jeton.
- Beklenen (KARARLAR): zayıf oyuncu da yavaş ama belirgin ilerler; K5 iyi tur 2-3.
- Görüntü: `cikti/bot_tur.json`.
- Öneri: tur 1-5 için zayıf oyuncuya ilk alımın etkisi (örn. Rampa gücü 1) tur süresini/hızı ölçülebilir yükseltsin; K6'daki iyi bot tavanı için seyrekleştirme kuralı (uygulayıcı üzerinde) ayrıca doğrulanmalı.

### 4. [küçük] Hangar: 360x780 + x1,4'te roket ezilmiş (72 px yükseklik)
- Görüntü: `g_360x780_hangar_y1.4.png` (kartlar 534 px alıyor, roket küçülüyor). Öneri: roket alanına min-height ver ya da kart açıklamasını gizleyip kısalt.

### 5. [küçük] Hangar kart açıklaması 11,5 px
- 384x832, x1,0'da kart açıklama metni ("Kalkış hızı 661 -> 948 km/sa") 11,52 px; telefonda okunması zor (hedef >=12-13). Görüntü: `g_384x832_hangar_y1.0.png`.

### 6. [küçük] İlk açılışta iki dokunuş gerekiyor
- Yeniden üretme: ilk açılış. İlk dokunuş "yalnız başlatır" (iğne bekler, "Başlamak için dokun"), ikinci dokunuş kalkış. Hiç dokunmazsanız tur sonsuza kadar bekler (80 s bekledim, ilerleme yok). Tasarım gereği (tam ekran/ses izni) ama yeni oyuncu için ilk 5 s'de ölü an. Görüntü: `a_hic_rampa.png`.
- Öneri: ilk dokunuşta iğne zaten başlasın (iğne p=0'dan 0,84 s'ye kadar zayıf bölgede kalıyor) ya da ilk turda iğnenin yarım sürede otomatik kalkışa geçmemesini koru ama ilk dokunuşu kalkış sayma.

### 7. [küçük] Sayfa gizlenip görününce `bekleyen` siliniyor, ama tur duraklatılmış durumda; bu halde süreç öldürülürse tur kazancı kaybolur
- Yeniden üretme: uçuşta `visibilitychange` hidden -> visible (menü açık kalır), sonra sayfayı kapat. Gözlem: gizlenince `bekleyen={j:39}`, görününce `null`, jeton değişmedi. Çift sayım yok (tur sonu jeton farkı = kara kutu toplamı, gizle-görün-gizle çiftlemesi tek `bekleyen`). Yani güvenli, yalnız kaçırılan kazanç.
- Öneri: `bekleyen`i görününce değil, tur gerçekten devam edince (DEVAM sayımı bitince) sil.

### 8. [küçük] Kayıt doğrulaması: sınırsız büyük sayı ve yeni sürüm
- `jeton: 1e308` ve `bekleyen: 1e12` olduğu gibi kabul ediliyor (bildirim "+1.000.000.000.000 jeton"). `v: 99` kayıt "bozuk" sayılıp sıfırlanıyor (777 jeton `sdp_kayit_bozuk`ta saklanıyor, oyuna dönmüyor). Eksi jeton 0'a, bozuk sv/ayar düzeltiliyor ("Kayıt kısmen onarıldı"), JSON hatası/null/dizi/sayı güvenli varsayılana düşüyor; çökme ve konsol hatası yok (16 vaka).
- Öneri: jeton ve bekleyen için makul üst sınır (örn. 1e9) ve `v` > mevcut için ayrı bildirim.

### 9. [küçük, test kancası] `__oyun.olaylar` yalnız sekme/dalış/boş dalış/son şans içeriyor
- Martı/uçurtma/ip/balon teması günlükte yok; "ilk 5 s olay sayısı" ve kontak.py'deki "ses duvarı" arama deseni bu yüzden zayıf. Öneri: `temas` olayları (tür, t) günlüğe eklensin.

### 10. [küçük] Tek kare takılmaları 150-283 ms (swiftshader)
- Gözlem: rampa/geçiş anlarında en uzun kare 150-283 ms, 5 dk koşuda 100 ms; telefonda ayrıca ölçülmeli (K11 elle).

## Geçen kontroller (sorun yok)
- (a) Hiç dokunmadan 3 tur: ilk dokunuştan sonra otomatik "iyi" kalkış (rampa 3,0 s), tur 11-14 s, kara kutu doğru, jeton 300.
- (b) Spam (her karede dokunan): rampada ilk karede "zayıf" kalkış (prim 0), dalışlar boş dalış toparlanmasına gidiyor, tur ~5 s'de son şans, jeton 249 < dokunmayan 300 (spam cezalı). Çökme yok.
- (c) Yalnız rampada dokunan: kalkış primi 18, jeton 401 / 3 tur.
- (d) Duraklat -> devam -> yeniden başla: duraklatmada x donuyor, menüde ve 3-2-1'de dokunuş dalış yapmıyor, rampada duraklayınca iğne duruyor, YENİDEN BAŞLA "Yarım uçuş: +54 jeton" (taban/prim yok), HANGAR/UÇ akışı çalışıyor.
- (e) visibilitychange: aynı karede duruyor, `bekleyen` yazılıyor, öldürülünce açılışta bir kez ekleniyor ("Yarım kalan uçuş: +35 jeton"), ikinci yenilemede tekrar eklenmiyor.
- (f) Bozuk localStorage: yukarıdaki not dışında 16 vakanın hepsinde çökme yok.
- (g) 384x832, 360x780, 412x915 (x1,0): HUD çakışması ve taşma yok; roket-gösterge çakışması yok; kara kutu/hangar/ayarlar temiz (x1,4'te yalnız 360x780 bozuk, madde 1-2).
- (h) Hızlı ardışık 10 tur (bot, hiz 8): her tur jeton farkı = kara kutu toplamı, `tur` 1..10, `son` son 3 turu doğru kaydırıyor, rekor tutarlı. Yenilemede jeton 1 artıyor, çünkü tur uçuştayken "yarım kalan uçuş" yazıldı (beklenen).
- (i) 5 dk sürekli oyun: 15 tur, fps/bellek kararlı (tablo).

## Dosyalar
`oyun/b0/testci/senaryo_a_hic.py` (a/b/c; argüman hic|spam|rampa), `senaryo_d_duraklat.py` (d+e), `senaryo_f_bozuk.py`, `senaryo_g_yerlesim.py`, `senaryo_h_kayit.py`, `senaryo_i_uzun.py`, `senaryo_his_metrik.py`, `senaryo_ortak.py`. Ekran görüntüleri `oyun/b0/testci/cikti/senaryo/`, kontak `oyun/b0/testci/cikti/kontak.png`.
