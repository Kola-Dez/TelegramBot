import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import sqlite3 as sq

# Инициализация подключения к базе данных SQLite
async def db_start():
    global db, cur
    db = sq.connect('new.db')
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, number TEXT, proxy_1 TEXT, proxy_2 TEXT, proxy_3 TEXT, promo TEXT, username TEXT, activation_id TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS proxys(id INTEGER PRIMARY KEY AUTOINCREMENT, proxy TEXT, state TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS promocodes(id INTEGER PRIMARY KEY AUTOINCREMENT, promo TEXT, state TEXT)")

def create_profile(user_id, username):
    user = cur.execute("SELECT 1 FROM profile WHERE user_id = ?", (user_id,)).fetchone()
    if not user:
        cur.execute("INSERT INTO profile VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (user_id, '', 'Открыто', 'Открыто', 'Открыто', '', username, ''))
        db.commit()


def edit_number(state, activation_id, user_id):
    cur.execute("UPDATE profile SET number = ?, activation_id = ? WHERE user_id = ?", (state, activation_id, user_id))
    db.commit()
    
def DeliteNumber(number):
    what = cur.execute("SELECT 1 FROM profile WHERE number = ?", (number,)).fetchone()
    if what != None:
        cur.execute("UPDATE profile SET number = ? WHERE number = ?", ('', number,))
        db.commit()
    else:
        return "error"

action = 0

def edit_proxy(proxy):
    cur.execute("INSERT INTO proxys (proxy, state) VALUES (?, ?)", (proxy, action))
    db.commit()

def edit_promo(promo):
    cur.execute("INSERT INTO promocodes (promo, state) VALUES (?, ?)", (promo, action))
    db.commit()

async def get_all_proxies(message: types.Message):
    proxies = cur.execute("SELECT proxy FROM proxys").fetchall()
    if proxies:
        proxy_list = "\nProxy: ".join([row[0] for row in proxies])
        await message.answer(f"Список прокси:\nProxy: {proxy_list}")
    else:
        await message.answer("В базе данных отсутствуют прокси.")

def delete_proxy(proxy):
    what = cur.execute("SELECT 1 FROM proxys WHERE proxy = ?", (proxy,)).fetchone()
    if what != None:
        cur.execute("DELETE FROM proxys WHERE proxy = ?", (proxy,))
        db.commit()
    else:
        return "error"

def delete_proxy1(proxy):
    cur.execute("DELETE FROM proxys WHERE proxy = ?", (proxy,))
    db.commit()


async def get_all_promo(message: types.Message):
    promocodes = cur.execute("SELECT promo FROM promocodes").fetchall()
    if promocodes:
        promo_list = "\nPromo: ".join([row[0] for row in promocodes])
        await message.answer(f"Список промокодов:\nPromo: {promo_list}")
    else:
        await message.answer("В базе данных отсутствуют промокоды.")

def delete_promo(promo):
    what = cur.execute("SELECT 1 FROM promocodes WHERE promo = ?", (promo,)).fetchone()
    if what != None:
        cur.execute("DELETE FROM promocodes WHERE promo = ?", (promo,))
        db.commit()
    else:
        return "error"

def profiles(user_id):
    profile = cur.execute("SELECT * FROM profile WHERE user_id = ?", (user_id,)).fetchone()
    return profile

def prox1(user_id):
    cur.execute("UPDATE profile SET proxy_1 = ?, proxy_2 = ?, proxy_3 = ? WHERE user_id = ?", ('Открыто', 'Заблокированно', 'Заблокированно', user_id))
    db.commit()

def prox2(user_id):
    cur.execute("UPDATE profile SET proxy_1 = ?, proxy_2 = ?, proxy_3 = ? WHERE user_id = ?", ('Открыто', 'Открыто', 'Заблокированно', user_id))
    db.commit()
    
def prox3(user_id):
    cur.execute("UPDATE profile SET proxy_1 = ?, proxy_2 = ?, proxy_3 = ? WHERE user_id = ?", ('Открыто', 'Открыто', 'Открыто', user_id))
    db.commit()
    
def whatActivation_id(user_id):
    activation_id = cur.execute("SELECT activation_id FROM profile WHERE user_id = ?", (user_id,)).fetchone()
    db.commit()
    return activation_id[0]