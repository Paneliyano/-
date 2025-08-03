import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# تنظیمات
BOT_TOKEN = "7806713370:AAFKYhXskmj5g_uASsD0EFXIpp7trlnUX6k"
ADMIN_ID = 5065547877
SUPPORT_USERNAME = "Amo_pouria"
CARD_INFO = "💳 شماره کارت: 6219 8619 2805 6588\n👤 پوریا خسروی - بانک سامان"

# لاگ
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# استارت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📦 پلن تک‌کاربره (۸۰)", callback_data="plan_1")],
        [InlineKeyboardButton("👥 دوکاربره (۱۲۰)", callback_data="plan_2")],
        [InlineKeyboardButton("🧰 خرید عمده (نمایندگی)", callback_data="plan_reseller")],
        [InlineKeyboardButton("🆘 پشتیبانی", url=f"https://t.me/{SUPPORT_USERNAME}")]
    ]
    await update.message.reply_text(
        f"سلام خوش اومدی به پنل V2RY 🌐\n\n{CARD_INFO}\n\n🔻برای خرید، یکی از پلن‌ها رو انتخاب کن و رسید رو بعدش بفرست تو همین ربات.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# دکمه‌ها
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data.startswith("plan_"):
        msg = {
            "plan_1": "📦 پلن تک‌کاربره (۱ ماهه - ۸۰ هزار)",
            "plan_2": "👥 پلن دوکاربره (۱ ماهه - ۱۲۰ هزار)",
            "plan_reseller": "🧰 خرید عمده / نمایندگی"
        }.get(query.data, "❌ پلن نامشخصه")

        await context.bot.send_sticker(chat_id=user_id, sticker="CAACAgUAAxkBAAEEblhmY_GymY8gPGUKAMrpT9dyLsqynQACBAEAAmSR6VcJfvay8J1Q6jQE")
        await context.bot.send_message(chat_id=user_id, text=f"{msg}\n\nاین شکلاتو داشته باش تا پنل کامل بشه 🍫")

# رسید پرداخت
async def handle_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo or update.message.document:
        caption = f"📥 رسید از @{update.message.from_user.username or 'User'}"
        await update.message.forward(chat_id=ADMIN_ID)
        await context.bot.send_message(chat_id=ADMIN_ID, text=caption)
        await update.message.reply_text("✅ رسید دریافت شد. به‌زودی بررسی می‌کنم و کانفیگ رو برات می‌فرستم.")

# اجرای اصلی
if name == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, handle_receipt))
    print("✅ ربات در حال اجراست...")
    app.run_polling()
