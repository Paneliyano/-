
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputSticker
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# لاگ برای بررسی خطاها
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# اطلاعات شما
BOT_TOKEN = "7806713370:AAE4BcVS9XICvAvjQ0Iod9BBT2JLJ4QOkTU"
SUPPORT_USERNAME = "@Amo_pouria"
SUPPORT_ID = 5065547877  # آیدی عددی

# استیکر شکلات (پیشنهادی: جایگزین کن با استیکر دلخواه خودت)
STICKER_ID = "CAACAgQAAxkBAAEBG3lgZKRKNrxAvJt3pckMlMOUWYPm4AACRgoAAuAg4VY8NPB-cV1YiDAE"  # شکلات

# پیام خوش‌آمد و پرداخت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🍫 پلن تک کاربره - 1 ماهه - 80 تومان", callback_data="plan1")],
        [InlineKeyboardButton("🍬 پلن دو کاربره - 1 ماهه - 120 تومان", callback_data="plan2")],
        [InlineKeyboardButton("📦 پلن عمده / نمایندگی", callback_data="reseller")],
        [InlineKeyboardButton("🆘 ارتباط با پشتیبانی", callback_data="support")]
    ]
    await update.message.reply_text(
        "سلام رفیق خوش اومدی 🌟\n\n"
        "فعلاً درگاه نداریم، لطفاً مبلغ رو به کارت زیر واریز کن و رسیدش رو برامون بفرست:\n\n"
        "💳 6219 8619 2805 6588\n"
        "به نام پوریا خسروی - بانک سامان\n\n"
        "سرویس تست هم بخوای بگو، داریم 🍭",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# دکمه‌ها
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data in ["plan1", "plan2", "reseller"]:
        await query.message.reply_sticker(STICKER_ID)
        await query.message.reply_text("فعلاً در حال ساخت پنل هستیم 🍬 تا آماده بشه این شکلات مال تو 😄")

    elif query.data == "support":
        await context.bot.send_message(
            chat_id=SUPPORT_ID,
            text=f"🔔 یه نفر نیاز به پشتیبانی داره: @{query.from_user.username or 'بدون نام کاربری'}"
        )
        await query.message.reply_text("پیام شما به پشتیبانی ارسال شد ✅")

# اجرای ربات
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("✅ ربات در حال اجراست...")
    app.run_polling()
