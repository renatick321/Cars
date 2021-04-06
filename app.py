from loader import bot
from config import ADMIN, TEST_ADMIN


async def on_shutdown(dp):
	try:
		await bot.send_message(chat_id=TEST_ADMIN, text="Бот окончил свою работу")
		await bot.close()
	except:
		pass

async def send_to_admin(dp):
	try:
		await bot.send_message(chat_id=TEST_ADMIN, text="Бот запущен")
	except:
		pass


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=send_to_admin, on_shutdown=on_shutdown)