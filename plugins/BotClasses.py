from bot_logger import logger

class User:
    
    def __init__(self):
        self.id = None
        self.tg_id = None
        self.username = None
        self.nickname = None
        self.privilege = None
        self.banned = False
        self.ban_time = None
        self.ban_duration = None
        self.rating = None
        self.transfer_details = None
        
    def put_data(self, data):
        if len(data) == 10:
            (self.id,
             self.tg_id,
             self.username,
             self.nickname,
             self.privilege,
             self.banned, 
             self.ban_time,
             self.ban_duration,
             self.rating,
             self.transfer_details) = data
        else:
            logger.error("User.put_data принимает список длиной 9")


class Order:
    
    def __init__(self):
        self.id = None
        self.tg_id = None
        self.order_list = None
        self.time = None
        self.exec_id = None
        self.ready = None
        
        
    def put_data(self, data):
        if len(data) == 6:
            (self.id,
             self.tg_id,
             self.order_list,
             self.time,
             self.exec_id,
             self.ready) = data
            self.order_list = self.order_list.split("/")
        else:
            logger.error("Order.put_data принимает список длинной 6")