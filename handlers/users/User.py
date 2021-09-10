import re
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot

from udemy_course.handlers.users.Tasks import get_tasks, get_Sprint, Task
from udemy_course.keyboards.default import markupSprint, markupRetro, markupmenu
from udemy_course.states.Scrum import ReScrum, Retro, Good, Bad, MoodRETRO, Task_done
from udemy_course.utils.db_api.database import Database
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
)

# from udemy_course.keyboards.inline.inlinemarkup import mainMenu2

db = Database()


class Users:
    def __init__(
            self, id: int, first_name: str, last_name: str, phone_number: str, email: str
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email


class Task_User:
    def __init__(self, name_task: str, description: str, date1: datetime, Sprint_id: int):
        self.name_task = name_task
        self.descrip = description
        self.dattime = date1
        self.Sprint_id = Sprint_id


def get_users():
    users = db.get_users()
    users_array = []

    for user in users:
        users_array.append(Users(user[0], user[1], user[2], user[3], user[4]))
    return users_array


#     if user_id in users:
#         if regis == isregisted:
#             await message.answer("Вы не регистрированы. Введите фамилию ",reply_markup=ReplyKeyboardRemove())
#             await ReScrum.Q1.set()
#         else:
#             await message.answer("Вы уже регистрованы ")
#             await message.answer("Прошу выбарите из менью все что хотите", reply_markup=markupmenu)
#
#     else:
#         await message.answer("Ваша id не регистрирована!!!")
#


@dp.message_handler(state=ReScrum.Q1)
async def first_name(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(first_name=answer)

    await message.answer("Введите Имя : ")

    await ReScrum.next()


@dp.message_handler(state=ReScrum.Q2)
async def last_name(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(last_name=answer)
    await message.answer("Введите тел. номер(998*******) :")
    await ReScrum.next()


@dp.message_handler(state=ReScrum.Q3)
async def phone_number(message: types.Message, state: FSMContext):
    answer = message.text
    if re.search("^998\d{9}$", answer):

        await state.update_data(phone_number=answer)
        await message.answer("Введите эл.почту : ")
        await ReScrum.next()
    else:
        await message.answer("Вы ввели не правилно, введите номер тел.")
        await ReScrum.Q3.set()


@dp.message_handler(state=ReScrum.Q4)
async def email(message: types.Message, state: FSMContext):
    answer = message.text
    regex = re.compile(
        r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
    )
    if re.fullmatch(regex, answer):
        await state.update_data(email=answer)
        data = await state.get_data()
        first_name1 = data.get("first_name")
        last_name1 = data.get("last_name")
        phone_number1 = data.get("phone_number")
        email1 = data.get("email")
        isregistered = bool(False)
        user_id = message.from_user.id
        db.create_table_users()
        # sql = "INSERT INTO Users(id, first_name, last_name, phone_number, email) VALUES (?,?,?,?,?)"
        # parameters = [user_id, first_name1, last_name1, phone_number1, email1]
        db.add_user(
            first_name1, last_name1, phone_number1, email1, isregistered, user_id
        )
        await message.answer("Вы успешно зарегистрированы")
        await state.reset_state()

    else:
        await message.answer("Вы ввели не правилно, введите эл.почту : ")

        await ReScrum.Q4.set()


@dp.message_handler(text="⚒Задачи")
async def tasks_get(message: types.Message):
    await message.answer("Свободные задачи 🔽", reply_markup=ReplyKeyboardRemove())
    tasks = get_tasks()
    if not tasks:
        await message.answer("Свободных задач нет!!!", reply_markup=markupSprint)
    else:
        for task in tasks:
            mainMenu2 = InlineKeyboardMarkup(row_width=1)
            mainMenu2.insert(
                InlineKeyboardButton(text="✅", callback_data="Task-" + str(task.id))
            )
            await message.answer(
                f"<b>все данные  </b>\n<b>id :</b>{task.id}\n<b>Название :</b> {task.title} \n<b>Описание :</b> {task.description} \n<b>Время :</b> {task.created_date}\n<b>Sprint: </b> {task.Sprint_id} ",
                reply_markup=mainMenu2,
            )


@dp.callback_query_handler(text_contains="Task-")
async def taskget(call: CallbackQuery):
    # Обязательно сразу сделать answer, чтобы убрать "часики" после нажатия на кнопку.
    # Укажем cache_time, чтобы бот не получал какое-то время апдейты, тогда нижний код не будет выполняться.
    await call.answer(cache_time=30)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    user_id = call.from_user.id
    if call.data[0:5] == "Task-":
        id = call.data.split("-")
        db.add_id_task(user_id, int(id[1]))
        await call.message.answer("Задача прикреплена", reply_markup=markupSprint)
    else:
        pass


@dp.message_handler(text="🙎🏽‍♂️/🙍🏻‍♀️Профиль")
async def user_show(message: types.Message):
    users = db.select_all_tg_id()
    user_id = message.from_user.id
    users = [user[0] for user in users]

    if user_id in users:
        user = db.select_user(user_id)

        # user = [user[0]for ues in user] w
        await message.answer(
            f"Ваше данные:\n <b>Фамиля</b> : {user[1]}\n <b>Имя</b> : {user[0]}\n <b>Телефон номер </b> : {user[2]}\n <b>Элк.почта</b> : {user[3]}"
        )
    else:
        await message.answer("Вас нету в базе данных")


@dp.message_handler(text="Всё сразу")
async def Mood(message: types.Message):
    await message.answer("Как ваша ностроения в этой неделе какие проблемы", reply_markup=ReplyKeyboardRemove())
    await Retro.R1.set()


@dp.message_handler(state=Retro.R1)
async def reg_mood(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(mood=answer)
    await message.answer("Что было хорошего в этой неделе ")
    await Retro.R2.set()


@dp.message_handler(state=Retro.R2)
async def reg_good(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(good=answer)
    await message.answer("Идём дальше 🔽🔽")
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
    await Retro.R3.set()


@dp.callback_query_handler(text_contains="Sprint-", state=Retro.R3)
async def sprint_get(call: CallbackQuery, state: FSMContext):
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
    await call.message.answer("<b>Что было плогово в этой неделе</b> 🔽 ")
    await Retro.R4.set()


@dp.message_handler(state=Retro.R4)
async def reg_bad(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(bad=answer)
    data = await state.get_data()
    mood = data.get("mood")
    good = data.get("good")
    bad = data.get("bad")
    id_S = data.get("id_Sprint")
    Sprint = int(id_S[1])
    user_id = message.from_user.id
    db.create_table_Retro()
    db.add_Retro(mood, good, bad, Sprint, user_id)
    await message.answer("Процесс успешно сделан", reply_markup=markupRetro)
    await state.reset_state()


@dp.message_handler(text="👍Классно")
async def Good_Retro(message: types.Message):
    await message.answer("***", reply_markup=ReplyKeyboardRemove())
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
    await Good.G1.set()


@dp.callback_query_handler(text_contains="Sprint-", state=Good.G1)
async def sp_RETRO(call: CallbackQuery, state: FSMContext):
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
    await call.message.answer("Введите всё что было 👍Классно в этой неделе")
    await Good.G2.set()


@dp.message_handler(state=Good.G2)
async def reg_Good(message: types.Message, state: FSMContext):
    Good = message.text
    data = await state.get_data()
    user_id = message.from_user.id
    sp_array = data.get("id_Sprint")
    Sprint_id = sp_array[1]
    await message.answer("Процесс успешно сделан", reply_markup=markupRetro)
    db.create_table_Retro()
    db.add_Retro_Good(Good, Sprint_id, user_id)
    await state.reset_state()


@dp.message_handler(text="👎Плохо")
async def Bad_Retro(message: types.Message):
    await message.answer("***", reply_markup=ReplyKeyboardRemove())
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
    await Bad.B1.set()


@dp.callback_query_handler(text_contains="Sprint-", state=Bad.B1)
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
    await call.message.answer("Успешьно закриплено✔️✔️✔️")
    await call.message.answer("Введите всё что было 👎Плохо в этой неделе")
    await Bad.B2.set()


@dp.message_handler(state=Bad.B2)
async def reg_BAD(message: types.Message, state: FSMContext):
    Bad = message.text
    data = await state.get_data()
    user_id = message.from_user.id
    sp_array = data.get("id_Sprint")
    Sprint_id = sp_array[1]
    await message.answer("Процесс успешно сделан", reply_markup=markupRetro)
    db.create_table_Retro()
    db.add_Retro_Bad(Bad, Sprint_id, user_id)
    await state.reset_state()


@dp.message_handler(text="Настроения")
async def MOOD_Retro(message: types.Message):
    await message.answer("***", reply_markup=ReplyKeyboardRemove())
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
    await MoodRETRO.M1.set()


@dp.callback_query_handler(text_contains="Sprint-", state=MoodRETRO.M1)
async def sprint_MOODR(call: CallbackQuery, state: FSMContext):
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
    await call.message.answer("Введите всё что было 👎Плохо в этой неделе")
    await MoodRETRO.M2.set()


@dp.message_handler(state=MoodRETRO.M2)
async def reg_Good(message: types.Message, state: FSMContext):
    Mood = message.text
    data = await state.get_data()
    user_id = message.from_user.id
    sp_array = data.get("id_Sprint")
    Sprint_id = sp_array[1]
    await message.answer("Процесс успешно сделан", reply_markup=markupRetro)
    db.create_table_Retro()
    db.add_Retro_Bad(Mood, Sprint_id, user_id)
    await state.reset_state()


@dp.message_handler(text='⚒Закрипленные👊')
async def your_tasks(message: types.Message):
    user_id = message.from_user.id
    await message.answer("Ваши задачи :")

    def tasks_user():
        tasks = db.select_task_get(user_id)
        tasks_array = []
        for task in tasks:
            tasks_array.append(Task_User(task[0], task[1], task[2], task[3]))
        return tasks_array

    taks = tasks_user()
    # for done_task in done_tasks:
    #     if done_task:
    if not taks:
        await message.answer("У вас нет задач!!!")
    else:
        for task in taks:
            mainMenu2 = InlineKeyboardMarkup(row_width=1)
            mainMenu2.insert(
                InlineKeyboardButton(text="✅", callback_data="task_done-" + str(task.name_task))
            )

            await message.answer(
                f"Все данные  \n<b>Название :</b>{task.name_task}\n<b>Описание :</b> {task.descrip} \n<b>Время :</b> {task.dattime} \n<b> Sprint_id :</b> {task.Sprint_id}",
                reply_markup=mainMenu2
            )


# else:
#     await message.answer("Задач нету!!!!")

@dp.callback_query_handler(text_contains="task_done-")
async def task_done(call: CallbackQuery, state: FSMContext):
    # Обязательно сразу сделать answer, чтобы убрать "часики" после нажатия на кнопку.
    # Укажем cache_time, чтобы бот не получал какое-то время апдейты, тогда нижний код не будет выполняться.
    await call.answer(cache_time=20)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data[0:10] == "task_done-":
        name_task = call.data.split("-")
        await state.update_data(name_task=name_task)
        data = await state.get_data()
        task_array = data.get("name_task")
        task_name = task_array[1]
        task_done = bool(False)
        db.update_task_user(task_done, task_name)
    else:
        pass
    await call.message.answer("Успешьно ✔️✔️✔️")
    await state.reset_state()
