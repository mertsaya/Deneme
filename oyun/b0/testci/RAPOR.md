# B0 kabul raporu (otomatik: testci/kabul.py)

Sayfa: `index.html` · Koşu: 2026-10-08 20:47 · Süre: 17 s · Konsol hatası: 2

| K | Ölçüt | Durum | Ayrıntı |
|---|---|---|---|
| K1 | Vay anı <=5 s (>=%90) | **KOŞULMADI** | - |
| K2 | Tur 1 süresi 16-30 s, 65 s'ye çarpma yok | **KOŞULMADI** | - |
| K3 | Beceri farkı (1,30 / 1,60) | **KOŞULMADI** | - |
| K4 | Satın alma ritmi | **KOŞULMADI** | - |
| K5 | Ses duvarı tur | **KOŞULMADI** | - |
| K6 | Kampanya tur süresi | **KOŞULMADI** | - |
| K7 | Yeniden başlatma <=0,5 / <=3 s | **KOŞULMADI** | - |
| K8 | Sim eşliği (>=200 tohum) | **KOŞULMADI** | - |
| K9 | Belirlenimlilik | **KOŞULMADI** | - |
| K10 | Mantık denetimi (debug) | **KOŞULMADI** | - |
| K11 | Kare hızı (telefon) | **KOŞULMADI** | - |
| K12 | Kararlılık, 0 konsol hatası | **KOŞULMADI** | - |
| K13 | Kayıt | **GECTI** | yenileyince jeton/sv ayni=True; gizlenince bekleyen={'j': 336, 'ses': True}, gorunur olunca=None; bekleyen 40 acilista jeton 50 (beklenen 50), tekrar acinca 50; bozuk kayit tasindi=True, varsayilan jeton=0, yeni konsol hata=0. 'Elle bitirilen turda taban/prim yok' ve 'hicbir senaryoda tur iki kez sayilmaz' tam kontrol icin elle de bak |
| K14 | Duraklat | **GECTI** | gizlenince fizik durdu=True (dt=0.000); 3-2-1 sirasinda dokunus dalis yapmadi=True (gosterge 1.00->1.00); duraklat dugmesi dalis yapmadi=True; toplu'da blur duraklatmadi=True |
| K15 | Erişilebilirlik | **GECTI** | yazi x1.0: kucuk dugme [], tasan [], yatay kayma False; yazi x1.2: kucuk dugme [], tasan [], yatay kayma False; yazi x1.4: kucuk dugme [], tasan [], yatay kayma False; hareket azaltma: sarsinti degeri=0 (durum() alani yoksa elle). Flas <=3/s ve parlama alani/suresi icin kontak sayfasina ELLE bak (kontak.py) |
| K16 | Kullanıcı kararı (10 dk) | **KOŞULMADI** | - |
| EK | Ses AudioContext + tam ekran/kilit/titreşim reddi | **KOŞULMADI** | - |

Geçme şartlı KALDI: yok
ATLANDI (kanca eksik): yok

## Konsol hataları

- console.error: Failed to load resource: the server responded with a status of 404 (File not found)
- console.error: Failed to load resource: the server responded with a status of 404 (File not found)

## Elle doldurulacak (usta oyuncu gözlemi)

- K11: S24 Ultra fps ort/min:
- K16: Kalkış heyecanlı mı? Vuruşlar tok mu? Bir tur daha? Tur sayısı:
