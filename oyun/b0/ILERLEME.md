# B0 ilerleme (gece çalışması)

Plan: `oyun/PLAN_B.md`. Kullanıcı uyurken zamanlanmış görev bu listeden sıradaki işi yapar, işaretler, not düşer.
Kullanıcı onayı bekleyen yaratıcı kararlar için plandaki önerilen varsayılanlar kullanılıyor (aşağıda "Sabah sorulacaklar").

## Adımlar
- [ ] 1. Denetçi incelemesi: PLAN_B.md (denetci rolü). Bulgular buraya; gerekiyorsa planı düzelt.
- [ ] 2. Tasarımcı: `oyun/b0/TASARIM.md` — B0 şartnamesi (yalnız B0 kapsamı: rampa göstergesi, uçuş fiziği g_etkin/sürükleme/sekme, dalış, 5 nesne: martı, balon, şamandıra, ağ, yakıt dronu; ses duvarı; kara kutu; 6 geliştirmelik hangar; kayıt) + JS yapılandırma nesnesi.
- [ ] 3. Tasarımcı: `oyun/ekonomi_b.py` — bot oyuncu simülasyonu; B0 ekonomisi kabul ölçütlerini sağlıyor mu.
- [ ] 4. Uygulayıcı: `oyun/b0/index.html` — gri kutu prototip (basit renkli şekiller, yandan 2.5B, dikey ekran), test kancaları `?t= ?seed= ?bot=`.
- [ ] 5. Testçi: bot turları (iyi / kötü / hiç dokunmayan), ölçümler, ekran görüntüsü kontak sayfası `oyun/b0/test/`.
- [ ] 6. Uygulayıcı: testçinin ilk 3 sorununu düzelt; 5'e dön (en fazla 2 döngü).
- [ ] 7. Denetçi: B0 teslimat incelemesi (mantık kuralları §3, kabul ölçütleri §12).
- [ ] 8. Yayın: artifact https://claude.ai/artifact/GXoa5nw3mw4jwrYmxYSbB4 (önce `read`, sonra aynı url'ye index.html + gerekli dosyalar). Sabah raporu: `oyun/b0/SABAH_RAPORU.md`.

## Sabah sorulacaklar (varsayılanla ilerlendi)
- Para teması: "İzlenme → sponsor parası" (varsayılan) mı, düz "kredi" mi?
- Rakip ajans zeplini (Burrito Bison'daki ringdeki rakip) olsun mu? (varsayılan: evet, B1'de)
- Kalkış Akdeniz kıyısından, deniz üstünde su sekmesi (varsayılan: evet)
- İlk sürüm kapsamı: önce yalnız Dünya bölümü cilalı (varsayılan: evet)

## Notlar
(her çalışma buraya tarih-saat ve kısa not ekler)
