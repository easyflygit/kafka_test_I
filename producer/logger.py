import logging

# Создаем логгер с именем 'receipts_logger'
logger = logging.getLogger('receipts_logger')

# Устанавливаем уровень логирования для логгера
logger.setLevel(logging.INFO)

# Создаем обработчик для записи логов в файл
file_handler = logging.FileHandler('logfile.log')

# Устанавливаем уровень логирования для обработчика
file_handler.setLevel(logging.INFO)

# Создаем форматтер для определения формата сообщений лога
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Устанавливаем форматтер для обработчика
file_handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(file_handler)


def some_function(message):
    # Пример использования логгера
    logger.info(message)