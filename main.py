import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# تنظیم لاگ برای دیباگ راحت‌تر
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# آیدی پشتیبانی و توکن
SUPPORT = "@amo_pouria"
BOT_TOKEN = "7806713370:AAFKYhXskmj5g_uASsD0EFXIpp7trlnUX6k"

# تابع استارت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📦 دریافت پلن تستی", callback_data="get_plan")],
        [InlineKeyboardButton("🆘 تماس با پشتیبانی", url=f"https://t.me/{SUPPORT.strip('@')}")]
    ]
    await update.message.reply_text(
        "سلام! خوش اومدی 🌟\nبرای دریافت پلن، دکمه زیر رو بزن:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# تابع هندل کلیک روی دکمه‌ها
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

# اجرای اصلی ربات
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("✅ ربات فعال شد...")
    app.run_polling()
