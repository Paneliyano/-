
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputSticker
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = "7806713370:AAE4BcVS9XICvAvjQ0Iod9BBT2JLJ4QOkTU"
SUPPORT_USER_ID = 5065547877  # آی‌دی عددی برای پی‌وی

# استارت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💠 پلن تک‌کاربره 1 ماهه (80هزار)", callback_data="plan1")],
        [InlineKeyboardButton("💠 پلن دوکاربره 1 ماهه (120هزار)", callback_data="plan2")],
        [InlineKeyboardButton("💎 پلن عمده / نمایندگی", callback_data="plan3")],
        [InlineKeyboardButton("🆘 ارتباط با پشتیبانی", callback_data="support")]
    ]
    await update.message.reply_text(
        "سلام عزیز 🌟 به *Paneliyano* خوش اومدی!\nیکی از گزینه‌ها رو انتخاب کن:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# هندلر دکمه‌ها
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # پیام آماده
    msg = "🍫 عزیز دل فعلاً پنل در حال ساخت هست!\nبه زودی بهترین پلن‌ها برات فعال می‌شه 😍"

    if query.data in ["plan1", "plan2", "plan3"]:
        # ارسال پیام به کاربر
        await query.message.reply_sticker("CAACAgUAAxkBAAEcJAZlkgUUCcD_IbLruq0x-luK9nUodQAC-QEAAj-V0VViPZPzTKuQbjQE")  # استیکر شکلات
        await query.message.reply_text(msg)

    elif query.data == "support":
        await context.bot.send_message(
            chat_id=SUPPORT_USER_ID,
            text=f"🆘 یک نفر درخواست پشتیبانی داد:\n\nنام کاربر: {query.from_user.full_name}\nیوزرنیم: @{query.from_user.username or 'نداره'}\nآی‌دی عددی: {query.from_user.id}",
            parse_mode="Markdown"
        )
        await query.message.reply_text("🧑‍💻 درخواست شما به پشتیبانی ارسال شد. منتظر پاسخ باش عزیز ✨")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("✅ ربات در حال اجراست...")
    app.run_polling()
