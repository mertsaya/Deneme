# Tasarım belgesi sayfasını veri yapılarından üretir.
import html
E = html.escape

# etki türleri: kod -> (etiket, css sınıfı)
FX = {"P": ("Patlatır", "fx-p"), "Y": ("Yavaşlatır", "fx-y"), "S": ("Saptırır", "fx-s"), "I": ("İvme verir", "fx-i")}

chapters = [
 ("1", "Kalkış ve Troposfer", "0 – 12 km", 1.08,
  "Rampa sarsıntısıyla başlıyor, hava yoğun ve kalabalık. Oyuncu ilk uçuşta en fazla 3–4 km'ye çıkıp kuşlara ya da şimşeğe yeniliyor.",
  [("Pogo titreşimi", "0–1 km", "S", "Motor ve yakıt hattı rezonansa giriyor, roket sallanıyor.", "Pogo sönümleyici", "Saturn V'de gerçek sorun"),
   ("Kuş sürüsü", "0,5–3 km", "P", "Motor girişine giren kuş itkiyi tek taraflı keser, roket dönmeye başlar.", "Eskort drone, zırhlı burun", None),
   ("Termal sütun", "1–5 km", "I", "Sıcak hava kolonu yukarı doğru küçük bir itki verir.", "—", None),
   ("Rüzgâr kesmesi", "2–8 km", "S", "Ani yanal rüzgâr rotayı bozar.", "Jimbal motor", None),
   ("Fırtına bulutu ve yıldırım", "4–10 km", "P", "Yıldırım aviyoniği kapatır, kontrol birkaç saniye gider.", "Faraday kafesi", "Apollo 12'ye kalkışta iki kez yıldırım çarptı (1969)"),
   ("Buzlanma", "6–10 km", "Y", "Gövdede buz birikir, kütle artar.", "Isıtmalı gövde", None),
   ("Jet akımı", "9–12 km", "I", "Doğru yönde girersen ivme, ters açıda girersen sapma.", "Rota hesaplayıcı", None),
   ("Max-Q", "11–14 km", "P", "Çok hızlıysan aerodinamik basınç roketi parçalar. Gazı kısmayı öğrenmek zorundasın.", "Karbon gövde", "Her gerçek fırlatmada gaz bu noktada kısılır")]),
 ("2", "Üst Atmosfer", "12 – 100 km", 2.0,
  "Gökyüzü maviden laciverte, sonra siyaha döner. Oyunun ilk görsel 'vay' anı Kármán hattı.",
  [("Meteoroloji balonları", "15–35 km", "P", "Rastgele yükselen balonlarla çarpışma.", "Engel radarı", None),
   ("Kademe ayırma penceresi", "60–80 km", "I", "Boş kademeyi doğru anda atarsan ani ivme, geç kalırsan ölü ağırlık.", "Çok kademeli roket", None),
   ("Kırmızı sprite şimşekleri", "50–90 km", "P", "Bulutların üzerinde çakan kısa elektrik boşalmaları.", "Faraday kafesi +", "Gerçek üst atmosfer olayı"),
   ("Göktaşı izleri", "70–100 km", "Y", "Yanan küçük göktaşı parçaları gövdeyi döver.", "Whipple kalkanı", None),
   ("Kármán hattı", "100 km", "I", "Uzayın başlangıcı. Sinematik an, bilim puanı ve ilk büyük ödül.", "—", "Uzayın uluslararası kabul gören sınırı")]),
 ("3", "Yörünge", "100 – 2.000 km", 2.6,
  "Yukarı çıkmak yetmiyor. Saniyede 7,8 km yatay hıza ulaşmazsan düşersin. Oyuncu burada gerçek roket fiziğini keşfediyor.",
  [("Yerçekimi dönüşü", "100–200 km", "Y", "Dik çıkmakta ısrar edersen yörüngeye giremez, geri düşersin.", "Otopilot", "Gerçek fırlatmalarda roket yavaşça yatar"),
   ("Termosfer sürtünmesi", "100–400 km", "Y", "İnce ama etkili hava direnci.", "—", None),
   ("Aurora perdesi", "100–300 km", "S", "Manyetik alan pusulayı saptırır, ama geçiş bilim puanı kazandırır.", "Yıldız izleyici", None),
   ("Uzay istasyonu", "400 km", "I", "Yanaşabilirsen yakıt ikmali alırsın.", "Yanaşma sistemi", None),
   ("Uzay çöpü kuşağı", "600–1.000 km", "P", "Çarptığın her parça yeni parçalara bölünür ve tehlike zincirleme büyür.", "Whipple kalkanı, robot kol", "Kessler sendromu"),
   ("Ölü uydu", "800 km", "I", "Robot kolla yakalarsan hurda kredisi verir.", "Robot kol (yan araç)", None),
   ("Van Allen iç kuşağı", "1.000+ km", "P", "Radyasyon aviyoniği sıfırlar.", "Radyasyon zırhı", "Gerçek radyasyon kuşağı")]),
 ("4", "Ay", "384.400 km", 5.58,
  "İlk gerçek yolculuk. Yörüngeden kopma anını doğru zamanlamak ve Ay'ın yerçekimini kullanmak gerekiyor.",
  [("Ay'a atış zamanlaması", "Dünya yörüngesi", "I", "Motoru Dünya'ya en yakın noktada yakarsan çok daha fazla hız kazanırsın.", "Yörünge hesaplayıcı", "Oberth etkisi"),
   ("L1 Lagrange noktası", "~326.000 km", "S", "Dengesiz bölge, roketi yavaşça sürükler.", "Hassas iticiler", None),
   ("Ay sapanı", "Ay yakını", "I", "Doğru açıyla geçersen yakıt harcamadan büyük ivme, yanlışsa çarpma.", "Rota hesaplayıcı", "Apollo 13 dönüşünde kullanıldı"),
   ("Masconlar", "Ay yörüngesi", "S", "Ay'ın düzensiz kütle yoğunlukları yörüngeyi bozar.", "Otopilot +", "Gerçek, Apollo'da keşfedildi"),
   ("Regolit tozu", "İniş", "Y", "İnişte kalkan toz görüşü kapatır.", "LIDAR", None),
   ("Ay Üssü", "Ödül", "I", "Kurulunca sonraki uçuşlar Ay'dan başlayabilir. He-3 madenciliği açılır.", "—", None)]),
 ("5", "Mars Yolu", "~78 milyon km", 7.89,
  "Güneş artık bir tehdit. Uzun yolculuk boyunca fırtınalar gelir, Mars'a varınca da atmosfere doğru açıyla girmek gerekir.",
  [("Güneş patlaması (CME)", "Yol boyu", "P", "Dev plazma dalgası. Kalkansızsan ölümcül; plazma emici kalkanla ise ivmeye dönüşür.", "Plazma emici kalkan", None),
   ("Güneş rüzgârı", "Yol boyu", "I", "Güneş yelkenin varsa sürekli küçük ivme verir.", "Güneş yelkeni", "IKAROS yelkeni 2010'da uçtu"),
   ("Mikrometeoroid yağmuru", "Yol boyu", "Y", "Küçük ama sürekli çarpışmalar.", "Whipple kalkanı", None),
   ("Phobos", "Mars yakını", "I", "Küçük ama kullanışlı bir sapan.", "—", None),
   ("Atmosfer frenlemesi", "Mars atmosferi", "Y", "Dik girersen yanarsın, sığ girersen sekip uzaya kaçarsın. Doğru açı yakıtsız yavaşlatır.", "Ablatif ısı kalkanı", "Gerçek iniş tekniği"),
   ("Toz fırtınası", "Mars yüzeyi", "S", "Görüşü ve güneş enerjisini keser.", "RTG", None)]),
 ("6", "Asteroit Kuşağı", "~300 milyon km", 8.48,
  "Oyunun 'kaçış' bölümü. Dönen kayalar, madencilik fırsatları ve Ceres.",
  [("Çarpışma kümesi", "Kuşak içi", "P", "Yoğun ve dönen kaya alanı.", "Otomatik kaçınma", None),
   ("Madenlik asteroit", "Kuşak içi", "I", "Yanaşıp kazarsan nadir metal kazanırsın.", "Madenci drone", None),
   ("Ceres sapanı", "Ceres", "I", "Orta büyüklükte ivme.", "—", None)]),
 ("7", "Jüpiter", "~630 milyon km", 8.8,
  "Hem en büyük ödül hem en büyük tehlike: oyunun en güçlü sapanı ile en ölümcül radyasyonu bir arada.",
  [("Jüpiter sapanı", "Jüpiter yakını", "I", "Oyundaki en büyük ivme.", "Rota hesaplayıcı", "Voyager ve New Horizons kullandı"),
   ("Radyasyon kuşakları", "Jüpiter yakını", "P", "Güneş sistemindeki en sert radyasyon.", "Manyetik kalkan", None),
   ("Io plazma halkası", "Io yörüngesi", "I", "Elektrodinamik ipin varsa elektrik üretir.", "Elektrodinamik ip", None),
   ("Güneş enerjisi sınırı", "Jüpiter ötesi", "Y", "Güneş panelleri artık yetmez, nükleer enerji gerekir.", "RTG", "Gerçek: dış gezegen sondaları RTG kullanır")]),
 ("8", "Satürn", "~1,3 milyar km", 9.11,
  "Görsel olarak oyunun zirvesi: halkaların arasından geçiş.",
  [("Halka geçişi", "Halka boşluğu", "P", "Buz parçalarının arasından dar bir koridor.", "Otomatik kaçınma", "Cassini 2017'de bu boşluktan 22 kez geçti"),
   ("Titan", "Titan", "Y", "Kalın atmosfer frenler, metan gölleri yakıt verir.", "Ablatif ısı kalkanı", None),
   ("Enceladus gayzerleri", "Enceladus", "S", "Buz püskürtüleri iter; içinden geçmek su toplar.", "—", None)]),
 ("9", "Uranüs, Neptün ve Kuiper", "2,7 – 4,5 milyar km", 9.55,
  "Karanlık, soğuk ve sessiz. Engeller artık görünmüyor, sensörlerle uçmak gerekiyor.",
  [("Neptün rüzgârları", "Neptün atmosferi", "S", "Saatte 2.000 km'yi aşan, Güneş sisteminin en hızlı rüzgârları.", "—", None),
   ("Triton gayzerleri", "Triton", "S", "Azot püskürtüleri.", "—", None),
   ("Karanlık Kuiper nesneleri", "Kuiper kuşağı", "P", "Görünmez buz kayaları. Radar olmadan kör uçarsın.", "LIDAR, radar", None)]),
 ("10", "Plüton: Zafer", "~5,9 milyar km", 9.77,
  "Plüton ve Charon birbirinin etrafında dans ediyor. Hedef, Plüton'un kalp şeklindeki ovasına inmek.",
  [("Plüton–Charon ikilisi", "Plüton sistemi", "S", "İki yerçekimi merkezi aynı anda çeker.", "Yörünge hesaplayıcı", None),
   ("Tombaugh Regio'ya iniş", "Final", "I", "Kalp şeklindeki azot buzu ovası. Zafer sinematiği.", "—", "New Horizons 2015'te fotoğrafladı")]),
]

tree = [
 ("İtki", ["Kerosen motor", "Metan motor (yeniden ateşleme)", "Nükleer termal motor", "İyon motoru", "Füzyon motoru"], "Nükleer termal motor 1960'larda NERVA programında yer testlerinden geçti."),
 ("Gövde ve kalkan", ["Alüminyum gövde", "Karbon kompozit", "Ablatif ısı kalkanı", "Whipple kalkanı", "Manyetik radyasyon kalkanı"], "Whipple kalkanı, çarpan parçayı ince bir ön katmanda buharlaştırır. Uzay istasyonunda kullanılıyor."),
 ("Aviyonik", ["Yerçekimi dönüşü otopilotu", "Engel radarı", "Otomatik kaçınma", "Rota hesaplayıcı (hayalet rota çizgisi)", "Pilot zekâ: kısa süreli ağır çekim"], "Rota hesaplayıcı, sapan manevrasının sonucunu önceden çizer."),
 ("Enerji", ["Batarya", "Güneş paneli", "Yakıt hücresi", "RTG (nükleer pil)", "Kompakt füzyon"], "Jüpiter'den sonra güneş paneli yetmez. Bu, oyunun doğal bir ilerleme kapısı."),
 ("Lojistik", ["2 kademe", "3 kademe ve booster dönüşü", "Yakıt tankeri randevusu", "Ay Üssü", "Mars yakıt fabrikası"], "Üsler checkpoint işlevi görür. Kurulunca yolculuk oradan devam edebilir."),
]

side = [
 ("Eskort drone", "Roketin önünde uçar, kuşları ve balonları dağıtır. Sınırlı şarjı var."),
 ("Kurtarma kapsülü", "Patlamadan hemen önce fırlatılırsa o uçuşta kazanılanların yarısını kurtarır."),
 ("Keşif sondası", "Önden gider, 30 saniye boyunca yaklaşan engelleri haritada gösterir."),
 ("Booster dönüşü", "Ayrılan kademe Dünya'ya geri iner. Mini oyunu başarırsan kredinin bir kısmı geri gelir."),
 ("Robot kol", "Ölü uyduları ve uzay çöpünü yakalar, hurdayı krediye çevirir."),
 ("Madenci drone", "Asteroitten metal, Europa'dan buz, Titan'dan metan toplar."),
]

legend = [
 ("Skyhook", "Dünya yörüngesinde dönen dev bir halat roketi yakalar ve sapan gibi fırlatır.", "Ciddi olarak çalışılmış bir mühendislik kavramı"),
 ("Lazer yelken", "Dünya'daki dev bir lazer dizisi yelkeni iter. Ekranda Dünya'dan gelen ışık sütunu görünür.", "Breakthrough Starshot projesi, 2016"),
 ("Orion darbesi", "Roketin arkasında küçük nükleer patlamalar art arda itki verir. Oyunun en çarpıcı efekti.", "Orion Projesi, 1958–1965"),
 ("Plazma emici kalkan", "Güneş fırtınasının enerjisini emip ivmeye çevirir. En büyük tehdit ödüle dönüşür.", "Kurgusal, oyun için"),
 ("Ay kütle sürücüsü", "Ay Üssü'nden elektromanyetik rayla fırlatma. Yakıt harcamadan derin uzaya çıkış.", "Gerard O'Neill, 1970'ler"),
 ("Uzay asansörü", "Son aşama: Dünya'dan kalkışı tamamen atlar, Plüton denemelerini hızlandırır.", "Kavram; malzeme henüz yok"),
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

def fxchip(c):
    l, cls = FX[c]; return f'<span class="chip {cls}">{l}</span>'

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
  --flame:#ff9a3c; --ion:#55d6c2; --danger:#ff5d6c; --slow:#f2c14e; --drift:#a993ff;
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
/* rota şeridi */
.route{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:16px 12px 12px}
.route svg{width:100%;height:auto;display:block}
.route .cap{color:var(--faint);font-size:.8rem;margin-top:6px}
/* pazar */
.mk{display:flex;flex-direction:column;border-top:1px solid var(--line)}
.mk > div{display:grid;grid-template-columns:minmax(0,11rem) minmax(0,1fr);gap:4px 16px;padding:12px 0;border-bottom:1px solid var(--line)}
.mk b{font-family:var(--f-display);font-size:1.12rem}
.mk .plat{font-family:var(--f-mono);font-size:.72rem;color:var(--faint);display:block}
.mk .what{color:var(--dim)}
.mk .take{grid-column:2}
@media (max-width:520px){.mk > div{grid-template-columns:1fr}.mk .take{grid-column:1}}
.pos{background:var(--panel2);border:1px solid var(--line);border-radius:8px;padding:16px;display:flex;flex-direction:column;gap:10px}
.pos ul{margin:0;padding-left:1.1em;display:flex;flex-direction:column;gap:6px}
/* bölümler */
.legend{display:flex;flex-wrap:wrap;gap:6px}
.chip{display:inline-block;font-family:var(--f-mono);font-size:.7rem;letter-spacing:.06em;text-transform:uppercase;padding:2px 7px;border-radius:3px;border:1px solid currentColor;white-space:nowrap}
.fx-p{color:var(--danger)} .fx-y{color:var(--slow)} .fx-s{color:var(--drift)} .fx-i{color:var(--ion)}
.ch{border-top:1px solid var(--line);padding-top:22px;display:flex;flex-direction:column;gap:12px}
.ch-head{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
.ch-no{font-family:var(--f-mono);color:var(--flame);font-size:.85rem}
.ch-dist{font-family:var(--f-mono);font-size:.78rem;color:var(--dim);margin-left:auto;font-variant-numeric:tabular-nums}
.ch > p{color:var(--dim)}
.obs{display:flex;flex-direction:column;gap:8px}
.ob{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px 12px;background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:11px 12px}
.ob .nm{font-weight:600}
.ob .at{font-family:var(--f-mono);font-size:.74rem;color:var(--faint);font-variant-numeric:tabular-nums}
.ob .ds{grid-column:1 / -1;color:var(--dim);font-size:.92rem;line-height:1.5}
.ob .ct{grid-column:1 / -1;font-size:.84rem;display:flex;flex-wrap:wrap;gap:4px 14px}
.ob .ct span{color:var(--faint)}
.ob .ct i{font-style:normal;color:var(--star)}
.ob .real{color:var(--flame);font-size:.8rem}
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
/* yol haritası */
.ms{display:flex;flex-direction:column;gap:0;border-left:1px solid var(--line);margin-left:6px}
.ms > div{position:relative;padding:0 0 18px 20px;display:flex;flex-direction:column;gap:3px}
.ms > div::before{content:"";position:absolute;left:-5px;top:7px;width:9px;height:9px;border-radius:50%;background:var(--void);border:2px solid var(--flame)}
.ms > div:first-child::before{background:var(--flame)}
.ms b{font-family:var(--f-display);font-size:1.2rem}
.ms p{color:var(--dim);font-size:.93rem}
.qs{display:flex;flex-direction:column;gap:10px;counter-reset:q}
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
<p class="eyebrow">Oyun tasarım belgesi · Taslak 1 · Tartışma için</p>
<h1>Son Durak:<br><em>Plüton</em></h1>
<p class="pitch">Dünya'dan kalkan bir roket her denemede biraz daha uzağa gidiyor. Önce atmosfer, sonra yörünge, Ay, Mars ve sonunda Plüton. Her patlamadan sonra hangarda geliştirme yapıyor, bir sonraki denemede bir önceki seni öldüren engeli aşıyorsun.</p>
<div class="loop">
<div><b>Kalk</b><span>Gazı ve rotayı yönet</span></div>
<div><b>Düş</b><span>Kara kutu raporu: neden patladın?</span></div>
<div><b>Geliştir</b><span>5 dal, 25 geliştirme, yan araçlar</span></div>
<div><b>Uzağa</b><span>Üs kur, oradan devam et</span></div>
</div>
</header>
''')

# rota şeridi: log10(km), 1..10
W, H = 720, 210
x0, x1 = 40, 700
def X(v): return x0 + (v - 1) / 9 * (x1 - x0)
svg = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Dünya\'dan Plüton\'a logaritmik rota">']
svg.append(f'<line x1="{x0}" y1="110" x2="{x1}" y2="110" stroke="var(--line)" stroke-width="2"/>')
for k in range(1, 11):
    svg.append(f'<line x1="{X(k):.1f}" y1="104" x2="{X(k):.1f}" y2="116" stroke="var(--faint)" stroke-width="1"/>')
    lab = {1:"10 km",2:"100 km",3:"1.000",4:"10⁴",5:"10⁵",6:"1 mn km",7:"10⁷",8:"10⁸",9:"1 mr km",10:"10¹⁰"}[k]
    svg.append(f'<text x="{X(k):.1f}" y="134" fill="var(--faint)" font-family="IBM Plex Mono,monospace" font-size="11" text-anchor="middle">{lab}</text>')
names = {"1":"Troposfer","2":"Kármán","3":"Yörünge","4":"Ay","5":"Mars","6":"Kuşak","7":"Jüpiter","8":"Satürn","9":"Neptün","10":"Plüton"}
for i,(no, t, d, lg, *_ ) in enumerate(chapters):
    up = i % 2 == 0
    y = 74 if up else 160
    col = "var(--flame)" if no == "10" else "var(--ion)"
    svg.append(f'<line x1="{X(lg):.1f}" y1="110" x2="{X(lg):.1f}" y2="{86 if up else 146}" stroke="{col}" stroke-width="1" stroke-dasharray="2 3"/>')
    svg.append(f'<circle cx="{X(lg):.1f}" cy="110" r="{6 if no=="10" else 4.5}" fill="{col}"/>')
    anchor = "end" if lg > 9.6 else ("start" if lg < 1.5 else "middle")
    svg.append(f'<text x="{X(lg):.1f}" y="{y}" fill="var(--star)" font-family="Saira Condensed,Arial Narrow,sans-serif" font-size="15" font-weight="700" text-anchor="{anchor}">{E(names[no])}</text>')
    svg.append(f'<text x="{X(lg):.1f}" y="{y+(-16 if up else 16)}" fill="var(--dim)" font-family="IBM Plex Mono,monospace" font-size="10.5" text-anchor="{anchor}">{no}</text>')
svg.append(f'<text x="{x0}" y="22" fill="var(--dim)" font-family="IBM Plex Mono,monospace" font-size="11">DÜNYA\'DAN UZAKLIK · LOGARİTMİK ÖLÇEK</text>')
svg.append('</svg>')

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
<li><b>Hem itki hem tehdit.</b> Aynı olay donanıma göre öldürür ya da hızlandırır. Güneş fırtınası kalkansız roketi yok eder, plazma kalkanlı roketi fırlatır.</li>
<li><b>Üsler checkpoint işlevi görür.</b> Ay Üssü kurunca Dünya'dan kalkış tekrarı biter, oyun uzunluğu kontrol altında kalır.</li>
</ul></div></section>
''')

out.append('<section><p class="eyebrow">Engeller ve itkiler</p><h2>Bölüm bölüm konumlandırma</h2>')
out.append('<div class="legend">' + "".join(fxchip(c) for c in "PYSI") + '</div>')
out.append('<p class="note">Turuncu notlar gerçekte yaşanmış ya da gerçek fiziğe dayanan olayları işaretliyor.</p>')
for no, t, d, lg, desc, obs in chapters:
    out.append(f'<div class="ch"><div class="ch-head"><span class="ch-no">BÖLÜM {no}</span><h3>{E(t)}</h3><span class="ch-dist">{E(d)}</span></div><p>{E(desc)}</p><div class="obs">')
    for nm, at, fx, ds, ct, real in obs:
        r = f'<span class="real">{E(real)}</span>' if real else ''
        out.append(f'<div class="ob"><div><div class="nm">{E(nm)}</div><div class="at">{E(at)}</div></div><div>{fxchip(fx)}</div><p class="ds">{E(ds)}</p><div class="ct"><span>Karşılığı: <i>{E(ct)}</i></span>{r}</div></div>')
    out.append('</div></div>')
out.append('</section>')

out.append('<section><p class="eyebrow">Hangar</p><h2>Geliştirme ağacı</h2><p class="lead">Beş dal, her dalda beş kademe. Bir sonraki kademe hem kredi hem de ilgili bölümde toplanan bilim puanı istiyor, böylece geri dönüp keşif yapmak anlam kazanıyor.</p><div class="tree">')
for n, items, note in tree:
    out.append(f'<div class="br"><h3>{E(n)}</h3><ol>' + "".join(f'<li>{E(i)}</li>' for i in items) + f'</ol><p>{E(note)}</p></div>')
out.append('</div></section>')

out.append('<section><p class="eyebrow">Yan araçlar</p><h2>Rokete eşlik edenler</h2><div class="cards">')
for n, d in side:
    out.append(f'<div><b>{E(n)}</b><p>{E(d)}</p></div>')
out.append('</div></section>')

out.append('<section><p class="eyebrow">Efsanevi geliştirmeler</p><h2>"Ağzımız açık kalsın" listesi</h2><p class="lead">Oyunun sonlarına doğru açılan, ekranda çok etkileyici duran ve çoğu gerçek mühendislik fikirlerine dayanan altı geliştirme.</p><div class="cards legendary">')
for n, d, s in legend:
    out.append(f'<div><b>{E(n)}</b><p>{E(d)}</p><small>{E(s)}</small></div>')
out.append('</div></section>')

out.append('''<section><p class="eyebrow">Ekonomi</p><h2>Üç para birimi</h2>
<div class="cards">
<div><b>Kredi</b><p>Yükseklik ve mesafeden kazanılır. Geliştirmelerin ana bedeli.</p></div>
<div><b>Bilim</b><p>Aurora geçişi, örnek toplama, fotoğraf anları. Üst kademe geliştirmeleri açar.</p></div>
<div><b>Malzeme</b><p>He-3, buz, metan, nadir metal. Üsler ve efsanevi geliştirmeler için gerekir.</p></div>
</div>
<p class="note"><b>Fotoğraf anları:</b> Ay'ın arkasından Dünya'nın doğuşu (Earthrise, 1968) ya da Satürn'den bakınca Dünya'nın "Soluk Mavi Nokta" olarak görünmesi gibi ünlü kareleri yakalamak, koleksiyon ve bonus bilim puanı veriyor.</p>
</section>
''')

out.append('''<section><p class="eyebrow">Görsel yön</p><h2>Çocuk oyunu değil, belgesel sinema</h2>
<div class="cards">
<div><b>Gökyüzü</b><p>Fiziksel tabanlı atmosfer gölgelendiricisi: yükseldikçe mavi laciverte, sonra siyaha döner, ufukta ince mavi çizgi kalır.</p></div>
<div><b>Ateş ve duman</b><p>Parçacık tabanlı egzoz, ışık patlaması (bloom), sıcak hava titremesi, kalkışta rampa dumanı.</p></div>
<div><b>Patlama</b><p>Ağır çekim, parçalara ayrılan gövde, kamera sarsıntısı ve ardından kara kutu ekranı.</p></div>
<div><b>Gezegenler</b><p>Prosedürel dokular: bulutlar, Jüpiter'in bantları, Satürn'ün halkaları, Plüton'un kalbi.</p></div>
</div>
<p class="note"><b>Gerçekçi sınır:</b> Tarayıcıda çalışan Three.js ile sinematik bir görünüm mümkün, ama AAA oyun seviyesi değil. Dış kaynaklardan NASA dokuları yüklenemiyor, bu yüzden gezegen yüzeyleri kodla üretilecek. Telefonda akıcı kalması için grafik kalitesi cihaza göre otomatik ayarlanacak.</p>
</section>
''')

out.append('''<section><p class="eyebrow">Yol haritası</p><h2>Adım adım geliştirme</h2>
<div class="ms">
<div><b>A1 · Oynanabilir dilim: Kalkış → Yörünge</b><p>Bölüm 1–3, roket fiziği, 20 engel, hangar (3 dal), kara kutu raporu, atmosfer geçişi. Burada "his" doğru mu diye birlikte karar veriyoruz.</p></div>
<div><b>A2 · Ay</b><p>Ay'a atış, sapan mekaniği, iniş, Ay Üssü checkpoint'i, yan araçların ilk üçü.</p></div>
<div><b>A3 · Mars</b><p>Güneş fırtınası, atmosfer frenlemesi, Mars yakıt fabrikası.</p></div>
<div><b>A4 · Dış gezegenler ve Plüton</b><p>Bölüm 6–10, efsanevi geliştirmeler, final sinematiği.</p></div>
</div>
<p class="note">Her adımın sonunda telefonundan oynayabileceğin bir link gelecek. Bir sonraki adıma, bir öncekinde konuştuklarımızı düzelttikten sonra geçeceğiz.</p>
</section>
''')

out.append('''<section><p class="eyebrow">Tartışalım</p><h2>Karar vermemiz gerekenler</h2>
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
<a href="https://www.mlwgames.com/news/509/kerbal-space-program-rockets-to-its-highest-player-count-on-steam">Kerbal Space Program oyuncu sayısı ve Steam değerlendirmeleri</a>
<a href="https://raijin.gg/app/1718870/Spaceflight_Simulator">Spaceflight Simulator satış tahminleri</a>
<a href="https://toucharcade.com/2014/11/28/earn-to-die-2-review/">Earn to Die 2 incelemesi</a>
<a href="https://www.appspy.com/earn-to-die-review">Earn to Die incelemesi</a>
</div></section>
</div>
<script>
// Hero arka planı: yavaş akan yıldızlar ve yükselen ince bir egzoz izi.
(function(){
  const c=document.getElementById('sky'); if(!c) return;
  const x=c.getContext('2d'); let w,h,st=[];
  function size(){ const r=c.getBoundingClientRect(), d=Math.min(devicePixelRatio||1,2);
    w=c.width=r.width*d; h=c.height=r.height*d;
    st=Array.from({length:120},()=>({x:Math.random()*w,y:Math.random()*h,z:Math.random()*0.8+0.2})); }
  size(); addEventListener('resize',size);
  const still=matchMedia('(prefers-reduced-motion: reduce)').matches;
  function frame(t){
    x.clearRect(0,0,w,h);
    for(const s of st){ s.y+= still?0:s.z*0.35; if(s.y>h){s.y=0;s.x=Math.random()*w;}
      x.fillStyle=`rgba(233,238,248,${0.25+s.z*0.6})`; x.fillRect(s.x,s.y,s.z*2,s.z*2); }
    const px=w*0.86, py=h*(0.75-0.04*Math.sin(t/1400));
    const g=x.createLinearGradient(px,py,px,h); g.addColorStop(0,'rgba(255,154,60,.9)'); g.addColorStop(1,'rgba(255,154,60,0)');
    x.fillStyle=g; x.fillRect(px-1.5,py,3,h-py);
    x.fillStyle='#e9eef8'; x.beginPath(); x.moveTo(px,py-22); x.lineTo(px+5,py-6); x.lineTo(px+5,py); x.lineTo(px-5,py); x.lineTo(px-5,py-6); x.closePath(); x.fill();
    if(!still) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();
</script>
''')
open('tasarim.html','w').write("".join(out))
print("ok")
