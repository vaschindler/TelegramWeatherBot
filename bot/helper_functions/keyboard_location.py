from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import telegram


def get_keyboard_location(update):
    location_keyboard = telegram.KeyboardButton(text="send_location", request_location=True)
    custom_keyboard = [[ location_keyboard]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text(text="Would you mind sharing your location with me?",
                              reply_markup=reply_markup)
