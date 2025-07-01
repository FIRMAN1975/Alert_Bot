import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from dotenv import load_dotenv
from sheets import kirim_ke_google_sheets

load_dotenv()

data = {}

def is_double(number):
    return len(number) == 2 and number[0] == number[1]

def update_pasaran(pasaran, angka):
    if pasaran not in data:
        data[pasaran] = {"history": [], "status": "Belum Diketahui"}
    data[pasaran]["history"].append(angka)
    data[pasaran]["history"] = data[pasaran]["history"][-10:]
    if is_double(angka):
        data[pasaran]["status"] = "Aman"
    elif any(is_double(x) for x in data[pasaran]["history"]):
        data[pasaran]["status"] = "Aman"
    else:
        data[pasaran]["status"] = "Waspada"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    lines = text.splitlines()
    response = []

    for line in lines:
        if ":" in line:
            pasaran, angka = map(str.strip, line.split(":", 1))
            if not angka.isdigit() or len(angka) != 2:
                response.append(f"- {pasaran}: ⚠️ Format angka tidak valid (2 digit)")
                continue
            update_pasaran(pasaran, angka)
            status = data[pasaran]["status"]
            kirim_ke_google_sheets(pasaran, angka, status)
            simbol = "✅" if status == "Aman" else "❗"
            response.append(f"- {pasaran}: {angka} → {simbol} {status}")
    if response:
        await update.message.reply_text("\n".join(response))
    else:
        await update.message.reply_text("Format tidak dikenali. Contoh:\nPasaran A: 45")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not data:
        await update.message.reply_text("Belum ada data.")
        return
    msg = "📊 Status Pasaran:\n"
    for p, info in data.items():
        simbol = "✅" if info["status"] == "Aman" else "❗"
        msg += f"- {p}: {simbol} {info['status']}\n"
    await update.message.reply_text(msg.strip())

async def histori_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Gunakan: /histori <pasaran>")
        return
    pasaran = context.args[0]
    if pasaran not in data:
        await update.message.reply_text(f"Tidak ada data untuk {pasaran}.")
        return
    history = ", ".join(data[pasaran]["history"])
    await update.message.reply_text(f"📜 Histori {pasaran}:\n{history}")

if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("histori", histori_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("🤖 Bot aktif...")
    app.run_polling()
