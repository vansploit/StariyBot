def add_ord(lst):
    result = "📌Ваш заказ:\n"
    for i in lst:
        result += f" 🔹{i}\n"
    return result
    
    
def user_order(
               dict, #id, tg_id, order_list, time, exec_id, ready
               username):

    result = f"📦Заказы пользователя @{username}\n\n"+ f"📌№{dict['id']}:\n"
    for i in dict['order_list']:
        result += f" 🔹{i}\n"
    
    result += f"🕰️Дата: {dict['time']}\n" + "👤Исполнитель: {}\n".format(dict['exec_id'] if dict['exec_id'] != None else "нет") + "❓Готово: {}\n".format("да" if dict['ready'] else "нет")
             
    return result
    
    
def accept_order(order):
    result = f"❓Вы принимаете заказ №{order['id']}❓\n"
    for i in order['order_list']:
        result += f" 🔹{i}\n"
    
    result += f"🕰️Дата: {order['time']}"
             
    return result