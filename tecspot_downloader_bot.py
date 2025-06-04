
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
import instaloader

# لاگ برای اشکال‌زدایی
logging.basicConfig(level=logging.INFO)

# شروع ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! 👋\nلینک پست یا استوری اینستاگرام را برای دانلود بفرست 🌐📥")

# دانلود از اینستاگرام
async def download_instagram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    chat_id = update.effective_chat.id

    if "instagram.com" not in url:
        await update.message.reply_text("❗ لطفاً یک لینک معتبر اینستاگرام بفرست.")
        return

    folder = f"downloads/{chat_id}"
    os.makedirs(folder, exist_ok=True)

    loader = instaloader.Instaloader(dirname_pattern=folder, download_videos=True, save_metadata=False)

    try:
        shortcode = url.split("/p/")[-1].split("/")[0] if "/p/" in url else url.rstrip("/").split("/")[-1]
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        loader.download_post(post, target=folder)

        sent = False
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith(('.jpg', '.mp4')):
                    with open(os.path.join(root, file), 'rb') as f:
                        await update.message.reply_document(f)
                        sent = True

        if sent:
            await update.message.reply_text("✅ دانلود انجام شد!")
        else:
            await update.message.reply_text("⚠️ فایلی برای ارسال پیدا نشد.")

    except Exception as e:
        logging.error(str(e))
        await update.message.reply_text("❌ خطا در دانلود! ممکنه پیج خصوصی باشه یا لینک اشتباه باشه.")

# اجرای اصلی
def main():
    TOKEN = "7996560379:AAFonoVy76Ew50tu_WznVppY4hO12wYUqrg"
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_instagram))

    print("ربات در حال اجراست...")
    app.run_polling()

if __name__ == "__main__":
    main()
