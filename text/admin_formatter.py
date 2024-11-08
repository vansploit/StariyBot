def user(order):
    result = (
        "📌Пользователь #{id}"
        "👤Телеграм id: {tg_id}"
        "🗣️Имя пользователя: {username}"
        "🥸Никнейм: {nickname}"
        "🛡️Права: {privilege}"
        "⛔Баны: {banned}"
        "⌛Время бана: {ban_time}"
        "⏳На сколько: {ban_duration}"
        "⭐Рейтинг: {rating}"
        "💳Данные для перевода: {transfer_details}"
        ).format(
    id = order.id,
    tg_id = order.tg_id,
    username = order.username,
    nickname = order.nickname,
    privilege = order.privilege,
    banned = order.banned,
    ban_time = order.ban_time,
    ban_duration = order.ban_duration,
    rating = order.rating,
    transfer_details = order.transfer_details)
    
    return result