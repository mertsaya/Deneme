# Araç ve eklenti araştırması: Son Durak: Plüton

Tarih: 2026-10-08. Yöntem: WebSearch/WebFetch, `SearchPlugins` (claude.ai "Anthropic Directory" kataloğu), `SearchSkills`/`ListPlugins`. **Hiçbir şey kurulmadı**, kurulum kartı gösterilmedi.

**Güven notu.** Her satırdaki kaynak, bakılan yerdir. "(bilgi)" işareti, bu oturumda doğrulanmamış genel bilgi demektir. Arama motoru yalnızca özet verdi; aşağıdaki depoların kendi sayfalarını çoğunlukla açmadım (aşağıda "Erişilemeyen/doğrulanamayan"). Topluluk eklentilerinin içeriği bana yalnızca katalog açıklamasından göründü, kodunu okumadım: kurmadan önce okunmalı.

Projede zaten olanlar (tekrar önerilmedi): Playwright (Python) + Chromium + `oyun/b0/testci/` botları ve `kabul.py`; `oyun/sim/ucus_sim.py` + `/denge` komutu; gltf-transform, adb, KTX-Software (indirildi, kurulmadı); `oyun/ses/olc.py` (LUFS/BS.1770, spektrogram, telefon hoparlörü benzetimi, eleme kuralları); Kenney CC0 sesleri; 7 alt ajan (`.claude/agents/`, `mantik-denetcisi` dahil); bulutta `ffmpeg`, Node 22, Python (numpy, scipy, soundfile, playwright 1.63) kurulu.

---

## Şimdi kurulacak 5 şey

| # | Ne | Neden bu proje için | Nerede | Maliyet |
|---|---|---|---|---|
| 1 | **`/code-review`** (Claude Code yerleşik; kurulum yok) ve kilometre taşlarında **`/code-review ultra`** | B0 kodunu (tek dosya `index.html`, sim ile eşlik) mantık hatasına karşı tarar. Yerel sürüm ücretsiz (normal kullanım); `ultra` bulutta çok ajanlı, her bulguyu yeniden üretip doğrular | Bulut oturumu da olur, PC de | Yerel: normal kullanım. Ultra: Pro/Max'te 3 ücretsiz, sonra kullanım kredisi (belgede $5–25/inceleme) |
| 2 | **cloudflared hızlı tünel** (`cloudflared tunnel --url http://localhost:8765`) | Telefonda "dosyayı kaydet, yayınla, bekle" döngüsünü kaldırır: PC'deki yerel sunucuyu telefona HTTPS adresi olarak açar | PC | Ücretsiz, hesap gerekmez. Risk: tünel açıkken yerel sunucu internete açık (oyunda gizli uç yok, sorun değil) |
| 3 | **ccusage** (`npx ccusage daily`) | 100 $ bulut kredisi ve oturum limiti için hangi ajan/model ne yakıyor görmek. Yerel JSONL günlüklerini okur, model başına döküm verir | PC (günlükler orada). Bulut oturum günlüğü bulut kabında kalır | Ücretsiz, açık kaynak, günlük dışarı gitmez (bilgi: yerel okur) |
| 4 | **Playwright'ta kare-süresi ölçümü + piksel farkı testi** (yeni araç değil, `testci/`ya iki betik) | Gerçek telefon yokken: oyun içi `requestAnimationFrame` kare süresi histogramı (p95/p99) ve tohumlu sahnede ekran görüntüsü farkı. Oyunda `__oyun` kancaları ve `?sv=` tohum zaten var | Bulut | Ücretsiz |
| 5 | **Sprite paketleyici: `free-tex-packer-cli` ya da 60 satırlık Pillow betiği** | B1'de Blender'dan çıkan kareleri tek atlas PNG + JSON yapar. Canvas2D için KTX2 işe yaramaz, atlas gerekir (aşağıda) | Bulut veya PC | MIT |

"Şimdi" dışında kalıp B1'de gelecekler ve elenenler aşağıdaki tablolarda.

---

## 1. Mantık / kod denetimi

**"ClaudeDevs X'te paylaşılan, mantık hatası bulan ajan" için bulabildiğim:** X'teki gönderinin kendisine erişemedim (WebSearch yalnızca web sayfalarını döndürdü). Tarife uyan resmî özellikler iki tane: (a) **Code Review** (GitHub PR'larına satır içi yorum yapan çok ajanlı yönetilen hizmet) ve (b) **ultrareview** (`/code-review ultra`). İkisini de Anthropic belgesinde doğruladım: https://code.claude.com/docs/en/code-review ve https://code.claude.com/docs/en/ultrareview. Hangisinin paylaşıldığını kesin söyleyemem.

| Ad | Ne işe yarar (bu projede) | Zorluk | Nerede | Maliyet / lisans / gizlilik | Öncelik |
|---|---|---|---|---|---|
| **`/code-review`** (yerleşik; `/review` takma adı) | Dal farkı veya `oyun/b0/index.html` + `sim/ucus_sim.py` farkı için arka plan alt ajanıyla doğruluk hataları; `--fix` uygular, `--comment` PR'a yazar, `low`…`max` çaba düzeyi. Örnek: JS portu ile sim arasındaki sapmalar. Not: `REVIEW.md` okumaz, `CLAUDE.md`yi okur | Kolay | İkisi | Normal kullanım sayılır. Kod Anthropic'e gider (zaten gidiyor) | **Şimdi** |
| **`/code-review ultra`** / `claude ultrareview` | Buluttaki ajan filosu, her bulguyu bağımsız yeniden üretir; 5–10 dk. Kilometre taşı öncesi (B0 teslim, B1 sonu, mağaza öncesi) | Kolay | Claude.ai girişi gerek | Pro/Max: tek seferlik 3 ücretsiz, sonra $5–25 (belge). Kredi bakiyesi yoksa başlamaz. Bedrock/Vertex/ZDR'de yok. Fark limiti: 500 dosya / 8000 satır | **Şimdi** (B0 teslimi için 1 kez) |
| **Yönetilen Code Review (GitHub App)** | PR başına otomatik çok ajanlı inceleme, `REVIEW.md` ile ayarlanır | Orta | GitHub + yönetici ayarı | **Yalnızca Team/Enterprise** (belge); inceleme başı ort. $15–25. Kişisel hesapta büyük olasılıkla yok | Gerek yok |
| Resmî eklenti **code-review** (`anthropics/claude-plugins-official`, `plugins/code-review`) | PR için çok ajanlı, güven puanlı inceleme (katalog: "multiple specialized agents with confidence-based scoring"). Yerleşik komutla büyük ölçüde örtüşüyor | Kolay | İkisi | Anthropic imzalı; ağ gerek: `gh` ile PR | Gerek yok (yerleşik var) |
| **security-review** (yerleşik beceri; bu oturumda listede) | Bekleyen değişikliklerin güvenlik taraması. Oyun sunucusuz; telemetri/PWA gelince anlamlı | Kolay | İkisi | Normal kullanım | Sonra |
| **code-review-harness** (topluluk, "Generator-Evaluator", kodu gerçekten çalıştırır) | "Kodu okuyarak bulunmayan" hataları çalıştırarak arar; bizde zaten sim + botlar bunu yapıyor | Orta | Bulut | Topluluk, v1.0.0, hiç denetlenmedi | Gerek yok (kendi `kabul.py`'miz var) |
| **claude-code-review-council** (topluluk, 6 uzman ajan) | Doğruluk, test kanıtı, mimari, arayüz uzmanları; `PreToolUse` kancası ve "privileged" erişim var | Orta | Bulut | Topluluk. Kancalar yetkili: kurmadan önce okunmalı | Gerek yok |
| **finecomb** (topluluk, denetim listesi) | Dil/özellik başına çok uzun kontrol listesi, salt-okunur | Kolay | İkisi | Topluluk | Gerek yok |
| Kendi `mantik-denetcisi` / `denetci` ajanları | Zaten var; oyuna özel (KARARLAR, sim eşliği) bilgiyi taşıyor | — | — | — | Mevcut, öncelik bunlarda |

**Öneri:** yerleşik `/code-review high` ile `denetci`'yi birbirine alternatif değil tamamlayıcı kullan: yerleşik genel hata arar, `denetci` şartname ve oyun kurallarına uyumu denetler.

---

## 2. Oyun testi

| Ad | Ne işe yarar | Zorluk | Nerede | Maliyet / risk | Öncelik |
|---|---|---|---|---|---|
| **Playwright** (mevcut) + CDP | Bot turları, `__oyun` kancaları. Playwright belgesi: `toHaveScreenshot` kararlılık bekler, animasyonları kapatır; canvas oyunlarında asıl sorun determinizm (tohum, sabit görünüm). Bizde `?sv=` tohum var (NOTLAR) | Kolay | Bulut | Ücretsiz. Görüntü farkı tabanları aynı ortamda üretilmeli (tarayıcı sürümünü sabitle) | **Şimdi** |
| Kare-süresi ölçümü (kendi betiğimiz) | Sayfada rAF aralıklarını topla (p50/p95/p99, 33 ms üstü kare sayısı). `Performance.getMetrics` kare süresi vermez (kaynak: CDP belgesi özeti), iz (trace) gerek ya da sayfa içi sayaç; sayaç daha basit | Kolay | Bulut | Ücretsiz. Dikkat: bulutta yazılım çizimi, telefonla karşılaştırılamaz; yalnız **göreli** gerileme yakalar | **Şimdi** |
| CPU kısma (CDP `Emulation.setCPUThrottlingRate`) (bilgi, doğrulanmadı) | Düşük seviye telefonu kabaca benzetmek için 4x yavaşlatma | Kolay | Bulut | Ücretsiz | B1'de |
| **`@playwright/mcp`** (Microsoft; katalogda "playwright", iş ortağı) | Claude'un sayfayı etkileşimli gezmesi; `--device="iPhone 15"` gibi cihaz kalıbı (kaynak: playwright.dev/agents/browser-and-emulation). Bizde betik zaten var; MCP yalnız keşif için | Kolay | Bulut | Ücretsiz. Bağlam harcar | Gerek yok (şimdilik) |
| **Gerçek telefon, Playwright `_android`** | Playwright belgesi: Android Chrome 87+, ADB gerek, "komut satırı" bayrağı açılmalı, ekran uyanık olmalı; **deneysel**. Telefondaki gerçek fps'i betikle ölçer | Orta | PC (adb + USB) | Ücretsiz. Kaynak: https://playwright.dev/docs/api/class-android | B1'de |
| `adb` + `chrome://inspect` (bilgi: `adb forward`/uzaktan hata ayıklama) | Telefonda DevTools Performance kaydı, bellek | Orta | PC | Ücretsiz | B1'de (adb kurulu) |
| **Firebase Test Lab** | Gerçek cihazda betikli test (APK'ya, Robo). Ücretsiz Spark planı günlük sınırlı (kaynaklar uyumsuz: "15 test/gün" gibi); cihaz süresi sınırı var | Orta | Bulut hizmeti (Google hesabı) | APK gerektirir (Capacitor/TWA sonrası). Sayılar belirsiz, siteden doğrula | Sonra |
| **BrowserStack / LambdaTest (TestMu AI)** | Gerçek cihazda elle deneme; ücretsiz dakika çok az (30–100 dk, kaynaklar tutarsız) | Kolay | Bulut hizmeti | Ücretli; kullanıcının telefonu varken gereksiz. Oyun hesabı/veri yok ama oyun adresi 3. tarafa gider | Gerek yok (en fazla 1 kez düşük seviye cihaz bakmak için) |
| **Android Emulator QA Plugin** (topluluk, "privileged") | Emülatörde uygulama başlatma, ekran görüntüsü, günlük | Zor | PC (Android Studio gerek) | Topluluk, v1.0.0 | Sonra (APK çıkınca) |
| **Oh My Android** (topluluk) | Yalnız **macOS** uygulaması (`brew`); kullanıcı Windows | — | — | — | Gerek yok |
| **parallax-threejs** (topluluk) | Aşağıda, bölüm 5 | | | | |
| **Oyun hissi ölçümü** | Araçla ölçülmez. Ölçülebilenler: dokunuştan tepkiye gecikme (olay zamanı → ilk çizim karesi), kare süresi dalgalanması, sim'deki denge (`/denge`). His için 3–5 kişilik gözlemli telefon testi ve soru formu | — | — | — | Süreç (bölüm 7) |

**Not:** `kabul.py` 404 uyarısı `/__bos__` sayfasından (NOTLAR). `about:blank` kullanmak testçinin işi.

---

## 3. Ses

| Ad | Ne işe yarar | Zorluk | Nerede | Maliyet / risk | Öncelik |
|---|---|---|---|---|---|
| **ffmpeg `ebur128` / `loudnorm`** | Bağımsız LUFS/LRA/gerçek tepe doğrulaması: `ffmpeg -i x.mp3 -af ebur128=peak=true -f null -` (kaynak: DCP-o-matic hata kaydı). `olc.py` çıktısını çapraz kontrol eder | Kolay | Bulut (`/usr/bin/ffmpeg` var) | Ücretsiz | **Şimdi** (bir kez, `olc.py` ile karşılaştır) |
| `ffmpeg showspectrumpic` | Spektrogram PNG (bilgi; `ffmpeg` belgesi açılmadı). `spektrogram/` klasörünüz zaten var | Kolay | Bulut | Ücretsiz | Gerek yok |
| **pyloudnorm** (bilgi) | BS.1770 ölçümü Python'da. `olc.py` kendi K-ağırlıklı ölçüsünü yapıyor | Kolay | Bulut | MIT (bilgi) | Gerek yok |
| **Kenney** (CC0) | Zaten kullanılıyor. Atıf zorunlu değil; Kenney logosu yasak (kaynak: https://gtstu.com/?p=5011, ikincil) | — | — | CC0 | Mevcut |
| **OpenGameArt** | Eser başına lisans etiketi; CC0 olanları seç | Kolay | — | Eser başına kontrol | Gerekirse |
| **Freesound** | Lisans **klip başına** (CC0/CC-BY/NC). CC0 süzgeci şart; kayıt tutun (`LISANSLAR.md` biçimi iyi) | Kolay | — | Her klipte lisans sayfasına bak | Gerekirse |
| **Freesound MCP** (`timjrobinson/FreesoundMCPServer`, topluluk; Glama listesi) | Claude'un Freesound'da aramasını sağlar; Freesound API anahtarı ve Node 16+ gerek | Orta | Bulut (anahtar = gizli) | Ücretsiz API; anahtar gizli tutulmalı. Hâlâ bakımlı mı bilmiyorum | Sonra (gerekirse) |
| **jsfxr / ZzFX / sfxr** (bilgi) | Hızlı yapısal efekt. Bizde `ses_lib.py` zaten kodla üretiyor | Kolay | — | ZzFX MIT sanılıyor, **doğrulanmadı** | Gerek yok |
| **audiorective** (topluluk; katalog: "Web Audio toolkit for coding agents", 2 beceri, three.js/PlayCanvas bağlamaları) | Çalışma zamanı ses motoru (hızla perde yükselen motor, katman müziği) yazarken Claude'a Web Audio kalıbı öğretir. Şu an sesler hazır dosya (MP3) çalıyor; sentez değil | Kolay | Bulut | Topluluk v2.4.0, yalnız Markdown beceri (kod yok gibi, kontrol et) | B1'de (ses motoru yazılırken), düşük |
| **mcp-music-analysis** (`hugohow`, librosa; son güncelleme Nis 2025 — AIBase özeti) | Tempo/onset analizi. Oyun SFX'i için gereksiz | Orta | — | Eski | Gerek yok |
| **AudioPod** eklentisi (topluluk, uzak hizmet) | Gürültü temizleme, stem ayırma, dönüştürme | Orta | Uzak hizmet | **Ses dosyaları üçüncü tarafa yüklenir**; hesap/ücret belirsiz | Gerek yok |

---

## 4. Görsel

| Ad | Ne işe yarar | Zorluk | Nerede | Maliyet / risk | Öncelik |
|---|---|---|---|---|---|
| **Blender MCP** (`ahujasid/blender-mcp`) | Blender'ı Claude'dan canlı yönetmek: Python çalıştırma, sahne kurma, Poly Haven/Sketchfab/Hyper3D bağlantıları (kaynak: dizin özetleri). Bizim betikli `-b -P` yöntemi yeniden üretilebilir; MCP, **bakıp düzeltme** döngüsü için iyi (ışık, malzeme ayarı) | Orta | **PC** (Blender 5.2 kurulu; bulutta Blender yok) | MIT (dizin özeti, depoyu açmadım). Blender 5.2 ile uyum **doğrulanmadı**. Eklenti soket üzerinden keyfi Python çalıştırır → yalnız yerelde, güvenilir istemciyle | B1'de (görsel sanatçı işi) |
| Blender başsız betik (mevcut yöntem) | Sprite/kare render + glTF dışa aktarma (`--background … --python`). Kaynak: TIL notu, ClawKit. Tekrarlanabilir ve bulutta/CI'da koşar | Kolay | PC (Blender gerek) | — | Mevcut, ana yol |
| `coreway-labs/blender-sprite-render` | Çok yönlü sprite render + otomatik kırpma + 2'nin kuvveti dolgu (depo özeti). Bizim görüntü yönümüz (boyalı plastik, abartılı ölçek) için kendi betiğimiz daha kontrollü | Kolay | PC | Lisansı bilmiyorum | Gerek yok (örnek olarak bak) |
| **free-tex-packer-cli** (npm, `odrick`, MIT, v0.3.0 — jsDelivr) | Klasör → atlas PNG + JSON | Kolay | İkisi (Node) | MIT. Bakımı belirsiz (son güncellemeyi görmedim) | **Şimdi/B1** |
| **FastPack** (CLI, Phaser/Pixi biçimleri, döndürme — mintlify özeti) | Aynı iş; CI için | Orta | İkisi | Lisans bilinmiyor | B1'de (yedek) |
| **yatp-cli** (Rust, MIT — lib.rs) | Basit atlas | Orta | PC | MIT | Gerek yok |
| **TexturePacker** | Ücretli referans araç | — | — | Ücretli | Gerek yok |
| 60 satırlık Pillow/MaxRects betiği | Sıfır bağımlılık, kendi JSON biçimin | Kolay | Bulut | — | **B1'de** (eşit seçenek) |
| **KTX2 / Basis** (gltf-transform `etc1s`/`uastc`; Khronos) | Yalnızca **Three.js 3D doku** için GPU sıkıştırma (kaynak: Babylon forumu: ETC1S renk dokuları, UASTC normal/veri). **B0 Canvas2D'de işe yaramaz**: `drawImage` çözülmüş bitmap ister. B1 Three.js olursa gündeme gelir | Orta | PC (`toktx` yönetici onayı ister) | Ücretsiz | Yalnız Three.js seçilirse |
| **Canva MCP** (bu oturumda var: `generate-image`, `remove-background`, `separate-image-layers`, `resize-design`, `export-design`, marka kiti, şablon…) | Tutarlı **oyun içi sprite** için uygun değil (sanat yönü kontrolü zayıf, her çıktı farklı). Uygun olan: Play Store görselleri (512 ikon, 1024x500 öne çıkan grafik), itch.io kapağı, ekran görüntüsü çerçeveleri, arka plan kaldırma (kaba tasarım taslağından). Not: araçların adlarını gördüm; çıktı kalitesini ve ticari kullanım koşullarını **denemedim/okumadım** | Kolay | Bulut (bağlı) | Canva hesap koşulları geçerli; üretilen görsellerin lisansını Canva şartlarından kontrol et | Sonra (yayın görselleri) |
| **Unsplash MCP** (bu oturumda var) | Fotoğraf arama; çizgi film oyunu için yararsız | — | — | — | Gerek yok |
| **SpriteCook** eklentisi (topluluk, uzak hizmet; sprite/UI kiti/doku/animasyon üretimi) | Piksel/tile ağırlıklı görünüyor; bizim "boyalı plastik" yön için belirsiz. Fiyat ve lisans bilmiyorum | Orta | Uzak hizmet | Ücretli olabilir; istemler dışarı gider | Gerek yok (şimdilik) |
| **Clipwave** (AI video/görsel, topluluk) | Tanıtım videosu; kontrol zayıf | — | Uzak | Hesap/ücret | Gerek yok |

---

## 5. Three.js / oyun geliştirme eklentileri

**Önkoşul:** B0 Canvas2D ve tek dosya. B1'in motoru henüz kararlaştırılmadı. Aşağıdakiler yalnız **Three.js'e geçilirse** değer taşır.

| Ad | Ne işe yarar | Zorluk | Nerede | Maliyet / risk | Öncelik |
|---|---|---|---|---|---|
| **parallax-threejs** (topluluk, v0.4.12; katalog: "Three.js/GLSL debugging… SHA-indexed visual regression"; içerir: chrome-devtools-mcp, playwright-mcp, spector, threejs-devtools-mcp, komutlar `checkpoint/diff/replay/sweep/ship-check/memcheck`, ajanlar `visual-debugger/shader-reviewer`, `PostToolUse` kancası) | Shader ve GL durumu hata ayıklama, piksel tabanlı görsel gerileme. Canvas2D'de gereksiz | Orta | Bulut | Topluluk; 4 MCP sunucusu + kanca → "remote" erişim. Kurmadan önce `plugin.json` ve kancayı oku | Yalnız Three.js seçilirse (B1) |
| **threejs-game-skills** (`majidmanzarpour`, MIT; 9 beceri: yönetmen, oynanış, grafik, arayüz, hata ayıklama/profil, QA/yayın, 3D/görsel/ses üretimi; Vite+TS iskeleti, Playwright şablonları, **tohumlu RNG ve test kancaları**) | Fikir olarak bizim yapıya çok yakın (tohum, test kancası). Ama kendi iskeletini dayatır; KARARLAR.md ile çatışabilir | Orta | Bulut | MIT. Üretim araçları Tripo/Gemini/ElevenLabs (ücretli anahtar, isteğe bağlı). `npx skills add …` komutu kendi sürecini kurar | Yalnız Three.js seçilirse; yoksa gerek yok |
| **cloudai-x/threejs-skills**, **kndoshn/threejs-skill-plugin** | Three.js bilgi dosyaları (geometri, malzeme, ışık, shader, bellek sızıntısı) | Kolay | Bulut | Topluluk | Yalnız Three.js seçilirse |
| **Unity eklentisi** (Unity Technologies, iş ortağı) | Unity içindir; bizim web oyunu için alakasız | — | — | — | Gerek yok |
| **Meta VR** | VR; alakasız | — | — | — | Gerek yok |

`audiorective`: bölüm 3.

---

## 6. Yayın

| Ad | Ne işe yarar | Zorluk | Nerede | Maliyet / risk | Öncelik |
|---|---|---|---|---|---|
| **Cloudflare Pages** | Ücretsiz HTTPS statik barındırma; sınırsız bant, 500 yapı/ay, dosya 25 MiB, 20k dosya (kaynak: freetier.co özeti, ikincil) | Kolay | Bulut hizmeti | Ücretsiz; şartlar siteden doğrulansın | B1'de (PWA için sabit adres) |
| **GitHub Pages** | En basit; yumuşak sınırlar (100 GB/ay, 1 GB), ticari kullanım kısıtı var (aynı kaynak). Depo zaten GitHub'da | Kolay | Bulut hizmeti | Ticari oyun için şartları oku | Şimdi/B1'de, geçici |
| **Netlify** | Kredi tabanlı ücretsiz, bant en dar | Kolay | Bulut hizmeti | — | Gerek yok |
| **cloudflared hızlı tünel** | Bkz. "şimdi 5" | Kolay | PC | — | **Şimdi** |
| **itch.io + butler** | HTML5 oyunu ZIP veya `butler push klasor kullanici/oyun:kanal`; ikinci itme artımlı. İki ayar gerekir: sayfa türü HTML ve kanal "tarayıcıda oynanır" (kaynak: https://itch.io/docs/butler/pushing, https://itch.io/docs/creators/html5). Bir arkadaş grubuna gizli test sayfası olarak kullanılabilir (bilgi: sayfayı kısıtlı yapma, doğrula) | Kolay | PC (butler indir) | Ücretsiz; komisyon ayarlanabilir (bilgi). Zip köküne `index.html` | B1'de (arkadaş testi) |
| **PWA** (manifest + service worker + ikonlar) | Ana ekrana ekleme, çevrimdışı. HTTPS gerek | Orta | Kodda | — | B1/B2 |
| **Bubblewrap / TWA** (Google; `GoogleChromeLabs/bubblewrap`) | PWA'yı Play için Android paketine çevirir. Gerekenler: canlı HTTPS alan adı, `/.well-known/assetlinks.json`; imza anahtarı uyuşmazlığı en sık hata (kaynak: Chrome belgesi quick-start, Thinktecture) | Orta | PC (JDK + Android SDK) | Ücretsiz. TWA Chrome'da çizer (bilgi) → canvas oyununda daha tutarlı fps beklenir; native API az | B2 (yayın) |
| **Capacitor** | Sistem WebView içinde; Android'de cihaza göre değişken fps raporları var (Capacitor tartışması; ölçülmedi). Gerçek avantaj: reklam, uygulama içi satın alma, titreşim gibi native eklentiler | Orta | PC | Ücretsiz | Gerek olursa; önce TWA dene |
| **pwa2play** (topluluk v0.1.0; "check/package/update" komutları) | PWA→imzalı Play paketi, ret nedenlerini önler | Orta | Bulut/PC | Çok yeni sürüm; imza anahtarını ellemesin, **anahtarı kendin tut** | Sonra, denetleyerek |
| **Play Console kapalı test kuralı** | Kişisel hesap (13 Kas 2023 sonrası açılan): üretim öncesi **12 test kullanıcısı × 14 gün kesintisiz** kapalı test (ikincil kaynaklar: gitconnected, testerscommunity, extendsclass; Google'ın kendi sayfasına bakmadım). Kuruluş hesabı (D-U-N-S) muaf. Bu, "arkadaş testi" ile başlayıp 14 gün öncesinden planlanmalı | — | Play Console | Hesap ücreti (bilgi: tek seferlik 25 $, doğrula) | Planla (B2) |

---

## 7. Ölçüm ve geri bildirim

| Ad | Ne işe yarar | Zorluk | Nerede | Maliyet / gizlilik | Öncelik |
|---|---|---|---|---|---|
| **Yerel olay günlüğü + "Geri bildirimi kopyala" düğmesi** (kendi kodumuz; `secici.html`'deki "Sonucu kopyala" kalıbı) | Tur başına: tur no, mesafe, süre, bitiş nedeni, cihaz/fps. Hiçbir sunucuya gitmez; test eden kişi JSON'u sana yapıştırır. `kayit` şeması zaten var (NOTLAR) | Kolay | Kodda | Sıfır maliyet, sıfır üçüncü taraf, **en düşük gizlilik riski** | **B1'de** (telefon testi başlarken) |
| **Google Form / Drive** (Drive bağlayıcısı bu oturumda var) | Test kullanıcıları için kısa anket ("zevkli miydi, nerede sıkıldın"); Drive'dan yanıtları okutmak. Form oluşturma araçları yok (`create_file`, `read_file_content`… var), yani form elle kurulur | Kolay | Bulut hizmeti | Kişisel veri toplama: ad/e-posta isteme | B1'de |
| **GoatCounter / Plausible** | Çerezsiz sayfa görüntüleme sayacı; Plausible'da özel olay (`track()`), olayın panoda hedef olarak tanımlanması gerek. GoatCounter olayları sınırlı olabilir (kaynaklar çelişiyor) | Kolay | Bulut hizmeti | Plausible ücretli (bilgi), GoatCounter ücretsiz/kişisel (bilgi). Çerezsiz = rıza çubuğu çoğu zaman gerekmiyor (ikincil site iddiası) | Sonra (yayın) |
| **PostHog** | Olay analizi; ücretsiz 1M olay/ay, 1 yıl saklama (resmî fiyat sayfası özeti) | Orta | Bulut hizmeti | **SDK + kullanıcı kimliği** → çocuklara dönük görünen çizgi film oyununda risk | Gerek yok |
| **Google Play Console: Android vitals / ön yayın raporu** (bilgi, doğrulanmadı) | Çökme, ANR, cihaz başına fps raporu | Kolay | Play | Ücretsiz | Yayın sonrası |

**Gizlilik uyarısı.** Oyun renkli çizgi film ve çocuklarca oynanabilir. 3. taraf SDK'ların çocuk uygulamalarında COPPA ihlallerinin ana nedeni olduğunu gösteren bir akademik çalışma buldum (PETS 2018: https://petsymposium.org/popets/2018/popets-2018-0021.php). Güncel COPPA/GDPR-K kuralını **doğrulamadım**; yayın öncesi Play Families politikasını ve KVKK/GDPR metnini hukuk kaynağından kontrol et. Öneri: kimlik yok, çerez yok, 3. taraf SDK yok, ağa veri göndermeyen yerel günlük, test kullanıcısına ne toplandığını açıkça yaz. Reklam/IAP kararı çıkarsa yeniden bakılır.

---

## 8. Süreç: maliyet, kanca/komut, orkestrasyon

| Ad | Ne işe yarar | Zorluk | Nerede | Maliyet / risk | Öncelik |
|---|---|---|---|---|---|
| **ccusage** (`ryoppippi/ccusage`; `npx ccusage daily`, `blocks --live`) | Yerel JSONL günlüklerinden günlük/oturum/model döküm ve 5 saatlik blok izleme; önbellek jetonlarını ayrı sayar | Kolay | PC | Ücretsiz; maliyet **tahmin** (API fiyatı, fatura değil) | **Şimdi** |
| **Claude Code Cost** (topluluk, RoninForge; `/by-day`, `/by-project`…) | Aynı iş, eklenti olarak | Kolay | PC | Topluluk, "privileged" | Gerek yok (ccusage yeter) |
| Resmî maliyet belgesi | `/usage-credits` ile kredi ayarı kontrolü (ultrareview belgesi); maliyet yönetimi: https://code.claude.com/docs/en/costs | Kolay | İkisi | — | Oku |
| **Kendi komutlarımız** (`.claude/commands/`, `/denge` gibi) | Öneri: `/kabul` (`testci/kabul.py` + özet), `/ses-olc` (`olc.py` + elenenler), `/sartname` (TASARIM.md maddelerini kodla karşılaştır), `/fps` (kare süresi betiği), `/oturum-ozeti` (OZET.md'ye 10 satır). Hepsi kısa Markdown dosyası | Kolay | Repo | — | **B1'de**, ihtiyaç doğdukça |
| **`update-config` becerisi** (bu oturumda var) → kanca | Örn. `Stop` kancası ile bitiş öncesi `python ucus_sim.py kontrol`; `PreToolUse` ile `KARARLAR.md`ye yazmayı engelle. Bu mekanizma kullanıcı ayarında; harness çalıştırır, bellek değil | Orta | PC/Repo | Yanlış kanca oturumu kilitleyebilir; önce dar başla | B1'de |
| **`skill-creator`** (bu oturumda var) | Kendi becerimizi (ör. "oyun hissi kontrol listesi", "ses seçici") tasarlayıp sınamak | Orta | Bulut | — | Sonra |
| **Alt ajanlar** (mevcut) | Zaten 7 ajan + CLAUDE.md model yönlendirmesi | — | — | — | Mevcut |
| **Bulut "Routine"** (bu oturumun `create_trigger`/`send_later` araçları) | Önceki gece görevi PC uyuduğu için çalışmadı (OZET 7. oturum). Bulut zamanlanmış oturum PC'ye bağlı değil; gece botu/ölçüm için yeniden denenebilir. **Denemedim** | Orta | Bulut | Kredi harcar; yeni oturum başına standalone talimat gerek | Sonra; önce maliyeti ölç |
| **Session Orchestration** (topluluk; Alpha/Beta/Gamma/Delta/Polish oturumları) | Çok oturum koordinasyonu; bizim yönetici+alt ajan düzeninle örtüşüyor | Orta | — | Topluluk, "privileged" | Gerek yok |
| **claude-cursor-orchestration**, **cmux-ultimate** | Başka araçlar (Cursor/cmux) ister | — | — | — | Gerek yok |
| **GitHub MCP** (bu oturumda var) | PR/sorun/dal işlemleri; push izin sistemince engelli (OZET 8), bunu değiştirmez | Kolay | Bulut | — | Mevcut |

---

## Kurulum sırası önerisi (kısa)

1. Bu hafta: `/code-review high` (B0 farkı), bir `/code-review ultra` (B0 teslim öncesi, 3 bedava hakkın birini harca), `npx ccusage daily`, cloudflared tüneli, `testci/`ya kare-süresi + piksel farkı.
2. B1 başı: motor kararı (Canvas2D sprite ya da Three.js). Canvas2D ise → sprite atlas (free-tex-packer-cli ya da Pillow), Blender başsız + (istersen) Blender MCP, KTX2'yi atla. Three.js ise → parallax-threejs ve threejs-game-skills'e bak (önce kodu oku), KTX2 yolunu aç.
3. B1 sonu: telefonda `_android`/`chrome://inspect` ile gerçek fps, yerel olay günlüğü + kopyala düğmesi, itch.io gizli sayfa.
4. B2: PWA + Bubblewrap/TWA (gerekirse Capacitor), Play 12 kişi/14 gün kapalı test, mağaza görselleri (Canva).

## Erişilemeyen / doğrulanamayan

- **X (Twitter) / ClaudeDevs gönderisi**: açılamadı; yalnızca resmî belge ve ikincil blog yazıları.
- **Açılmayan depo/site sayfaları** (yalnızca arama özeti): `ahujasid/blender-mcp`, `free-tex-packer-cli`, `coreway-labs/blender-sprite-render`, Bubblewrap deposu, Kenney, Freesound, Google Play yardım sayfası, Firebase/BrowserStack fiyat sayfaları. Lisans, bakım durumu ve fiyatlar bu yüzden belirtilen yerde "doğrulanmadı".
- **Doğrulananlar (sayfayı açtım)**: https://code.claude.com/docs/en/code-review, https://code.claude.com/docs/en/ultrareview, https://github.com/majidmanzarpour/threejs-game-skills (MIT), https://github.com/anthropics/claude-plugins-official (kurulum biçimi `/plugin install ad@claude-plugins-official`; eklenti listesi sayfada görünmedi).
- **Katalog kaynağı** (`SearchPlugins`, "Anthropic Directory"): audiorective, parallax-threejs, Pwa2play, SpriteCook, Android Emulator QA, Oh My Android, Claude Code Cost, code-review (Anthropic), claude-code-review-council, code-review-harness. Hepsi "etkin değil"; kurulum yapılmadı. `SearchSkills` boş döndü, `ListPlugins` boş (hesapta etkin eklenti yok).
- WebSearch yalnızca ABD sonuçları verir; Türkçe kaynak aranmadı.

## Başlıca kaynaklar

- Code Review: https://code.claude.com/docs/en/code-review
- Ultrareview: https://code.claude.com/docs/en/ultrareview
- Resmî eklenti deposu: https://github.com/anthropics/claude-plugins-official
- Three.js oyun becerileri: https://github.com/majidmanzarpour/threejs-game-skills
- Playwright Android: https://playwright.dev/docs/api/class-android
- Playwright cihaz taklidi (MCP): https://playwright.dev/agents/browser-and-emulation
- itch.io butler: https://itch.io/docs/butler/pushing — HTML5: https://itch.io/docs/creators/html5
- TWA hızlı başlangıç: https://developer.chrome.com/docs/android/trusted-web-activity/quick-start
- Bubblewrap anlatımı: https://www.thinktecture.com/en/pwa/twa-bubblewrap
- Play 12 test kullanıcısı kuralı (ikincil): https://www.testerscommunity.com/guides/how-many-testers-do-you-need-google-play
- ccusage: https://npmjs.com/package/ccusage
- KTX2/gltf-transform (Babylon forumu): https://forum.babylonjs.com/t/how-to-use-ktx2-basis-compressed-normals/16021
- Atlas CLI'ları: https://www.jsdelivr.com/package/npm/free-tex-packer-cli , https://lib.rs/crates/yatp-cli , https://www.mintlify.com/Hexeption/FastPack/quickstart
- Cloudflare hızlı tünel: https://flaviocopes.com/cloudflare-quick-tunnels/
- COPPA/3. taraf SDK çalışması: https://petsymposium.org/popets/2018/popets-2018-0021.php
- Freesound MCP: https://glama.ai/mcp/servers/timjrobinson/FreesoundMCPServer/inspect
