from aiogram import types
my_commands = [
    types.BotCommand(command="/start", description="Начать работу с ботом"),
    types.BotCommand(command="/link", description="Отправить ссылку на свой профиль"),
    types.BotCommand(command="/next", description="Новый собеседник"),
    types.BotCommand(command="/stop", description="Остановить диалог"),
]