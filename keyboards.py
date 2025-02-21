from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🚀 Начать", callback_data="start")
    ]
])

main = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🚀 Начать", callback_data="start")
    ],
    [
        InlineKeyboardButton(text="👤 Профиль", callback_data="profile")
    ]
])

main_admin = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🚀 Начать", callback_data="start")
    ],
    [
        InlineKeyboardButton(text="👤 Профиль", callback_data="profile")
    ],
    [
        InlineKeyboardButton(text="⚙️ Админ-панель", callback_data="admin_panel")
    ]
])

menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu")
    ]
])

admin_panel = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="✏️ Управление пользователем", callback_data="user_management")
    ]
])

profile = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🛒 Купить подписку", callback_data="subscription_buy")
    ],
    [
        InlineKeyboardButton(text="💳 Пополнение баланса", callback_data="add_balance")
    ]
])


subscription_buy = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🛒 Купить подписку", callback_data="subscription_buy")
    ]
])

subscription_duration = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="📅 7 дней (70₽)", callback_data="7|7 дней|70₽"),
        InlineKeyboardButton(text="📅 14 дней (140₽)", callback_data="14|14 дней|140₽")
    ],
    [
        InlineKeyboardButton(text="📅 30 дней (210₽)", callback_data="30|30 дней|210₽"),
        InlineKeyboardButton(text="📅 60 дней (420₽)", callback_data="60|60 дней|420₽")
    ],
    [
        InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")
    ]
])

user_management = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🎁 Подарить подписку", callback_data="gift_a_sub|🎁 Подарить подписку")
    ],
    [
        InlineKeyboardButton(text="💸 Изменить баланс", callback_data="change_balance|💸 Изменить баланс")
    ]
])

category = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="👤 Жалобы на пользователя", callback_data="report_user")
    ],
    [
        InlineKeyboardButton(text="📢 Жалобы на канал", callback_data="report_channel")
    ],
    [
        InlineKeyboardButton(text="🤖 Жалобы на бота", callback_data="report_bot")
    ],
    [
        InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")
    ]
])

reasons_for_user = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="🚫 Спам", callback_data="spam_user|🚫 Спам"),
        InlineKeyboardButton(text="🔒 Личные данные", callback_data="personal_data_user|🔒 Личные данные")

    ],
    [
        InlineKeyboardButton(text="😈 Троллинг", callback_data="trolling_user|😈 Троллинг"),
        InlineKeyboardButton(text="🗑️ Снос сессий", callback_data="delete_sessions_user|🗑️ Снос сессий")
    ],
    [
        InlineKeyboardButton(text="💎 Премиум", callback_data="premium_user|💎 Премиум"),
        InlineKeyboardButton(text="🌐 Виртуальный номер", callback_data="virtual_number_user|🌐 Виртуальный номер")
    ]
])

reasons_for_channel = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="🔐 Личные данные в ТГК", callback_data="personal_data_channel|🔐 Личные данные в ТГК"),
        InlineKeyboardButton(text="🐾 Живодерство", callback_data="flaying_channel|🐾 Живодерство")
    ],
    [
        InlineKeyboardButton(text="🚫 ЦП", callback_data="cp_channel|🚫 ЦП"),
        InlineKeyboardButton(text="📜 Прайс-лист (DOX & SWAT)", callback_data="price_channel|📜 Прайс-лист (DOX & SWAT)")
    ]
])

reasons_for_bot = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🕵️‍♂️ Осинт бот", callback_data="osint_bot|🕵️‍♂️ Осинт бот")
    ]
])

confirm_mailing_yes_no = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="✅ Да", callback_data="confirm_mailing_yes"),
        InlineKeyboardButton(text="❌ Нет", callback_data="confirm_mailing_no")
    ]
])

confirm_gift_a_sub_yes_no = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="✅ Да", callback_data="confirm_gift_a_sub_yes"),
        InlineKeyboardButton(text="❌ Нет", callback_data="confirm_gift_a_sub_no")
    ]
])

confirm_change_balance_yes_no = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="✅ Да", callback_data="confirm_change_balance_yes"),
        InlineKeyboardButton(text="❌ Нет", callback_data="confirm_change_balance_no")
    ]
])

confirm_add_balance_yes_no = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="✅ Да", callback_data="confirm_add_balance_yes"),
        InlineKeyboardButton(text="❌ Нет", callback_data="confirm_add_balance_no")
    ]
])

confirm_pay_yes_no = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="✅ Да", callback_data="confirm_pay_yes"),
        InlineKeyboardButton(text="❌ Нет", callback_data="confirm_pay_no")
    ]
])

payment_systems = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="💳 Crypto Bot", callback_data="cryptobot_payment|💳 Crypto Bot")
    ]
])

cancel = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")
    ]
])

repeat = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🔄 Повторить", callback_data="start")
    ]
])

stop = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="⛔ Остановить рассылку", callback_data="stop")
    ]
])

pay = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🛒 Перейти к оплате", callback_data="pay")
    ],
    [
        InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")
    ]
])
