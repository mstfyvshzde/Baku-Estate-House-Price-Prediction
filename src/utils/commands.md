# Config Okuma Dosyası Notları

## Dosya

`src/utils/config.py`

## Ne işe yarar?

Bu dosya `config/config.yaml` dosyasını okumak için kullanılır.

Amaç:

- proje ana klasörünü bulmak
- config dosyasını okumak
- config içindeki ayarları Python sözlüğü olarak döndürmek

---

## Kod parçaları

```python
from pathlib import Path
import yaml
```

Path → dosya ve klasör yollarını yönetmek için kullanılır.
yaml → .yaml dosyasını okumak için kullanılır.


```python
PROJECT_ROOT = Path(__file__).resolve().parents[2]
```
Bu satırın amacı:
Projenin ana klasör yolunu otomatik bulmak.
Yani Python’a şunu dedirtiyoruz:
Ben şu an hangi dosyanın içindeyim?
Bu dosyanın tam yolunu bul.
Sonra klasörlerde yukarı çık.
Proje ana klasörüne ulaş.
Parça parça analiz

1. __file__
```python
__file__
```
Bu, şu an çalışan Python dosyasının yolunu verir.
Mesela dosyamız burada:
baku-house-price-api/src/utils/config.py

O zaman __file__ yaklaşık bunu temsil eder:
src/utils/config.py

Yani Python der ki:
Ben şu an config.py dosyasındayım.


2. Path(__file__)

```python
Path(__file__)
```
Bu yol bilgisini daha rahat yönetmek için Path objesine çevirir.
Normal string gibi değil, dosya yolu gibi davranır.

Mesela:
Path(__file__)
şuna benzer:
src/utils/config.py

Ama artık bununla / kullanarak yollar oluşturabiliriz:
PROJECT_ROOT / "data" / "raw" / "raw_data.csv"

3. .resolve()
```python
Path(__file__).resolve()
```
Bu dosyanın tam ve gerçek yolunu verir.

Mesela:
/Users/s/Desktop/baku-house-price-api/src/utils/config.py
Yani artık göreceli yol değil, tam yol var.
Bu önemli çünkü terminali nereden çalıştırırsan çalıştır, proje yolu daha güvenli bulunur.

4. .parents
```python
Path(__file__).resolve().parents
```
Bu, bulunduğun dosyadan yukarı doğru klasörleri gösterir.
Dosyanın tam yolu şöyle olsun:
/Users/s/Desktop/baku-house-price-api/src/utils/config.py

O zaman parents şöyle çalışır:
parents[0] → /Users/s/Desktop/baku-house-price-api/src/utils
parents[1] → /Users/s/Desktop/baku-house-price-api/src
parents[2] → /Users/s/Desktop/baku-house-price-api

Bizim istediğimiz proje ana klasörü:
/Users/s/Desktop/baku-house-price-api

Bu yüzden:
parents[2] kullanıyoruz.


```python
def get_project_root() -> Path:
    return PROJECT_ROOT
```

Kısaca: proje ana klasör yolunu döndüren yardımcı fonksiyondur.

Parça parça
```python
def get_project_root()
```

Yeni bir fonksiyon tanımlar.
Fonksiyonun adı:
get_project_root
Anlamı:
proje ana klasörünü getir

```python
-> Path
```
Bu, fonksiyonun Path türünde değer döndüreceğini gösterir.
Yani dönüş değeri normal yazı değil, dosya yolu objesidir.

```python
return PROJECT_ROOT
```
Daha önce hesaplanan proje ana klasör yolunu geri döndürür.

Mesela:
/Users/s/Desktop/baku-house-price-api

Neden fonksiyon yazdık?
Başka dosyalarda direkt PROJECT_ROOT kullanmak yerine bunu çağırırız:

```python
project_root = get_project_root()
```


```python
def load_config(config_path: str = "config/config.yaml") -> dict:
```

Bu fonksiyon config/config.yaml dosyasını okur ve ayarları Python dictionary olarak döndürür.

config_path: str → okunacak config dosyasının yolu
"config/config.yaml" → varsayılan config dosyası
-> dict → fonksiyon dictionary döndürür

```python
full_path = PROJECT_ROOT / config_path
```

Config dosyasının tam yolunu oluşturur.

Örnek:
/Users/s/Desktop/baku-house-price-api/config/config.yaml

```python
if not full_path.exists():
    raise FileNotFoundError(...)
```

Config dosyası yoksa hata verir.
Bu kontrol sayesinde eksik dosya problemi hemen anlaşılır.

```python
with open(full_path, "r", encoding="utf-8") as file:
```

Config dosyasını okuma modunda açar.
"r" → read mode
encoding="utf-8" → karakter problemi olmaması için
config = yaml.safe_load(file)
YAML dosyasını Python dictionary formatına çevirir.

Örnek:
config["paths"]["raw_data"]

```python
if not config:
    raise ValueError("Config file is empty.")
``` 
Config dosyası boşsa hata verir.

```python
return config
```
Okunan config ayarlarını geri döndürür.