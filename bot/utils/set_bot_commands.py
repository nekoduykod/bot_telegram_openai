from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Start Bot"),
        types.BotCommand("help", 'Help/Instruction'),
        types.BotCommand("exit", 'exits a state/checklist')
    ])