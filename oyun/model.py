# "Son Durak: Plüton" sayısal oyun modeli: tek doğru kaynak.
# Belge (tasarim_uret.py) tabloları buradan üretir; oyun kodu ileride aynı veriyi JSON olarak okuyacak.
# Çalıştır: python3 oyun/model.py   -> tutarlılık kontrolleri + kalkış fiziği kontrolü + oyun/model.json
import json, math, os

# ---------------------------------------------------------------- roketin durum değişkenleri
# (kimlik, ad, birim, başlangıç değeri, açıklama)
STATE = [
    ("m_kuru", "Kuru kütle", "t", "12", "Yakıtsız roket. Her kalkan ve modül ekler."),
    ("m_yakit", "Yakıt", "t", "50", "Birinci kademe. Biterse motor susar."),
    ("T", "İtki", "kN", "1.100", "Gaz kolu 0–100% ile ölçeklenir. İtki/ağırlık başlangıçta 1,8: tam gazda Max-Q aşılır."),
    ("Isp", "Verim (özgül itki)", "s", "280 / 310", "Deniz seviyesi / boşluk. Yakıt tüketimi = itki ÷ (Isp × 9,81)."),
    ("CdA", "Hava direnci", "m²", "4,0", "Göçükler ve kopan parçalarla artar."),
    ("q_max", "Yapısal basınç sınırı", "kPa", "35", "Dinamik basınç q = ½ρv² bunu aşarsa gövde hasar alır."),
    ("HP", "Bölge dayanıklılığı", "puan", "100", "Burun, tank, motor, aviyonik 100; kanatçıklar 60; panel ve yelken 40."),
    ("H", "Isı", "%", "0", "100'de hasar başlar; 80'in üstünde motor gücü kısılır."),
    ("D", "Radyasyon dozu", "birim", "0", "Birikir. 100'de aviyonik çöker."),
    ("E", "Enerji", "kWh", "5", "Sıfırlanırsa aviyonik ve kontrol kapanır."),
    ("w", "Kontrol gücü", "°/s", "25", "En yüksek dönüş hızı. Jimbal ve hassas iticilerle artar, hasarla düşer."),
    ("R", "Algılama menzili", "m", "600", "Engelin ekranda belirdiği uzaklık. Karanlıkta 300."),
    ("slot", "Modül yuvası", "adet", "2", "Lojistik dalıyla 5'e kadar çıkar."),
]

# ---------------------------------------------------------------- ortam
ENV = [
    ("Hava yoğunluğu", "ρ(h) = 1,225 · e^(−h / 8,5 km) kg/m³", "Dünya. Mars'ta yüzeyde 0,020 ve ölçek 11 km; Titan'da yüzeyde 5,4."),
    ("Yerçekimi", "g(h) = 9,81 · (R / (R + h))²", "Her gök cismi kendi kütlesi ve yarıçapıyla."),
    ("Güneş akısı", "S(r) = 1361 W/m² · (1 AU / r)²", "Güneş paneli, güneş yelkeni ve ısınma bununla ölçeklenir."),
    ("Güneş rüzgârı", "yoğunluk ∝ 1/r², hız 400 km/s (koronal delikte 800)", "Elektrik yelken itkisi ∝ 1/r, manyetik yelken ∝ 1/r^(2/3)."),
]

# ---------------------------------------------------------------- engel aileleri: sayısal etkiler
# (aile, değişkenlere etkisi, sayılar, karşı önlemlerin etkisi)
FAMILY_FX = {
 "Hareketli sürüler": ("Çarpışma hasarı; motora girerse itki kaybı ve tork",
    "Kuş: 25 HP; motor girişine girerse 4 s boyunca itki −%30 ve dönme torku. Balon: 60 HP. Uydu: 80 HP. Yolcu uçağı: anında son.",
    "Eskort drone sürüyü 80 m önden dağıtır (3 şarj). Karbon kompozit hasarı −%30. Engel radarı 5 s önceden uyarır."),
 "Küçük darbe yağmuru": ("Sürekli küçük hasar ve kalıcı direnç artışı",
    "Saniyede yoğunluk × hız/100 darbe; darbe başına 1–3 HP ve CdA +%0,5 (göçük).",
    "Whipple kalkanı −%60, karbon kompozit −%30. Alandan hızlı çıkmak toplam darbeyi azaltır."),
 "Elektrik darbesi": ("Kontrol kesintisi",
    "Yön girişi 1,5–3 s işlemez, gaz sabit kalır. %20 olasılıkla aviyonik −15 HP.",
    "Faraday kafesi süreyi −%80 kısaltır ve aviyonik hasarını önler."),
 "Radyasyon alanı": ("Birikimli doz ve aviyonik hataları",
    "D saniyede alan yoğunluğu (1–12) kadar artar. Her saniye D × 0,02% olasılıkla kısa yön sapması. D = 100'de aviyonik çöker.",
    "Radyasyon zırhı alımı −%50, manyetik radyasyon kalkanı −%85. Doz uçuş sonunda sıfırlanır."),
 "Rüzgâr ve akıntılar": ("Yanal kuvvet; doğru hizada ileri ivme",
    "Atmosferde F = ½ρ · 1,2 · A_yan · v_rüzgâr² (A_yan 40 m²). Uzayda 0,5–3 m/s² sabit ivme alanı. Kopan her kanatçık A_yan +%20.",
    "Jimbal motor kontrol gücü +%40. Engel radarı rüzgâr okunu gösterir."),
 "İtki sütunları": ("Dikey ivme",
    "Sütun içinde +2–6 m/s². Gayzerde ayrıca buzlanma: kütle +0,2 t/s.",
    "Karşı önlem gerekmez; içinden geçmek fırsat."),
 "Yoğun enkaz alanları": ("Çarpışma hasarı; çarpılan parça bölünür",
    "Hasar = 20–100 HP (parça kütlesine göre). Çarpılan parça 3–5 parçaya bölünür, her biri 1/4 hasar verir (Kessler).",
    "Otomatik kaçınma çarpışmadan 0,8 s önce yan kaçış yapar (%70 başarı, 4 s bekleme). Whipple kalkanı küçük parçalarda −%40."),
 "Görünmez tehlikeler": ("Algılama menzilini düşürür",
    "Karanlıkta ve tozda R 300 m'ye, kara halkalarda 80 m'ye iner.",
    "LIDAR R = 2 km, engel radarı R = 3 km (radar tozdan etkilenmez)."),
 "Sinsi yükler": ("Kütle artışı, itki kaybı, yavaş HP kaybı",
    "Buzlanma kütle +0,3 t/s. Volkanik kül itki −%1/s (en fazla −%30, uçuş boyunca kalıcı). Atomik oksijen gövde −0,5 HP/s. Termosfer ve parlayan bulutlar hız kaybı.",
    "Isıtmalı gövde buzlanmayı −%90, seramik kaplama kül ve atomik oksijeni −%80 azaltır."),
 "Yapısal sınırlar": ("Hız ve açı eşiği",
    "q > q_max ise gövde saniyede (q/q_max − 1) × 200 HP kaybeder. Pogo ilk 1 km'de kontrolü ±%30 titretir. Yörünge için yatay hız ≥ √(μ/r) (Dünya'da ~7,8 km/s).",
    "Karbon kompozit q_max ×1,5. Pogo sönümleyici titreşimi kaldırır. Otopilot ideal dönüş profilini uygular."),
 "Zamanlama anları": ("Doğru anda yapılan eylemin ödülü",
    "Kademe ayırma: yakıt bitince 1,5 s içinde ayırırsan +%8 anlık hız; sonraki her saniye ölü kütle cezası. Ay'a atış: motoru en yakın noktada ±2 s içinde yakarsan tam verim, dışında verim düşer.",
    "Sapan hesaplayıcı pencereyi önceden gösterir."),
 "Sapanlar": ("Yakıtsız hız kazancı ya da frenleme",
    "Δv = 2 · V_gezegen · sin(δ/2) · cos θ. δ sapma açısı (yakın geçiş = büyük açı, ama çarpma riski), θ gezegenin hareket yönüne göre giriş açısı: arkasından geçersen artı, önünden geçersen eksi.",
    "Sapan hesaplayıcı tek sapanın sonucunu, zincir planlayıcı art arda sapanları önceden çizer."),
 "Kararsız yerçekimi": ("Yavaş sürüklenme",
    "Yönü yavaşça değişen 0,05–0,3 m/s² sürüklenme ivmesi.",
    "Hassas iticiler düzeltme gücünü ×3 yapar."),
 "Atmosfere giriş": ("Giriş açısı koridoru",
    "Isınma ∝ ρ · v³. Çok dik girersen H 100'ü geçer ve yanarsın; çok sığ girersen sekip uzaya kaçarsın. Mars koridoru −10° ile −13° arası.",
    "Ablatif ısı kalkanı koridoru ×1,5 genişletir ve ısı alımını −%50 azaltır. Süpersonik retro motor son evrede frenler."),
 "İnişler": ("İniş toleransları",
    "Dikey hız ≤ 3 m/s, yatay ≤ 1 m/s, eğim ≤ 10°. Ay depremi zemini ±0,5 m/s salar.",
    "Esnek iniş bacakları dikey sınırı 5 m/s'ye çıkarır. LIDAR zemini önceden tarar."),
 "Enerji kapıları": ("Güç dengesi",
    "Üretim − tüketim < 0 ise E azalır; E = 0'da aviyonik kapanır. Güneş paneli üretimi Dünya'da %100, Mars'ta %43, Jüpiter'de %3,7, Satürn'de %1,1. Ay gecesinde panel 0 ve batarya kapasitesi −%50.",
    "RTG sabit 2 kW, yakıt hücresi 3 kW (30 dk), kompakt füzyon 20 kW. Toz şeytanı panel verimini %100'e döndürür."),
 "Yakala ve topla": ("Yanaşma ödülü",
    "Göreli hız ≤ 2 m/s ve 15 m içinde 2 s kalırsan yakalanır.",
    "Robot kol menzili 30 m, hız toleransı 5 m/s. Madenci drone kaynak başına 20 s."),
 "Bilim ve kilometre taşları": ("Bilim puanı",
    "Bölgeden geçiş ya da fotoğraf: hedef ekranın en az %30'unu kaplarken 1 s sabit kadraj.",
    "Karşı önlem gerekmez."),
 "Güvenli koridorlar ve üsler": ("Tehlikeyi azaltan yollar ve checkpoint",
    "Koridor içinde enkaz yoğunluğu ×0,1. Üs kurulunca sonraki uçuşlar oradan başlayabilir.",
    "Zincir planlayıcı koridorları haritada gösterir."),
}

SUN_FX = [
    ("Erime sınırı", "En yakın güvenli Güneş uzaklığı: kalkansız 0,30 AU, ablatif kalkanla 0,20, Güneş dalış kalkanıyla 0,05 (~10 Güneş yarıçapı), gölge drone ile 0,04. İçine girersen H saniyede +40."),
    ("Güneş patlaması", "Uyarısız; algılama ve kontrol 2 s kör. Uzay hava durumu uydusu 3 s önceden uyarır."),
    ("CME", "Ani doz +40 ve plazma basıncı (dalga yönünde 3 m/s², 8 s). Normalde 15 s, uzay hava durumu uydusuyla 60 s önceden uyarı."),
    ("Yerçekimi kuyusu", "Güneş'ten uzaklaşırken hız sürekli azalır (gerçek yörünge mekaniği); dış gezegenler için gereken hız buradan gelir."),
    ("Güneş Oberth dalışı", "Ateşleme verimi = e^(−(t − t_peri)² / 0,72): en yakın anın ±1,5 s'si içinde verim > %20, tam anında %100. Kazanılan enerji ∝ anlık hız × Δv; aynı yakıt Dünya yakınındakinin 5–8 katı hız kazandırır."),
    ("Koronal delik akımı", "Yelken itkisi ×4, 60–120 s boyunca. Uzay hava durumunda 'Maksimum' günlerde %35, 'Aktif' günlerde %15 olasılıkla görünür."),
    ("Plazma sörfü", "CME dalgasının ilk 5 s'sinde plazma emici kalkan açıksa dalga +8 m/s² itki verir ve doz almazsın."),
]
WEATHER = [("Sakin", 0.5, 0.0, 0.7), ("Aktif", 1.0, 0.15, 1.0), ("Maksimum", 2.5, 0.35, 1.3)]  # (ad, CME sıklık çarpanı, koronal delik olasılığı, yelken çarpanı)

# ---------------------------------------------------------------- geliştirme ağacı: sayısal etkiler
# kademe fiyatı: 220 × 1,95^(k−1) kredi; kademe 3+ ayrıca bilim, kademe 5+ ayrıca malzeme ister
PRICE = lambda k: round(220 * 1.95 ** (k - 1) / 10) * 10
SCIENCE = {1: 0, 2: 0, 3: 20, 4: 45, 5: 90, 6: 160}
MATERIAL = {1: 0, 2: 0, 3: 0, 4: 0, 5: 10, 6: 25}
UNLOCK = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 6}  # kademe k, şu bölüme ulaşınca satın alınabilir (0 = baştan)

TREE = {
 "İtki": [
  ("Kerosen motor", "İtki ×1,25", "—"),
  ("Aerospike nozul", "Deniz seviyesi verimi boşluk verimine eşitlenir (Isp 310 / 310)", "Kuru kütle +%3"),
  ("Metan motor (yeniden ateşleme)", "Isp 310 / 350; uzayda yeniden ateşlenebilir (yörünge ve Ay için şart)", "—"),
  ("Hava soluyan motor", "0–25 km arasında oksitleyici harcamaz: atmosferde yakıt tüketimi −%45", "Kuru kütle +%8"),
  ("Nükleer termal motor", "Isp 850, itki 250 kN", "Atmosferde çalışmaz; 100 km üstünde açılır"),
  ("Füzyon motoru", "Isp 20.000, itki 400 kN", "Kompakt füzyon enerjisi ister"),
 ],
 "Uzun yol sürüşü": [
  ("Güneş yelkeni", "1 AU'da 0,5 m/s² × cos²(açı) × (1 AU / r)²", "Karanlıkta işe yaramaz; çarpışmada kopabilir"),
  ("İyon motoru", "Isp 3.000, sürekli 0,2 m/s²", "1,5 kW enerji tüketir"),
  ("Elektrik yelken", "1 AU'da 0,4 m/s², uzaklıkla yalnızca 1/r azalır", "0,5 kW tüketir; manyetik yelkenle aynı anda açılamaz"),
  ("Manyetik yelken", "Güneş rüzgârıyla itki ya da varışta frenleme; CME'de itki ×5", "Elektrik yelkenle aynı anda açılamaz"),
  ("Güneş termal roketi", "Isp 800, itki ∝ (1 AU / r)²: Güneş'e yaklaştıkça çok güçlenir", "Uranüs ötesinde neredeyse sıfır"),
  ("Buhar roketi", "Isp 190; yakıtı buzdan doldurulur", "Madenci drone ile anlamlı"),
 ],
 "Gövde ve kalkan": [
  ("Karbon kompozit", "Kuru kütle −%10, q_max ×1,5, darbe hasarı −%30", "—"),
  ("Ablatif ısı kalkanı", "Giriş koridoru ×1,5, atmosferik ısı −%50", "Kütle +%6; her uçuşta yenilenir"),
  ("Whipple kalkanı", "Küçük darbe −%60, küçük enkaz −%40", "Kütle +%5"),
  ("Kendini onaran gövde", "Saniyede +1 HP; göçük direnci zamanla geri alınır", "Kopan parçaları geri getirmez"),
  ("Güneş dalış kalkanı", "En yakın güvenli Güneş uzaklığı 0,05 AU; önden ısı −%90", "Kütle +%8; yalnızca önden korur, kalkanı Güneş'e dönük tutmak gerekir"),
  ("Manyetik radyasyon kalkanı", "Radyasyon −%85, CME hasarı −%70", "2 kW enerji tüketir"),
 ],
 "Aviyonik": [
  ("Yerçekimi dönüşü otopilotu", "Yükselişte ideal eğim profili; oyuncu yalnızca kaçınır", "—"),
  ("Engel radarı", "Algılama 3 km; ekran dışı tehlike 5 s önceden", "—"),
  ("Otomatik kaçınma", "Çarpışmadan 0,8 s önce yan kaçış, %70 başarı", "4 s bekleme; yakıt harcar"),
  ("Sapan hesaplayıcı", "Tek sapanın ve ateşleme pencerelerinin hayalet rotası", "—"),
  ("Zincir planlayıcı", "Çoklu sapan, rezonans kombosu, Lagrange otoyolları ve güvenli koridorlar", "—"),
  ("Uzay hava durumu uydusu", "CME uyarısı 60 s, patlama uyarısı 3 s önce; koronal delikleri gösterir", "—"),
 ],
 "Enerji": [
  ("Batarya", "Enerji kapasitesi ×2", "—"),
  ("Güneş paneli", "1 AU'da 5 kW × (1 AU / r)²", "Açık panel çarpışmada kopabilir"),
  ("Yakıt hücresi", "Sabit 3 kW, 30 dakika", "—"),
  ("Isı radyatörleri", "Soğuma ×2,5", "Çarpışmada kopabilir"),
  ("RTG (nükleer pil)", "Sabit 2 kW, süresiz", "Kütle +%5"),
  ("Kompakt füzyon", "Sabit 20 kW", "Kütle +%7"),
 ],
 "Lojistik": [
  ("İki kademe", "Üst kademe ekler (bkz. kalkış fiziği); modül yuvası 3", "—"),
  ("Balonla kalkış", "Uçuş 30 km'den başlar, troposfer atlanır", "O uçuşta troposferden kazanç yok"),
  ("Üç kademe ve booster dönüşü", "Üçüncü kademe; booster dönüş mini oyunu başarılırsa kazanç +%15; modül yuvası 4", "—"),
  ("Yörünge yakıt deposu", "Yörüngede bir kez tam yakıt ikmali", "—"),
  ("Ay Üssü", "Ay checkpoint'i; He-3 madenciliği; modül yuvası 5", "He-3 malzemesi ister"),
  ("Mars yakıt fabrikası", "Mars checkpoint'i; metan ikmali", "—"),
 ],
}

# modüller: tek seferlik satın alınır, uçuş öncesi yuvaya takılır (yuva sayısı sınırlı)
MODULES = [
 ("Pogo sönümleyici", 1, 120, "Kalkış titreşimini kaldırır."),
 ("Jimbal motor", 1, 180, "Kontrol gücü +%40."),
 ("Isıtmalı gövde", 1, 160, "Buzlanma −%90."),
 ("Faraday kafesi", 1, 240, "Elektrik darbesi süresi −%80, aviyonik hasarı yok."),
 ("Seramik kaplama", 1, 260, "Volkanik kül ve atomik oksijen −%80."),
 ("Yıldız izleyici", 3, 300, "Manyetik sapmalardan etkilenmeyen yön."),
 ("Yanaşma sistemi", 3, 320, "Yanaşma toleransı ×2."),
 ("Radyasyon zırhı", 3, 450, "Radyasyon −%50. Kütle +%4."),
 ("Hassas iticiler", 4, 520, "Sürüklenme düzeltmesi ×3, ince manevra."),
 ("LIDAR", 4, 600, "Algılama 2 km, iniş zemini taraması."),
 ("Esnek iniş bacakları", 4, 480, "İniş dikey hız sınırı 5 m/s."),
 ("Süpersonik retro motor", 5, 900, "İnce atmosferde son evre frenleme."),
 ("Elektrodinamik ip", 7, 1400, "Jüpiter ve Io çevresinde 10 kW enerji üretir."),
]

SIDE = [  # yan araçlar: (ad, açılış bölümü, fiyat, sayısal etki)
 ("Eskort drone", 1, 300, "Sürüyü 80 m önden dağıtır; 3 şarj."),
 ("Kurtarma kapsülü", 1, 400, "Patlamadan önce fırlatılırsa o uçuşun kazancının %50'si korunur."),
 ("Keşif sondası", 3, 650, "30 s boyunca önündeki engelleri haritada gösterir."),
 ("Booster dönüşü", 3, 700, "Lojistik 3 ile; mini oyun başarılırsa kazanç +%15."),
 ("Robot kol", 3, 800, "Menzil 30 m, hız toleransı 5 m/s."),
 ("Madenci drone", 4, 1100, "Kaynak başına 20 s; buz, metal, metan, He-3."),
 ("Uzay römorkörü", 4, 1300, "Yakıt deposundan tank getirir ya da hedef yörüngeye çeker."),
 ("Lazer temizleyici", 3, 1500, "Rotadaki enkazın %60'ını düşürür, uçuş başına 1 kez."),
 ("Gölge drone", 5, 2200, "Güneş'e en yakın güvenli uzaklığı −%20 iter; dalışta kendisi erir."),
 ("Aerojel toplayıcı", 6, 1800, "Kuyruklu yıldız tozundan bilim ×3."),
]

LEGEND = [  # (ad, açılış bölümü, kredi, malzeme, sayısal etki) — fiyatlar 6. kademenin ~1–3 katı
 ("Skyhook", 3, 4000, 20, "Doğru anda yakalanırsan +3 km/s anlık hız."),
 ("Lazer yelken", 4, 6000, 30, "5 m/s², 10 dakika; Dünya'dan uzaklaştıkça azalır."),
 ("Ay kütle sürücüsü", 4, 7000, 40, "Ay Üssü'nden 2,5 km/s ile bedava fırlatma."),
 ("Plazma emici kalkan", 5, 9000, 40, "CME'yi itkiye çevirir (+8 m/s²) ve dozu sıfırlar."),
 ("Kuyruklu yıldız sörfü", 6, 10000, 50, "Zıpkınla tutun; kuyruklu yıldızın Güneş geçişini kalkansız paylaş."),
 ("Orion darbesi", 6, 12000, 60, "Saniyede 1 darbe, darbe başına +40 m/s; her darbe sarsıntı ve 1 HP."),
 ("Merkür ayna dizisi", 7, 15000, 80, "Yelken itkisi 40 AU'ya kadar uzaklıktan bağımsız sabit."),
 ("Uzay asansörü", 8, 20000, 100, "Dünya'dan yörüngeye bedava; bölüm 1–3 atlanır."),
]

ORBIT_FX = [
 ("Sapanın yönü", "Δv = 2 · V_gezegen · sin(δ/2) · cos θ. Ay ~1 km/s'ye, Jüpiter 10 km/s'nin üstüne kadar kazandırabilir; önden geçişte aynı miktar kaybettirir."),
 ("Fırlatma pencereleri", "Pencere içinde Mars'a gereken hız −%35. Oyun ölçeğinde pencere her 6 uçuşta bir açılır ve 2 uçuş sürer; hangarda sayaç."),
 ("Büyük Tur hizalanması", "Jüpiter'e ulaşan uçuşlarda %8 olasılıkla görünür; zincir planlayıcı ile dört sapan art arda, toplam +25 km/s'ye kadar."),
 ("Lagrange otoyolları", "Yakıt harcamaz; aynı mesafe ×3 sürede alınır. Otoyol içinde enkaz yoğunluğu ×0,1."),
 ("Rezonans kombosu", "Doğru ritimde her sapan bir öncekinin kazancını ×1,3 büyütür (üç sapanda toplam ×1,69)."),
 ("Atmosfer yakalaması", "Koridor içinde yakıtsız yörüngeye giriş; koridor genişliği ablatif kalkanla ×1,5."),
]

INTERACTIONS = [
 ("Çarpanlar birikir", "Aynı değişkene etki eden çarpanlar çarpılır; azaltma oranları 1 − ∏(1 − r) ile birleşir ve en fazla %90'a ulaşır. Hiçbir şey tam bağışıklık vermez."),
 ("Kütle her şeyi etkiler", "Her kalkan ve modül kütle ekler; itki/ağırlık ve ivme düşer. Hafif uçmak da bir strateji."),
 ("Hasarlı motor", "Motor HP %50'nin altına inince itki (1 − HP) × 0,5 oranında düşer ve tek taraflı tork başlar."),
 ("Kopan kanatçık", "Her biri kontrol gücü −%25 ve yan alan +%20; rüzgâr daha çok iter."),
 ("Delinen tank", "Tank HP %40'ın altında yakıt sızar: saniyede (0,4 − HP) × %2."),
 ("Hasarlı aviyonik", "Aviyonik HP %50'nin altında kontrol 0,2 s gecikir; elektrik darbesi ve radyasyon etkisi ×1,5."),
 ("Isı ve güç", "H > 80 iken motor gücü kısılır; Güneş termal roketi ve dalış birlikte ısı yönetimini zorlaştırır."),
 ("Yelkenler", "Elektrik ve manyetik yelken aynı rüzgârı kullanır; aynı anda yalnızca biri açılır. Güneş yelkeni ikisiyle birlikte açılabilir."),
 ("Nükleer kısıt", "Nükleer termal motor atmosferde çalışmaz; kalkış için kimyasal bir alt kademe gerekir."),
 ("En güçlü kombo", "Güneş termal roketi + Güneş dalış kalkanı + gölge drone + uzay hava durumu uydusu: Oberth dalışında oyunun en büyük hız kazancı."),
]

# ---------------------------------------------------------------- kalkış fiziği (Dünya, 2B nokta kütle)
MU, RE, G0 = 3.986e14, 6.371e6, 9.80665

TURN_H = 60000
P = dict(T1=1100, kuru1=12, yakit1=50, kuru2=2.0, yakit2=12, T2=130, kuru3=0.9, yakit3=3.2, T3=40)

def roket(it=0, gov=0, lojistik=0):
    """(kuru t, yakıt t, itki kN, Isp_deniz, Isp_boşluk) kademeleri ve q_max kPa."""
    T = P["T1"] * (1.25 if it >= 1 else 1)
    isp_sl, isp_vac = (310, 310) if it >= 2 else (280, 310)
    if it >= 3: isp_sl, isp_vac = 310, 350
    kuru = P["kuru1"] * (0.9 if gov >= 1 else 1) * (1.03 if it >= 2 else 1)
    st = [(kuru, P["yakit1"], T, isp_sl, isp_vac)]
    if lojistik >= 1:
        st.append((P["kuru2"], P["yakit2"], P["T2"] * (1.25 if it >= 1 else 1), isp_vac, isp_vac + 15))
    if lojistik >= 3:
        st.append((P["kuru3"], P["yakit3"], P["T3"], isp_vac, isp_vac + 25))
    return st, 35 * (1.5 if gov >= 1 else 1)

def ucus(stages, q_max, otopilot=False, gaz_yonetimi=False, dt=0.05):
    """Otopilot: gerçek yerçekimi dönüşü; en iyi başlangıç yatırmasını dener."""
    if otopilot:
        sonuc = [_ucus(stages, q_max, kick, gaz_yonetimi, dt) for kick in (40e3, 60e3, 80e3, 100e3, 130e3, 170e3, 220e3)]
        yor = [r for r in sonuc if r[3]]
        return yor[0][:4] if yor else max(sonuc, key=lambda r: r[4])[:4]
    return _ucus(stages, q_max, None, gaz_yonetimi, dt)[:4]

def _ucus(stages, q_max, kick, gaz_yonetimi, dt):
    """Sonuç: (durum, en yüksek irtifa km, en yüksek q kPa, yörünge mi)."""
    x = h = vx = vy = 0.0
    yakit = [s[1] for s in stages]; k = 0
    qmax_seen = 0.0; apo = 0.0
    t = 0.0; thr_s = 1.0
    while t < 1200:
        t += dt
        r = RE + h
        g = MU / r**2
        rho = 1.225 * math.exp(-h / 8500)
        v = math.hypot(vx, vy)
        q = 0.5 * rho * v * v
        qmax_seen = max(qmax_seen, q / 1000)
        if q / 1000 > q_max:
            return ("Max-Q'da parçalandı", h / 1000, qmax_seen, False, -9e9)
        kuru = sum(s[0] for s in stages[k:])
        m = (kuru + sum(yakit[k:])) * 1000
        thr = 0.0
        if yakit[k] > 0:
            ku, _, T, isp_sl, isp_vac = stages[k]
            p = math.exp(-h / 8500)
            isp = isp_vac - (isp_vac - isp_sl) * p
            if gaz_yonetimi:
                thr_s = thr_s - 1.5 * dt if q / 1000 > 0.85 * q_max else thr_s + 0.5 * dt
                thr_s = min(1.0, max(0.0, thr_s))
            thr = thr_s if gaz_yonetimi else 1.0
            F = T * 1000 * thr
            yakit[k] -= F / (isp * G0) * dt / 1000
            if yakit[k] <= 0:
                yakit[k] = 0
                if k + 1 < len(stages): k += 1
        else:
            F = 0.0
        # yön: dik ya da otopilot (1 km'den sonra yatarak 70 km'de yataya)
        if kick is not None and h > 500:
            ang = max(0.0, 90 * (1 - min(1.0, (h - 500) / kick) ** 0.5))  # kick = dönüş yüksekliği (m)
        else:
            ang = 90.0
        a = math.radians(ang)
        drag = 0.5 * rho * v * v * 4.0
        ax = (F * math.cos(a) - (drag * vx / v if v > 0 else 0)) / m
        ay = (F * math.sin(a) - (drag * vy / v if v > 0 else 0)) / m - g + vx * vx / r
        vx += ax * dt; vy += ay * dt
        h += vy * dt; x += vx * dt
        apo = max(apo, h)
        if h < 0 and t > 5:
            return ("düştü", apo / 1000, qmax_seen, False, -9e9)
        if F == 0 and all(y <= 0 for y in yakit[k:]):
            # yakıt bitti: yörünge mi, balistik mi?
            r = RE + h; v2 = vx * vx + vy * vy
            E = v2 / 2 - MU / r; hh = r * vx
            if E < 0:
                sma = -MU / (2 * E); ecc = math.sqrt(max(0, 1 + 2 * E * hh * hh / MU**2))
                peri = sma * (1 - ecc) - RE; apoh = sma * (1 + ecc) - RE
                if peri > 100e3:
                    return ("yörüngede", apoh / 1000, qmax_seen, True, peri)
                return ("yakıt bitti, geri düşüyor", apoh / 1000, qmax_seen, False, peri)
            return ("kaçış hızı", h / 1000, qmax_seen, True, 9e9)
    return ("zaman aşımı", apo / 1000, qmax_seen, False, -9e9)

def fizik_kapilari():
    """Hangi donanımla nereye fiziksel olarak varılabildiği (ideal pilot, engelsiz)."""
    sen = [
        ("Başlangıç roketi, tam gaz", dict(), dict()),
        ("Başlangıç roketi, Max-Q'da gaz kısılarak", dict(), dict(gaz_yonetimi=True)),
        ("+ Karbon kompozit, tam gaz", dict(gov=1), dict()),
        ("+ Karbon + iki kademe (dik çıkış)", dict(gov=1, lojistik=1), dict(gaz_yonetimi=True)),
        ("+ Karbon + iki kademe + otopilot", dict(gov=1, lojistik=1), dict(otopilot=True, gaz_yonetimi=True)),
        ("+ Kerosen motor + aerospike + karbon + iki kademe + otopilot", dict(it=2, gov=1, lojistik=1), dict(otopilot=True, gaz_yonetimi=True)),
        ("+ Metan motor + karbon + üç kademe + otopilot", dict(it=3, gov=1, lojistik=3), dict(otopilot=True, gaz_yonetimi=True)),
    ]
    out = []
    for ad, rk, uk in sen:
        st, qm = roket(**rk)
        out.append((ad,) + ucus(st, qm, **uk))
    return out

# ---------------------------------------------------------------- tutarlılık kontrolleri
def kontroller(chapters, families):
    tree_names = {n: (dal, i + 1) for dal, items in TREE.items() for i, (n, _, _) in enumerate(items)}
    mod_names = {n: b for n, b, _, _ in MODULES}
    side_names = {n: b for n, b, _, _ in SIDE}
    leg_names = {n: b for n, b, _, _, _ in LEGEND}
    sonuc = []
    def ok(ad, hatalar):
        sonuc.append((ad, not hatalar, hatalar))
    # 1) her karşılık tanımlı bir öğe mi
    tanimsiz = sorted({o[4] for c in chapters for o in c[5] if o[4] != "—" and o[4] not in tree_names and o[4] not in mod_names and o[4] not in side_names and o[4] not in leg_names})
    ok("Her engel karşılığı tanımlı bir geliştirme, modül ya da yan araç", tanimsiz)
    # 2) her ölümcül engelin karşılığı var
    karsiliksiz = [o[0] for c in chapters for o in c[5] if o[2] == "P" and o[4] == "—"]
    ok("Her ölümcül engelin bir karşılığı var", karsiliksiz)
    # 3) ölümcül engellerin karşılığı o bölümde satın alınabilir
    gec = []
    for c in chapters:
        b = int(c[0]) - 1
        for o in c[5]:
            if o[2] != "P" or o[4] == "—": continue
            n = o[4]
            if n in tree_names: acilis = UNLOCK[tree_names[n][1]]
            elif n in mod_names: acilis = mod_names[n] - 1
            elif n in side_names: acilis = side_names[n] - 1
            else: acilis = leg_names[n] - 1
            if acilis > b: gec.append(f"{o[0]} (bölüm {c[0]}) → {n} ancak bölüm {acilis + 1}'de açılıyor")
    ok("Ölümcül engellerin karşılığı, engelin çıktığı bölümde satın alınabiliyor", gec)
    # 4) aile etkileri eksiksiz
    eksik = [f[0] for f in families if f[0] not in FAMILY_FX]
    ok("Her engel ailesinin sayısal etkisi tanımlı", eksik)
    # 5) her bölümde en az bir fırsat
    firsatsiz = [c[1] for c in chapters if not any(o[2] == "I" for o in c[5])]
    ok("Her bölümde en az bir fırsat var", firsatsiz)
    # 6) fizik kapıları: başlangıç roketi Max-Q'yu tam gazla geçemez, iki kademe olmadan Kármán'a ulaşılmaz, yörünge mümkün
    fk = fizik_kapilari()
    h = []
    if fk[0][1] != "Max-Q'da parçalandı": h.append("Başlangıç roketi tam gazla Max-Q'yu geçebiliyor (ders kaybolur)")
    if fk[1][2] < 100: h.append("Gaz yönetimiyle bile Kármán'a fiziksel olarak ulaşılamıyor")
    if fk[4][4]: h.append("Motor geliştirmesi olmadan yörüngeye girilebiliyor (yörünge bölümü gereksinimiyle çelişir)")
    if not fk[5][4]: h.append("İtki 2 + karbon + iki kademe + otopilot yörüngeye yetmiyor")
    if not fk[6][4]: h.append("Metan motor + üç kademe yörüngeye yetmiyor")
    ok("Kalkış fiziği ilerleme kapılarını doğruluyor", h)
    return sonuc, fk

def json_disari(path):
    d = dict(state=STATE, env=ENV, family_fx=FAMILY_FX, sun_fx=SUN_FX, weather=WEATHER,
             tree={k: v for k, v in TREE.items()}, price={k: PRICE(k) for k in range(1, 7)}, science=SCIENCE,
             material=MATERIAL, unlock=UNLOCK, orbit_fx=ORBIT_FX, modules=MODULES, side=SIDE, legend=LEGEND, interactions=INTERACTIONS)
    json.dump(d, open(path, "w"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    for r in fizik_kapilari():
        print(f"{r[0]:60s} {r[1]:28s} irtifa {r[2]:8.1f} km  q {r[3]:5.1f} kPa")
