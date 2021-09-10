from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, Command
from aiogram.types import ReplyKeyboardRemove
from loader import dp

from keyboards.default import markupmenu
from states import ReScrum

from udemy_course.handlers.users.Admin import admin
from udemy_course.utils.db_api import Database

db = Database()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    db.create_table_users()
    users = db.select_all_tg_id()
    users = [user[0] for user in users]
    user_id = message.from_user.id
    regis = bool(True)
    isregisted = bool(db.select_isregis(user_id))

    if user_id in users:
        if regis == isregisted:
            await message.answer(
                "Вы не регистрированы. Введите фамилию",
                reply_markup=ReplyKeyboardRemove(),
            )
            await ReScrum.Q1.set()
        else:
            await message.answer(f"Вы уже регистрованы ")
            await message.answer(
                "Прошу выбарите из менью все что хотите", reply_markup=markupmenu
            )

    else:
        await message.answer("Ваша id не регистрирована!!!")


@dp.message_handler(Command("cancel"))
async def cancel(message: types.Message):
    await bot_start()
