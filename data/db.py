import sqlite3
from config import DB_URL, password_create, RADIUS, TEMPORY_DB_URL
from datetime import datetime, timedelta
from config import base_image
import random
from math import acos, sin, cos
from haversine import haversine
import json



conn = sqlite3.connect(DB_URL)
cursor = conn.cursor()


def phone_save(phone, user_id):
	cursor.execute("DELETE FROM Phone WHERE user_id = {}".format(user_id))
	cursor.execute("INSERT INTO Phone(user_id, phone) VALUES ({}, '{}')".format(user_id, phone))
	conn.commit()

def password_save(password, user_id):
	cursor.execute("UPDATE Phone SET password = '{}' WHERE user_id = {}".format(password, user_id))
	conn.commit()

def get_user_info(user_id):
	for i in cursor.execute("SELECT phone, password from Phone WHERE user_id = {}".format(user_id)):
		return i[0], i[1]
	return None


def get_phone(user_id):
	for i in cursor.execute("SELECT phone from Phone WHERE user_id = {}".format(user_id)):
		return i[0]
	return None


def car_save(user_id, link, ssd, data):
	cursor.execute("DELETE FROM Car WHERE user_id = {}".format(user_id))
	cursor.execute("INSERT INTO Car(user_id, link, ssd, data) VALUES ({}, '{}', '{}', '{}')".format(user_id, link, ssd, data))
	conn.commit()

def ssd_save(user_id, ssd):
	cursor.execute("DELETE FROM Car WHERE user_id = {}".format(user_id))
	cursor.execute("INSERT INTO Car(user_id, ssd) VALUES ({}, '{}')".format(user_id, ssd))
	conn.commit()

def get_ssd(user_id):
	for i in cursor.execute("SELECT ssd from Car WHERE user_id = {}".format(user_id)):
		return i[0]
	return None


def link_data_save(user_id, link, data):
	cursor.execute("UPDATE Car SET link = '{}' WHERE user_id = {}".format(link, user_id))
	cursor.execute("UPDATE Car SET data = '{}' WHERE user_id = {}".format(json.dumps(data), user_id))
	conn.commit()


def get_data(user_id):
	for i in cursor.execute("SELECT data from Car WHERE user_id = {}".format(user_id)):
		return json.loads(i[0])


def get_car(user_id):
	for i in cursor.execute("SELECT link, ssd from Car WHERE user_id = {}".format(user_id)):
		return {"link": i[0], "ssd": i[1]}
	return None

def car_models_save(user_id, data):
	cursor.execute("DELETE FROM Car_Models WHERE user_id = {}".format(user_id))
	cursor.execute("INSERT INTO Car_Models(user_id, data) VALUES ({}, '{}')".format(user_id, json.dumps(data)))
	conn.commit()

def get_car_models_data(user_id):
	for i in cursor.execute("SELECT data from Car_Models WHERE user_id = {}".format(user_id)):
		return json.loads(i[0])
	return None





























def user_create(id):
	cursor.execute("""
					  INSERT INTO Users(user_id, name, location, description, photo, profile_status, gender, age, dt, cash, wasted, x, y, username) 
					  SELECT {}, '{}', '{}', '{}', '{}', {}, '{}', '{}', {}, 0, 0, 0, 0, 'username' WHERE NOT EXISTS(SELECT 1 FROM Users WHERE user_id = {})
				   """.format(id, "Имя", "Город", "О себе", base_image, 1, "Парень", "Возраст", datetime.now().strftime('%Y-%m-%d'), id))
	conn.commit()


def block(user_id):
	a = False
	for i in cursor.execute("SELECT cash FROM Users WHERE user_id = {}".format(user_id)):
		a = True
	if a:
		cursor.execute("UPDATE Users SET is_blocked = 1 WHERE user_id = {}".format(user_id))
		conn.commit()
		return "Пользователь успешно заблокирован!"
	else:
		return "Пользователь не найден"


def unblock(user_id):
	a = False
	for i in cursor.execute("SELECT cash FROM Users WHERE user_id = {}".format(user_id)):
		a = True
	if a:
		cursor.execute("UPDATE Users SET is_blocked = 0 WHERE user_id = {}".format(user_id))
		conn.commit()
		return "Пользователь успешно разблокирован!"
	else:
		return "Пользователь не найден"


def updatetime():
	cursor.execute("UPDATE Users SET dt = '{}'".format(datetime.now()))
	conn.commit()


def ref_create(user_id, promo_id="NULL"):
	cursor.execute("""INSERT INTO Promo(user_id, promo_id, cash) 
					  SELECT {}, {}, {} WHERE NOT EXISTS(SELECT 1 FROM Promo WHERE user_id = {})
				   """.format(user_id, promo_id, 0, user_id))
	conn.commit()


def get_ref(user_id):
	referrals = []
	for i in cursor.execute("SELECT user_id, promo_id, cash FROM Promo WHERE promo_id={}".format(user_id)):
		d = {}
		d["user_id"] = i[0]
		d["promo_id"] = i[1]
		d["cash"] = i[2]
		referrals.append(d)
	return referrals

def payment_done(user_id, amount):
	for i in cursor.execute("SELECT cash FROM Users WHERE user_id = {}".format(user_id)):
		amount += float(i[0])
	cursor.execute("UPDATE Users SET cash = {} WHERE user_id = {}".format(round(amount, 2), user_id))
	d = {}
	for i in cursor.execute("SELECT promo_id FROM Promo WHERE user_id = {}".format(user_id)):
		d["promo_id"] = i[0]
	try:
		for i in cursor.execute("SELECT cash FROM Promo WHERE user_id = {}".format(d["promo_id"])):
			d["cash"] = i[0]
		for i in cursor.execute("SELECT cash FROM Users WHERE user_id = {}".format(d["promo_id"])):
			d["cash_"] = i[0]
		cursor.execute("UPDATE Users SET cash = {} WHERE user_id = {}".format(round(d["cash_"] + amount * 0.2, 2), user_id))
		cursor.execute("UPDATE Promo SET cash = {} WHERE user_id = {}".format(round(d["cash"] + amount * 0.2, 2), user_id))
	except:
		pass
	conn.commit()



def get_users(location="all"):
	users = []
	if location == "all":
		for i in cursor.execute("SELECT user_id FROM Users WHERE is_blocked = 0"):
			users.append(i[0])
	else:
		for i in cursor.execute("SELECT user_id FROM Users WHERE location='{}' AND is_blocked = 0".format(location)):
			users.append(i[0])

	return users


def get_info(user_id):
	d = {}
	print(user_id, "********")
	for i in cursor.execute("SELECT user_id, name, location, description, photo, profile_status, age, gender, name2, age2, cash, wasted, x, y FROM Users WHERE user_id={}".format(user_id)):
		d["id"] = i[0]
		d['name'] = i[1]
		d["location"] = i[2]
		d["description"] = i[3]
		d["photo"] = i[4]
		d["state"] = i[5]
		d["age"] = i[6]
		d['gender'] = i[7]
		d["name2"] = i[8]
		d['age2'] = i[9]
		d["cash"] = i[10]
		d["wasted"] = i[11]
		d["x"] = i[12]
		d["y"] = i[13]
	return d


def is_activate(user_id):
	for i in cursor.execute("SELECT profile_status FROM Users WHERE user_id={}".format(user_id)):
		a = i[0]
		return True if a == 1 else False


def edit_name(user_id, name):
	cursor.execute("UPDATE Users SET name = '{}' WHERE user_id = {}".format(name, user_id))
	conn.commit()


def edit_age(user_id, age):
	cursor.execute("UPDATE Users SET age = '{}' WHERE user_id = {}".format(age, user_id))
	conn.commit()


def edit_name2(user_id, name):
	cursor.execute("UPDATE Users SET name2 = '{}' WHERE user_id = {}".format(name, user_id))
	conn.commit()


def edit_age2(user_id, age):
	cursor.execute("UPDATE Users SET age2 = '{}' WHERE user_id = {}".format(age, user_id))
	conn.commit()


def edit_location(user_id, x, y):
	cursor.execute("UPDATE Users SET x = {}, y = {} WHERE user_id = {}".format(x, y, user_id))
	conn.commit()


def edit_description(user_id, description):
	cursor.execute("UPDATE Users SET description = '{}' WHERE user_id = {}".format(description, user_id))
	conn.commit()


def edit_photo(user_id, photo):
	cursor.execute("UPDATE Users SET photo = '{}' WHERE user_id = {}".format(photo, user_id))
	conn.commit()


def edit_status(user_id, status):
	cursor.execute("UPDATE Users SET profile_status = {} WHERE user_id = {}".format(status, user_id))
	conn.commit()


def edit_gender(user_id, gender):
	cursor.execute("UPDATE Users SET gender = '{}' WHERE user_id = {}".format(gender, user_id))
	conn.commit()



def edit_status_(user_id, partner_id, status):
	cursor.execute("UPDATE History SET status = {} WHERE user_id = {} AND partner_id = {}".format(status, user_id, partner_id))
	conn.commit()


def edit_username(user_id, username):
	cursor.execute("UPDATE Users SET username = '{}' WHERE user_id = {}".format(username, user_id))
	conn.commit()


def edit_cash(user_id, cash):
	cursor.execute("UPDATE Users SET cash = {} WHERE user_id = {}".format(cash, user_id))
	conn.commit()


def get_partners(user_id):
	lst = []
	info = get_info(user_id)
	location = info["location"]
	x = info["x"]
	y = info["y"]
	lst = []
	for i in cursor.execute("SELECT user_id, cash, x, y, name FROM Users WHERE x != 0 AND y != 0 AND profile_status = 1 AND user_id != {}".format(user_id, user_id)):
		if haversine((x, y), (i[2], i[3])) < RADIUS: # В ближайших RADIUS км
			lst.append([i[0], i[1]]) # Для сортировки по дате и деньгам 
	assessed = []
	lst = lst[::-1] # Переворачиваем список, чем новее анкета, тем раньше
	index = 1
	try:
		while int(lst[index][0]) != int(user_id):
			index += 1
		place = index
	except:
		place = index
	for i in cursor.execute("SELECT partner_id, user_id FROM History WHERE user_id = {} OR partner_id = {}".format(user_id, user_id)):
		if i[0] == user_id:
			assessed.append(i[1])
		else:
			assessed.append(i[0])
	lst = list(filter(lambda l: l[0] not in assessed, lst))
	lst = sorted(lst, key=lambda l: l[1]) # Сортируем по cash
	lst = list(map(lambda l: l[0], lst))
	s = 'Вы на {} месте'.format(place)
	if place != 1:
		s += ', поднимите!'
	if lst:
		d = get_info(lst[0])
		d['place'] = s
		return d
	else:
		return False



def is_couple(user_id):
	lst = []
	for i in cursor.execute("SELECT gender FROM Users WHERE user_id = {}".format(user_id)):
		a = i[0]
		lst.append(a)
	if lst[0] == "Мы пара":
		return True
	else:
		return False


def get_distance(user_id1, user_id2):
	lst1 = []
	for i in cursor.execute("SELECT x, y FROM Users WHERE user_id = {}".format(user_id1)):
		x1 = i[0]
		y1 = i[1]
		lst1 += [x1, y1]
		if True:
			break

	lst2 = []
	for i in cursor.execute("SELECT x, y FROM Users WHERE user_id = {}".format(user_id2)):
		x2 = i[0]
		y2 = i[1]
		lst2 += [x2, y2]
		if True:
			break
	x1 = lst1[0]
	x2 = lst2[0]
	y1 = lst1[1]
	y2 = lst2[1]
	l = haversine((x1, y1), (x2, y2))
	return round(l, 2)


def get_users_count():
	return len(cursor.execute("SELECT user_id FROM Users").fetchall())

# Получение пустого события
def get_empty_event(user_id):
	lst = []
	for i in cursor.execute("SELECT id FROM Event WHERE creator_id = {} AND place = 'None'".format(user_id)):
		lst.append(i[0])
		return lst[0]
	return None


def get_event(id):
	d = None
	for i in cursor.execute("SELECT id, dt, description, woman_pay, man_pay, place, creator_id, name FROM Event WHERE id = {}". format(id)):
		d = {}
		d["id"] = i[0]
		d["date"] = i[1]
		d["description"] = i[2]
		d["woman_pay"] = i[3]
		d["man_pay"] = i[4]
		d["place"] = i[5]
		d['creator_id'] = i[6]
		d['title'] = i[7]
		break
	d.update(get_secondary_info(id))
	return d



def can_skip(user_id):
	for i in cursor.execute("SELECT place FROM Event WHERE creator_id = {}".format(user_id)):
		if i[0] == "":
			return False
		else:
			return True


# Удаление мероприятия
def event_delete(id):
	cursor.execute("DELETE FROM Event WHERE id = {}".format(id))
	conn.commit()


# Повышение прав до организатора
def add_qiwi(user_id, qiwi):
	cursor.execute("INSERT INTO Creater(user_id, qiwi) VALUES ({}, '{}')".format(user_id, qiwi))
	conn.commit()


def get_qiwi(user_id):
	for i in cursor.execute("SELECT qiwi FROM Creater WHERE user_id = {}".format(user_id)):
		return i[0]
	return None


def edit_qiwi(user_id):
	cursor.execute("DELETE FROM Creater WHERE user_id = {}".format(user_id))
	conn.commit()

def is_creator(user_id, event_id):
	for i in cursor.execute("SELECT place FROM Event WHERE creator_id = {} AND id = {}".format(user_id, event_id)):
		return True
	return False



# Создание мероприятия
def event_create(user_id):
	cursor.execute("""
		INSERT INTO Event(name, dt, description, woman_pay, man_pay, creator_id, place) 
		VALUES ('None', 'None', 'None', 0, 0, {}, 'None')
		""".format(user_id))
	conn.commit()
	return get_empty_event(user_id)


# Редактирование мероприятия / создание
def event_name_edit(id, name):
	cursor.execute("UPDATE Event SET name = '{}' WHERE id = {}".format(name, id))
	conn.commit()


def event_description_edit(id, description):
	cursor.execute("UPDATE Event SET description = '{}' WHERE id = {}".format(description, id))
	conn.commit()


def event_man_pay_edit(id, man_pay):
	cursor.execute("UPDATE Event SET man_pay = {} WHERE id = {}".format(man_pay, id))
	conn.commit()


def event_woman_pay_edit(id, woman_pay):
	cursor.execute("UPDATE Event SET woman_pay = {} WHERE id = {}".format(woman_pay, id))
	conn.commit()



def event_dt_edit(id, dt):
	cursor.execute("UPDATE Event SET dt = '{}' WHERE id = {}".format(dt, id))
	conn.commit()


def event_place_edit(id, place):
	cursor.execute("UPDATE Event SET place = '{}' WHERE id = {}".format(place, id))
	conn.commit()


def can_create_event(user_id):
	a = False
	for i in cursor.execute("SELECT qiwi FROM Creater WHERE user_id = {}". format(user_id)):
		a = True
		break
	lst = []
	for i in cursor.execute("SELECT id FROM Event WHERE creator_id = {}". format(user_id)):
		lst.append(i[0])
	if len(lst) < 3 and a:
		return True
	else:
		return False


def get_my_events(user_id):
	lst = []
	for i in cursor.execute("SELECT id, dt, description, woman_pay, man_pay, place, name FROM Event WHERE creator_id = {}".format(user_id)):
		d = {}
		d["id"] = i[0]
		d["date"] = i[1]
		d["description"] = i[2]
		d["woman_pay"] = i[3]
		d["man_pay"] = i[4]
		d["place"] = i[5]
		d['title'] = i[6]
		lst.append(d)
	return lst


def get_event_inside(user_id):
	lst = []
	for i in cursor.execute("SELECT event_id, status FROM Event_History WHERE user_id = {}".format(user_id)):
		if i[1] == 1:
			lst.append(i[0])
	return lst


def get_members(event_id, user_id):
	lst = []
	for i in cursor.execute("SELECT user_id FROM Event_History WHERE event_id = {} AND user_id != {}".format(event_id, user_id)):
		lst.append(i[0])
	return lst


def raise_up_event(id, amount):
	cash = None
	for i in cursor.execute("SELECT cash FROM Event WHERE id = {}". format(id)):
		cash = float(i[0])
		break
	all_cash = round(cash + amount, 2)
	cursor.execute("UPDATE Event SET cash = {}".format(all_cash))
	conn.commit()


def event_status(event_id, user_id, status):
	a = False
	for i in cursor.execute("SELECT id FROM Event_History WHERE user_id = {} AND event_id = {}".format(user_id, event_id)):
		a = True
	if a:
		cursor.execute("UPDATE Event_History SET status = {} WHERE user_id = {} AND event_id = {}".format(status, user_id, event_id))
	else:
		cursor.execute("INSERT INTO Event_History(user_id, event_id, status) VALUES ({}, {}, {})".format(user_id, event_id, status))
	conn.commit()


# Оплата по киви 
def get_comment():
	for i in cursor.execute("SELECT comment FROM Comment"):
		a = i[0] + 1
		break
	cursor.execute("UPDATE Comment SET comment = {}".format(a))
	conn.commit()
	return a


#Сгенерировать ленту
def get_tape(user_id):
	lst = []
	info = get_info(user_id)
	location = info["location"]
	x = info["x"]
	y = info["y"]
	lst = []
	for i in cursor.execute("SELECT user_id, cash, x, y, name FROM Users WHERE x != 0 AND y != 0"):
		if haversine((x, y), (i[2], i[3])) < RADIUS:
			lst.append(i[0])
	events = []
	for user in lst:
		for i in cursor.execute("SELECT id, cash, dt FROM Event WHERE creator_id = {}".format(user, user)):
			year = int(i[2][:4])
			month = int(i[2][5:7])
			day = int(i[2][8:10]) 
			hour = int(i[2][11:13])
			minute = int(i[2][14:16])
			if datetime(year, month, day, hour=hour, minute=minute) > datetime.now():
				boolen = False
				events.append([i[0], i[1]])
	my_events = {}
	for i in cursor.execute("SELECT status, event_id FROM Event_History WHERE user_id = {}".format(user_id)):
		my_events[i[1]] = i[0]
	events = list(map(lambda x: x[0], sorted(events, key=lambda l: l[1])))
	d = {}
	for j in cursor.execute("SELECT id FROM Event WHERE creator_id = {}".format(user_id)):
		d[j[0]] = 1
	for i in events:
		try:
			if my_events[i] != 1:
				d[i] = my_events[i]
		except KeyError:
			d[i] = -1
	if d:
		return d
	return None


# Клуб
def get_club(user_id):
	for i in cursor.execute("SELECT name FROM Club WHERE user_id = {}".format(user_id)):
		return i[0]
	return False



def get_clubs(user_id):
	clubs = []
	for i in cursor.execute("SELECT user_id FROM Club_History WHERE follower_id = {}".format(user_id)):
		clubs.append(i[0])
	return clubs


def club_name_edit(user_id, name):
	if get_club(user_id):
		cursor.execute("UPDATE Club SET name = '{}' WHERE user_id = {}".format(name, user_id))
	else:
		cursor.execute("INSERT INTO Club(user_id, name) VALUES ({}, '{}')".format(user_id, name))
	conn.commit()


def club_description_edit(user_id, description):
	boolen = False
	for i in cursor.execute("SELECT description FROM Club WHERE user_id = {}".format(user_id)):
		boolen = True
	if boolen:
		cursor.execute("UPDATE Club SET description = '{}' WHERE user_id = {}".format(description, user_id))
	else:
		cursor.execute("INSERT INTO Club(user_id, description) VALUES ({}, '{}')".format(user_id, description))
	conn.commit()


def get_club_info(user_id):
	name = None
	description = None
	info = {}
	for i in cursor.execute("SELECT name, description FROM Club WHERE user_id = {}".format(user_id)):
		info["title"] = i[0]
		info["creator_id"] = user_id
		info["description"] = i[1]
		break
	j = 0
	info['man'] = 0
	info['woman'] = 0
	for i in cursor.execute("SELECT follower_id FROM Club_History WHERE user_id = {}".format(user_id)):
		for j in cursor.execute("SELECT gender FROM Users WHERE user_id = {}".format(i[0])):
			if j[0] == 'Парень':
				info['man'] += 1
			elif j[0] == 'Девушка':
				info['woman'] += 1
	info["event_count"] = 0
	for i in cursor.execute("SELECT id FROM Event WHERE creator_id = {}".format(user_id)):
		info["event_count"] += 1
	return info


def come_to_club(user_id, club_id):
	cursor.execute("INSERT INTO Club_History(user_id, follower_id) SELECT {}, {} WHERE NOT EXISTS(SELECT 1 FROM Club_History WHERE follower_id = {} AND user_id = {})".format(club_id, user_id, user_id, club_id))
	conn.commit()


def get_club_events(club_id, user_id):
	lst = []
	for i in cursor.execute("SELECT id FROM Event WHERE creator_id = {}".format(club_id)):
		lst.append(i[0])
	events = {}
	for event_id in lst:
		events[event_id] = -1
		for i in cursor.execute("SELECT status FROM Event_History WHERE user_id = {} AND event_id = {}".format(user_id, event_id)):
			events[event_id] = i[0]
	return events


def exit_from_club(user_id, club_id):
	cursor.execute("DELETE FROM Club_History WHERE follower_id = {} AND user_id = {}".format(user_id, club_id))
	conn.commit()


def delete_club(user_id):
	cursor.execute("DELETE FROM Club WHERE user_id = {}".format(user_id))
	lst = []
	for i in cursor.execute("SELECT follower_id FROM Club_History WHERE user_id = {}".format(user_id)):
		lst.append(i[0])
	for i in lst:
		cursor.execute("DELETE FROM Club_History WHERE follower_id = {}".format(i))
	conn.commit()








#Временная бд
def update_tempory(user_id, value, value_name):
	default_card = "raise_up"
	temp_cursor.execute("""
					  INSERT INTO Users(user_id, card) 
					  SELECT {}, '{}' WHERE NOT EXISTS(SELECT 1 FROM Users WHERE user_id = {})
				   """.format(user_id, default_card, user_id))
	temp_conn.commit()
	if value_name == 'card':
		temp_cursor.execute("UPDATE Users SET card = '{}' WHERE user_id = {}".format(value, user_id))
	elif value_name == 'event_id':
		temp_cursor.execute("UPDATE Users SET event_id = {} WHERE user_id = {}".format(value, user_id))
	temp_conn.commit()


def get_tempory_value(user_id, value_name):
	default_card = "raise_up"
	temp_cursor.execute("""
					  INSERT INTO Users(user_id, card) 
					  SELECT {}, '{}' WHERE NOT EXISTS(SELECT 1 FROM Users WHERE user_id = {})
				   """.format(user_id, default_card, user_id))
	temp_conn.commit()
	for i in temp_cursor.execute("SELECT {} FROM Users WHERE user_id = {}".format(value_name, user_id)):
		return i[0]
	return None


# УТИЛИТЫ 
def get_secondary_info(id):
	d = {"uncorrupted": 0, "man": 0, "woman": 0}
	for i in cursor.execute("SELECT user_id, status FROM Event_History WHERE event_id = {}".format(id)):
		if i[1] != 1:
			d['uncorrupted'] += 1
		else:
			for j in cursor.execute("SELECT gender FROM Users WHERE user_id = {}".format(i[0])):
				if j[0] == 'Парень':
					d['man'] += 1
				elif j[0] == 'Девушка':
					d['woman'] += 1
	return d


def add_user_by_username(user_id, s):
	s = s.replace("@", '')
	a = True
	for i in cursor.execute("SELECT user_id FROM Users WHERE username = '{}'".format(s)):
		a = False
		user_id_ = i[0]
	if a:
		return "Пользователь не найден"
	a = True
	for i in cursor.execute("SELECT user_id FROM Club_History WHERE follower_id = {} AND user_id = {}".format(user_id_, user_id)):
		a = False
	if a:
		come_to_club(user_id_, user_id)
		return "Пользователь успешно добавлен"
	else:
		return 'Пользователь не может быть добавлен'


def add_user_by_id(user_id, s):
	a = True
	for i in cursor.execute("SELECT user_id FROM Users WHERE user_id = {}".format(s)):
		a = False
	if a:
		return "Пользователь не найден"
	a = True
	for i in cursor.execute("SELECT user_id FROM Club_History WHERE follower_id = {} AND user_id = {}".format(s, user_id)):
		a = False
	if a:
		come_to_club(s, user_id)
		return "Пользователь успешно добавлен"
	else:
		return 'Пользователь не может быть добавлен'


def withdraw(id, cash):
	cursor.execute("INSERT INTO Withdraw(user_id, cash) SELECT {}, {}".format(id, cash))
	conn.commit()
	return get_withdraw(id)['id']


def get_withdraw(id):
	for i in cursor.execute("SELECT id, user_id, cash FROM Withdraw WHERE user_id = {}".format(id)):
		d = {}
		d["id"] = i[0]
		d['user_id'] = i[1]
		d['cash'] = i[2]
		return d
	return None


def del_withdraw(id):
	cursor.execute("DELETE FROM Withdraw WHERE user_id = {}".format(id))
	conn.commit()


def new_increase():
	count = get_users_count()
	last = cursor.execute("SELECT now FROM Increse_History").fetchall()[-1][0]
	cursor.execute(f"INSERT INTO Increse_History(now, increase) VALUES ({count}, {count - last})")
	conn.commit()
	return count - last


def cout_blocked():
	return len(cursor.execute("SELECT user_id FROM Users WHERE is_blocked = 1").fetchall())


def count_unblocked():
	return len(cursor.execute("SELECT user_id FROM Users WHERE is_blocked = 0").fetchall())


def get_statistic():
	increase = new_increase()
	blocked = cout_blocked()
	unblocked = count_unblocked()
	man = 0
	woman = 0
	for i in cursor.execute("SELECT gender FROM Users"):
		if i[0] == 'Парень':
			man += 1
		elif i[0] == 'Девушка':
			woman += 1
	s = "Количество пользователей: {}\n".format(get_users_count())
	s += "Прирост с прошлой статистики: {}\n".format(increase)
	s += 'Женщин: {}\n'.format(woman)
	s += "Мужчин: {}\n".format(man)
	s += "Заблокированных: {}\n".format(blocked)
	s += "Незаблокированных: {}\n".format(unblocked)
	return s



def new_status_(user_id, partner_id, status):
	cursor.execute("INSERT INTO History(user_id, partner_id, status) VALUES ({}, {}, {})".format(user_id, partner_id, status))
	conn.commit()



def get_status(user_id1, user_id2):
	for i in cursor.execute('SELECT status FROM History WHERE user_id = {} AND partner_id = {}'.format(user_id1, user_id2)):
		return i[0]
	return None