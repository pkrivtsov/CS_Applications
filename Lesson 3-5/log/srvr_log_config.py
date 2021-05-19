import logging
from logging.handlers import TimedRotatingFileHandler
import sys
 
# Определить формат сообщений
format = logging.Formatter('[%(asctime)-10s] %(levelname).1s %(module)s %(message)s')
 
# Создать обработчик, который выводит сообщения с уровнем INFO в файл, с ежедневной ротацией
fh = logging.TimedRotatingFileHandler('log/info.log', when='D', interval=1, encoding = 'utf-8')
fh.setLevel(logging.INFO)
fh.setFormatter(format)
 

# Создать объект-логгер с именем 'app'
app_log = logging.getLogger('app')
app_log.setLevel(logging.INFO)
app_log.addHandler(fh)

