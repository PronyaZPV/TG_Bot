import telebot
from config import keys, TOKEN, logo
from extensions import APIException, ConverterClass, Ending, input_values

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def help(message: telebot.types.Message):
    text = f'Приветствую, {message.chat.first_name}!\n\n' \
           f'Я умею пересчитывать валюту в другой валюте по актуальному биржевому курсу.\n\n' \
           f'Увидеть список всех валют: /values\nКак пользоваться: /help'
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = '\U00002705 Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести>\nТретим аргументом можно указать <количество переводимой валюты> \
\n\n\U00002705 Например "доллар рубль 125"\n\n\U00002705 Увидеть список всех валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = '\U00002705 Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key + ' ' + logo[key]))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def converter(message: telebot.types.Message):
    try:
        values = input_values(message)
        quote, base, amount = values
        total_base = str(ConverterClass.get_price(quote, base, amount)).rstrip('0').rstrip('.')
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        quote = Ending.quote_end(quote, amount)
        base = Ending.base_end(base, amount)

        text = f'\U00002705 Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
