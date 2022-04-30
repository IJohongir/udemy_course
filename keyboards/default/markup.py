from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

markupmenu = ReplyKeyboardMarkup(
    keyboard=[
        [

            KeyboardButton('Sprint'),
            KeyboardButton('📺Ретро'),

        ],
        [

            KeyboardButton('⚒Закрипленные👊'),
            KeyboardButton('🙎🏽‍♂️/🙍🏻‍♀️Профиль')
        ],
    ], resize_keyboard=True)

markupRetro = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Всё сразу"), KeyboardButton('👍Классно'), KeyboardButton('👎Плохо'),
        ],

        [
            KeyboardButton('Настроения'), KeyboardButton('◀️Назад')
        ],

    ], resize_keyboard=True)

markupSprint = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('⚒Задачи'), KeyboardButton('Новые задачи'), KeyboardButton('◀️Назад')
        ],

    ], resize_keyboard=True)

markupAdmin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Новые задачи(admin)'), KeyboardButton('Все задачи'), KeyboardButton('Работники')

        ], [
            KeyboardButton('Добавить id:'), KeyboardButton('Sprintadd:'), KeyboardButton("Retro(admin)")
        ],
    ], resize_keyboard=True)
markupDropTable = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Retro(drop)'), KeyboardButton('Sprint(drop)'), KeyboardButton('admin(drop)'),

        ],
        [
            KeyboardButton('tasks(drop)'), KeyboardButton('users(drop)')
        ]
    ], resize_keyboard=True)
