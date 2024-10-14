import asyncio

from skincare.bot import dp, logger, bot
from skincare.handlers import router


async def main():
    """
    Асинхронная функция для запуска бота.

    - Подключает маршрутизатор (router) с обработчиками событий к диспетчеру (dp).
    - Запускает опрос Telegram API для получения обновлений и обработки сообщений.

    Ожидается, что функция `start_polling` будет непрерывно работать до тех пор,
    пока программа не будет остановлена вручную (например, с помощью прерывания).
    """
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")
