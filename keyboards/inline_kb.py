from aiogram.utils.keyboard import InlineKeyboardBuilder

class BotInlineKB:
    def __init__(self, logger):
        self._logger = logger
        self.start = self._get_start_kb()
        self.exit = self._get_exit_kb()
        self.back = self._get_back_button()
        self.admin_panel = self._get_admin_panel()
        self.admin_users = self._get_admin_users()
        self.confirm = self._get_confirm()
        
        
    def _get_start_kb(self):
        builder = InlineKeyboardBuilder()
        builder.button(text="📖Профиль", callback_data="profile")
        builder.button(text="✏️Заказать", callback_data="order_add")
        builder.button(text="📋Мои заказы", callback_data="orders_list")
        builder.button(text="🛒Взять заказ", callback_data = "get_order")
        builder.button(text="📘Приняте заказы", callback_data = "all_accepted_orders")
        builder.adjust(1, 2, 1, 1)
        return builder.as_markup()
        
    def _get_exit_kb(self):
        builder = InlineKeyboardBuilder()
        builder.button(text="🏠В меню", callback_data="menu")
        return builder.as_markup()
        
    def _get_admin_panel(self):
        builder = InlineKeyboardBuilder()
        builder.button(text="📊Статистика📊", callback_data="a_statistics")
        builder.button(text="👥Список пользователей👥", callback_data="a_users")
        builder.button(text="🛒Список заказов🛒", callback_data="a_orders")
        builder.adjust(1)
        return builder.as_markup()
        
    def _get_admin_users(self):
        builder = InlineKeyboardBuilder()
        builder.button(text="⚙️Изменить", callback_data="a_edit_user")
        builder.button(text="⛔Забанить", callback_data="a_ban_user")
        builder.button(text="❌Удалить", callback_data="a_delete_user")  
        builder.attach(InlineKeyboardBuilder.from_markup(self.exit))   
        builder.adjust(1, 2)
        return builder.as_markup()
        
    def _get_back_button(self):
        builder = InlineKeyboardBuilder()
        builder.button(text="🔙Назад", callback_data="back")
        return builder.as_markup()
        
    def _get_pages(self, page):
        builder = InlineKeyboardBuilder()
        if page == 'start':
            builder.button(
                text="#",
                callback_data="empty")
            builder.button(
                text=">>>",
                callback_data="next_page")
        elif page == 'end':
            builder.button(
                text="<<<",
                callback_data="prev_page")
            builder.button(
                text="#",
                callback_data="empty")
        else:
            builder.button(
                text="<<<",
                callback_data="prev_page")
            builder.button(
                text=">>>",
                callback_data="next_page")
        builder.adjust(2)
        return builder
        
    def _get_confirm(self):
        builder = InlineKeyboardBuilder()
        builder.button(text="✅Подтвердить", callback_data="confirm")
        builder.button(text="❌Отменить", callback_data="cancel")
        builder.adjust(2)
        return builder.as_markup()
        
    def get_orders_editor(self, page='middle'):
        builder = InlineKeyboardBuilder()
        builder.attach(self._get_pages(page))
        builder.button(text="⚙️Изменить", callback_data="edit_order")
        builder.button(text="❌Удалить", callback_data="delete_order")
        builder.attach(InlineKeyboardBuilder.from_markup(self.exit))
        builder.adjust(2, 2, 1)
        return builder.as_markup()