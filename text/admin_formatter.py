def user(lst):
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
    id = lst['id'],
    tg_id = lst['tg_id'],
    username = lst['username'],
    nickname = lst['nickname'],
    privilege = lst['privilege'],
    banned = lst['banned'],
    ban_time = lst['ban_time'],
    ban_duration = lst['ban_duration'],
    rating = lst['rating'],
    transfer_details = lst['transfer_details'])
    
    return result