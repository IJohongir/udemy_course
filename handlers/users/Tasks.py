from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from keyboards.default import markupmenu, markupSprint
from states.Scrum import ReTasks
from utils.db_api import Database
from datetime import datetime

from loader import dp, bot

db = Database()


class Task:
    def __init__(self, id: int, description: str, title: str, created_date: datetime, user_id: int, Sprint_id: int):
        self.id = id
        self.description = description
        self.title = title
        self.created_date = created_date
        self.user_id = user_id
        self.Sprint_id = Sprint_id

#
# class Task_admin:
#     def __init__(self, id: int, description: str, title: str, created_date: datetime, user_id: int, Sprint_id: int,
#                  task_done: bool):
#         self.id = id
#         self.description = description
#         self.title = title
#         self.created_date = created_date
#         self.user_id = user_id
#         self.Sprint_id = Sprint_id
#         self.task_done = task_done


def get_tasks():
    tasks = db.get_user_tasks()
    task_array = []
    for task in tasks:
        task_array.append(Task(task[0], task[1], task[3], task[2], task[4], task[5]))
    return task_array


def get_tasks_admin():
    tasks = db.get_admin_tasks()
    task_array = []
    for task in tasks:
        task_array.append(Task(task[0], task[1], task[3], task[2], task[4], task[5]))
    return task_array


# def all_tasks():
#     tasks_count = db.count_tasks()
#     tasks_array = []
class Sprint:
    def __init__(self, id: int, name_s: str, first_date: datetime, last_date: datetime):
        self.id = id
        self.name_sprint = name_s
        self.first_date = first_date
        self.last_date = last_date


def get_Sprint():
    sprints = db.sprint_all()
    sprint_array = []
    for sprint in sprints:
        sprint_array.append(Sprint(sprint[0], sprint[1], sprint[2], sprint[3]))
    return sprint_array


@dp.message_handler(text="Новые задачи")
async def reg_tasks(message: types.Message):
    await message.answer("Введите имя новые задачи: ", reply_markup=ReplyKeyboardRemove())
    await ReTasks.T1.set()


@dp.message_handler(state=ReTasks.T1)
async def name_task(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(name_task=answer)
    await message.answer("Введите описания :")
    await ReTasks.next()


@dp.message_handler(state=ReTasks.T2)
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
    await ReTasks.T3.set()


@dp.callback_query_handler(text_contains="Sprint-", state=ReTasks.T3)
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
    await ReTasks.T4.set()
    await call.message.answer("Успешьно закриплено✔️✔️✔️")
    await call.message.answer("Зарегат задачу да/нет")


@dp.message_handler(state=ReTasks.T4)
async def reg_task(message: types.Message, state: FSMContext):
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
        await message.answer("Процесс успешно сделан", reply_markup=markupSprint)
        await state.reset_state()
    elif answer == 'нет':
        await message.answer("задача отменён")
    else:
        await message.answer("ответьте 'да' или 'нет' ")
        await ReTasks.T4.set()
