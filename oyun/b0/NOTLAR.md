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
3. **K6 sapması B0 kapsamından geliyor (karar gerekiyor).** Ayrıntı aşağıda.

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
