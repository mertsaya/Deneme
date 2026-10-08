# Kullanıcı kararları (yaratıcı yön)

Ajanlar bu dosyayı kesin kabul eder; değiştirmek için kullanıcıya sorulur.

| Tarih | Konu | Karar | Not |
|---|---|---|---|
| 2026-10-08 | Oynanış | Burrito Bison mantığı | Gerçekçi simülasyon (A0) reddedildi |
| 2026-10-08 | Kamera / kontrol / tarz | Yandan 2.5B · tek dokunuş + zamanlama · renkli çizgi film | |
| 2026-10-08 | Zemin | Her şey gökyüzünde, deniz yok | Sekme yüzeyi havadaki nesneler |
| 2026-10-08 | Son şans | Yere düşmek üzereyken kademe ayrılır, üstteki kademe olay yerinden yeniden fırlar | İlerleme bir hatayla kaybolmasın |
| 2026-10-08 | Ölümcül çarpışma | Tur bitmez, bir kademe kaybedilir; son kademedeysen tur biter | Uyarı ≥ 1,2 s |
| 2026-10-08 | Pilot | Maskot pilot (çizgi film astronot; son şansta kapsülde kalır) | Oyunun yüzü |
| 2026-10-08 | Ton ve kültür | **Evrensel** çizgi film tonu, yerel gönderme yok | ICERIK'teki Simit/Nazar/Lokum kaplamaları, "SICAK SİMİT" reklamları, Türk karakterli rakipler ve yerel bilgi kartları değiştirilecek |
| 2026-10-08 | Fırsat dokunuşu | Her fırsat nesnesinin kendi mini zamanlama oyunu | Öğrenme yükü için: her yeni mini oyun ilk karşılaşmada tek satır ipucuyla, turda en çok bir yeni kural |
| 2026-10-08 | Araçlar | Playwright+Chromium, gltf-transform, adb kuruldu; KTX-Software indirildi (kurulum yönetici onayı ister, B2'de) | |
| 2026-10-08 | Nadir olaylar | Komik ve tuhaf (şişme kedi, balina zeplin, sahte uzaylı = rakip zeplini, leylek termalleri, meteor şok dalgası) | Absürt ama kendi içinde mantıklı |
| 2026-10-08 | Kargo kapsülü kartları | 3 kartın üçü de kazanılır | |
| 2026-10-08 | Müzik | Enerjik çizgi film; hızlandıkça katman kazanır | |
| 2026-10-08 | B1 kapsamı | Önce ilk 25 tur (~24 nesne, 5 nadir olay, 6 fırsat) | Eğlence kanıtlanınca gerisi |

## 8. oturum kararları (2026-10-08, kullanıcı onaylı)
- Para birimi: **altın jeton** (₺ kaldırılır; evrensel ton).
- Sekme açısı: bilim balonu **40°** (fazla irtifa üst atmosfer sönümüyle çözülür); habitat **15°** ama ayrı nesne sınıfı ("kayma yüzeyi"). Görsel tasarımı kullanıcı onayına gider.
- Zayıf oyuncu: dokunmasa da geliştirmelerle **yavaş ama ilerler** (ısı duvarı ~tur 25, Kármán ~tur 45). Beceri hızlandırır, şart değil.
- Kapsam: B0/B1'e yalnız **ayarlar, duraklat, erişilebilirlik** girer. Renk körlüğü modu, yedek kodu ver/al, satın alma kilidi, istatistik ekranı B1 sonrası.
- Sanat yönü (kullanıcı onaylı): `oyun/konsept/` altındaki üç konsept (oyun içi, hangar, ana ekran) kabul: parlak renkli çizgi film, kalın yumuşak hatlar, parlak yuvarlak arayüz, maskot pilot. Görsel yazılar kodla konur (üretilen görseldeki yazılara güvenilmez). Ana ekranda Plüton daha belirgin olmalı.
- Kabul edilen kurallar (kullanıcı onaylı): (1) tropopoz üstünde yatay hız 2 sn boyunca 110'un altında kalırsa tur biter (`vx_dur`); (2) turda en çok 5 fırsat nesnesi, römorkör hariç (`firsat_tur_max`); (3) dalış itkisi gelişimi 14→54 (4,0/sv).
- PLAN_B §16 / ICERIK §10 önerileri kabul (kullanıcı onaylı): vx_dur'da önce kademe ateşlenir; geç dönem kazanç = irtifa bandı; boş dalış 0,4 s sonra toparlanır; yeryüzü dekoru tarla; rakipler adsız hayvan maskot arketipleri; hedef değişiklikleri (mesafe 150 km bilgi satırı, tur 5 kazanç 500, ses duvarı tur 2–3, tur 1 beceri farkı ≥%30); uçan sayılar jeton; görev/albüm/günlük hedef/hayalet B1 sonrası; römorkör y 1500'de kalır. Simülasyon ayarları S1–S9 uygulanacak (bulut, Opus).

## B0 kararları (2026-10-08, kullanıcı onaylı)
- Yakıt dronu B0'a **mini oyunla** girer (halka daralınca dokun; ayrıntı b0/TASARIM.md §7.4, öneri olarak işaretli, gri kutuda ayarlanır).
- Dalış hedef vurgusu: **var** (`vurgu: 1`).
- İlk açılış: **hangarsız ilk tur**, hangar ilk turdan sonra açılır.
- Bitiş sahnesi: **karışık** (normal bitişler sakin, rekor / büyük kayıpta abartılı).
- "Seni durduran şey" metinleri: **öğretici** ton.
- (B0 denetimi sonrası, kullanıcı onaylı) Abartılı bitiş: mesafe rekoru %10'dan fazla aşılınca (ilk tur hariç) ya da tur mesafesi son 3 turun ortalamasının yarısından kısaysa; diğer bitişler sakin. Rakip zeplini B0'da yok, kalkış primi kalır (S1 b). Dron halkası yalnız dron rotadaysa açılır.
- (Ses, kullanıcı seçimi, 2. seçim) Seçimler `oyun/ses/SECIM.md`: müzik A, motor tutuşma c, motor uçuş b (puansız), trambolin c, martı c, balon c, kademe ayrılma i, dalış b, mükemmel e, ses duvarı b, jeton d, tık a, kart satın alma a, son şans b.
- (B1 görsel dilimi, kullanıcı onaylı) Roket boyu kararı Claude'a bırakıldı: **kamera yakınlaşır** (B1'de; ekran yoğunluğu/ileriyi görme sim'de yeniden ölçülecek). Arayüz onaylı konsept düzeni + küçük pilot rozeti. Pilot: açık vizörlü mevcut maskot. Engel yüzleri: balon, zeplin, uçurtma, dron, martı hepsinde yüz.
- (B0 telefon testi, kullanıcı onaylı) Kalkış açısı oyuncu seçimi: rampada önce açı ibresi (kilitlenir), sonra güç ibresi (iki dokunuş); açılar arasında mantıklı tatlı nokta, tek açı baskın olmasın. Nesne yoğunluğu ~%30 seyreltilir (ekran başı 7→5). Motor uçuş sesi her koşulda çalmalı (sentez yedeği).

## B1 kararları (2026-10-08, kullanıcı onaylı; kaynak: oyun/B1_ONERI.md, 12 soru)
- **Görsel yol:** B1 başında önce görsel dilim (roket, pilot, B0'ın 5 nesnesi son kalitede); kullanıcı onaylayınca aynı kaliteyle kalan nesneler çoğaltılır. Çizim kalitesi Burrito Bison'un altında bulundu; kodla çizilmiş vektör yol yeterli değil (Blender 3B→sprite denemesi sürüyor).
- **Pilot:** yüz ifadesi (6) + kısa anlamsız sesler, yazı yok.
- **Komik ton:** tokat-şaklak komedi (abartılı şaşkın gözler, sersemleme yıldızları, savrulup toparlanma); şiddet yok, herkes toparlanır.
- **Roket evrimi:** her hangar sekmesinin görünür parçası, parça 2 kademede büyür, belli seviyelerde bütün roket evrim geçirir (~12 parça modeli).
- **Vay anları (B1'e girer):** bant başlık kartı, yeni nesne tanıtımı, zengin bant dekoru, kartpostal anı.
- **Kara kutu:** sonraki hedefe kalan (gerçek sayı) + bu tur ve en iyi tur eğrisi. (Sonraki alıma kalan jeton ve anlık tekrar B1'e alınmadı.)
- **B1 sonrası ilk meta:** görevler (aynı anda 3, rütbe).
- **Seri ödülü:** seri yok, cezasız (hoş geldin hediyesi).
- **Rekabet:** yalnız kendi rekorları (sunucu yok).
- **Kayıt:** yerel çift kayıt.
- **Hedef yaş:** herkes, çocuk hedefli değil (içerik şiddetsiz ve çocuk dostu kalır).
- **Para modeli:** ilke şimdi: parayla güç satılmaz, enerji yok, reklam yok; model yayına yakın sorulur.
- (B0 telefon testi, kullanıcı onaylı) **Sanat yönü güncellemesi:** vektör ve Canva denemeleri 'çocuksu / ilkokul seviyesinde' bulundu. Yeni yön: **Burrito Bison kalitesi ama çocuksu olmayan**: neşeli abartılı ton ve ifadeler korunur; çizim kalitesi, ayrıntı, malzeme ve renk uyumu premium; basit yuvarlak şekiller yerine detaylı tasarım; genç yetişkin astronot; bebeksi büyük göz/pembe yanak yok. (Önceki 'parlak renkli çizgi film' onayı bu yönle birlikte yorumlanır.) Canva ticari kullanım şartları yayından önce kontrol edilecek.
- (B0, kullanıcı onaylı) Kalkış açısı iki dokunuşlu seçim uygulandı; nesne yoğunluğu ekran başı 5; motor sesi sentez yedekli.
