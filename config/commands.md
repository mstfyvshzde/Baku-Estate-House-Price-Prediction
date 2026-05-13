# Config Dosyası Notları

## Dosya

`config/config.yaml`

## Ne işe yarar?

Bu dosya proje ayarlarını tek yerde tutar.

İçinde:

- dosya yolları
- kolon adları
- data temizleme kuralları

bulunur.

Amaç: Python kodunun içine sürekli dosya yolu ve kural yazmamak.

---

## paths bölümü
Bu bölüm dosya yollarını gösterir.
raw_data → ham verinin yeri
clean_data → temizlenmiş verinin kaydedileceği yer
removed_rows → silinen/hatalı satırların kaydedileceği yer
cleaning_summary → temizleme özetinin kaydedileceği JSON dosyası

## schema bölümü
Bu bölüm CSV dosyasındaki kolon adlarını belirler.
Eğer raw data içinde kolon başlığı yoksa, Python bu isimleri kullanır.
district → rayon
location → lokasyon
rooms → oda sayısı
area → evin sahesi
floor → bulunduğu kat
total_floors → binadaki toplam kat
price → evin fiyatı

## validation bölümü
Bu bölüm data temizleme kurallarını tutar.
Yani hangi değerler normal, hangi değerler hatalı sayılır onu belirler.
Örnek:
- oda sayısı 1 ile 10 arasında olmalı
- alan 15 ile 500 m² arasında olmalı
- kat en az 1 olmalı
- toplam kat 1 ile 60 arasında olmalı
- fiyat 10.000 ile 2.000.000 arasında olmalı
Bu kurallara uymayan satırlar temiz dataya alınmaz.




