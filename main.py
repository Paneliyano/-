import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# تنظیم لاگ برای بررسی ارورها
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# تنظیمات
BOT_TOKEN = "7806713370:AAFKYhXskmj5g_uASsD0EFXIpp7trlnUX6k"
ADMIN_ID = 5065547877  # آیدی عددی تو
CARD_INFO = "💳 شماره کارت: 6219 8619 2805 6588\n👤 پوریا خسروی - بانک سامان"

# استارت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📦 پلن تک‌کاربره (۱ ماهه - ۸۰)", callback_data="plan_1")],
        [InlineKeyboardButton("👥 دو کاربره (۱ ماهه - ۱۲۰)", callback_data="plan_2")],
        [InlineKeyboardButton("🧰 خرید عمده (نمایندگی)", callback_data="plan_reseller")],
        [InlineKeyboardButton("🆘 ارتباط با پشتیبانی", url="https://t.me/amo_pouriya")]
    ]
    await update.message.reply_text(
        f"سلام خوش اومدی به پنل V2RY 🌐\n\n{CARD_INFO}\n\n🔻برای خرید یکی از گزینه‌های زیر رو انتخاب کن و بعد رسید رو بفرست تا تایید کنم.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# رسید → برای ادمین فوروارد کن
async def handle_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo or update.message.document:
        await context.bot.send_message(ADMIN_ID, f"📩 رسید از طرف @{update.message.from_user.username or 'بدون آیدی'}:")
        await update.message.forward(chat_id=ADMIN_ID)
        await update.message.reply_text("✅ رسیدت دریافت شد. بررسی می‌کنم و بهت اطلاع می‌دم 🌟")

# دکمه‌ها
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text_map = {
        "plan_1": "📦 پلن تک‌کاربره (۱ ماهه - ۸۰ هزار)\nفعلاً پنل در حال راه‌اندازیه، این شکلاتو داشته باش تا کامل بشه 🍫",
        "plan_2": "👥 پلن دو کاربره (۱ ماهه - ۱۲۰ هزار)\nفعلاً پنل در حال راه‌اندازیه، این شکلاتو داشته باش تا کامل بشه 🍫",
        "plan_reseller": "🧰 نمایندگی و فروش عمده\nفعلاً پنل در حال راه‌اندازیه، این شکلاتو داشته باش تا کامل بشه 🍫"
    }

    if query.data in text_map:
        await query.message.reply_sticker("CAACAgUAAxkBAAEEblhmY_GymY8gPGUKAMrpT9dyLsqynQACBAEAAmSR6VcJfvay8J1Q6jQE")
        await query.message.reply_text(text_map[query.data])

# اجرای اصلی
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, handle_receipt))
    print("✅ ربات در حال اجراست...")
    app.run_polling()
