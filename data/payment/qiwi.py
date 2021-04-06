import requests
from SimpleQIWI import *


QIWI_TOKEN = "9ee0094a2e6b0c8cb1d552b225207496"
QIWI_NUMBER = '79139161087'
MAIN_URL = "https://edge.qiwi.com"


def get_comments(length=15):
	headers = {
		"Accept": "application/json",
		"Content-Type": "application/json",
		"Authorization": "Bearer {}".format(QIWI_TOKEN)
			  }
	comments = {}
	r = requests.get("https://edge.qiwi.com/payment-history/v2/persons/{}/payments?rows={}".format(QIWI_NUMBER, length), 
		headers=headers, verify=False).json()
	for i in r["data"]:
	    if i['total']['currency'] == 643:
	        a = "r" if i["comment"] is None else i["comment"]
	        comments[a] = i["sum"]["amount"]
	print(comments)
	return comments


def get_number():
	headers = {
		"Accept": "application/json",
		"Content-Type": "application/json",
		"Authorization": "Bearer {}".format(QIWI_TOKEN)
			  }
	comments = {}
	r = requests.get("https://edge.qiwi.com/payment-history/v2/persons/{}/payments?rows={}".format(QIWI_NUMBER, 15), headers=headers, verify=False).json()
	for i in r["data"]:
	    if i['total']['currency'] == 643:
	        a = "r" if i["comment"] is None else i["comment"]
	        comments[a] = i["account"]
	return comments


def send_money(price, qiwi):
	api = QApi(token=QIWI_TOKEN, phone=QIWI_NUMBER)
	print(api.balance)
	print(api.pay(account="{}".format(qiwi), amount=price))


def get_balance():
	api = QApi(token=QIWI_TOKEN, phone=QIWI_NUMBER)
	return api.balance