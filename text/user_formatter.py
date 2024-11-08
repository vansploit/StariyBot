def add_ord(lst):
    result = "📌Ваш заказ:\n"
    for i in lst:
        result += f" 🔹{i}\n"
    return result
    
    
def user_order(
               order, #id, tg_id, order_list, time, exec_id, ready
               username):

    result = f"📦Заказы пользователя @{username}\n\n"+ f"📌№{order.id}:\n"
    for i in order.order_list:
        result += f" 🔹{i}\n"
    
    result += f"🕰️Дата: {order.time}\n" + "👤Исполнитель: {}\n".format(order.exec_id if order.exec_id != None else "нет") + "❓Готово: {}\n".format("да" if order.ready else "нет")
             
    return result
    
    
def accept_order(order):
    result = f"❓Вы принимаете заказ №{order.id}❓\n"
    for i in order.order_list:
        result += f" 🔹{i}\n"
    
    result += f"🕰️Дата: {order.time}"
             
    return result
    
    
def user_notify(order, user):
    result = f"Ваш заказ №{order.id} принял @{user.username}\nРейтинг исполнителя: {user.rating}⭐️"
    