from loader import dp, bot
from aiogram.dispatcher.filters import Command
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions, Message, CallbackQuery
from keyboards.inline.choice_buttons import *
from keyboards.reply.choice_buttons import *
from data import db
from config import ADMIN, BOT_TOKEN
from data.db import *
from data.payment.p2p import payment_create, payment_check, get_amount, QIWI_NUMBER
from data.payment.qiwi import get_number, send_money, get_balance
from utils import StartStates, RegistrationStates, LoginStates, send_notification, SomeStufStates
from aiogram.dispatcher import FSMContext
import data.api.site as site
import data.api.levam as levam
import random
import json
from google_trans_new import google_translator
from time import sleep
import sys
import requests


@dp.message_handler(Command('start'))  # Начало начал
async def start_command(message):
    await bot.send_message(
        message.chat.id,
                "Здравствуйте, вы хотите заказать запчасть?",
        reply_markup=yes() 
                    )
    await StartStates.SPARE_PARTS_STATE.set()

s = 'XWFPF2DC1C0018349'


@dp.message_handler(state=StartStates.SPARE_PARTS_STATE)
async def spare_parts_state(message: Message):
    if message.text == '✅ Да':
        await bot.send_message(message.chat.id, "Вы зарегистрированы?", reply_markup=yesno())
        await StartStates.REG_LOG_STATE.set()
    

@dp.message_handler(state=StartStates.REG_LOG_STATE)
async def spare_parts_state(message: Message):
    if message.text == '❌ Нет':
        await bot.send_message(message.chat.id, "Зарегистрируйтесь на сайте: https://чемпион-автозапчасти.рф", reply_markup=remove_keyboard())
    await bot.send_message(message.chat.id, "Введите ваш номер телефона в формате +7ХХХХХХХХХХ", reply_markup=remove_keyboard())
    await LoginStates.NUMBER_STATE.set()



# Авторизация
@dp.message_handler(state=LoginStates.NUMBER_STATE)
async def spare_parts_state(message: Message):
    s = message.text
    if not bool(await get_user_number_(s[1:])):
        await message.answer("Вы не зарегистрированы на https://чемпион-автозапчасти.рф")
    elif len(s) == 12:
        phone_save(s, message.chat.id)
        await bot.send_message(message.chat.id, "Введите пароль")
        await LoginStates.PASSWORD_STATE.set()
    else:
        await bot.send_message(message.chat.id, "Пожалуйста, введите ваш номер телефона в формате +7ХХХХХХХХХХ", reply_markup=remove_keyboard())


@dp.message_handler(state=LoginStates.PASSWORD_STATE)
async def spare_parts_state(message: Message):
    s = message.text
    phone = get_phone(message.chat.id)
    password = s
    if site.auth(phone, password):
        await bot.send_message(message.chat.id, 
            "Вы успешно вошли в свой аккаунт!\nВведите ваш VIN или сфотографируйте СТС", 
            reply_markup=remove_keyboard())
        await SomeStufStates.START_VIN_STATE.set()
        password_save(password, message.chat.id)
    else:
        await bot.send_message(message.chat.id, 
            "Ваши номер телефона или пароль были введены неверно, попробуйте снова", 
            reply_markup=remove_keyboard())
        await bot.send_message(message.chat.id, "Введите номер телефона", reply_markup=remove_keyboard())
        await LoginStates.NUMBER_STATE.set()



@dp.message_handler(content_types=['photo'], state=SomeStufStates.START_VIN_STATE)
async def vin_msg(message: Message):
    await message.answer("Ваш VIN не получилось идентифицировать, пожалуйста, введите его сообщением")


@dp.message_handler(state=SomeStufStates.START_VIN_STATE)
async def vin_msg(message: Message, state: FSMContext):
    s = message.text
    if s == '🗒 Использовать шаблонизатор':
        await message.answer("Выберите тип вашей машины", reply_markup=type_btns())
        await state.finish()
    else:
        try:
            link = levam.get_link(s)
            ssd = levam.get_ssd(link)
            tree = levam.tree_get(link)
            car_save(message.chat.id, link, ssd, json.dumps(tree))
            await state.finish()
            await message.answer("Вы успешно ввели свой VIN", reply_markup=menu())
        except KeyError:
            await message.answer("Не удалось найти ваш VIN, повторите попытку снова или найдите вашу машину при помощи нашего шаблонизатора", reply_markup=use_sh())


@dp.message_handler(state=SomeStufStates.TEMPLATE_STATE)
async def vin_msg(message: Message, state: FSMContext):
    await message.answer("Введите данные вашей машины")

@dp.message_handler()
async def text_msg(message: Message):
    s = message.text
    if not bool(get_data(message.chat.id)):
        await message.answer("Выберите тип вашей машины", reply_markup=type_btns())
    elif s == '💼 Каталог товаров':
        data = levam.get_names(get_data(message.chat.id))
        names = list(data.values())
        numbers = list(data.keys())
        s = ''
        for i in range(len(names)):
            s += f"{i+1}: {names[i]}\n"
        await message.answer(s, reply_markup=catalog_btns(numbers))
    elif s =='🚗 Изменить VIN':
        await bot.send_message(message.chat.id, "Вы успешно вошли в свой аккаунт!\nВведите ваш VIN или сфотографируйте СТС", reply_markup=remove_keyboard())
        await SomeStufStates.START_VIN_STATE.set()
    else:
        data = get_data(message.chat.id)
        path = part_search(data, s)
        if path is None:
            await message.answer("Узел {} не найден, вы в главном меню".format(s), reply_markup=menu())
        else:
            data = levam.get_names(get_data(message.chat.id), path)
            if data:
                names = list(data.values())
                numbers = list(data.keys())
                s = ''
                for i in range(len(names)):
                    s += f"{i+1}: {names[i]}\n"
                await message.answer(s, reply_markup=catalog_btns(numbers, path))
            else:
                s = levam.get_named_path(get_data(message.chat.id), path)
                await message.answer(s, reply_markup=choice_btns(path))



@dp.callback_query_handler(lambda call: "path" in call.data)
async def get_event_info(call: CallbackQuery):
    path = call.data[5:]
    data = levam.get_names(get_data(call.message.chat.id), path)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    if data:
        names = list(data.values())
        numbers = list(data.keys())
        s = ''
        for i in range(len(names)):
            s += f"{i+1}: {names[i]}\n"
        await call.message.answer(s, reply_markup=catalog_btns(numbers, path))
    else:
        s = levam.get_named_path(get_data(call.message.chat.id), path)
        await call.message.answer(s, reply_markup=choice_btns(path))


@dp.callback_query_handler(lambda call: "back" in call.data)
async def get_event_info(call: CallbackQuery):
    path = call.data[5:]
    path = list(map(str, path.split(":")))[::-1]
    del path[0]
    path = ":".join(path[::-1])
    data = levam.get_names(get_data(call.message.chat.id), path)
    names = list(data.values())
    numbers = list(data.keys())
    s = ''
    for i in range(len(names)):
        s += f"{i+1}: {names[i]}\n"
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    print(numbers, path)
    await call.message.answer(s, reply_markup=catalog_btns(numbers, path))


@dp.callback_query_handler(lambda call: "choice" in call.data)
async def get_event_info(call: CallbackQuery):
    path = "->".join(list(map(str, call.data[7:].split(":"))))
    print("12121122121221")
    data = get_car(call.message.chat.id)
    link = data['link']
    ssd = data['ssd']
    data = levam.get_node(link, ssd, path)
    if type(data) == type([]):
        s = '*'
        lst = []
        for i in range(len(data)):
            d = data[i]
            s += f'{i + 1}: ' + d['header'].lower() + "\n"
            print("node", d['node'])
            if d['node'] != '':
                lst.append(f"{d['node']}||| ")
            try:
                s = d['image']
                img = s
                print(img)
                print(d['node'])
                p = requests.get(img)
                out = open(f"{d['node']}.png", "wb")
                print(d['node'])
                out.write(p.content)
                out.close()
            except:
                pass
        print("11111111111")
        print(lst)
        if lst:
            s = await short(s, call.message)
            print("1221211")
            await call.message.answer(s, reply_markup=get_nodes(lst))
        else:
            await call.message.answer("Данного узла не существует", reply_markup=menu())
    else:
        await call.message.answer("Ошибка: " + data, reply_markup=menu())


@dp.callback_query_handler(lambda call: "node" in call.data)
async def get_event_info(call: CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    node, image = map(str, call.data[5:].split("|||"))
    data = get_car(call.message.chat.id)
    link = data['link']
    ssd = data['ssd']
    parts = []
    if image != ' ':
        s = image
    else:
        s = ''
    for i in levam.get_parts(node, ssd, link):
        parts.append(i['standart']['part_code'])
        s += str(s.count('\n') + 1) + f"({i['standart']['part_code']}): {i['standart']['part_name']}" + "\n"
    print("node:", node)
    try:
        photo = open(f"{node}.png", "rb")
        s = await short_caption(s, call.message)
        await bot.send_photo(call.message.chat.id, caption=s, photo=photo, reply_markup=parts_btns(parts))
    except FileNotFoundError:
        s = await short(s, call.message)
        await call.message.answer(s, reply_markup=parts_btns(parts))




@dp.callback_query_handler(lambda call: "part" in call.data)
async def get_event_info(call: CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    part = call.data[5:]
    money_brand = None
    time_brand = None
    phone, password = get_user_info(call.message.chat.id)
    parser = site.Parser(part, phone, password)
    for i in parser.get_named():
        sleep(7)
        try:
            data = parser.get_prices(i)
        except:
            continue
        if money_brand is None and time_brand is None:
            money_brand = data[0]
            money = data[1]
            time_brand = data[0]
            time = data[2]
        if money < data[1]:
            money = data[1]
            money_brand = data[0]
        if time < data[2]:
            time = data[2]
            time_brand = data[0]
    if money_brand is None:
        money_brand = 'GENERAL MOTORS'
    if time_brand is None:
        money_brand = 'GENERAL MOTORS'
    await call.message.answer("Ваша запчасть", reply_markup=urls_btns(part, money_brand, time_brand))




@dp.callback_query_handler(lambda call: "type" in call.data)
async def get_event_info(call: CallbackQuery):
    num = call.data[5:]
    print(num)
    data = levam.catalogslistget(num)
    codes = list(data.values())
    names = list(data.keys())
    s = ''
    for i in range(len(names)):
        s += f"{i + 1}: {names[i]}\n"
    print(data)
    await call.message.answer(s, reply_markup=code_btns(codes))


@dp.callback_query_handler(lambda call: "code" in call.data)
async def get_event_info(call: CallbackQuery):
    code = call.data[5:]
    data = levam.get_family_tree(code)
    car_models_save(call.message.chat.id, data)
    names = levam.get_family_names(data)
    s = ''
    for i in range(len(names)):
        s += f"{i + 1}: {names[i]}\n"
    await call.message.answer(s, reply_markup=family_btns(names, code))


@dp.callback_query_handler(lambda call: "family" in call.data)
async def get_event_info(call: CallbackQuery):
    family, code = call.data[7:].split("|")
    print(family)
    data = get_car_models_data(call.message.chat.id)
    names = levam.get_model_names(data, family)
    s = ''
    for i in range(len(names)):
        s += f"{i + 1}: {names[i]}\n"
    await call.message.answer(s, reply_markup=models_btns(names, family, code))


@dp.callback_query_handler(lambda call: "model" in call.data)
async def get_event_info(call: CallbackQuery):
    model, family, code = call.data[6:].split("|")
    ssd = levam.vehicle(family, model, code)
    modif = levam.get_modifications(ssd)
    s = ''
    ssd_save(call.message.chat.id, ssd)
    links = []
    for i in range(len(modif)):
        print()
        lst = []
        for j in modif[i]:
            if j != 'link':
                lst.append(modif[i][j])
        s += f'{i + 1}: {" ".join(lst)}\n'
        links.append(modif[i]["link"])
    await call.message.answer(s, reply_markup=modif_btns(links))


@dp.callback_query_handler(lambda call: "modif" in call.data)
async def get_event_info(call: CallbackQuery, state: FSMContext):
    num = call.data[6:]
    link = levam.get_modifications(get_ssd(call.message.chat.id))[int(num)]['link']
    data = levam.tree_get(link)
    link_data_save(call.message.chat.id, link, data)
    await state.finish()
    await call.message.answer("Вы в главном меню", reply_markup=menu())





{'standart': {'part_number': '20', 'part_code': '13283239', 'part_name': 'CLAMP,HOSE,OUTLET  (PRODUCTION NO. 13239145)', 'part_quantity': '1', 'node_link': '', 'type': 'part'}, 'add': {'info': '', 'applicability': ''}}


async def short(string, message):
    lst = list(map(str, string.split("\n")))
    s = ''
    print(lst)
    for i in lst:
        if len(s + "\n" + i) > 1000:
            await message.answer(s)
            s = i
        else:
            s += "\n" + i
    return s



import asyncio
import asyncpg
async def get_user_number_(number):
    conn = await asyncpg.connect(user='champion', password='bae2EM7eeex7ze9Rseiwoh0W',
                                 database='champion', host='127.0.0.1')
    values = await conn.fetch(f"""SELECT * FROM client where phone='{number}'""")
    await conn.close()
    return values


async def short_caption(string, message):
    lst = list(map(str, string.split("\n")))
    s = ''
    for i in lst:
        if len(s + "\n" + i) > 1000:
            await message.answer(s)
            s = i
        else:
            s += "\n" + i
    return s



def translate(text):
    text = google_translator().translate(text, lang_src='en', lang_tgt='ru').lower()
    translit(text, 'ru')
    return translit(text, 'ru')



def part_search(data, part_name):
    d = {}
    lst = []
    lst.append(data)
    ind = 0
    part_name = part_name.lower()
    print(part_name)
    while len(lst) != ind:
        ii = list(lst[ind].keys())
        for i in ii:
            if lst[ind][i]['data']:
                lst.append(lst[ind][i]['data'])
                for j in lst[ind][i]['data'].keys():
                    d[j] = i
            if lst[ind][i]['name'].lower() == part_name or lst[ind][i]['name'].lower() == " ".join(list(map(str, part_name.split()))[::-1]) or part_name in lst[ind][i]['name'].lower() and len(part_name) > 3:
                path = []
                try:
                    path.append(str(i))
                    back = d[i]
                    while True:
                        path.append(str(back))
                        back = d[back]
                except KeyError:
                    return ":".join(path[::-1])
        ind += 1
    return None
