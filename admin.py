from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
import sqlite3 as sq

filename = "option.txt"
with open(filename, 'r') as file:
    for line in file:
        if 'admin_id' in line:
            admin_id = line.split('=')[1].strip().strip('"')
admin_id = int(admin_id)



from index import dp  # Импорт dp из основного файла
from aiogram import executor

from aiogram.dispatcher.filters.state import StatesGroup, State

async def admin_panel(message: types.Message):
    # Проверяем, является ли пользователь администратором
    if message.from_user.id == admin_id:  # Замените ADMIN_USER_ID на фактический ID администратора
        db = sq.connect('new.db')
        cur = db.cursor()
        await message.answer("Добро пожаловать в админ-панель!")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)  # Создаем экземпляр клавиатуры
        number_button1 = types.KeyboardButton('Все прокси')
        number_button2 = types.KeyboardButton('Все промокоды')
        number_button3 = types.KeyboardButton('Мои данные')
        number_button3 = types.KeyboardButton('Установите ограничения прокси')
        proxy_button1 = types.KeyboardButton("Добавить прокси")
        promo_button2 = types.KeyboardButton("Добавить промокод")
        Delproxy_button3 = types.KeyboardButton("Удалить прокси")
        Delproxy_button4 = types.KeyboardButton("Удалить промокод")
        allusers_button4 = types.KeyboardButton("Все пользователи")
        DelNumber = types.KeyboardButton("Удалить номер")
        markup.add(number_button1, number_button2, proxy_button1, promo_button2, Delproxy_button3, Delproxy_button4, number_button3, DelNumber, allusers_button4)  # Добавляем кнопку на клавиатуру
        await message.answer("Выберите опцию:", reply_markup=markup)
        # Вывод всех пользователей
        all_users = cur.execute("SELECT user_id,  number, proxy_1, proxy_2, proxy_3, promo, username FROM profile").fetchall()
        if all_users:
            user_list = "\n".join([f"Имя: {row[6]}\nid: {row[0]}\nНомер: {row[1]}\nПрокси: {row[2]}, {row[3]}, {row[4]}\nПромокод: {row[5]}\n{ '-' * 55}\n" for row in all_users])
            await message.answer(f"Список пользователей и их доступа к прокси:\n{user_list}")
        else:
            await message.answer("В базе данных отсутствуют пользователи.")
    else:
        await message.answer("Недостаточно прав для доступа в админ-панель!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
