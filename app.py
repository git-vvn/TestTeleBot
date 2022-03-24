import telebot
import pymorphy2
from cfg import keys, TOKEN
from extensions import APIException, Currencyconverter

bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands = ['start', 'help'])
def help(message: telebot.types.Message):
    msg_txt = 'чтобы начать работу, введите команду боту в следующем формате:\n \
<название валюты> <в какую валюту перевести> <количество $$$>\n  \
Список доступных валют: /values '
    bot.reply_to(message, msg_txt)

@bot.message_handler(commands = ['values'])
def values(message: telebot.types.Message):
    msg_txt = 'Доступные валюты:\n'
    for elem in keys.keys():
        msg_txt = '\n'.join((msg_txt, elem, ))
    bot.reply_to(message, msg_txt)

@bot.message_handler(content_types = ['text',])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        target, src, quantity = values

        total_price = Currencyconverter.convert(target, src, quantity)

    except APIException as err:
        bot.reply_to(message, f'Ошибка пользователя.\n{err}')
    except Exception as err:
        bot.reply_to(message, f'Не удалось обработать команду {err}')
    else:
        target_gent, src_loct = wordhandler(target, src, quantity, total_price)


        text = f'Цена {quantity} {target_gent} в {src_loct} составляет {str(total_price)}'
        #text = str(courses)
        bot.send_message(message.chat.id, text)

def wordhandler(target, src, quantity,total_price):
    morph = pymorphy2.MorphAnalyzer()
    changed_word_trg = morph.parse(target)[0]
    changed_word_src = morph.parse(src)[0]
    if float(quantity) > 1:
        target_gent = changed_word_trg.inflect({'plur', 'gent'}).word
    else:
        target_gent = changed_word_trg.inflect({'sing', 'gent'}).word
    if total_price > 1:
        src_loct = changed_word_src.inflect({'plur', 'loct'}).word
    else:
        src_loct = changed_word_src.inflect({'sing', 'loct'}).word
    return target_gent, src_loct

bot.polling()

