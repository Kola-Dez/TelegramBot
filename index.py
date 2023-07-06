import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from sqlite import edit_proxy, edit_promo, DeliteNumber, whatActivation_id
import sqlite3 as sq
import json

filename = "option.txt"
with open(filename, 'r') as file:
    for line in file:
        if 'admin_id' in line:
            admin_id = line.split('=')[1].strip()
        elif 'API_KEY' in line:
            API_KEY = line.split('=')[1].strip().split()

admin_id = int(admin_id)
API_KEY = API_KEY[0]
print("admin_id =", admin_id)
print("API_KEY =", API_KEY)


from smsactivate.api import SMSActivateAPI
sa = SMSActivateAPI(API_KEY)

import random
from sqlite import db_start, create_profile, edit_number, get_all_proxies, delete_proxy, get_all_promo, delete_promo, profiles, prox1, prox2, delete_proxy1, prox3
async def on_startup(_):
    await db_start()


# Здесь необходимо вставить токен вашего бота
bot_token = '6187905230:AAEhtWIO4J2LE3CvmVCivOF40TX73c_sP2k'

# Инициализация бота и диспетчера
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

class SomeState(StatesGroup):
    Proxy = State()
    Promo = State()
    ProxyDelete = State()
    PromoDelete = State()
    SET_PROXY_ACCESS = State()
    Ogranich1 = State()
    Ogranich2 = State()
    Ogranich3 = State()
    DelNumber = State()



# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    profile = profiles(user_id)
    create_profile(user_id, username)
    user_id = message.from_user.id
    profile = profiles(user_id)
    if profile:
        if profile[3] == 'Открыто' and profile[4] != 'Открыто':
            await message.answer(f"👤Пользователь: {message.from_user.username}\n📳Номер: {profile[1]}\nПромокод: {profile[2]}\n🌐Прокси: {profile[3]}\n⭕Промокод: {profile[5]}")
        elif profile[4] == 'Открыто':
            await message.answer(f"👤Пользователь: {message.from_user.username}\n📳Номер: {profile[1]}\n🌐Прокси: {profile[2]}\n🌐Прокси: {profile[3]}\n🌐Прокси: {profile[4]}\n⭕Промокод: {profile[5]}")
        else:
            await message.answer(f"👤Пользователь: {message.from_user.username}\n📳Номер: {profile[1]}\n🌐Прокси: {profile[2]}\n⭕Промокод: {profile[5]}")
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        Kode_button = types.KeyboardButton("КОД активации")
        Numb_button = types.KeyboardButton("Взять номер")
        proxy_button = types.KeyboardButton(text="Взять прокси")
        promo_button = types.KeyboardButton(text="Взять промокод")
        Home_button = types.KeyboardButton(text="Мои данные")
        keyboard.add(Numb_button, Kode_button, proxy_button, promo_button, Home_button)
        await message.answer("⭐Добро пожаловать⭐\nВыберите опцию:", reply_markup=keyboard)
    else:
        await message.answer("⚠️У вас нет данных в профиле.⚠️")

# Обработчик нажатия на кнопку "Выдать номер"
@dp.message_handler(lambda message: message.text == 'Взять номер')
async def handle_profile_button(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    profile = profiles(user_id)
    if profile and profile[1]:  # Если у пользователя уже есть номер в категории worker
        await message.answer("⚠️У вас уже есть номер.⚠️")
    else:
        number = sa.getNumber(service='lf', country=11, freePrice ="true")
        try:
            edit_number(number['phone'], number['activation_id'], message.from_user.id)
            await message.answer(f"Ваш номер: {number['phone']}")
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            Kode_button = types.KeyboardButton("КОД активации")
            Numb_button = types.KeyboardButton("Взять номер")
            proxy_button = types.KeyboardButton(text="Взять прокси")
            promo_button = types.KeyboardButton(text="Взять промокод")
            Home_button = types.KeyboardButton(text="Мои данные")
            keyboard.add(Numb_button, Kode_button, proxy_button, promo_button, Home_button)
            await message.answer("Выберите опцию:", reply_markup=keyboard)
        except:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            Kode_button = types.KeyboardButton("КОД активации")
            Numb_button = types.KeyboardButton("Взять номер")
            proxy_button = types.KeyboardButton(text="Взять прокси")
            promo_button = types.KeyboardButton(text="Взять промокод")
            Home_button = types.KeyboardButton(text="Мои данные")
            keyboard.add(Numb_button, Kode_button, proxy_button, promo_button, Home_button)
            # print(number['message'])
            await message.answer(f"⚠️ Oшибка ⚠️", reply_markup=keyboard)



# Обработчик нажатия на кнопку "Мои данные2"
@dp.message_handler(lambda message: message.text == 'Мои данные')
async def handle_profile_button(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    profile = profiles(user_id)
    if profile:
        if profile[3] == 'Открыто' and profile[4] != 'Открыто':
            await message.answer(f"👤Пользователь: {message.from_user.username}\n📳Номер: {profile[1]}\n🌐Прокси: {profile[2]}\n🌐Прокси: {profile[3]}\n⭕Промокод: {profile[5]}")
        elif profile[4] == 'Открыто':
            await message.answer(f"👤Пользователь: {message.from_user.username}\n📳Номер: {profile[1]}\n🌐Прокси: {profile[2]}\n🌐Прокси: {profile[3]}\n🌐Прокси: {profile[4]}\n⭕Промокод: {profile[5]}")
        else:
            await message.answer(f"👤Пользователь: {message.from_user.username}\n📳Номер: {profile[1]}\n🌐Прокси: {profile[2]}\n⭕Промокод: {profile[5]}")
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        Kode_button = types.KeyboardButton("КОД активации")
        Numb_button = types.KeyboardButton("Взять номер")
        proxy_button = types.KeyboardButton(text="Взять прокси")
        promo_button = types.KeyboardButton(text="Взять промокод")
        Home_button = types.KeyboardButton(text="Мои данные")
        keyboard.add(Numb_button, Kode_button, proxy_button, promo_button, Home_button)
        await message.answer("Выберите опцию:", reply_markup=keyboard)
    else:
        await message.answer("⚠️У вас нет данных в профиле.⚠️")

#TEKE KEY    
@dp.message_handler(lambda message: message.text == 'КОД активации')
async def handle_profile_button(message: types.Message, state: FSMContext):
    activation_id = whatActivation_id(message.from_user.id)
    status = sa.getStatus(activation_id) # STATUS_WAIT_CODE
    if status == 'STATUS_WAIT_CODE':
        await message.answer("Oжидание смс")# {'status': 'STATUS_WAIT_CODE', 'message': 'Ожидание смс'}
    elif status == 'STATUS_OK':
        activations = sa.getActiveActivations()
        try:
            sorted_activations = sorted(activations["activeActivations"], key=lambda x: x["activationId"] == activation_id, reverse=True)
            for activation in sorted_activations:
                if activation['activationId'] == activation_id:
                    await message.answer(f"Ваш код: {activation['smsCode']}")
        except:
            await message.answer(f"Ваш код: {activations['error']}")
    else:
        await message.answer(f"Код: {status}")
        
        



#TEKE PROXY
@dp.message_handler(lambda message: message.text == 'Взять прокси')
async def handle_profile_button(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    profile = profiles(user_id)
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    proxy_button_1 = types.InlineKeyboardButton(text="Прокси 1", callback_data="TakeProxyField_1")
    
    if profile[3] == 'Открыто' and profile[4] != 'Открыто':
        proxy_button_2 = types.InlineKeyboardButton(text="Прокси 2", callback_data="TakeProxyField_2")
        keyboard.add(proxy_button_1, proxy_button_2)
    elif profile[4] == 'Открыто':
        proxy_button_3 = types.InlineKeyboardButton(text="Прокси 3", callback_data="TakeProxyField_3")
        proxy_button_2 = types.InlineKeyboardButton(text="Прокси 2", callback_data="TakeProxyField_2")
        keyboard.add(proxy_button_1, proxy_button_2, proxy_button_3)
    else:
        keyboard.add(proxy_button_1)
    
    await message.answer("Выберите поле для прокси:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith("TakeProxyField_"))
async def process_proxy_field(callback_query: types.CallbackQuery):
    db = sq.connect('new.db')
    cur = db.cursor()
    user_id = callback_query.from_user.id
    proxy_field = int(callback_query.data.split("_")[1])  # Получаем номер выбранного поля
    profile = profiles(user_id)
    if profile[proxy_field + 1] == 0:  # Проверка наличия прокси в выбранном поле профиля пользователя
        await callback_query.answer("⚠️Нельзя⚠️")
    else:
        proxy = cur.execute("SELECT proxy FROM proxys WHERE state = 0 LIMIT 1").fetchone()
        if proxy:
            proxy_value = proxy[0]
            cur.execute(f"UPDATE profile SET proxy_{proxy_field} = ? WHERE user_id = ?", (proxy_value, user_id))
            cur.execute("UPDATE proxys SET state = 1 WHERE proxy = ?", (proxy_value,))
            db.commit()
            await callback_query.answer(f"Взят прокси: {proxy_value} (Поле: {proxy_field})")
        else:
            await callback_query.answer("Нет доступных прокси.")


#TEKE PROMO
@dp.message_handler(lambda message: message.text == 'Взять промокод')
async def handle_profile_button(message: types.Message, state: FSMContext):
    db = sq.connect('new.db')
    cur = db.cursor()
    user_id = message.from_user.id
    profile = profiles(user_id)
    if profile[5]:  # Проверка наличия промокод в поле promo_1 профиля пользователя
        await message.answer("У вас уже есть промокод.")
    else:
        promo = cur.execute("SELECT promo FROM promocodes WHERE state = 0 LIMIT 1").fetchone()
        if promo:
            promo_value = promo[0]
            cur.execute("UPDATE profile SET promo = ? WHERE user_id = ?", (promo_value, user_id))
            cur.execute("UPDATE promocodes SET state = 1 WHERE promo = ?", (promo_value,))
            db.commit()
            await message.answer(f"Взят промокод: {promo_value}")
        else:
            await message.answer("Нет доступных промокодов.")
        
        
        
        
        
        


        
@dp.message_handler(lambda message: message.text == 'admin')
async def handle_number_button(message: types.Message, state: FSMContext):
    # Регистрируем обработчик команды /admin
    from admin import admin_panel
    await admin_panel(message)
    
    
#admin

#Добавить прокси
@dp.message_handler(lambda message: message.text == 'Добавить прокси')
async def handle_proxies_command(message: types.Message):
    if message.from_user.id == admin_id:
        await message.answer("Введите прокси:")
        await SomeState.Proxy.set()

@dp.message_handler(state=SomeState.Proxy)
async def handle_proxy(message: types.Message, state: FSMContext):
    proxy = message.text
    edit_proxy(proxy)
    await message.answer("Прокси успешно добавлен!")
    await state.finish()  # Завершаем состояние FSM
    
#Добавить промокод
@dp.message_handler(lambda message: message.text == 'Добавить промокод')
async def handle_proxies_command(message: types.Message):
    if message.from_user.id == admin_id:
        await message.answer("Введите промокод:")
        await SomeState.Promo.set()

@dp.message_handler(state=SomeState.Promo)
async def handle_promo(message: types.Message, state: FSMContext):
    promo = message.text
    edit_promo(promo)
    await message.answer("Промокод успешно добавлен!")
    await state.finish()  # Завершаем состояние FSM





    
#ALL proxy
@dp.message_handler(lambda message: message.text == 'Все прокси')
async def handle_proxies_command(message: types.Message):
    if message.from_user.id == admin_id:
        await get_all_proxies(message)

#ALL proxy
@dp.message_handler(lambda message: message.text == 'Все промокоды')
async def handle_proxies_command(message: types.Message):
    if message.from_user.id == admin_id:
        await get_all_promo(message)




#Удаление прокси
@dp.message_handler(lambda message: message.text == 'Удалить прокси')
async def handle_proxies_command(message: types.Message):
    if message.from_user.id == admin_id:
        await message.answer("Введите прокси для удаления:")
        await SomeState.ProxyDelete.set() 

@dp.message_handler(state=SomeState.ProxyDelete)
async def handle_delete_proxy(message: types.Message, state: FSMContext):
    proxy = message.text.strip()  # Удаляем лишние пробелы в начале и конце строки
    if proxy:
        what = delete_proxy(proxy)
        if what == 'error':
            await message.answer(f"Прокси {proxy} не найден.")   
        else:
            await message.answer(f"Прокси {proxy} успешно удален.")
    else:
        await message.answer("⚠️Укажите прокси для удаления.⚠️")
    await state.finish()  # Завершаем состояние FSM


#Удаление промокода 
@dp.message_handler(lambda message: message.text == 'Удалить промокод')
async def handle_proxies_command(message: types.Message):   
    if message.from_user.id == admin_id:
        await message.answer("Введите промокод для удаления:")
        await SomeState.PromoDelete.set()

@dp.message_handler(state=SomeState.PromoDelete)
async def handle_delete_proxy(message: types.Message, state: FSMContext):
    promo = message.text.strip()  # Удаляем лишние пробелы в начале и конце строки
    if promo:
        what = delete_promo(promo)
        if what == 'error':
            await message.answer(f"промокод {promo} не найден.") 
        else:
            await message.answer(f"промокод {promo} успешно удален.")
    else:
        await message.answer("Укажите промокод для удаления.")
    await state.finish()  # Завершаем состояние FSM


#ограничения    
@dp.message_handler(lambda message: message.text == 'Установите ограничения прокси')
async def handle_proxies_command(message: types.Message):   
    if message.from_user.id == admin_id:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        proxy_button = types.KeyboardButton(text="Выдать 1 прокси")
        promo_button = types.KeyboardButton(text="Выдать 2 прокси")
        Home_button = types.KeyboardButton(text="Выдать 3 прокси")
        keyboard.add(proxy_button, promo_button, Home_button)
        await message.answer("Какое ограничение выберите", reply_markup=keyboard)
#1
@dp.message_handler(lambda message: message.text == 'Выдать 1 прокси')
async def handle_proxies_command(message: types.Message):   
    if message.from_user.id == admin_id:
        await message.answer("Введите \"id\" пользователя которому хотите задать ограничение {1 прокси}:")
        await SomeState.Ogranich1.set()
        
@dp.message_handler(state=SomeState.Ogranich1)
async def handle_delete_proxy1(message: types.Message, state: FSMContext):
    db = sq.connect('new.db')
    cur = db.cursor()
    user_id = message.text
    what = cur.execute("SELECT 1 FROM profile WHERE user_id = ?", (user_id,)).fetchone()
    if what != None:
        proxy_1 = cur.execute("SELECT proxy_1 FROM profile WHERE user_id = ?", (user_id,)).fetchone()
        delete_proxy1(proxy_1[0])  # Use proxy_1[0] to get the value from the fetched result
        proxy_2 = cur.execute("SELECT proxy_2 FROM profile WHERE user_id = ?", (user_id,)).fetchone()
        delete_proxy1(proxy_2[0])  # Use proxy_2[0] to get the value from the fetched result
        proxy_3 = cur.execute("SELECT proxy_3 FROM profile WHERE user_id = ?", (user_id,)).fetchone()
        delete_proxy1(proxy_3[0])  # Use proxy_3[0] to get the value from the fetched result
        prox1(user_id)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        proxy_button = types.KeyboardButton(text="admin")
        keyboard.add(proxy_button)
        query = "SELECT user_id, number, proxy_1, proxy_2, proxy_3, promo FROM profile WHERE user_id = ?"
        user_data = cur.execute(query, (user_id,)).fetchone()
        user_list = (f"ID: {user_data[0]}\nНомер: {user_data[1]}\nProxy: {user_data[2]}, {user_data[3]}, {user_data[4]}\nPromo: {user_data[5]}\n{'-' * 55}\n")
        await message.answer(f"Успешно:\n{user_list}", reply_markup=keyboard)
        await state.finish()  # Завершаем состояние FSM
    else:
        await message.answer("⚠️Пользователь не найден⚠️")
    
#2
@dp.message_handler(lambda message: message.text == 'Выдать 2 прокси')
async def handle_proxies_command(message: types.Message):   
    if message.from_user.id == admin_id:
        await message.answer("Введите \"id\" пользователя которому хотите задать ограничение {2 прокси}:")
        await SomeState.Ogranich2.set()
        
@dp.message_handler(state=SomeState.Ogranich2)
async def handle_delete_proxy2(message: types.Message, state: FSMContext):
    db = sq.connect('new.db')
    cur = db.cursor()
    user_id = message.text
    what = cur.execute("SELECT 1 FROM profile WHERE user_id = ?", (user_id,)).fetchone()
    if what != None:
        proxy_1 = cur.execute("SELECT proxy_1 FROM profile WHERE user_id = ?", (user_id,)).fetchone()
        delete_proxy1(proxy_1[0])  # Use proxy_1[0] to get the value from the fetched result
        proxy_2 = cur.execute("SELECT proxy_2 FROM profile WHERE user_id = ?", (user_id,)).fetchone()
        delete_proxy1(proxy_2[0])  # Use proxy_2[0] to get the value from the fetched result
        proxy_3 = cur.execute("SELECT proxy_3 FROM profile WHERE user_id = ?", (user_id,)).fetchone()
        delete_proxy1(proxy_3[0])  # Use proxy_3[0] to get the value from the fetched result
        prox2(user_id)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        proxy_button = types.KeyboardButton(text="admin")
        keyboard.add(proxy_button)
        query = "SELECT user_id, number, proxy_1, proxy_2, proxy_3, promo FROM profile WHERE user_id = ?"
        user_data = cur.execute(query, (user_id,)).fetchone()
        user_list = (f"ID: {user_data[0]}\nНомер: {user_data[1]}\nProxy: {user_data[2]}, {user_data[3]}, {user_data[4]}\nPromo: {user_data[5]}\n{'-' * 55}\n")
        await message.answer(f"Успешно:\n{user_list}", reply_markup=keyboard)
        await state.finish()  # Завершаем состояние FSM
    else:
        await message.answer("⚠️Пользователь не найден⚠️")
    
#3
@dp.message_handler(lambda message: message.text == 'Выдать 3 прокси')
async def handle_proxies_command(message: types.Message):
    if message.from_user.id == admin_id:
        await message.answer("Введите \"id\" пользователя которому хотите задать ограничение {3 прокси}:")
        await SomeState.Ogranich3.set()
        
@dp.message_handler(state=SomeState.Ogranich3)
async def handle_delete_proxy3(message: types.Message, state: FSMContext) -> None:
    db = sq.connect('new.db')
    cur = db.cursor()
    user_id = message.text
    what = cur.execute("SELECT 1 FROM profile WHERE user_id = ?", (user_id,)).fetchone()
    if what is not None:
        proxy_1 = cur.execute("SELECT proxy_1 FROM profile WHERE user_id = ?", (user_id,)).fetchone()
        delete_proxy1(proxy_1[0])  # Use proxy_1[0] to get the value from the fetched result
        proxy_2 = cur.execute("SELECT proxy_2 FROM profile WHERE user_id = ?", (user_id,)).fetchone()
        delete_proxy1(proxy_2[0])  # Use proxy_2[0] to get the value from the fetched result
        proxy_3 = cur.execute("SELECT proxy_3 FROM profile WHERE user_id = ?", (user_id,)).fetchone()
        delete_proxy1(proxy_3[0])  # Use proxy_3[0] to get the value from the fetched result
        prox3(user_id)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        proxy_button = types.KeyboardButton(text="admin")
        keyboard.add(proxy_button)
        user_data = cur.execute("SELECT user_id, number, proxy_1, proxy_2, proxy_3, promo FROM profile WHERE user_id = ?", (user_id,)).fetchone()
        user_list = f"ID: {user_data[0]}\nНомер: {user_data[1]}\nПрокси: {user_data[2]}, {user_data[3]}, {user_data[4]}\nПромокод: {user_data[5]}\n{'-' * 55}\n"
        await message.answer(f"Успешно:\n{user_list}", reply_markup=keyboard)
        await state.finish()  # Завершаем состояние FSM
    else:
        await message.answer("⚠️Пользователь не найден⚠️")



@dp.message_handler(lambda message: message.text == 'Удалить номер')
async def DelNumbers(message: types.Message): 
    if message.from_user.id == admin_id:  
        await message.answer("Введите номер который хотите удалить")
        await SomeState.DelNumber.set()

@dp.message_handler(state=SomeState.DelNumber)
async def handle_delete_proxy3(message: types.Message, state: FSMContext):
    number = message.text
    what = DeliteNumber(number)
    if what == "error":
        await message.answer("⚠️Номер не был найден⚠️")
        await state.finish()  # Завершаем состояние FSM
    else:
        await message.answer("Номер был удален")
        await state.finish()  # Завершаем состояние FSM


@dp.message_handler(lambda message: message.text == 'Все пользователи')
async def handle_proxies_command(message: types.Message):
    if message.from_user.id == admin_id:
        db = sq.connect('new.db')
        cur = db.cursor()
        all_users = cur.execute("SELECT user_id,  number, proxy_1, proxy_2, proxy_3, promo, username FROM profile").fetchall()
        if all_users:
            user_list = "\n".join([f"Имя: {row[6]}\nid: {row[0]}\nНомер: {row[1]}\nПрокси: {row[2]}, {row[3]}, {row[4]}\nПромокод: {row[5]}\n{ '-' * 55}\n" for row in all_users])
            await message.answer(f"Список пользователей и их доступа к прокси:\n{user_list}")
        else:
            await message.answer("⚠️В базе данных отсутствуют пользователи.⚠️")

# Запуск бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)