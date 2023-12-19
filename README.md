# 🤖 Бот-ассистент
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)

Telegram-бот, который обращается к API сервиса Практикум.Домашка и узнает статус вашей домашней работы: взята ли ваша домашка в ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку.

### __Возможности бота__
- раз в 10 минут опрашивает API сервис Практикум.Домашка и проверяет статус отправленной на ревью домашней работы;
- при обновлении статуса анализирует ответ API и отправляет соответствующее уведомление в Telegram;
- логирует свою работу и сообщает о важных проблемах сообщением в Telegram.

### __Установка на локальном компьютере__
1. Клонируйте репозиторий
```
> git clone git@github.com:Lozhkin-pa/telegram_bot.git
```
2. Установите и активируйте виртуальное окружение
```
> python -m venv venv
> source venv/Scripts/activate  - для Windows
> source venv/bin/activate - для Linux
```
3. Установите зависимости
```
> python -m pip install --upgrade pip
> pip install -r requirements.txt
```
4. Запустите проект
```
> python homework.py
```

### __Технологии__
* [Python 3.2.0](https://www.python.org/doc/)
* [Python-telegram-bot 13.7](https://docs.python-telegram-bot.org/en/v20.7/)

### __Автор__
[Павел Ложкин](https://github.com/Lozhkin-pa)
