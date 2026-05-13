
## commands.md için Türkçe kısa not

```md
## Feature Preparation Script

Dosya: `scripts/prepare_features.py`

Bu script feature engineering işlemini çalıştırır.

Asıl feature kodları burada değildir:

`src/features/build_features.py`

Bu script sadece süreci başlatır.

---

## Ne yapar?

- `config.yaml` dosyasını okur
- `build_features(config)` fonksiyonunu çalıştırır
- model datasını oluşturur
- sonucu dosyaya kaydeder
- terminalde özet gösterir

---

## Çalıştırma

```bash
python3 scripts/prepare_features.py