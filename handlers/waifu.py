import waifu
from aiogram import Router
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from waifu import WaifuAioClient

from callbacks.waifu import WaifuTypeCallbackData, WaifuCategoryCallbackData
from keyboards.inline import sfw_categories_inline_keyboard, nsfw_categories_inline_keyboard
from states.waifu import WaifuTypeStatesGroup

waifu_router = Router()


@waifu_router.callback_query(WaifuTypeCallbackData.filter())
async def handle_waifu_type(query: CallbackQuery, callback_data: WaifuTypeCallbackData, state: FSMContext):
    if callback_data.type == 'sfw':
        await state.set_state(WaifuTypeStatesGroup.sfw)
        await query.message.answer('Вы выбрали обычные картинки. Выберите категорию',
                                   reply_markup=sfw_categories_inline_keyboard)
    else:
        await state.set_state(WaifuTypeStatesGroup.nsfw)
        await query.message.answer('Вы погрязли в разврате. Выбирайте категорию',
                                   reply_markup=nsfw_categories_inline_keyboard)


@waifu_router.callback_query(WaifuCategoryCallbackData.filter(), StateFilter(WaifuTypeStatesGroup.sfw))
async def handle_sfw_category(query: CallbackQuery, callback_data: WaifuCategoryCallbackData, state: FSMContext):
    category = callback_data.category
    async with WaifuAioClient() as session:
        image = await session.sfw(category)
    await query.message.answer_photo(image, reply_markup=sfw_categories_inline_keyboard)


@waifu_router.message(Command('waifu'))
async def get_waifu_command(message: Message):
    words = message.text.split()[1:]
    if len(words) == 2:
        waifu_type = words[0]
        waifu_category = words[1]
        if waifu_type in ('sfw', 'nsfw') and waifu_category in waifu.ImageCategories[waifu_type]:
            async with waifu.WaifuClient() as session:
                if waifu_type == 'sfw':
                    image = await session.sfw(waifu_category)
                else:
                    image = await session.nsfw(waifu_category)
            await message.answer_photo(image)
        else:
            await message.answer('Возможно вы ввели недопустимый тип или категорию')
