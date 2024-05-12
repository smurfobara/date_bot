from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import logging
from config import admin
import sqlite3
import re 
from datetime import *

c = None

data = None
import keyboards as kb

db = sqlite3.connect('base.db')
c = db.cursor()

router = Router()


class get_data(StatesGroup):
    get_text_data = State()
    to_base = State()
    finish = State()

@router.message(Command('base'))
async def base_test(message: Message, state: FSMContext):
    c.execute("""CREATE TABLE IF NOT EXISTS baseusers (
              name text,
              username text,
              user_id integer,
              date text
    )""")

@router.message(Command('start'))
async def start(message: Message):
    #userIDs_s = []
    #strIDs = ''
    c.execute('SELECT user_id FROM baseusers')
    userIDs = c.fetchall()
    #for item in userIDs:
     #   userIDs_s.append(str(item))
    #for item in userIDs_s:
     #   strIDs = ' '.join(str(item))
    print(userIDs)
    await message.answer('Привет!👋\n Это бот который поможет тебе посчитать дни для какой-нибудь даты, например до дня рождения.', reply_markup=kb.create)
    if str(message.from_user.id) in str(userIDs):
        pass
    else:
        c.execute(f'INSERT INTO baseusers (name, username, user_id) VALUES ("{message.from_user.first_name}", "{message.from_user.username}", {message.from_user.id})')
        db.commit()
        print('new user!')


@router.message(Command('showbase'))
async def base_get(message: Message):
    c.execute('SELECT * FROM baseusers')
    print(c.fetchall())
    await message.answer(str(c.fetchall()))

@router.message(Command('new_data'))
async def create_new_date(message: Message, state: FSMContext):
    await state.set_state(get_data.get_text_data)
    await message.answer('Хорошо, тогда напишите дату в формте гггг.мм.дд')


@router.message(F.text, get_data.get_text_data)
async def get_date_from_message(message: Message, state: FSMContext):
    pattern = r"\d{4}\,\d{2}\,\d{2}"
    global data
    isFormated = None
    data = message.text
    if re.fullmatch(pattern, message.text):
        isFormated = True
        if data[5] == '0':
            month = data[6]
            print('check')
            year = data[0, 3]
            day = data[8, 9]
            data = f'{year}, {month}, {day}'
            await message.answer(data)
            print(data)
        #await state.set_state(get_data.to_base)
        #today = date.today()
        #soon = (data-today).days
        #await message.answer(soon)

    else:
        isFormated = False
    
    if isFormated == False:
        await message.answer('⛔️Вы неправильно указали дату')

#@router.message(F.text, get_data.to_base)
#async def date_to_base(message: Message, state: FSMContext):
 #   print('state')
  #  today = date.today()
   # soon = int(data)-today
    #print(soon)



@router.message(Command('delall'))
async def delete_all(message: Message):
    if message.from_user.id == 5893427261:
        c.execute('DELETE FROM baseusers')
        db.commit()
