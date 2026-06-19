import telebot
from telebot import types

TOKEN = "8858237214:AAFR9q9NrBlnvk9iVmw_lKj5ozqEdrc2cXE"
ADMIN_ID = 1902991988

bot = telebot.TeleBot(TOKEN)

user_data = {}


@bot.message_handler(commands=['start'])
def start(message):

    markup = types.InlineKeyboardMarkup(row_width=2)

    btn1 = types.InlineKeyboardButton(
        "🎁 Пробное занятие",
        callback_data="register"
    )

    btn2 = types.InlineKeyboardButton(
        "📅 Расписание",
        callback_data="schedule"
    )

    btn3 = types.InlineKeyboardButton(
        "💰 Стоимость",
        callback_data="price"
    )

    btn4 = types.InlineKeyboardButton(
        "📍 Филиалы",
        callback_data="address"
    )

    btn5 = types.InlineKeyboardButton(
        "📞 Контакты",
        callback_data="contacts"
    )

    btn6 = types.InlineKeyboardButton(
        "💬 WhatsApp",
        callback_data="whatsapp"
    )
    btn7 = types.InlineKeyboardButton(
    "📸 Instagram",
    url="https://instagram.com/studiofirst90_almaty"
    )
    markup.add(btn1)
    markup.row(btn2, btn3)
    markup.row(btn4, btn5)
    markup.row(btn6, btn7)

    bot.send_message(
        message.chat.id,
        "💃 Добро пожаловать в студию танцев First!\n\n"
        "✨ Первое пробное занятие бесплатно\n\n"
        "Выберите действие:",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    chat_id = call.message.chat.id

    if call.data == "register":

        user_data[chat_id] = {"step": "name"}

        bot.send_message(
            chat_id,
            "Введите имя ребенка"
        )

    elif call.data == "contacts":

        bot.send_message(
            chat_id,
            "📞 Телефон:\n+7 777 396 76 98"
        )

    elif call.data == "address":

        bot.send_message(
            chat_id,
            "📍 Наши филиалы:\n\n"
            "🏫 Потанина 226\n"
            "🏫 Боткина 20"
        )

    elif call.data == "schedule":

     bot.send_message(
        chat_id,
        "🗓️ Расписание занятий\n\n"

        "📍 Боткина, 20\n"
        "👧 Детская группа\n"
        "Вторник, четверг — 18:30-20:00\n\n"

        "🕺 Старшие дети и взрослые\n"
        "Вторник, четверг — 20:00-21:30\n\n"

        "📍 Потанина, 226 (школа №102)\n"
        "👨‍👩‍👧 Общая группа\n"
        "Понедельник, среда, пятница — 19:30-20:30"
    )

    elif call.data == "price":

     bot.send_message(
        chat_id,
        "💰 Стоимость:\n\n"
        "🏫 Потанина 226\n"
        "12 занятий по 1 часу — 27 000 ₸\n\n"
        "🏫 Боткина 20\n"
        "8 занятий по 1.5 часа — 27 000 ₸\n\n"
        "🎁 Первое пробное занятие бесплатно"
    )

    elif call.data == "whatsapp":

        markup = types.InlineKeyboardMarkup()

        btn = types.InlineKeyboardButton(
            "📲 Написать в WhatsApp",
            url="https://wa.me/77773967698"
        )

        markup.add(btn)

        bot.send_message(
            chat_id,
            "Связаться с администратором:",
            reply_markup=markup
        )

    elif call.data == "studio1":

        user_data[chat_id]["studio"] = "Потанина 226"

        phone_markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
        )

        phone_btn = types.KeyboardButton(
            "📱 Отправить телефон",
            request_contact=True
        )

        phone_markup.add(phone_btn)

        bot.send_message(
            chat_id,
            "Отправьте номер телефона родителя",
            reply_markup=phone_markup
        )

    elif call.data == "studio2":

        user_data[chat_id]["studio"] = "Боткина 20"

        phone_markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
        )

        phone_btn = types.KeyboardButton(
            "📱 Отправить телефон",
            request_contact=True
        )

        phone_markup.add(phone_btn)

        bot.send_message(
            chat_id,
            "Отправьте номер телефона родителя",
            reply_markup=phone_markup
        )


@bot.message_handler(content_types=['contact'])
def contact_handler(message):

    chat_id = message.chat.id

    if chat_id not in user_data:
        return

    phone = message.contact.phone_number

    name = user_data[chat_id]["name"]
    age = user_data[chat_id]["age"]
    studio = user_data[chat_id]["studio"]

    bot.send_message(
    ADMIN_ID,
    f"🔔 Новая заявка на пробное занятие\n\n"
    f"Имя: {name}\n"
    f"Возраст: {age}\n"
    f"Группа: {'🧒 Детская группа (4-8 лет)' if 4 <= age <= 8 else '🧑 Старшая группа'}\n"
    f"Филиал: {studio}\n"
    f"Телефон: {phone}"
    )

    markup = types.InlineKeyboardMarkup()

    wa_btn = types.InlineKeyboardButton(
        "💬 Написать в WhatsApp",
        url="https://wa.me/77773967698"
    )

    markup.add(wa_btn)

    bot.send_message(
        chat_id,
        "✅ Спасибо!\n\n"
        "Заявка отправлена.\n"
        "Наш администратор скоро свяжется с вами.",
        reply_markup=markup
    )

    del user_data[chat_id]


@bot.message_handler(func=lambda message: True)
def answer(message):

    chat_id = message.chat.id

    if chat_id not in user_data:
        return

    step = user_data[chat_id]["step"]

    if step == "name":

        user_data[chat_id]["name"] = message.text
        user_data[chat_id]["step"] = "age"

        bot.send_message(
            chat_id,
            "Введите возраст ребенка"
        )

    elif step == "age":

        if not message.text.isdigit():

            bot.send_message(
                chat_id,
                "Введите возраст цифрами"
            )
            return

        age = int(message.text)
    if 4 <= age <= 8:
     group = "👶 Детская группа (4–8 лет)"
    else:
     group = "🧑 Старшая группа"
     user_data[chat_id]["age"] = age

     markup = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton(
            "🏫 Потанина 226",
            callback_data="studio1"
        )

    btn2 = types.InlineKeyboardButton(
            "🏫 Боткина 20",
            callback_data="studio2"
        )

    markup.add(btn1)
    markup.add(btn2)

    bot.send_message(
            chat_id,
            "🎉 Отлично!\n\n"
            "Выберите филиал:",
            reply_markup=markup
        )


bot.infinity_polling()