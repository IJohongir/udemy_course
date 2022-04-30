from datetime import datetime
import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, bot

from states import AdminTasks, IDAdmin, Sprint, getRetro
from utils.db_api import Database
from keyboards.default.markup import markupAdmin, markupDropTable
from .Tasks import Task, get_tasks_admin as get_tasks_from_db, get_Sprint
from .User import Users, get_users
from data.config import admins

db = Database()


class Retro:
    def __init__(self, Mood: str, Good: str, Bad: str, user_id: int):
        self.mood = Mood
        self.good = Good
        self.Bad = Bad
        self.user_id = user_id


@dp.message_handler(Command("admin"))
async def admin(message: types.Message):
    admin = admins
    user_id = message.from_user.id

    if user_id in admin:
        await message.answer(
            "Привествую вас оо все могучий 💪💪💪", reply_markup=markupAdmin
        )
        db.create_table_Admin()
    else:
        await message.answer("У вас нет права админа😬!!!")


@dp.message_handler(Command("delete"))
async def admin(message: types.Message):
    admin = admins
    user_id = message.from_user.id

    if user_id in admin:
        await message.answer(
            "Привествую вас оо все могучий 💪💪💪", reply_markup=markupDropTable
        )
    else:
        await message.answer("У вас нет права админа😬!!!")


@dp.message_handler(text='Retro(drop)')
async def Clear_Retro(message: types.Message):
    admin = admins
    user_id = message.from_user.id

    if user_id in admin:
        db.clear_table_Retro()
        await message.answer("Успешно почистена", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("У вас нет права админа😬!!!")


@dp.message_handler(text='Sprint(drop)')
async def Clear_Retro(message: types.Message):
    admin = admins
    user_id = message.from_user.id

    if user_id in admin:
        db.clear_table_Sprint()
        await message.answer("Успешно почистена", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("У вас нет права админа😬!!!")


@dp.message_handler(text='admin(drop)')
async def Clear_Retro(message: types.Message):
    admin = admins
    user_id = message.from_user.id

    if user_id in admin:
        db.clear_table_admin()
        await message.answer("Успешно почистена", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("У вас нет права админа😬!!!")


@dp.message_handler(text='tasks(drop)')
async def Clear_Retro(message: types.Message):
    admin = admins
    user_id = message.from_user.id

    if user_id in admin:
        db.clear_table_tasks()
        await message.answer("Успешно почистена", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("У вас нет права админа😬!!!")


@dp.message_handler(text='users(drop)')
async def Clear_Retro(message: types.Message):
    admin = admins
    user_id = message.from_user.id

    if user_id in admin:
        db.clear_table_users()
        await message.answer("Успешно почистена", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("У вас нет права админа😬!!!")


@dp.message_handler(text="Новые задачи(admin)")
async def delete_user(message: types.Message):
    await message.answer("Введите новые задачи", reply_markup=ReplyKeyboardRemove())

    await AdminTasks.AT1.set()


@dp.message_handler(state=AdminTasks.AT1)
async def name_task(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(name_task=answer)
    await message.answer("Введите описания :")
    await AdminTasks.next()


@dp.message_handler(state=AdminTasks.AT2)
async def Sprint_id(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(description=answer)
    sprints = get_Sprint()

    for task in sprints:
        mainMenu2 = InlineKeyboardMarkup(row_width=1)
        mainMenu2.insert(
            InlineKeyboardButton(text=f"{task.name_sprint}", callback_data="Sprint-" + str(task.id))
        )
        await message.answer(
            f"Выбариты : {task.name_sprint}",
            reply_markup=mainMenu2
        )
    await AdminTasks.AT3.set()


@dp.callback_query_handler(text_contains="Sprint-", state=AdminTasks.AT3)
async def spirnget(call: CallbackQuery, state: FSMContext):
    # Обязательно сразу сделать answer, чтобы убрать "часики" после нажатия на кнопку.
    # Укажем cache_time, чтобы бот не получал какое-то время апдейты, тогда нижний код не будет выполняться.
    await call.answer(cache_time=20)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data[0:7] == "Sprint-":
        id = call.data.split("-")
        await state.update_data(id_Sprint=id)

    else:
        pass

    await call.message.answer("Успешьно закриплено✔️✔️✔️")
    await AdminTasks.AT4.set()
    await call.message.answer("Зарегат задачу да/нет")


@dp.message_handler(state=AdminTasks.AT4)
async def description(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'да':
        data = await state.get_data()
        name_task = data.get("name_task")
        description = data.get("description")
        sprint_array = data.get("id_Sprint")
        id_sprint = int(sprint_array[1])
        datae = message.date
        db.create_table_Tasks()
        db.add_tasks(name_task, description, datae, id_sprint)
        await message.answer("Процесс успешно сделан", reply_markup=markupAdmin)
        await state.reset_state()
    elif answer == 'нет':
        await message.answer("задача отменён")
    else:
        await message.answer("ответьте 'да' или 'нет' ")
        await AdminTasks.AT4.set()


@dp.message_handler(text="Добавить id:")
async def admin_adduser(message: types.Message):
    await message.answer(
        "Введите ID пользователя: ", reply_markup=ReplyKeyboardRemove()
    )
    await IDAdmin.I1.set()


@dp.message_handler(state=IDAdmin.I1)
async def id_user(message: types.Message, state: FSMContext):
    answer = int(message.text)
    isregis = 1
    db.admin_add_users(answer, isregis)
    await message.answer("Успешно добавлена")
    await state.reset_state()


@dp.message_handler(text="Все задачи")
async def get_tasks(message: types.Message):
    tasks = get_tasks_from_db()

    for task in tasks:
        await message.answer(
            f"<b>все данные  </b>\n<b>id : </b>{task.id}\n<b>Название : </b>{task.title} \n<b>Описание : </b>{task.description} \n<b>Время : </b>{task.created_date} \n<b>Кто прикреплен : </b>{task.user_id}\n<b>Sprint id  : </b>{task.Sprint_id}"
        )


@dp.message_handler(text="Работники")
async def get_tasks(message: types.Message):
    users = get_users()

    for user in users:
        await message.answer(
            f"<b>все данные  </b>\n<b>id :  </b>{user.id}\n<b>Имя : </b>{user.first_name} \n<b>Фамиля : </b>{user.last_name} \n<b>Телефон номер:    </b>{user.phone_number} \n<b>Электронный почта :    </b>{user.email} "
        )


@dp.message_handler(text="Sprintadd:")
async def add_sprint(message: types.Message):
    await message.answer("Введите Sprint№*", reply_markup=ReplyKeyboardRemove())
    await Sprint.S1.set()


@dp.message_handler(state=Sprint.S1)
async def name_sprint(message: types.Message, state: FSMContext):
    answer = message.text
    if re.search("^Sprint\d{1}$", answer):
        await state.update_data(name_sprint=answer)
        await message.answer("Введите началу(date):")
        await Sprint.next()
    else:
        await message.answer("Введите 'Sprint#' место # номер Sprintа 🧐")
        await Sprint.S1.set()


@dp.message_handler(state=Sprint.S2)
async def first_date(message: types.Message, state: FSMContext):
    answer = message.text
    if re.search("\d\d/\d\d/\d{2}", answer):
        await Sprint.next()
        await state.update_data(first_date=answer)
        await message.answer("Введите конец Sprinta(date):")
    else:
        await message.answer("Ошибка при вводе😬")
        await Sprint.S2.set()


@dp.message_handler(state=Sprint.S3)
async def last_date(message: types.Message, state: FSMContext):
    answer = message.text
    if re.search("\d\d/\d\d/\d{2}", answer):
        db.create_table_Sprint()
        await state.update_data(last_date=answer)
        data = await state.get_data()
        name_sprint = data.get("name_sprint")
        first_date = data.get("first_date")
        last_date = data.get("last_date")
        plus = ' 12:01:20'
        first_date = first_date + plus
        last_date = last_date + plus
        date_time_first = datetime.strptime(first_date, '%d/%m/%y %H:%M:%S')
        date_time_last = datetime.strptime(last_date, '%d/%m/%y %H:%M:%S')
        db.add_Sprint(name_sprint, date_time_first, date_time_last)
        await message.answer("Sprint успешно добавлена🙂")
        await state.reset_state()

    else:
        await message.answer("Ошибка при вводе😬")
        await Sprint.S3.set()

    # name_sprint = data.get("name_sprint")
    # first_date = datetime(data.get("first_date"))
    # last_date = datetime(data.get("last_date"))
    # db.add_Sprint(name_sprint, first_date, last_date)


@dp.message_handler(text="Retro(admin)")
async def get_retro_admin(message: types.Message):
    await message.answer("Выбарите Sprint 🔽🔽🔽", reply_markup=ReplyKeyboardRemove())
    sprints = get_Sprint()

    for task in sprints:
        mainMenu2 = InlineKeyboardMarkup(row_width=1)
        mainMenu2.insert(
            InlineKeyboardButton(text=f"{task.name_sprint}", callback_data="Sprint-" + str(task.id))
        )
        await message.answer(
            f"Выбариты : {task.name_sprint}",
            reply_markup=mainMenu2
        )

    await getRetro.gR1.set()


@dp.callback_query_handler(text_contains="Sprint-", state=getRetro.gR1)
async def sprint_Bad(call: CallbackQuery, state: FSMContext):
    # Обязательно сразу сделать answer, чтобы убрать "часики" после нажатия на кнопку.
    # Укажем cache_time, чтобы бот не получал какое-то время апдейты, тогда нижний код не будет выполняться.
    await call.answer(cache_time=20)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data[0:7] == "Sprint-":
        id = call.data.split("-")
        await state.update_data(id_Sprint=id)

    else:
        pass
    await call.message.answer("Выброна✔️✔️✔️")
    await call.message.answer("Введите любое слова !!!!")
    await getRetro.gR2.set()


@dp.message_handler(state=getRetro.gR2)
async def Get_retro(message: types.Message, state: FSMContext):
    date = await state.get_data()
    S_array = date.get("id_Sprint")
    sprint_id = int(S_array[1])

    def retro_user():
        Retros = db.admin_Retro(sprint_id)
        retro_array = []
        for retro in Retros:
            retro_array.append(Retro(retro[0], retro[1], retro[2], retro[3]))
        return retro_array

    retros = retro_user()
    if not retros:
        await message.answer("Retro нет !!!")
    else:
        for task in retros:
            await message.answer(
                f"Все данные  \n<b>Настроения :</b>{task.mood}\n<b>👍Классно :</b> {task.good} \n<b>👎Плохо:</b> {task.Bad} \n<b> User_id :</b> {task.user_id}"
            )
    await state.reset_state()
