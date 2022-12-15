from CalculatedData import CalculatedData
import telebot
# from telebot import types

def data_output(full_calculations = False):
    calculatedData = CalculatedData()
    final_text = calculatedData.exchange_rate_calculation(full_calculations, True)
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
    # Добавляем кнопки
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("Курсы")
    item2 = telebot.types.KeyboardButton("Курс Узбекистана")
    item3 = telebot.types.KeyboardButton("Расчеты")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    bot.send_message(message.chat.id, 'Выбери действие: '
                                      '\n- Курсы: для вывода текущих курсов'
                                      '\n- Курс Узбекистана: для расчета курса вывода через Тинькофф в Узбекистан'
                                      '\n- Расчеты: вывод подробных расчетов',  reply_markup=markup)

# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.strip() == 'Курсы' :
        bot.send_message(message.chat.id, data_output(), parse_mode='HTML')
    elif message.text.strip() == 'Курс Узбекистана':
        bot.send_message(message.chat.id, "Напишите курс rub-uzs в Тинькофе для отправки в Узбекистан (разделитель точка)", parse_mode='HTML')
    elif message.text.strip() == 'Расчеты':
        bot.send_message(message.chat.id, data_output(True), parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, data_output_uzb(float(message.text)), parse_mode='HTML')


# Запускаем бота
bot.polling(none_stop=True, interval=0)