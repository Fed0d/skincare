from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile

from skincare.skin_analyser import skin_analyser

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer("Привет! Я бот, который анализирует кожу.")


@router.message(F.photo)
async def process_photo(message: Message, bot: Bot):
    await message.answer("Спасибо за фото! Обрабатываю...")
    file_name = f"photos/{message.photo[-1].file_id}.jpg"
    await bot.download(message.photo[-1], destination=file_name)
    try:
        skin_analyser(message.photo[-1].file_id)
        await message.answer_photo(photo=FSInputFile(f"photos/{message.photo[-1].file_id}_contours.jpg"))
        await message.answer_photo(photo=FSInputFile(f"photos/{message.photo[-1].file_id}_canny.jpg"))
        await message.answer_photo(photo=FSInputFile(f"photos/{message.photo[-1].file_id}_mask_red.jpg"))
    except ValueError as e:
        await message.answer(str(e))
