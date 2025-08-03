import logging
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)

# لاگ برای بررسی خطا
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# مشخصات
BOT_TOKEN = "7806713370:AAFKYhXskmj5g_uASsD0EFXIpp7trlnUX6k"
ADMIN_ID = 5065547877
SUPPORT = "@amo_pourya"

# استیکر خوشگل 🍬
STICKER_ID = "CAACAgUAAxkBAAEZdc1mZoXtNiUVJOU3Ka3cZKBi2PHyCwACVwoAAhdHcVURsMeYobJibzAE"

# فرمان استارت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📶 تک‌کاربره | 1 ماهه - 80", callback_data="plan_1")],
        [InlineKeyboardButton("👥 دوکاربره | 1 ماهه - 120", callback_data="plan_2")],
        [InlineKeyboardButton("🏢 خرید عمده (نمایندگی)", callback_data="plan_vip")],
        [InlineKeyboardButton("🧾 ارسال رسید پرداخت", callback_data="send_receipt")],
        [InlineKeyboardButton("🆘 ارتباط با پشتیبانی", url=f"https://t.me/{SUPPORT.strip('@')}")]
    ]
    text = (
        "سلام به *پنلیانو* خوش اومدی 🎉\n\n"
        "فعلاً به دلیل مشکل درگاه، لطفاً مبلغ رو به کارت زیر واریز کن:\n\n"
        "💳 6219 8619 2805 6588\n"
        "👤 پوریا خسروی\n"
        "🏦 بانک سامان\n\n"
        "بعد رسید پرداخت رو داخل ربات بفرست تا تأیید کنیم ✅"
    )
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

# دکمه‌ها
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_sticker(STICKER_ID)

    if query.data == "plan_1":
        await query.message.reply_text("🍬 پلن *تک‌کاربره* انتخاب شد.\nبه‌زودی فعال می‌شه!")
    elif query.data == "plan_2":
        await query.message.reply_text("🍬 پلن *دوکاربره* انتخاب شد.\nدر حال آماده‌سازی!")
    elif query.data == "plan_vip":
        await query.message.reply_text("🍬 پلن *نمایندگی* در دست احداثه، به زودی میاد!")
    elif query.data == "send_receipt":
        await query.message.reply_text("🧾 لطفاً رسید پرداخت رو ارسال کن (عکس یا متن).")

# رسید پرداخت
async def handle_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    caption = f"📥 رسید جدید:\n👤 {user.full_name}\n🔗 @{user.username or 'نداره'}\n🆔 {user.id}"
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        await context.bot.send_message(chat_id=ADMIN_ID, text=caption, parse_mode="Markdown")
        await context.bot.send_photo(chat_id=ADMIN_ID, photo=file_id)
    elif update.message.text:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"{caption}\n📝 {update.message.text}", parse_mode="Markdown")

    await update.message.reply_text("✅ رسید دریافت شد. منتظر تأیید باش.")

# اجرای ربات
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_receipt))

    print("🤖 ربات با موفقیت اجرا شد.")
    app.run_polling()
