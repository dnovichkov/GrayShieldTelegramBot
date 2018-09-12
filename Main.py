import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai, json
import datetime

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_API_KEY')
APIAI_TOKEN = os.environ.get('APIAI_TOKEN')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

updater = Updater(TELEGRAM_TOKEN)
dispatcher = updater.dispatcher

# Обработка команд
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')

def textMessage(bot, update):
    text = ""
    lower_text = update.message.text.lower()
    parsed_entities = update.message.parse_entities()
    if "КТ!" in update.message.text or "кэтэ" in lower_text:
        text = "Кэтэ - фуэтэ!"
    if "осщ" in lower_text:
        text = "Будь здоров!"
    elif "паф" in lower_text:
        text = "Паф - тиран (бывший)! И могу по секрету сказать, что на клан-сайте есть пачка статей. Только тс-с-с..."
    elif "привет всем" in lower_text or "приветы всем" in lower_text or "утра всем" in lower_text \
            or "всем привет" in lower_text or "всем приветы" in lower_text or "всем утра" in lower_text\
            or "ку" == lower_text or "утра" == lower_text:
        text = "Привет-привет"
    elif "@GrShieldBot" in parsed_entities.values():
        if "что ты умеешь" in lower_text:
            text = 'Мало: говорить "Будь здоров" и вести непринужденную беседу. Но знаю, что Паф - тиран (бывший)! ' \
                   'И могу по секрету сказать, что на клан-сайте есть пачка статей. Только тс-с-с...'
        else:
            request = apiai.ApiAI(APIAI_TOKEN).text_request()  # Токен API к Dialogflow
            request.lang = 'ru'  # На каком языке будет послан запрос
            request.session_id = 'BatlabAIBot'  # ID Сессии диалога (нужно, чтобы потом учить бота)
            request.query = update.message.text  # Посылаем запрос к ИИ с сообщением от юзера
            response_json = json.loads(request.getresponse().read().decode('utf-8'))
            response = response_json['result']['fulfillment']['speech']  # Разбираем JSON и вытаскиваем ответ
            # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
            if response:
                text = response
            else:
                text = 'Я Вас не совсем понял!'
    bot.send_message(chat_id=update.message.chat_id, text=text)

# Хендлеры
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)

# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
# Начинаем поиск обновлений
updater.start_polling(clean=True)
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()
