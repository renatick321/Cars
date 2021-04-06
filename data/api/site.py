import requests
from bs4 import BeautifulSoup


def auth(phone, password):
	p = phone
	d = {"phone": f'{p[0:2]}({p[2:5]}){p[5:8]}-{p[8:10]}-{p[10:]}', 'password': str(password)}
	r = requests.post('https://xn----8sbaaipreg6amlehj7alg2fo.xn--p1ai/account/account/login', data=d)
	return r.status_code == 200


class Parser:
	def __init__(self, article, phone, password):
		self.article = article
		self.session = requests.Session()
		p = phone
		d = {"phone": f'{p[0:2]}({p[2:5]}){p[5:8]}-{p[8:10]}-{p[10:]}', 'password': str(password)}
		self.session.post('https://xn----8sbaaipreg6amlehj7alg2fo.xn--p1ai/account/account/login', data=d)

	def get_named(self):
		url = f'https://чемпион-автозапчасти.рф/parts/search/{self.article}'
		page = self.session.get(url)
		soup = BeautifulSoup(page.text, "html.parser")
		lst = []
		for i in soup.findAll('table', class_='table table-hover'):
			for j in i.findAll('tr', class_='pointer'):
				lst.append(j.find_all('td')[0].getText())
		print(lst)
		return lst

	def get_prices(self, brand):
		url = f'https://xn----8sbaaipreg6amlehj7alg2fo.xn--p1ai/parts/search/{self.article}/{brand}'
		page = self.session.get(url)
		soup = BeautifulSoup(page.text, "html.parser")
		money_lst = []
		time_lst = []
		for i in soup.findAll('div', class_='bestpart'):
			time, money = i.findAll("span", class_='btn btn-sm btn-default')
			time = time.getText()
			money = money.getText()
			time_lst.append(list(map(str, time.split()))[0])
			money_lst.append(money[::-1][1:][::-1])
		money = min(money_lst)
		time = min(time_lst)
		return [brand, money, time]