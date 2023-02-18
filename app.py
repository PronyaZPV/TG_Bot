import telebot
from config import keys, TOKEN
from extensions import APIException, ConverterClass, Ending


bot = telebot.TeleBot(TOKEN)


# def input_values(message):
#     values = message.text.split(' ')
#     if len(values) > 3:
#         raise APIException('Слишком много параметров')
#     elif len(values) == 2:
#         values.append('1')
#     elif len(values) < 2:
#         raise APIException('Слишком мало параметров')
#     return values


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести>\nТретим аргументом можно указать <количество переводимой валюты> \
\nНапример "доллар рубль 125"\nУвидеть список всех валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def converter(message: telebot.types.Message):
    try:
        # input_values(message)
        values = message.text.split(' ')
        if len(values) > 3:
            raise APIException('Слишком много параметров')
        elif len(values) == 2:
            values.append('1')
        elif len(values) < 2:
            raise APIException('Слишком мало параметров')
        quote, base, amount = values
        total_base = ConverterClass.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        quote = Ending.quote_end(quote, amount)
        base = Ending.base_end(base, amount)

        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()