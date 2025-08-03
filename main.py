
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = "7806713370:AAE4BcVS9XICvAvjQ0Iod9BBT2JLJ4QOkTU"
SUPPORT_USER_ID = 5065547877

# استارت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💠 پلن تک‌کاربره (80هزار)", callback_data="plan1")],
        [InlineKeyboardButton("💠 پلن دوکاربره (120هزار)", callback_data="plan2")],
        [InlineKeyboardButton("💎 پلن نمایندگی / عمده", callback_data="plan3")],
        [InlineKeyboardButton("📤 ارسال رسید پرداخت", callback_data="send_receipt")],
        [InlineKeyboardButton("🆘 ارتباط با پشتیبانی", callback_data="support")]
    ]
    await update.message.reply_text(
        "سلام عزیز! به *Paneliyano* خوش اومدی 🌟\nلطفاً یکی از گزینه‌ها رو انتخاب کن:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# دکمه‌ها
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("plan"):
        await query.message.reply_sticker("CAACAgUAAxkBAAEcJAZlkgUUCcD_IbLruq0x-luK9nUodQAC-QEAAj-V0VViPZPzTKuQbjQE")
        await query.message.reply_text("🍫 پلن‌ها در حال ساختن هستن قربونت! به زودی آماده‌ن!")

    elif query.data == "send_receipt":
        await query.message.reply_text("📥 لطفاً رسید پرداخت خودتو (عکس یا متن) همینجا بفرست تا بررسی کنیم 🙏")

    elif query.data == "support":
        await context.bot.send_message(
            chat_id=SUPPORT_USER_ID,
            text=f"🆘 درخواست پشتیبانی:\nنام: {query.from_user.full_name}\nآیدی عددی: {query.from_user.id}\nیوزرنیم: @{query.from_user.username or 'نداره'}",
            parse_mode="Markdown"
        )
        await query.message.reply_text("✅ درخواست شما برای پشتیبانی ارسال شد.")

# دریافت رسید پرداخت
async def handle_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    caption = f"📩 رسید پرداخت جدید!\n\n👤 نام: {user.full_name}\n🆔 آیدی عددی: {user.id}\n📎 یوزرنیم: @{user.username or 'نداره'}"

    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        await context.bot.send_photo(chat_id=SUPPORT_USER_ID, photo=file_id, caption=caption, parse_mode="Markdown")
        await update.message.reply_text("✅ رسید شما ارسال شد. بررسی می‌کنیم و اطلاع می‌دیم ✨")
    else:
        text = update.message.text
        await context.bot.send_message(chat_id=SUPPORT_USER_ID, text=f"{caption}\n\n📝 متن رسید:\n{text}", parse_mode="Markdown")
        await update.message.reply_text("✅ رسید شما دریافت شد عزیز! منتظر تایید باش ✌️")

# اجرا
if name == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_receipt))
    print("✅ ربات اجرا شد")
    app.run_polling()
