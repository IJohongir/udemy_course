import sqlite3

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove
from loader import dp, db
from udemy_course.keyboards.default import markupmenu, markupRetro, markupSprint
from udemy_course.states import ReScrum
from udemy_course.utils.db_api import Database

db = Database()
@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
    users = db.select_all_tg_id()
    users = [user[0] for user in users]
    user_id = message.from_user.id
    regis = bool(True)
    isregisted = bool(db.select_isregis(user_id))

    if user_id in users:
        if regis == isregisted:
            await message.answer(
                "Вы не регистрированы. Введите фамилию : ",
                reply_markup=ReplyKeyboardRemove(),
            )
            await ReScrum.Q1.set()
        else:
            await message.answer("Вы уже регистрованы ")
            await message.answer(
                "Прошу выбарите из менью все что хотите", reply_markup=markupmenu
            )

    else:
        await message.answer("Ваша id не регистрирована!!!")


@dp.message_handler(text="Sprint")
async def get_Sprint2(message: types.Message):
    db.create_table_Sprint()
    await message.answer("📅", reply_markup=markupSprint)


@dp.message_handler(text="📺Ретро")
async def get_Retro(message: types.Message):
    await message.answer("📺", reply_markup=markupRetro)


@dp.message_handler(text="◀️Назад")
async def get_Retro(message: types.Message):
    await message.answer("◀️", reply_markup=markupmenu)
