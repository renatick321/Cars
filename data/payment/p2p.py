import requests
import random
from datetime import datetime

CHARS = 'abcdefghijklnopqrstuvwxyz1234567890'

def password_create(length=31):
	password = ''
	for i in range(length):
		password += random.choice(CHARS)
	return password


QIWI_TOKEN = "9ee0094a2e6b0c8cb1d552b225207496"
QIWI_NUMBER = '79139161087'
PUBLIC_KEY = "48e7qUxn9T7RyYE1MVZswX1FRSbE6iyCj2gCRwwF3Dnh5XrasNTx3BGPiMsyXQFNKQhvukniQG8RTVhYm3iP75TsN1Nbjg6KniAPSoWRGKMNFCtaeug7v194Cutw2Q8ugpBVgPjk1cv9ZGFcG3FiGgsuXAYWyJvjkLC8cLVL6sgW1HHChdcRRe63WLh5n"
SECRET_KEY = "eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6IjlocnZ5OC0wMCIsInVzZXJfaWQiOiI3OTEzOTE2MTA4NyIsInNlY3JldCI6Ijc4ODhkODU2YjMyNGIyMTgzMDNlOTNkYzlmNDJiMGM2ZjM1OTU5Mzc2MWZmMmYwMzRiZmUwODM4ODAyZjUyMWEifX0="


from pyqiwip2p import QiwiP2P
from pyqiwip2p.types import QiwiCustomer, QiwiDatetime

QIWI_PRIV_KEY = SECRET_KEY


p2p = QiwiP2P(auth_key=QIWI_PRIV_KEY)

def payment_create(amount):
	d = {}
	bill_id = password_create(10)
	new_bill = p2p.bill(bill_id=bill_id, amount=amount, lifetime=15)
	d["bill_id"] = bill_id
	d["url"] = new_bill.pay_url
	return d


def payment_check(bill_id):
	return p2p.check(bill_id=bill_id).status


def get_amount(bill_id):
	return float(p2p.check(bill_id=bill_id).amount)



# Выставим счет на сумму 228 рублей который будет работать 45 минут



#print(new_bill.bill_id, new_bill.pay_url)

# Проверим статус выставленного счета

#print(p2p.check(bill_id=new_bill.bill_id).status)

# Потеряли ссылку на оплату счета? Не проблема!

#print(p2p.check(bill_id=billid).pay_url)

# Клиент отменил заказ? Тогда и счет надо закрыть

#p2p.reject(bill_id=new_bill.bill_id)


# Если планируете выставлять счета с одинаковой суммой,
# можно воспользоваться параметром default_amount

# Теперь, если не указывать в методе p2p.bill() значение суммы заказа,
# будет применяться указанная базовая сумма

# А ещё можно не указывать bill_id, тогда значение сгенерируется автоматически.
# Его можно будет посмотреть в объекте ответа Bill
# В комбинации со стандартным значением суммы будет вот так