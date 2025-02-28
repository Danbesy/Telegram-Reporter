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
    ],
    [
        InlineKeyboardButton(text="🔞 Порнография (18+)", callback_data="pornography_channel|🔞 Порнография (18+)"),
        InlineKeyboardButton(text="🩸 Насилие", callback_data="violence_channel|🩸 Насилие")
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

change_language_ru = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="🇺🇸 English", callback_data="select_language_en"),
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="select_language_ru")
    ]
])

start_en = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🚀 Start", callback_data="start")
    ]
])

main_en = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🚀 Start", callback_data="start")
    ],
    [
        InlineKeyboardButton(text="👤 Profile", callback_data="profile")
    ]
])

main_admin_en = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🚀 Start", callback_data="start")
    ],
    [
        InlineKeyboardButton(text="👤 Profile", callback_data="profile")
    ],
    [
        InlineKeyboardButton(text="⚙️ Admin-panel", callback_data="admin_panel")
    ]
])

menu_en = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🏠 Main menu", callback_data="menu")
    ]
])

admin_panel_en = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="✏️ User management", callback_data="user_management")
    ]
])

profile_en = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🛒 Buy a subscription", callback_data="subscription_buy")
    ],
    [
        InlineKeyboardButton(text="💳 Top up balance", callback_data="add_balance")
    ]
])


subscription_buy_en = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🛒 Buy a subscription", callback_data="subscription_buy")
    ]
])

subscription_duration_en = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="📅 7 days (70₽)", callback_data="7|7 days|70₽"),
        InlineKeyboardButton(text="📅 14 days (140₽)", callback_data="14|14 days|140₽")
    ],
    [
        InlineKeyboardButton(text="📅 30 days (210₽)", callback_data="30|30 days|210₽"),
        InlineKeyboardButton(text="📅 60 days (420₽)", callback_data="60|60 days|420₽")
    ],
    [
        InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")
    ]
])

user_management_en = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🎁 Give a subscription", callback_data="gift_a_sub|🎁 Give a subscription")
    ],
    [
        InlineKeyboardButton(text="💸 Change balance", callback_data="change_balance|💸 Change balance")
    ]
])

category_en = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="👤 Report user", callback_data="report_user")
    ],
    [
        InlineKeyboardButton(text="📢 Report channel", callback_data="report_channel")
    ],
    [
        InlineKeyboardButton(text="🤖 Report bot", callback_data="report_bot")
    ],
    [
        InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")
    ]
])

reasons_for_user_en = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="🚫 Spam", callback_data="spam_user_en|🚫 Spam"),
        InlineKeyboardButton(text="🔒 Personal data", callback_data="personal_data_user_en|🔒 Personal data")

    ],
    [
        InlineKeyboardButton(text="😈 Trolling", callback_data="trolling_user_en|😈 Trolling"),
        InlineKeyboardButton(text="🗑️ Delete sessions", callback_data="delete_sessions_user_en|🗑️ Delete sessions")
    ],
    [
        InlineKeyboardButton(text="💎 Premium", callback_data="premium_user_en|💎 Premium"),
        InlineKeyboardButton(text="🌐 Virtual number", callback_data="virtual_number_user_en|🌐 Virtual number")
    ]
])

reasons_for_channel_en = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="🔐 Personal data in chahnel", callback_data="personal_data_channel_en|🔐 Personal data in chahnel"),
        InlineKeyboardButton(text="🐾 Flaying", callback_data="flaying_channel_en|🐾 Flaying")
    ],
    [
        InlineKeyboardButton(text="🚫 CP", callback_data="cp_channel_en|🚫 CP"),
        InlineKeyboardButton(text="📜 Price-list (DOX & SWAT)", callback_data="price_channel_en|📜 Price-list (DOX & SWAT)")
    ],
    [
        InlineKeyboardButton(text="🔞 Pornography (18+)", callback_data="pornography_channel_en|🔞 Pornography (18+)"),
        InlineKeyboardButton(text="🩸 Violence", callback_data="violence_channel_en|🩸 Violence")
    ]
])

reasons_for_bot_en = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🕵️‍♂️ Osint bot", callback_data="osint_bot_en|🕵️‍♂️ Osint bot")
    ]
])

confirm_mailing_yes_no_en = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="✅ Yes", callback_data="confirm_mailing_yes"),
        InlineKeyboardButton(text="❌ No", callback_data="confirm_mailing_no")
    ]
])

confirm_gift_a_sub_yes_no_en = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="✅ Yes", callback_data="confirm_gift_a_sub_yes"),
        InlineKeyboardButton(text="❌ No", callback_data="confirm_gift_a_sub_no")
    ]
])

confirm_change_balance_yes_no_en = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="✅ Yes", callback_data="confirm_change_balance_yes"),
        InlineKeyboardButton(text="❌ No", callback_data="confirm_change_balance_no")
    ]
])

confirm_add_balance_yes_no_en = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="✅ Yes", callback_data="confirm_add_balance_yes"),
        InlineKeyboardButton(text="❌ No", callback_data="confirm_add_balance_no")
    ]
])

confirm_pay_yes_no_en = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="✅ Yes", callback_data="confirm_pay_yes"),
        InlineKeyboardButton(text="❌ No", callback_data="confirm_pay_no")
    ]
])

payment_systems_en = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="💳 Crypto Bot", callback_data="cryptobot_payment|💳 Crypto Bot")
    ]
])

cancel_en = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")
    ]
])

repeat_en = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🔄 Repeat", callback_data="start")
    ]
])

stop_en = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="⛔ Stop mailing", callback_data="stop")
    ]
])

pay_en = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🛒 Go to payment", callback_data="pay")
    ],
    [
        InlineKeyboardButton(text="❌ Cancel", callback_data="cancel")
    ]
])

change_language_en = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="select_language_ru"),
        InlineKeyboardButton(text="🇺🇸 English", callback_data="select_language_en")
    ]
])
