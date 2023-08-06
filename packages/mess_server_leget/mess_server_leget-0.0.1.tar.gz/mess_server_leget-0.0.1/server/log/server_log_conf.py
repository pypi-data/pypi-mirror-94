import logging.handlers
import os
import sys

sys.path.append('../')
# Подготовка имени файла для логирования
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'logs/server_log.log')
# Создаю логгер 'log_server'
log_server = logging.getLogger('log_server')
# Устанавливаю уровень логирования
log_server.setLevel(logging.DEBUG)
# Настройка формата вывода
format_log = logging.Formatter("%(asctime)-30s %(levelname)-10s %(module)-20s %(message)s")
# Логирование в поток вывода
log_in_stderr = logging.StreamHandler(sys.stderr)
# Логирование в файл
log_in_file = logging.handlers.TimedRotatingFileHandler(PATH, interval=1, when='D', encoding='utf-8')
# Настройка уровня логирования для вывода в поток
log_in_stderr.setLevel(logging.CRITICAL)
# Настройка формата вывода в поток
log_in_stderr.setFormatter(format_log)
# Настройка формата вывода в файл
log_in_file.setFormatter(format_log)
# Настройка уровня логирования для вывола в файл
log_in_file.setLevel(logging.DEBUG)
# Добавляю обработчик для log_in_stderr и log_in_file
log_server.addHandler(log_in_stderr)
log_server.addHandler(log_in_file)

if __name__ == '__main__':
    log_server.debug('Информация при отладке сервера')
    log_server.info('Действия ксервера')
    log_server.warning('Предупреждение')
    log_server.error('Ошибка сервера')
    log_server.critical('Критическая ошибка сервера')
