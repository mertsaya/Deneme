# B0 mantık denetimi: bulgular ve durum (2026-10-08)

Denetçi: Opus mantık denetçisi. Uygulayan: uygulayıcı. Yeniden üretim testi: `test/mantik_test.py` (her madde ayrı GECTI/KALDI basar; son koşu 10/10).

| # | Bulgu | Durum | Not / test |
|---|---|---|---|
| 1 | Kayıtta sv B0 tavanını aşınca (`rampa` 7) hangarda `repeat(negatif)` çöküşü | Düzeltildi | Okumada sv `svMaks`'a kırpılıyor; `repeat(Math.max(0, mx − s))`. Test 1 |
| 2 | UÇ / TEKRAR UÇ / YENİDEN BAŞLA'dan hemen sonraki ikinci dokunuş zayıf kalkış yapıyor | Düzeltildi | Rampaya girişten sonra 0,25 s dokunuş kilidi (`B0_ARAYUZ.rampa_kilit`); üç yol da `turBasla`'dan geçiyor. Test 2 |
| 3 | Kara kutuda atlama dokunuşu 0,3 s düğme kilidini geçiyor | Düzeltildi | Kilit ayrı gerçek zaman sayacıyla (`kkAcikT`); atlama yalnız animasyonu ilerletiyor. Görüntülü botun bekleme süresi de bu sayaçla. Test 3 |
| 4 | "Seni durduran" ses metninde negatif Δ (en yüksek hız ≥ ses_v ama 0,3 s tutulmadı) | Düzeltildi | Yeni metin `durduran.ses_yakin`: "Ses duvarına çok yakındın: hızını 0,3 saniye daha koru." (süre `ses_sure`'den). Test 4 |
| 5 | Geri sayımda arka plana geçince menü açılmıyor; sayım sırasında duraklat düğmesi çalışmıyor | Düzeltildi | `duraklat()` geri sayımda da çalışıyor: sayımı iptal edip menüyü açıyor. Test 5 |
| 6 | İlk dokunuş bir düğmeye gelince "Başlamak için dokun" ipucu takılı kalıyor | Düzeltildi | İlk dokunuş hangi yoldan gelirse gelsin ipucu "Yeşilde dokun"a dönüyor. Test 6 |
| 7 | Kayıt doğrulaması tek alanda bütün kaydı siliyor; `efekt`/`yazi` NaN olabiliyor; ikinci bozulma yedeği eziyor | Düzeltildi | `onar()` alan bazında onarıyor (geçersiz alan → varsayılan). `efekt` 0–100, `yazi` ∈ {1; 1,2; 1,4}, `kalite` ∈ liste. `duvar.ses` null ya da tam sayı (ilk kırılışın uçuş numarası; şartnamede tur numarası tutulduğu için boolean değil, doğrulanıyor). Kayıt yalnız JSON/sürüm hatasında yenileniyor; ilk yedek `sdp_kayit_bozuk` korunuyor, sonrakiler `_bozuk_<zaman>`. Test 7 |
| 8 | `duvar.ses` / kara kutu tur numarası üç yolda (doğal bitiş, elle bitirme, açılışta bekleyen) farklı hesaplanıyor | Düzeltildi | Tek işlev: `ucusNo() = tur + elle + 1`. Test 8 |
| 9 | Duraklat menüsünden "Kaydı sıfırla" süren turla çakışıyor | Düzeltildi | Sıfırlama yalnız hangardaki ayarlardan görünüyor. Test 9 |
| 10 | Aynı kayıtla iki sekme açılırsa son yazan kazanır | Bilinen sınır | Yapılmadı (koordinatör kararı); NOTLAR.md "Bilinen sınırlar" |
| 11 | Sim `gorunur_hedef` önbelleği `id(o)` kullanıyor (çöp toplamadan sonra kimlik yeniden kullanılabilir) | Düzeltildi | `ucus_sim.py`: `Nesne.kimlik` sayaçlı (`itertools.count`). `ayar_uret --denetle` temiz, `dogrula.py 200` eşliği 27/27, `kabul.py --hizli` geçti |
| 12 | `?b0s=` eksik değerde NaN | Düzeltildi | Eksik/bozuk değer varsayılana düşüyor. Test 12 |
| 13 | Kara kutuda her karede `querySelectorAll`; efekt havuzlarında `find` kapanışı | Düzeltildi | Satırlar kara kutu açılışında önbelleğe alınıyor; havuz aramaları düz döngü |
