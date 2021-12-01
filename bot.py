from random import randrange
from khayyam import JalaliDatetime

import telebot
from telebot import types
from gtts import gTTS
import qrcode

token = '2121727921:AAHWyZaFY615YmIKtvcG3t6MDBvUkk1GHZ8'

bot = telebot.TeleBot(token, parse_mode=None)

markup = types.ReplyKeyboardMarkup()
new_game = types.KeyboardButton('/game')
markup.add(new_game)

number_to_guess = -1


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f' خوش آمدی{message.chat.first_name}')


@bot.message_handler(commands=['voice'])
def voice(message):
    msg = bot.reply_to(message, "متن خود را به انگیلیسی وارد کنید")
    bot.register_next_step_handler(msg, get_voice_file)


def get_voice_file(message):
    chat_id = message.chat.id
    try:
        text = message.text
        chat_id = message.chat.id
        language = 'en'

        obj = gTTS(text=text, lang=language, slow=False)
        obj.save('voice.mp3')
        bot.send_audio(chat_id, open('voice.mp3', 'rb'))
    except Exception as e:
        bot.send_message(chat_id, 'خطایی بوجود آمد، بار دیگر دستور را وارد کنید!')


@bot.message_handler(commands=['qrcode'])
def qrcode_command(message):
    msg = bot.reply_to(message, "متن خود را وارد کنید")
    bot.register_next_step_handler(msg, get_qrcode_pic)


def get_qrcode_pic(message):
    chat_id = message.chat.id
    try:
        text = message.text

        img = qrcode.make(text)
        img.save('qr.png')
        bot.send_photo(chat_id, open('qr.png', 'rb'))
    except Exception as e:
        bot.send_message(chat_id, 'خطایی بوجود آمد، بار دیگر دستور را وارد کنید!')


@bot.message_handler(commands=['age'])
def age_command(message):
    msg = bot.reply_to(message, "تاریخ تولد شمسی خود را به فرمت 'YYYY-MM-DD' وارد کنید")
    bot.register_next_step_handler(msg, convert_date)


def convert_date(message):
    chat_id = message.chat.id
    try:
        text = message.text

        year, month, day = text.split('-')
        age = JalaliDatetime.now().year - JalaliDatetime(year, month, day).year
        bot.send_message(chat_id, str(age))
    except Exception as e:
        bot.send_message(chat_id, 'خطایی بوجود آمد، بار دیگر دستور را وارد کنید!')


@bot.message_handler(commands=['game'])
def game(message):
    global number_to_guess
    chat_id = message.chat.id
    number_to_guess = randrange(1, 11)

    bot.send_message(chat_id, "شروع کنید به حدس زدن", reply_markup=markup)


@bot.message_handler(commands=['max'])
def max_command(message):
    msg = bot.reply_to(message, "آرایه را به فرمت [x,x,x,x] بدون براکت وارد کنید")
    bot.register_next_step_handler(msg, print_max)


def print_max(message):
    chat_id = message.chat.id
    try:
        text = message.text

        array = [int(x) for x in text.split(',')]
        bot.send_message(chat_id, 'ماکسیمم آرایه عدد زیر است')
        bot.send_message(chat_id, str(max(array)))
    except Exception as e:
        bot.send_message(chat_id, 'خطایی بوجود آمد، بار دیگر دستور را وارد کنید!')


@bot.message_handler(commands=['argmax'])
def argmax_command(message):
    msg = bot.reply_to(message, "آرایه را به فرمت [x,x,x,x] بدون براکت وارد کنید")
    bot.register_next_step_handler(msg, print_argmax)


def print_argmax(message):
    chat_id = message.chat.id
    try:
        text = message.text

        array = [int(x) for x in text.split(',')]
        bot.send_message(chat_id, 'اندیس ماکسیمم آرایه عدد زیر است')
        bot.send_message(chat_id, str(array.index(max(array))))
    except Exception as e:
        bot.send_message(chat_id, 'خطایی بوجود آمد، بار دیگر دستور را وارد کنید!')


@bot.message_handler(commands=['help'])
def help_command(message):
    out = "/start"
    out += "\n"
    out += "با نام کاربر، خوش آمدید چاپ کند. مثلا (sajjad خوش آمدی)"
    out += "\n"
    out += "/game"
    out += "\n"
    out += "بازی حدس عدد اجرا شود. کاربر یک عدد حدس میزند و بات راهنمایی می‌کند (برو بالا، برو پایین، برنده شدی) - در هنگام بازی، یک دکمه new game در پایین بات مشاهده شود."
    out += "\n"
    out += "/age"
    out += "\n"
    out += "تاریخ تولد را به صورت هجری شمسی دریافت نماید و سن را محاسبه نماید. (برای راهنمایی به آدرس اینستاگرامی pylearn@ مراجعه نمایید)"
    out += "\n"
    out += "/voice"
    out += "\n"
    out += "یک جمله به انگلیسی از کاربر دریافت نماید و آن را به صورت voice ارسال نماید. (برای راهنمایی به آدرس اینستاگرامی pylearn@ مراجعه نمایید)"
    out += "\n"
    out += "/max"
    out += "\n"
    out += "یک آرایه به صورت 14,7,78,15,8,19,20 از کاربر دریافت نماید و بزرگترین مقدار را چاپ نماید."
    out += "\n"
    out += "/argmax"
    out += "\n"
    out += "یک آرایه به صورت 14,7,78,15,8,19,20 از کاربر دریافت نماید و اندیس بزرگترین مقدار را چاپ نماید."
    out += "\n"
    out += "/qrcode"
    out += "\n"
    out += "یک رشته از کاربر دریافت نماید و qrcode آن را تولید نماید."

    bot.reply_to(message, out)


@bot.message_handler(content_types=['text'])
def play_game(message):
    global number_to_guess
    if number_to_guess > 0:
        chat_id = message.chat.id
        text = message.text
        value = int(text)

        if value < number_to_guess:
            bot.send_message(chat_id, 'برو بالا!', reply_markup=markup)
        elif value > number_to_guess:
            bot.send_message(chat_id, 'برو پایین!', reply_markup=markup)

        if value == number_to_guess:
            bot.send_message(chat_id, 'شما برنده شدید!!!', reply_markup=markup)
            number_to_guess = -1


bot.infinity_polling()
