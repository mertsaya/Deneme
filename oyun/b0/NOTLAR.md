# B0 uygulama notları (uygulayıcı, 2026-10-08)

Kaynaklar: `TASARIM.md` (şartname), `oyun/KARARLAR.md`, `oyun/sim/ucus_sim.py`, koordinatör yayın notu.

## Karara bağlananlar (kullanıcı, koordinatör aracılığıyla; uygulandı)

- **Bitiş sahnesi:** abartılı bitiş yalnız şu iki durumda. (a) Mesafe rekoru %10'dan fazla aşıldıysa (ilk tur hariç). (b) Tur mesafesi son 3 normal turun ortalamasının yarısından kısaysa. Geri kalan her bitiş sakin; yer/durma ayrımı ölçüt değil (`B0_ARAYUZ.abarti_*`). Kayda `son_mesafe` eklendi.
- **Rakip zeplini:** B0'da yok, kalkış primi kalıyor (S1 (b)).
- **Dron halkası:** yalnız dron rotadaysa başlıyor: |rota_nokta(τ).y − o.y| ≤ 2·(r+4) (`YAKIT_HALKA.rota_kat`).
- **"Seni durduran" metinleri:** "trambolin" yerine "balon ya da zeplin" yazıldı; süre metni verildi. Ses kuralının eşiği en yüksek hız ≥ ~100 (`durduran_ses_v`). Öbür metinler hâlâ benim yazdığım öğretici yer tutucular.
- **Tur sayacı:** elle bitirilen turlar `kayit.elle` alanında ayrı sayılıyor. `kayit.tur` yalnız doğal bitişleri sayıyor (K16 sayımı şişmesin). Elle turlar `son`, `son_dalis` ve `son_mesafe` ortalamalarına da girmiyor.

## Sorulacak

1. **Elle bitirilen turda kara kutu** gösterilsin mi? Şimdilik gösterilmiyor; kazanç bildirimle yazılıyor.
2. **Denge (eski ölçüm, aşağıdaki "Sim S1–S9 eşlemesi" bölümüne bak).** Sim güncellendikten sonra `kabul.py --hizli` sonuçları:
   - K5: iyi bot ses duvarını medyan 4. turda kırıyor (hedef 2–3).
   - K6: iyi bot 5–15. turlarda medyan 52 s uçuyor, turların %42'si 65 s tavanına çarpıyor (hedef 20–40 s, ≤ %5).
3. **K6:** koordinatör seçenek (b)'yi seçti; uygulandı (aşağıda "B0 seyrekleşmesi").

## Denetim düzeltmeleri (uygulandı)

- **Kamera:** zemin ekran altından 160 px yukarıda (`alt_pay_px`). Aynı kaydırma `Ucus.ekran()` içinde de var (görüntüsüzde `kay` = 0, sim aynen). Rampa göstergesi altta %43'te: istenen ~%34'te roket rampadayken göstergenin altında kalıyordu. Rampa sırasında ipucu göstergenin üstünde.
- **His:** sarsıntı genliği 0,05. Duraksama sırasında hiç fizik adımı atılmıyor. Ara değer (alfa) en çok 1.
- **HUD:** rampada da güncelleniyor (eski turun sayıları kalmıyor).
- **İlk açılış:** iğne ve otomatik kalkış ilk dokunuşa kadar bekliyor ("Başlamak için dokun"). O dokunuş yalnız tam ekranı ve sesi başlatıyor. Ses `state !== 'closed'` ise çalıyor. `ipucu.rampa` yalnız insan dokunuşuyla yazılıyor.
- **Bekleyen:** `bekleyen = { j, ses }`. Açılışta `ses` doluysa `duvar.ses` yazılıyor, ödül ikinci kez alınamıyor. Eski biçim (sayı) de kabul ediliyor.
- **Küçük görseller:** üstten sekmede balon/zeplin 0,15 s 2,5 birim aşağı itiliyor. Dron bidonu rokete uçuyor. İrtifa yazıları büyütüldü.
- **Tahsis:** HUD önce sayıyı karşılaştırıyor, yalnız değişince biçimliyor. Intl.NumberFormat ve matchMedia önbellekte. Gök gradyanı yalnız renk değişince kuruluyor. Flaş sayacı halka tampon. Yazı tipi dizgileri, kesik çizgi deseni ve pervane dizisi önbellekte.
- **404:** kabul koşusundaki 2 adet 404, `kabul.py` K13'ün kendi açtığı `/__bos__` sayfasından (betikte iki `goto`). Oyun hiçbir dosya istemiyor; favicon `data:` URI. Gidermek için testçinin boş sayfayı `about:blank` ya da var olan bir dosyayla değiştirmesi gerekiyor (testçi dosyalarına dokunmadım).

## Şartnameyle çelişen ya da şartnamede eksik olup kendim çözdüklerim

- **Çizici (koordinatör notu, şartnameyi geçersiz kılar):** Three.js ve `lib/three.module.min.js` yok. Tek dosya, bağımlılıksız **Canvas2D** kullandım. §14'teki "perspektif kamera, 50°" yerine düzlemsel kamera var; bulut paralaksı aynı geometriden hesaplanıyor (`d/(d+z)`, d = 50° görüş açısına denk uzaklık). Oynanış dikdörtgeni kuralları (W, 2,1, gerçek oran) aynen geçerli.
- **Yapılandırma:** `araclar/ayar_uret.py` sim'i içe aktarıyor, `ayar.json` dosyasını ve `index.html` içine gömülü JSON'u yazıyor. Oyun yalnız gömülü bloktan okuyor (fetch yok). `--denetle` çalışıyor.
- **Ekonomi sayıları:** §3 ve §9'daki ×2,4, km başına 70 ve prim katsayısı 0,6 eski kalmış. Kod sim'deki güncel değerleri okuyor: `nesne_prim` 2,0, `km_odul` 55, `rakip_odul` 0,45. Sim'deki irtifa bandı çarpanı (`bant_carpan`, S3) da aktarıldı.
- **Sim'de olup şartnamede olmayan iki B0 kuralı aktarıldı:** `seyrek` (S8: uzun uçuşta alçak bantta trambolin ağırlığı azalıyor, garanti de bundan etkileniyor) ve `Ucus.__init__` içindeki `olumcul_zaman` rastgele çekimi. Ölümcül nesne B0'da yok ama çekim sırası korunsun diye o çekim yapılıyor.
- **Sekme garantisi sayacı:** §7.2 "0,25'ten başlar" diyor, sim'de 0'dan başlıyor. Sim mantığını aynen aldım (sonuç yine 0,3 s'de bir).
- **Kalkış primi ve `__oyun.tur`:** sim `tur_oyna()` rakip vermiyor (`rakip_hp=None`), sim `kampanya()` veriyor. JS de aynısını yapıyor: `__oyun.tur` primsiz (K8 eşliği için), `__oyun.kampanya` ve gerçek oyun primli. Prim `sonuc.kazanc_rakip` alanında ayrı duruyor. `?prim=0` oyunda primi kapatır.
- **Bot ve halka:** bot oynarken dokunuş her zaman dalış oluyor (sim'deki gibi); halka sonucu temas anındaki rastgele çekimden geliyor (§7.4). Halka başarılıysa ekranda bot dokunuş halkası çiziliyor.
- **Geç halka dokunuşu:** başarı penceresi temastan 0,05 s sonrasına kadar açık. Temastan sonra dokunulursa +0,25 sonradan ekleniyor (sim sırasından en çok 0,05 s sapma var, yalnız insanda).
- **Kayıt:** görüntülü bot (`?bot=`) kayda yazıyor (testçinin K13'ü bunu bekliyor). `?kayit=0` hiç yazmıyor. `?sv=` ile oynanan tur kayda yazılmıyor, hangarda satın alma da kapalı.
- **Görüntülü bot** kara kutuda 3 s bekleyip yeniden uçuyor.
- **`durum().t`:** RAMPA'da rampa süresi, uçuşta uçuş süresi (testçinin K7'si iğne ilerlemesini buradan ölçüyor). Ayrıca `sarsinti`, `duraklat`, `uyari` alanları ve `__oyun.uyarilar` (K10 denetim uyarıları, `console.warn` ile birlikte) eklendi. `__oyun.olaylar` son görüntüsüz `__oyun.tur` turunun günlüğünü, yoksa ekrandaki turun günlüğünü verir.
- **Jeton sayacı (üst sol):** nesne ödülü + ses duvarı. Kalkış primi, mesafe ve taban kara kutuda ekleniyor.
- **Hız yayı ölçeği** şartnamede yok: 0–250 iç hız (`B0_ARAYUZ.hiz_ust`).
- **İpuçları:** "turda en çok bir yeni kural" kuralını yalnız yakıt halkası ipucuna uyguladım. §3 ve §6 ilk turda hem "Yeşilde dokun" hem "Dalış için dokun" istiyor.
- **Tam ekran, yön kilidi, titreşim:** hepsi try/catch içinde ve isteğe bağlı. Titreşim ilk dokunuştan önce çağrılmıyor. Ses yalnız ilk `pointerdown`'dan sonra başlıyor. alert/confirm yok: kayıt sıfırlama onayı sayfanın içinde.
- **`?t=` (görüntülü):** fizik gerçek ekran oranını kullanıyor, görüntüsüz `__oyun.tur` ise 2,1'i (§14). Bu yüzden aynı tohumda olay zamanları biraz kayabilir. `kontak.py`'nin `__oyun.tur` günlüğünden seçtiği anlar bu yüzden yaklaşık.
- **Kampanya (bilgi):** sim kampanyasında tur 6'dan sonra ölümcül kargo var, B0'da yok. K4–K6 bu yüzden sim kampanyasıyla birebir karşılaştırılamaz.

## Sim S1–S9 eşlemesi (sim ayarı tamamlandıktan sonra)

- `ayar_uret.py` yeniden koşuldu, `--denetle` temiz. S5/S6/S8/S9 sayıları (`bos_dalis_kayip` 0, bant çarpanları, `nesne_prim` vb.) JSON'dan geliyor; kodda gömülü sayı yok.
- **E1 aktarıldı:** boş dalışta y < kademe_y + `bos_dalis_yer` olunca hemen toparlanır.
- **E2 aktarıldı:** `cakisir` ile yeni nesne mevcut nesneyle d < r1 + r2 + `dogus_pay` ise doğmaz; garanti sayacı yalnız nesne gerçekten eklendiyse artar. Fırsat nesnesi doğarken üst üste binen eski tr/yv nesneleri etkisizleştirilir. Rastgele çekim sırası sim'le aynı.
- **Eşlik:** 200 tohum, hic/orta/iyi: dokuz ölçünün hepsi geçti (`test/dogrula.json`).
- **K5:** ses duvarının ilk kırıldığı tur sim'le aynı. Tohum 1–3 iyi botta JS medyanı 4, sim medyanı da 4 (sim'in kendi 20 tohumlu medyanı 3).
- **K6 (B0'da iyi botta tavana çarpan tur %58–61, sim'de ~%20) port hatası değil:** JS, sim'i B0 koşullarında birebir tekrarlıyor.
  - Sim'in kendisini B0 koşullarına kısıtlayınca (yalnız 5 nesne, yalnız yakıt fırsatı, B0 kartları, ısı/ölümcül/rakip nakavtı yok) tavan %52–58 çıkıyor.
  - Etkenleri tek tek ayırdım. Asıl sebep, nesne kümesinin yalnız balon/parti/zeplin/martı/uçurtma olması: sim'de yalnız bu kısıt bile tavanı %51'e çıkarıyor.
  - Özellikle `bilim` balonu eksik (tropopozdan sonra açılıyor, 40°). B0 nesneleri + bilim → %22.
  - Sebep: B0'da y > 500'de hiç nesne yok. İyi oyuncu alçak bantta zeplinden zeplin sekip 65 s boyunca düşmüyor. Sim'de bilim balonu oyuncuyu üst atmosfere taşıyor; orada `vx_dur` ve üst sönüm turu bitiriyor.
  - Öbür kısıtların etkisi küçük: yalnız B0 kartları %25, ölümcül yok %17, ısı yok %17.
  - **Çözüm önerisi (karar verilmedi, uygulanmadı):**
    - (a) `bilim`i ve tropopoz bayrağını B0'a almak.
    - (b) B0'a özel daha sert `seyrek`.
    - (c) K6'yı B0'da bilgi olarak bırakmak (şartnamede zaten bilgi amaçlı).

## Ses (oyun/ses/SECIM.md bağlandı)

- Seçilen 12 efekt, motor döngüsü ve müzik A'nın 3 katmanı `ses/` altına kopyalandı (1,1 MB; lisans `ses/LISANS.md`).
- Sayfa açılışta göreli `fetch` ile indiriyor, ilk dokunuşta çözüyor. Hata olursa sessizce sentez seslere düşüyor (dosyalar engelliyken de denendi: oyun açılıyor, uçuyor).
- Seçimler tek yerde: `SES_SECIM` nesnesi. Puansız seçimler `SES_SECIM.gecici` listesinde.
- **Motor:** uçuşta döngü. Oynatma hızı 0,7 + 0,9·s, alçak geçiren 1200·2^(2,5·s), kazanç 0,55 + 0,45·s; s = hız / 300 (README "Teknik").
- **Müzik:** 1. katman hep çalıyor; 2. katman s 0,25–0,40, 3. katman s 0,55–0,70 arasında açılıyor (uçuş hızına göre).
- Ayarlar: efekt kaydırıcısı efektleri ve motoru kısıyor; yeni **Müzik açık/kapalı** düğmesi var. Kayıtta `ayar.muzik` alanı.
- **Eşlemeler:**
  - Kalkış: tutuşma (mükemmelde ek olarak mükemmel sesi).
  - Trambolin sekmesi: kombo başına +1 yarım ton.
  - Martı ve balon patlaması: kendi sesleri.
  - Son şans: uyarı sesi, 0,12 s sonra kademe ayrılma.
  - Ses duvarı, dalış, kart satın alma, düğme tıkı: kendi sesleri. Boş dokunuşta da tık.
  - Kara kutu sayacı bitince jeton sesi.
  - Uçurtma, ip, dron halkası ve tam dolum: sentez kaldı (seçim listesinde karşılığı yok).
- Sayfa gizlenince ses bağlamı askıya alınıyor, görünür olunca sürüyor.

## B0 seyrekleşmesi (K6, koordinatör kararı (b))

- **Kural:** yalnız B0'da (sim'de yok). Ayar JSON'unda `b0_seyrek` bloğu: `{y: 1000, t0: 30, t1: 45, en_az: 0.05}`. Değerler `araclar/ayar_uret.py` içindeki `B0_SEYREK`'ten gelir.
  - Roket y < 1000'deyken uçuşun 30–45. saniyeleri arasında iki şey doğrusal olarak ×1'den ×0,05'e iner: yönetmenin yoğunluk hedefi, ve sekme garantisinin çalışma olasılığı (o noktada ek bir rastgele çekim yapılıyor).
  - Varsayılan açık; `?b0seyrek=0` kapatır. `test/dogrula.py` eşliği kapalıyken ölçer, `kabul.py` K6'yı açıkken ölçer. `?b0s=y,t0,t1,en_az` yalnız ayar denemesi içindir.
- **Neden yoğunluk, ağırlık değil:** önce trambolin doğma ağırlığını düşürmeyi denedim, işe yaramadı (tavan ~%27'de kaldı). Sebebi şu: y > 220'de yalnız trambolin türleri var, hepsinin ağırlığı aynı oranda düşünce seçim değişmiyor. Ağırlık 0 olsa bile `tip_sec` ilk türü döndürüyor (sim'deki davranış).
- **Ölçüm (40 tohum, 15 turluk kampanya, 5–15. turlar):**

| Bot | Kapalı: medyan / tavan | Açık: medyan / tavan |
|---|---|---|
| iyi | 62 s / %49 | **51 s / %8** |
| orta | 30 s / %15 | 30 s / %1 |
| hiç | 20 s / %0 | 20 s / %0 |

- Ses duvarının ilk kırıldığı tur değişmedi (iyi 3, orta 4, hiç 6). Tur 1 süresi değişmedi; K8 eşliği kural açıkken de geçiyor (tur 1 uçuşları çoğunlukla 30 s'nin altında).

## Mantık denetimi (Opus) düzeltmeleri

Bulgu bulgu durum: `MANTIK_RAPOR.md`; yeniden üretim: `test/mantik_test.py` (10/10).

- Sim'de `gorunur_hedef` önbelleği artık sayaçlı `Nesne.kimlik` kullanıyor (`ucus_sim.py`'ye yalnız bu değişiklik).
- Sonrasında ölçüm:
  - `ayar_uret --denetle` temiz.
  - `dogrula.py 200`: eşlik 27/27, `deger()` sim'le aynı, belirlenimlilik doğru.
  - `kabul.py --hizli`: geçme şartlılar geçti.
  - K7 0,48 s (sınır 0,5; ölçüme Playwright gecikmesi de giriyor).
- **Kullanıcıya bildirilecek yeni metin:** "Ses duvarına çok yakındın: hızını 0,3 saniye daha koru." (en yüksek hız ≥ ses eşiği ama 0,3 s tutulamadıysa).

## Bilinen sınırlar

- **Çoklu sekme:** aynı tarayıcıda oyun iki sekmede açılırsa her sekme kendi bellekteki kaydını yazar, son yazan kazanır (jeton/satın alma kaybolabilir). B0'da ele alınmadı (koordinatör kararı).

## Testçi düzeltmeleri (testci/SORUNLAR.md)

- **(1) Kara kutu ve hangar:** düğme çubuğu ekranın altına sabit (`position: sticky`), içerik kayıyor. Ana düğmeler tek satır: yazı boyutu `clamp(…, 6vw)` ve `nowrap`.
- **(2) Ayarlar:** satırlar sarıyor (`flex-wrap`). Ekran içerikleri sıkışmıyor (`flex-shrink: 0`), TAMAM düğmesi altta sabit.
- **(4) Hangar:** roket en az 110 px; kart açıklaması en az 13 px; ekran kayabiliyor.
- **K15 genişletmesi:** `test/k15_genis.py`, 360×780, 384×832 ve 412×915 görünümlerinde × yazı 1,0/1,2/1,4. Hepsi geçti (9/9); görüntüler `test/k15/`.
- **(6) Duraklatılmış turun kazancı:** §13.1 gereği görünür olunca `bekleyen = null` kalıyor (K13 bunu bekliyor). Kazanç aynı yazımda yeni `askida` alanına taşınıyor. `askida` DEVAM sayımı bitince ya da tur bitince siliniyor. Süreç bu arada ölürse açılışta bir kez ekleniyor.
- **(7) Kayıt sınırları:** jeton ve bekleyen için üst sınır 1e9. İleri ya da bilinmeyen sürüm (`v: 99`) artık bozuk sayılmıyor: bilinen alanlar onarılıyor, bilinmeyen alanlar korunuyor, "Kayıt başka bir sürümden" bildirimi çıkıyor.
- **(8) Olay günlüğü:** `__oyun.olaylar` artık yandan temas, martı, uçurtma gövdesi, ip ve balon patlamasını da içeriyor (`temas`, `ip`, `sondu`). Fizik ve rastgele çekim değişmedi.

## Seyreltme (kullanıcı kararı) ve E3

- Sim'de `ekran_hedef` 7 → 5, `nesne_prim` 2,8 → 3,1; yeni geçit kuralı E3 (`gecit`). JS'e birebir aktarıldı. Ayrıntı: `oyun/sim/RAPOR.md` §7.
- Eşlik (200 tohum) tuttu.
- B0 seyrekleşmesi (`b0_seyrek`) değişmeden hedefte kaldı (30 tohum): iyi botta 5–15. tur medyanı 47 s, tavana çarpan %6,7; orta 31 s / %1,5; hiç 19 s / %0. Ses duvarının ilk kırıldığı tur iyi 3, orta 4, hiç 6.

## Motor sesi (kullanıcı: "uçuşta motor duyulmuyor")

- **Neden (bulgu):**
  - Motor yalnız `motor_ucus_b.mp3` çözüldüyse başlıyordu, sentez yedeği yoktu. Dosya yayında indirilemez ya da çözülemezse uçuş tamamen sessiz kalıyordu. Yayında `ses/` dosyalarının sayfanın yanında yayınlanıp yayınlanmadığı ayrıca doğrulanmalı.
  - Dosya yüklense bile düzey düşüktü: dosya −20 LUFS, motor düzeyi ×0,5 × efekt kazancı (~0,57), müzik ise 0,45. Motor müziğin altında kalıyordu.
  - İlk dokunuş ve AudioContext akışı doğruydu: tur ilk dokunuşu bekliyor, ses o dokunuşla başlıyor.
- **Düzeltme:**
  - mp3 yoksa sentez yedek motor çalıyor (testere 70 Hz + kare 140 Hz + süzülmüş gürültü; perde, filtre ve kazanç hıza göre). mp3 sonradan çözülünce mp3'e geçiyor.
  - Motor düzeyi 0,5 → 0,8, müzik 0,45 → 0,38.
  - `__oyun.sesDurum()` artık `{ac, motorAktif, motorTur, kazanc, perde, yuklu}` döndürüyor.
- **Test:** `test/ses_test.py` iki yolu ölçüyor, ikisi de geçti. Normal yolda motor mp3, engelli yolda sentez; uçuşta aktif ve kazanç > 0, duraklatınca kesiliyor.

## Kalkış açısı seçimi (kullanıcı kararı; ölçüm `oyun/sim/RAPOR.md` §8)

- **Rampa iki faz:**
  - **Açı fazı:** ibre 26°→52°→26° gidip geliyor (tam tur 1,8 s, `B0_ARAYUZ.aci_T`); kesik nişan çizgisi ve "NN°" göstergesi var. Dokunuşla açı kilitleniyor; dokunulmazsa 3 s sonra 38°.
  - **Güç fazı:** eski gösterge. Açı kilidinden sonra 0,25 s dokunuş kilidi var (`rampa_kilit`, çift dokunuş koruması).
  - Uçuşta tek dokunuş değişmedi.
- İlk kez açılışta ipucu "Önce açıyı seç, sonra gücü"; güç fazında "Yeşilde dokun". Kayda `ipucu.aci` eklendi.
- **Sayılar sim'den:** `aci_aralik`, `aci_hiz_k` 0,07, `aci_oto`, `aci_opt`, `BOTLAR[*].aci_sapma/aci_t`, `SABIT_EK.tohum_aci`.
- **Kalkış hızı:** × (1 + 0,07·(38 − açı)/26). Alçak açı biraz hızlı ama alçakta kalıyor; yüksek açı irtifa ve zeplin getiriyor. En iyi açı tur 1'de ~28°, geliştirmeyle ortaya kayıyor; ≥ 3 açılık plato var.
- **Test kancaları:**
  - `?aci=<derece>` açı fazını atlıyor.
  - `__oyun.tur(seed, sv, bot, tur, {aci: sayı | 'bot'})`. Açı verilmezse 38° kullanılıyor; sim eşliği ve kabul.py böylece bozulmuyor.
  - Görüntülü bot açıyı kendisi seçiyor (`aci_karar`).
  - `durum()` içinde `rampa_faz` ve `aci` alanları var; `t` rampada açı + güç fazı süresi.
- **Eşlik (200 tohum, `aci='bot'`, orta ve iyi):** süre, mesafe, en yüksek hız, kazanç ve açı ortalaması geçti (fark %0,3–4,1).
- **Tur süresine etkisi:** insan için +1–3 s (açı fazı).

## Kalkış boş bölgesi (kullanıcı: "fırlatılır fırlatılmaz engellere çarpıyor"; ölçüm `oyun/sim/RAPOR.md` §9)

- **Kurallar** (sim ve oyunda birebir; rastgele çekim sırası aynı):
  - Kalkıştan sonra x < 90 bölgesinde rokete değebilecek hiçbir nesne doğmuyor (`baslangic_bos_x`), yakıt dronu dahil. "İlk ekran temiz": nesneler o bölgede hiç görünmüyor.
  - Açılış zeplini bölgenin hemen ötesinde, rota üstünde. İlk sekme hic botunda ~1,8 s.
  - Tur 1–3'te x < 400'de martı ve uçurtma yok (`yavaslatici_ac_x`, `yavaslatici_tur`).
- **Bölge neden 90:** önerilen 150–200 K1'i bozuyor. Hic botunun 3 s'lik otomatik rampası yüzünden ilk sekme 2 s içinde olmalı; 100'de hic botunda vay ≤ 5 s oranı %1, 150 ve üstünde %0.
- **Hız ölçütü (`baslangic_bos_v`) yok:** roket kalkıştan sonra hızlanmıyor, ölçüt tanımsız.
- **Test:** `test/bos_bolge_test.py`. 5 bot × 100 tohum × (tur 1, tur 1 açılı, tur 3) koşuldu; x < 90'da çarpışma 0, x < 400'de yavaşlatıcı teması 0. 15/15 geçti.
- **Test kancası:** `sonuc` artık `ilk_temas_x` ve `erken_yv` alanlarını da veriyor (yalnız JS).
- **Eşlik:**
  - 200 tohumda 36/37 geçti. Kalan tek ölçü orta botun mükemmel sekme sayısı: JS 0,69, sim 0,82.
  - 800 tohumda ikisi aynı çıktı (0,72 / 0,74; tohum 200–800 arası 0,73 / 0,71). Yani ilk 200 tohumda sim tarafında örneklem sapması; port farkı değil.
- **Menü arkası çizim:** kara kutu ve hangarda sahne artık bir kez çiziliyor (pil ve menü tepkisi için; boyut değişince yeniden çiziliyor).
- **K7 notu:** oyun içinde TEKRAR UÇ'tan RAMPA'ya geçiş 1,7 ms. Playwright ölçümü 0,26–0,68 s arasında oynuyor. Sebep makinedeki yük: başka bir ajanın Blender süreci %300 CPU kullanıyordu, yük ortalaması 5, 4 çekirdek. Yük düşükken önceki koşularda 0,24–0,48 s ölçülmüştü.

## Büyük tur (kullanıcı kararları; KARARLAR'a işlenmek üzere). Sim ayrıntısı: `oyun/sim/RAPOR.md` §10

- **Kalkış boş bölgesi:** max(120, kalkış vx × 2,6 s). İlk temas kalkıştan ~2,7 s sonra; bölgede hiçbir şey yok (açılış zeplini, fırsat, akım dahil). Tur 1–3'te x < 600'de yavaşlatıcı yok. Tur 1'de ilk 5 nesne ≥ 1,5 ekran aralıklı.
- **K1 gevşetildi:** vay kalkış anından ≤ 6,5 s (rampa beklemesi sayılmaz). `test/k1_gevsek.py`: hic ve iyi %100.
  - `testci/kabul.py` K1 eski eşikle (rampa dahil ≤ 5 s) hic botunda %0 veriyor; beklenen bir sonuç. Testçinin K1'i yeni tanıma çekmesi gerekiyor.
- **Uçurtma:** gövde −%8. İp yavaşlatmıyor; kopuyor, uçurtma kuyruğu dalgalanarak yukarı süzülüyor, "İP KOPTU +N" yazısı ve sentez kopma sesi (`SES.ip_kopma`) var. Ödül 16 tabanı. Martı −%3, afiş −%25.
  - "İp kesici" geliştirmesi B0 kart listesinde yok. Sim'deki `ip` kartı artık anlamsız (ip kaybı 0); hangardan çıkarılması için karar gerekiyor.
- **Yönlendirme + yakıt:**
  - Uçuşta basılı tutup sürüklemek burnu çeviriyor; 100 px dikey = tam sınır açısı.
  - Hızlı dokunuş (< 180 ms, < 10 px) dalış ya da itiş. Uçuşta karar parmak kalkınca veriliyor, dalış gecikmesi en çok 180 ms. Rampa dokunuşları eskisi gibi anında.
  - Dalış düğmesinin solunda turkuaz yakıt çubuğu; boşalınca kırmızı, "YAKIT BİTTİ" ya da "YAKIT YOK" çıkıyor.
  - Yeni kartlar: Yakıt deposu, Yönlendirme gücü, Hava akımı. Toplam 9 kart oldu, 3 sütun. İstenen "8 kart" ile "Hava akımı kartı" çelişiyordu; ikisi de konduğu için 9.
- **İtiş (boş dalış yerine):** hedefsiz hızlı dokunuş = 0,3 s ileri-yukarı itiş. En çok +30° (mutlak ≤ 60°), |v| en çok +%8 (≤ 150), 20 yakıt, en çok 2/s. Alev uzuyor, kısa tutuşma sesi var.
- **Hava akımları:** termal sütun (titreşen; bazıları leylekli, görsel) ve jet şeridi (çizgili). Satın almadan doğal (nadir/zayıf). Hava akımı kartı sıklık ve güç ekliyor.
- **Nesneler:**
  - Reklam balonu yuvarlak turuncu; sıcak hava balonu iri kırmızı-beyaz damla.
  - Yük dronu, balina zeplin, paraşütlü kargo kutusu (tur 5), afiş uçağı (tur 4).
  - Parti balonu ve radyosonde kaldırıldı. "Bulut sıçrama pedi" eklenmedi (yalnız gerekirse istenmişti).
- **Trambolin yalnız üstten:** alttan ve yandan içinden geçiliyor (nesne hafifçe titriyor, roket etkilenmiyor).
- **Yay sekmesi** (mantık kuralı 1'in bilinçli istisnası): |v'| = v·k + b·(1 − v/200). Enerjinin görünür sebebi: "BOING ×1,1" yazısı, nesne ezilip geri fırlıyor, hız göstergesi kısa parlıyor.
- **Çeşitlilik ve ritim:** aile kuralları, aynı tür aralığı, küme ve nefes boşluğu (ayrıntı RAPOR §10). Ekranda ortalama ~2 nesne.
- **Doğrulama:**
  - Eşlik 37/37; tur 10'da tüm türlerle de tuttu.
  - `kabul.py --hizli`: K1 (eski eşik) dışında geçme şartlıların hepsi geçti. K7 0,30 s; yük yüksekken (load 5) bile geçti.
  - K5: iyi 2, orta 2, hic 7. K6 (B0): iyi 34 s, tavana çarpan %0.
  - Diğer testler: mantik_test 10/10, bos_bolge 15/15, ses_test, k15_genis 9/9, k1_gevsek, yeni `test/yon_test.py` (sürükleme açıyı 18°→36° çeviriyor, yakıt harcanıyor; hızlı dokunuş itiş yapıyor), insan.py konsol temiz.
- **Hata düzeltmesi:** insan yönlendirme hedefi ilk turda tanımsız kalıp konumu NaN yapıyordu (kayıtta jeton `null` oluyordu). Düzeltildi; ayrıca kara kutu toplamına sayı değilse 0 koruması kondu.
- **Açık:**
  - Sim kampanyasında iyi botun tavana çarpan payı %23 (B0'da %0). Yüksek bant sınırı kararı gerekiyor.
  - Hic botunun erken kazancı ~%18 düştü.
