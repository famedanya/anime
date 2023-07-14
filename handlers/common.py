from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from API.waifu import waifu_api

common_router = Router()


@common_router.message(Command('start'))
async def handle_start(message: Message):
    waifu = await waifu_api.get_waifu('kill')
    await message.answer_photo(waifu)
