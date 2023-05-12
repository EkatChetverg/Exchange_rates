import json
import requests # Модуль для обработки URL
from bs4 import BeautifulSoup # Модуль для работы с HTML


class Currency:

	def __init__(self):
		# Ссылки на сайты
		self.usd_ils = 'https://www.google.com/search?q=usd+to+ils'
		self.usd_rub ='https://www.google.com/search?q=usd+to+rub'
		self.gold_crown = 'https://koronapay.com/transfers/online/api/transfers/tariffs?sendingCountryId=RUS&sendingCurrencyId=810&receivingCountryId=ll_name_country_ll&receivingCurrencyId=840&paymentMethod=debitCard&receivingAmount=100&receivingMethod=cash&paidNotificationEnabled=true'
		self.kursy_mir = 'https://mironline.ru/support/list/kursy_mir/'
		self.kicb = 'https://kicb.net/'
		self.bcs = 'https://bank.bcs.ru/get_courses_update'
		self.ravnak = 'https://ravnaqbank.uz/ru/services/exchange-rates/'
		self.tinkoff = 'https://www.tinkoff.ru/invest/currencies/USDRUB/'
		self.binance = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'

		self.percent_kicb = 1.025
		self.percent_ravnak1 = 1.024
		self.percent_ravnak2 = 0.01
		self.percent_gold_crown = 1.05

		# Заголовки для передачи вместе с URL
		self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

		# Предварительный расчет
		self.official_usd_rub = self.get_currency_price_usd_rub()

	# Преобразуем строку в число
	def str_to_float(self, text):
		try:
			text = text.replace(",", ".")
			new_value = float(text)
		except:
			new_value = -1
		return new_value

	def get_currency_price_usd_rub(self):
		# official_usd_rub_google = self.get_currency_price_google(self.usd_rub)
		official_usd_rub_tinkoff = self.get_currency_price_tinkoff()
		return official_usd_rub_tinkoff

	# Метод для получения курса валюты с переданного сайта
	def get_currency_price_google(self, url_site):
		try:
			full_page = requests.get(url_site, headers=self.headers) # Парсим всю страницу
			soup = BeautifulSoup(full_page.content, 'html.parser') # Разбираем через BeautifulSoup
			course_text = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2}) # Получаем нужное для нас значение и возвращаем его
			course = self.str_to_float(course_text[0].text)
			return course
		except:
			return -1

	# Метод для получения курса валюты с сайта Tinkoff
	def get_currency_price_tinkoff(self):
		try:
			full_page = requests.get(self.tinkoff, headers=self.headers) # Парсим всю страницу
			soup = BeautifulSoup(full_page.content, 'html.parser') # Разбираем через BeautifulSoup
			convert = soup.findAll("div", {"class": "SecurityInvitingScreen__price_FSP8P"})[0]
			course = convert.text.strip()
			course = course[:-2]
			course = self.str_to_float(course)
			return course
		except:
			return -1

	# Метод для получения курса с сайта kursy_mir
	def get_currency_price_kursy_mir(self, received_currency):
		try:
			full_page = requests.get(self.kursy_mir, headers=self.headers)
			soup = BeautifulSoup(full_page.content, 'html.parser')
			table_course = soup.find(class_="sf-text") # Получаем таблицу всех курсов
			result = {}
			all_rows = table_course.findAll('tr') # Преобразуем таблицу HYML в словарь
			for row in all_rows:
				all_cols = row.findAll('td')
				if len(all_cols) == 2:
					result[all_cols[0].text.strip()] = all_cols[1].text.strip()
			return result[received_currency]
		except:
			return -1

	# Метод для получения курса с сайта kicb
	def get_currency_price_kicb(self, list_kicb):
		try:
			full_page = requests.get(self.kicb, headers=self.headers)
			soup = BeautifulSoup(full_page.content, 'html.parser')
			table_course = soup.findAll("div", {"class": "con"}) # Получаем html всех курсов
			for val in table_course:
				calculation_type = val.find(class_="head1").text.strip()
				if calculation_type == "Безналичный":
					list_all = val.findAll("span")

					number_call = 0
					result = {}
					for val2 in list_all:
						number_call += 1
						if number_call == 1:
							name_currency = val2.text.strip()
						if number_call == 2:
							result[f"{name_currency}_buy"] = val2.text.strip()
						if number_call == 3:
							result[f"{name_currency}_sell"] = val2.text.strip()
							number_call = 0
			list_course = {}
			for type_of_activity, received_currency in list_kicb:
				name_course = f"{received_currency}_{type_of_activity}"
				list_course[name_course] = result[name_course]
		except:
			list_course = {}
			for type_of_activity, received_currency in list_kicb:
				name_course = f"{received_currency}_{type_of_activity}"
				list_course[name_course] = -1
		return list_course

	# Метод для получения курса с сайта bcs
	def get_currency_price_bcs(self, type_of_activity, received_currency):
		try:
			full_page = requests.get(self.bcs, headers=self.headers)
			soup = BeautifulSoup(full_page.content, 'html.parser')
			online_courses = json.loads(soup.string)["online_courses"]
			return online_courses[received_currency][type_of_activity]
		except:
			return -1

	# Метод для получения курса с сайта золотой короны
	def ger_currency_price_gold_crown(self, name_country):
		try:
			full_page = requests.get(self.gold_crown.replace('ll_name_country_ll', name_country), headers=self.headers)
			soup = BeautifulSoup(full_page.content, 'html.parser').string
			soup = soup.replace("[", "")
			soup = soup.replace("]", "")
			return json.loads(soup)["exchangeRate"]
		except:
			return -1

	# Метод для получения курсов с сайта Ravnak
	def ger_currency_price_ravnak(self, list_ravnak):
		try:
			full_page = requests.get(self.ravnak, headers=self.headers)
			soup = BeautifulSoup(full_page.content, 'html.parser')
			convert = soup.findAll("div", {"class": "rates-list"})[0]
			list_of_currency = convert.findAll("div", {"class": "item-col item-col-1"})[1].findAll("span")
			list_of_buy = convert.findAll("div", {"class": "item-col item-col-2"})[1].findAll("span")
			list_of_sell = convert.findAll("div", {"class": "item-col item-col-3"})[1].findAll("span")
			result = {}
			for number in range(len(list_of_currency)):
				name_currency = list_of_currency[number].text.strip()
				result[f"{name_currency}_buy"] = list_of_buy[number].text.strip()
				result[f"{name_currency}_sell"] = list_of_sell[number].text.strip()
			list_course = {}
			for type_of_activity, received_currency in list_ravnak:
				name_course = f"{received_currency}_{type_of_activity}"
				list_course[name_course] = result[name_course]
		except:
			list_course = {}
			for type_of_activity, received_currency in list_ravnak:
				name_course = f"{received_currency}_{type_of_activity}"
				list_course[name_course] = -1
		return list_course

	# Метод для расчета переплаты при переводе от официального курса с гугла
	def overpayment(self, value):
		new_value = value * 100 / self.official_usd_rub - 100
		return round(new_value, 2)

	# Метод для получения курса валюты с binance
	def get_currency_price_binance(self):
		try:
			data = {
				"fiat": "RUB",
				"page": 1,
				"rows": 10,
				"tradeType": "buy",
				"asset": "USDT",
				"countries": [],
				"proMerchantAds": False,
				"publisherType": None,
				"payTypes": ["TinkoffNew"]
			}
			response = requests.post(self.binance, headers=self.headers, json=data)
			price = response.json()['data'][0]['adv']['price']
			course = self.str_to_float(price)
			return course
		except:
			return -1

# cur = Currency()
# cur.get_currency_price_binance()