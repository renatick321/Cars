from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def remove_keyboard():
	keyboard = ReplyKeyboardRemove()
	return keyboard


def menu():
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	keyboard.row(KeyboardButton("💼 Каталог товаров"), KeyboardButton("🚗 Изменить VIN"))
	return keyboard

def yes():
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	keyboard.row(KeyboardButton("✅ Да"))
	return keyboard

def yesno():
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	keyboard.row(KeyboardButton("✅ Да"), KeyboardButton("❌ Нет"))
	return keyboard

def use_sh():
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	keyboard.row(KeyboardButton("🗒 Использовать шаблонизатор"))
	return keyboard