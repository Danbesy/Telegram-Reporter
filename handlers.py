import logging
import asyncio
from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiosmtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import keyboards as kb
from config import *

# Настройки бота
bot = Bot(TOKEN)

router = Router()

logging.basicConfig(level=logging.INFO)

# Обработчик команды /start
@router.message(CommandStart())
async def cmd_start(message: Message):

    user_id = message.from_user.id

    user_link = f'tg://user?id={user_id}'

    if user_id in ADMINS:
        await message.answer(
            f"<b>👋 Приветствую, <a href='{user_link}'>{message.from_user.full_name}</a> ! Добро пожаловать в бота для автоматической отправки жалоб в Telegram! 🚀</b>\n\n"
            "<b>Используйте кнопки ниже, чтобы начать. 💼</b>",
            parse_mode="HTML",
            reply_markup=kb.start)
    else:
        await message.answer(
            "<b>⛔ Доступ запрещен!</b>\n\n"
            "<b>К сожалению, вы не являетесь авторизованным пользователем данного бота.</b>",
            parse_mode="HTML")

class Mailing(StatesGroup):
    category = State()
    confirm = State()

class ReportUser(StatesGroup):
    username = State()
    telegram_id = State()
    chat_link = State()
    link_for_user = State()
    reasons = State()

@router.callback_query(F.data == "start")
async def start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "<b>📂 Выберите нужную категорию, для отправки жалоб:</b>",
        parse_mode="HTML",
        reply_markup=kb.category)
        
    await state.set_state(Mailing.category)

@router.callback_query(F.data == "report_user")
async def report_user(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "<b>📝 Для начала введите имя пользователя (например, @username):</b>",
        parse_mode="HTML",
        reply_markup=kb.cancel)

    await state.set_state(ReportUser.username)

@router.message(ReportUser.username)
async def get_username(message: Message, state: FSMContext):

    username = message.text
    await state.update_data(username=username)

    await message.answer(
        f"<b>👤 Введенное вами имя пользователя:</b> <code>{username}</code>\n\n"
        "<b>📝 Теперь введите Telegram ID:</b>",
        parse_mode="HTML",
        reply_markup=kb.cancel)

    await state.set_state(ReportUser.telegram_id)

@router.message(ReportUser.telegram_id)
async def get_telegram_id(message: Message, state: FSMContext):

    telegram_id = message.text
    await state.update_data(telegram_id=telegram_id)

    data = await state.get_data()
    username = data.get('username')

    await message.answer(
        f"<b>👤 Имя пользователя: </b> <code>{username}</code>\n"
        f"<b>🆔 Telegram ID:</b> <code>{telegram_id}</code>\n\n"
        "<b>🔗 Введите ссылку (@username) или ID на чат с нарушением:</b>",
        parse_mode="HTML",
        reply_markup=kb.cancel)

    await state.set_state(ReportUser.chat_link)

@router.message(ReportUser.chat_link)
async def get_chat_link(message: Message, state: FSMContext):

    chat_link = message.text
    await state.update_data(chat_link=chat_link)

    data = await state.get_data()
    username = data.get('username')
    telegram_id = data.get('telegram_id')

    await message.answer(
        f"<b>👤 Имя пользователя:</b> <code>{username}</code>\n"
        f"<b>🆔 Telegram ID:</b> <code>{telegram_id}</code>\n"
        f"<b>🔗 Ссылка на чат с нарушением:</b> <code>{chat_link}</code>\n\n"
        "<b>⚠️ Теперь укажите ссылку на нарушение:</b>",
        parse_mode="HTML",
        reply_markup=kb.cancel)

    await state.set_state(ReportUser.link_for_user)

@router.message(ReportUser.link_for_user)
async def get_link(message: Message, state: FSMContext):
    
    link_for_user = message.text
    await state.update_data(link_for_user=link_for_user)

    data = await state.get_data()

    username = data.get('username')
    telegram_id = data.get('telegram_id')
    chat_link = data.get('chat_link')

    await message.answer(
        f"<b>👤 Имя пользователя:</b> <code>{username}</code>\n"
        f"<b>🆔 Telegram ID:</b> <code>{telegram_id}</code>\n"
        f"<b>🔗 Ссылка на чат с нарушением:</b> <code>{chat_link}</code>\n"
        f"<b>⚠️ Ссылка на нарушение:</b> <code>{link_for_user}</code>\n\n"
        "<b>📋 Выберите причину жалобы:</b>",
        parse_mode="HTML",
        reply_markup=kb.reasons_for_user)

    await state.set_state(ReportUser.reasons)

@router.callback_query(ReportUser.reasons)
async def get_reason(callback: CallbackQuery, state: FSMContext):

    callback_data = callback.data
    reason = callback_data.split("|")[1]
    await state.update_data(reason=reason)

    data = await state.get_data()
    username = data.get('username')
    telegram_id = data.get('telegram_id')
    chat_link = data.get('chat_link')
    link_for_user = data.get('link_for_user')

    await callback.message.answer(
        "<b>🔍 Пожалуйста, проверьте введенные данные:</b>\n\n"
        f"<b>👤 Имя пользователя:</b> <code>{username}</code>\n"
        f"<b>🆔 Telegram ID:</b> <code>{telegram_id}</code>\n"
        f"<b>🔗 Ссылка на чат с нарушением:</b> <code>{chat_link}</code>\n"
        f"<b>⚠️ Ссылка на нарушение:</b> <code>{link_for_user}</code>\n"
        f"<b>📋 Причина жалобы:</b> <code>{reason}</code>\n\n"
        "<b>➡️ Желаете продолжить?</b>",
        parse_mode="HTML",
        reply_markup=kb.confirm_yes_no)
    
    await state.set_state(Mailing.confirm)

class ReportChannel(StatesGroup):
    channel = State()
    link_for_channel = State()
    reasons = State()

@router.callback_query(F.data == "report_channel")
async def report_channel(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "<b>📝 Для начала введите ссылку на канал (@username или его ID):</b>",
        parse_mode="HTML",
        reply_markup=kb.cancel)
        
    await state.set_state(ReportChannel.channel)

@router.message(ReportChannel.channel)
async def get_channel(message: Message, state: FSMContext):

    channel = message.text  
    await state.update_data(channel=channel)

    await message.answer(
        f"<b>🔗 Введенная вами ссылка на канал:</b> <code>{channel}</code>\n\n"
        "<b>⚠️ Теперь укажите ссылку на нарушение:</b>",
        parse_mode="HTML",
        reply_markup=kb.cancel)

    await state.set_state(ReportChannel.link_for_channel)

@router.message(ReportChannel.link_for_channel)
async def get_link(message: Message, state: FSMContext):

    link_for_channel = message.text
    await state.update_data(link_for_channel=link_for_channel)

    data = await state.get_data()

    channel = data.get('channel')

    await message.answer(
        f"<b>📢 Ссылка на канал:</b> <code>{channel}</code>\n"
        f"<b>🔗 Ссылка на нарушение:</b> <code>{link_for_channel}</code>\n\n"
        "<b>⚠️ Выберите причину жалобы:</b>",
        parse_mode="HTML",
        reply_markup=kb.reasons_for_channel)

    await state.set_state(ReportChannel.reasons)

@router.callback_query(ReportChannel.reasons)
async def get_reason(callback: CallbackQuery, state: FSMContext):

    callback_data = callback.data
    reason = callback_data.split("|")[1]
    await state.update_data(reason=reason)

    data = await state.get_data()
    channel = data.get('channel')
    link_for_channel = data.get('link_for_channel')

    await callback.message.answer(
        "<b>🔍 Пожалуйста, проверьте введенные данные:</b>\n\n"
        f"<b>📢 Ссылка на канал:</b> <code>{channel}</code>\n"
        f"<b>🔗 Ссылка на нарушение:</b> <code>{link_for_channel}</code>\n"
        f"<b>⚠️ Причина жалобы:</b> <code>{reason}</code>\n\n"
        "<b>➡️ Желаете продолжить?</b>",
        parse_mode="HTML",
        reply_markup=kb.confirm_yes_no)

    await state.set_state(Mailing.confirm)

class ReportBot(StatesGroup):
    username_bot = State()
    reasons = State()

@router.callback_query(F.data == "report_bot")
async def report_bot(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "<b>📝 Введите имя бота (@username):</b>",
        parse_mode="HTML",
        reply_markup=kb.cancel)

    await state.set_state(ReportBot.username_bot)

@router.message(ReportBot.username_bot)
async def get_username_bot(message: Message, state: FSMContext):

    username_bot = message.text
    await state.update_data(username_bot=username_bot)

    await message.answer(
        f"<b>🤖 Ввёденное вами имя бота:</b> <code>{username_bot}</code>\n\n"
        "<b>⚠️ Теперь выберите причину для жалобы:</b>",
        parse_mode="HTML",
        reply_markup=kb.reasons_for_bot)

    await state.set_state(ReportBot.reasons)

@router.callback_query(ReportBot.reasons)
async def get_reason(callback: CallbackQuery, state: FSMContext):

    callback_data = callback.data
    reason = callback_data.split("|")[1]
    await state.update_data(reason=reason)

    data = await state.get_data()
    username_bot = data.get('username_bot')

    await callback.message.answer(
        "<b>🔍 Пожалуйста, проверьте введенные данные:</b>\n\n"
        f"<b>🤖 Имя бота:</b> <code>{username_bot}</code>\n"
        f"<b>⚠️ Причина жалобы:</b> <code>{reason}</code>\n\n"
        "<b>➡️ Хотите продолжить?</b>",
        parse_mode="HTML",
        reply_markup=kb.confirm_yes_no)

    await state.set_state(Mailing.confirm)

# Список почт для рассылки
mailing_list = [
    'sms@telegram.org',
    'dmca@telegram.org',
    'abuse@telegram.org',
    'sticker@telegram.org',
    'support@telegram.org'
]

# SMTP настройки
DELAY = 2 # Задержка в секундах

# Обработчик коллбеков для подтверждения (Yes/No)
@router.callback_query(F.data.startswith("confirm_"))
async def confirm_callback(callback: CallbackQuery, state: FSMContext):
    # Получаем все сохраненные данные
    data = await state.get_data()
    username = data.get('username')
    telegram_id = data.get('telegram_id')
    chat_link = data.get('chat_link')
    link_for_user = data.get('link_for_user')
    channel = data.get('channel')
    link_for_channel = data.get('link_for_channel')
    username_bot = data.get('username_bot')
    reason = data.get('reason')

    # Словарь с текстами для репортов
    REPORT_TEXTS = {
    "spam_user": f"Здравствуйте, уважаемая поддержка. На вашей платформе я нашел пользователя, который отправляет много ненужных сообщений - СПАМ. Его юзернейм - {username}, его айди - {telegram_id}, ссылка на чат - {chat_link}, ссылка на нарушение/нарушения - {link_for_user}. Пожалуйста, примите меры по отношению к данному пользователю.",
    "personal_data_user": f"Здравствуйте, уважаемая поддержка. На вашей платформе я нашел пользователя, который распространяет чужие данные без их согласия. Его юзернейм - {username}, его айди - {telegram_id}, ссылка на чат - {chat_link}, ссылка на нарушение/нарушения - {link_for_user}. Пожалуйста, примите меры по отношению к данному пользователю путем блокировки его акккаунта.",
    "trolling_user": f"Здравствуйте, уважаемая поддержка Telegram. Я нашел пользователя, который открыто выражается нецензурной лексикой и спамит в чатах. Его юзернейм - {username}, его айди - {telegram_id}, ссылка на чат - {chat_link}, ссылка на нарушение/нарушения - {link_for_user}. Пожалуйста, примите меры по отношению к данному пользователю путем блокировки его акккаунта.",
    "delete_sessions_user": f"Здравствуйте, уважаемая поддержка. Я случайно перешел по фишинговой ссылке и утерял доступ к своему аккаунту. Его юзернейм - {username}, его айди - {telegram_id}. Пожалуйста, удалите аккаунт или обнулите сессии",
    "premium_user": f"Здравствуйте, уважаемая поддержка Telegram.! Аккаунт {username}, {telegram_id} приобрёл Premium подписку в вашем мессенджере, чтобы рассылать спам-сообщения и обходить ограничения Telegram. Прошу проверить данную жалобу и принять меры!",
    "virtual_number_user": f"Здравствуйте, уважаемая поддержка Telegram! Аккаунт {username}, {telegram_id} использует виртуальный номер купленный на сайте по активации номеров. Отношения к номеру он не имеет, номер никак к нему не относится. Пожалуйста, разберитесь с этим. Заранее спасибо!",
    "personal_data_channel": f"Здравствуйте, уважаемая поддержка Telegram. На вашей платформе я нашел канал, который распространяет личные данные невинных людей. Ссылка на канал - {channel}, Ссылка на нарушение - {link_for_channel}. Пожалуйста, заблокируйте данный канал.",
    "flaying_channel": f"Здравствуйте, уважаемая поддержка Telegram. На вашей платформе я нашел канал который распространяет жестокое обращение с животными. Ссылка на канал - {channel}, Ссылка на нарушение - {link_for_channel}. Пожалуйста, заблокируйте данный канал.",
    "cp_channel": f"Здравствуйте, уважаемая поддержка Telegram. На вашей платформе я нашел канал который распространяет порнографию с участием несовершеннолетних. Ссылка на канал - {channel}, Ссылка на нарушение - {link_for_channel}. Пожалуйста, заблокируйте данный канал.",
    "price_channel": f"Здравствуйте, уважаемый модератор Telegram. Хочу вам пожаловаться на канал, который продает услуги доксинга и сваттинга. Ссылка на телеграмм канал: {channel} Ссылка на нарушение: {link_for_channel} Просьба заблокировать данный канал.",
    "osint_bot": f"Здравствуйте, уважаемая поддержка Telegram. На вашей платформе я нашел бота, который осуществляет поиск по личным данным ваших пользователей. Ссылка на бота - {username_bot}. Пожалуйста, разберитесь и заблокируйте данного бота."
    }

    # Маппинг для соответствия строк с эмодзи и другими значениями на правильные ключи в REPORT_TEXTS
    reason_map = {
        "🚫 Спам": "spam_user",
        "🔒 Личные данные": "personal_data_user",
        "😈 Троллинг": "trolling_user",
        "🗑️ Снос сессий": "delete_sessions_user",
        "💎 Премиум": "premium_user",
        "🌐 Виртуальный номер": "virtual_number_user",
        "🔐 Личные данные в ТГК": "personal_data_channel",
        "🐾 Живодерство": "flaying_channel",
        "🚫 ЦП": "cp_channel",
        "📜 Прайс-лист (DOX & SWAT)": "price_channel",
        "🕵️‍♂️ Осинт бот": "osint_bot"
    }

# Пример для добавления почты:
    
# accounts = {
#     'mail1@gmail.com': {
#         'password': 'pass1',
#         'smtp_server': 'smtp.gmail.com',
#         'smtp_port': 465
#     },
#     'mail2@gmail.com': {
#         'password': 'pass2',
#         'smtp_server': 'smtp.gmail.com',
#         'smtp_port': 465
#     },
#     'mail3@gmail.com': {
#         'password': 'pass3',
#         'smtp_server': 'smtp.gmail.com',
#         'smtp_port': 465
#     },
#     # Продолжайте добавлять данные для остальных почт
# }

    accounts = {
        'mail1@gmail.com': {
            'password': 'pass1',
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 465
        },
        'mail2@gmail.com': {
            'password': 'pass2',
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 465
        },
        'mail3@gmail.com': {
            'password': 'pass3',
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 465
        }
    }

    async def send_email(account_email, recipient, subject, body):
        """
        Функция для отправки письма с индивидуальными настройками SMTP
        """
        # Извлечение данных аккаунта
        account_info = accounts.get(account_email)
        if not account_info:
            raise ValueError(f"Конфигурация аккаунта для {account_email} не найдена")

        password = account_info["password"]
        smtp_server = account_info["smtp_server"]
        smtp_port = account_info["smtp_port"]

        # Создание сообщения
        message = MIMEMultipart()
        message["From"] = account_email
        message["To"] = recipient
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Используем индивидуальные настройки SMTP
        async with SMTP(hostname=smtp_server, port=smtp_port, use_tls=True) as smtp:
            await smtp.login(account_email, password)
            await smtp.send_message(message)

    async def distribute_emails(callback: CallbackQuery, reason, data):
        """
        Функция для рассылки писем
        """
        global stop_mailing
        stop_mailing = False  # Сбрасываем флаг перед началом рассылки

        for account_email in accounts.keys():  # Перебираем аккаунты
            if stop_mailing:  # Проверяем флаг перед началом обработки аккаунта
                break

            for recipient in mailing_list:
                if stop_mailing:  # Проверяем флаг перед отправкой каждого письма
                    break

                text = REPORT_TEXTS[reason].format(**data)
                subject = "Жалоба от пользователя"

                try:
                    # Отправка письма
                    await send_email(account_email, recipient, subject, text)

                    await callback.message.answer(
                        f"<b>✅ Письмо отправлено с {account_email} на {recipient}</b>",
                        parse_mode="HTML",
                        reply_markup=kb.stop
                    )

                except Exception as e:
                    from html import escape
                    await callback.message.answer(
                        f"<b>❌ Не удалось отправить письмо с {account_email} на {recipient}: {escape(str(e))}</b>",
                        parse_mode="HTML",
                        reply_markup=kb.stop
                    )

                await asyncio.sleep(DELAY)  # Задержка между отправками

    if callback.data == "confirm_yes":
        await callback.message.answer(
            "<b>✅ Отправка жалоб успешно начата!</b>",
            parse_mode="HTML",
            reply_markup=kb.stop)

        reason = reason_map.get(reason, reason)

        await distribute_emails(callback, reason, data)

        await state.clear()

    elif callback.data == "confirm_no":
        await callback.message.answer(
            "<b>❌ Вы отменили процесс. Используйте кнопку ниже, чтобы начать заново.</b>",
            parse_mode="HTML",
            reply_markup=kb.start
        )
        await state.clear()

@router.callback_query(F.data == "cancel")
async def cancel(callback: CallbackQuery, state: FSMContext):

    await state.clear()

    await callback.message.answer(
        "<b>❌ Действие успешно отменено.</b>",
        parse_mode="HTML",
        reply_markup=kb.repeat)
    
@router.callback_query(F.data == "stop")
async def stop(callback: CallbackQuery):

    global stop_mailing
    stop_mailing = True
    await callback.message.answer(
        "<b>⛔ Рассылка успешно остановлена.</b>",
        parse_mode="HTML",
        reply_markup=kb.repeat)