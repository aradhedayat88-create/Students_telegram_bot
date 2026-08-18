import telebot
import base
import app_db

bot = telebot.TeleBot(base.TOKEN)

print("Bot started!")


@bot.message_handler(commands=['start'])
def say_hello(message):
    # print(message)
    bot.send_message(message.chat.id, "به بات کنترل دانشجویان خوش آمدید")
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("نمایش کل لیست", "پیدا کردن بر اساس شماره آیدی")
    markup.row("پیدا کردن بر اساس کد ملی", "اضافه کردن دانشجو")
    markup.row("حذف دانشجو", "آپدیت اطلاعات دانشجو")
    bot.reply_to(message, text="یکی از گزینه ها را انتخاب کنید:",
                reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def show_message(message):
    if message.text == "نمایش کل لیست":
        msg = app_db.show_list()
        bot.send_message(message.chat.id, str(msg))

    elif message.text == "پیدا کردن بر اساس شماره آیدی":
        msg2 = bot.send_message(
            message.chat.id, "آیدی مورد نظر را وارد کنید: ")
        bot.register_next_step_handler(msg2, find_by_id)

    elif message.text == "پیدا کردن بر اساس کد ملی":
        msg3 = bot.send_message(message.chat.id, "کد ملی خود را وارد کنید: ")
        bot.register_next_step_handler(msg3, find_by_nat_id_num)

    elif message.text == "اضافه کردن دانشجو":
        msg4 = bot.send_message(
            message.chat.id,
            "اطلاعات دانشجو را به این شکل وارد کنید:\n\n"
            "نام,نام خانوادگی,سن,کدملی,دروس,نمره\n\n"
        )
        bot.register_next_step_handler(msg4, add_student)

    elif message.text == "حذف دانشجو":
        msg5 = bot.send_message(
            message.chat.id, "آیدی دانشجویی که میخواهید حذف کنید را وارد کنید: ")
        bot.register_next_step_handler(msg5, remove_student)

    elif message.text == "آپدیت اطلاعات دانشجو":
        msg6 = bot.send_message(
            message.chat.id,
            "اطلاعات را به این شکل وارد کنید:\n\n"
            "آیدی,فیلد,مقدارجدید\n\n"

        )
    bot.register_next_step_handler(msg6, update_student_handler)


# -----------------------------------------------------------
def find_by_id(message):
    student_id = message.text
    result = app_db.show_by_id(student_id)

    if result is None:
        bot.send_message(message.chat.id, "دانشجویی با این آیدی پیدا نشد.")
    else:
        text = (
            f"شناسه: {result.id}\n"
            f"نام: {result.name}\n"
            f"نام خانوادگی: {result.surname}\n"
            f"سن: {result.age}\n"
            f"کد ملی: {result.nat_id_num}\n"
            f"دروس: {result.courses}\n"
            f"نمره: {result.score}"
        )
        bot.send_message(message.chat.id, text)


def find_by_nat_id_num(message):
    student_nat_num = message.text
    result = app_db.show_by_nat_id_num(student_nat_num)

    if result is None:
        bot.send_message(message.chat.id, "دانشجویی با این کد ملی پیدا نشد.")
    else:
        text = (
            f"شناسه: {result.id}\n"
            f"نام: {result.name}\n"
            f"نام خانوادگی: {result.surname}\n"
            f"سن: {result.age}\n"
            f"کد ملی: {result.nat_id_num}\n"
            f"دروس: {result.courses}\n"
            f"نمره: {result.score}"
        )
        bot.send_message(message.chat.id, text)


def add_student(message):
    parts = [p.strip() for p in message.text.split(",")]

    if len(parts) != 6:
        bot.send_message(
            message.chat.id, "❌ تعداد اطلاعات اشتباه است. باید دقیقاً ۶ تا باشد.")
        return

    name = parts[0]
    surname = parts[1]
    age = parts[2]
    nat_id_num = parts[3]
    courses = parts[4]
    score = parts[5]

    student = app_db.add_student(
        name=name,
        surname=surname,
        age=age,
        nat_id_num=nat_id_num,
        courses=courses,
        score=score
    )

    bot.send_message(
        message.chat.id,
        f"✅ دانشجو با موفقیت اضافه شد.\n"
        f"شناسه: {student.id}\n"
        f"نام: {student.name} {student.surname}"
    )


def remove_student(message):
    student_id = message.text
    result = app_db.del_by_id(student_id)

    if result is None:
        bot.send_message(message.chat.id, "دانشجویی با این آیدی پیدا نشد.")
    else:
        bot.send_message(message.chat.id, app_db.show_list())


def update_student_handler(message):
    parts = [p.strip() for p in message.text.split(",")]

    if len(parts) != 3:
        bot.send_message(
            message.chat.id, "❌ فرمت اشتباه است. باید ۳ قسمت باشد.")
        return

    student_id, field, new_value = parts

    result = app_db.update_student(student_id, field, new_value)

    if result is None:
        bot.send_message(message.chat.id, "دانشجویی با این آیدی پیدا نشد.")
    elif result == "invalid_field":
        bot.send_message(message.chat.id, "نام فیلد اشتباه است.")
    else:
        bot.send_message(
            message.chat.id,
            f"✅ با موفقیت آپدیت شد.\n"
            f"شناسه: {result.id}\n"
            f"نام: {result.name} {result.surname}"
        )


if __name__ == '__main__':
    bot.infinity_polling()
