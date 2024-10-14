from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile

from skincare.skin_analyser import skin_analyser

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    """
    Обработка команды /start. Бот приветствует пользователя и сообщает о своем функционале.

    :param message: Объект сообщения, содержащий информацию о команде /start.
    """
    await message.answer("Привет! Я бот, который анализирует кожу.")


@router.message(F.photo)
async def process_photo(message: Message, bot: Bot):
    """
    Обработка сообщения с фото. Бот загружает фотографию, выполняет анализ кожи с помощью функции skin_analyser и
    отправляет результаты пользователю в виде трех изображений: контуры, Canny-изображение и маска красных оттенков.

    :param message: Объект сообщения, содержащий информацию о фото, присланном пользователем.
    :param bot: Объект бота для взаимодействия с пользователем.

    Функциональные шаги:
    1. Бот принимает фото и сохраняет его локально.
    2. Выполняется анализ изображения с помощью функции skin_analyser.
    3. Бот отправляет результаты анализа в виде изображений:
    — Фото с контурами,
    — Canny-обработанное изображение,
    — Маска красных оттенков.
    4. Если на фото не обнаружено лицо, отправляется сообщение об ошибке.
    """
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
