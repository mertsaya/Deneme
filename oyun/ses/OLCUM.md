# Ses adayları: ölçüm ve eleme

`python3 oyun/ses/olc.py` üretir (elle düzenleme). Ölçüm, oyunun kullanacağı **mp3 dosyası çözülerek** yapılır.

## Ölçüler

- **LUFS**: ITU-R BS.1770 K-ağırlıklı ses şiddeti. Tek atımlık seslerde en yüksek 100 ms pencere (kısa seslerin algısına daha yakın), döngülerde bütünleşik (kapılı).
- **Hedef**: kategori başına ses şiddeti hedefi (uret.py `KATEGORI`). Adaylar hedefe getirildi; tepe −1,5 dBTP tavanına çarparsa kalan fark **eksik** olarak yazılır.
- **Tel. kaybı**: 500 Hz altını 12 dB/oktav kısan, 10 kHz üstünü kesen kaba telefon hoparlörü benzetiminde ses şiddeti düşüşü. Büyükse ses telefonda "kaybolur".
- **Tepe/RMS**: sivrilik (dB). **Atak**: ilk sesten tepeye ms. **Bantlar**: enerji yüzdesi <150 / 150–600 / 600–3k / 3k–8k / >8k Hz. **Merkez**: spektral ağırlık merkezi.
- **Döngü**: kayıpsız ara dosyada x[n] ile x[n+L] farkı (dB; −100 civarı = tam periyodik). **Dikiş**: mp3 çözülüp döngü gövdesi tarayıcıdaki gibi arka arkaya çalınınca ekteki 5 kHz üstü enerji, gövdenin geri kalanının %99 değerine göre kaç dB fazla (tık varsa büyür).

## Eleme kuralları

1. Kırpılma (|x| ≥ 0,999) olmamalı.
2. Hedef ses şiddetine tavan yüzünden 3 dB'den fazla eksik kalmamalı (çok sivri ses diğerlerinin yanında cılız kalır).
3. Telefon kaybı ≤ 10 dB (oyun telefonda oynanır).
4. Darbe seslerinde atak ≤ 30 ms (vuruş ile görüntü eş zamanlı).
5. Etkin süre kategori aralığında.
6. 6 kHz üstü enerji ≤ %35 (sık çalan seste yorucu olmasın).
7. Döngü periyodiklik hatası ≤ -25 dB ve dikiş ≤ 6 dB. 8. DC kayması yok (|ort.| ≤ 0,01). 9. Son 2 ms, tepeye göre ≤ -40 dB (kesik son tık yapar).

**Puan** (yalnız geçenler arasında sıralama için): 100 − 6·max(0, tel. kaybı − 4) − 10·eksik − 80·max(0, 6k üstü − 0,15) − 2·|LUFS − hedef| − süre sapması. Zevk ölçmez; telefonda net, dengeli ve hedef yükseklikte olanı öne alır. **Son karar kulakla verilir.**

## Motor tutuşma (rampa) (`motor_tutusma`)

Hedef -12 LUFS (100 ms tepe), etkin süre 1.0–3.0 s. Spektrogram: `spektrogram/motor_tutusma.png`

| Aday | Kaynak | LUFS | Tepe dBTP | Tepe/RMS | Eksik | Tel. kaybı | Atak ms | Süre s | Bantlar % | Merkez Hz | Puan | Sonuç |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a. Kükreyen tutuşma | sentez | -12.8 | -3.2 | 9.0 | 0.8 | 5.1 | 0 | 2.89 | 65/22/12/1/0 | 301 | 79 | geçti (4.) |
| b. Fıs... VUUM! | sentez | -12.0 | -4.8 | 9.6 | 0.0 | 5.8 | 127 | 2.73 | 55/28/15/2/0 | 440 | 85 | geçti (3.) |
| c. Turbo şarj + ateşleme | sentez | -12.5 | -4.4 | 14.7 | 0.0 | 4.9 | 991 | 2.78 | 60/17/21/1/2 | 536 | 90 | **ÖNERİ** (1.) |
| d. Kenney itici + tok başlangıç | karma | -16.5 | -3.7 | 20.5 | 4.3 | 11.4 | 1 | 2.19 | 65/31/0/0/4 | 753 | 3 | ELENDİ: çok sivri: hedef yüksekliğe 4.3 dB eksik kalıyor (tepe/RMS 21 dB); telefonda kaybolur: hoparlör benzetiminde 11.4 dB düşüş |
| e. Pıt-pıt-VRUUM | sentez | -12.0 | -4.7 | 7.0 | 0.0 | 5.5 | 1 | 2.49 | 67/22/10/0/0 | 259 | 89 | geçti (2.) |

## Motor uçuş döngüsü (hızla tizleşir) (`motor_ucus`)

Hedef -20 LUFS (bütünleşik). Spektrogram: `spektrogram/motor_ucus.png`

| Aday | Kaynak | LUFS | Tepe dBTP | Tepe/RMS | Eksik | Tel. kaybı | Atak ms | Süre s | Bantlar % | Merkez Hz | Döngü / dikiş dB | Puan | Sonuç |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a. Gürleyen roket | sentez | -20.0 | -4.4 | 13.7 | 0.0 | 5.2 | 8 | 2.00 | 51/33/15/0/0 | 314 | -222 / -2.8 | 93 | geçti (4.) |
| b. Çizgi film jet ıslığı | sentez | -19.9 | -8.3 | 12.8 | 0.0 | 0.3 | 3 | 2.00 | 1/7/74/18/1 | 1912 | -219 / -1.4 | 100 | geçti (2.) |
| c. Derin çatırtılı | sentez | -20.0 | -5.8 | 12.0 | 0.0 | 3.5 | 9 | 2.00 | 53/24/22/1/0 | 381 | -222 / -7.7 | 100 | **ÖNERİ** (1.) |
| d. Kenney uzay motoru | kenney | -20.0 | -5.1 | 7.0 | 0.0 | 5.0 | 11 | 2.00 | 95/1/3/1/0 | 110 | -228 / 0.0 | 94 | geçti (3.) |
| e. Pırpır çizgi film | sentez | -20.0 | -8.6 | 10.2 | 0.0 | 5.9 | 4 | 2.00 | 48/38/13/1/0 | 351 | -221 / -0.6 | 89 | geçti (5.) |

## Sekme: trambolin "boing" (`sekme_trambolin`)

Hedef -13 LUFS (100 ms tepe), etkin süre 0.15–0.8 s. Spektrogram: `spektrogram/sekme_trambolin.png`

| Aday | Kaynak | LUFS | Tepe dBTP | Tepe/RMS | Eksik | Tel. kaybı | Atak ms | Süre s | Bantlar % | Merkez Hz | Puan | Sonuç |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a. Şartname "boing" (sinüs 300→600 Hz, 120 ms) | sentez | -13.0 | -3.4 | 10.5 | 0.0 | 7.6 | 2 | 0.16 | 0/100/0/0/0 | 368 | 74 | geçti (4.) |
| b. Yay boyoing | sentez | -13.0 | -3.2 | 14.3 | 0.0 | 8.0 | 1 | 0.54 | 11/82/7/0/0 | 370 | 75 | geçti (3.) |
| c. Ağız arpı "boyoyoyng" | sentez | -13.6 | -1.5 | 17.1 | 0.6 | 6.4 | 1 | 0.58 | 47/24/29/0/0 | 430 | 76 | geçti (2.) |
| d. Kenney yumuşak + cıvıltı | karma | -13.0 | -2.8 | 12.1 | 0.0 | 13.7 | 1 | 0.49 | 45/55/0/0/0 | 210 | 42 | ELENDİ: telefonda kaybolur: hoparlör benzetiminde 13.7 dB düşüş |
| e. Lastik tok | sentez | -13.0 | -7.3 | 8.6 | 0.0 | 15.3 | 1 | 0.34 | 99/1/0/0/0 | 120 | 30 | ELENDİ: telefonda kaybolur: hoparlör benzetiminde 15.3 dB düşüş |
| f. Telefon dostu tiz boing | sentez | -13.0 | -3.7 | 13.9 | 0.0 | 2.9 | 1 | 0.49 | 2/39/59/0/0 | 656 | 100 | **ÖNERİ** (1.) |

## Çarpma: martı dağılma (`carpma_marti`)

Hedef -14 LUFS (100 ms tepe), etkin süre 0.15–1.0 s. Spektrogram: `spektrogram/carpma_marti.png`

| Aday | Kaynak | LUFS | Tepe dBTP | Tepe/RMS | Eksik | Tel. kaybı | Atak ms | Süre s | Bantlar % | Merkez Hz | Puan | Sonuç |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a. Şartname "pof" (gürültü 60 ms) | sentez | -17.7 | -1.6 | 14.5 | 3.6 | 0.5 | 1 | 0.06 | 3/12/75/10/0 | 1637 | 50 | ELENDİ: çok sivri: hedef yüksekliğe 3.6 dB eksik kalıyor (tepe/RMS 14 dB); süre uygun değil: 0.06 s (beklenen 0.15–1.0 s) |
| b. Pof + tüy + çığlık | sentez | -14.9 | -1.5 | 16.3 | 0.9 | 1.1 | 1 | 0.52 | 17/6/66/11/0 | 1775 | 88 | geçti (2.) |
| c. Kenney yumruk + kumaş kanat | karma | -14.0 | -3.9 | 13.4 | 0.0 | 1.6 | 18 | 0.53 | 32/30/35/3/0 | 920 | 99 | **ÖNERİ** (1.) |
| d. Çift çığlık | sentez | -16.5 | -1.5 | 18.3 | 2.6 | 1.3 | 1 | 0.46 | 13/6/65/15/0 | 1871 | 68 | geçti (4.) |
| e. Yastık + tüy bulutu | sentez | -15.9 | -1.5 | 14.2 | 2.0 | 0.4 | 3 | 0.55 | 58/3/4/32/3 | 2052 | 76 | geçti (3.) |

## Çarpma: balon patlama (`carpma_balon`)

Hedef -13 LUFS (100 ms tepe), etkin süre 0.1–0.8 s. Spektrogram: `spektrogram/carpma_balon.png`

| Aday | Kaynak | LUFS | Tepe dBTP | Tepe/RMS | Eksik | Tel. kaybı | Atak ms | Süre s | Bantlar % | Merkez Hz | Puan | Sonuç |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a. Keskin ince "pat" | sentez | -23.7 | -3.3 | 22.5 | 9.7 | 2.7 | 0 | 0.15 | 0/1/22/36/40 | 7230 | -52 | ELENDİ: çok sivri: hedef yüksekliğe 9.7 dB eksik kalıyor (tepe/RMS 22 dB); sert/tiz: enerjinin %51'i 6 kHz üstünde |
| b. Pat + lastik + konfeti | sentez | -12.9 | -3.9 | 14.4 | 0.0 | 0.2 | 0 | 0.36 | 0/2/42/55/1 | 3377 | 99 | geçti (2.) |
| c. Pat + hava kaçışı | sentez | -13.0 | -3.2 | 15.1 | 0.0 | 0.2 | 0 | 0.36 | 0/14/72/13/0 | 1508 | 99 | **ÖNERİ** (1.) |
| d. Büyük reklam balonu | sentez | -13.0 | -4.7 | 13.5 | 0.0 | 2.9 | 0 | 0.73 | 82/1/8/9/0 | 674 | 96 | geçti (3.) |
| e. Kenney çatırtı tiz | karma | -16.8 | -1.2 | 16.9 | 3.9 | 2.8 | 0 | 0.47 | 58/28/11/3/0 | 436 | 54 | ELENDİ: çok sivri: hedef yüksekliğe 3.9 dB eksik kalıyor (tepe/RMS 17 dB) |

## Kademe ayrılma (`kademe_ayrilma`)

Hedef -12 LUFS (100 ms tepe), etkin süre 0.4–1.6 s. Spektrogram: `spektrogram/kademe_ayrilma.png`

| Aday | Kaynak | LUFS | Tepe dBTP | Tepe/RMS | Eksik | Tel. kaybı | Atak ms | Süre s | Bantlar % | Merkez Hz | Puan | Sonuç |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a. Piro cıvata + metal halka | sentez | -14.4 | -2.1 | 13.6 | 1.9 | 4.5 | 0 | 1.00 | 83/1/16/0/0 | 205 | 74 | geçti (2.) |
| b. Kenney metal + tıslama | karma | -14.3 | -1.4 | 18.4 | 2.0 | 7.1 | 1 | 0.83 | 66/0/2/11/21 | 3326 | 46 | geçti (4.) |
| c. Ka-çank + pışşş | sentez | -13.4 | -1.5 | 18.9 | 1.5 | 3.5 | 121 | 1.02 | 35/35/23/6/1 | 895 | 82 | ELENDİ: geç vuruş: tepeye 121 ms |
| d. Patlamalı ayrılma | karma | -13.7 | -1.7 | 14.7 | 1.7 | 5.8 | 0 | 1.40 | 74/16/9/1/0 | 250 | 66 | geçti (3.) |
| e. Yay fırlatma | sentez | -13.5 | -1.5 | 16.6 | 1.6 | 3.7 | 1 | 0.55 | 16/47/31/5/1 | 983 | 77 | **ÖNERİ** (1.) |

## Dalış (vuuş + vuruş) (`dalis`)

Hedef -12 LUFS (100 ms tepe), etkin süre 0.2–1.0 s. Spektrogram: `spektrogram/dalis.png`

| Aday | Kaynak | LUFS | Tepe dBTP | Tepe/RMS | Eksik | Tel. kaybı | Atak ms | Süre s | Bantlar % | Merkez Hz | Puan | Sonuç |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a. Şartname "vuuş" (bant süpürme 250 ms) | sentez | -12.6 | -1.2 | 14.8 | 0.6 | 0.3 | 78 | 0.25 | 0/4/81/12/3 | 2041 | 88 | geçti (5.) |
| b. Vuuş + tok vuruş | sentez | -11.9 | -4.3 | 12.4 | 0.0 | 3.0 | 199 | 0.66 | 80/1/11/7/1 | 699 | 99 | **ÖNERİ** (1.) |
| c. Bomba ıslığı + güm | sentez | -12.0 | -1.7 | 14.5 | 0.0 | 4.1 | 351 | 0.81 | 68/1/31/0/0 | 415 | 97 | geçti (2.) |
| d. Vuuş + Kenney yumruk | karma | -12.2 | -1.5 | 14.9 | 0.3 | 2.8 | 180 | 0.67 | 61/23/9/7/1 | 686 | 96 | geçti (3.) |
| e. Hava yırtılması + klank | sentez | -12.0 | -3.7 | 12.9 | 0.0 | 4.7 | 96 | 0.61 | 54/2/38/5/1 | 879 | 95 | geçti (4.) |

## Mükemmel sekme (`mukemmel`)

Hedef -12 LUFS (100 ms tepe), etkin süre 0.3–1.3 s. Spektrogram: `spektrogram/mukemmel.png`

| Aday | Kaynak | LUFS | Tepe dBTP | Tepe/RMS | Eksik | Tel. kaybı | Atak ms | Süre s | Bantlar % | Merkez Hz | Puan | Sonuç |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a. Şartname "ding" (880 + 1320 Hz, 200 ms) | sentez | -12.0 | -1.7 | 13.0 | 0.0 | 0.3 | 2 | 0.22 | 0/0/100/0/0 | 1026 | 94 | ELENDİ: süre uygun değil: 0.22 s (beklenen 0.3–1.3 s) |
| b. Arpej + parıltı + boing | sentez | -12.0 | -2.5 | 14.3 | 0.0 | 0.3 | 1 | 0.70 | 2/11/84/4/0 | 1479 | 99 | **ÖNERİ** (1.) |
| c. FM çan + şok dalgası | sentez | -12.1 | -2.6 | 18.1 | 0.0 | 2.3 | 1 | 0.92 | 23/0/37/34/6 | 2920 | 99 | geçti (2.) |
| d. Kenney güç + boing | karma | -13.9 | -1.5 | 16.5 | 1.9 | 3.3 | 1 | 0.40 | 9/55/25/11/0 | 1060 | 74 | geçti (4.) |
| e. Zil + boing | karma | -12.0 | -1.6 | 15.8 | 0.0 | 5.9 | 0 | 0.75 | 0/89/11/0/0 | 444 | 88 | geçti (3.) |

## Ses duvarı kırılışı (sinematik) (`ses_duvari`)

Hedef -10 LUFS (100 ms tepe), etkin süre 1.2–4.0 s. Spektrogram: `spektrogram/ses_duvari.png`

| Aday | Kaynak | LUFS | Tepe dBTP | Tepe/RMS | Eksik | Tel. kaybı | Atak ms | Süre s | Bantlar % | Merkez Hz | Puan | Sonuç |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a. Şartname "BUM" (60 Hz sinüs + gürültü, 400 ms) | sentez | -12.4 | -1.5 | 11.7 | 2.4 | 15.3 | 2 | 0.40 | 99/0/1/0/0 | 69 | -5 | ELENDİ: telefonda kaybolur: hoparlör benzetiminde 15.3 dB düşüş; süre uygun değil: 0.40 s (beklenen 1.2–4.0 s) |
| b. N-dalga çift çatlak + parıltı | sentez | -10.7 | -2.3 | 11.2 | 0.4 | 1.8 | 0 | 3.68 | 57/7/27/9/0 | 889 | 91 | **ÖNERİ** (1.) |
| c. Emme + BUM + çınlama | sentez | -12.7 | -1.3 | 13.3 | 2.4 | 0.8 | 396 | 3.73 | 65/12/17/4/1 | 682 | 66 | geçti (2.) |
| d. Kenney alçak patlama + çatlak | karma | -12.8 | -2.0 | 13.3 | 2.8 | 3.4 | 0 | 1.67 | 93/3/4/1/0 | 165 | 63 | geçti (3.) |
| e. BUM + fanfar | sentez | -12.8 | -1.8 | 12.3 | 2.6 | 5.4 | 0 | 2.70 | 51/25/22/1/0 | 397 | 60 | geçti (4.) |

## Jeton / kazanç (`jeton`)

Hedef -15 LUFS (100 ms tepe), etkin süre 0.1–0.7 s. Spektrogram: `spektrogram/jeton.png`

| Aday | Kaynak | LUFS | Tepe dBTP | Tepe/RMS | Eksik | Tel. kaybı | Atak ms | Süre s | Bantlar % | Merkez Hz | Puan | Sonuç |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a. İki nota (Re-La) | sentez | -15.0 | -12.8 | 6.7 | 0.0 | 0.1 | 1 | 0.32 | 0/0/91/8/0 | 1810 | 99 | geçti (2.) |
| b. Metal çın | sentez | -15.0 | -8.4 | 13.9 | 0.0 | 0.2 | 0 | 0.49 | 0/0/85/14/2 | 2884 | 98 | geçti (3.) |
| c. Kenney para şıngırtısı | kenney | -17.4 | -1.4 | 21.3 | 2.3 | 0.4 | 58 | 0.31 | 0/0/17/75/8 | 4915 | 68 | ELENDİ: geç vuruş: tepeye 58 ms |
| d. Parıltılı iki çan | sentez | -15.0 | -7.0 | 14.0 | 0.0 | 0.1 | 1 | 0.48 | 0/0/95/4/1 | 1915 | 99 | **ÖNERİ** (1.) |
| e. Kenney fiş + ding | karma | -15.6 | -1.6 | 20.6 | 0.6 | 0.1 | 4 | 0.30 | 0/0/95/4/0 | 2771 | 91 | geçti (4.) |

## Arayüz tıklama (`ui_tik`)

Hedef -20 LUFS (100 ms tepe), etkin süre 0.01–0.2 s. Spektrogram: `spektrogram/ui_tik.png`

| Aday | Kaynak | LUFS | Tepe dBTP | Tepe/RMS | Eksik | Tel. kaybı | Atak ms | Süre s | Bantlar % | Merkez Hz | Puan | Sonuç |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a. Yumuşak pop | sentez | -20.0 | -4.9 | 11.0 | 0.0 | 0.2 | 0 | 0.05 | 0/0/100/0/0 | 894 | 97 | geçti (2.) |
| b. Tahta tık | sentez | -19.9 | -2.9 | 13.1 | 0.0 | 4.0 | 0 | 0.05 | 0/99/0/0/0 | 389 | 97 | geçti (3.) |
| c. Kenney click_001 | kenney | -26.0 | -1.5 | 17.4 | 6.3 | 1.5 | 1 | 0.09 | 81/8/7/3/0 | 347 | 24 | ELENDİ: çok sivri: hedef yüksekliğe 6.3 dB eksik kalıyor (tepe/RMS 17 dB) |
| d. Kenney select_001 | kenney | -20.0 | -2.2 | 14.5 | 0.0 | 0.1 | 0 | 0.04 | 0/17/53/30/0 | 2339 | 96 | geçti (4.) |
| e. Baloncuk "blup" | sentez | -20.0 | -9.7 | 7.3 | 0.0 | 3.1 | 2 | 0.06 | 0/60/40/0/0 | 572 | 98 | **ÖNERİ** (1.) |

## Kart satın alma (`kart_satin`)

Hedef -15 LUFS (100 ms tepe), etkin süre 0.3–1.2 s. Spektrogram: `spektrogram/kart_satin.png`

| Aday | Kaynak | LUFS | Tepe dBTP | Tepe/RMS | Eksik | Tel. kaybı | Atak ms | Süre s | Bantlar % | Merkez Hz | Puan | Sonuç |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a. Ka-çing! | sentez | -15.6 | -2.7 | 18.9 | 0.6 | 0.3 | 0 | 0.94 | 0/0/73/23/4 | 3201 | 91 | geçti (3.) |
| b. Arpej + jeton yağmuru | sentez | -15.0 | -3.7 | 16.3 | 0.0 | 0.1 | 3 | 0.78 | 0/0/88/11/1 | 2518 | 100 | **ÖNERİ** (1.) |
| c. Kenney onay | kenney | -15.0 | -7.4 | 10.1 | 0.0 | 4.6 | 0 | 0.28 | 0/75/25/0/0 | 560 | 91 | ELENDİ: süre uygun değil: 0.28 s (beklenen 0.3–1.2 s) |
| d. Kenney fiş yığını + çan | karma | -15.0 | -5.9 | 14.5 | 0.0 | 0.0 | 4 | 0.66 | 0/0/95/5/0 | 1937 | 99 | geçti (2.) |
| e. Kart savur + damga | sentez | -15.1 | -2.7 | 16.4 | 0.0 | 3.0 | 119 | 0.54 | 29/33/33/5/1 | 979 | 98 | ELENDİ: geç vuruş: tepeye 119 ms |

## Son şans uyarısı (`son_sans`)

Hedef -13 LUFS (100 ms tepe), etkin süre 0.9–2.0 s. Spektrogram: `spektrogram/son_sans.png`

| Aday | Kaynak | LUFS | Tepe dBTP | Tepe/RMS | Eksik | Tel. kaybı | Atak ms | Süre s | Bantlar % | Merkez Hz | Puan | Sonuç |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a. İki ton alarm | sentez | -13.0 | -9.8 | 4.1 | 0.0 | 0.4 | 3 | 1.18 | 0/0/99/1/0 | 927 | 98 | **ÖNERİ** (1.) |
| b. Çizgi film korna "avuga" | sentez | -13.0 | -1.5 | 12.7 | 0.0 | 0.3 | 9 | 1.09 | 0/2/97/1/0 | 1188 | 97 | geçti (2.) |
| c. Siren + kalp atışı | sentez | -13.7 | -1.5 | 14.2 | 0.7 | 3.0 | 50 | 1.24 | 38/8/54/0/0 | 705 | 90 | geçti (3.) |
| d. Kenney üç ton | kenney | -13.0 | -4.2 | 9.4 | 0.0 | 18.7 | 22 | 0.85 | 90/10/0/0/0 | 89 | 6 | ELENDİ: telefonda kaybolur: hoparlör benzetiminde 18.7 dB düşüş; süre uygun değil: 0.85 s (beklenen 0.9–2.0 s) |
| e. Şartname "pat" + alçak gümbürtü | sentez | -17.0 | -1.3 | 9.1 | 4.0 | 0.3 | 0 | 1.07 | 93/1/3/4/0 | 249 | 48 | ELENDİ: çok sivri: hedef yüksekliğe 4.0 dB eksik kalıyor (tepe/RMS 9 dB) |

## Müzik döngüsü (hızla katman kazanır) (`muzik`)

Hedef -18 LUFS (bütünleşik). Spektrogram: `spektrogram/muzik.png`

| Aday | Kaynak | LUFS | Tepe dBTP | Tepe/RMS | Eksik | Tel. kaybı | Atak ms | Süre s | Bantlar % | Merkez Hz | Döngü / dikiş dB | Puan | Sonuç |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a. Roket sörfü (160 BPM, Mi minör) | sentez | -18.0 | -4.4 | 15.6 | 0.0 | 2.7 | 2 | 24.00 | 36/23/37/3/1 | 671 | -206 / 0.7 | 100 | **ÖNERİ** (1.) |
| b. Çiptün hız (150 BPM, Do majör) | sentez | -18.0 | -5.1 | 14.8 | 0.0 | 5.8 | 5 | 25.60 | 41/49/8/2/0 | 420 | -205 / -1.8 | 89 | geçti (4.) |
| c. Çizgi film galopu (168 BPM, Fa majör) | sentez | -18.0 | -4.8 | 15.7 | 0.0 | 2.5 | 2 | 22.86 | 18/35/45/2/0 | 673 | -209 / -0.1 | 100 | geçti (2.) |
| d. Uzay ska (136 BPM, Si♭ majör) | sentez | -18.0 | -4.1 | 15.8 | 0.0 | 5.3 | 8 | 28.24 | 38/49/11/2/1 | 483 | -204 / -13.5 | 92 | geçti (3.) |

Katman ses şiddetleri (k1 temel / k2 orta / k3 ezgi, bütünleşik LUFS):

- a. Roket sörfü (160 BPM, Mi minör): -21.9 / -30.8 / -20.8 · 160 BPM · döngü 24.0 s
- b. Çiptün hız (150 BPM, Do majör): -19.8 / -31.3 / -23.4 · 150 BPM · döngü 25.6 s
- c. Çizgi film galopu (168 BPM, Fa majör): -21.9 / -28.1 / -21.3 · 168 BPM · döngü 22.9 s
- d. Uzay ska (136 BPM, Si♭ majör): -20.0 / -33.1 / -22.7 · 136 BPM · döngü 28.2 s
