from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("menu","Менью для работы"),
        types.BotCommand("admin","Для администратора"),
        types.BotCommand("cancel","Отмена дейтвия")
    ])
