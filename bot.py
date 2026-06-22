import telebot
from telebot import types
import csv
from datetime import datetime

TOKEN = "8858237214:AAFR9q9NrBlnvk9iVmw_lKj5ozqEdrc2cXE"
ADMIN_ID = 1902991988

WHATSAPP = "https://wa.me/77773967698"
INSTAGRAM = "https://instagram.com/studiofirst90_almaty"

bot = telebot.TeleBot(TOKEN)
user_data = {}

def save_lead(name, age, group, studio, phone):
    with open("leads.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow([
            datetime.now().strftime("%d.%m.%Y %H:%M"),
            name, age, group, studio, phone
        ])

@bot.message_handler(commands=["start"])
def start(message):

    markup = types.InlineKeyboardMarkup(row_width=2)

    markup.add(
        types.InlineKeyboardButton("🎁 Пробное занятие", callback_data="trial")
    )

    markup.row(
        types.InlineKeyboardButton("📅 Расписание", callback_data="schedule"),
        types.InlineKeyboardButton("💰 Стоимость", callback_data="price")
    )

    markup.row(
        types.InlineKeyboardButton("📍 Филиалы", callback_data="branches"),
        types.InlineKeyboardButton("📞 Контакты", callback_data="contacts")
    )

    markup.row(
        types.InlineKeyboardButton("💬 WhatsApp", url=WHATSAPP),
        types.InlineKeyboardButton("📸 Instagram", url=INSTAGRAM)
    )

    bot.send_message(
        message.chat.id,
        "💃 Добро пожаловать в студию танцев First!\n\n"
        "✨ Первое пробное занятие бесплатно\n\n"
        "🏆 Дети и взрослые\n"
        "🏫 2 филиала в Алматы\n\n"
        "Выберите действие 👇",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    chat_id = call.message.chat.id

    if call.data == "trial":

        user_data[chat_id] = {}

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("👧 4-8 лет", callback_data="age_child"))
        markup.add(types.InlineKeyboardButton("🕺 9+ лет и взрослые", callback_data="age_adult"))

        bot.send_message(
            chat_id,
            "Выберите возрастную группу:",
            reply_markup=markup
        )

    elif call.data == "age_child":

        user_data[chat_id]["group"] = "👧 Детская группа (4-8 лет)"

        show_branches(chat_id)

    elif call.data == "age_adult":

        user_data[chat_id]["group"] = "🕺 Старшие дети и взрослые"

        show_branches(chat_id)

    elif call.data == "schedule":

        bot.send_message(
            chat_id,
            "🗓️ РАСПИСАНИЕ\n\n"
            "📍 Боткина 20\n"
            "👧 Детская группа\n"
            "Вт, Чт — 18:30-20:00\n\n"
            "🕺 Старшие дети и взрослые\n"
            "Вт, Чт — 20:00-21:30\n\n"
            "📍 Потанина 226 (Школа №102)\n"
            "👨‍👩‍👧 Общая группа\n"
            "Пн, Ср, Пт — 19:30-20:30"
        )

    elif call.data == "price":

        bot.send_message(
            chat_id,
            "💰 СТОИМОСТЬ\n\n"
            "27 000 ₸ в месяц\n\n"
            "🎁 Первое пробное занятие бесплатно"
        )

    elif call.data == "branches":

        bot.send_message(
            chat_id,
            "📍 НАШИ ФИЛИАЛЫ\n\n"
            "🏫 Потанина 226 (Школа №102)\n"
            "🏫 Боткина 20"
        )

    elif call.data == "contacts":

        bot.send_message(
            chat_id,
            "📞 +7 777 396 76 98\n\n"
            "💬 WhatsApp:\n" + WHATSAPP
        )

    elif call.data == "studio_potanina":

        user_data[chat_id]["studio"] = "Потанина 226"

        request_phone(
            chat_id,
            "🎉 Отличный выбор!\n\n"
            "📍 Потанина 226 (Школа №102)\n\n"
            "📅 Пн, Ср, Пт\n"
            "⏰ 19:30 - 20:30\n\n"
            "💰 27 000 ₸\n"
            "🎁 Первое занятие бесплатно\n\n"
            "📱 Отправьте номер телефона родителя."
        )

    elif call.data == "studio_botkina":

        user_data[chat_id]["studio"] = "Боткина 20"

        group = user_data[chat_id]["group"]

        if "Детская" in group:
            text = (
                "🎉 Отличный выбор!\n\n"
                "📍 Боткина 20\n\n"
                "👧 Детская группа\n"
                "📅 Вт, Чт\n"
                "⏰ 18:30 - 20:00\n\n"
                "💰 27 000 ₸\n"
                "🎁 Первое занятие бесплатно\n\n"
                "📱 Отправьте номер телефона родителя."
            )
        else:
            text = (
                "🎉 Отличный выбор!\n\n"
                "📍 Боткина 20\n\n"
                "🕺 Старшие дети и взрослые\n"
                "📅 Вт, Чт\n"
                "⏰ 20:00 - 21:30\n\n"
                "💰 27 000 ₸\n"
                "🎁 Первое занятие бесплатно\n\n"
                "📱 Отправьте номер телефона родителя."
            )

        request_phone(chat_id, text)

def show_branches(chat_id):

    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton("🏫 Потанина 226", callback_data="studio_potanina")
    )

    markup.add(
        types.InlineKeyboardButton("🏫 Боткина 20", callback_data="studio_botkina")
    )

    bot.send_message(
        chat_id,
        "Выберите филиал 👇",
        reply_markup=markup
    )

def request_phone(chat_id, text):

    phone_markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

    phone_markup.add(
        types.KeyboardButton(
            "📱 Отправить телефон",
            request_contact=True
        )
    )

    bot.send_message(
        chat_id,
        text,
        reply_markup=phone_markup
    )

@bot.message_handler(content_types=["contact"])
def contact_handler(message):

    chat_id = message.chat.id

    phone = message.contact.phone_number

    group = user_data[chat_id]["group"]
    studio = user_data[chat_id]["studio"]

    save_lead(
        "Заявка из Telegram",
        "-",
        group,
        studio,
        phone
    )

    bot.send_message(
        ADMIN_ID,
        f"🔔 Новая заявка\n\n"
        f"Группа: {group}\n"
        f"Филиал: {studio}\n"
        f"Телефон: {phone}"
    )

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "💬 Написать в WhatsApp",
            url=WHATSAPP
        )
    )

    bot.send_message(
        chat_id,
        "✅ Заявка успешно отправлена!\n\n"
        "Спасибо за интерес к студии танцев First 💃\n\n"
        "Наш администратор свяжется с вами в ближайшее время.",
        reply_markup=markup
    )

    user_data.pop(chat_id, None)

bot.infinity_polling(skip_pending=True)
