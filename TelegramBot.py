from CalculatedData import CalculatedData
import telebot
from telebot import types

def data_output():
    calculatedData = CalculatedData()
    result_courses = calculatedData.exchange_rate_calculation()
    final_text = calculatedData.composing_message(result_courses, True)
    return final_text

def data_output_uzb(course):
    calculatedData = CalculatedData()
    final_text = calculatedData.exchange_rate_calculation_uzb(course)
    return final_text

# Создаем экземпляр бота
bot = telebot.TeleBot('5283971555:AAG9Yq3kQ5dNriD04o7UtuMUphMABCrR8Ao')
# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(message, res=False):
    # Добавляем две кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Курсы")
    item2 = types.KeyboardButton("Курс Узбекистана")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(message.chat.id, 'Нажми: \nКурсы - для вывода текущих курсов\nКурс Узбекистана — для расчета курса вывода через Тинькофф в Узбекистан',  reply_markup=markup)

# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.strip() == 'Курсы' :
        bot.send_message(message.chat.id, data_output(), parse_mode='Markdown')
    elif message.text.strip() == 'Курс Узбекистана':
        bot.send_message(message.chat.id, "Напишите курс rub-usd в Тинькофе для отправки в Узбекистан (разделитель точка)", parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, data_output_uzb(float(message.text)), parse_mode='Markdown')


# Запускаем бота
bot.polling(none_stop=True, interval=0)