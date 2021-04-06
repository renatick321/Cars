import requests


API_KEY = "9877666e97772bdd580d6bf60a65aabc"

# FOR TESTS
VIN = "XWFPF2DC1C0018349"
LINK = "ek5qRStrekU0RTNOV216Z3BHQzV0M0lGQTNCckJ4WXp1VUdlQ1VTeHlQMUU2RVJWVVBYN3JPdnIwWmlVSnFONQ=="
SSD = "81ecacee4994a8de3cea2d170b27d285:8875b8c78a3c5168784657637c55cfb3"


def get_link(vin):
	r = requests.get(f"https://api.levam.ru/oem/v1/VinFind?api_key={API_KEY}&vin={vin}")
	return r.json()['models'][0]['link']

def tree_get(link):
	r = requests.get(f"https://api.levam.ru/oem/v1/TreeGet?api_key={API_KEY}&link={link}&lang=ru")
	return r.json()['tree']


def get_ssd(link):
	r = requests.get(f"https://api.levam.ru/oem/v1/TreeGet?api_key={API_KEY}&link={link}&lang=ru")
	return r.json()["client"]['ssd']


def get_names(data, path=''):
	if path != '':
		l = list(map(str, path.split(":")))
		while l:
			one = l.pop(0)
			data = data[one]['data']
	d = {}
	for i in data:
		print(i)
		d[i] = data[i]['name']
	return d

def get_named_path(data, path):
	l = list(map(str, path.split(":")))
	lst = []
	while l:
		one = l.pop(0)
		lst.append(data[one]['name'])
		data = data[one]['data']
	return "->".join(lst)

def get_node(link, ssd, path):
	url = f"https://api.levam.ru/oem/v1/TreeNodeSearch?api_key={API_KEY}&link={link}&&ssd={ssd}&path={path}&lang=ru"
	try:
		data = requests.get(url).json()['tree']
	except KeyError:
		return requests.get(url).json()['error']
	return data

def get_parts(group, ssd, link):
	url = f"https://api.levam.ru/oem/v1/TreeNodePartsGet?api_key={API_KEY}&link={link}&ssd={ssd}&group={group}&lang=ru"
	return requests.get(url).json()


# Шаблонизатор
def catalogslistget(num):
	url = f'https://api.levam.ru/oem/v1/CatalogsListGet?api_key={API_KEY}&type={num}'
	d = {}
	for i in requests.get(url).json()['catalogs']:
		d[i['name']] = i['code']
	return d

def get_family_tree(catalog_code):
	url = f'https://api.levam.ru/oem/v1/ModelsListGet2?api_key={API_KEY}&catalog_code={catalog_code}&type='
	return requests.get(url).json()['families']

def get_family_names(data):
	lst = []
	for i in data.keys():
		lst.append(data[i]['family_name'])
	return lst

def get_model_names(data, family):
	lst = []
	for i in data.keys():
		if data[i]['family_name'] == family:
			for j in data[i]['models']:
				lst.append(j['model'])
	return lst

def vehicle(family, model, catalog_code):
	url = f"https://api.levam.ru/oem/v1/VehicleParamsSet?api_key={API_KEY}&catalog_code={catalog_code}&model={model}&ssd=&family={family}"
	ssd = requests.get(url).json()['client']['ssd']
	return ssd

def get_modifications(ssd):
	url = f"https://api.levam.ru/oem/v1/VehicleModificationsGet?api_key={API_KEY}&ssd={ssd}"
	return requests.get(url).json()['modifications']