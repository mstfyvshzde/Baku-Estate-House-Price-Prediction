
## Ne işe yarar?

Bu dosya data cleaning işlemini çalıştıran script dosyasıdır.

Asıl temizleme fonksiyonları `src/data/cleaning.py` içinde durur.  
Bu dosya onları çağırır ve süreci başlatır.

Çalıştırma komutu:

```bash
python3 scripts/clean_data.py
```

```python
from pathlib import Path
import sys
```

Path → proje yolunu bulmak için kullanılır.
sys → Python’a proje klasörünü tanıtmak için kullanılır.

```python
PROJECT_ROOT = Path(__file__).resolve().parents[1]
```

Bu satır proje ana klasörünü bulur.
Bu dosya burada olduğu için:
scripts/clean_data.py
parents[1] proje ana klasörüne çıkar:
baku-house-price-api/

```python
sys.path.append(str(PROJECT_ROOT))
```

Python’a proje ana klasörünü tanıtır.

Amaç:
from src.utils.config import load_config
gibi importların düzgün çalışmasıdır.

Proje fonksiyonlarını import etmek
```python
from src.utils.config import load_config
from src.data.cleaning import clean_dataset, save_cleaning_outputs
```

Bu satırlar gerekli fonksiyonları çağırır.
load_config() → config dosyasını okur
clean_dataset() → raw datayı temizler
save_cleaning_outputs() → sonuçları dosyaya kaydeder


```python
def main():
```
Script çalışınca yapılacak ana işlemler burada yazılır.

```python
config = load_config()
```
config/config.yaml dosyasını okur.
Yani:
path bilgileri
kolon adları
validation kuralları
Python içine alınır.

```python
clean_data, removed_rows, summary = clean_dataset(config)
```
Data cleaning işlemini çalıştırır.
Sonuçta 3 şey döner:
clean_data → temiz data
removed_rows → hatalı/silinen satırlar
summary → temizleme özeti


```python
save_cleaning_outputs(
    clean_data=clean_data,
    removed_rows=removed_rows,
    summary=summary,
    config=config
)
```

Sonuçları dosyaya kaydeder.
Oluşan dosyalar:
data/interim/clean_data.csv
outputs/reports/removed_rows.csv
outputs/reports/cleaning_summary.json


```python
print("Data cleaning completed.")
Temizleme işleminin bittiğini terminalde gösterir.
print(f"Original rows: {summary['original_rows']}")
print(f"Clean rows: {summary['clean_rows']}")
print(f"Removed rows: {summary['removed_rows']}")
Temizleme özetini terminalde gösterir.
başlangıç satır sayısı
temiz kalan satır sayısı
silinen satır sayısı
Script başlatma bölümü
```


```python
if __name__ == '__main__':
    main()
```
Bu satır dosya direkt çalıştırıldığında main() fonksiyonunu başlatır.
Yani şu komutu yazınca:


python3 scripts/clean_data.py
otomatik olarak main() çalışır.