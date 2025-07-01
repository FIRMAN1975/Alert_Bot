# Bot Pasaran 2D Telegram

Bot Telegram yang menerima input nomor 2D dari berbagai pasaran dan menyimpan data ke Google Sheets.

## 🚀 Cara Menjalankan (Local / Render)

### 1. Install dependensi
```
pip install -r requirements.txt
```

### 2. Buat file `.env`
Salin dari `.env.example` dan isi dengan token bot Telegram dan URL Webhook Google Apps Script.

### 3. Jalankan bot (lokal)
```
python bot.py
```

## 📦 Perintah Telegram
- Kirim: `Pasaran A: 45`
- `/status` → Lihat status semua pasaran
- `/histori Pasaran A` → Lihat histori angka
