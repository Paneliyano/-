import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

SUPPORT = "@amo_pouria"
BOT_TOKEN = "7806713370:AAFKYhXskmj5g_uASsD0EFXIpp7trlnUX6k"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        keyboard = [
            [InlineKeyboardButton("📦 دریافت پلن تستی", callback_data="get_plan")],
            [InlineKeyboardButton("🆘 تماس با پشتیبانی", url=f"https://t.me/{SUPPORT.strip('@')}")]
        ]
        await update.message.reply_text(
            "سلام! خوش اومدی 🌟\nبرای دریافت پلن، دکمه زیر رو بزن:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        logging.error(f"خطا در تابع start: {e}")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()

        if query.data == "get_plan":
            await query.edit_message_text(
                "✅ پلن تستی فعال شد!\n"
                "کانفیگ تستی شما:\n\n"
                "vless://test-config-generated\n\n"
                f"در صورت نیاز به پلن بیشتر با پشتیبانی تماس بگیر:\n{SUPPORT}",
                parse_mode="Markdown"
            )
    except Exception as e:
        logging.error(f"خطا در تابع button_handler: {e}")

if __name__ == '__main__':
    try:
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(button_handler))
        print("✅ ربات در حال اجراست...")
        app.run_polling()
    except Exception as e:
        print("❌ خطا در اجرای کلی ربات:", e)
