# Data Cleaning Notları

## Dosya

`src/data/cleaning.py`

## Ne işe yarar?

Bu dosya raw datayı temizlemek için kullanılır.

Görevi:

- raw CSV dosyasını okumak
- kolon adlarını config dosyasından almak
- text kolonlarını temizlemek
- numeric kolonları sayıya çevirmek
- hatalı satırları bulmak
- temiz data ile silinen satırları ayırmak
- sonuçları dosyaya kaydetmek

---

## Import bölümü

```python
import json
import unicodedata

import pandas as pd

from src.utils.config import get_project_root
```

Ne işe yarar?
json → cleaning summary dosyasını .json formatında kaydetmek için kullanılır.

unicodedata → text içindeki unicode karakterleri normalize etmek için kullanılır.

pandas → CSV okuma, dataframe temizleme ve veri işleme için kullanılır.

get_project_root → proje ana klasör yolunu almak için kullanılır.


## Sabit kolon listeleri
```python
TEXT_COLUMNS = ["district", "location"]
NUMERIC_COLUMNS = ["rooms", "area", "floor", "total_floors", "price"]
```

Ne işe yarar?
Bu listeler hangi kolonlara hangi temizlik işleminin uygulanacağını gösterir.

TEXT_COLUMNS → yazı/text kolonları
NUMERIC_COLUMNS → sayısal kolonlar

Örnek:
district ve location text olduğu için küçük harfe çevrilir, boşlukları temizlenir.
rooms, area, floor, price gibi kolonlar sayıya çevrilir.

```python
def normalize_text(value):
    if pd.isna(value):
        return pd.NA

    text = str(value).strip().casefold()
    text = unicodedata.normalize("NFKC", text)
    text = " ".join(text.split())

    if text == "":
        return pd.NA

    return text
```

```python
def normalize_text(value):
```

Tek bir text değerini temizleyen fonksiyon.


```python
if pd.isna(value):
    return pd.NA
```

Değer boşsa `pd.NA` döndürür.

- `pd.isna()` → boş/NaN kontrolü
- `pd.NA` → standart eksik değer

---

```python
text = str(value).strip().casefold()
```

Text’i standart hale getirir.

- `str(value)` → değeri yazıya çevirir
- `.strip()` → baş/son boşlukları siler
- `.casefold()` → küçük harfe çevirir

Örnek:

```text
"  Yasamal  " → "yasamal"
```

---

```python
text = unicodedata.normalize("NFKC", text)
```

Unicode karakterleri standartlaştırır.

Amaç: yazıdaki gizli/farklı karakter problemlerini azaltmak.

---

```python
text = " ".join(text.split())
```

Fazla boşlukları tek boşluğa indirir.

Örnek:

```text
"yeni   günəşli" → "yeni günəşli"
```

---

```python
if text == "":
    return pd.NA
```

Temizlemeden sonra text boş kaldıysa eksik değer sayar.

---

```python
return text
```

Temizlenmiş text’i döndürür.


```python
def load_raw_data(config: dict) -> pd.DataFrame:
```

Raw CSV dosyasını okuyan fonksiyon.

- `config: dict` → config ayarlarını alır
- `-> pd.DataFrame` → pandas DataFrame döndürür

---

```python
project_root = get_project_root()
```

Proje ana klasör yolunu alır.

---

```python
raw_path = project_root / config["paths"]["raw_data"]
```

Raw data dosyasının tam yolunu oluşturur.

Örnek:

```text
data/raw/raw_data.csv
```

---

```python
columns = config["schema"]["columns"]
```

Kolon adlarını config dosyasından alır.

---

```python
if not raw_path.exists():
    raise FileNotFoundError(...)
```

Raw data dosyası yoksa hata verir.

Amaç: dosya eksikse problemi hemen görmek.

---

```python
data = pd.read_csv(
    raw_path,
    header=None,
    names=columns,
    sep=None,
    engine="python",
    encoding="utf-8-sig",
    on_bad_lines="skip",
)
```

CSV dosyasını okur.

- `header=None` → CSV içinde başlık yok
- `names=columns` → kolon adlarını biz veriyoruz
- `sep=None` → ayırıcıyı otomatik algılar
- `engine="python"` → esnek CSV okuma
- `encoding="utf-8-sig"` → karakter problemi azaltır
- `on_bad_lines="skip"` → bozuk satırları atlar

---

```python
return data
```

Okunan raw datayı döndürür.

---


```python
def clean_text_columns(data: pd.DataFrame) -> pd.DataFrame:
```

Text kolonlarını temizleyen fonksiyon.

---

```python
data = data.copy()
```

Orijinal datayı bozmamak için kopya alır.

---

```python
for col in TEXT_COLUMNS:
```

Text kolonları üzerinde döner.

Örnek:

```text
district
location
```

---

```python
data[col] = data[col].apply(normalize_text)
```

Her text değere `normalize_text()` fonksiyonunu uygular.

Amaç:

```text
"  Yasamal  " → "yasamal"
```

---

```python
return data
```

Text kolonları temizlenmiş datayı döndürür.

---


```python
def clean_numeric_columns(data: pd.DataFrame) -> pd.DataFrame:
```

Sayısal kolonları numeric tipe çeviren fonksiyon.

---

```python
data = data.copy()
```

Orijinal datayı bozmamak için kopya alır.

---

```python
for col in NUMERIC_COLUMNS:
```

Sayısal kolonlar üzerinde döner.

Örnek:

```text
rooms
area
floor
total_floors
price
```

---

```python
data[col] = pd.to_numeric(data[col], errors="coerce")
```

Kolonu sayıya çevirir.

- `"120"` → `120`
- `"abc"` → `NaN`

`errors="coerce"` hatalı değerleri `NaN` yapar.

---

```python
return data
```

Sayısal kolonları düzeltilmiş datayı döndürür.

---


```python
def build_removal_reasons(data: pd.DataFrame, config: dict) -> pd.Series:
```

Her satırın neden silineceğini bulan fonksiyon.

- `data` → temizlenecek dataset
- `config` → validation kuralları
- `pd.Series` → her satır için hata sebebi döndürür

---

```python
validation = config["validation"]
```

Config içindeki temizlik kurallarını alır.

Örnek:

```text
rooms min/max
area min/max
price min/max
```

---

```python
reasons = pd.Series("", index=data.index, dtype="object")
```

Her satır için boş sebep listesi oluşturur.

Başta her satır temiz kabul edilir.

---

```python
def add_reason(mask, reason):
    reasons.loc[mask] = reasons.loc[mask] + reason + "; "
```

Hatalı satırlara sebep ekleyen yardımcı fonksiyon.

- `mask` → hangi satırlar hatalı?
- `reason` → hata sebebi ne?

add_reason(data["price"] < 10000, "invalid_price_range")
Fiyatı 10000’den küçük olan satırlara "invalid_price_range" yazar.
---

```python
add_reason(data["district"].isna(), "missing_district")
add_reason(data["location"].isna(), "missing_location")
```

District veya location boşsa sebep ekler.

---

```python
for col in NUMERIC_COLUMNS:
    add_reason(data[col].isna(), f"missing_or_invalid_{col}")
```

Sayısal kolonlarda boş veya hatalı değer varsa sebep ekler.

Örnek:

```text
missing_or_invalid_price
```

---

```python
add_reason(
    (data["rooms"] < validation["rooms"]["min"])
    | (data["rooms"] > validation["rooms"]["max"]),
    "invalid_rooms_range",
)
```

Oda sayısı min/max aralığı dışındaysa hata sebebi ekler.

---

```python
add_reason(
    (data["area"] < validation["area"]["min"])
    | (data["area"] > validation["area"]["max"]),
    "invalid_area_range",
)
```

Ev sahesi belirlenen aralıkta değilse hata sebebi ekler.

---

```python
add_reason(
    data["floor"] < validation["floor"]["min"],
    "invalid_floor_range",
)
```

Kat değeri minimum değerden küçükse hata sebebi ekler.

---

```python
add_reason(
    (data["total_floors"] < validation["total_floors"]["min"])
    | (data["total_floors"] > validation["total_floors"]["max"]),
    "invalid_total_floors_range",
)
```

Toplam kat sayısı belirlenen aralıkta değilse hata sebebi ekler.

---

```python
add_reason(
    data["floor"] > data["total_floors"],
    "floor_greater_than_total_floors",
)
```

Evin bulunduğu kat, toplam kattan büyükse hata sebebi ekler.

Örnek:

```text
floor = 15
total_floors = 9
```

Bu hatalıdır.

---

```python
add_reason(
    (data["price"] < validation["price"]["min"])
    | (data["price"] > validation["price"]["max"]),
    "invalid_price_range",
)
```

Fiyat belirlenen aralıkta değilse hata sebebi ekler.

Örnek:

```text
260 → hatalı
260000 → mantıklı
```

---

```python
duplicate_mask = data.duplicated(keep="first")
add_reason(duplicate_mask, "duplicate_row")
```

Tekrarlanan satırları bulur.

- ilk satır kalır
- tekrar edenler hatalı sayılır

---

```python
reasons = reasons.str.strip("; ")
```

Sebep yazılarının sonundaki fazla `;` işaretini temizler.

---

```python
return reasons
```

Her satır için hata sebebini döndürür.

---


```python
def clean_dataset(config: dict):
```

Tüm data cleaning sürecini çalıştıran ana fonksiyon.

---

```python
data = load_raw_data(config)
```

Raw datayı okur.

---

```python
original_shape = data.shape
```

Temizlemeden önceki satır/sütun sayısını saklar.

Örnek:

```text
(500, 7)
```

---

```python
data = clean_text_columns(data)
data = clean_numeric_columns(data)
```

Önce text kolonlarını temizler, sonra numeric kolonları sayıya çevirir.

---

```python
removal_reasons = build_removal_reasons(data, config)
```

Her satırı kontrol eder ve hatalıysa neden hatalı olduğunu yazar.
Örnek:
price = 260 → invalid_price_range
floor = 15, total_floors = 9 → floor_greater_than_total_floors

---

```python
valid_mask = removal_reasons == ""
```

Hatasız satırları seçmek için maske oluşturur.

- boş sebep → temiz satır
- sebep varsa → hatalı satır

---

```python
clean_data = data.loc[valid_mask].copy()
removed_rows = data.loc[~valid_mask].copy()
```

Datayı ikiye ayırır.

- `clean_data` → kullanılacak temiz data
- `removed_rows` → silinen/hatalı satırlar

~valid_mask ne demek?
valid_mask’in tersidir.
Yani:
valid_mask True ise → temiz
~valid_mask True ise → hatalı

---

```python
removed_rows["removal_reason"] = removal_reasons.loc[~valid_mask]
```

Silinen satırlara neden silindiğini ekler.

---

```python
clean_data = clean_data.reset_index(drop=True)
removed_rows = removed_rows.reset_index(drop=True)
```

Indexleri sıfırdan düzenler.

---

```python
summary = {
    "original_rows": int(original_shape[0]),
    "original_columns": int(original_shape[1]),
    "clean_rows": int(clean_data.shape[0]),
    "removed_rows": int(removed_rows.shape[0]),
    "clean_columns": int(clean_data.shape[1]),
}
```

Temizleme özetini oluşturur.

İçinde:

- başlangıç satır sayısı
- başlangıç kolon sayısı
- temiz satır sayısı
- silinen satır sayısı
- temiz kolon sayısı

vardır.

---

```python
return clean_data, removed_rows, summary
```

Temiz datayı, silinen satırları ve özeti döndürür.

---

## `save_cleaning_outputs()`

```python
def save_cleaning_outputs(
    clean_data: pd.DataFrame,
    removed_rows: pd.DataFrame,
    summary: dict,
    config: dict,
) -> None:
```

Temizleme sonuçlarını dosyaya kaydeden fonksiyon.

- `clean_data` → temiz dataset
- `removed_rows` → silinen satırlar
- `summary` → cleaning özeti
- `config` → dosya yolları

`-> None` demek: bu fonksiyon değer döndürmez, sadece dosya kaydeder.

---

```python
project_root = get_project_root()
```

Proje ana klasör yolunu alır.

---

```python
clean_path = project_root / config["paths"]["clean_data"]
removed_path = project_root / config["paths"]["removed_rows"]
summary_path = project_root / config["paths"]["cleaning_summary"]
```

Kaydedilecek dosyaların tam yollarını oluşturur.

---

```python
clean_path.parent.mkdir(parents=True, exist_ok=True)
removed_path.parent.mkdir(parents=True, exist_ok=True)
summary_path.parent.mkdir(parents=True, exist_ok=True)
```

Gerekli klasörler yoksa oluşturur.

- `parents=True` → üst klasörleri de oluşturur
- `exist_ok=True` → klasör varsa hata vermez

---

```python
clean_data.to_csv(clean_path, index=False)
removed_rows.to_csv(removed_path, index=False)
```

Temiz data ve silinen satırları CSV olarak kaydeder.

`index=False` gereksiz index kolonunu kaydetmez.

---

```python
with open(summary_path, "w", encoding="utf-8") as file:
    json.dump(summary, file, indent=4, ensure_ascii=False)
```

Cleaning özetini JSON olarak kaydeder.

- `"w"` → yazma modu
- `indent=4` → okunabilir JSON
- `ensure_ascii=False` → Türkçe/Azerbaycanca karakterleri bozmaz

---

## Genel Akış

```text
raw_data.csv
    ↓
load_raw_data()
    ↓
clean_text_columns()
    ↓
clean_numeric_columns()
    ↓
build_removal_reasons()
    ↓
clean_dataset()
    ↓
save_cleaning_outputs()
    ↓
clean_data.csv
removed_rows.csv
cleaning_summary.json
```