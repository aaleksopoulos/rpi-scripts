from dotenv import load_dotenv
import os, logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from wakeonlan import send_magic_packet

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
USER_ID = os.getenv("USER_ID")
PC_MAC = os.getenv("PC_MAC")

# Ρύθμιση Logging για να βλέπεις σφάλματα
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# Το httpx γράφει κάθε URL στο log σε INFO, και τα URL περιέχουν το API_TOKEN
logging.getLogger("httpx").setLevel(logging.WARNING)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Γεια! Στείλε /wake για να ανοίξω το PC.")

async def wake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    print("user_id", user_id)
   
    if user_id == int(USER_ID):
        # Εδώ βάζεις τη MAC Address του PC σου
        send_magic_packet(PC_MAC)
        await update.message.reply_text("🚀 Το Magic Packet στάλθηκε!")
    else:
        await update.message.reply_text("🚫 Μη εξουσιοδοτημένος χρήστης.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(API_TOKEN).build()

    # Handlers για τις εντολές
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('wake', wake))

    application.run_polling()
