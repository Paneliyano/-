import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# تنظیم لاگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# توکن ربات
BOT_TOKEN = "7806713370:AAFKYhXskmj5g_uASsD0EFXIpp7trlnUX6k"

# آیدی عددی پشتیبانی
ADMIN_ID = 5065547877

# تابع استارت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🍫 پلن تک‌کاربره 1 ماهه - 80", callback_data="plan1")],
        [InlineKeyboardButton("🍫 پلن دوکاربره 1 ماهه - 120", callback_data="plan2")],
        [InlineKeyboardButton("🍫 پلن عمده (نمایندگی)", callback_data="reseller")],
        [InlineKeyboardButton("🧑‍💼 ارتباط با پشتیبانی", url="https://t.me/Amo_pouria")]
    ]
    await update.message.reply_text(
        "سلام خوش اومدی به پنلیانو 🌟\n\n"
        "فعلاً چون درگاه پرداخت مشکل داره، مبلغ پلن رو به شماره کارت زیر واریز کن و رسید رو ارسال کن:\n\n"
        "💳 شماره کارت: 6219 8619 2805 6588\n"
        "👤 بنام پوریا خسروی (بانک سامان)\n\n"
        "✅ بعد از واریز، رسید رو اینجا بفرست تا بررسی بشه.",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# هندل دکمه‌ها
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    sticker = "CAACAgUAAxkBAAIBD2YvLWi6i_1sGNNNdOwoV_yOiyBEAAJGAAPtDl9Tihgf2szdWjsZBA"

    await query.message.reply_sticker(sticker)

    await query.edit_message_text(
        "این پلن فعلاً در دست احداثه 👷‍♂️\nبه زودی فعال میشه، صبور باش 🌟"
    )

# هندل پیام رسید و ارسال برای ادمین
async def handle_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    if update.message.photo or update.message.document:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📥 رسید جدید از @{user.username or user.first_name} (ID: {user.id})"
        )
        await context.bot.forward_message(
            chat_id=ADMIN_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )
        await update.message.reply_text("✅ رسیدت ثبت شد، بررسی می‌کنیم و خبرت می‌کنیم.")
    else:
        await update.message.reply_text("لطفاً رسید رو به صورت عکس یا فایل بفرست 🌟")

# اجرای اصلی
if name == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.ALL, handle_receipt))
    print("✅ ربات در حال اجراست...")
    app.run_polling()
