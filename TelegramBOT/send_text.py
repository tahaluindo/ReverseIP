from telegram.ext.updater import Updater
updater = Updater("Dapatkan Token Dari BOT Father", use_context=True)

def send_msg(text, chat_id):
    updater.bot.sendMessage(chat_id, text)
