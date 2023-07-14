import asyncio  # Работа с асинхронностью

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from API.waifu import WaifuApi
from config import config  # Config
from handlers import common
from middleware.api import WaifuApiMiddleWare


def register_all_routers(dp: Dispatcher):
    dp.include_router(common.common_router)


def register_all_middlewares(dp: Dispatcher, waifu_api: WaifuApi):
    waifu_api_middleware = WaifuApiMiddleWare(waifu_api)
    dp.update.middleware(waifu_api_middleware)


async def main():
    bot = Bot(token=config.token)
    dp = Dispatcher(storage=MemoryStorage())  # Менеджер бота

    register_all_routers(dp)

    waifu_api = WaifuApi()

    register_all_middlewares(dp, waifu_api)

    try:
        print('Bot Started')
        await dp.start_polling(bot)

    finally:
        await bot.session.close()


if __name__ == '__main__':  # Если мы запускаем конкретно этот файл.
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')