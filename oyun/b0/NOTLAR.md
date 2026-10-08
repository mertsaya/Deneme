# B0 uygulama notları (uygulayıcı, 2026-10-08)

Kaynaklar: `TASARIM.md` (şartname), `oyun/KARARLAR.md`, `oyun/sim/ucus_sim.py`, koordinatör yayın notu.

## Sorulacak (kullanıcı / tasarımcı kararı gerekiyor)

1. **"Seni durduran" metinleri.** §20 K-C "§11 anahtarlarındaki mevcut metinler" diyor ama §11'de metin yok, yalnız anahtarlar var. Öğretici tonda **yer tutucu** metinler yazdım (`index.html` → `METIN['durduran.*']`). Onay ya da yeni metin gerekiyor.
2. **Bitiş sahnesinin ne zaman abartılı olacağı.** KARARLAR: "rekor / büyük kayıpta abartılı". TASARIM §20: "`yer`'de abartılı, `durma`/`sure`'de sakin". İkisi farklı. Şimdilik ikisinin birleşimi: bitiş `yer` **ya da** mesafe rekoru → abartılı, öbürleri sakin. "Büyük kayıp" tanımlanmamış.
3. **Elle bitirilen turda kara kutu.** §9/§11'e göre kara kutuda prim ve taban "—" görünmeli; ama §13.3'te YENİDEN BAŞLA ile HANGAR'ın kara kutu gösterip göstermediği yazmıyor. Şimdilik kara kutu yok: YENİDEN BAŞLA doğrudan RAMPA'ya, HANGAR doğrudan hangara gidiyor, kazanç "Yarım uçuş: +X jeton" bildirimiyle gösteriliyor. `—` satırları kodda hazır.
4. **Denge (bilgi; testçi `kabul.py --hizli` ölçtü, geçme şartı değil).** K5: ses duvarının ilk kırıldığı tur medyanı iyi bot için 4 (hedef 2–3). K6: iyi bot tur 5–15'te medyan 60 s ve turların %48'i 65 s tavanına çarpıyor (hedef 20–40 s, ≤ %5). Sebep büyük olasılıkla şu: B0'da ısı ve üst bantlar yok, dalış gücü/verim ucuz geliyor. Sim ayarı (S1–S9) bitince yeniden ölçülmeli; gerekirse B0'a özel kart tavanı (rampa gibi) konabilir.

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
