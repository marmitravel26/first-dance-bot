import telebot
from telebot import types
import csv
from datetime import datetime

TOKEN = "8858237214:AAFR9q9NrBlnvk9iVmw_lKj5ozqEdrc2cXE"
ADMIN_ID = 1902991988

bot = telebot.TeleBot(TOKEN)
user_data = {}

WHATSAPP = "https://wa.me/77773967698"
INSTAGRAM = "https://instagram.com/studiofirst90_almaty"

def save_lead(name, age, group, studio, phone):
    with open("leads.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow([
            datetime.now().strftime("%d.%m.%Y %H:%M"),
            name, age, group, studio, phone
        ])

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)

    markup.add(types.InlineKeyboardButton("🎁 Пробное занятие", callback_data="trial"))
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
        "🏫 2 филиала в Алматы",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    chat_id = call.message.chat.id

    if call.data == "trial":
        user_data[chat_id] = {"step": "name"}
        bot.send_message(chat_id, "👶 Введите имя ребёнка:")
        return
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
            "Пн, Ср, Пт — 19:30-20:30"
        )

    elif call.data == "price":
        bot.send_message(chat_id, "💰 Стоимость обучения\n\n27 000 ₸\n\n🎁 Первое занятие бесплатно")

    elif call.data == "branches":
        bot.send_message(chat_id, "🏫 Потанина 226 (Школа №102)\n🏫 Боткина 20")

    elif call.data == "contacts":
        bot.send_message(chat_id, "📞 +7 777 396 76 98")

    elif call.data == "studio1":
        user_data[chat_id]["studio"] = "Потанина 226"
        ask_phone(chat_id,
                   "🎉 Отличный выбор!\n\n📍 Потанина 226\n📅 Пн, Ср, Пт\n⏰ 19:30-20:30\n\n💰 27 000 ₸\n🎁 Первое занятие бесплатно\n\n📱 Отправьте телефон родителя")

    elif call.data == "studio2":
        user_data[chat_id]["studio"] = "Боткина 20"

        if "Детская" in user_data[chat_id]["group"]:
            text = ("🎉 Отличный выбор!\n\n📍 Боткина 20\n\n👧 Детская группа\n"
                    "📅 Вт, Чт\n⏰ 18:30-20:00\n\n💰 27 000 ₸\n🎁 Первое занятие бесплатно\n\n📱 Отправьте телефон родителя")
        else:
            text = ("🎉 Отличный выбор!\n\n📍 Боткина 20\n\n🕺 Старшие дети и взрослые\n"
                    "📅 Вт, Чт\n⏰ 20:00-21:30\n\n💰 27 000 ₸\n🎁 Первое занятие бесплатно\n\n📱 Отправьте телефон родителя")

        ask_phone(chat_id, text)

def ask_phone(chat_id, text):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("📱 Отправить телефон", request_contact=True))
    bot.send_message(chat_id, text, reply_markup=markup)

@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    chat_id = message.chat.id

    if chat_id not in user_data:
        return

    phone = message.contact.phone_number
    data = user_data[chat_id]

    save_lead(
        data["name"],
        data["age"],
        data["group"],
        data["studio"],
        phone
    )

    bot.send_message(
        ADMIN_ID,
        f"🔔 Новая заявка\n\n"
        f"👶 Имя: {data['name']}\n"
        f"🎂 Возраст: {data['age']}\n"
        f"🏆 Группа: {data['group']}\n"
        f"📍 Филиал: {data['studio']}\n"
        f"📱 Телефон: {phone}"
    )

    bot.send_message(
        chat_id,
        "✅ Заявка успешно отправлена!\n\n"
        "Наш администратор скоро свяжется с вами."
    )

    del user_data[chat_id]

@bot.message_handler(func=lambda m: True)
def messages(message):
    chat_id = message.chat.id

    if chat_id not in user_data:
        return

    step = user_data[chat_id]["step"]

    if step == "name":
        user_data[chat_id]["name"] = message.text
        user_data[chat_id]["step"] = "age"
        bot.send_message(chat_id, "🎂 Введите возраст ребёнка:")
        return

    if step == "age":
        if not message.text.isdigit():
            bot.send_message(chat_id, "Введите возраст цифрами")
            return

        age = int(message.text)

        user_data[chat_id]["age"] = age

        if 4 <= age <= 8:
            user_data[chat_id]["group"] = "👧 Детская группа"
        else:
            user_data[chat_id]["group"] = "🕺 Старшие дети и взрослые"

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🏫 Потанина 226", callback_data="studio1"))
        markup.add(types.InlineKeyboardButton("🏫 Боткина 20", callback_data="studio2"))

        bot.send_message(chat_id, "📍 Выберите филиал 👇", reply_markup=markup)

bot.infinity_polling(skip_pending=True)

