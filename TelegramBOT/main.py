import recon_online
import enum_online
import scan_online
import vulac_online
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import os

updater = Updater(<5570084115:AAHKp7_DyntWYa21ja2duAmqbu2iJc28gTM>, use_context=True)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello sir, Welcome to the Bot. Please write /menu to see the commands available.")

def menu(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
    /recon : To perform Reconnaissance
    /enum : To perform Enumeration
    /scan : To perform Scanning
    /vulac : To perform Vulnerability Assesment
    /special_tools : To use Special Tools.
    /miscellaneous : To use additional tools.
    """)


def reply(update: Update, context: CallbackContext):
    user_input = update.message.text
    print(user_input)
    global chat_id
    chat_id = update.message.chat_id
    print(chat_id)

    if user_input.__contains__('recon'):
        lst = user_input.split()
        print(lst)
        lst.pop()
        print(lst)
        for target in lst:
            update.message.reply_text("Reconnaissance Started For Target " + target)
            result_recon = recon_online.doRecon(target, chat_id)
            filename = target.replace('.' and 'https://', '_') + "_recon.txt"
            with open(filename, 'w') as f:
                f.write(result_recon)
            context.bot.send_document(chat_id=chat_id, document=open(filename, 'rb'), filename=filename)
            os.remove(filename)

    elif user_input.__contains__('enum'):
        lst = user_input.split()
        print(lst)
        lst.pop()
        print(lst)
        for target in lst:
            update.message.reply_text("Enumeration Started For Target " + target)
            result_enum = enum_online.doEnum(target, chat_id)
            filename = target.replace('.' and 'https://', '_') + "_enum.txt"
            with open(filename, 'w') as f:
                f.write(result_enum)
            context.bot.send_document(chat_id=chat_id, document=open(filename, 'rb'), filename=filename)
            os.remove(filename)
    
    elif user_input.__contains__('scan'):
        lst = user_input.split()
        print(lst)
        lst.pop()
        print(lst)
        for target in lst:
            update.message.reply_text("Scanning Started For Target " + target)
            result_scan = scan_online.doScan(target, chat_id)
            filename = target.replace('.' and 'https://', '_') + "_scan.txt"
            with open(filename, 'w') as f:
                f.write(result_scan)
            context.bot.send_document(chat_id=chat_id, document=open(filename, 'rb'), filename=filename)
            os.remove(filename)
    
    elif user_input.__contains__('vulac'):
            lst = user_input.split()
            print(lst)
            lst.pop()
            print(lst)
            for target in lst:
                update.message.reply_text("Vulnerability Assesment started for " + target)
                result_vulac = vulac_online.doVulac(target, chat_id)
                filename = target.replace('.' and 'https://', '_') + "_vulac.txt"
                with open(filename, 'w') as f:
                    f.write(result_vulac)
                context.bot.send_document(chat_id=chat_id, document=open(filename, 'rb'), filename=filename)
                os.remove(filename)

def recon(update, context):
    update.message.reply_text("To Perform Reconnaissance enter target followed by word recon. \nFor Example: "
                              "\nhttps://example.com recon\n\nTo Perform Reconnaissance on multiple targets enter targets followed by space.\nFor Example: \nhttps://example.com https://example2.com recon")


def enum(update: Update, context: CallbackContext):
    update.message.reply_text("To Perform Enumeration enter target followed by word enum. \nFor Example: "
                              "\nhttps://example.com enum\n\nTo Perform Enumeration on multiple targets enter targets followed by space.\nFor Example: \nhttps://example.com https://example2.com enum")

def scanning(update: Update, context: CallbackContext):
     update.message.reply_text("To Perform Scanning enter target followed by word scan. \nFor Example: "
                              "\nhttps://example.com scan\n\nTo Perform Scanning on multiple targets enter targets followed by space.\nFor Example: \nhttps://example.com https://example2.com scan")

def vulac(update: Update, context: CallbackContext):
     update.message.reply_text("Vulac")


def spl_tools(update: Update, context: CallbackContext):
    pass


def misc(update: Update, context: CallbackContext):
    pass

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('enum', enum))
updater.dispatcher.add_handler(CommandHandler('menu', menu))
updater.dispatcher.add_handler(CommandHandler('special_tools', spl_tools))
updater.dispatcher.add_handler(CommandHandler('recon', recon))
updater.dispatcher.add_handler(CommandHandler('scan', scanning))
updater.dispatcher.add_handler(CommandHandler('miscellaneous', misc))
updater.dispatcher.add_handler(CommandHandler('vulac', vulac))
updater.dispatcher.add_handler(MessageHandler(Filters.text, reply))

updater.start_polling()
