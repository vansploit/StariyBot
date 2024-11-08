order_temp = "🤷‍♂️Нет {} заказов🤷‍♂️"

no_users = "🤷‍♂️Нет пользователей🤷‍♂️"

no_orders = order_temp.replace(" ", "").format(" ")
no_accepted_orders = order_temp.format("принятых")
no_available_orders = order_temp.format("доступных")