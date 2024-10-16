# Телеграм-бот "Skincare"
## Для запуска бота необходимо:
1. Создать Docker образ:
```bash
docker build -t skincare_bot .
```
2. Запустить Docker контейнер:
```bash
docker run -d --name skincare_bot skincare_bot
```
## Организация проекта:
* **skincare/**
  * **skin_analyser.py**: Модуль, содержащий функцию skin_analyser, которая анализирует изображение для обнаружения лиц, удаления фона и выделения красных областей.
  * **bot.py**: Модуль, настраивающий бота с использованием библиотеки aiogram.
  * **handlers/**: Директория, содержащая обработчики для различных команд и событий бота.
* **run_bot.py**: Модуль, содержащий точку входа для запуска бота.
* **.env**: Файл, содержащий переменные окружения, такие как токен бота.
* **.gitignore**: Файл, указывающий файлы и директории, которые должны быть проигнорированы Git.
* **Dockerfile**: Файл, содержащий инструкции для создания Docker образа.
* **requirements.txt**: Файл, содержащий список зависимостей проекта.
* **README.md**: Файл с описанием проекта и инструкциями по его запуску.
