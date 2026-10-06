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
   ("Dolu fırtınası", "2–8 km", "Y", "Buz taneleri gövdeyi döver, hız ve dayanıklılık düşer.", "Karbon kompozit", None, "S", 1),
   ("Rüzgâr kesmesi", "2–8 km", "S", "Ani yanal rüzgâr rotayı bozar.", "Jimbal motor", None, "Y", 0),
   ("Volkanik kül bulutu", "3–10 km", "Y", "Aşındırıcı kül motor nozulunu yıpratır, itki kademeli olarak düşer.", "Seramik kaplama", "2010 Eyjafjallajökull külü Avrupa hava trafiğini durdurdu", "S", 1),
   ("Fırtına bulutu ve yıldırım", "4–10 km", "P", "Yıldırım aviyoniği kapatır, kontrol birkaç saniye gider.", "Faraday kafesi", "Apollo 12'ye kalkışta iki kez yıldırım çarptı (1969)", "Y", 0),
   ("Buzlanma", "6–10 km", "Y", "Gövdede buz birikir, kütle artar.", "Isıtmalı gövde", None, "Y", 0),
   ("Yolcu uçağı koridoru", "10–12 km", "P", "Ticari uçuş rotası. Çarpışma kesin son; çevik manevra gerekir.", "Jimbal motor", None, "S", 1),
   ("Jet akımı", "9–12 km", "I", "Doğru yönde girersen ivme, ters açıyla girersen sapma.", "Engel radarı", None, "Y", 0),
   ("Max-Q", "6–14 km (hıza göre)", "P", "Çok hızlıysan aerodinamik basınç roketi parçalar. Gazı kısmayı öğrenmek zorundasın.", "Karbon kompozit", "Çoğu fırlatmada gaz bu noktada kısılır", "Y", 0)]),
 ("2", "Üst Atmosfer", "12 – 100 km", 2.0,
  "Gökyüzü maviden laciverte, sonra siyaha döner. Oyunun ilk görsel 'vay' anı Kármán hattı.",
  [("Stratosfer balonları", "15–35 km", "P", "Rastgele yükselen bilim balonlarıyla çarpışma.", "Engel radarı", None, "Y", 0),
   ("Ozon tabakası", "20–30 km", "I", "Tehlikesiz. UV ölçümü bilim puanı verir.", "—", None, "Y", 1),
   ("Mavi jetler", "40–50 km", "P", "Bulut tepesinden yukarı fışkıran mavi şimşek.", "Faraday kafesi", "Gerçek üst atmosfer olayı", "S", 1),
   ("Kırmızı sprite şimşekleri", "50–90 km", "P", "Bulutların çok üzerinde çakan kısa elektrik boşalmaları.", "Faraday kafesi", "Gerçek üst atmosfer olayı", "S", 0),
   ("Kademe ayırma penceresi", "60–80 km", "I", "Boş kademeyi doğru anda atarsan ani ivme, geç kalırsan ölü ağırlık.", "İki kademe", None, "Y", 0),
   ("Gece parlayan bulutlar", "76–85 km", "Y", "Buz kristallerinden oluşan en yüksek bulutlar. Hafif fren, ama bilim puanı verir.", "—", "Dünya'nın en yüksek bulutları", "S", 1),
   ("Göktaşı izleri", "70–100 km", "Y", "Yanan küçük göktaşı parçaları gövdeyi döver.", "Whipple kalkanı", None, "Y", 0),
   ("Kármán hattı", "100 km", "I", "Uzayın başlangıcı. Sinematik an, bilim puanı ve ilk büyük ödül.", "—", "FAI'nin kabul ettiği uzay sınırı (ABD 80 km kullanır)", "Y", 0)]),
 ("3", "Yörünge", "100 – 36.000 km", 2.6,
  "Yukarı çıkmak yetmiyor. Saniyede 7,8 km yatay hıza ulaşmazsan düşersin. Oyuncu burada gerçek roket fiziğini keşfediyor.",
  [("Yerçekimi dönüşü", "100–200 km", "Y", "Dik çıkmakta ısrar edersen yörüngeye giremez, geri düşersin.", "Yerçekimi dönüşü otopilotu", "Gerçek fırlatmalarda roket yavaşça yatar", "Y", 0),
   ("Termosfer sürtünmesi", "100–400 km", "Y", "İnce ama etkili hava direnci.", "—", None, "Y", 0),
   ("Atomik oksijen", "200–600 km", "Y", "Tek atomlu oksijen gövde kaplamasını kemirir.", "Seramik kaplama", "Alçak yörüngede gerçek malzeme sorunu", "Y", 1),
   ("Aurora perdesi", "100–300 km", "S", "Manyetik alan pusulayı saptırır, ama geçiş bilim puanı kazandırır.", "Yıldız izleyici", None, "S", 0),
   ("Uzay istasyonu", "400 km", "I", "Yanaşabilirsen yakıt ikmali alırsın.", "Yanaşma sistemi", None, "Y", 0),
   ("Kayıp alet çantası", "400 km", "I", "Yakalarsan küçük bir bilim ödülü.", "Robot kol", "Bir astronot 2008'de uzay yürüyüşünde alet çantasını kaybetti", "N", 1),
   ("Uydu treni", "550 km", "S", "Sıra halinde ilerleyen yüzlerce küçük uydu. Aradan geçmek zamanlama ister.", "Otomatik kaçınma", None, "Y", 1),
   ("Güney Atlantik Anomalisi", "200–800 km", "S", "Radyasyonun yere en çok yaklaştığı bölge. Aviyonikte rastgele hatalar.", "Radyasyon zırhı", "Gerçek; uydular burada hata yapar", "S", 1),
   ("Uzay çöpü kuşağı", "600–1.000 km", "P", "Çarptığın her parça yeni parçalara bölünür ve tehlike zincirleme büyür.", "Whipple kalkanı", "Kessler sendromu", "Y", 0),
   ("Uydu karşıtı test enkazı", "Rastgele", "P", "Ani beliren yoğun enkaz bulutu.", "Otomatik kaçınma", "2007 ve 2021'de gerçek testler binlerce parça bıraktı", "N", 1),
   ("Ölü uydu", "800 km", "I", "Robot kolla yakalarsan hurda kredisi verir.", "Robot kol", None, "S", 0),
   ("Van Allen iç kuşağı", "1.000+ km", "P", "Radyasyon aviyoniği sıfırlar.", "Radyasyon zırhı", "Gerçek radyasyon kuşağı", "Y", 0),
   ("Mezarlık yörüngesi", "36.000 km", "P", "Yer-durağan kuşağın hemen üstünde emekli uydular birikmiş.", "Engel radarı", "Gerçek; emekli uydular buraya itilir", "S", 1)]),
 ("4", "Ay", "384.400 km", 5.58,
  "İlk gerçek yolculuk. Yörüngeden kopma anını doğru zamanlamak ve Ay'ın yerçekimini kullanmak gerekiyor.",
  [("Ay'a atış zamanlaması", "Dünya yörüngesi", "I", "Motoru Dünya'ya en yakın noktada yakarsan çok daha fazla hız kazanırsın.", "Sapan hesaplayıcı", "Oberth etkisi", "Y", 0),
   ("Dünya'nın manyetik kuyruğu", "Ay yolu", "S", "Güneş rüzgârının arkaya doğru uzattığı manyetik alan. Yüklü toz roketi iter.", "Manyetik radyasyon kalkanı", "Ay her ay bu kuyruğun içinden geçer", "S", 1),
   ("L1 Lagrange noktası", "~326.000 km", "S", "Dengesiz bölge, roketi yavaşça sürükler.", "Hassas iticiler", None, "Y", 0),
   ("Ay sapanı", "Ay yakını", "I", "Doğru açıyla geçersen yakıt harcamadan büyük ivme, yanlışsa çarpma.", "Sapan hesaplayıcı", "Apollo 13 dönüşünde kullanıldı", "Y", 0),
   ("Masconlar", "Ay yörüngesi", "S", "Ay'ın düzensiz kütle yoğunlukları yörüngeyi bozar.", "Hassas iticiler", "1968'de Lunar Orbiter verileriyle keşfedildi", "Y", 0),
   ("Apollo hurdası", "Dünya–Ay arası", "I", "Güneş yörüngesinde dolaşan eski bir Saturn V üst kademesi ara sıra yakınlardan geçer. Yakalarsan koleksiyon ve bilim ödülü.", "Robot kol", "2002'de asteroit sanılan J002E3, Apollo 12'nin üst kademesi çıktı", "N", 1),
   ("Ay gecesi", "Ay yüzeyi", "Y", "−173 °C. Bataryalar donar, güç düşer.", "RTG (nükleer pil)", "Gerçek; 14 gün sürer", "Y", 1),
   ("Regolit tozu", "İniş", "Y", "İnişte kalkan toz görüşü kapatır.", "LIDAR", None, "Y", 0),
   ("Ay depremi", "İniş", "P", "İniş anında yüzey sarsılır, bacaklar kırılabilir.", "Esnek iniş bacakları", "Apollo sismometreleri kaydetti", "S", 1),
   ("Shackleton krateri buzu", "Güney kutbu", "I", "Hiç güneş görmeyen kraterlerde su buzu. Yakıta dönüşür.", "Madenci drone", "Güney kutbundaki kalıcı gölgeli kraterlerde buz izleri bulundu; Artemis'in hedef bölgesi", "S", 1),
   ("Ay Üssü", "Ödül", "I", "Kurulunca sonraki uçuşlar Ay'dan başlayabilir.", "—", None, "Y", 0)]),
 ("5", "Mars Yolu", "~78 milyon km", 7.89,
  "Güneş artık bir oyuncu (aşağıdaki Güneş bölümüne bak). Mars'a varınca atmosfere doğru açıyla girmek gerekiyor.",
  [("Mikrometeoroid yağmuru", "Yol boyu", "Y", "Küçük ama sürekli çarpışmalar.", "Whipple kalkanı", None, "Y", 0),
   ("Kozmik ışın sağanağı", "Yol boyu", "S", "Galaksi dışından gelen parçacıklar bellekte bit hatası yapar, kontrol anlık şaşar.", "Radyasyon zırhı", "Gerçek; derin uzay elektroniğinin baş belası", "S", 1),
   ("Phobos", "Mars yakını", "I", "Küçük ama kullanışlı bir sapan.", "—", None, "Y", 0),
   ("Atmosfer frenlemesi", "Mars atmosferi", "Y", "Dik girersen yanarsın, sığ girersen sekip uzaya kaçarsın. Doğru açı yakıtsız yavaşlatır.", "Ablatif ısı kalkanı", "Gerçek iniş tekniği", "Y", 0),
   ("İnce atmosfer", "İniş", "Y", "Paraşüt tek başına yetmez, son metrelerde motorla frenlemek gerekir.", "Süpersonik retro motor", "Gerçek; Mars inişlerinin en zor kısmı", "Y", 1),
   ("Toz fırtınası", "Mars yüzeyi", "S", "Görüşü ve güneş enerjisini keser.", "RTG (nükleer pil)", None, "S", 0),
   ("Toz şeytanları", "Mars yüzeyi", "I", "Küçük hortumlar güneş panellerinin tozunu temizler, enerji geri gelir.", "—", "Spirit gezgininin panellerini gerçekten temizlediler", "S", 1),
   ("Olympus Mons", "İniş bölgesi", "P", "22 km yüksekliğindeki dağ. Yanlış rotada iniş yamaca çarpar.", "LIDAR", "Güneş sisteminin en yüksek dağlarından", "Y", 1),
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
   ("Radyasyon kuşakları", "Jüpiter yakını", "P", "Güneş sistemindeki en sert radyasyon.", "Manyetik radyasyon kalkanı", None, "Y", 0),
   ("Büyük Kırmızı Leke", "Jüpiter atmosferi", "S", "Dünya'dan büyük bir fırtına. Yaklaşırsan seni içine çeker.", "—", "En az 150 yıldır gözlenen gerçek fırtına", "Y", 1),
   ("Laplace rezonans zinciri", "Io–Europa–Ganymede", "I", "Üç uydu 1:2:4 ritmiyle dönüyor. Doğru anda üçünden art arda sapan yaparsan dev kombo ivme.", "Zincir planlayıcı", "Gerçek yörünge rezonansı", "N", 1),
   ("Io plazma halkası", "Io yörüngesi", "I", "Elektrodinamik ipin varsa elektrik üretir.", "Elektrodinamik ip", None, "S", 0),
   ("Europa buz tozları", "Europa", "I", "Yüzeyden kopan buz. Buhar roketinin yakıtı.", "Madenci drone", None, "Y", 1),
   ("Kuyruklu yıldız parçaları", "Jüpiter yakını", "P", "Jüpiter'e düşen parçalanmış kuyruklu yıldız zinciri.", "Otomatik kaçınma", "Shoemaker–Levy 9, 1994", "N", 1),
   ("Güneş enerjisi sınırı", "Jüpiter ötesi", "Y", "Güneş panelleri artık yetmez, nükleer enerji gerekir.", "RTG (nükleer pil)", "Juno Jüpiter'de dev panellerle idare etti; Satürn ve ötesine giden her sonda RTG kullandı", "Y", 0)]),
 ("8", "Satürn", "~1,3 milyar km", 9.11,
  "Görsel olarak oyunun zirvesi: halkaların arasından geçiş.",
  [("Halka geçişi", "Halka boşluğu", "P", "Buz parçalarının arasından dar bir koridor.", "Otomatik kaçınma", "Cassini 2017'de bu boşluktan 22 kez geçti", "Y", 0),
   ("Çoban uydular", "Halka içi", "I", "Pan ve Daphnis halkalarda temiz boşluklar açar. Onları takip eden güvenli geçer.", "Zincir planlayıcı", "Gerçek; halkalardaki dalgaları onlar yapar", "S", 1),
   ("Halka yağmuru", "Halka altı", "Y", "Halkalardan gezegene buz parçacıkları yağar, hafif fren.", "—", "Gerçek; Cassini ölçtü", "Y", 1),
   ("Halka parmakları", "Halka üstü", "S", "Elektrostatik toz şeritleri aviyoniği şaşırtır.", "Faraday kafesi", "Halkalardaki gizemli 'spoke'lar", "S", 1),
   ("Kutup altıgeni", "Kuzey kutbu", "S", "Altıgen biçimli dev jet akımı. Kenarından girersen savrulursun.", "—", "Gerçek; Voyager keşfetti", "S", 1),
   ("Hyperion", "Dış yörünge", "P", "Kaotik dönen, sünger gibi uydu. Yanaşmak neredeyse imkânsız.", "Otomatik kaçınma", "Dönüşü gerçekten öngörülemez", "S", 1),
   ("Titan", "Titan", "Y", "Kalın atmosfer frenler, metan gölleri yakıt verir.", "Ablatif ısı kalkanı", None, "Y", 0),
   ("Enceladus gayzerleri", "Enceladus", "S", "Buz püskürtüleri iter; içinden geçmek su toplar.", "—", None, "Y", 0)]),
 ("9", "Uranüs, Neptün ve Kuiper", "2,7 – 4,5 milyar km", 9.55,
  "Karanlık, soğuk ve sessiz. Güneş ışığı artık işe yaramıyor, sensörlerle uçmak gerekiyor.",
  [("Güneş ışığının sönüşü", "Uranüs ötesi", "Y", "Güneş yelkeni ve paneller neredeyse sıfıra düşer. Yalnızca nükleer güç.", "RTG (nükleer pil)", "Işık, uzaklığın karesiyle azalır", "Y", 1),
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
  "Hava soluyan motor atmosferde oksijeni havadan alır, ilk bölümlerde yakıtı ikiye katlar. Gerçek: SABRE motor kavramı."),
 ("Uzun yol sürüşü", ["Güneş yelkeni", "İyon motoru", "Elektrik yelken", "Manyetik yelken", "Güneş termal roketi", "Buhar roketi"],
  "Buhar roketi Europa, Enceladus veya Kuiper buzuyla çalışır; madenci drone'la birlikte her yerde yakıt ikmali demek."),
 ("Gövde ve kalkan", ["Karbon kompozit", "Ablatif ısı kalkanı", "Whipple kalkanı", "Kendini onaran gövde", "Güneş dalış kalkanı", "Manyetik radyasyon kalkanı"],
  "Güneş dalış kalkanı Parker Solar Probe'unkine benzer karbon köpük bir kalkan; Güneş Oberth dalışını açar."),
 ("Aviyonik", ["Yerçekimi dönüşü otopilotu", "Engel radarı", "Otomatik kaçınma", "Sapan hesaplayıcı", "Zincir planlayıcı", "Uzay hava durumu uydusu"],
  "Zincir planlayıcı birden fazla sapanı ve rezonans kombolarını hayalet rota olarak önceden çizer."),
 ("Enerji", ["Batarya", "Güneş paneli", "Yakıt hücresi", "Isı radyatörleri", "RTG (nükleer pil)", "Kompakt füzyon"],
  "Isı radyatörleri Güneş yakınında motoru soğutur. Satürn'den itibaren güneş paneli yetmez; RTG doğal bir ilerleme kapısı."),
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
 ("Kuyruklu yıldız sörfü", "Zıpkınla bir kuyruklu yıldıza tutun ve onunla birlikte Güneş'in etrafından fırla. Güneş dalışını kalkansız yapmanın tek yolu.", "Philae iniş aracında gerçek zıpkınlar vardı, 2014'te ateşlenemediler", 1),
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

FAMILIES = [
 ("Hareketli sürüler", "Kaç ya da araya gir", ["Kuş sürüsü", "Stratosfer balonları", "Yolcu uçağı koridoru", "Uydu treni"]),
 ("Küçük darbe yağmuru", "Kalkan al ya da alandan hızlı çık", ["Dolu fırtınası", "Göktaşı izleri", "Mikrometeoroid yağmuru", "Halka yağmuru"]),
 ("Elektrik darbesi", "Kısa kontrol kaybı; Faraday kafesi", ["Fırtına bulutu ve yıldırım", "Mavi jetler", "Kırmızı sprite şimşekleri", "Halka parmakları"]),
 ("Radyasyon alanı", "İçinde kalma süresini yönet; zırh", ["Güney Atlantik Anomalisi", "Van Allen iç kuşağı", "Kozmik ışın sağanağı", "Radyasyon kuşakları"]),
 ("Rüzgâr ve akıntılar", "Açını ayarla; doğru yönde ivme", ["Rüzgâr kesmesi", "Jet akımı", "Dünya'nın manyetik kuyruğu", "Büyük Kırmızı Leke", "Kutup altıgeni", "Neptün rüzgârları", "Büyük Karanlık Leke"]),
 ("İtki sütunları", "İçinden geç ya da kaçın", ["Termal sütun", "Enceladus gayzerleri", "Triton gayzerleri"]),
 ("Yoğun enkaz alanları", "Slalom; çarptığın parça bölünür", ["Uzay çöpü kuşağı", "Uydu karşıtı test enkazı", "Mezarlık yörüngesi", "Çarpışma kümesi", "Truva asteroitleri", "Halka geçişi", "Kuyruklu yıldız parçaları", "Nix ve Hydra"]),
 ("Görünmez tehlikeler", "Sensörle uç", ["Karanlık Kuiper nesneleri", "Karanlık halkalar", "Regolit tozu", "Toz fırtınası"]),
 ("Sinsi yükler", "Yavaşça zayıflatır; doğru kaplama", ["Buzlanma", "Volkanik kül bulutu", "Termosfer sürtünmesi", "Atomik oksijen", "Gece parlayan bulutlar"]),
 ("Yapısal sınırlar", "Hız ve açı eşiği; gazı yönet", ["Max-Q", "Pogo titreşimi", "Yerçekimi dönüşü"]),
 ("Zamanlama anları", "Doğru anda bas", ["Kademe ayırma penceresi", "Ay'a atış zamanlaması"]),
 ("Sapanlar", "Açı ve yön seç", ["Ay sapanı", "Phobos", "Ceres sapanı", "Jüpiter sapanı", "Laplace rezonans zinciri", "Yan yatık Uranüs"]),
 ("Kararsız yerçekimi", "Sürüklenmeyi düzelt", ["L1 Lagrange noktası", "Masconlar", "Plüton–Charon ikilisi", "Hyperion"]),
 ("Atmosfere giriş", "Giriş açısı koridoru", ["Atmosfer frenlemesi", "İnce atmosfer", "Titan", "Mavi pus"]),
 ("İnişler", "İniş mini oyunu", ["Ay depremi", "Olympus Mons", "Buz dağları", "Tombaugh Regio'ya iniş", "Moloz yığını asteroit"]),
 ("Enerji kapıları", "Güç kaynağını değiştir", ["Ay gecesi", "Güneş enerjisi sınırı", "Güneş ışığının sönüşü", "Toz şeytanları"]),
 ("Yakala ve topla", "Yanaş, yakala, ödül al", ["Uzay istasyonu", "Kayıp alet çantası", "Ölü uydu", "Apollo hurdası", "Madenlik asteroit", "Psyche metal asteroit", "Shackleton krateri buzu", "Europa buz tozları", "Io plazma halkası", "Kuyruklu yıldız geçişi"]),
 ("Bilim ve kilometre taşları", "Fotoğraf, ölçüm, sinematik", ["Ozon tabakası", "Kármán hattı", "Aurora perdesi", "Arrokoth"]),
 ("Güvenli koridorlar ve üsler", "Rehber yol ve checkpoint", ["Kirkwood boşlukları", "Çoban uydular", "Ay Üssü", "Mars yakıt fabrikası"]),
]
_all = [o[0] for c in chapters for o in c[5]]
_fam = [m for f in FAMILIES for m in f[2]]
assert sorted(_all) == sorted(_fam), (set(_all) ^ set(_fam))

sys.path.insert(0, HERE)
import model as M
_chk, _fk = M.kontroller(chapters, FAMILIES)
M.json_disari(os.path.join(HERE, "model.json"))
for _ad, _ok, _h in _chk:
    print(("TAMAM " if _ok else "HATA  ") + _ad, _h if _h else "")
import ekonomi_sim
_eko_rows, _eko_dk = ekonomi_sim.main(600)

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
/* görsel katmanlar */
.tiers{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}
@media (max-width:520px){.tiers{grid-template-columns:1fr}}
.tiers > div{border:1px solid var(--line);border-radius:6px;padding:10px 12px;display:flex;flex-direction:column;gap:2px;background:var(--panel)}
.tiers > div:last-child{border-color:#5a4426;background:linear-gradient(170deg,#2a2016,var(--panel))}
.tier{font-family:var(--f-mono);font-size:.68rem;letter-spacing:.1em;text-transform:uppercase;color:var(--flame)}
.tiers b{font-family:var(--f-display);font-size:1.2rem}
.tiers p{color:var(--dim);font-size:.85rem}
.sig{display:flex;flex-direction:column;border-top:1px solid var(--line)}
.sig > div{display:grid;grid-template-columns:2rem minmax(0,1fr);gap:2px 10px;padding:10px 0;border-bottom:1px solid var(--line)}
.sig span{grid-row:span 2;font-family:var(--f-mono);font-size:.8rem;color:var(--flame);padding-top:2px}
.sig b{font-weight:600}
.sig p{color:var(--dim);font-size:.9rem}
.fam{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,230px),1fr));gap:8px}
.fam > div{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:10px 12px;display:flex;flex-direction:column;gap:3px;min-width:0}
.fam b{font-weight:600}
.fam .act{font-family:var(--f-mono);font-size:.72rem;color:var(--ion)}
.fam p{color:var(--faint);font-size:.82rem;line-height:1.45}
.obj{display:flex;flex-direction:column;gap:8px}
.obj > div{border:1px solid var(--line);border-radius:8px;padding:12px 14px;display:flex;flex-direction:column;gap:4px;background:var(--panel)}
.obj b{font-family:var(--f-display);font-size:1.15rem}
.obj p{color:var(--dim);font-size:.9rem;line-height:1.5}
.obj i{font-style:normal;color:var(--star);font-weight:500}
.sfx{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,230px),1fr));gap:8px}
.sfx > div{border-left:2px solid var(--flame);padding:4px 0 4px 12px;display:flex;flex-direction:column;gap:3px;min-width:0}
.sfx b{font-weight:600}
.sfx p{color:var(--dim);font-size:.88rem;line-height:1.5}
.screens{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,230px),1fr));gap:10px}
.screens > div{border:1px solid var(--line);border-radius:8px;padding:13px;display:flex;flex-direction:column;gap:4px}
.screens b{font-family:var(--f-display);font-size:1.18rem;color:var(--ion)}
.screens p{color:var(--dim);font-size:.9rem;line-height:1.5}
.eko{display:flex;flex-direction:column;border-top:1px solid var(--line);font-variant-numeric:tabular-nums}
.eko > div{display:grid;grid-template-columns:minmax(0,1fr) 4rem 7rem;gap:10px;padding:7px 0;border-bottom:1px solid var(--line);font-size:.92rem}
.eko .v{text-align:right;color:var(--flame);font-family:var(--f-mono)}
.eko .r{text-align:right;color:var(--faint);font-family:var(--f-mono);font-size:.82rem}
.eko .h{color:var(--faint);font-family:var(--f-mono);font-size:.72rem;letter-spacing:.06em;text-transform:uppercase}
.eko .h .v{color:var(--faint)}
.est .h:last-child{color:var(--star);font-size:.9rem;text-transform:none;letter-spacing:0}
.est .h:last-child .v{color:var(--flame)}
code{font-family:var(--f-mono);font-size:.85em;color:var(--star)}
.qs i{font-style:normal;color:var(--ion)}
.tbl{overflow-x:auto;border:1px solid var(--line);border-radius:8px}
.tbl table{width:100%;border-collapse:collapse;font-size:.86rem;min-width:520px}
.tbl th{font-family:var(--f-mono);font-size:.68rem;letter-spacing:.06em;text-transform:uppercase;color:var(--faint);text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);font-weight:500;background:var(--panel)}
.tbl td{padding:8px 10px;border-bottom:1px solid var(--line);color:var(--dim);vertical-align:top;line-height:1.45}
.tbl tr:last-child td{border-bottom:0}
.tbl td b{color:var(--star);font-weight:600}
.tbl .num{font-family:var(--f-mono);font-variant-numeric:tabular-nums;white-space:nowrap;color:var(--star)}
.tbl .ok{color:var(--ion)} .tbl .bad{color:var(--danger)}
.fx{display:flex;flex-direction:column;gap:8px}
.fx > div{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:11px 13px;display:flex;flex-direction:column;gap:4px}
.fx b{font-weight:600}
.fx .act{font-family:var(--f-mono);font-size:.72rem;color:var(--ion)}
.fx p{color:var(--dim);font-size:.88rem;line-height:1.5}
.fx i{font-style:normal;color:var(--star);font-weight:500}
.tree2{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:10px}
.br2{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:14px;display:flex;flex-direction:column;gap:9px;min-width:0}
.up{display:grid;grid-template-columns:1.5rem minmax(0,1fr);gap:8px}
.up .k{font-family:var(--f-mono);font-size:.72rem;color:var(--flame);border:1px solid var(--line);border-radius:3px;text-align:center;line-height:1.5rem;height:1.5rem}
.up b{font-size:.93rem}
.up p{color:var(--dim);font-size:.84rem;line-height:1.45}
.cost{color:var(--slow)!important;font-size:.8rem!important}
.fail > div{grid-template-columns:minmax(0,1fr) 9rem}
.fail b{color:var(--star);font-weight:600}
ol.rules{padding-left:1.3em}
.chk{display:flex;flex-direction:column;gap:6px}
.chk > div{display:grid;grid-template-columns:1.6rem minmax(0,1fr);gap:8px;align-items:start;border:1px solid var(--line);border-radius:6px;padding:9px 12px}
.chk span{font-weight:700;font-size:1rem}
.chk .ok span{color:var(--ion)} .chk .bad span{color:var(--danger)} .chk .bad{border-color:var(--danger)}
.chk p{font-size:.9rem}
.chk small{color:var(--faint)}
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
<p class="eyebrow">Oyun tasarım belgesi · Taslak 5 · Plan tamam, kodlamaya hazır</p>
<h1>Son Durak:<br><em>Plüton</em></h1>
<p class="pitch">Dünya'dan kalkan bir roket her denemede biraz daha uzağa gidiyor. Önce atmosfer, sonra yörünge, Ay, Mars ve sonunda Plüton. Her patlamadan sonra hangarda geliştirme yapıyor, bir sonraki denemede bir önceki seni öldüren engeli aşıyorsun.</p>
<div class="loop">
<div><b>Kalk</b><span>Gazı ve rotayı yönet</span></div>
<div><b>Düş</b><span>Kara kutu raporu: neden patladın?</span></div>
<div><b>Geliştir</b><span>6 dal, ''' + str(n_upg) + ''' geliştirme, yan araçlar</span></div>
<div><b>Uzağa</b><span>Üs kur, oradan devam et</span></div>
</div>
''')
out.append(f'''<div class="changes"><p class="eyebrow">Taslak 5'te neler değişti</p><ul>
<li><b>Sayısal model:</b> roketin 13 değişkeni, 19 engel ailesinin sayısal etkileri, tüm geliştirme, modül, yan araç ve efsanevilerin sayıları, Güneş ve yörünge formülleri, etkileşim kuralları.</li>
<li><b>Kalkış fiziği simülasyonu:</b> roket değerleri gerçek fizikle doğrulandı; ekonomi simülasyonu buna bağlandı (Plüton'a iniş ~92 uçuş).</li>
<li><b>Yeni kategori, modüller:</b> engel karşılıklarında adı geçip ağaçta olmayan 13 donanım (Faraday kafesi, LIDAR…) sınırlı yuvalı modüllere dönüştü.</li>
<li><b>Düzeltmeler:</b> efsanevi fiyatlar kazançla orantısızdı (120.000 → 20.000 kredi); Max-Q konumu fiziğe göre 6–14 km oldu.</li>
<li><b>Eksik kontrolü:</b> başarısızlık türleri, kazanç formülü, zaman ölçeği, ilk 10 dakika, rastgelelik, görev hedefleri, oyun sonu, kayıt yedeği, erişilebilirlik, lisanslar, mimari ve test planı.</li>
<li><b>Tutarlılık denetimi:</b> plan her üretildiğinde kendi kurallarını otomatik kontrol ediyor.</li>
</ul><p class="eyebrow" style="margin-top:6px">Taslak 4'te eklenenler</p><ul>
<li><b>Hasar sistemi ve nesneler:</b> göçük, kopan parça, bükülme, parçalanma; kuş, bulut, balon, uydu ve asteroitlerin hareket ve çarpışma tepkileri.</li>
<li><b>Engel aileleri:</b> 89 engel 19 davranışa indirildi.</li>
<li><b>Ekonomi simülasyonu:</b> Plüton'a iniş yaklaşık 86 uçuş.</li>
<li><b>Ses, müzik, arayüz, S24 Ultra performans hedefi, geliştirme tahmini ve varsayılan kararlar.</b></li>
<li><b>Bilgi doğrulaması:</b> 11 not düzeltildi (Soluk Mavi Nokta, masconların keşfi, Juno'nun güneş panelleri, Kármán sınırı…).</li>
</ul><p class="eyebrow" style="margin-top:6px">Taslak 3'te eklenenler</p><ul>
<li><b>Tasarım ilkeleri eklendi:</b> rota ve uygulama katmanları, engel aileleri, 3 saniyede yeniden kalkış, önce ekonomi simülasyonu.</li>
<li><b>Görsel sistem ayrıntılandırıldı:</b> taban katman, her bölümün görsel imzası ve 4 kahraman an; gerçekçilik kuralları ve performans bütçesi.</li>
<li><b>Yol haritasına A0 eklendi:</b> oynanabilir sürümden önce telefonunda deneyeceğin 20 saniyelik görsel prototip.</li>
<li><b>Düzeltme:</b> Apollo hurdası Ay yörüngesinde değil, Güneş yörüngesinde.</li>
</ul><p class="eyebrow" style="margin-top:6px">Taslak 2'de eklenenler</p><ul>
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
out.append('''<section><p class="eyebrow">Tasarım ilkeleri</p><h2>Kerbal 2'nin düştüğü tuzağa düşmemek</h2>
<div class="qs">
<div><b>Rota ve uygulama: iki katman</b><p>Atmosfer gerçek zamanlı bir aksiyon, uzay ise bir planlama oyunu. Bu yüzden uzayda önce <b>rota ekranında</b> hangi sapanı ve pencereyi kullanacağını seçiyorsun, sonra bunu zamanlama anlarıyla ve engellerden kaçarak <b>uyguluyorsun</b>. Fizik gerçek kalıyor; oyuncu hesap yapmıyor, karar veriyor ve beceri gösteriyor.</p></div>
<div><b>Engel aileleri</b><p>Bir engel ancak oyuncuyu farklı bir şey yapmaya zorluyorsa ayrı engeldir. Aşağıdaki 89 madde, 15–20 davranış ailesine indirilecek. Örneğin dolu, göktaşı izi ve mikrometeoroid aynı ailenin ("küçük darbeler") farklı görünümleri. Görsel çeşitlilik kalıyor, kurallar sadeleşiyor.</p></div>
<div><b>3 saniyede yeniden kalkış</b><p>Patlama, kara kutu, hangar, kalkış döngüsü çok hızlı. Her bölüm başında checkpoint var; Jüpiter'de ölen oyuncu Dünya'dan baştan uçmuyor.</p></div>
<div><b>Önce ekonomi simülasyonu</b><p>Kaç uçuşta Ay'a varılacağı, geliştirmelerin fiyatı ve kazançlar kodlamadan önce bir simülasyonla ayarlanacak.</p></div>
<div><b>En fazla 4 kontrol</b><p>Yön, gaz, kademe ayırma ve yan araç. Kurallar uzun metinlerle değil, patlayıp kara kutu raporunu okuyarak öğreniliyor.</p></div>
<div><b>Gerçek notlar doğrulanır</b><p>"Gerçek" diye sunulan her bilgi yayından önce tek tek kontrol edilecek.</p></div>
</div></section>
<section><p class="eyebrow">Güneş</p><h2>Üç yüzlü yıldız</h2>
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

# Güneş ve yörünge sayıları
out.append('<section><p class="eyebrow">Hızlandırıcı ve Güneş sayıları</p><h2>Formüller</h2><p class="lead">Güneş\'in üç yüzü ve gezegen fırsatlarının oyundaki sayısal karşılıkları.</p><div class="tbl"><table><thead><tr><th>Olay</th><th>Değer ve formül</th></tr></thead><tbody>')
for a_, b_ in M.SUN_FX + M.ORBIT_FX:
    out.append(f'<tr><td><b>{E(a_)}</b></td><td>{E(b_)}</td></tr>')
out.append('</tbody></table></div><div class="tbl"><table><thead><tr><th>Uzay hava durumu</th><th>Uçuş olasılığı</th><th>CME sıklığı</th><th>Koronal delik</th><th>Yelken itkisi</th></tr></thead><tbody>')
for (ad, cme, kd, ye), ol in zip(M.WEATHER, ("%40", "%45", "%15")):
    out.append(f'<tr><td><b>{ad}</b></td><td>{ol}</td><td class="num">×{cme:g}</td><td class="num">%{kd*100:.0f}</td><td class="num">×{ye:g}</td></tr>'.replace(".", ","))
out.append('</tbody></table></div></section>')

# Engel aileleri
out.append(f'<section><p class="eyebrow">Engel aileleri</p><h2>{len(_all)} engel, {len(FAMILIES)} davranış</h2><p class="lead">Bir engel ancak oyuncuyu farklı bir şey yapmaya zorluyorsa ayrı engeldir. Aşağıdaki bölüm listesindeki her madde bu ailelerden birinin, o ortama uygun görünümü. Kod tarafında {len(FAMILIES)} davranış yazılıyor, görsel çeşitlilik korunuyor.</p><div class="fam">')
for n, act, mem in FAMILIES:
    out.append(f'<div><b>{E(n)}</b><span class="act">{E(act)}</span><p>{E(", ".join(mem))}</p></div>')
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

# Roket modeli ve etki tablosu (veriler model.py'den)
def _n(x):
    return f"{x:,}".replace(",", ".")

out.append('<section><p class="eyebrow">Roket modeli</p><h2>Roketin değişkenleri</h2><p class="lead">Her engel, geliştirme ve hızlandırıcı bu değişkenlerden birini ya da birkaçını değiştirir. Başlangıç değerleri ilk ayardır ve kalkış fiziği simülasyonuyla doğrulandı.</p><div class="tbl"><table><thead><tr><th>Değişken</th><th>Birim</th><th>Başlangıç</th><th>Not</th></tr></thead><tbody>')
for _id, ad, bi, de, no in M.STATE:
    out.append(f'<tr><td><b>{E(ad)}</b></td><td>{E(bi)}</td><td class="num">{E(de)}</td><td>{E(no)}</td></tr>')
out.append('</tbody></table></div><h3>Ortam</h3><div class="tbl"><table><thead><tr><th>Büyüklük</th><th>Formül</th><th>Not</th></tr></thead><tbody>')
for ad, f, no in M.ENV:
    out.append(f'<tr><td><b>{E(ad)}</b></td><td>{E(f)}</td><td>{E(no)}</td></tr>')
out.append('</tbody></table></div><h3>Kalkış fiziği doğrulaması</h3><p class="note">Engelsiz, ideal pilotla Dünya\'dan kalkış simülasyonu: gerçek yerçekimi, hava yoğunluğu, sürükleme ve yörünge mekaniği. Her satır, hangi donanımla nereye fiziksel olarak varılabildiğini gösteriyor.</p><div class="tbl"><table><thead><tr><th>Donanım</th><th>Sonuç</th><th>En yüksek nokta</th><th>En yüksek q</th></tr></thead><tbody>')
for ad, durum, irt, q, yor in _fk:
    cls = "ok" if yor else ("bad" if "Max-Q" in durum else "")
    out.append(f'<tr><td>{E(ad)}</td><td class="{cls}">{E(durum)}</td><td class="num">{_n(round(irt))} km</td><td class="num">{q:.1f} kPa</td></tr>'.replace(".1f", ""))
out.append('</tbody></table></div><p class="note">Sonuç: başlangıç roketi tam gazla 6 km\'de Max-Q\'da parçalanıyor. Gaz kısmayı öğrenen oyuncu yükseğe çıkabiliyor ama yörüngeye giremiyor. Yörünge için iki kademe, otopilot, karbon gövde ve motor geliştirmesi birlikte gerekiyor; metan motor ve üç kademe Ay\'a gidecek kadar fazla hız bırakıyor. Ekonomi simülasyonundaki bölüm gereksinimleri bu sonuçlarla uyumlu.</p></section>')

out.append('<section><p class="eyebrow">Etki tablosu</p><h2>Engel aileleri roketi nasıl değiştirir</h2><p class="lead">19 davranışın her biri için: hangi değişkene dokunduğu, sayıları ve karşı önlemlerin etkisi.</p><div class="fx">')
for n, act, mem in FAMILIES:
    d, sayi, karsi = M.FAMILY_FX[n]
    out.append(f'<div><b>{E(n)}</b><span class="act">{E(d)}</span><p><i>Sayılar:</i> {E(sayi)}</p><p><i>Karşı önlem:</i> {E(karsi)}</p></div>')
out.append('</div></section>')

_bol = ["Baştan", "Üst atmosfer", "Yörünge", "Ay", "Mars yolu", "Asteroit kuşağı", "Jüpiter"]
out.append('<section><p class="eyebrow">Hangar</p><h2>Geliştirme ağacı</h2><p class="lead">Altı dal, her dalda altı kademe. Kademe fiyatı 220 × 1,95^(k−1) kredi; 3. kademeden itibaren bilim, 5. kademeden itibaren malzeme de ister. Her kademe belirli bir bölüme ulaşıldıktan sonra açılır.</p><div class="tbl"><table><thead><tr><th>Kademe</th><th>Kredi</th><th>Bilim</th><th>Malzeme</th><th>Açılış</th></tr></thead><tbody>')
for k in range(1, 7):
    out.append(f'<tr><td><b>{k}</b></td><td class="num">{_n(M.PRICE(k))}</td><td class="num">{M.SCIENCE[k]}</td><td class="num">{M.MATERIAL[k]}</td><td>{_bol[M.UNLOCK[k]]}</td></tr>')
out.append('</tbody></table></div><div class="tree2">')
for dal, items in M.TREE.items():
    out.append(f'<div class="br2"><h3>{E(dal)}</h3>')
    for i, (n, etki, bedel) in enumerate(items, 1):
        out.append(f'<div class="up"><span class="k">{i}</span><div><b>{E(n)}</b><p>{E(etki)}</p>' + (f'<p class="cost">{E(bedel)}</p>' if bedel != "—" else '') + '</div></div>')
    out.append('</div>')
out.append('</div></section>')

_bn = {c[0]: c[1] for c in chapters}
out.append('<section><p class="eyebrow">Modüller</p><h2>Uçuş öncesi takılan donanımlar</h2><p class="lead">Bir kez satın alınır, her uçuş öncesi sınırlı sayıdaki modül yuvasına takılır. Başlangıçta 2 yuva var, lojistik dalıyla 5\'e çıkar. Hangi modülü takacağını seçmek, uçuşun hedefine göre verilen bir karar.</p><div class="tbl"><table><thead><tr><th>Modül</th><th>Açılış</th><th>Kredi</th><th>Etki</th></tr></thead><tbody>')
for n, b_, fiyat, etki in M.MODULES:
    out.append(f'<tr><td><b>{E(n)}</b></td><td>{E(_bn[str(b_)])}</td><td class="num">{_n(fiyat)}</td><td>{E(etki)}</td></tr>')
out.append('</tbody></table></div></section>')

out.append('<section><p class="eyebrow">Yan araçlar</p><h2>Rokete eşlik edenler</h2><div class="tbl"><table><thead><tr><th>Araç</th><th>Açılış</th><th>Kredi</th><th>Etki</th></tr></thead><tbody>')
for n, b_, fiyat, etki in M.SIDE:
    out.append(f'<tr><td><b>{E(n)}</b></td><td>{E(_bn[str(b_)])}</td><td class="num">{_n(fiyat)}</td><td>{E(etki)}</td></tr>')
out.append('</tbody></table></div></section>')

_src = {x[0]: x[2] for x in legend}
out.append('<section><p class="eyebrow">Efsanevi geliştirmeler</p><h2>"Ağzımız açık kalsın" listesi</h2><p class="lead">Oyunun sonlarına doğru açılan, çoğu gerçek mühendislik fikirlerine dayanan geliştirmeler. Fiyatları, o bölümdeki bir uçuşun kazancının birkaç katı.</p><div class="cards legendary">')
for n, b_, kr, ma, etki in M.LEGEND:
    out.append(f'<div><b>{E(n)}</b><p>{E(etki)}</p><p class="cost">{E(_bn[str(b_)])} sonrası · {_n(kr)} kredi · {ma} malzeme</p><small>{E(_src.get(n, ""))}</small></div>')
out.append('</div></section>')

out.append('<section><p class="eyebrow">Etkileşimler</p><h2>Değişkenler birbirini nasıl etkiler</h2><div class="qs">')
for a_, b__ in M.INTERACTIONS:
    out.append(f'<div><b>{E(a_)}</b><p>{E(b__)}</p></div>')
out.append('</div></section>')

out.append('''<section><p class="eyebrow">Ekonomi</p><h2>Üç para birimi</h2>
<div class="cards">
<div><b>Kredi</b><p>Yükseklik ve mesafeden kazanılır. Geliştirmelerin ana bedeli.</p></div>
<div><b>Bilim</b><p>Aurora geçişi, örnek toplama, fotoğraf anları. Üst kademe geliştirmeleri açar.</p></div>
<div><b>Malzeme</b><p>He-3, buz, metan, nadir metal. Üsler ve efsanevi geliştirmeler için gerekir.</p></div>
</div>
__EKO__<p class="note"><b>Fotoğraf anları:</b> Ay'ın arkasından Dünya'nın doğuşu (Earthrise, 1968) ya da Plüton'dan geriye bakınca Dünya'nın tek bir piksel olarak görünmesi (Voyager 1'in 1990'daki "Soluk Mavi Nokta" fotoğrafı) gibi ünlü kareleri yakalamak, koleksiyon ve bonus bilim puanı veriyor.</p>
</section>
<section><p class="eyebrow">Görsel sistem</p><h2>Çocuk oyunu değil, belgesel sinema</h2>
<p class="lead">Telefonda her şeyi aynı kalitede yapmaya çalışmak oyunu kasar. Bu yüzden grafik üç katmanda düşünülüyor: her yerde geçerli sağlam bir <b>taban</b>, her bölümün tek bir <b>görsel imzası</b>, ve emeğin yığıldığı 4 <b>kahraman an</b>. Referans estetik: canlı roket yayınları ve uzay belgeselleri. Doygun, çizgi film renkleri yok.</p>
<div class="tiers">
<div><span class="tier">Katman 1</span><b>Taban</b><p>Her saniye, her bölümde</p></div>
<div><span class="tier">Katman 2</span><b>Bölüm imzası</b><p>Her bölümde tek, akılda kalan bir görüntü</p></div>
<div><span class="tier">Katman 3</span><b>Kahraman anlar</b><p>4 an, en yüksek kalite</p></div>
</div>

<h3>Katman 1 · Taban</h3>
<div class="cards">
<div><b>Roket</b><p>Metal ve boya malzemeli, Güneş yönünden gerçek zamanlı aydınlatılan model. <b>Her geliştirme roketin görünüşünü değiştirir:</b> kalkan takınca burun değişir, yelken açılınca gövdeden çıkar. Oyuncu ilerlemesini roketinde görür.</p></div>
<div><b>Egzoz</b><p>Parçacık tabanlı alev. Atmosferde dar ve uzun, yükseldikçe genişler; boşlukta dev bir yelpazeye dönüşür. Bu gerçek bir olay ve neredeyse bedava bir gerçekçilik hissi verir.</p></div>
<div><b>Işık</b><p>Tek ana ışık kaynağı Güneş. Gezegenlerden yansıyan zayıf dolgu ışığı, sinematik ton eşleme, sadece parlak kaynaklarda hafif ışık taşması (bloom).</p></div>
<div><b>Gökyüzü</b><p>Gerçek yıldız haritası: en parlak birkaç bin yıldız gerçek konum ve parlaklıklarıyla yerleştirilir, takımyıldızlar tanınabilir. Arkada Samanyolu bandı.</p></div>
<div><b>Hız hissi</b><p>Atmosferde katmanlı bulutlar, rüzgâr çizgileri ve ses hızında yoğuşma konisi. Uzayda yakın toz zerreleri, yıldızlarda paralaks ve hedefin büyümesi. FOV hızla birlikte açılır.</p></div>
<div><b>Kamera</b><p>Roketi hafif gecikmeyle izleyen takip kamerası. Sarsıntı aerodinamik basınçla orantılı; Max-Q'da en sert, uzayda tamamen yok.</p></div>
<div><b>Engellerin okunması</b><p>Gerçekçilikten önce okunaklılık. Her engel ailesinin tutarlı bir görsel dili var; ölümcül engellerde ince kırmızı, fırsatlarda turkuaz kenar ışığı var. Ekran dışından gelenler için kenarda ok.</p></div>
<div><b>Gösterge paneli</b><p>Canlı roket yayınlarındaki telemetri gibi sade: irtifa, hız, yakıt, aşama. Yazı tipi teknik ve küçük, ekranı kapatmaz.</p></div>
<div><b>Patlama</b><p>En sık görülen sahne olduğu için her zaman iyi olmalı. Atmosferde ateş topu ve duman; boşlukta ateş yok, sessiz bir parlama ve dağılan parçalar var (gerçekte de öyle). Kısa ağır çekim, sonra kara kutu.</p></div>
<div><b>Hangar</b><p>Roket, dramatik ışıklı bir hangarda dönen platformda duruyor. Geliştirme alındığında parça yerine oturur, kısa bir test ateşlemesi yapılır.</p></div>
</div>

<h3>Gerçekçilik kuralları</h3>
<ul class="rules">
<li><b>Güneş uzaklıkla küçülür ve sönükleşir.</b> Mars'ta 2/3'ü, Jüpiter'de 1/5'i, Plüton'da parlak bir yıldız kadar. Dış gezegenler kendiliğinden karanlık ve ürkütücü olur.</li>
<li><b>Havasız yerde gölgeler simsiyahtır.</b> Ay'da ve asteroitlerde sert, keskin gölgeler; atmosferi olan yerlerde yumuşak.</li>
<li><b>Uzayda ses yok.</b> Atmosferden çıkınca motor sesi gövde titreşimine dönüşür, dış sesler kesilir.</li>
<li><b>Ölçek dürüstlüğü.</b> Engeller oyun için gerçekte olduğundan yoğun yerleştirilir, ama gezegenlerin büyüklükleri ve renkleri doğru kalır.</li>
</ul>

<h3>Katman 2 · Bölüm imzaları</h3>
<div class="sig">
<div><span>1</span><b>Troposfer</b><p>Katmanlı bulut tavanını delip geçmek; aşağıda küçülen rampa ve şehir.</p></div>
<div><span>2</span><b>Üst atmosfer</b><p>Dünya'nın eğriliğinin ilk kez görünmesi, gece parlayan bulutların gümüş ışığı.</p></div>
<div><span>3</span><b>Yörünge</b><p>Gündüz–gece sınırı, gece yüzündeki şehir ışıkları, ufuktaki ince mavi atmosfer çizgisi ve aurora perdeleri.</p></div>
<div><span>4</span><b>Ay</b><p>Ay'ın arkasından Dünya'nın doğuşu; kraterli yüzeyde simsiyah gölgeler.</p></div>
<div><span>5</span><b>Mars</b><p>Pas renkli pus, ufukta Olympus Mons silueti, toz fırtınasında kararan Güneş.</p></div>
<div><span>6</span><b>Asteroit kuşağı</b><p>Binlerce dönen kaya; Kirkwood boşluğunda aniden açılan temiz koridor.</p></div>
<div><span>7</span><b>Jüpiter</b><p>Akan bulut bantları ve dönen Büyük Kırmızı Leke. Radyasyon arttıkça gösterge paneli bozulur ve karıncalanır.</p></div>
<div><span>9</span><b>Neptün ve Kuiper</b><p>Derin mavi gezegen, sonra zifiri karanlık. LIDAR taraması görünmez kayaları yeşil tarama çizgileriyle ortaya çıkarır.</p></div>
</div>
<p class="note">Bölüm 8 (Satürn) ve 10 (Plüton) kahraman anlara dahil.</p>

<h3>Katman 3 · Kahraman anlar</h3>
<div class="cards">
<div><b>Kármán geçişi</b><p>Gökyüzü maviden laciverte, sonra siyaha döner; yıldızlar birer birer belirir, ses kesilir, ufukta ince mavi çizgi kalır.</p></div>
<div><b>Satürn halkaları</b><p>Halka boşluğundan geçiş: iki yanda buz duvarları, gölgesi halkalara düşen gezegen.</p></div>
<div><b>Güneş dalışı</b><p>Ekran beyaza kayar, kalkan kenarları akkor turuncuya döner, ses kısılır. Ateşleme anında zaman yavaşlar.</p></div>
<div><b>Plüton'un kalbi</b><p>Mavi pusun içinden alçalış, buz dağlarının arasından kalp şeklindeki ovaya iniş ve zafer sinematiği.</p></div>
</div>

<h3>Yolculuk ekranı</h3>
<p class="note">Gezegenler arası uzun yolculuklar ve rota ekranı, görev kontrolündeki gibi sade bir güneş sistemi haritasıyla gösterilir. Haritada ince yörünge çizgileri, hayalet rota ve Lagrange otoyolları var. Zaman hızlandığında gezegenler yörüngelerinde akar.</p>

<h3>Performans bütçesi</h3>
<ul class="rules">
<li><b>Hedef:</b> orta seviye bir telefonda saniyede 60 kare, zayıf cihazlarda 30.</li>
<li><b>Otomatik kalite:</b> 3 kademe; kare hızı düşerse çözünürlük ve parçacık sayısı kendiliğinden azalır.</li>
<li><b>Sınırlar:</b> telefonda aynı anda en fazla ~2.000 parçacık; kayalar gibi tekrar eden nesneler tek seferde çizilir.</li>
</ul>

<h3>Yapılamayacaklar</h3>
<p class="note">Fotoğraf gerçekliğinde dokular (dış kaynaktan NASA görüntüsü yüklenemiyor; yüzeyler kodla üretilecek), telefonda gerçek hacimli bulutlar ve gerçekçi insan karakterleri bu kapsamda yok. Hedef AAA değil; tutarlı, şık ve inandırıcı bir görünüm.</p>
</section>
<section><p class="eyebrow">Hasar sistemi</p><h2>Roket hırpalanır, bükülür, parçalanır</h2>
<p class="lead">Telefonda gerçek metal simülasyonu çok ağır. Bunun yerine aynı hissi veren beş teknik bir arada kullanılıyor. Hasar sadece görüntü değil, uçuşu da değiştiriyor.</p>
<div class="cards">
<div><b>Göçükler</b><p>Çarpma noktasında gövde içeri göçer. Darbeler birikir; uçuş boyunca roket giderek hırpalanır.</p></div>
<div><b>Kopan parçalar</b><p>Kanatçık, anten, güneş paneli ve yelken darbe alınca kopar, dönerek uzaklaşır.</p></div>
<div><b>Bükülme</b><p>Max-Q'da ya da sert manevrada gövde yavaşça bükülür ve çatırdar. Bükük hâl Blender'da önceden hazırlanır, oyunda yumuşak geçişle uygulanır.</p></div>
<div><b>Parçalanma</b><p>Patlamada gövde, Blender'da önceden kesilmiş gerçekçi kırık parçalara ayrılır ve fizikle saçılır.</p></div>
<div><b>Yüzey izleri</b><p>Isı kararmaları, çizikler, delikler; Güneş'e yaklaşınca akkor hâle gelen kalkan kenarları.</p></div>
<div><b>Mekanik etki</b><p>Göçmüş motor tek taraflı itki verir ve roketi döndürür. Kopan kanatçık rotayı saptırır. Delinen tank yakıt sızdırır.</p></div>
</div>
<p class="note"><b>Hasar bölgeleri:</b> burun, tanklar, motor, kanatçıklar, panel ve yelkenler, aviyonik. Kara kutu raporu roketin hasar haritasını gösterir: "sol kanatçık 2,1 km'de kuşa çarparak koptu."</p>
</section>
<section><p class="eyebrow">Nesneler</p><h2>Hiçbir şey sahte durmasın</h2>
<p class="lead">Her nesnenin üç hâli var: uzaktan ucuz ama doğru siluet, yakından ayrıntılı model ve hareket, çarpışınca kendine özgü tepki. Kalite "gerektiği kadar": emek, oyuncunun gerçekten yakından gördüğü şeye harcanır.</p>
<div class="obj">
<div><b>Kuşlar</b><p><i>Hareket:</i> kanat çırpan modeller ve gerçek sürü davranışı: birbirini izleyen, dağılıp yeniden toplanan kuşlar. Roket yaklaşınca panikle dağılırlar.</p><p><i>Çarpışma:</i> tüy patlaması ve takla atan kuş; kan ve vahşet yok. Motor girişine giren kuş motoru tekletir.</p></div>
<div><b>Bulutlar</b><p><i>Hareket:</i> Güneş'le aydınlanan, katmanlı ve hacimli görünen bulut tabakaları.</p><p><i>Çarpışma:</i> roket bulutu delip geçerken arkasında bir tünel bırakır, kameraya su damlacıkları düşer, görüntü anlık bulanıklaşır.</p></div>
<div><b>Dolu ve yıldırım</b><p><i>Hareket:</i> hız çizgili buz taneleri; dallanan ve bulutları içeriden aydınlatan şimşekler, ardından gecikmeli gök gürültüsü.</p><p><i>Çarpışma:</i> dolu tanesi buz kırıntısına dönüşür ve göçük bırakır; yıldırım gösterge panelini kısa süre karartır.</p></div>
<div><b>Balonlar</b><p><i>Hareket:</i> rüzgârla salınan zarf ve altında sallanan yük.</p><p><i>Çarpışma:</i> zarf yırtılıp söner, yük paraşütle düşer.</p></div>
<div><b>Uçaklar</b><p><i>Hareket:</i> arkasında yoğuşma izi bırakan uzak siluetler.</p><p><i>Etki:</i> yakın geçişte uçağın türbülansı roketi sarsar; çarpışma kesin son.</p></div>
<div><b>Uydular ve uzay çöpü</b><p><i>Hareket:</i> kendi ekseninde yuvarlanan parçalar; güneş panelleri Güneş'i yakaladıkça parlar.</p><p><i>Çarpışma:</i> parçalar yeni parçalara bölünüp yeni engellere dönüşür (Kessler etkisi). Boşlukta ateş yok, sadece kıvılcım ve saçılan parçalar.</p></div>
<div><b>Asteroitler</b><p><i>Hareket:</i> her biri farklı biçimli, farklı hızda dönen kayalar; tekrar eden kopya yok.</p><p><i>Çarpışma:</i> toz bulutu ve kopan parçalar. Moloz yığını asteroitte roket çakıl denizine gömülür.</p></div>
<div><b>Halka buzları ve gayzerler</b><p><i>Hareket:</i> çakıl taşından ev büyüklüğüne buz parçaları Güneş'te parıldar; gayzerler arkadan aydınlanınca ışıldar.</p><p><i>Çarpışma:</i> buz kırılıp parıltılı kırıntılara dönüşür; gayzerin içinden geçen roket buz tutar.</p></div>
</div>
<h3>Sahtelik karşıtı kurallar</h3>
<ul class="rules">
<li><b>Hiçbir nesne donuk değil:</b> her şey döner, salınır, kanat çırpar ya da sürüklenir.</li>
<li><b>Tekrar yok:</b> boyut, renk, dönüş ve biçimde rastgele farklılık; aynı kayanın iki kopyası yan yana görünmez.</li>
<li><b>Tek Güneş:</b> her nesne aynı ışık kaynağıyla aydınlanır ve gölgesi doğru tarafa düşer.</li>
<li><b>Aniden belirme yok:</b> nesneler uzaklıkla yumuşakça belirir ve kaybolur.</li>
<li><b>Momentum:</b> büyük nesneye çarpmak daha çok iter; çarpışma tepkisi kütleyle orantılı.</li>
<li><b>Ortama uygunluk:</b> atmosferde ateş, duman ve ses; boşlukta sessiz parlama ve kıvılcım.</li>
</ul>
</section>
<section><p class="eyebrow">Ses</p><h2>Müzik, efektler ve anonslar</h2>
<p class="lead">Ses üç katmandan oluşuyor ve her biri ayarlardan ayrı ayrı kısılabiliyor. Ortak kural: atmosferde her şey duyulur, uzayda dışarıdan hiçbir şey gelmez; duyduğun her şey roketin gövdesinden ya da telsizden gelir.</p>
<h3>Ses efektleri</h3>
<div class="sfx">
<div><b>Motor</b><p>Gaz ve hava basıncına göre değişen gürleme. Kalkışta yeri titreten bas, irtifa arttıkça incelir; boşlukta gövdeden gelen boğuk bir uğultuya dönüşür. Motor tekleyince ses de tekler.</p></div>
<div><b>Rüzgâr ve gövde</b><p>Hızla artan rüzgâr uğultusu, Max-Q'da metalin gerilme sesi ve çatırtıları, bükülürken inleyen gövde.</p></div>
<div><b>Çarpışmalar</b><p>Her malzemenin kendi sesi: dolunun tıkırtısı, kuşun boğuk darbesi, metale metal çarpması, buz kırılması, kaya sürtünmesi. Uzayda bunlar dışarıdan değil, gövdenin içinden boğuk tok sesler olarak gelir.</p></div>
<div><b>Yanından geçenler</b><p>Kuş sürüsü, uçak ve balonlar yön ve uzaklığa göre sağdan soldan duyulur; hızla geçerken ses perdesi kayar.</p></div>
<div><b>Doğa olayları</b><p>Gecikmeli gök gürültüsü, yağmur ve dolu, bulut içinde değişen ses rengi. Radyasyon bölgesinde telsizde artan cızırtı, Jüpiter yakınında manyetik alanın garip vızıltısı.</p></div>
<div><b>Mekanik</b><p>Kademe ayrılmasındaki patlayıcı cıvatalar, yelken açılması, robot kol, drone fırlatma, iniş bacaklarının yere değmesi.</p></div>
<div><b>Uyarılar</b><p>Kısa ve ayırt edilebilir uyarı tonları: yaklaşan tehlike, düşük yakıt, aşırı ısınma, hasar. Her uyarının kendi tonu var, bakmadan anlaşılır.</p></div>
<div><b>Arayüz</b><p>Hangarda parça takılma sesi, satın alma onayı, kara kutu açılışında teyp sesi; hepsi kısa ve yumuşak.</p></div>
</div>
<h3>Müzik</h3>
<p class="note">Bölüme göre değişen ortam müziği: troposferde gergin bir ritim, yörüngede geniş ve sakin tonlar, Mars yolunda yalnızlık, Jüpiter'de derin bir uğultu, Plüton'da ana tema. Kahraman anlarda müzik yükselir; Güneş dalışında neredeyse tamamen susar ve yalnızca kalp atışına benzer bir nabız kalır.</p>
<h3>Telsiz anonsları</h3>
<p class="note">"Max-Q geçildi", "Kademe ayrıldı", "Yörüngedesin" gibi kısa anonslar telsiz hışırtısıyla birlikte üstte altyazı olarak gelir. Telefonun Türkçe ses motoru bunları seslendirebilir; sesin tonu telefona göre değişir ve istenirse kapatılır.</p>
<p class="note"><b>Nasıl üretilecek:</b> Efektlerin ve müziğin çoğu kodla, gerçek zamanlı üretilecek. Bu, sesin oyundaki duruma (hız, basınç, hasar) anlık tepki vermesini sağlar. Gerektiği yerlerde (patlama, metal gıcırtısı gibi) lisansı uygun ücretsiz ses kayıtları eklenebilir. Gerçekçi sınır: sonuç atmosferik ve tutarlı olur, ama stüdyoda kaydedilmiş orkestra müziği seviyesinde değil. Ses, tarayıcı kuralı gereği ekrana ilk dokunuşla başlar.</p>
</section>
<section><p class="eyebrow">Arayüz</p><h2>Ekranlar</h2>
<p class="lead">Dikey ekran; tek elle de oynanabilir. Görsel dil bu belgeyle aynı: görev kontrolü estetiği, sade telemetri, teknik yazı tipi.</p>
<div class="screens">
<div><b>Uçuş</b><p>Sol üstte irtifa, hız ve yakıt; sağ üstte uzay hava durumu ve hedef. Ekranın sol yarısında parmakla yön, sağ kenarda dikey gaz kaydırıcısı, altta iki buton: kademe ayır ve yan araç. Ekran dışı tehlikeler için kenarlarda oklar; telsiz altyazıları üstte.</p></div>
<div><b>Kara kutu</b><p>Patlamadan hemen sonra: irtifa ve hız grafiği ile ölüm noktası, roketin hasar haritası, ölüm nedeni ve "bunu çözen geliştirme" kartı. Büyük "Tekrar uç" butonu; patlamadan yeni kalkışa 3 saniye.</p></div>
<div><b>Hangar</b><p>Ortada dönen platformda roket; altta altı dal sekmesi; geliştirme kartlarında fiyat, etki ve kilit koşulu. Alınan parça roketin üzerine yerleşir.</p></div>
<div><b>Rota</b><p>Güneş sistemi haritası. Hedef ve sapanlar parmakla seçilir, hayalet rota çizgisi sonucu gösterir, fırlatma penceresi sayacı burada.</p></div>
<div><b>Koleksiyon</b><p>Yakalanan fotoğraf anları ve uçuşta açılan gerçek uzay bilgileri: küçük bir uzay ansiklopedisi.</p></div>
<div><b>Ayarlar</b><p>Grafik kalitesi (otomatik, yüksek, dengeli, pil tasarrufu), müzik, efekt ve anons seviyeleri ayrı ayrı.</p></div>
</div>
</section>
<section><p class="eyebrow">Hedef cihaz</p><h2>Samsung Galaxy S24 Ultra</h2>
<ul class="rules">
<li><b>Güç:</b> Snapdragon 8 Gen 3 ve Adreno 750 grafik birimi; tarayıcıda 3B için çok güçlü bir telefon.</li>
<li><b>Hedef:</b> kararlı 60 kare/sn. Ekran 120 Hz destekliyor, ama 120 kare telefonu ısıtır ve uzun oyunda performans düşer; 60 daha dengeli.</li>
<li><b>Çözünürlük:</b> ekran 1440×3120. Tam çözünürlük gereksiz yük; iç çözünürlük yaklaşık yarısı, kare hızına göre otomatik ayarlanır.</li>
<li><b>Bütçe:</b> bu telefonda roket gölgeleri, ışık taşması ve yaklaşık 8.000 parçacık rahat çalışır.</li>
<li><b>Isınma koruması:</b> uzun oyunda telefon ısınıp yavaşlarsa kalite bir kademe düşer.</li>
<li><b>Tarayıcı:</b> en iyi performans için oyunu Chrome'da açmak önerilir.</li>
</ul>
</section>
__EKSIK__<section><p class="eyebrow">Yol haritası</p><h2>Adım adım geliştirme</h2>
<div class="ms">
<div><b>A0 · Görsel prototip</b><p>Etkileşimsiz, 20 saniyelik bir sahne: Blender'dan çıkmış roket, rampadan kalkış, bulutları delme, kuş sürüsü, küçük bir çarpışma ve Kármán geçişi. Telefonunda grafiğin hissini ve akıcılığını test ediyorsun; beğenmezsen kodlamaya geçmeden yönü değiştiriyoruz.</p></div>
<div><b>A1 · Oynanabilir dilim: Kalkış → Yörünge</b><p>Bölüm 1–3, roket fiziği, bu bölümlerin engel aileleri, hasar sistemi, hangar (4 dal), kara kutu raporu, ses, kayıt sistemi. Burada "his" doğru mu diye birlikte karar veriyoruz.</p></div>
<div><b>A2 · Ay</b><p>Ay'a atış, sapan mekaniği, iniş, Ay Üssü checkpoint'i, yan araçların ilk dördü.</p></div>
<div><b>A3 · Mars ve Güneş</b><p>Uzay hava durumu, Güneş'in üç yüzü, atmosfer frenlemesi, Mars yakıt fabrikası.</p></div>
<div><b>A4 · Dış gezegenler ve Plüton</b><p>Bölüm 6–10, Büyük Tur, rezonans kombosu, efsanevi geliştirmeler, final sinematiği.</p></div>
</div>
<p class="note">Her adımın sonunda telefonundan oynayabileceğin bir link gelecek. Bir sonraki adıma, bir öncekinde konuştuklarımızı düzelttikten sonra geçeceğiz.</p>
</section>
<section><p class="eyebrow">Geliştirme tahmini</p><h2>Ne kadar sürer, ne kadar kullanım harcar</h2>
<div class="eko est"><div class="h"><span>Adım</span><span class="v">Oturum</span><span class="r">Kod</span></div>
<div><span>A0 · Görsel prototip</span><span class="v">1</span><span class="r">~1.500 satır</span></div>
<div><span>A1 · Kalkış → Yörünge</span><span class="v">4–6</span><span class="r">~7.000 satır</span></div>
<div><span>A2 · Ay</span><span class="v">3–4</span><span class="r">+3.000</span></div>
<div><span>A3 · Mars ve Güneş</span><span class="v">3–4</span><span class="r">+3.000</span></div>
<div><span>A4 · Dış gezegenler ve Plüton</span><span class="v">5–8</span><span class="r">+5.000</span></div>
<div><span>Cila, denge, hata ayıklama</span><span class="v">3–5</span><span class="r">—</span></div>
<div class="h"><span>Toplam</span><span class="v">~20–30</span><span class="r">~20.000 satır</span></div>
</div>
<p class="note">"Oturum" burada benim birkaç saat yoğun çalıştığım bir iş bloğu. Kodlama sohbetten çok daha fazla kullanım harcar: her adımda binlerce satır yazılıyor, ekran görüntüsüyle test ediliyor, düzeltiliyor. Pro aboneliğinde 5 saatlik kullanım penceresi yoğun kodlamayla 1–2 saatte dolabilir; haftalık bir sınır da var. Kesin sınırını göremiyorum, Ayarlar'daki Kullanım bölümünden takip edebilirsin. Kabaca takvim: günde 1–2 oturumla 4–8 hafta. Kullanımı azaltmak için büyük parçalar halinde çalışırım; sen de aralarda telefonunda test edip toplu geri bildirim verirsin.</p>
</section>
<section><p class="eyebrow">Kararlar</p><h2>Varsayılanlar (değiştirebilirsin)</h2>
<div class="qs">
<div><b>Telefon</b><p>Samsung Galaxy S24 Ultra. <i>Karar verildi.</i></p></div>
<div><b>Kamera ve ekran</b><p>Roketin arkasından takip eden 3B kamera, dikey ekran.</p></div>
<div><b>Gerçekçilik</b><p>Gerçek fizik kuralları; hayalet rota çizgisi ve rota ekranıyla öğretilir.</p></div>
<div><b>Uçuş süresi</b><p>İlk uçuşlar 30–60 saniye, ileri bölümlerde 3–4 dakika; uzun yolculuklarda zaman hızlandırma.</p></div>
<div><b>Ton</b><p>Ciddi belgesel havası; kara kutu raporlarında kısa, kuru bir mizah.</p></div>
<div><b>İsim</b><p>"Son Durak: Plüton". Kurgusal ajans adı sonra seçilebilir.</p></div>
<div><b>Dil</b><p>Türkçe. İngilizce sonra eklenebilir.</p></div>
<div><b>Modeller</b><p>Blender scriptleri ve NASA'nın ücretsiz modelleriyle ben hazırlarım; istersen elle katkı yapabilirsin.</p></div>
<div><b>Paylaşım</b><p>Önce sadece sen. Arkadaşlarınla paylaşmak istersen sayfanın paylaşım ayarından açarsın.</p></div>
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
_ek = open(os.path.join(HERE, "belge_ek.html")).read()
_den = '<section><p class="eyebrow">Tutarlılık denetimi</p><h2>Plan kendi kendini kontrol ediyor</h2><p class="lead">Bu belge her üretildiğinde aşağıdaki kontroller otomatik çalışır. Bir kural bozulursa burada kırmızı görünür.</p><div class="chk">'
for _ad, _ok, _h in _chk:
    _den += f'<div class="{"ok" if _ok else "bad"}"><span>{"✓" if _ok else "✗"}</span><p>{E(_ad)}' + (f'<br><small>{E("; ".join(_h))}</small>' if _h else '') + '</p></div>'
_den += '</div></section>'
page = page.replace("__EKSIK__", _ek + _den)
_rows = "".join(f'<div><span>{E(a)}</span><span class="v">{m:.0f}</span><span class="r">{lo}–{hi}</span></div>' for a, m, lo, hi in _eko_rows)
page = page.replace("__EKO__", '<h3>İlerleme simülasyonu</h3><p class="note">Kodlamadan önce ekonomi bir simülasyonla ayarlandı: kazanç derinlikle, fiyatlar kademeyle katlanarak artıyor. Her bölüm belirli dallarda belirli kademeler istiyor; oyuncu aynı yerde denedikçe ustalaşıyor. Sonuç (uçuş sayısı, medyan ve %10–90 aralığı):</p>'
    + f'<div class="eko"><div class="h"><span>Kilometre taşı</span><span class="v">Uçuş</span><span class="r">Aralık</span></div>{_rows}</div>'
    + f'<p class="note">Toplam: yaklaşık <b>{_eko_dk/60:.0f} saatlik</b> bir oyun. Bunlar ilk tahminler; gerçek denge A1\'den itibaren oynayarak ince ayarlanacak. Araç: <code>oyun/ekonomi_sim.py</code>.</p>')
for p in OUTS:
    open(p, "w").write(page)
print(f"engel={n_obs} yeni={n_new} gelistirme={n_upg} denge={tot}")
