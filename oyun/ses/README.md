# Ses adayları: nasıl dinlenir, nasıl seçilir

1. `oyun/ses/secici.html` dosyasını telefonda aç (dosya olarak da çalışır; internet gerekmez). Sesin gelmesi için ekrana bir kez dokun; telefon sessizdeyse zil anahtarını aç.
2. **Sesler** sekmesinde her ses için turuncu ▶ ile adayları dinle (ya da "Hepsini sırayla çal"). Beğendiğine **Bunu seç** de, 1–5 puan ver, istersen not yaz. Yeşil "ölçüm önerisi" rozeti yalnız ölçüme dayanır, zevke değil.
3. Müzikte "Yavaş / Hızlı / Çok hızlı" düğmeleri katmanları açar (oyunda hız arttıkça böyle eklenir). Motor uçuşunda ▶ hızlanan bir demo çalar.
4. **Oyun simülasyonu** sekmesinde hız kaydırıcısını oynat, olay düğmelerine bas ya da "Örnek tur"u dinle: seçtiğin sesler birlikte nasıl duruyor, burada anlaşılır.
5. Bitince alttaki **Sonucu kopyala** ile JSON'u kopyalayıp yöneticiye yapıştır. Seçimler bu telefonda saklanır; sayfayı kapatıp sonra devam edebilirsin.

## Öne çıkardıklarım ve nedeni

Ben sesleri duyamıyorum. Öneriler ölçüme (telefon hoparlöründe ne kadar kaybolduğu, hedef yüksekliğe ulaşıp ulaşmadığı, tizlik, süre, atak) ve tasarım niyetine dayanır. Puanlar birbirine çok yakınsa (1–2 puan) fark anlamsızdır, kulağın karar versin. Ayrıntılı tablo: `OLCUM.md`. Spektrogramlar: `spektrogram/`.

| Ses | Benim önerim | Neden |
|---|---|---|
| Motor tutuşma | **C Turbo şarj + ateşleme** (yedek: E Pıt-pıt-VRUUM) | Ölçümde 1. Rampa göstergesi dolarken yükselen ıslık "şarj" hissi verir; E en komik olanı. |
| Motor uçuş döngüsü | **B Çizgi film jet ıslığı** (yedek: C Derin çatırtılı) | Telefon kaybı 0,3 dB, en iyisi. Islık tonu sayesinde hız arttıkça perdenin yükseldiği telefonda da duyulur. C ölçümde 0,1 puan önde ama alçak sesleri telefonda daha çok kaybolur. |
| Trambolin | **F Telefon dostu tiz boing** | Ölçüm a–e boing'lerinin telefonda 6–15 dB kaybolduğunu gösterdi; F bunun üzerine bir oktav yukarı yeniden yapıldı (kayıp 2,9 dB). Kombo perde artışı simülasyonda dinlenebilir. |
| Martı | **C Kenney yumruk + kumaş kanat** (yedek: D Çift çığlık) | Ölçümde 1.; gerçek kayıt vuruşu ve sentez çığlık karışımı. |
| Balon | **D Büyük reklam balonu** (yedek: C hava kaçışı) | Ölçümde 1. İlk sürümü fazla uzundu, kısaltıldı. |
| Kademe ayrılma | **E Yay fırlatma** | Ölçümde 1. "Üst kademe yeniden fırlar" kuralını sesle anlatıyor: klank, yay ve yukarı vuuş. |
| Dalış | **B Vuuş + tok vuruş** | Ölçümde 1. Dengeli: hava süpürmesi tam vuruş anında biter. |
| Mükemmel sekme | **B Arpej + parıltı + boing** veya **C FM çan** | Puanları eşit. B daha "aferin", C daha parlak. |
| Ses duvarı | **B N-dalga çift çatlak** (sinematik isteniyorsa C Emme + BUM) | Gerçek ses patlaması gibi iki çatlak, telefonda kayıp 1,7 dB. Şartnamedeki 60 Hz'lik "BUM" telefonda 15 dB kaybolduğu için elendi. |
| Jeton | **D Parıltılı iki çan** (yedek: A İki nota) | Yumuşak ve tiz değil, çok tekrar edilince yormaz. Zincirde perde gamla yükselir. |
| Arayüz tık | **A Yumuşak pop** | Puanlar eşit; parlak yuvarlak arayüze en uygun olanı. |
| Kart satın alma | **B Arpej + jeton yağmuru** | Ölçümde 1. Ödül hissi en güçlü olanı. |
| Son şans | **C Siren + kalp atışı** (yedek: A İki ton alarm) | Ölçümde 1. Gerilim veriyor; A daha net ama sıradan. |
| Müzik | **C Çizgi film galopu** veya **A Roket sörfü** | İkisi de ölçümde 100 puan. C en klasik çizgi film, A daha "roket". B (çiptün) ve D (ska) alçak bölgede telefonda biraz daha zayıf. |

**Şartnameye not:** TASARIM §14'teki basit tariflerin (sinüs boing, 60 ms pof, 200 ms ding, 60 Hz BUM, pat + gümbürtü) çoğu ölçümde elendi: telefonda kayboluyor, çok kısa ya da çok sivri. Adaylarda hepsinin "telefonda duyulan" sürümleri var.

## Teknik

- Yeniden üretmek: `python3 oyun/ses/uret.py && python3 oyun/ses/olc.py` (~1,5 dk). Ara wav'lar `_ara/` içinde (git dışı).
- Ses düzeyleri: kategori hedefleri `uret.py` içindeki `KATEGORI[...]['hedef']` (LUFS). Simülasyonda efekt, müzik ve motor kaydırıcıları ayrı.
- Döngüler (motor, müzik) başta ve sonda 0,5 s pay içerir. Oyunda `loopStart`/`loopEnd` değerleri `adaylar/liste.js` içindeki `dongu` alanından alınmalı (mp3 kodlayıcı gecikmesi olsa bile ek duyulmaz).
- Motor eşlemesi (oyunda da aynısı): oynatma hızı 0,7 + 0,9·s, alçak geçiren 1200·2^(2,5·s) Hz, kazanç 0,55 + 0,45·s; s = hız / 300. Müzik: 2. katman s 0,25–0,40, 3. katman s 0,55–0,70 arasında açılır.
- `adaylar/gomulu.js`, sayfa dosya olarak (`file://`) açılınca kullanılır. Sayfa sunucudan açılacaksa bu dosya silinebilir.
