#подключение библеотек
import sqlite3
import telebot
import pyowm
import random
import sys
import time 
#Гнавная часть бота

bot = telebot.TeleBot('1386594700:AAEO3viFlCnzT4FAQBcrT39FBbTe-TBOnHc')

#Переменные

text = '''
Привет, я бот казино можно сказать бесполезный но щяс
просто тестируюсь.

'''
stadia_st = 0
s_stadia1 = 1
straniza = 0
stadia = 1
stadia_v = 1
user_login = ''
user_password = ''
user_login_vxod = ''
user_password_vxod = ''
vxod = False
coin = None
pog = None
v = None
igra = None
#Узнавание погоды
def yz(pog, idd):
	try:
		owm = pyowm.OWM('2b81034cf1e96c904e721b0da1ad3f9d', language="RU")
		observation = owm.weather_at_place(pog)
		w=observation.get_weather()
		temp = w.get_temperature('celsius'),['temp']
		pogoda = w.get_detailed_status()
		pogoda_k = 'В ' + str(pog) + ' сейчас ' + str(pogoda)
		bot.send_message(idd, pogoda_k, reply_markup=keyboard2)	
	except:
		bot.send_message(idd, 'Незнаю такого места :(')
def nev_ig(idd):
	global igra
	v = random.randint(1, 2)
	i = random.randint(1, 4)
	s = ['Navi vs Virtus Pro', 'Тест команда 1 vs Тест команда 2', 'OG vs Teem Sekret', 'Тест команда 1 vs Тест команда 2', 'Navi vs Ноунеймы']
	igra = s[i]
	bot.send_message(idd, 'Ближайшая игра будет ' + str(igra) + ' что хотите сделать?')
#тексты и иконки бота

button1_k = telebot.types.KeyboardButton('Зарегестрироваться')
button2_k = telebot.types.KeyboardButton('Залогинеться')	
button3_k = telebot.types.KeyboardButton('Вывод бд')
keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.add(button1_k, button2_k, button3_k)

button1_k2 = telebot.types.KeyboardButton('Посмотреть погоду')
button2_k2 = telebot.types.KeyboardButton('Сыграть')	
button3_k2 = telebot.types.KeyboardButton('Выйти с аккаунта')
keyboard2 = telebot.types.ReplyKeyboardMarkup(True)
keyboard2.add(button1_k2, button2_k2, button3_k2)

button1_k3 = telebot.types.KeyboardButton('Поставить')
button2_k3 = telebot.types.KeyboardButton('Воздержаться')	
button3_k3 = telebot.types.KeyboardButton('Назад')
keyboard3 = telebot.types.ReplyKeyboardMarkup(True)
keyboard3.add(button1_k3, button2_k3, button3_k3)
#Основной back-end

@bot.message_handler(commands = ['start'])
def send_welcome(message): 
	global straniza
	if straniza != 1:
		bot.reply_to(message, text, reply_markup=keyboard1)
		bot.send_sticker(message.chat.id, 'CAADAgADsQADWQMDAAEJK1niI56hlhYE')
		straniza = 1
	else:
		bot.send_message(message.chat.id, 'Ты уже перешёл этот лвл')
@bot.message_handler(content_types=['text'])
def send_text(message):
	#Работа с БД
	db = sqlite3.connect('server.db')
	sql = db.cursor() 
	#БД пользователей
	sql.execute("""CREATE TABLE IF NOT EXISTS user (
		login TEXT,
		password TEXT,
		coins INT
)""")
	r = sqlite3.connect('server2.db')
	cur = r.cursor() 
	#БД максимальной регистрации
	cur.execute("""CREATE TABLE IF NOT EXISTS reg (
		id INT,
		registrazii INT
)""")
	#Переменные

	global stadia, user_login, user_password, vxod, stadia_v, reg, user_login_vxod, user_password_vxod, regis, straniza, stadia_st, coin
	id_user = message.chat.id
	idd = message.chat.id
	#Алгоритм регистрации
	if straniza == 0:
		bot.send_message(message.chat.id, 'Для начала введите команду /start')
	if straniza == 1:
		if message.text == 'Зарегестрироваться' and vxod == False:
			cur.execute('''SELECT registrazii FROM reg WHERE id = '{id_user}' ''')
			if cur.fetchone() is None:
				cur.execute('''INSERT INTO reg VALUES (?, ?)''', (id_user, 0))
				r.commit()
			if stadia == 1:
				bot.send_message(message.chat.id, 'Введите логин')
				stadia = 2
		elif stadia == 2:
			user_login = message.text
			bot.send_message(message.chat.id, 'Введите пороль')
			stadia = 3
		elif stadia == 3:
			user_password = message.text
			#Проверки на макс. число аккаунтов и нету ли такого логина уже в БД
			sql.execute(f'''SELECT login FROM user WHERE login = '{user_login}' ''')
			if sql.fetchone() is None:
				sql.execute("INSERT INTO user VALUES (?, ?, ?)", (user_login, user_password, 100))
				cur.execute(f'''SELECT registrazii FROM reg WHERE id = '{id_user}' ''')
				reg = cur.fetchone()
				re = reg[0]
				re += 1
				cur.execute(f'''UPDATE reg SET registrazii = '{re}' WHERE id = '{id_user}' ''')
				#Проверка на макс кол-во аккаунтов
				if re <= 2:
					db.commit()
					r.commit()
					bot.send_message(message.chat.id, 'Пользователь внесён в систему')
				else:
					bot.send_message(message.chat.id, 'У вас максимальное число аккаунтов')
			else:
				bot.send_message(message.chat.id, 'Пользователь с таким логином уже зарегестрирован')
			stadia = 1
		elif vxod == True:
			bot.send_message(message.chat.id, 'Вы уже вошли в аккаунт')
		#Алгоритм вывода базы данных
		if message.text == 'Вывод бд':
			#вывод через цикл
			for value in sql.execute('SELECT * FROM user'):
				print(value)
		#Алгоритм входа в аккаунт
		if message.text == 'Залогинеться' and vxod == False:
			if stadia_v == 1:
				bot.send_message(message.chat.id, 'Введите логин', parse_mode='html')
				stadia_v = 2
		elif stadia_v == 2 and vxod == False:
			user_login_vxod = message.text
			bot.send_message(message.chat.id, 'Введите пороль')
			stadia_v = 3
		elif stadia_v == 3 and vxod == False:
			user_password_vxod = message.text
			stadia_v = 1
			sql.execute(f'''SELECT login FROM user WHERE login = '{user_login_vxod}' ''')
			if sql.fetchone() is None:
				bot.send_message(message.chat.id, 'Такого пользователя нету в базе данных')
			else:
				sql.execute(f'''SELECT password FROM user WHERE login = '{user_login_vxod}' ''')
				if sql.fetchone()[0] == user_password_vxod:
					vxod = True
					bot.send_message(message.chat.id, 'Вы успешно вошли в аккаунт', reply_markup=keyboard2)
					straniza = 2
				else:
					bot.send_message(message.chat.id, 'Неправильный пороль')
	elif straniza == 2:
		global s_stadia1, pog
		if message.text == 'Посмотреть погоду':
			bot.send_message(message.chat.id, 'Введите город')
			s_stadia1 = 2
		elif s_stadia1 == 2:
			pog = message.text
			idd = message.chat.id
			yz(pog, idd)
			s_stadia1 = 1
		if message.text == 'Сыграть':
			bot.send_message(message.chat.id, 'Оу :)', reply_markup = keyboard3)
			nev_ig(idd)
			straniza = 3
		elif message.text == 'Выйти с аккаунта':
			print('f')
			bot.send_message(message.chat.id, 'Хорошо выходим с аккаунта', reply_markup = keyboard1)
			straniza = 1
			vxod = False
	elif straniza == 3:
		if message.text == 'Поставить':
			sql.execute(f'''SELECT coins FROM user WHERE login = '{user_login_vxod}'  ''')
			coin = sql.fetchone()
			bot.send_message(message.chat.id, 'У вас есть:' + str(coin[0]))
			bot.send_message(message.chat.id, 'сколько ставить будете?')
			stadia_st = 1
		elif message.text == 'Назад':
			stadia_st = 0
		elif stadia_st == 1:
			st_coin = message.text
			try:
				C = coin[0] - int(st_coin)
				if C < 0:
					bot.send_message(message.chat.id, 'Извените, но у вас нету столько коинов')
					bot.send_message(message.chat.id, 'У вас есть:' + str(coin[0]))
					stadia_st = 0
				else:
					vr = random.randint(3, 7)
					bot.send_message(message.chat.id, 'Хорошо, теперь только ждите через ' + str(vr) + ' секунд я скажу вам результат пожалуста подождите')
					time.sleep(vr)
					if v == 1:
						VP = coin[0] + int(st_coin)
						bot.send_message(message.chat.id, 'Мои поздравления вы выиграли ^_^')
						sql.execute(f'''UPDATE user SET coins = '{VP}' WHERE login = '{user_login_vxod}' ''')
						db.commit()
						nev_ig()
					else:
						VP = coin[0] + int(st_coin)
						bot.send_message(message.chat.id, 'Эх... Вы проиграли')	
						sql.execute(f'''UPDATE user SET coins = '{VP}' WHERE login = '{user_login_vxod}' ''')
						db.commit()
						nev_ig(idd)	
			except ValueError:
				try:
					try:
						if int(st_coin):
							bot.send_message(message.chat.id, 'Вы ввели не число')
					except ValueError:
						bot.send_message(message.chat.id, 'Вы ввели не число')
				except ValueError:
					bot.send_message(message.chat.id, 'Ждёмс')
		if message.text == 'Воздержаться':
			bot.send_message(message.chat.id, 'Хорошо ищу другую игру')
			time.sleep(1)
			nev_ig(idd)
		if message.text == 'Назад':
			bot.send_message(message.chat.id, 'Окей идём назад', reply_markup = keyboard2)
			straniza = 2

#запуск бота
bot.polling()