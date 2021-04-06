from loader import dp, bot
from aiogram.dispatcher.filters import Command
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions, Message, CallbackQuery
from keyboards.inline.choice_buttons import *
from keyboards.reply.choice_buttons import *
from utils import TestStates
from data import db
from config import ADMIN
from data.db import *



@dp.message_handler(Command('start'))  # Начало начал
async def start_command(message):
    db.user_create(message.chat.id)
    # Создание открытой анкеты
    print(message)
    await bot.send_message(  
        message.chat.id,
                "Здравствуй, Повелитель 👑,\n" +
                "Я бот, созданный для свинг знакомств \n" +
                "Убедительная просьба установить себе в телеграм username, иначе будут работать не все функции",
        reply_markup=menu() 
                    )
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(TestStates.all()[3])
    await message.answer("Выберите, пара МЖ, М или Ж?", reply_markup=gender_btns())


@dp.message_handler(Command('send'))  # Начало начал
async def send(message):
    if message.chat.id == ADMIN:
        s = message.text
        send, location, *lst = map(str, s.split("\n"))
        came = 0
        try:
            text = "\n".join(lst)
        except:
            pass
        users = get_users(location)
        notcame = 0
        for user in users:
            try:
                await bot.send_message(user, text, reply_markup=menu())
                came += 1
            except:
                notcame += 1
            s = "Данная рассылка дошла до " + str(came) + " пользователей\nНедошла до " + str(notcame) + " пользователей"
        await bot.send_message(ADMIN, s)

@dp.callback_query_handler(lambda call: call.data == "Home")
async def home(call: CallbackQuery):
    await call.message.answer("Вы в главном меню", reply_markup=menu())


@dp.callback_query_handler(lambda call: "message_id" in call.data and "user_id" in call.data and "answer" in call.data)
async def mark_up(call: CallbackQuery):
    print("1")
    s1, s2 = map(str, call.data.split("|"))
    print(2)
    s, partner_id = map(str, s1.split(":"))
    print(3)
    s, message_id = map(str, s2.split(":"))
    print(4)
    edit_status_(call.message.chat.id, partner_id, 2)
    print(4)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    print(5)
    try: 
        await bot.send_message(partner_id, "@{} понравилась твоя анкета".format(call.message.chat.username))
    except:
        pass
    print(6)


@dp.callback_query_handler(lambda call: "message_id" in call.data and "user_id" in call.data)
async def mark_down(call: CallbackQuery):
    s1, s2 = map(str, call.data.split("|"))
    s, user_id = map(str, s1.split(":"))
    s, message_id = map(str, s2.split(":"))
    d = get_info(call.message.chat.id)
    if d["is_couple"]:
        s = "{}, {},\n{}, {} \n{}\n{}".format(d["name"], d["age"], d["name2"], d["age2"], d["location"], d["description"])
    else:
        s = "{}, {}, {}\n{}".format(d["name"], d["age"], d["location"], d["description"])
    if call.message.chat.username:
        try:
            print(11)
            edit_status_(call.message.chat.id, user_id, 2)
            print(user_id)
            await bot.send_message(user_id, "@{} понравилась твоя анкета".format(call.message.chat.username))
            print(22)
            try:
                await bot.send_photo(user_id, caption=s, photo=d['photo'], reply_markup=mark(call.message.chat.id, call.message.message_id, "answer"))
            except:
                await bot.send_message(user_id, s, reply_markup=mark(call.message.chat.id, call.message.message_id, "answer"))
            print(33)
        except:
            pass
    print(44)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    d = get_partners(call.message.chat.id)
    print(d)
    if d:
        print(55)
        s = "{}, {}, {}\n{}".format(d["name"], d["age"], d["location"], d["description"])
        try:
            await bot.send_photo(call.message.chat.id, caption=s, photo=d['photo'], reply_markup=mark(d["id"], call.message.message_id))
        except:
            await bot.send_message(call.message.chat.id, s, reply_markup=mark(d["id"], call.message.message_id))
        print(66)
        print(call.message.message_id)
    else:
        await call.message.answer("В вашем городе нету подходящих для вас партнёров", reply_markup=menu())


@dp.callback_query_handler(lambda call: "message_id" in call.data)
async def mark_up(call: CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    d = get_partners(call.message.chat.id)
    print(d)
    if d:
        if d["is_couple"]:
            s = "{}, {},\n{}, {} \n{}\n{}".format(d["name"], d["age"], d["name2"], d["age2"], d["location"], d["description"])
        else:
            s = "{}, {}, {}\n{}".format(d["name"], d["age"], d["location"], d["description"])
        try:
            await bot.send_photo(call.message.chat.id, caption=s, photo=d['photo'], reply_markup=mark(d["id"], call.message.message_id))
        except:
            await bot.send_message(call.message.chat.id, s, reply_markup=mark(d["id"], call.message.message_id))
        print(call.message.message_id)
    else:
        await call.message.answer("В вашем городе нету подходящих для вас партнёров", reply_markup=menu())


@dp.message_handler(state=TestStates.GENDER_STATE)
async def description(message: Message):
    s = message.text
    state = dp.current_state(user=message.from_user.id)
    if s == "👱":
        edit_gender(message.chat.id, "Парень")
        await state.set_state(TestStates.all()[5])
        await message.answer("Введите ваше имя", reply_markup=remove_keyboard())
    elif s == "👩":
        edit_gender(message.chat.id, "Девушка")
        await state.set_state(TestStates.all()[5])
        await message.answer("Введите ваше имя", reply_markup=remove_keyboard())
    elif s == "👱👩":
        edit_gender(message.chat.id, "Мы пара")
        await state.set_state(TestStates.all()[5])
        await message.answer("Введите имя парня", reply_markup=remove_keyboard())
    else:
        await message.answer("Выберите, пара МЖ, М или Ж?", reply_markup=gender_btns())



@dp.message_handler(state=TestStates.NAME_STATE)
async def name(message: Message):
    s = message.text
    state = dp.current_state(user=message.from_user.id)
    if is_couple(message.chat.id):
        if len(s) > 30:
            await message.answer("Введите имя парня")
        else:
            edit_name(message.chat.id, s)
            await message.answer("Сколько лет парню?")
            await state.set_state(TestStates.all()[0])
    else:
        if len(s) > 30:
            await message.answer("Введите ваше имя")
        else:
            edit_name(message.chat.id, s)
            await state.set_state(TestStates.all()[0])
            await message.answer("Сколько вам лет?")


@dp.message_handler(state=TestStates.AGE_STATE)
async def age(message: Message):
    s = message.text
    state = dp.current_state(user=message.from_user.id)
    if is_couple(message.chat.id):
        print("True")
        if not s.isdigit():
            await message.answer("Сколько лет парню?")
        else:
            edit_age(message.chat.id, s)
            await state.set_state(TestStates.all()[9])
            await message.answer("Введите имя девушки")
    else:
        print("False")
        if not s.isdigit():
            await message.answer("Сколько вам лет?")
        else:
            edit_age(message.chat.id, s)
            await state.set_state(TestStates.all()[2])
            await message.answer("Расскажите о себе и с кем хотите познакомиться")


@dp.message_handler(state=TestStates.SECOND_NAME)
async def name(message: Message):
    s = message.text
    state = dp.current_state(user=message.from_user.id)
    if len(s) > 30:
        await message.answer("Введите имя девушки")
    else:
        edit_name2(message.chat.id, s)
        await message.answer("Сколько лет девушке?")
        await state.set_state(TestStates.all()[8])


@dp.message_handler(state=TestStates.SECOND_AGE)
async def age(message: Message):
    s = message.text
    state = dp.current_state(user=message.from_user.id)
    if not s.isdigit():
        await message.answer("Сколько лет девушке?")
    else:
        edit_age2(message.chat.id, s)
        await state.set_state(TestStates.all()[2])
        await message.answer("Расскажите о себе и с кем хотите познакомиться")


@dp.message_handler(state=TestStates.DESCRIPTION_STATE)
async def description(message: Message):
    s = message.text
    print("description")
    if len(s) > 999:
        await message.answer("Расскажите о себе и с кем хотите познакомиться")
    else:
        edit_description(message.chat.id, s)
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(TestStates.all()[4])
        await message.answer("Из какого вы города?")



@dp.message_handler(state=TestStates.LOCATION_STATE)
async def location(message: Message):
    s = message.text
    print("location")
    if len(s) > 30:
        await message.answer("Из какого вы города?")
    else:
        edit_location(message.chat.id, s)
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(TestStates.all()[6])
        await message.answer("Отправьте мне картинку для анкеты")


@dp.message_handler(content_types=['photo'], state=TestStates.PHOTO_STATE)
async def handle_docs_photo(message):
    edit_photo(message.chat.id, message.photo[0].file_id)
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    await message.answer("Редактирование завершено", reply_markup=menu())




@dp.message_handler()
async def text_msg(message):
    db.user_create(message.chat.id)
    state = dp.current_state(user=message.from_user.id)
    print(TestStates.all())
    s = message.text
    if s == "📋 Анкета":
        d = get_info(message.chat.id)
        if d["is_couple"]:
            s = "{}, {},\n{}, {} \n{}\n{}".format(d["name"], d["age"], d["name2"], d["age2"], d["location"], d["description"])
        else:
            s = "{}, {}, {}\n{}".format(d["name"], d["age"], d["location"], d["description"])
        try:
            await bot.send_photo(message.from_user.id, caption=s, photo=d['photo'])
        except:
            await bot.send_message(message.from_user.id, s)
        await message.answer("Выберете действие с вашей анкетой", reply_markup=user_form_btns(is_activate(message.from_user.id)))
    elif s == '📝 Редактировать':
        print("|")
        print("|")
        print("V")
        print(is_couple(message.chat.id))
        await state.set_state(TestStates.all()[3])
        await message.answer("Выберите, пара МЖ, М или Ж?", reply_markup=gender_btns())
    elif s == "✅ Открыть":
        edit_status(message.chat.id, 1)
        await message.answer("Ваша анкета открыта для общего доступа", reply_markup=menu())
    elif s == "❌ Закрыть":
        edit_status(message.chat.id, 0)
        await message.answer("Ваша анкета закрыта для общего доступа", reply_markup=menu())

    elif s == '👍 Поиск симпатий':
        print("👍 Поиск симпатий")
        print(1)
        d = get_partners(message.chat.id)
        print(2)
        if d:
            print(3)
            if d["is_couple"]:
                s = "{}, {},\n{}, {} \n{}\n{}".format(d["name"], d["age"], d["name2"], d["age2"], d["location"], d["description"])
            else:
                s = "{}, {}, {}\n{}".format(d["name"], d["age"], d["location"], d["description"])
            print(4)
            print(s)
            try:
                await bot.send_photo(message.from_user.id, caption=s, photo=d['photo'], reply_markup=mark(d["id"], message.message_id))
            except:
                await bot.send_message(message.from_user.id, s, reply_markup=mark(d["id"], message.message_id))
            print(5)
            print(message.message_id)
        else:
            await message.answer("В вашем городе нет подходящих для вас партнёров", reply_markup=menu())

    elif s == "🔙 Назад" or s == "↪️ В главное меню ↩️":
        await message.answer("Вы в главном меню", reply_markup=menu())

    elif s == "💩 Помощь":
        await message.answer("Обращайтесь к @MSadovskiy", reply_markup=menu())

    elif s == "🆘 Правила":
        await message.answer("Ждём свод законов от @MSadovskiy", reply_markup=menu())

    elif s == "💼 Мой профиль":
        info = get_info(message.chat.id)
        cash = int(info["cash"]) if info["cash"] == int(info["cash"]) else info["cash"]
        wasted = int(info["wasted"]) if info["wasted"] == int(info["wasted"]) else info["wasted"]
        s = "id: " + str(message.chat.id) + "\n"
        s += "Ваш баланс: " + str(cash) + " руб.\n"
        s += "Потрачено за всё время: " + str(wasted) + " руб.\n"
        await message.answer(s, reply_markup=info_btns())

    elif s == "👤 Рефералы":
        ref_create(message.chat.id)
        referrals = get_ref(message.chat.id)
        refs = list(map(lambda x: x["cash"], referrals))
        all_cash = sum(refs)
        count = len(refs)
        await message.answer("👤Ваш реферер:  \nПроцент возврата по реферальной программе 50% \nВаша реферальная ссылка: https://t.me/swingerclubbot?start={} \nКоличество ваших рефералов: {} \nВыплаченная сумма за рефералов: {} руб.".format(message.chat.id, count, all_cash), reply_markup=tomenu())

    else:
        await message.answer("Воспользуйтесь клавиатурой", reply_markup=menu()) 