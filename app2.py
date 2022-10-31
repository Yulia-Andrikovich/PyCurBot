import telebot

from config import keys, TOKEN

from extensions import APIExclusions, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def help(message: telebot.types.Message):
    text = 'Enter the command in the following format (comma separated):' \
           ' \n- <Name of the currency you want to convert>  \n- <Name of the currency to which you want to convert ' \
           'the price of the first currency> \n- <Quantity of first currency in digits>\n \
 List of available currencies: /types_of_currencies'

    bot.reply_to(message, text)


@bot.message_handler(commands=['types_of_currencies'])
def values(message: telebot.types.Message):
    text = 'Available currencies:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)



@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        types_of_currencies = message.text.split(',')

        if len(types_of_currencies) < 3:
            raise APIExclusions('You entered less than 3 parameters')
        if len(types_of_currencies) > 3:
            raise APIExclusions('You entered more than 3 parameters')


        base, quote, amount = types_of_currencies
        total_base = CurrencyConverter.get_price(base, quote, amount)
    except APIExclusions as e:
        bot.reply_to(message, f'Error on the client side:( \n{e}')

    except Exception as e:
        bot.reply_to(message, f'The command could not be processed\n{e}')
    else:
        text = f'Price {amount} {base} in {quote}: {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)