from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🚀 Начать", callback_data="start")
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

confirm_yes_no = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="✅ Да", callback_data="confirm_yes"),
        InlineKeyboardButton(text="❌ Нет", callback_data="confirm_no")
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