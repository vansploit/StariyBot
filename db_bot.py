import sqlite3
import datetime
import pytz

from bot_logger import logger
from plugins.BotClasses import User, Order

class MyDatabase:
    
    def __init__(self, logger):
        
        self._logger = logger
        self._connection = None
        self._cursor = None
        
        self._connect()
        
        self._logger.info("Создание таблицы Users если её нет")
        
        self._cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        telegram_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        nickname TEXT,
        privilege TEXT NOT NULL,
        banned BOOL DEFAULT FALSE,
        ban_time DATETIME,
        ban_duration INTEGER,
        rating TEXT NOT NULL,
        transfer_details TEXT
        )
        ''')
        
        self._logger.info("Создание таблицы Orders если её нет")
        
        self._cursor.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
        id INTEGER PRIMARY KEY,
        telegram_id INTEGER NOT NULL,
        order_list TEXT NOT NULL,
        time DATETIME NOT NULL,
        exec_id INTEGER,
        ready BOOL DEFAULT FALSE
        )
        ''')
        
        self._disconnect()
        
        
    def _get_time(self):
        moscow_tz = pytz.timezone('Europe/Moscow')
        current_time = datetime.datetime.now(moscow_tz)

        # Форматируем дату и время без миллисекунд
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_time

        
    def _user_to_dict(self, user):
        return {
        "id": user[0],
        "tg_id": user[1],
        "username": user[2],
        "nickname": user[3],
        "privilege": user[4],
        "banned": user[5],
        "ban_time": user[6],
        "ban_duration": user[7],
        "rating": user[8],
        "transfer_details": user[9]
        }
        
        
    def _order_to_dict(self, order):
        return {
        "id": order[0],
        "tg_id": order[1],
        "order_list": order[2].split("/"),
        "time": order[3],
        "exec_id": order[4],
        "ready": order[5]
        }
        
        
    def _order_to_class(self, lst):
        order = Order()
        print(lst)
        print(len(lst))
        order.put_data(lst)
        return order
        
        
    def _user_to_class(self, lst):
        user = User()
        print("User:")
        print(lst)
        print(len(lst))
        user.put_data(lst)
        return user
        
    # system   
    def _connect(self):
        self._connection = sqlite3.connect('Mybot_database_.db')
        self._cursor = self._connection.cursor()
        
    # system
    def _disconnect(self):
        self._connection.commit()
        self._connection.close()

    # User management
    def add_user(self, telegram_id, username, privilege = 'user', rating = '0/0', nickname=None, transfer_details=None):
        self._connect()
        self._cursor.execute('''
            INSERT INTO Users (telegram_id, username, nickname, privilege, rating, transfer_details)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (telegram_id, username, nickname, privilege, rating, transfer_details))
        self._logger.info(f"Добавлен пользователь: {username}:{telegram_id} ")
        self._disconnect()
        
    # Order management
    def add_order(self, telegram_id, order_list):
        order_time = self._get_time()
        order = "/".join(order_list)
        self._connect()
        self._cursor.execute('''
            INSERT INTO Orders (telegram_id, order_list, time)
            VALUES (?, ?, ?)
        ''', (telegram_id, order, order_time))
        self._logger.info(f"Добавлен заказ для telegram_id: {telegram_id}, время: {order_time}")
        self._disconnect()


    def update_user(self, telegram_id, **kwargs):
        self._connect()
        for key, value in kwargs.items():
            self._cursor.execute(f'''
                UPDATE Users
                SET {key} = ?
                WHERE telegram_id = ?
            ''', (value, telegram_id))
        self._logger.info(f"Обновлен пользователь с telegram_id: {telegram_id}")
        self._disconnect()
        
        
    def update_order(self, order_id, **kwargs):
        self._connect()
        for key, value in kwargs.items():
            if key == "order_list":
                value = "/".join(value)
            self._cursor.execute(f'''
                UPDATE Orders
                SET {key} = ?
                WHERE id = ?
            ''', (value, order_id))
        self._logger.info(f"Обновлен заказ с id: {order_id}")
        self._disconnect()


    def get_user(self, telegram_id):
        self._connect()
        self._cursor.execute('''
            SELECT * FROM Users WHERE telegram_id = ?
        ''', (telegram_id,))
        user = self._cursor.fetchone()
        self._disconnect()
        return self._user_to_class(user) if user else None


    def get_order(self, order_id):
        self._connect()
        self._cursor.execute('''
            SELECT * FROM Orders WHERE id = ?
        ''', (order_id,))
        order = self._cursor.fetchone()
        self._disconnect()
        return self._order_to_class(order) if order else None
        
        
    def get_all_users(self):
        self._connect()
        self._cursor.execute('''
            SELECT * FROM Users
        ''')
        users = self._cursor.fetchall()
        self._disconnect()
        return [self._user_to_class(user) for user in users] if len(users) != 0 else None

    
    def get_all_orders(self):
        self._connect()
        self._cursor.execute('''
            SELECT * FROM Orders
        ''')
        orders = self._cursor.fetchall()
        self._disconnect()
        return [self._order_to_class(order) for order in orders] if len(orders) != 0 else None

  
    def get_orders_by_user(self, telegram_id):
        self._connect()
        self._cursor.execute('''
            SELECT * FROM Orders WHERE telegram_id = ?''', (telegram_id,))
        orders = self._cursor.fetchall()
        self._disconnect()
        return [self._order_to_class(order) for order in orders] if len(orders) != 0 else None
        
    #функция для удаления пользователя
    def delete_user(self, telegram_id):
        self._connect()
        self._cursor.execute('''
            DELETE FROM Users WHERE telegram_id = ?
        ''', (telegram_id,))
        self._logger.info(f"Удален пользователь с telegram_id: {telegram_id}")
        self._disconnect()
        
    #функция удаления заказа
    def delete_order(self, order_id):
        self._connect()
        self._cursor.execute('''
            DELETE FROM Orders WHERE id = ?
        ''', (order_id,))
        self._logger.info(f"Удален заказ с id: {order_id}")
        self._disconnect()        
        
    #проверка является ли пользователь администратором
    def is_admin(self, telegram_id):
        user = self.get_user(telegram_id)
        return user is not None and user[4] == 'admin'  # privilege

    #проверка на наличие пользователя в бд
    def user_exists(self, telegram_id):
        self._connect()
        self._cursor.execute('''
            SELECT COUNT(*) FROM Users WHERE telegram_id = ?
        ''', (telegram_id,))
        exists = self._cursor.fetchone()[0] > 0
        self._disconnect()
        return exists

    #возвращает не готовые заказы
    def get_unfinished_orders(self):
        self._connect()
        self._cursor.execute('''
            SELECT * FROM Orders WHERE ready = FALSE
        ''')
        orders = self._cursor.fetchall()
        self._disconnect()
        return [self._order_to_class(order) for order in orders] if len(orders) != 0 else None

    #возвращает готовые заказы
    def get_finished_orders(self):
        self._connect()
        self._cursor.execute('''
            SELECT * FROM Orders WHERE ready = TRUE
        ''')
        orders = self._cursor.fetchall()
        self._disconnect()
        return [self._order_to_class(order) for order in orders] if len(orders) != 0 else None
        
        
    def finish_order(self, order_id):
        self.update_order(order_id, ready = True)
        
        
    def get_picked_orders_by_user(self, user_id):
        self._connect()
        self._cursor.execute('''
            SELECT * FROM Orders WHERE exec_id = ? AND ready = FALSE
        ''', (user_id,))
        orders = self._cursor.fetchall()
        self._disconnect()
        return [self._order_to_class(order) for order in orders] if len(orders) != 0 else None
        
    #функция возвращает заказы без исполнителя
    def get_not_picked_orders(self):
        self._connect()
        self._cursor.execute('''
            SELECT * FROM Orders WHERE exec_id IS NULL
        ''')
        orders = self._cursor.fetchall()
        logger.info(orders)
        self._disconnect()
        return [self._order_to_class(order) for order in orders] if len(orders) != 0 else None
        
    #функция для сохранения исполнителя для заказа
    def set_picked_order(self, order_id, user_id):
        self.update_order(order_id, exec_id = user_id)
        
        
    def ban_user(self, telegram_id, duration_in_seconds):
        ban_time = self._get_time()
        self.update_user(telegram_id, banned=True, ban_time=ban_time, ban_duration=duration_in_seconds)


    def unban_user(self, telegram_id):
        self.update_user(telegram_id, banned=False, ban_time=None, ban_duration=None)


    def is_banned(self, telegram_id):
        user = self.get_user(telegram_id)
        if user is None:
            return False  # Пользователь не существует

        banned = user['banned']  # Статус бана
        ban_time = user['ban_time']  # Время бана
        ban_duration = user['ban_duration']  # Длительность бана

        if not banned:
            return False  # Пользователь не забанен
        
        # Сравниваем текущее время с временем бана
        current_time = self._get_time()

        # Проверка на истечение срока бана
        ban_expiry_time = ban_time + datetime.timedelta(seconds=ban_duration)

        return current_time < ban_expiry_time  # Если текущее время меньше времени истечения, пользователь все еще забанен
        
BotDB = MyDatabase(logger) 