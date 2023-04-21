from dotenv import load_dotenv
import logging
import os
import time
import sys
import requests
from exceptions import HTTPStatusException
from http import HTTPStatus
import telegram

load_dotenv()

logger = logging.getLogger(__name__)
handlers = [logging.StreamHandler(sys.stdout)]
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=handlers
)

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens():
    """Проверяет доступность переменных окружения."""
    if (PRACTICUM_TOKEN or TELEGRAM_TOKEN or TELEGRAM_CHAT_ID) is None:
        message = 'Отсутствие обязательных переменных окружения!'
        logger.critical(msg=message)
        sys.exit()


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.debug(f'Сообщение "{message}" успешно отправлено в Telegram')
    except Exception as error:
        logger.error(
            f'Сбой при отправке сообщения "{message}" в Telegram: {error}'
        )


def get_api_answer(timestamp):
    """Делает запрос к эндпоинту Практикум.Домашка."""
    payload = {'from_date': timestamp}
    try:
        response = requests.get(url=ENDPOINT, headers=HEADERS, params=payload)
    except Exception as error:
        logger.error(f'Сбой при запросе к эндпоинту: {error}')
    if response.status_code != HTTPStatus.OK:
        raise HTTPStatusException('Полученный статус отличается от 200!')
    return response.json()


def check_response(response):
    """Проверяет ответ API на соответствие документации."""
    if not isinstance(response, dict):
        raise TypeError('В ответе API получен не словарь!')
    homework = response.get('homeworks')
    current_date = response.get('current_date')
    if homework is None:
        raise KeyError('В ответе API отсутствует ключ "homeworks"!')
    if current_date is None:
        raise KeyError('В ответе API отсутствует ключ "current_date"!')
    if not isinstance(homework, list):
        raise TypeError(
            'В ответе API под ключом "homework" получен не список!'
        )
    return homework


def parse_status(homework):
    """Извлекает из информации о конкретной домашней работе её статус."""
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if homework_name is None:
        raise KeyError('Ключ homework_name не найден')
    if homework_status is None:
        raise KeyError('Ключ homework_status не найден')
    if homework_status not in HOMEWORK_VERDICTS:
        raise ValueError(
            f'В ответе API обнаружен неожиданный статус домашней работы:'
            f'{homework_status}'
        )
    else:
        verdict = HOMEWORK_VERDICTS[homework_status]
    return (f'Изменился статус проверки работы "{homework_name}". {verdict}')


def main():
    """Основная логика работы бота."""
    check_tokens()
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    logger.info('Бот запущен!')
    timestamp = int(time.time())
    hw_status = ''

    while True:
        try:
            response = get_api_answer(timestamp)
            timestamp = response.get('current_date')
            homework = check_response(response)[0]
            message = parse_status(homework)
            if message != hw_status:
                logger.info(message)
                send_message(bot, message)
                hw_status = message
        except Exception as error:
            logger.critical(f'Сбой в работе программы: {error}!')
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
