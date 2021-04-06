import random


TEST_TOKEN = "1300122347:AAE7lijSVYwFBmUkU82x4tyJt31UDTP-PVo"
TEST_ADMIN = 1198883635

TOKEN = "1613314929:AAH2YDtCf00WcWyfk5j4oHCdJJQz4H4afcQ"
ADMIN_ID = 1372229127

BOT_TOKEN = TEST_TOKEN
ADMIN = TEST_ADMIN

DB_URL = "data/db.db"
TEMPORY_DB_URL = "data/temporary.db"

base_image = "AgACAgIAAxkBAANeX23Zxu85ylTKcDrLhw8FX1ODzZQAAouuMRuP03FLllvjRge28UYh3s-WLgADAQADAgADbQADpgABAQABGwQ"

CHARS = 'abcdefghijklnopqrstuvwxyz1234567890'
LETTERS = "abcdefghijklnopqrstuvwxyz"

QIWI_TOKEN = "cf2258772ff94b31f98ecfcd4f362b73"
QIWI_NUMBER = '79647833930'

RADIUS = 200

def price_boost(price):
	price = float(price)
	price *= 1.7
	price = float(int(price * 100)) / 100
	return price


def password_create(length=16):
	password = ''
	for i in range(length):
		password += random.choice(CHARS)
	return password