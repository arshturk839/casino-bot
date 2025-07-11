import logging from telegram import Update, ReplyKeyboardMarkup from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes import requests from config import TELEGRAM_TOKEN, CREATE_ID_URL, DEPOSIT_URL, WITHDRAW_URL, BALANCE_URL, STATIC_UPI_ID

logging.basicConfig(level=logging.INFO)

menu_keyboard = ReplyKeyboardMarkup( [["🆔 Create ID", "💸 Add Money"], ["💵 Withdraw", "💰 Balance"]], resize_keyboard=True )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text("Welcome to the Casino Bot 🌰", reply_markup=menu_keyboard)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE): text = update.message.text user_id = str(update.effective_user.id)

if text == "🆔 Create ID":
    data = {"telegram_id": user_id, "name": update.effective_user.first_name}
    response = requests.post(CREATE_ID_URL, data=data)
    await update.message.reply_text(f"🆔 ID Created: {response.text}")

elif text == "💸 Add Money":
    await update.message.reply_text("Send UTR and Amount like this:\nutr:1234567890 amount:500")

elif text.startswith("utr:") and "amount:" in text:
    try:
        utr = text.split("utr:")[1].split("amount:")[0].strip()
        amount = text.split("amount:")[1].strip()
        data = {"telegram_id": user_id, "utr": utr, "amount": amount}
        response = requests.post(DEPOSIT_URL, data=data)
        await update.message.reply_text(f"💸 Deposit:\n{response.text}")
    except:
        await update.message.reply_text("❌ Format error. Please send in correct format.")

elif text == "💵 Withdraw":
    await update.message.reply_text("Send withdrawal in format:\n\namount:500\nupi:yourupi@upi")

elif text.startswith("amount:") and "upi:" in text:
    try:
        amount = text.split("amount:")[1].split("upi:")[0].strip()
        upi_id = text.split("upi:")[1].strip()
        data = {"telegram_id": user_id, "amount": amount, "upi_id": upi_id}
        response = requests.post(WITHDRAW_URL, data=data)
        await update.message.reply_text(f"💵 Withdraw:\n{response.text}")
    except:
        await update.message.reply_text("❌ Format error. Please send in correct format.")

elif text == "💰 Balance":
    params = {"telegram_id": user_id}
    response = requests.get(BALANCE_URL, params=params)
    await update.message.reply_text(f"💰 Balance:\n{response.text}")

else:
    await update.message.reply_text("Invalid command. Please use buttons.", reply_markup=menu_keyboard)

def main(): app = ApplicationBuilder().token(TELEGRAM_TOKEN).build() app.add_handler(CommandHandler("start", start)) app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)) app.run_polling()

if name == "main": main()

