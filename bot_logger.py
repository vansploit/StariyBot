import os
import logging

class BotLogger:
    def __init__(self):
        # Проверяем, существует ли папка
        if not os.path.exists('Logs'):
        # Создаём папку
            os.makedirs('Logs')
        # Создаем логгер
        self.logger = logging.getLogger('bot_logger')
        self.logger.setLevel(logging.DEBUG)  # Устанавливаем уровень логирования
        
        # Создаем обработчик для файла INFO
        self._info_handler = logging.FileHandler('./Logs/bot_info.log')
        self._info_handler.setLevel(logging.INFO)  # Уровень для этого обработчика
        
        # Создаем обработчик для файла DEBUG
        self._debug_handler = logging.FileHandler('./Logs/bot_debug.log')
        self._debug_handler.setLevel(logging.DEBUG)  # Уровень для этого обработчика
        
        # Создаем консольный обработчик
        self._console_handler = logging.StreamHandler()
        self._console_handler.setLevel(logging.INFO)  # Уровень для вывода в консоль
        
        # Создаем форматтер и добавляем его к обработчикам
        self._formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
        self._info_handler.setFormatter(self._formatter)
        self._debug_handler.setFormatter(self._formatter)
        self._console_handler.setFormatter(self._formatter)
        
        # Добавляем обработчики к логгеру
        self.logger.addHandler(self._info_handler)
        self.logger.addHandler(self._debug_handler)
        self.logger.addHandler(self._console_handler)
        
BotLog = BotLogger()
logger = BotLog.logger