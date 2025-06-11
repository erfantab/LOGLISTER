from telegram import Update, Message
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

TOKEN = '7360314470:AAE2kFtkVdYyCLZrUhbGsrVYV6SDSRtGsrg'

# فقط این افراد مجازن استفاده کنن
ALLOWED_USERS = [56271843180, 680132542, 5959049408, 1942111839]
ADMIN_ID = 1942111839  # پیام‌ها به این آیدی فوروارد می‌شن

user_messages = {}  # برای ذخیره کردن آیدی کاربر و آیدی پیام فوروارد شده

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id

    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("❌ شما به این بات دسترسی ندارید.")
        return

    if user_id == ADMIN_ID:
        await update.message.reply_text("✅ حالت مدیری فعال شد. منتظر پیام‌ها باش.")
    else:
        await update.message.reply_text(
            "یوزرنیم کاربر رو وارد بکن و یه فاصله بزار بعدش بگو کدوم یکی از اینارو بهت بگه:\n"
            "گروه ها | کانال ها | دوستان"
        )

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    message_text = update.message.text

    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("❌ شما به این بات دسترسی ندارید.")
        return

    # اگر ادمینه و داره ریپلای می‌کنه
    if user_id == ADMIN_ID:
        if update.message.reply_to_message:
            original_msg = update.message.reply_to_message
            forwarded_user_id = None
            for uid, mid in user_messages.items():
                if mid == original_msg.message_id:
                    forwarded_user_id = uid
                    break
            if forwarded_user_id:
                await context.bot.send_message(chat_id=forwarded_user_id, text=update.message.text)
                await update.message.reply_text("📤 پاسخ فرستاده شد")
            else:
                await update.message.reply_text("❌ پیام اصلی پیدا نشد.")
        else:
            await update.message.reply_text("⛔️ این پیام ریپلای نیست.")
        return

    # کاربر معمولی
    if message_text.startswith('@') and len(message_text.split()) > 1:
        sent = await context.bot.send_message(chat_id=ADMIN_ID, text=f"📥 از {user_id}:\n{message_text}")
        user_messages[user_id] = sent.message_id
        await update.message.reply_text(
            "آیدی دریافت شد، چون یکی دیگه داره از بات استفاده میکنه، برای جلوگیری از بن شدن، تو صف انتظاری. تا 10 دیقه تو مشتته"
        )
    else:
        await update.message.reply_text("فرمت اشتباهه! یوزرنیم با @ و بعدش یکی از گزینه‌ها رو بنویس.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))

    print("🤖 Bot is running...")
    app.run_polling()
