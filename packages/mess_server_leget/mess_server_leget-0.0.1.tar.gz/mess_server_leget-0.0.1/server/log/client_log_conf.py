import logging.handlers
import os
import sys

sys.path.append('../')
# Подготовка имени файла для логирования
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'logs/client_logs.log')
# Создаю логгер 'log_client'
log_client = logging.getLogger('log_client')
# Устанавливаю уровень логирования
log_client.setLevel(logging.DEBUG)
# Настройка формата вывода
format_log = logging.Formatter("%(asctime)-30s %(levelname)-10s %(module)-20s %(message)s")
# Логирование в поток вывода
log_in_stderr = logging.StreamHandler(sys.stderr)
# Логирование в файл
log_in_file = logging.FileHandler(PATH, encoding='UTF-8')
# Настройка уровня логирования для вывола в поток
log_in_stderr.setLevel(logging.CRITICAL)
# Настройка формата вывода в поток
log_in_stderr.setFormatter(format_log)
# Настройка формата вывода в файл
log_in_file.setFormatter(format_log)
# Настройка уровня логирования для вывола в файл
log_in_file.setLevel(logging.DEBUG)
# Добавляю обработчик для log_in_stderr и log_in_file
log_client.addHandler(log_in_stderr)
log_client.addHandler(log_in_file)

if __name__ == '__main__':
    log_client.debug('Информация при отладке')
    log_client.info('Действия клиента')
    log_client.warning('Предупреждение')
    log_client.error('Ошибка')
    log_client.critical('Критическая ошибка')
