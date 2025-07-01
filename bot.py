import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Inisialisasi Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
gc = gspread.authorize(credentials)
sheet = gc.open_by_url(os.getenv("SHEET_URL")).sheet1

# Fungsi untuk mengecek apakah angka adalah double
def is_double(nomor):
    return len(str(nomor)) == 2 and str(nomor)[0] == str(nomor)[1]

# Fungsi menangani pesan masuk
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.message.chat_id

    if ":" in text:
        try:
            pasaran, angka = map(str.strip, text.split(":"))
            angka = int(angka)

            waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            status = "DOBEL" if is_double(angka) else "BELUM DOBEL"

            # Simpan ke sheet
            sheet.append_row([waktu, pasaran, angka, status])

            # Kirim balasan
            if status == "DOBEL":
                reply = f"✅ Pasaran *{pasaran}*: {angka} tercatat.\n🟢 Status: SUDAH DOBEL → Reset Aman"
            else:
                reply = f"✅ Pasaran *{pasaran}*: {angka} tercatat.\n🔴 Status: BELUM DOBEL (Waspada)"

            await context.bot.send_message(chat_id=chat_id, text=reply, parse_mode='Markdown')
        except:
            await context.bot.send_message(chat_id=chat_id, text="Format salah. Gunakan: `Pasaran A: 55`", parse_mode='Markdown')
    else:
        await context.bot.send_message(chat_id=chat_id, text="Format salah. Gunakan: `Pasaran A: 55`", parse_mode='Markdown')


async def main():
    bot_token = os.getenv("BOT_TOKEN")
    webhook_url = os.getenv("WEBHOOK_URL")

    app = ApplicationBuilder().token(bot_token).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    # Set Webhook
    await app.bot.set_webhook(webhook_url)
    logging.info("🤖 Bot aktif via Webhook!")

    await app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        webhook_url=webhook_url
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
