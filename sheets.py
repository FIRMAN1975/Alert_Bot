import requests
import os

def kirim_ke_google_sheets(pasaran, nomor, status):
    url = os.getenv("WEBHOOK_URL")
    if not url:
        print("⚠️ URL webhook tidak ditemukan")
        return
    payload = {
        "pasaran": pasaran,
        "nomor": nomor,
        "status": status
    }
    try:
        response = requests.post(url, json=payload)
        print("✅ Terkirim:", response.text)
    except Exception as e:
        print("❌ Gagal kirim ke Google Sheets:", e)
