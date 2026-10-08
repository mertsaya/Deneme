# Proje kuralları: Son Durak: Plüton

## Model yönlendirme (tasarruf)

Ana oturum **Sonnet** ile çalışır ve yönetici gibi davranır: işi böler, uygun ajana uygun modelle verir.
Ana oturum kendi modelini değiştiremez; zor iş Opus'lu bir alt ajana devredilir.

| Model | Ne zaman | Varsayılan ajanlar |
|---|---|---|
| **Opus** | Oyun mantığı/tasarım kararları, fizik ve denge, mimari, inatçı hatalar, shader yazımı, denetim | `oyun-tasarimci`, `denetci` |
| **Sonnet** | Normal kod yazma, Blender betikleri, ses, test senaryosu yazma, rapor okuma | `uygulayici`, `gorsel-sanatci`, `ses-tasarimci`, `oyun-testcisi` |
| **Haiku** | Mekanik işler: dosya arama/özetleme, aynı testi tekrar koşup sayı toplama, metin taşıma, biçim düzeltme | `Explore` ve tek seferlik küçük görevler |

Kurallar:
- Ajanın varsayılanı yetmiyorsa Agent çağrısında `model` ile değiştir. Örnek: `uygulayici` fizik çekirdeğini veya shader'ı sıfırdan yazacaksa `opus`; `oyun-testcisi` yalnızca hazır betiği tekrar koşacaksa `haiku`.
- Aynı iş Sonnet'te iki kez başarısız olursa bir kez Opus'la dene.
- Büyük, kullanım yiyen işlerden önce kullanıcıya hangi modelle ve yaklaşık ne kadar süreceğini tek satırla söyle.
- Kullanıcı ana oturumu yanlışlıkla Opus'ta açtıysa bir kez hatırlat: "Model menüsünden Sonnet'i seçersen daha tasarruflu olur."
