import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.error import TelegramError

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- CONFIGURATION (UPDATED TOKEN) ---
BOT_TOKEN = "8936580905:AAHYZu2sOumvWn4MEm0U7L5WIEJALVPn2LQ"  
PUBLIC_CHANNEL = "@privately_009"  
BLOG_LINK = "https://notesphere12.blogspot.com"
PRIVATE_CHANNEL_LINK = "https://t.me/+hKPnP9PA0zwyOTFl"
# -------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    
    try:
        member = await context.bot.get_chat_member(chat_id=PUBLIC_CHANNEL, user_id=user_id)
        if member.status in ['member', 'administrator', 'creator']:
            keyboard = [[InlineKeyboardButton("📚 Access Premium Material", url=PRIVATE_CHANNEL_LINK)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(f"Welcome back {first_name}! Tasks complete hain:", reply_markup=reply_markup)
            return
    except TelegramError:
        pass

    keyboard = [
        [InlineKeyboardButton("1️⃣ Join Telegram Channel", url=f"https://t.me/{PUBLIC_CHANNEL.strip('@')}")],
        [InlineKeyboardButton("2️⃣ Visit Our Blog/Website", url=BLOG_LINK)],
        [InlineKeyboardButton("Done ✅ (Verify Tasks)", callback_data="verify_tasks")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"Hello {first_name}!\n\nPremium Material unlock karne ke liye ye 2 Tasks complete karein:", reply_markup=reply_markup)

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    try:
        member = await context.bot.get_chat_member(chat_id=PUBLIC_CHANNEL, user_id=user_id)
        if member.status in ['member', 'administrator', 'creator']:
            keyboard = [[InlineKeyboardButton("🎉 Enter Private Channel", url=PRIVATE_CHANNEL_LINK)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text="✅ Tasks Verified!\n\nPrivate Channel join karein:", reply_markup=reply_markup)
        else:
            keyboard = [
                [InlineKeyboardButton("1️⃣ Join Telegram Channel", url=f"https://t.me/{PUBLIC_CHANNEL.strip('@')}")],
                [InlineKeyboardButton("2️⃣ Visit Our Blog/Website", url=BLOG_LINK)],
                [InlineKeyboardButton("Done ✅ (Verify Tasks)", callback_data="verify_tasks")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text="❌ Verification Failed! Pehle channel join karein.", reply_markup=reply_markup)
    except TelegramError:
        await query.edit_message_text(text="Error: Bot ko public channel ka Admin banayein pehle!")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(verify, pattern="verify_tasks"))
    print("Bot cloud par chalu ho raha hai...")
    application.run_polling()

if __name__ == '__main__':
    main()
  
