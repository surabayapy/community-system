from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    uname = update['message']['chat']['username']
    response = requests.get('http://surabayapy.pythonanywhere.com/api/kegiatan/%s/' % (uname))
    data = response.json()
    if data['data'] == 'Not found':
        update.message.reply_text('Halo, sepertinya kamu belom mendaftar di http://surabayapy.pythonanywhere.com')
    else:
        update.message.reply_text('Hi %s!' % (uname))


def kegiatan(bot, update):
    response = requests.get('http://surabayapy.pythonanywhere.com/api/daftar-kegiatan/')
    data = response.json()
    for i in data['data']:
        update.message.reply_text('Meetup %s: %s' % (i['id'],i['tema']))

def ikut(bot, update):
    response = requests.get('http://surabayapy.pythonanywhere.com/api/daftar-kegiatan/')
    data = response.json()
    reply_keyboard = []
    for i in data['data']:
        reply_keyboard.append(i['tema'])

    reply_keyboard = [reply_keyboard]
    update.message.reply_text(
        'Kegiatan mana yang mau kamu ikuti?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

def terdaftar(bot, update):
    uname = update['message']['chat']['username']
    response = requests.get('http://surabayapy.pythonanywhere.com/api/kegiatan/%s/' % (uname))
    data = response.json()
    print(data)
    for i in data['data']:
        update.message.reply_text('Meetup %s: %s' % (i['id'],i['tema']))

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("359141565:AAEM6w-y_oYgwXiiZbk4oO-3TQbKjyaYvlA")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("kegiatan", kegiatan))
    dp.add_handler(CommandHandler("ikut", ikut))
    dp.add_handler(CommandHandler("terdaftar", terdaftar))


    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()