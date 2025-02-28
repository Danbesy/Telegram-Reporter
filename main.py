import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from handlers import router
from config import *

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Основная функция
async def main():
    dp.include_router(router)

    # Удаляем старые команды    
    await bot.delete_my_commands()

    commands = [
        BotCommand(command="/start", description="Перезапустить бота 🔁 Restart bot"),
        BotCommand(command="/language", description="Смена языка 🌐 Change language")
    ]
    await bot.set_my_commands(commands)

    # Запускаем поллинг
    await dp.start_polling(bot)

# Запуск программы
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
        
