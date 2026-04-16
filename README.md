# Bulk File Renamer / Toplu Dosya Yeniden Adlandırıcı

Windows için GUI tabanlı toplu dosya yeniden adlandırma aracı. Tek bir arayüzde çoklu kural (bul/değiştir, önek, sonek, numaralandırma, harf dönüşümü) aynı anda uygulanabilir. Python + Tkinter ile yazılmıştır.

A Windows GUI tool for bulk file renaming. Combine multiple rules (find/replace, prefix, suffix, numbering, case conversion) in a single pass. Written in Python with Tkinter.

---

## Özellikler / Features

- **Bul ve Değiştir** — düz metin veya regex
- **Çoklu Bul/Değiştir** — satır satır yüzlerce eşleştirme (ör: `eskiAd yeniAd`)
- **Önek / Sonek** ekleme
- **Numaralandırma** — `foto001`, `foto002`, ... (taban ad + başlangıç + basamak)
- **Harf Dönüşümü** — küçük / BÜYÜK / İlk Harfler
- **Alt klasör desteği** — opsiyonel olarak alt klasörleri de tara
- **Uzantı filtresi** — ör. `.jpg,.png`
- **Önizleme** — uygulamadan önce yeni adları gör (çakışmalar renkli vurgulanır)
- **Geri Al** — son işlemi geri döndür
- **Güvenli yeniden adlandırma** — iki aşamalı rename (`a ↔ b` takası da çalışır)

## Kurulum / Installation

### Seçenek 1: Hazır .exe (önerilen)

[Releases](../../releases) sayfasından en son sürümün `.exe` dosyasını indir ve çalıştır. Python kurulumu gerekmez.

### Seçenek 2: Kaynaktan çalıştır

```bash
git clone https://github.com/ayberkbgln/bulk-file-renamer.git
cd bulk-file-renamer
python toplu_rename.py
```

Python 3.8+ gerekli. Tkinter standart kütüphanede olduğu için ek bağımlılık yok.

### Seçenek 3: Kendi .exe'ni derle

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "TopluDosyaYenidenAdlandirici" toplu_rename.py
```

Çıktı `dist/` klasöründe olur.

## Kullanım / Usage

1. **Gözat...** ile klasörü seç
2. İsteğe bağlı: alt klasörleri dahil et, uzantı filtresi ekle
3. İstediğin işlemleri işaretle ve değerleri gir
4. **Önizleme** → listeyi kontrol et (yeşil=OK, kırmızı=çakışma)
5. **Uygula** → onay ver
6. Hata olursa **Geri Al** ile geri dönebilirsin

### Çoklu Bul/Değiştir Formatı

Her satır bir kural:

```
eskiKelime yeniKelime
IMG_ Tatil_
DSC_ Foto_
_v1
```

- **Ayraç:** TAB veya boşluk (ilk boşluk grubu ayraç kabul edilir)
- **Tek kelime yazarsan** → o metin silinir (yukarıdaki `_v1` örneği)
- **`#` ile başlayan satırlar** yorum sayılır

## Ekran Görüntüsü / Screenshot

<img width="980" height="930" alt="image" src="https://github.com/user-attachments/assets/673b42b7-6d82-481d-af25-9336f418affc" />


## Katkıda Bulunma / Contributing

Pull request ve issue'lar açıktır. Öneriler için issue açmaktan çekinme.

## Lisans / License

[MIT](LICENSE)
