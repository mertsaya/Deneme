# "Son Durak: Plüton" tasarım belgesini veri yapılarından üretir.
# Çalıştır: python3 oyun/tasarim_uret.py  ->  oyun/tasarim.html
import html, os, sys
E = html.escape
HERE = os.path.dirname(os.path.abspath(__file__))
OUTS = [os.path.join(HERE, "tasarim.html")] + sys.argv[1:]

FX = {"P": ("Patlatır", "fx-p"), "Y": ("Yavaşlatır", "fx-y"), "S": ("Saptırır", "fx-s"), "I": ("İvme / fırsat", "fx-i")}
FQ = {"Y": "Yaygın", "S": "Seyrek", "N": "Nadir"}

# (ad, konum, etki, açıklama, karşılığı, gerçek not, sıklık, bu sürümde yeni mi)
chapters = [
 ("1", "Kalkış ve Troposfer", "0 – 12 km", 1.08,
  "Hava yoğun ve kalabalık. İlk uçuşta oyuncu en fazla 3–4 km'ye çıkıp kuşlara ya da yıldırıma yeniliyor.",
  [("Pogo titreşimi", "0–1 km", "S", "Motor ve yakıt hattı rezonansa girer, roket sallanır.", "Pogo sönümleyici", "Saturn V'de gerçek sorun", "Y", 0),
   ("Kuş sürüsü", "0,5–3 km", "P", "Motora giren kuş itkiyi tek taraflı keser, roket dönmeye başlar.", "Eskort drone", None, "Y", 0),
   ("Termal sütun", "1–5 km", "I", "Sıcak hava kolonu yukarı doğru küçük bir itki verir.", "—", None, "Y", 0),
   ("Dolu fırtınası", "2–8 km", "Y", "Buz taneleri gövdeyi döver, hız ve dayanıklılık düşer.", "Karbon gövde", None, "S", 1),
   ("Rüzgâr kesmesi", "2–8 km", "S", "Ani yanal rüzgâr rotayı bozar.", "Jimbal motor", None, "Y", 0),
   ("Volkanik kül bulutu", "3–10 km", "Y", "Aşındırıcı kül motor nozulunu yıpratır, itki kademeli olarak düşer.", "Seramik kaplama", "2010 Eyjafjallajökull külü Avrupa hava trafiğini durdurdu", "S", 1),
   ("Fırtına bulutu ve yıldırım", "4–10 km", "P", "Yıldırım aviyoniği kapatır, kontrol birkaç saniye gider.", "Faraday kafesi", "Apollo 12'ye kalkışta iki kez yıldırım çarptı (1969)", "Y", 0),
   ("Buzlanma", "6–10 km", "Y", "Gövdede buz birikir, kütle artar.", "Isıtmalı gövde", None, "Y", 0),
   ("Yolcu uçağı koridoru", "10–12 km", "P", "Ticari uçuş rotası. Çarpışma kesin son.", "Engel radarı", None, "S", 1),
   ("Jet akımı", "9–12 km", "I", "Doğru yönde girersen ivme, ters açıyla girersen sapma.", "Rota hesaplayıcı", None, "Y", 0),
   ("Max-Q", "11–14 km", "P", "Çok hızlıysan aerodinamik basınç roketi parçalar. Gazı kısmayı öğrenmek zorundasın.", "Karbon gövde", "Her gerçek fırlatmada gaz bu noktada kısılır", "Y", 0)]),
 ("2", "Üst Atmosfer", "12 – 100 km", 2.0,
  "Gökyüzü maviden laciverte, sonra siyaha döner. Oyunun ilk görsel 'vay' anı Kármán hattı.",
  [("Stratosfer balonları", "15–35 km", "P", "Rastgele yükselen bilim balonlarıyla çarpışma.", "Engel radarı", None, "Y", 0),
   ("Ozon tabakası", "20–30 km", "I", "Tehlikesiz. UV ölçümü bilim puanı verir.", "—", None, "Y", 1),
   ("Mavi jetler", "40–50 km", "P", "Bulut tepesinden yukarı fışkıran mavi şimşek.", "Faraday kafesi", "Gerçek üst atmosfer olayı", "S", 1),
   ("Kırmızı sprite şimşekleri", "50–90 km", "P", "Bulutların çok üzerinde çakan kısa elektrik boşalmaları.", "Faraday kafesi +", "Gerçek üst atmosfer olayı", "S", 0),
   ("Kademe ayırma penceresi", "60–80 km", "I", "Boş kademeyi doğru anda atarsan ani ivme, geç kalırsan ölü ağırlık.", "Çok kademeli roket", None, "Y", 0),
   ("Gece parlayan bulutlar", "76–85 km", "Y", "Buz kristallerinden oluşan en yüksek bulutlar. Hafif fren, ama bilim puanı verir.", "—", "Dünya'nın en yüksek bulutları", "S", 1),
   ("Göktaşı izleri", "70–100 km", "Y", "Yanan küçük göktaşı parçaları gövdeyi döver.", "Whipple kalkanı", None, "Y", 0),
   ("Kármán hattı", "100 km", "I", "Uzayın başlangıcı. Sinematik an, bilim puanı ve ilk büyük ödül.", "—", "Uzayın uluslararası kabul gören sınırı", "Y", 0)]),
 ("3", "Yörünge", "100 – 36.000 km", 2.6,
  "Yukarı çıkmak yetmiyor. Saniyede 7,8 km yatay hıza ulaşmazsan düşersin. Oyuncu burada gerçek roket fiziğini keşfediyor.",
  [("Yerçekimi dönüşü", "100–200 km", "Y", "Dik çıkmakta ısrar edersen yörüngeye giremez, geri düşersin.", "Otopilot", "Gerçek fırlatmalarda roket yavaşça yatar", "Y", 0),
   ("Termosfer sürtünmesi", "100–400 km", "Y", "İnce ama etkili hava direnci.", "—", None, "Y", 0),
   ("Atomik oksijen", "200–600 km", "Y", "Tek atomlu oksijen gövde kaplamasını kemirir.", "Seramik kaplama", "Alçak yörüngede gerçek malzeme sorunu", "Y", 1),
   ("Aurora perdesi", "100–300 km", "S", "Manyetik alan pusulayı saptırır, ama geçiş bilim puanı kazandırır.", "Yıldız izleyici", None, "S", 0),
   ("Uzay istasyonu", "400 km", "I", "Yanaşabilirsen yakıt ikmali alırsın.", "Yanaşma sistemi", None, "Y", 0),
   ("Kayıp alet çantası", "400 km", "I", "Yakalarsan küçük bir bilim ödülü.", "Robot kol", "Bir astronot 2008'de uzay yürüyüşünde alet çantasını kaybetti", "N", 1),
   ("Uydu treni", "550 km", "S", "Sıra halinde ilerleyen yüzlerce küçük uydu. Aradan geçmek zamanlama ister.", "Otomatik kaçınma", None, "Y", 1),
   ("Güney Atlantik Anomalisi", "200–800 km", "S", "Radyasyonun yere en çok yaklaştığı bölge. Aviyonikte rastgele hatalar.", "Radyasyon zırhı", "Gerçek; uydular burada hata yapar", "S", 1),
   ("Uzay çöpü kuşağı", "600–1.000 km", "P", "Çarptığın her parça yeni parçalara bölünür ve tehlike zincirleme büyür.", "Whipple kalkanı", "Kessler sendromu", "Y", 0),
   ("Uydu karşıtı test enkazı", "Rastgele", "P", "Ani beliren yoğun enkaz bulutu.", "Uzay hava durumu uydusu", "2007 ve 2021'de gerçek testler binlerce parça bıraktı", "N", 1),
   ("Ölü uydu", "800 km", "I", "Robot kolla yakalarsan hurda kredisi verir.", "Robot kol", None, "S", 0),
   ("Van Allen iç kuşağı", "1.000+ km", "P", "Radyasyon aviyoniği sıfırlar.", "Radyasyon zırhı", "Gerçek radyasyon kuşağı", "Y", 0),
   ("Mezarlık yörüngesi", "36.000 km", "P", "Yer-durağan kuşağın hemen üstünde emekli uydular birikmiş.", "Engel radarı", "Gerçek; emekli uydular buraya itilir", "S", 1)]),
 ("4", "Ay", "384.400 km", 5.58,
  "İlk gerçek yolculuk. Yörüngeden kopma anını doğru zamanlamak ve Ay'ın yerçekimini kullanmak gerekiyor.",
  [("Ay'a atış zamanlaması", "Dünya yörüngesi", "I", "Motoru Dünya'ya en yakın noktada yakarsan çok daha fazla hız kazanırsın.", "Sapan hesaplayıcı", "Oberth etkisi", "Y", 0),
   ("Dünya'nın manyetik kuyruğu", "Ay yolu", "S", "Güneş rüzgârının arkaya doğru uzattığı manyetik alan. Yüklü toz roketi iter.", "Manyetik kalkan", "Ay her ay bu kuyruğun içinden geçer", "S", 1),
   ("L1 Lagrange noktası", "~326.000 km", "S", "Dengesiz bölge, roketi yavaşça sürükler.", "Hassas iticiler", None, "Y", 0),
   ("Ay sapanı", "Ay yakını", "I", "Doğru açıyla geçersen yakıt harcamadan büyük ivme, yanlışsa çarpma.", "Sapan hesaplayıcı", "Apollo 13 dönüşünde kullanıldı", "Y", 0),
   ("Masconlar", "Ay yörüngesi", "S", "Ay'ın düzensiz kütle yoğunlukları yörüngeyi bozar.", "Otopilot +", "Gerçek, Apollo'da keşfedildi", "Y", 0),
   ("Apollo hurdası", "Ay yörüngesi", "I", "Eski Saturn V kademeleri. Bulursan koleksiyon ve bilim ödülü.", "Robot kol", "Gerçek; bazıları hâlâ yörüngede", "N", 1),
   ("Ay gecesi", "Ay yüzeyi", "Y", "−173 °C. Bataryalar donar, güç düşer.", "RTG", "Gerçek; 14 gün sürer", "Y", 1),
   ("Regolit tozu", "İniş", "Y", "İnişte kalkan toz görüşü kapatır.", "LIDAR", None, "Y", 0),
   ("Ay depremi", "İniş", "P", "İniş anında yüzey sarsılır, bacaklar kırılabilir.", "Esnek iniş bacakları", "Apollo sismometreleri kaydetti", "S", 1),
   ("Shackleton krateri buzu", "Güney kutbu", "I", "Hiç güneş görmeyen kraterde su buzu. Yakıta dönüşür.", "Madenci drone", "Gerçek; Artemis'in hedef bölgesi", "S", 1),
   ("Ay Üssü", "Ödül", "I", "Kurulunca sonraki uçuşlar Ay'dan başlayabilir.", "—", None, "Y", 0)]),
 ("5", "Mars Yolu", "~78 milyon km", 7.89,
  "Güneş artık bir oyuncu (aşağıdaki Güneş bölümüne bak). Mars'a varınca atmosfere doğru açıyla girmek gerekiyor.",
  [("Mikrometeoroid yağmuru", "Yol boyu", "Y", "Küçük ama sürekli çarpışmalar.", "Whipple kalkanı", None, "Y", 0),
   ("Kozmik ışın sağanağı", "Yol boyu", "S", "Galaksi dışından gelen parçacıklar bellekte bit hatası yapar, kontrol anlık şaşar.", "Radyasyon zırhı", "Gerçek; derin uzay elektroniğinin baş belası", "S", 1),
   ("Phobos", "Mars yakını", "I", "Küçük ama kullanışlı bir sapan.", "—", None, "Y", 0),
   ("Atmosfer frenlemesi", "Mars atmosferi", "Y", "Dik girersen yanarsın, sığ girersen sekip uzaya kaçarsın. Doğru açı yakıtsız yavaşlatır.", "Ablatif ısı kalkanı", "Gerçek iniş tekniği", "Y", 0),
   ("İnce atmosfer", "İniş", "Y", "Paraşüt tek başına yetmez, son metrelerde motorla frenlemek gerekir.", "Süpersonik retro motor", "Gerçek; Mars inişlerinin en zor kısmı", "Y", 1),
   ("Toz fırtınası", "Mars yüzeyi", "S", "Görüşü ve güneş enerjisini keser.", "RTG", None, "S", 0),
   ("Toz şeytanları", "Mars yüzeyi", "I", "Küçük hortumlar güneş panellerinin tozunu temizler, enerji geri gelir.", "—", "Spirit gezgininin panellerini gerçekten temizlediler", "S", 1),
   ("Olympus Mons", "İniş bölgesi", "P", "22 km yüksekliğindeki dağ. Yanlış rotada iniş yamaca çarpar.", "LIDAR", "Güneş sisteminin en yüksek dağı", "Y", 1),
   ("Mars yakıt fabrikası", "Ödül", "I", "Atmosferdeki karbondioksitten metan üretir. Yeni checkpoint.", "—", None, "Y", 0)]),
 ("6", "Asteroit Kuşağı", "~300 milyon km", 8.48,
  "Oyunun 'kaçış' bölümü. Ama kuşağın içinde Jüpiter'in açtığı gizli otoyollar var.",
  [("Çarpışma kümesi", "Kuşak içi", "P", "Yoğun ve dönen kaya alanı.", "Otomatik kaçınma", None, "Y", 0),
   ("Kirkwood boşlukları", "Kuşak içi", "I", "Jüpiter'in kütle çekiminin asteroitleri süpürdüğü güvenli koridorlar.", "Zincir planlayıcı", "Gerçek; Jüpiter rezonansıyla oluşur", "Y", 1),
   ("Moloz yığını asteroit", "Kuşak içi", "P", "Katı sanılan asteroit aslında gevşek çakıl. Yanaşırsan içine batarsın.", "LIDAR", "OSIRIS-REx 2020'de Bennu'ya dokununca neredeyse içine battı", "S", 1),
   ("Madenlik asteroit", "Kuşak içi", "I", "Yanaşıp kazarsan nadir metal kazanırsın.", "Madenci drone", None, "Y", 0),
   ("Psyche metal asteroit", "Dış kuşak", "I", "Neredeyse tamamen metal. Tek seferde dev kredi.", "Madenci drone", "Gerçek; NASA'nın Psyche sondası yolda", "N", 1),
   ("Kuyruklu yıldız geçişi", "Rastgele", "S", "İyon kuyruğu iter, toz bulutu gövdeyi aşındırır. Kuyruklu yıldız sörfünün de kapısı.", "Aerojel toplayıcı", None, "S", 1),
   ("Ceres sapanı", "Ceres", "I", "Orta büyüklükte ivme.", "—", None, "Y", 0)]),
 ("7", "Jüpiter", "~630 milyon km", 8.8,
  "Hem en büyük ödül hem en büyük tehlike: oyunun en güçlü sapanı ile en ölümcül radyasyonu bir arada.",
  [("Truva asteroitleri", "Jüpiter'in L4/L5'i", "P", "Jüpiter'le aynı yörüngede önde ve arkada giden iki asteroit sürüsü.", "Otomatik kaçınma", "Gerçek; Lucy sondası inceliyor", "Y", 1),
   ("Jüpiter sapanı", "Jüpiter yakını", "I", "Oyundaki en büyük gezegen ivmesi.", "Sapan hesaplayıcı", "Voyager ve New Horizons kullandı", "Y", 0),
   ("Radyasyon kuşakları", "Jüpiter yakını", "P", "Güneş sistemindeki en sert radyasyon.", "Manyetik kalkan", None, "Y", 0),
   ("Büyük Kırmızı Leke", "Jüpiter atmosferi", "S", "Dünya'dan büyük bir fırtına. Yaklaşırsan seni içine çeker.", "—", "Yüzyıllardır süren gerçek fırtına", "Y", 1),
   ("Laplace rezonans zinciri", "Io–Europa–Ganymede", "I", "Üç uydu 1:2:4 ritmiyle dönüyor. Doğru anda üçünden art arda sapan yaparsan dev kombo ivme.", "Zincir planlayıcı", "Gerçek yörünge rezonansı", "N", 1),
   ("Io plazma halkası", "Io yörüngesi", "I", "Elektrodinamik ipin varsa elektrik üretir.", "Elektrodinamik ip", None, "S", 0),
   ("Europa buz tozları", "Europa", "I", "Yüzeyden kopan buz. Buhar roketinin yakıtı.", "Madenci drone", None, "Y", 1),
   ("Kuyruklu yıldız parçaları", "Jüpiter yakını", "P", "Jüpiter'e düşen parçalanmış kuyruklu yıldız zinciri.", "Otomatik kaçınma", "Shoemaker–Levy 9, 1994", "N", 1),
   ("Güneş enerjisi sınırı", "Jüpiter ötesi", "Y", "Güneş panelleri artık yetmez, nükleer enerji gerekir.", "RTG", "Gerçek; dış gezegen sondaları RTG kullanır", "Y", 0)]),
 ("8", "Satürn", "~1,3 milyar km", 9.11,
  "Görsel olarak oyunun zirvesi: halkaların arasından geçiş.",
  [("Halka geçişi", "Halka boşluğu", "P", "Buz parçalarının arasından dar bir koridor.", "Otomatik kaçınma", "Cassini 2017'de bu boşluktan 22 kez geçti", "Y", 0),
   ("Çoban uydular", "Halka içi", "I", "Pan ve Daphnis halkalarda temiz boşluklar açar. Onları takip eden güvenli geçer.", "Zincir planlayıcı", "Gerçek; halkalardaki dalgaları onlar yapar", "S", 1),
   ("Halka yağmuru", "Halka altı", "Y", "Halkalardan gezegene buz parçacıkları yağar, hafif fren.", "—", "Gerçek; Cassini ölçtü", "Y", 1),
   ("Halka parmakları", "Halka üstü", "S", "Elektrostatik toz şeritleri aviyoniği şaşırtır.", "Faraday kafesi +", "Halkalardaki gizemli 'spoke'lar", "S", 1),
   ("Kutup altıgeni", "Kuzey kutbu", "S", "Altıgen biçimli dev jet akımı. Kenarından girersen savrulursun.", "—", "Gerçek; Voyager keşfetti", "S", 1),
   ("Hyperion", "Dış yörünge", "P", "Kaotik dönen, sünger gibi uydu. Yanaşmak neredeyse imkânsız.", "Otomatik kaçınma", "Dönüşü gerçekten öngörülemez", "S", 1),
   ("Titan", "Titan", "Y", "Kalın atmosfer frenler, metan gölleri yakıt verir.", "Ablatif ısı kalkanı", None, "Y", 0),
   ("Enceladus gayzerleri", "Enceladus", "S", "Buz püskürtüleri iter; içinden geçmek su toplar.", "—", None, "Y", 0)]),
 ("9", "Uranüs, Neptün ve Kuiper", "2,7 – 4,5 milyar km", 9.55,
  "Karanlık, soğuk ve sessiz. Güneş ışığı artık işe yaramıyor, sensörlerle uçmak gerekiyor.",
  [("Güneş ışığının sönüşü", "Uranüs ötesi", "Y", "Güneş yelkeni ve paneller neredeyse sıfıra düşer. Yalnızca nükleer güç.", "RTG / füzyon", "Işık, uzaklığın karesiyle azalır", "Y", 1),
   ("Yan yatık Uranüs", "Uranüs", "S", "98° eğik dönen gezegen. Sapan açıları alışılmadık.", "Sapan hesaplayıcı", "Gerçek; yan yatmış döner", "Y", 1),
   ("Karanlık halkalar", "Uranüs", "P", "Kömür kadar koyu halkalar, gözle görünmez.", "LIDAR", "Gerçek; 1977'de keşfedildi", "Y", 1),
   ("Neptün rüzgârları", "Neptün atmosferi", "S", "Saatte 2.000 km'yi aşan, Güneş sisteminin en hızlı rüzgârları.", "—", None, "Y", 0),
   ("Büyük Karanlık Leke", "Neptün", "S", "Gelip giden dev fırtına girdabı.", "—", "Voyager 2 gördü, sonra kayboldu", "S", 1),
   ("Triton gayzerleri", "Triton", "S", "Azot püskürtüleri.", "—", None, "Y", 0),
   ("Karanlık Kuiper nesneleri", "Kuiper kuşağı", "P", "Görünmez buz kayaları. Radar olmadan kör uçarsın.", "LIDAR", None, "Y", 0),
   ("Arrokoth", "Kuiper kuşağı", "I", "Kardan adam biçimli ilkel cisim. Fotoğrafı büyük bilim ödülü.", "—", "New Horizons 2019'da yanından geçti", "N", 1)]),
 ("10", "Plüton: Zafer", "~5,9 milyar km", 9.77,
  "Plüton ve Charon birbirinin etrafında dans ediyor. Hedef, Plüton'un kalp şeklindeki ovasına inmek.",
  [("Plüton–Charon ikilisi", "Plüton sistemi", "S", "İki yerçekimi merkezi aynı anda çeker.", "Sapan hesaplayıcı", None, "Y", 0),
   ("Nix ve Hydra", "Plüton sistemi", "P", "Kaotik takla atan küçük uydular.", "Otomatik kaçınma", "Gerçek; dönüşleri kaotik", "S", 1),
   ("Mavi pus", "Plüton atmosferi", "Y", "İnce mavi atmosfer, hafif aerofren.", "—", "New Horizons'ın en şaşırtıcı fotoğraflarından", "Y", 1),
   ("Buz dağları", "İniş yaklaşımı", "P", "6 km yüksekliğinde su buzu dağları.", "LIDAR", "Tenzing Montes", "Y", 1),
   ("Tombaugh Regio'ya iniş", "Final", "I", "Kalp şeklindeki azot buzu ovası. Buz hücreleri yavaşça kayar, iniş anı zamanlama ister. Zafer sinematiği.", "—", "New Horizons 2015'te fotoğrafladı", "Y", 0)]),
]

# Güneş: üç yüz
sun = [
 ("Yok edici", "fx-p", "Her zaman var", [
   ("Erime sınırı", "Kalkanla bile belli bir mesafeden fazla yaklaşırsan erirsin. Sınır, kalkan kademesine göre içeri doğru kayar."),
   ("Güneş patlaması", "X-ışını parlaması ışık hızında gelir: uyarı yok, aviyonik birkaç saniye kör kalır."),
   ("Koronal kütle atımı (CME)", "Dakikalar önce uyarı veren dev plazma dalgası. Kalkansızsan ölümcül."),
 ]),
 ("Yavaşlatıcı", "fx-y", "Sürekli ve sinsi", [
   ("Yerçekimi kuyusu", "Dış gezegenlere giderken Güneş seni sürekli geri çeker. Dış güneş sisteminin asıl zorluğu yakıt değil bu kuyudan tırmanmak."),
   ("Ters rüzgâr", "Güneş'e doğru giderken güneş rüzgârı ve ışık basıncı karşıdan eser; yelkenin yanlış açıdaysa fren olur."),
   ("Isı birikimi", "Yakın geçişte motorlar aşırı ısınır ve gücü kısılır. Radyatör yoksa ateşleme süresi kısalır."),
 ]),
 ("Mükemmel hızlandırıcı", "fx-i", "Nadir ve riskli", [
   ("Güneş Oberth dalışı", "Önce Güneş'e doğru düşersin. En yakın noktada hızın zirvedeyken motoru ateşlersen kazandığın hız katlanır. 3 saniyelik kusursuz ateşleme penceresi var; kaçırırsan erirsin ya da boşa geçer. Oyundaki en büyük ivme."),
   ("Koronal delik akımı", "Güneş yüzeyindeki 'deliklerden' saniyede 800 km'lik hızlı rüzgâr çıkar. Yelkeninle yakalarsan dakikalarca itilirsin. Uzay hava durumu tahmininde görünür."),
   ("Plazma sörfü", "CME dalgasının önüne plazma emici kalkanla girersen en büyük tehdit en büyük itkiye dönüşür."),
 ]),
]

# Yörünge mekaniği fırsatları
orbits = [
 ("Sapanın yönü", "I", "Gezegenin hareket yönünün arkasından geçersen hızlanırsın, önünden geçersen yavaşlarsın. Aynı gezegen bir uçuşta itki, başka uçuşta fren olur.", "MESSENGER, Merkür'e varabilmek için 6 sapanla yavaşladı"),
 ("Fırlatma pencereleri", "I", "Mars'a giden en ucuz yol 26 ayda bir açılır. Hangarda pencere sayacı olur; pencerede kalkan roket çok daha az yakıt harcar.", "Hohmann transferi"),
 ("Büyük Tur hizalanması", "I", "Dış gezegenler aynı tarafa dizildiğinde Jüpiter–Satürn–Uranüs–Neptün sapanları zincirlenebilir. Nadir olay; çıktığında Plüton'a giden en hızlı yol.", "175 yılda bir; Voyager 2 kullandı"),
 ("Lagrange otoyolları", "I", "Gezegenlerin denge noktalarını birbirine bağlayan, neredeyse yakıtsız ama yavaş kanallar. Oyunda ince ışıklı tüpler olarak görünür.", "Gezegenlerarası Ulaşım Ağı"),
 ("Rezonans kombosu", "I", "Io–Europa–Ganymede gibi ritmik dönen uydu zincirlerinde art arda sapan. Doğru ritimde her sapan bir öncekini büyütür.", "Laplace rezonansı"),
 ("Atmosfer yakalaması", "Y", "Hedef gezegene varınca motor yerine atmosferle frenleyip yörüngeye girmek. Yakıt tasarrufu büyük, hata payı küçük.", "Aerocapture kavramı"),
]

tree = [
 ("İtki", ["Kerosen motor", "Aerospike nozul", "Metan motor (yeniden ateşleme)", "Hava soluyan motor", "Nükleer termal motor", "Füzyon motoru"],
  "Hava soluyan motor atmosferde oksijeni havadan alır, ilk bölümlerde yakıtı ikiye katlar. Gerçek: SABRE motoru."),
 ("Uzun yol sürüşü", ["Güneş yelkeni", "İyon motoru", "Elektrik yelken", "Manyetik yelken", "Güneş termal roketi", "Buhar roketi"],
  "Buhar roketi Europa, Enceladus veya Kuiper buzuyla çalışır; madenci drone'la birlikte her yerde yakıt ikmali demek."),
 ("Gövde ve kalkan", ["Karbon kompozit", "Ablatif ısı kalkanı", "Whipple kalkanı", "Kendini onaran gövde", "Güneş dalış kalkanı", "Manyetik radyasyon kalkanı"],
  "Güneş dalış kalkanı Parker Solar Probe'unkine benzer karbon köpük bir kalkan; Güneş Oberth dalışını açar."),
 ("Aviyonik", ["Yerçekimi dönüşü otopilotu", "Engel radarı", "Otomatik kaçınma", "Sapan hesaplayıcı", "Zincir planlayıcı", "Uzay hava durumu uydusu"],
  "Zincir planlayıcı birden fazla sapanı ve rezonans kombolarını hayalet rota olarak önceden çizer."),
 ("Enerji", ["Batarya", "Güneş paneli", "Yakıt hücresi", "Isı radyatörleri", "RTG (nükleer pil)", "Kompakt füzyon"],
  "Isı radyatörleri Güneş yakınında motoru soğutur. Jüpiter'den sonra güneş paneli yetmez; RTG doğal bir ilerleme kapısı."),
 ("Lojistik", ["İki kademe", "Balonla kalkış", "Üç kademe ve booster dönüşü", "Yörünge yakıt deposu", "Ay Üssü", "Mars yakıt fabrikası"],
  "Balonla kalkış roketi 30 km'ye kadar balonla taşıyıp oradan ateşler; troposfer engellerini tamamen atlar. Gerçek: 1950'lerin 'rockoon'ları."),
]

side = [
 ("Eskort drone", "Roketin önünde uçar, kuşları ve balonları dağıtır. Sınırlı şarjı var.", 0),
 ("Kurtarma kapsülü", "Patlamadan hemen önce fırlatılırsa o uçuşta kazanılanların yarısını kurtarır.", 0),
 ("Keşif sondası", "Önden gider, 30 saniye boyunca yaklaşan engelleri haritada gösterir.", 0),
 ("Booster dönüşü", "Ayrılan kademe Dünya'ya geri iner. Mini oyunu başarırsan kredinin bir kısmı geri gelir.", 0),
 ("Robot kol", "Ölü uyduları, Apollo hurdasını ve uzay çöpünü yakalar.", 0),
 ("Madenci drone", "Asteroitten metal, Europa'dan buz, Titan'dan metan toplar.", 0),
 ("Gölge drone", "Güneş dalışında roketin önünde uçup gölge yapar. Erime sınırını biraz daha içeri iter, ama kendisi erir.", 1),
 ("Aerojel toplayıcı", "Kuyruklu yıldız kuyruğundan toz yakalar; nadir bilim puanı. Gerçek: Stardust sondası.", 1),
 ("Uzay römorkörü", "Yörüngedeki yakıt deposundan sana tank getirir, ya da seni yakalayıp istenen yörüngeye çeker.", 1),
 ("Lazer temizleyici", "Dünya'dan ateşlenen lazer, rotandaki uzay çöpünü yörüngeden düşürür.", 1),
]

legend = [
 ("Skyhook", "Dünya yörüngesinde dönen dev bir halat roketi yakalar ve sapan gibi fırlatır.", "Ciddi olarak çalışılmış bir mühendislik kavramı", 0),
 ("Lazer yelken", "Dünya'daki dev bir lazer dizisi yelkeni iter. Ekranda Dünya'dan gelen ışık sütunu görünür.", "Breakthrough Starshot projesi, 2016", 0),
 ("Orion darbesi", "Roketin arkasında küçük nükleer patlamalar art arda itki verir. Oyunun en çarpıcı efekti.", "Orion Projesi, 1958–1965", 0),
 ("Plazma emici kalkan", "Güneş fırtınasının enerjisini emip ivmeye çevirir. En büyük tehdit ödüle dönüşür.", "Kurgusal, oyun için", 0),
 ("Merkür ayna dizisi", "Merkür yörüngesindeki ayna filosu Güneş ışığını yelkenine odaklar. Uranüs ötesinde bile yelken çalışır.", "Robert Forward'ın odaklı ışık yelkeni fikrinden türetildi", 1),
 ("Kuyruklu yıldız sörfü", "Zıpkınla bir kuyruklu yıldıza tutun ve onunla birlikte Güneş'in etrafından fırla. Güneş dalışını kalkansız yapmanın tek yolu.", "Philae iniş aracında gerçek zıpkın vardı (2014)", 1),
 ("Ay kütle sürücüsü", "Ay Üssü'nden elektromanyetik rayla fırlatma. Yakıt harcamadan derin uzaya çıkış.", "Gerard O'Neill, 1970'ler", 0),
 ("Uzay asansörü", "Son aşama: Dünya'dan kalkışı tamamen atlar, Plüton denemelerini hızlandırır.", "Kavram; malzeme henüz yok", 0),
]

market = [
 ("Into Space 1–3", "Tarayıcı / mobil", "Roketle yukarı çık, düş, geliştir, tekrar dene.", "Tam bizim döngümüz, ama 2B, düz grafikli ve tekrara düşüyor."),
 ("Learn to Fly serisi", "Tarayıcı / Steam", "Penguen fırlat, mesafeye göre para kazan, ekipman al.", "Geliştirmelerin birbirini tamamlaması güzel; görsel olarak çocuksu."),
 ("Earn to Die", "Mobil", "Araçla zombi kalabalığını yararak ilerle, her turdan sonra güçlendir.", "Mükemmel ilerleme ritmi: aracı doyur, sonrakine geç."),
 ("Burrito Bison", "Tarayıcı / mobil", "Fırlatma, zıplama ve sürekli hız kazandıran objeler.", "İvme veren objelerin verdiği haz, bizim 'itki' fikrinin aynısı."),
 ("Kerbal Space Program", "PC", "Gerçek yörünge fiziğiyle roket tasarla ve uçur.", "Steam'de %95 olumlu, ~5 milyon satış. Fizik muhteşem, öğrenmesi zor."),
 ("Kerbal Space Program 2", "PC", "İlk oyunun devamı.", "Steam'de %27 olumlu. Ders: kapsamı aşırı büyütmek oyunu batırır."),
 ("Spaceflight Simulator", "Mobil / PC", "Telefonda parça parça roket inşası.", "Mobilde gerçekçi uzay oyunu talebi olduğunu gösteriyor."),
]

def fxchip(c): l, cls = FX[c]; return f'<span class="chip {cls}">{l}</span>'
def newtag(n): return '<span class="new">yeni</span>' if n else ''

n_obs = sum(len(c[5]) for c in chapters); n_new = sum(o[7] for c in chapters for o in c[5])
n_upg = sum(len(t[1]) for t in tree)

out = []
out.append('''<title>Son Durak: Plüton</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Saira+Condensed:wght@500;700;800&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Düzen: tek sütun görev dosyası; üstte logaritmik rota şeridi, altta bölüm bölüm engel kartları. Tek tema: derin uzay. */
:root{
  --void:#0a0f1d; --panel:#111a2e; --panel2:#16213a; --line:#24324f;
  --star:#e9eef8; --dim:#93a1bd; --faint:#5f6f8f;
  --flame:#ff9a3c; --ion:#55d6c2; --danger:#ff5d6c; --slow:#f2c14e; --drift:#a993ff; --sun:#ffd27a;
  --f-display:"Saira Condensed","Arial Narrow",system-ui,sans-serif;
  --f-body:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
  --f-mono:"IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;
  color-scheme:dark;
}
html{background:var(--void)}
body{background:var(--void);color:var(--star);font-family:var(--f-body);font-size:15.5px;line-height:1.6;padding-inline:16px;padding-block:0 64px}
.wrap{max-width:760px;margin:0 auto}
h1,h2,h3{font-family:var(--f-display);text-wrap:balance;margin:0;letter-spacing:.01em}
h1{font-size:clamp(2.6rem,9vw,4.2rem);line-height:.95;font-weight:800;text-transform:uppercase}
h1 em{font-style:normal;color:var(--flame)}
h2{font-size:1.9rem;font-weight:700;text-transform:uppercase;line-height:1.05}
h3{font-size:1.3rem;font-weight:700}
p{margin:0}
.eyebrow{font-family:var(--f-mono);font-size:.74rem;letter-spacing:.14em;text-transform:uppercase;color:var(--dim)}
.lead{color:var(--dim);font-size:1.05rem;max-width:62ch}
section{display:flex;flex-direction:column;gap:18px;padding-block:44px 0}
.hero{padding-block:40px 8px;display:flex;flex-direction:column;gap:16px;position:relative}
.hero canvas{position:absolute;inset:0;width:100%;height:100%;z-index:0;pointer-events:none;opacity:.8}
.hero > *:not(canvas){position:relative;z-index:1}
.pitch{border-left:2px solid var(--flame);padding-left:14px;font-size:1.08rem;max-width:60ch}
.loop{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}
.loop div{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:10px;display:flex;flex-direction:column;gap:2px;min-width:0}
.loop b{font-family:var(--f-display);font-size:1.15rem;text-transform:uppercase}
.loop span{color:var(--dim);font-size:.82rem;line-height:1.4}
@media (max-width:520px){.loop{grid-template-columns:repeat(2,minmax(0,1fr))}}
.changes{background:var(--panel2);border:1px solid var(--line);border-radius:8px;padding:14px 16px;display:flex;flex-direction:column;gap:8px}
.changes ul{margin:0;padding-left:1.1em;display:flex;flex-direction:column;gap:4px;color:var(--dim);font-size:.93rem}
.changes b{color:var(--star)}
.stats{display:flex;flex-wrap:wrap;gap:6px 18px;font-family:var(--f-mono);font-size:.8rem;color:var(--dim);font-variant-numeric:tabular-nums}
.stats b{color:var(--flame);font-weight:500}
.route{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:16px 12px 12px}
.route svg,.diagram svg{width:100%;height:auto;display:block}
.route .cap{color:var(--faint);font-size:.8rem;margin-top:6px}
.mk{display:flex;flex-direction:column;border-top:1px solid var(--line)}
.mk > div{display:grid;grid-template-columns:minmax(0,11rem) minmax(0,1fr);gap:4px 16px;padding:12px 0;border-bottom:1px solid var(--line)}
.mk b{font-family:var(--f-display);font-size:1.12rem}
.mk .plat{font-family:var(--f-mono);font-size:.72rem;color:var(--faint);display:block}
.mk .what{color:var(--dim)}
.mk .take{grid-column:2}
@media (max-width:520px){.mk > div{grid-template-columns:1fr}.mk .take{grid-column:1}}
.pos{background:var(--panel2);border:1px solid var(--line);border-radius:8px;padding:16px;display:flex;flex-direction:column;gap:10px}
.pos ul{margin:0;padding-left:1.1em;display:flex;flex-direction:column;gap:6px}
.legend{display:flex;flex-wrap:wrap;gap:6px}
.chip{display:inline-block;font-family:var(--f-mono);font-size:.7rem;letter-spacing:.06em;text-transform:uppercase;padding:2px 7px;border-radius:3px;border:1px solid currentColor;white-space:nowrap}
.fx-p{color:var(--danger)} .fx-y{color:var(--slow)} .fx-s{color:var(--drift)} .fx-i{color:var(--ion)}
.fq{font-family:var(--f-mono);font-size:.68rem;color:var(--faint);letter-spacing:.05em;text-transform:uppercase}
.fq.N{color:var(--sun)}
.new{font-family:var(--f-mono);font-size:.62rem;letter-spacing:.08em;text-transform:uppercase;color:var(--void);background:var(--ion);border-radius:3px;padding:1px 5px;margin-left:6px;vertical-align:2px}
/* güneş */
.sun{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
@media (max-width:640px){.sun{grid-template-columns:1fr}}
.face{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:14px;display:flex;flex-direction:column;gap:10px;min-width:0}
.face h3{display:flex;flex-direction:column;gap:2px}
.face h3 small{font-family:var(--f-mono);font-size:.7rem;font-weight:400;letter-spacing:.08em;text-transform:uppercase;color:var(--faint)}
.face.fx-p h3{color:var(--danger)} .face.fx-y h3{color:var(--slow)} .face.fx-i h3{color:var(--ion)}
.face.fx-i{border-color:#2b5a57;background:linear-gradient(170deg,#132a33,var(--panel))}
.face div{display:flex;flex-direction:column;gap:2px}
.face b{color:var(--star);font-size:.95rem}
.face p{color:var(--dim);font-size:.88rem;line-height:1.5}
.weather{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}
@media (max-width:520px){.weather{grid-template-columns:1fr}}
.weather div{border:1px solid var(--line);border-radius:6px;padding:10px 12px;display:flex;flex-direction:column;gap:2px}
.weather b{font-family:var(--f-display);font-size:1.1rem}
.weather p{color:var(--dim);font-size:.85rem;line-height:1.45}
.diagram{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:12px}
.orb{display:flex;flex-direction:column;gap:8px}
.orb > div{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px 12px;border-bottom:1px solid var(--line);padding:10px 0}
.orb b{font-weight:600}
.orb p{grid-column:1 / -1;color:var(--dim);font-size:.92rem}
.orb small{grid-column:1 / -1;color:var(--flame);font-size:.8rem}
/* bölümler */
.ch{border-top:1px solid var(--line);padding-top:22px;display:flex;flex-direction:column;gap:12px}
.ch-head{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
.ch-no{font-family:var(--f-mono);color:var(--flame);font-size:.85rem}
.ch-dist{font-family:var(--f-mono);font-size:.78rem;color:var(--dim);margin-left:auto;font-variant-numeric:tabular-nums}
.ch > p{color:var(--dim)}
.obs{display:flex;flex-direction:column;gap:8px}
.ob{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px 12px;background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:11px 12px}
.ob .nm{font-weight:600}
.ob .at{font-family:var(--f-mono);font-size:.74rem;color:var(--faint);font-variant-numeric:tabular-nums}
.ob .side{display:flex;flex-direction:column;align-items:flex-end;gap:4px}
.ob .ds{grid-column:1 / -1;color:var(--dim);font-size:.92rem;line-height:1.5}
.ob .ct{grid-column:1 / -1;font-size:.84rem;display:flex;flex-wrap:wrap;gap:4px 14px}
.ob .ct span{color:var(--faint)}
.ob .ct i{font-style:normal;color:var(--star)}
.ob .real{color:var(--flame);font-size:.8rem}
/* denge */
.bal{display:flex;flex-direction:column;gap:7px}
.bal > div{display:grid;grid-template-columns:7.5rem minmax(0,1fr) 2rem;gap:10px;align-items:center;font-size:.85rem}
.bal .lbl{color:var(--dim);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bal .bar{display:flex;height:12px;border-radius:2px;overflow:hidden;background:var(--panel)}
.bal .bar span{display:block;height:100%}
.bal .n{font-family:var(--f-mono);color:var(--faint);text-align:right;font-variant-numeric:tabular-nums}
.b-p{background:var(--danger)} .b-y{background:var(--slow)} .b-s{background:var(--drift)} .b-i{background:var(--ion)}
.rules{margin:0;padding-left:1.1em;color:var(--dim);display:flex;flex-direction:column;gap:6px;font-size:.93rem}
.rules b{color:var(--star)}
/* ağaç */
.tree{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));gap:10px}
.br{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:14px;display:flex;flex-direction:column;gap:10px;min-width:0}
.br ol{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:5px;counter-reset:t}
.br li{counter-increment:t;display:flex;gap:8px;font-size:.93rem}
.br li::before{content:counter(t);font-family:var(--f-mono);font-size:.72rem;color:var(--flame);border:1px solid var(--line);border-radius:3px;min-width:1.4rem;text-align:center;line-height:1.5rem;height:1.5rem}
.br p{color:var(--faint);font-size:.82rem;line-height:1.45}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));gap:10px}
.cards > div{border:1px solid var(--line);border-radius:8px;padding:13px;display:flex;flex-direction:column;gap:4px;min-width:0}
.cards b{font-family:var(--f-display);font-size:1.18rem}
.cards p{color:var(--dim);font-size:.9rem;line-height:1.5}
.cards small{color:var(--flame);font-size:.78rem}
.legendary > div{background:linear-gradient(160deg,var(--panel2),var(--void));border-color:#3a3156}
.legendary b{color:var(--flame)}
.ms{display:flex;flex-direction:column;border-left:1px solid var(--line);margin-left:6px}
.ms > div{position:relative;padding:0 0 18px 20px;display:flex;flex-direction:column;gap:3px}
.ms > div::before{content:"";position:absolute;left:-5px;top:7px;width:9px;height:9px;border-radius:50%;background:var(--void);border:2px solid var(--flame)}
.ms > div:first-child::before{background:var(--flame)}
.ms b{font-family:var(--f-display);font-size:1.2rem}
.ms p{color:var(--dim);font-size:.93rem}
.qs{display:flex;flex-direction:column;gap:10px}
.qs > div{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:13px 14px;display:flex;flex-direction:column;gap:4px}
.qs b{font-weight:600}
.qs p{color:var(--dim);font-size:.92rem}
.note{color:var(--dim);font-size:.92rem;max-width:62ch}
.src{font-size:.82rem;color:var(--faint);display:flex;flex-direction:column;gap:3px}
.src a{color:var(--dim)}
a:focus-visible{outline:2px solid var(--flame);outline-offset:2px}
@media (prefers-reduced-motion:reduce){.hero canvas{display:none}}
</style>
<div class="wrap">
<header class="hero">
<canvas id="sky" aria-hidden="true"></canvas>
<p class="eyebrow">Oyun tasarım belgesi · Taslak 2 · Tartışma için</p>
<h1>Son Durak:<br><em>Plüton</em></h1>
<p class="pitch">Dünya'dan kalkan bir roket her denemede biraz daha uzağa gidiyor. Önce atmosfer, sonra yörünge, Ay, Mars ve sonunda Plüton. Her patlamadan sonra hangarda geliştirme yapıyor, bir sonraki denemede bir önceki seni öldüren engeli aşıyorsun.</p>
<div class="loop">
<div><b>Kalk</b><span>Gazı ve rotayı yönet</span></div>
<div><b>Düş</b><span>Kara kutu raporu: neden patladın?</span></div>
<div><b>Geliştir</b><span>6 dal, ''' + str(n_upg) + ''' geliştirme, yan araçlar</span></div>
<div><b>Uzağa</b><span>Üs kur, oradan devam et</span></div>
</div>
''')
out.append(f'''<div class="changes"><p class="eyebrow">Taslak 2'de neler değişti</p><ul>
<li><b>Güneş artık bir oyuncu:</b> yok edici, yavaşlatıcı ve nadiren mükemmel hızlandırıcı. Her uçuş bir uzay hava durumu tahminiyle başlıyor.</li>
<li><b>Gezegen yörüngeleri:</b> sapanın yönüne göre hızlandırma ya da frenleme, fırlatma pencereleri, Büyük Tur hizalanması, Lagrange otoyolları, rezonans kombosu.</li>
<li><b>{n_new} yeni engel ve fırsat</b>, her biri kendi ortamına özgü: volkanik kül, uydu treni, Ay depremi, toz şeytanları, Kirkwood boşlukları, çoban uydular…</li>
<li><b>Geliştirmeler 25'ten {n_upg}'ya çıktı;</b> yeni bir dal (uzun yol sürüşü), 4 yeni yan araç ve 2 yeni efsanevi geliştirme eklendi.</li>
<li><b>Denge tablosu:</b> her bölümdeki engel türlerinin dağılımı ve sıklık (yaygın / seyrek / nadir).</li>
</ul><div class="stats"><span><b>{n_obs}</b> engel ve fırsat</span><span><b>{n_upg}</b> geliştirme</span><span><b>{len(side)}</b> yan araç</span><span><b>{len(legend)}</b> efsanevi</span></div></div>
</header>
''')

# rota şeridi
W, H = 720, 210
x0, x1 = 40, 700
def X(v): return x0 + (v - 1) / 9 * (x1 - x0)
svg = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Dünya\'dan Plüton\'a logaritmik rota">']
svg.append(f'<line x1="{x0}" y1="110" x2="{x1}" y2="110" stroke="#24324f" stroke-width="2"/>')
for k in range(1, 11):
    svg.append(f'<line x1="{X(k):.1f}" y1="104" x2="{X(k):.1f}" y2="116" stroke="#5f6f8f" stroke-width="1"/>')
    lab = {1:"10 km",2:"100 km",3:"1.000",4:"10⁴",5:"10⁵",6:"1 mn km",7:"10⁷",8:"10⁸",9:"1 mr km",10:"10¹⁰"}[k]
    svg.append(f'<text x="{X(k):.1f}" y="134" fill="#5f6f8f" font-family="IBM Plex Mono,monospace" font-size="11" text-anchor="middle">{lab}</text>')
names = {"1":"Troposfer","2":"Kármán","3":"Yörünge","4":"Ay","5":"Mars","6":"Kuşak","7":"Jüpiter","8":"Satürn","9":"Neptün","10":"Plüton"}
for i, ch in enumerate(chapters):
    no, lg = ch[0], ch[3]
    up = i % 2 == 0
    y = 74 if up else 160
    col = "#ff9a3c" if no == "10" else "#55d6c2"
    svg.append(f'<line x1="{X(lg):.1f}" y1="110" x2="{X(lg):.1f}" y2="{86 if up else 146}" stroke="{col}" stroke-width="1" stroke-dasharray="2 3"/>')
    svg.append(f'<circle cx="{X(lg):.1f}" cy="110" r="{6 if no=="10" else 4.5}" fill="{col}"/>')
    anchor = "end" if lg > 9.6 else ("start" if lg < 1.5 else "middle")
    svg.append(f'<text x="{X(lg):.1f}" y="{y}" fill="#e9eef8" font-family="Saira Condensed,Arial Narrow,sans-serif" font-size="15" font-weight="700" text-anchor="{anchor}">{E(names[no])}</text>')
    svg.append(f'<text x="{X(lg):.1f}" y="{y+(-16 if up else 16)}" fill="#93a1bd" font-family="IBM Plex Mono,monospace" font-size="10.5" text-anchor="{anchor}">{no}</text>')
svg.append(f'<text x="{x0}" y="22" fill="#93a1bd" font-family="IBM Plex Mono,monospace" font-size="11">DÜNYA\'DAN UZAKLIK · LOGARİTMİK ÖLÇEK</text></svg>')
out.append(f'''<section>
<p class="eyebrow">Rota</p>
<h2>On bölüm, dokuz basamak büyüklük</h2>
<p class="lead">Troposfer ile Plüton arasında yaklaşık 500 milyon kat fark var. Bu yüzden her bölüm kendi sahnesinde oynanıyor; aralardaki uzun yolculuklar hızlandırılmış zamanla ve yol üstü olaylarla geçiyor.</p>
<div class="route" style="overflow-x:auto">{''.join(svg)}<p class="cap">Mesafeler yaklaşık; gezegenler için Dünya'ya en yakın olduğu zamandaki uzaklık alındı.</p></div>
</section>
''')

out.append('<section><p class="eyebrow">Piyasa araştırması</p><h2>Benzer oyunlar ve onlardan aldığımız dersler</h2><div class="mk">')
for n, p, w, t in market:
    out.append(f'<div><div><b>{E(n)}</b><span class="plat">{E(p)}</span></div><p class="what">{E(w)}</p><p class="take">{E(t)}</p></div>')
out.append('''</div>
<div class="pos"><h3>Boşluk ve konumumuz</h3>
<p class="note">Piyasada ya eğlenceli ama çocuksu yükseltme oyunları var (Into Space, Learn to Fly) ya da gerçekçi ama zor simülasyonlar (Kerbal). Arada boşluk var: <b>Kerbal'ın gerçek fizik hissi + Into Space'in bağımlılık döngüsü + sinematik grafik, telefonda.</b></p>
<ul>
<li><b>Gerçek olaylara dayanan engeller.</b> Apollo 12'ye çarpan yıldırım, Max-Q, Kessler sendromu, Cassini'nin halka geçişi. Oyun oynarken uzay tarihi öğreniliyor.</li>
<li><b>Kara kutu raporu.</b> Her patlamadan sonra ne olduğunu gösteren telemetri grafiği ve "bunu çözen geliştirme" önerisi. Ölmek ceza değil, ders.</li>
<li><b>Aynı şey hem tehdit hem itki.</b> Güneş, gezegenler ve fırtınalar donanıma ve açıya göre ya öldürüyor ya fırlatıyor.</li>
<li><b>Üsler checkpoint işlevi görür.</b> Ay Üssü kurunca Dünya'dan kalkış tekrarı biter, oyun uzunluğu kontrol altında kalır.</li>
</ul></div></section>
''')

# Güneş bölümü
out.append('''<section><p class="eyebrow">Güneş</p><h2>Üç yüzlü yıldız</h2>
<p class="lead">Mars'tan itibaren Güneş her uçuşun gizli oyuncusu. Aynı yıldız, donanımına, açına ve zamanlamana göre seni eritebilir, frenleyebilir ya da oyundaki en büyük hızı verebilir.</p>
<div class="sun">''')
for title, cls, sub, items in sun:
    out.append(f'<div class="face {cls}"><h3>{E(title)}<small>{E(sub)}</small></h3>' + "".join(f'<div><b>{E(a)}</b><p>{E(b)}</p></div>' for a, b in items) + '</div>')
out.append('''</div>
<p class="note"><b>Gerçek dayanak:</b> Parker Solar Probe 24 Aralık 2024'te Güneş'in 6,2 milyon km yakınından saniyede 192 km hızla geçti; insan yapımı en hızlı nesne. Güneş Oberth dalışı da yıldızlararası görevler için ciddi şekilde çalışılan bir kavram. Oyundaki "mükemmel hızlandırıcı" bunun oyunlaştırılmış hâli.</p>
<h3>Uzay hava durumu</h3>
<p class="note">Her uçuş, Güneş'in o anki ruh hâlini gösteren bir tahminle başlıyor. Gerçekte Güneş 11 yıllık bir döngüyle sakinleşip coşuyor. Oyuncu ya bekler ya da riski göze alır.</p>
<div class="weather">
<div><b style="color:var(--ion)">Sakin</b><p>Fırtına az, yelken itkisi zayıf, koronal delik yok. Güvenli ama yavaş.</p></div>
<div><b style="color:var(--slow)">Aktif</b><p>Ara sıra patlama, orta güçte rüzgâr. Yelken için iyi bir denge.</p></div>
<div><b style="color:var(--danger)">Maksimum</b><p>Sık CME ve patlamalar, ama koronal delik ve plazma sörfü şansı en yüksek. Yüksek risk, yüksek ödül.</p></div>
</div>
</section>
''')

# Yörünge mekaniği + sapan diyagramı
dg = '''<svg viewBox="0 0 680 230" role="img" aria-label="Sapan yönü: gezegenin arkasından geçen hızlanır, önünden geçen yavaşlar">
<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#e9eef8"/></marker>
<marker id="ag" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#55d6c2"/></marker>
<marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#f2c14e"/></marker></defs>
<g>
<text x="170" y="24" fill="#55d6c2" font-family="Saira Condensed,Arial Narrow,sans-serif" font-size="17" font-weight="700" text-anchor="middle">ARKASINDAN GEÇ · HIZLAN</text>
<circle cx="170" cy="130" r="30" fill="#c58a52"/><line x1="205" y1="130" x2="255" y2="130" stroke="#e9eef8" stroke-width="2" marker-end="url(#ah)"/>
<text x="232" y="120" fill="#93a1bd" font-family="IBM Plex Mono,monospace" font-size="10" text-anchor="middle">gezegen</text>
<path d="M60,210 C90,150 110,120 128,130 C150,142 120,190 130,200" fill="none" stroke="#5f6f8f" stroke-width="1.5" stroke-dasharray="3 3"/>
<path d="M60,210 C95,150 112,105 140,98 C190,86 250,60 300,40" fill="none" stroke="#55d6c2" stroke-width="2.5" marker-end="url(#ag)"/>
<text x="292" y="64" fill="#55d6c2" font-family="IBM Plex Mono,monospace" font-size="11" text-anchor="end">çıkış hızı +</text>
</g>
<line x1="340" y1="20" x2="340" y2="215" stroke="#24324f" stroke-width="1"/>
<g>
<text x="510" y="24" fill="#f2c14e" font-family="Saira Condensed,Arial Narrow,sans-serif" font-size="17" font-weight="700" text-anchor="middle">ÖNÜNDEN GEÇ · YAVAŞLA</text>
<circle cx="510" cy="130" r="30" fill="#c58a52"/><line x1="545" y1="130" x2="595" y2="130" stroke="#e9eef8" stroke-width="2" marker-end="url(#ah)"/>
<text x="572" y="120" fill="#93a1bd" font-family="IBM Plex Mono,monospace" font-size="10" text-anchor="middle">gezegen</text>
<path d="M420,210 C470,190 540,190 560,172 C580,150 570,110 560,95" fill="none" stroke="#f2c14e" stroke-width="2.5" marker-end="url(#ar)"/>
<text x="610" y="92" fill="#f2c14e" font-family="IBM Plex Mono,monospace" font-size="11">çıkış hızı −</text>
</g></svg>'''
out.append(f'''<section><p class="eyebrow">Gezegen yörüngeleri</p><h2>Gezegenler hareket eden basamaklar</h2>
<p class="lead">Gezegenler Güneş'in etrafında saniyede 5 ila 47 km hızla dönüyor. Yanlarından geçen roket bu hızın bir kısmını çalabilir ya da onlara kaptırabilir. Oyuncunun öğrendiği en güçlü beceri bu.</p>
<div class="diagram" style="overflow-x:auto">{dg}</div>
<div class="orb">''')
for n, fx, d, s in orbits:
    out.append(f'<div><b>{E(n)}</b>{fxchip(fx)}<p>{E(d)}</p><small>{E(s)}</small></div>')
out.append('</div></section>')

# Bölümler
out.append('<section><p class="eyebrow">Engeller ve itkiler</p><h2>Bölüm bölüm konumlandırma</h2>')
out.append('<div class="legend">' + "".join(fxchip(c) for c in "PYSI") + '</div>')
out.append('<p class="note">Turuncu notlar gerçekte yaşanmış ya da gerçek fiziğe dayanan olayları işaretliyor. <span class="new">yeni</span> etiketi bu taslakta eklenenleri gösteriyor.</p>')
for no, t, d, lg, desc, obs in chapters:
    out.append(f'<div class="ch" id="b{no}"><div class="ch-head"><span class="ch-no">BÖLÜM {no}</span><h3>{E(t)}</h3><span class="ch-dist">{E(d)}</span></div><p>{E(desc)}</p><div class="obs">')
    for nm, at, fx, ds, ct, real, fq, nw in obs:
        r = f'<span class="real">{E(real)}</span>' if real else ''
        out.append(f'<div class="ob"><div><div class="nm">{E(nm)}{newtag(nw)}</div><div class="at">{E(at)}</div></div><div class="side">{fxchip(fx)}<span class="fq {fq}">{FQ[fq]}</span></div><p class="ds">{E(ds)}</p><div class="ct"><span>Karşılığı: <i>{E(ct)}</i></span>{r}</div></div>')
    out.append('</div></div>')
out.append('</section>')

# Denge
out.append('<section><p class="eyebrow">Denge</p><h2>Her bölümün tehlike karışımı</h2><p class="lead">Kırmızı ölümcül, sarı yavaşlatıcı, mor saptırıcı, turkuaz fırsat. Ölümcül engellerin oranı yolculuk boyunca artıyor, ama her bölümde en az bir güçlü fırsat bulunuyor.</p><div class="bal">')
tot = {"P":0,"Y":0,"S":0,"I":0}
for no, t, d, lg, desc, obs in chapters:
    c = {"P":0,"Y":0,"S":0,"I":0}
    for o in obs: c[o[2]] += 1; tot[o[2]] += 1
    n = len(obs)
    bar = "".join(f'<span class="b-{k.lower()}" style="width:{c[k]/n*100:.1f}%" title="{FX[k][0]}: {c[k]}"></span>' for k in "PYSI")
    out.append(f'<div><span class="lbl">{no}. {E(names[no])}</span><span class="bar">{bar}</span><span class="n">{n}</span></div>')
out.append(f'''</div>
<p class="stats"><span>Toplam: <b>{tot["P"]}</b> ölümcül</span><span><b>{tot["Y"]}</b> yavaşlatıcı</span><span><b>{tot["S"]}</b> saptırıcı</span><span><b>{tot["I"]}</b> fırsat</span></p>
<h3>Denge kuralları</h3>
<ul class="rules">
<li><b>Bir engel, bir cevap.</b> Her ölümcül engelin en az bir karşılığı var ve o karşılık, engelle ilk karşılaşmadan sonra en fazla 2–3 başarısız uçuşla alınabiliyor.</li>
<li><b>Sıklık ödülü dengeler.</b> Yaygın engeller öğretir, seyrekler sınar, nadirler (Güneş dalışı, Psyche, rezonans kombosu) uçuşu unutulmaz kılar. Nadir olaylar bir uçuşta en fazla bir kez çıkar.</li>
<li><b>Hiçbir geliştirme her şeyi çözmez.</b> Kalkanlar ağırdır, yelkenler karanlıkta işe yaramaz, nükleer motor atmosferde yasak. Her seçim bir şeyden vazgeçmek demek.</li>
<li><b>Fırsatlar beceri ister.</b> Sapan, Oberth dalışı ve kademe ayırma zamanlama gerektirir; para değil, oyuncunun ustalığı ödüllendirilir.</li>
</ul>
</section>
''')

out.append('<section><p class="eyebrow">Hangar</p><h2>Geliştirme ağacı</h2><p class="lead">Altı dal, her dalda altı kademe. Bir sonraki kademe hem kredi hem de ilgili bölümde toplanan bilim puanı istiyor, böylece geri dönüp keşif yapmak anlam kazanıyor.</p><div class="tree">')
for n, items, note in tree:
    out.append(f'<div class="br"><h3>{E(n)}</h3><ol>' + "".join(f'<li>{E(i)}</li>' for i in items) + f'</ol><p>{E(note)}</p></div>')
out.append('</div></section>')

out.append('<section><p class="eyebrow">Yan araçlar</p><h2>Rokete eşlik edenler</h2><div class="cards">')
for n, d, nw in side:
    out.append(f'<div><b>{E(n)}{newtag(nw)}</b><p>{E(d)}</p></div>')
out.append('</div></section>')

out.append('<section><p class="eyebrow">Efsanevi geliştirmeler</p><h2>"Ağzımız açık kalsın" listesi</h2><p class="lead">Oyunun sonlarına doğru açılan, ekranda çok etkileyici duran ve çoğu gerçek mühendislik fikirlerine dayanan geliştirmeler.</p><div class="cards legendary">')
for n, d, s, nw in legend:
    out.append(f'<div><b>{E(n)}{newtag(nw)}</b><p>{E(d)}</p><small>{E(s)}</small></div>')
out.append('</div></section>')

out.append('''<section><p class="eyebrow">Ekonomi</p><h2>Üç para birimi</h2>
<div class="cards">
<div><b>Kredi</b><p>Yükseklik ve mesafeden kazanılır. Geliştirmelerin ana bedeli.</p></div>
<div><b>Bilim</b><p>Aurora geçişi, örnek toplama, fotoğraf anları. Üst kademe geliştirmeleri açar.</p></div>
<div><b>Malzeme</b><p>He-3, buz, metan, nadir metal. Üsler ve efsanevi geliştirmeler için gerekir.</p></div>
</div>
<p class="note"><b>Fotoğraf anları:</b> Ay'ın arkasından Dünya'nın doğuşu (Earthrise, 1968) ya da Satürn'den bakınca Dünya'nın "Soluk Mavi Nokta" olarak görünmesi gibi ünlü kareleri yakalamak, koleksiyon ve bonus bilim puanı veriyor.</p>
</section>
<section><p class="eyebrow">Görsel yön</p><h2>Çocuk oyunu değil, belgesel sinema</h2>
<div class="cards">
<div><b>Gökyüzü</b><p>Fiziksel tabanlı atmosfer gölgelendiricisi: yükseldikçe mavi laciverte, sonra siyaha döner, ufukta ince mavi çizgi kalır.</p></div>
<div><b>Ateş ve duman</b><p>Parçacık tabanlı egzoz, ışık patlaması (bloom), sıcak hava titremesi, kalkışta rampa dumanı.</p></div>
<div><b>Güneş dalışı</b><p>Ekran beyaza kayar, kalkan kenarları akkor turuncuya döner, ses kısılır. Ateşleme anında zaman yavaşlar.</p></div>
<div><b>Gezegenler</b><p>Prosedürel dokular: bulutlar, Jüpiter'in bantları, Satürn'ün halkaları, Plüton'un kalbi.</p></div>
</div>
<p class="note"><b>Gerçekçi sınır:</b> Tarayıcıda çalışan Three.js ile sinematik bir görünüm mümkün, ama AAA oyun seviyesi değil. Dış kaynaklardan NASA dokuları yüklenemiyor, bu yüzden gezegen yüzeyleri kodla üretilecek. Telefonda akıcı kalması için grafik kalitesi cihaza göre otomatik ayarlanacak.</p>
</section>
<section><p class="eyebrow">Yol haritası</p><h2>Adım adım geliştirme</h2>
<div class="ms">
<div><b>A1 · Oynanabilir dilim: Kalkış → Yörünge</b><p>Bölüm 1–3, roket fiziği, yaklaşık 30 engel, hangar (4 dal), kara kutu raporu, atmosfer geçişi. Burada "his" doğru mu diye birlikte karar veriyoruz.</p></div>
<div><b>A2 · Ay</b><p>Ay'a atış, sapan mekaniği, iniş, Ay Üssü checkpoint'i, yan araçların ilk dördü.</p></div>
<div><b>A3 · Mars ve Güneş</b><p>Uzay hava durumu, Güneş'in üç yüzü, atmosfer frenlemesi, Mars yakıt fabrikası.</p></div>
<div><b>A4 · Dış gezegenler ve Plüton</b><p>Bölüm 6–10, Büyük Tur, rezonans kombosu, efsanevi geliştirmeler, final sinematiği.</p></div>
</div>
<p class="note">Her adımın sonunda telefonundan oynayabileceğin bir link gelecek. Bir sonraki adıma, bir öncekinde konuştuklarımızı düzelttikten sonra geçeceğiz.</p>
</section>
<section><p class="eyebrow">Tartışalım</p><h2>Karar vermemiz gerekenler</h2>
<div class="qs">
<div><b>1. Kamera</b><p>Önerim: roketin arkasından ve biraz yukarıdan takip eden 3B kamera. Alternatif: yandan görünüm (2,5B). Daha okunaklı olur ama daha az etkileyici.</p></div>
<div><b>2. Gerçekçilik ayarı</b><p>Gerçek fizik (yörünge, sapan) ne kadar ağır bassın? Önerim: gerçek kurallar, ama hayalet rota çizgisi gibi yardımlarla öğretilsin.</p></div>
<div><b>3. Kontroller</b><p>Önerim: sol başparmakla yön, sağda gaz kaydırıcısı, ayrıca kademe ayırma ve yan araç butonları. Telefonu eğme sensörü bu ortamda kullanılamıyor.</p></div>
<div><b>4. Bir uçuşun süresi</b><p>Önerim: ilk uçuşlar 30–60 saniye, ileri bölümlerde 3–4 dakika. Uzun yolculuklarda zaman hızlandırma.</p></div>
<div><b>5. Ton ve hikâye</b><p>Ciddi bir belgesel havası mı, yoksa kara kutu raporlarında hafif mizah mı? Kurgusal bir uzay ajansı adı da seçebiliriz.</p></div>
<div><b>6. Ses</b><p>Motor gürültüsü, telsiz anonsları ("Max-Q geçildi"), müzik. Hepsi kodla üretilebilir; ses ancak ekrana dokunduktan sonra başlayabiliyor.</p></div>
</div>
</section>
<section><p class="eyebrow">Kaynaklar</p><div class="src">
<a href="https://www.guinnessworldrecords.com/world-records/66135-fastest-spacecraft-speed">Guinness: en hızlı uzay aracı (Parker Solar Probe)</a>
<a href="https://space.com/astronomy/comets/a-risky-maneuver-could-send-a-spacecraft-to-interstellar-comet-3i-atlas-heres-the-plan">Space.com: Güneş Oberth manevrası planı</a>
<a href="https://arxiv.org/html/2601.02533v1">arXiv: Catching 3I/ATLAS Using a Solar Oberth</a>
<a href="https://www.mlwgames.com/news/509/kerbal-space-program-rockets-to-its-highest-player-count-on-steam">Kerbal Space Program oyuncu sayısı ve Steam değerlendirmeleri</a>
<a href="https://raijin.gg/app/1718870/Spaceflight_Simulator">Spaceflight Simulator satış tahminleri</a>
<a href="https://toucharcade.com/2014/11/28/earn-to-die-2-review/">Earn to Die 2 incelemesi</a>
</div></section>
</div>
<script>
// Hero arka planı: yavaş akan yıldızlar ve yükselen ince bir egzoz izi.
(function(){
  const c=document.getElementById('sky'); if(!c) return;
  const x=c.getContext('2d'); let w,h,st=[];
  function size(){ const r=c.getBoundingClientRect(), d=Math.min(devicePixelRatio||1,2);
    w=c.width=r.width*d; h=c.height=r.height*d;
    st=Array.from({length:140},()=>({x:Math.random()*w,y:Math.random()*h,z:Math.random()*0.8+0.2})); }
  size(); addEventListener('resize',size);
  const still=matchMedia('(prefers-reduced-motion: reduce)').matches;
  function frame(t){
    x.clearRect(0,0,w,h);
    for(const s of st){ s.y+= still?0:s.z*0.35; if(s.y>h){s.y=0;s.x=Math.random()*w;}
      x.fillStyle=`rgba(233,238,248,${0.25+s.z*0.6})`; x.fillRect(s.x,s.y,s.z*2,s.z*2); }
    const px=w*0.86, py=h*(0.3-0.03*Math.sin(t/1400));
    const g=x.createLinearGradient(px,py,px,h*0.6); g.addColorStop(0,'rgba(255,154,60,.9)'); g.addColorStop(1,'rgba(255,154,60,0)');
    x.fillStyle=g; x.fillRect(px-1.5,py,3,h*0.6-py);
    x.fillStyle='#e9eef8'; x.beginPath(); x.moveTo(px,py-22); x.lineTo(px+5,py-6); x.lineTo(px+5,py); x.lineTo(px-5,py); x.lineTo(px-5,py-6); x.closePath(); x.fill();
    if(!still) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();
</script>
''')
page = "".join(out)
for p in OUTS:
    open(p, "w").write(page)
print(f"engel={n_obs} yeni={n_new} gelistirme={n_upg} denge={tot}")
