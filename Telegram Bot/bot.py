import telebot
import requests
import random
from keyboa import keyboa_maker
from telebot import types


def get_random_stiker():
    try:
        page = random.randint(1, 300)
        page_url = 'https://tlgrm.ru/stickers?page=' + str(page)
        stikerpack = random.randint(1, 12)
        r = requests.get(page_url)
        url_to_pack = r.text.split('class="stickerbox" href="')[stikerpack].split('"')[0]
        r = requests.get(url_to_pack)
        all_pictures = r.text.split('.webp 192w,\n')
        stiker_index = random.randint(1, len(all_pictures) - 1)
        stiker_url = all_pictures[stiker_index].strip().split(' 256w,')[0]
        return stiker_url
    except:
        return get_random_stiker()


token = '1812787265:AAH8l9r3apEuQ2gZYtONVGzBsnv7nCB6voA'  # Bot username: olegpash_profile_bot
bot = telebot.TeleBot(token)


@bot.message_handler()
def initialize(message):
    print(message)
    if message.text == '/start':
        answer = f'Привет, {message.chat.first_name} {message.chat.last_name}!\n\nЭтот бот создан для ' \
                 f'портфолио пользователя olegpash! В нем продемонстрирована вся функциональность' \
                 f' какую только может предоставить библиотека PyTelegramBot.\nБот написан на языке программирования' \
                 f' Python.\n\nПриятного использования!'
        bot.send_message(message.chat.id, answer)
        file_id = 'https://cdn.tlgrm.ru/stickers/dc7/a36/dc7a3659-1457-4506-9294-0d28f529bb0a/256/1.webp'
        bot.send_sticker(message.chat.id, file_id)
        bot.send_message(message.chat.id, 'Для продолжения нажмите на кнопку "/" и выберите одну из команд.')
    elif message.text == '/help':
        bot.send_message(message.chat.id, "Ну что тут непонятного. Жми на '/' и нажимай на команду.")
        file_id = 'https://cdn.tlgrm.ru/stickers/d57/6d1/d576d1b3-d2b5-40de-8c91-f254307bf4be/256/1.webp'
        bot.send_sticker(message.chat.id, file_id)
    elif message.text == '/stiker':
        file_id = get_random_stiker()
        bot.send_sticker(message.chat.id, file_id)
    elif message.text == '/reply':
        bot.reply_to(message, 'Умею ли я отвечать на сообщение?\nКонечно. Я и не такое могу!')
    elif message.text == '/video':
        video = open('small.mp4', 'rb')
        bot.send_video(message.chat.id, video)
    elif message.text == '/audio':
        voice = open('audio.ogg', 'rb')
        bot.send_voice(message.chat.id, voice)
    elif message.text == '/button1':
        fruits = [
            ["banana", "coconut"], ["orange", "peach", "apricot"], ["apple", "pineapple"], "avocado", "melon"]
        kb_fruits = keyboa_maker(items=fruits, copy_text_to_callback=True)
        bot.send_message(message.chat.id, "Привет!", reply_markup=kb_fruits)
    elif message.text == '/button2':
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
        button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
        button1 = types.KeyboardButton('Обычная кнопка')
        keyboard.add(button_phone, button_geo, button1)
        bot.send_message(message.chat.id, "Hello!", reply_markup=keyboard)
    elif message.text == '/payment':
        bot.send_message(message.chat.id, 'Для оплаты используйте данные тестовой карты: 1111 1111 1111 1026, 12/22,'
                                          ' CVC 000.')
        bot.send_invoice(
            chat_id=message.chat.id,
            title='Пополнение счета',
            description='Описание',
            invoice_payload='true',
            provider_token='381764678:TEST:25398',
            start_parameter='true',
            currency='RUB',
            prices=[types.LabeledPrice(label='Продукт №1', amount=10000)]
        )
    else:
        bot.send_message(message.chat.id, "Я тебя не понимать.")


@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


bot.polling()
