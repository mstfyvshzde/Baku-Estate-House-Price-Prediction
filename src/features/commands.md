# Feature Engineering Notları


Bu dosya temizlenmiş datayı model için hazır hale getirir.

Görevi:

- `clean_data.csv` dosyasını okumak
- gerekli kolonlar var mı kontrol etmek
- yeni feature oluşturmak
- sonucu `model_data.csv` olarak kaydetmek
- feature summary raporu oluşturmak

---

## Import bölümü

```python
import json
import pandas as pd

from src.utils.config import get_project_root
```

- `json` → feature summary dosyasını `.json` olarak kaydetmek için
- `pandas` → CSV okuma ve data işlemleri için
- `get_project_root` → proje ana klasör yolunu almak için

---


```python
REQUIRED_COLUMNS = [
    "district",
    "location",
    "rooms",
    "area",
    "floor",
    "total_floors",
    "price",
]
```

Bu liste model datasında olması gereken zorunlu kolonları tutar.

Amaç: Eksik kolon varsa model aşamasına geçmeden hata vermek.

---


```python
def load_clean_data(config: dict) -> pd.DataFrame:
```

Temizlenmiş datayı okuyan fonksiyondur.

---

```python
project_root = get_project_root()
```

Proje ana klasörünü bulur.

---

```python
clean_path = project_root / config["paths"]["clean_data"]
```

`clean_data.csv` dosyasının tam yolunu oluşturur.

---

```python
if not clean_path.exists():
    raise FileNotFoundError(...)
```

Clean data dosyası yoksa hata verir.

Amaç: eksik dosya varsa problemi hemen görmek.

---

```python
data = pd.read_csv(clean_path)
```

Clean data CSV dosyasını pandas DataFrame olarak okur.

---

```python
return data
```

Okunan datayı döndürür.

---


```python
def validate_columns(data: pd.DataFrame) -> None:
```

Gerekli kolonlar datada var mı kontrol eder.

`-> None` demek: bu fonksiyon bir değer döndürmez, sadece kontrol yapar.

---

```python
missing_columns = [col for col in REQUIRED_COLUMNS if col not in data.columns]
```

Eksik kolonları bulur.

Mantık:

- `REQUIRED_COLUMNS` içindeki her kolona bakar
- eğer kolon datada yoksa `missing_columns` listesine ekler

---

```python
if missing_columns:
    raise ValueError(...)
```

Eksik kolon varsa hata verir.

Amaç: yanlış veya eksik data ile model aşamasına geçmemek.

---


```python
def add_area_features(data: pd.DataFrame) -> pd.DataFrame:
```

Alanla ilgili yeni feature oluşturan fonksiyondur.

---

```python
data = data.copy()
```

Orijinal datayı bozmamak için kopya alır.

---

```python
data["area_per_room"] = data["area"] / data["rooms"]
```

Yeni kolon oluşturur.

`area_per_room` şu demektir:

```text
evin sahesi / oda sayısı
```

Örnek:

```text
area = 90
rooms = 3

area_per_room = 30
```

Bu feature modelin evin oda başına düşen alanını anlamasına yardım eder.

---

```python
return data
```

Yeni feature eklenmiş datayı döndürür.

---


```python
def build_features(config: dict):
```

Tüm feature engineering sürecini çalıştıran ana fonksiyondur.

---

```python
data = load_clean_data(config)
```

Clean datayı okur.

---

```python
validate_columns(data)
```

Gerekli kolonlar var mı kontrol eder.

---

```python
original_shape = data.shape
```

Feature eklemeden önceki satır ve kolon sayısını saklar.

---

```python
data = add_area_features(data)
```

`area_per_room` feature’ını ekler.

Dikkat:

```python
data = add_area_features
```

yanlıştır. Çünkü fonksiyon çağrılmaz.

Doğrusu:

```python
data = add_area_features(data)
```

---

```python
data = data.reset_index(drop=True)
```

Indexleri yeniden düzenler.

`drop=True` eski indexi yeni kolon olarak eklemez.

---

```python
summary = {
    "original_rows": int(original_shape[0]),
    "original_columns": int(original_shape[1]),
    "processed_rows": int(data.shape[0]),
    "processed_columns": int(data.shape[1]),
    "added_features": [
        "area_per_room",
    ],
}
```

Feature engineering özetini oluşturur.

İçinde:

- ilk satır sayısı
- ilk kolon sayısı
- işlem sonrası satır sayısı
- işlem sonrası kolon sayısı
- eklenen feature listesi

bulunur.

---

```python
return data, summary
```

Model datasını ve feature özetini döndürür.

---


```python
def save_feature_outputs(
    model_data: pd.DataFrame,
    summary: dict,
    config: dict,
) -> None:
```

Feature engineering sonucunu dosyaya kaydeder.

- `model_data` → model için hazırlanmış data
- `summary` → feature engineering özeti
- `config` → dosya yolları

---

```python
processed_path = project_root / config["paths"]["processed_data"]
summary_path = project_root / config["paths"]["feature_summary"]
```

Kaydedilecek dosyaların tam yollarını oluşturur.

---

```python
processed_path.parent.mkdir(parents=True, exist_ok=True)
summary_path.parent.mkdir(parents=True, exist_ok=True)
```

Gerekli klasörler yoksa oluşturur.

- `parents=True` → üst klasörleri de oluştur
- `exist_ok=True` → klasör varsa hata verme

---

```python
model_data.to_csv(processed_path, index=False)
```

Model datasını CSV olarak kaydeder.

`index=False` gereksiz index kolonunu kaydetmez.

---

```python
json.dump(summary, file, indent=4, ensure_ascii=False)
```

Feature summary bilgisini JSON dosyasına kaydeder.

- `indent=4` → JSON dosyasını okunabilir yapar
- `ensure_ascii=False` → Türkçe/Azerbaycanca karakterleri bozmaz

---

## Genel Akış

```text
clean_data.csv
    ↓
load_clean_data()
    ↓
validate_columns()
    ↓
add_area_features()
    ↓
model_data.csv
feature_summary.json
```