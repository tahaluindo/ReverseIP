from telegram.ext.updater import Updater
updater = Updater("5570084115:AAHKp7_DyntWYa21ja2duAmqbu2iJc28gTM", use_context=True)

def send_msg(text, chat_id):
    updater.bot.sendMessage(chat_id, text)
