from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import buy_callback


def mark(user_id, message_id='112', answer=""):
    keyboard = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('❤', callback_data="user_id:{}|like".format(user_id))
    btn2 = InlineKeyboardButton('👎', callback_data="user_id:{}|notlike".format(user_id))
    btn3 = InlineKeyboardButton('🏠', callback_data="Home")
    keyboard.row(btn1, btn2)
    keyboard.row(btn3)
    return keyboard

def catalog_btns(data, path=''):
    data = list(map(lambda x: str(x), data))
    keyboard = InlineKeyboardMarkup()
    lst = [InlineKeyboardButton(str(i + 1), callback_data="path:" + (data[i] if path == '' else path + ":" + data[i])) for i in range(len(data))]
    keyboard.add(*lst)
    if path != '':
        keyboard.row(InlineKeyboardButton('🔙 Вернуться назад', callback_data="back:"+path))
    return keyboard

def choice_btns(path):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton('✅ Выбрать узел', callback_data="choice:"+path))
    keyboard.row(InlineKeyboardButton('🔙 Вернуться назад', callback_data="back:"+path))
    return keyboard

def get_nodes(lst):
    keyboard = InlineKeyboardMarkup()
    lst1 = []
    for i in range(len(lst)):
        lst1.append(InlineKeyboardButton(str(i + 1), callback_data="node:" + lst[i]))
    keyboard.add(*lst1)
    return keyboard


def parts_btns(parts):
    keyboard = InlineKeyboardMarkup()
    lst1 = []
    for i in range(len(parts)):
        lst1.append(InlineKeyboardButton(str(i + 1), callback_data="part:" + parts[i]))
    keyboard.add(*lst1)
    return keyboard


def urls_btns(part, money_brand, time_brand):
    url = f"https://чемпион-автозапчасти.рф/parts/search/{part}"
    money_url = f'https://xn----8sbaaipreg6amlehj7alg2fo.xn--p1ai/parts/search/{part}/{money_brand}'
    time_url = f'https://xn----8sbaaipreg6amlehj7alg2fo.xn--p1ai/parts/search/{part}/{time_brand}'
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Выбор бренда', url=url))
    keyboard.add(InlineKeyboardButton('Самая низкая цена', url=money_url))
    keyboard.add(InlineKeyboardButton('Самая быстрая доставка', url=time_url))
    return keyboard

def type_btns():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton('Легковые', callback_data="type:0"))
    keyboard.row(InlineKeyboardButton('Коммерческие', callback_data="type:1"))
    keyboard.row(InlineKeyboardButton('Мотоциклы', callback_data="type:2"))
    keyboard.row(InlineKeyboardButton('Грузовые', callback_data="type:3"))
    keyboard.row(InlineKeyboardButton('Спецтехника', callback_data="type:4"))
    return keyboard

def code_btns(codes):
    keyboard = InlineKeyboardMarkup()
    lst1 = []
    for i in range(len(codes)):
        lst1.append(InlineKeyboardButton(str(i + 1), callback_data="code:" + codes[i]))
    keyboard.add(*lst1)
    return keyboard

def family_btns(names, code):
    keyboard = InlineKeyboardMarkup()
    lst1 = []
    for i in range(len(names)):
        lst1.append(InlineKeyboardButton(str(i + 1), callback_data="family:" + names[i] + "|" + code))
    keyboard.add(*lst1)
    return keyboard

def models_btns(names, family, code):
    keyboard = InlineKeyboardMarkup()
    lst1 = []
    for i in range(len(names)):
        lst1.append(InlineKeyboardButton(str(i + 1), callback_data="model:" + names[i] + "|" + family + '|' + code))
    keyboard.add(*lst1)
    return keyboard

def modif_btns(lst):
    keyboard = InlineKeyboardMarkup()
    lst1 = []
    for i in range(len(lst)):
        lst1.append(InlineKeyboardButton(str(i + 1), callback_data="modif:" + str(i)))
    keyboard.add(*lst1)
    return keyboard