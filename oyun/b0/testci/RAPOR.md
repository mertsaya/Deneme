# B0 kabul raporu (otomatik: testci/kabul.py)

Sayfa: `index.html` · Koşu: 2026-10-08 20:07 · Süre: 80 s · Konsol hatası: 2

| K | Ölçüt | Durum | Ayrıntı |
|---|---|---|---|
| K1 | Vay anı <=5 s (>=%90) | **GECTI** | vay_t<=5s orani: iyi %90, hic %100 (hedef >=%90) |
| K2 | Tur 1 süresi 16-30 s, 65 s'ye çarpma yok | **GECTI** | ort tur suresi 16.2s (16-30), 65s'ye carpan 0 |
| K3 | Beceri farkı (1,30 / 1,60) | **GECTI** | tur1 iyi/hic mesafe orani 1.63 (>=1,30); tur5 sv={'rampa': 4, 'yakit_ac': 1, 'dalis': 2, 'yakit_s': 2}: 2.69 (>=1,60) |
| K4 | Satın alma ritmi | **BILGI** | iyi: en uzun alisverissiz 1 (<=3); orta: en uzun alisverissiz 1 (<=3); hic: en uzun alisverissiz 2 (<=3) |
| K5 | Ses duvarı tur | **BILGI** | ses duvari ilk kirilis medyan tur: {'iyi': 4, 'orta': 4, 'hic': 6} (iyi 2-3, hic <=8) |
| K6 | Kampanya tur süresi | **BILGI** | iyi t5-15 sure medyan 53.3s, tavan %3; orta t5-15 sure medyan 23.6s, tavan %0; hic t5-15 sure medyan 20.3s, tavan %0 (hedef 20-40s, tavan <=%5) |
| K7 | Yeniden başlatma <=0,5 / <=3 s | **GECTI** | TEKRAR UC -> RAMPA 0.45s (<=0,5), BITIS->KARA_KUTU 1.01s, bitis->rampa toplam ~1.86s (<=3), igne ilerliyor=True. Animasyon sirasinda TEKRAR UC ayri elle bakilmali |
| K8 | Sim eşliği (>=200 tohum) | **GECTI** | n=40; ayar_uret --denetle temiz; tum olculer uyumlu |
| K9 | Belirlenimlilik | **GECTI** | ayni tohum ayni sonuc=True; hiz=4 vs hiz=8 olay gunlugu ayni=True (hiz=1 yerine 4 kullanildi, sure icin) |
| K10 | Mantık denetimi (debug) | **GECTI** | debug=1 toplu=20: konsol uyari/hata 0; __oyun.uyarilar=0. NOT: oyun enerji denetimini konsola uyari olarak yazmali (uyar/enerji/ihlal ya da console.warn); yazmiyorsa bu madde guvenilir degil |
| K11 | Kare hızı (telefon) | **ELLE** | telefon olcumu sart; headless swiftshader bilgisi: fps ort 58 min 20 |
| K12 | Kararlılık, 0 konsol hatası | **GECTI** | kampanya(iyi,50) cokmedi; konsol hata 0; heap artisi 0.3 MB (<20) |
| K13 | Kayıt | **GECTI** | yenileyince jeton/sv ayni=True; gizlenince bekleyen={'j': 336, 'ses': True}, gorunur olunca=None; bekleyen 40 acilista jeton 50 (beklenen 50), tekrar acinca 50; bozuk kayit tasindi=True, varsayilan jeton=0, yeni konsol hata=0. 'Elle bitirilen turda taban/prim yok' ve 'hicbir senaryoda tur iki kez sayilmaz' tam kontrol icin elle de bak |
| K14 | Duraklat | **GECTI** | gizlenince fizik durdu=True (dt=0.000); 3-2-1 sirasinda dokunus dalis yapmadi=True (gosterge 1.00->1.00); duraklat dugmesi dalis yapmadi=True; toplu'da blur duraklatmadi=True |
| K15 | Erişilebilirlik | **GECTI** | yazi x1.0: kucuk dugme [], tasan [], yatay kayma False; yazi x1.2: kucuk dugme [], tasan [], yatay kayma False; yazi x1.4: kucuk dugme [], tasan [], yatay kayma False; hareket azaltma: sarsinti degeri=0 (durum() alani yoksa elle). Flas <=3/s ve parlama alani/suresi icin kontak sayfasina ELLE bak (kontak.py) |
| K16 | Kullanıcı kararı (10 dk) | **ELLE** | telefonda 10 dk, 3 soru + kayit 'tur' farki (kullanici). Uyari metni: 'Bu gri kutu yalniz his testidir...' |
| EK | Ses AudioContext + tam ekran/kilit/titreşim reddi | **GECTI** | AudioContext dokunustan once [] -> sonra ['running']; tam ekran/kilit/titresim reddi: (1, 0, 0) (oyun reddedilmis gibi calismaya devam etti) |

Geçme şartlı KALDI: yok
ATLANDI (kanca eksik): yok

## Konsol hataları

- console.error: Failed to load resource: the server responded with a status of 404 (File not found)
- console.error: Failed to load resource: the server responded with a status of 404 (File not found)

## Elle doldurulacak (usta oyuncu gözlemi)

- K11: S24 Ultra fps ort/min:
- K16: Kalkış heyecanlı mı? Vuruşlar tok mu? Bir tur daha? Tur sayısı:
