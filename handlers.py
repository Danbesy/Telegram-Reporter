#     ____                        _____                    _                                # Telegram - https://t.me/danbesy
#    |  _ \               ____   |  __ \                  | |                               # Telegram Channel - https://t.me/Danbesy_Dev
#    | |_) |  _   _      / __ \  | |  | |   __ _   _ __   | |__     ___   ___   _   _       # Telegram Bio - https://Danbesy_Bio
#    |  _ <  | | | |    / / _` | | |  | |  / _` | | '_ \  | '_ \   / _ \ / __| | | | |      # GitHub - https://github.com/Danbesy
#    | |_) | | |_| |   | | (_| | | |__| | | (_| | | | | | | |_) | |  __/ \__ \ | |_| |      # GitHub - https://github.com/Danbesy
#    |____/   \__, |    \ \__,_| |_____/   \__,_| |_| |_| |_.__/   \___| |___/  \__, |      # Telegram Bio - https://Danbesy_Bio
#             __/ |     \____/                                                  __/ |       # Telegram Channel - https://t.me/Danbesy_Dev
#            |___/                                                             |___/        # Telegram - https://t.me/danbesy

import logging
import asyncio
import time
import uuid
import keyboards as kb
from config import *
from db import *
from datetime import datetime
from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiosmtplib import SMTP
from aiocryptopay import AioCryptoPay, Networks
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Настройки бота
bot = Bot(TOKEN)

router = Router()

# Иницилизация CryptoPay
acp = AioCryptoPay(token=CRYPTOPAY_TOKEN, network=Networks.MAIN_NET)

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.message(CommandStart())
async def cmd_start(message: Message):

    # Инициализация базы данных
    await init_users_db()
    await init_logs_payments_db()

    user_id = message.from_user.id
    user_link = f'tg://user?id={user_id}'

    if user_id in ADMINS:
        await message.answer(
            f"<b>👋 Приветствую, </b><a href='{user_link}'>{message.from_user.full_name}</a> !\n\n"
            "<b>Добро пожаловать в бота для автоматической отправки жалоб в Telegram! 🚀</b>\n\n"
            "<b>Используйте кнопки ниже, чтобы начать. 💼</b>",
            parse_mode="HTML",
            reply_markup=kb.main_admin)  
    else:
        await message.answer(
            f"<b>👋 Приветствую, </b><a href='{user_link}'>{message.from_user.full_name}</a> !\n\n"
            "<b>Добро пожаловать в бота для автоматической отправки жалоб в Telegram! 🚀</b>\n\n"
            "<b>Используйте кнопки ниже, чтобы начать. 💼</b>",
            parse_mode="HTML",
            reply_markup=kb.main)

    if not await user_exists(user_id):
        registration_date = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        await add_user(user_id, registration_date)

@router.callback_query(F.data == "menu")
async def menu(callback: CallbackQuery):

    await callback.answer()

    user_id = callback.from_user.id

    user_link = f'tg://user?id={user_id}'

    if user_id in ADMINS:
        await callback.message.answer(
            f"<b>👋 Приветствую, </b><a href='{user_link}'>{callback.from_user.full_name}</a> !\n\n"
            "<b>Добро пожаловать в бота для автоматической отправки жалоб в Telegram! 🚀</b>\n\n"
            "<b>Используйте кнопки ниже, чтобы начать. 💼</b>",
            parse_mode="HTML",
            reply_markup=kb.main_admin)      
    else:
        await callback.message.answer(
            f"<b>👋 Приветствую,</b><a href='{user_link}'>{callback.from_user.full_name}</a>!\n\n"
            "<b>Добро пожаловать в бота для автоматической отправки жалоб в Telegram! 🚀</b>\n\n"
            "<b>Используйте кнопки ниже, чтобы начать. 💼</b>",
            parse_mode="HTML",
            reply_markup=kb.main)

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

    await callback.answer()

    user_id = callback.from_user.id

    subscription_datetime = await get_subscription_datetime(user_id)

    current_timestamp = int(time.time())

    if subscription_datetime > current_timestamp or user_id in ADMINS:

        await callback.answer()

        await callback.message.answer(
            "<b>📂 Выберите нужную категорию, для отправки жалоб:</b>",
            parse_mode="HTML",
            reply_markup=kb.category)
        await state.set_state(Mailing.category)
    else:
        await callback.answer()    

        await callback.message.answer(
            "<b>⛔ Доступ запрещен!</b>\n\n"
            "<b>У вас отсутствует активная подписка. Пожалуйста, оформите подписку, чтобы получить доступ.</b>",
            parse_mode="HTML",
            reply_markup=kb.subscription_buy)

@router.callback_query(F.data == "report_user")
async def report_user(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    await callback.message.answer(
        "<b>📝 Для начала введите Username пользователя:</b>",
        parse_mode="HTML",  
        reply_markup=kb.cancel)

    await state.set_state(ReportUser.username)

@router.message(ReportUser.username)
async def get_username(message: Message, state: FSMContext):

    username = message.text
    await state.update_data(username=username)

    await message.answer(
        f"<b>👤 Введенный Вами Username:</b> <code>{username}</code>\n\n"
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
        f"<b>👤 Username:</b> <code>{username}</code>\n"
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
        f"<b>👤 Username:</b> <code>{username}</code>\n"
        f"<b>🆔 Telegram ID:</b> <code>{telegram_id}</code>\n"
        f"<b>🔗 Ссылка на чат:</b> <code>{chat_link}</code>\n\n"
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
        f"<b>👤 Username:</b> <code>{username}</code>\n"
        f"<b>🆔 Telegram ID:</b> <code>{telegram_id}</code>\n"
        f"<b>🔗 Ссылка на чат:</b> <code>{chat_link}</code>\n"
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
        f"<b>👤 Username:</b> <code>{username}</code>\n"
        f"<b>🆔 Telegram ID:</b> <code>{telegram_id}</code>\n"
        f"<b>🔗 Ссылка на чат:</b> <code>{chat_link}</code>\n"
        f"<b>⚠️ Ссылка на нарушение:</b> <code>{link_for_user}</code>\n"
        f"<b>📋 Причина жалобы:</b> <code>{reason}</code>\n\n"
        "<b>➡️ Желаете продолжить?</b>",
        parse_mode="HTML",
        reply_markup=kb.confirm_mailing_yes_no)
    
    await state.set_state(Mailing.confirm)

class ReportChannel(StatesGroup):
    channel = State()
    link_for_channel = State()
    reasons = State()

@router.callback_query(F.data == "report_channel")
async def report_channel(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    await callback.message.answer(
        "📝 Для начала введите ссылку на канал (@username) или его ID:",
        parse_mode="HTML",
        reply_markup=kb.cancel)
        
    await state.set_state(ReportChannel.channel)

@router.message(ReportChannel.channel)
async def get_channel(message: Message, state: FSMContext):

    channel = message.text  
    await state.update_data(channel=channel)

    await message.answer(
        f"<b>🔗 Введенная Вами ссылка на канал:</b> <code>{channel}</code>\n\n"
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

    await callback.answer()

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
        reply_markup=kb.confirm_mailing_yes_no)

    await state.set_state(Mailing.confirm)

class ReportBot(StatesGroup):
    username_bot = State()
    reasons = State()

@router.callback_query(F.data == "report_bot")
async def report_bot(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    await callback.message.answer(
        "<b>📝 Введите Username бота:</b>",
        parse_mode="HTML",
        reply_markup=kb.cancel)

    await state.set_state(ReportBot.username_bot)

@router.message(ReportBot.username_bot)
async def get_username_bot(message: Message, state: FSMContext):

    username_bot = message.text
    await state.update_data(username_bot=username_bot)

    await message.answer(
        f"<b>🤖 Ввёденный вами Username бота:</b> <code>{username_bot}</code>\n\n"
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
        f"<b>🤖 Username бота:</b> <code>{username_bot}</code>\n"
        f"<b>⚠️ Причина жалобы:</b> <code>{reason}</code>\n\n"
        "<b>➡️ Хотите продолжить?</b>",
        parse_mode="HTML",
        reply_markup=kb.confirm_mailing_yes_no)

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
DELAY = 5 # Задержка в секундах

@router.callback_query(F.data.startswith("confirm_mailing_"))
async def confirm_callback(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

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
        "🕵️‍♂️ Осинт бот": "osint_bot",
        "📅 7 дней (70₽)": "7",
        "📅 14 дней (140₽)": "14",
        "📅 30 дней (210₽)": "30",
        "📅 60 дней (420₽)": "60"
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
        account_info = accounts.get(account_email)
        if not account_info:
            raise ValueError(f"Конфигурация аккаунта для {account_email} не найдена")

        password = account_info["password"]
        smtp_server = account_info["smtp_server"]
        smtp_port = account_info["smtp_port"]

        message = MIMEMultipart()
        message["From"] = account_email
        message["To"] = recipient
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        async with SMTP(hostname=smtp_server, port=smtp_port, use_tls=True) as smtp:
            await smtp.login(account_email, password)
            await smtp.send_message(message)

    async def distribute_emails(callback: CallbackQuery, reason, data):
        global stop_mailing
        stop_mailing = False

        for account_email in accounts.keys():
            if stop_mailing:
                break

            for recipient in mailing_list:
                if stop_mailing:
                    break

                text = REPORT_TEXTS[reason].format(**data)
                subject = "Жалоба от пользователя"

                try:
                    await send_email(account_email, recipient, subject, text)

                    await callback.message.answer(
                        f"Письмо отправлено с {account_email} на {recipient}",
                        parse_mode="HTML",
                        reply_markup=kb.stop)

                except Exception as e:
                    from html import escape
                    await callback.message.answer(
                        f"❌ Не удалось отправить письмо с {account_email} на {recipient}: {escape(str(e))}",
                        parse_mode="HTML",
                        reply_markup=kb.stop)

                await asyncio.sleep(DELAY)  # Задержка между отправками

    if callback.data == "confirm_mailing_yes":
        await callback.message.answer(
            "<b>✅ Отправка жалоб успешно начата!</b>",
            parse_mode="HTML",
            reply_markup=kb.stop)

        reason = reason_map.get(reason, reason)

        await distribute_emails(callback, reason, data)

        await state.clear()

    elif callback.data == "confirm_mailing_no":
        await callback.message.answer(
            "<b>❌ Вы отменили процесс. Используйте кнопку ниже, чтобы начать заново.</b>",
            parse_mode="HTML",
            reply_markup=kb.start)
        
        await state.clear()

@router.callback_query(F.data == "cancel")
async def cancel(callback: CallbackQuery, state: FSMContext):

    await state.clear()

    await callback.message.answer(
        "<b>❌ Действие успешно отменено.</b>",
        parse_mode="HTML",
        reply_markup=kb.menu)
    
@router.callback_query(F.data == "stop")
async def stop(callback: CallbackQuery):

    await callback.answer()

    global stop_mailing
    stop_mailing = True
    await callback.message.answer(
        "<b>⛔ Рассылка успешно остановлена.</b>",
        parse_mode="HTML",
        reply_markup=kb.repeat)
    
@router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery):

    await callback.answer()

    user_id = callback.from_user.id

    user_info = await get_user_info(callback.from_user.id)

    if user_info:
        user_id, registration_date, balance, subscription_date = user_info

    subscription_datetime = await get_subscription_datetime(user_id)
    
    current_timestamp = int(time.time())
    
    if subscription_datetime > current_timestamp:
        subscription_date = datetime.fromtimestamp(subscription_datetime).strftime('%d.%m.%Y %H:%M:%S')
        subscription_text = f"<b>💎 Активна до</b> {subscription_date}"
    elif user_id in ADMINS:
        subscription_text = "<b>💎 Активна</b>"
    else:
        subscription_text = "<b>❌ Отсутствует</b>"

    await callback.message.answer(
        "<b>👤 Ваш профиль:</b>\n\n"
        f"<b>🆔 Ваш Telegram ID:</b> <code>{user_id}</code>\n"
        f"<b>📅 Дата регистрации:</b> {registration_date}\n"
        f"<b>💰 Баланс:</b> {balance} ₽\n"
        f"<b>🌟 Статус подписки:</b> {subscription_text}\n",
        parse_mode="HTML",
        reply_markup=kb.profile)

class SubscriptionBuy(StatesGroup):
    subscription_duration = State()
    pay = State()
    confirm = State()

@router.callback_query(F.data == "subscription_buy")
async def subscription_buy(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    user_id = callback.from_user.id

    subscription_datetime = await get_subscription_datetime(user_id)
    
    current_timestamp = int(time.time())

    if subscription_datetime > current_timestamp or user_id in ADMINS:
        await callback.message.answer(
            "<b>❌ У вас уже есть активная подписка. Попробуйте позже.</b>",
            parse_mode="HTML",
            reply_markup=kb.menu)
    else:
        await callback.message.answer(
            "<b>💎 Оформите подписку и начните пользоваться всеми возможностями бота уже сегодня!</b>\n\n"
            "<b>⏳ Выберите подходящий срок подписки:</b>",
            parse_mode="HTML",
            reply_markup=kb.subscription_duration)

        await state.set_state(SubscriptionBuy.subscription_duration)
        
@router.callback_query(SubscriptionBuy.subscription_duration)
async def subscription_duration(callback: CallbackQuery, state: FSMContext):

    callback_data = callback.data

    try:
        duration = callback_data.split("|")[0]
    except IndexError:
        await callback.answer("❌ Произошла ошибка. Пожалуйста, выберите срок подписки еще раз.")
        return

    if duration == "7":
        price = "70"
    elif duration == "14":
        price = "140"
    elif duration == "30":
        price = "210"
    elif duration == "60":
        price = "420"
    else:
        price = "❌ Неизвестная сумма"

    await state.update_data(duration=duration, price=price)

    await callback.message.answer(
        "<b>🔍 Пожалуйста, проверьте введенные данные:</b>\n\n"
        f"<b>⏳ Срок для подписки: {duration} дней</b>\n"
        f"<b>💰 Сумма для оплаты:</b> {price} ₽\n\n"
        "<b>👇 Нажмите на кнопку ниже, чтобы оплатить. После этого подтвердите операцию.</b>",
        parse_mode="HTML",
        reply_markup=kb.pay)
    
    await state.set_state(SubscriptionBuy.pay)

@router.callback_query(SubscriptionBuy.pay)
async def pay(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()

    price = data.get('price')

    user_id = callback.from_user.id
    user_info = await get_user_info(user_id)
    _, _, balance, _ = user_info

    new_balance = int(balance) - int(price)

    await state.update_data(user_id=user_id, new_balance=new_balance, balance=balance, price=price)

    await callback.message.answer(
        "<b>📝 Детали оплаты:</b>\n\n"
        f"<b>💰 Ваш текущий баланс:</b> {balance} ₽\n"
        f"<b>📉 Баланс после оплаты:</b> {new_balance} ₽\n"
        f"<b>💵 Сумма к оплате:</b> {price} ₽\n\n"
        "<b>✅ Подтвердить оплату?</b>",
        parse_mode="HTML",
        reply_markup=kb.confirm_pay_yes_no)

    await state.set_state(SubscriptionBuy.confirm)

@router.callback_query(SubscriptionBuy.confirm)
async def confirm(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('user_id')
    duration = data.get('duration')
    new_balance = data.get('new_balance')
    balance = data.get('balance')
    price = data.get('price')

    # Проверка, что баланс больше или равен цене и подтверждение оплаты
    if callback.data == "confirm_pay_yes":
        if int(balance) >= int(price):
            duration_in_seconds = int(duration) * 86400
            current_timestamp = int(time.time())
            duration_result = duration_in_seconds + int(current_timestamp)

            # Списание средств и активация подписки
            await subtract_balance(new_balance, user_id)
            await add_subscription(duration_result, user_id)

            # Ответ о успешной оплате
            await callback.message.answer(
                f"<b>✅ Оплата успешно завершена!</b>\n\n"
                f"<b>🆔 Ваш ID:</b> {user_id}\n"
                f"<b>⏳ Срок подписки: {duration} дней</b>\n"
                f"<b>💰 Новый баланс:</b> {new_balance} ₽\n\n"
                "<b>🎉 Спасибо за оплату! Ваша подписка активирована. Если у вас возникнут вопросы, наша поддержка всегда на связи. 😊</b>",
                parse_mode="HTML",
                reply_markup=kb.menu)
        else:
            await callback.message.answer(
                "<b>❌ Ошибка!</b>\n\n"
                "<b>У вас недостаточно средств на балансе для завершения оплаты.</b> 💸\n"
                "<b>Попробуйте пополнить баланс и повторите попытку.</b> 💳",
                parse_mode="HTML",
                reply_markup=kb.menu)

    elif callback.data == "confirm_pay_no":
        await callback.message.answer(
            "<b>❌ Вы отменили процесс. Используйте кнопку ниже, чтобы начать заново.</b>",
            parse_mode="HTML",
            reply_markup=kb.main_admin)

        await state.clear()

@router.callback_query(F.data == "admin_panel")
async def admin_panel(callback: CallbackQuery):

    await callback.answer()

    await callback.message.answer(
        "<b>💼 Добро пожаловать в Админ Панель!</b>",
        parse_mode="HTML",
        reply_markup=kb.admin_panel)

class UserManagement(StatesGroup):
    user_id = State()
    action = State()
    duration = State()
    confirm = State()
    amount_new_balance = State()

@router.callback_query(F.data == "user_management")
async def user_management(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    await callback.message.answer(
        "<b>🔍 Введите ID пользователя:</b>",
        parse_mode="HTML",
        reply_markup=kb.cancel)

    await state.set_state(UserManagement.user_id)

@router.message(UserManagement.user_id)
async def get_user_id(message: Message, state: FSMContext):

    user_id = message.text

    await state.update_data(user_id=user_id)

    if not await user_exists(user_id):
            await message.answer(
                "<b>🚫 Пользователь не найден! Возможно, ID указан с ошибкой.</b>",
                parse_mode="HTML",
                reply_markup=kb.menu)
    else:
        await message.answer(
            f"<b>👤 Введеный ID пользователя:</b> <code>{user_id}</code>\n\n"
            "<b>🛠️ Выберите действие:</b>",
            parse_mode="HTML",
            reply_markup=kb.user_management)

        await state.set_state(UserManagement.action)

@router.callback_query(UserManagement.action)
async def action(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    user_id = data.get('user_id')
    action = callback.data.split("|")[1]

    await state.update_data(action=action)

    if action == "🎁 Подарить подписку":
        await callback.message.answer(
            "📅 <b>Введите количество дней для подписки:</b>\n"
            "🔢 <b>Например: 7, 30 или 365.</b>",
         parse_mode="HTML")
        
        await state.set_state(UserManagement.duration)

    if action == "💸 Изменить баланс":

        user_info = await get_user_info(user_id)
        _, _, balance, _ = user_info

        await state.update_data(balance=balance)

        await callback.message.answer(
            f"<b>💰 Текущий баланс пользователя с ID: {user_id} - {balance} ₽</b>\n\n"
            "<b>💸 Введите новый баланс:</b>",
            parse_mode="HTML",
            reply_markup=kb.cancel)
        
        await state.set_state(UserManagement.amount_new_balance)

@router.message(UserManagement.amount_new_balance)
async def get_amount_new_balance(message: Message, state: FSMContext):
    try:
        amount_new_balance = int(message.text)

        if amount_new_balance >= 0:
            await state.update_data(amount_new_balance=amount_new_balance)

            data = await state.get_data()
            user_id = data.get('user_id')
            action = data.get('action')

            await message.answer(
                "<b>🔍 Пожалуйста, проверьте введенные данные:</b>\n\n"
                f"<b>🆔 ID пользователя:</b> <code>{user_id}</code>\n"
                f"<b>🛠️ Действие:</b> {action}\n"
                f"<b>💸 Обновленный баланс пользователя:</b> {amount_new_balance} ₽\n\n"
                "<b>➡️ Хотите продолжить?</b>",
                parse_mode="HTML",
                reply_markup=kb.confirm_change_balance_yes_no)
            
            await state.set_state(UserManagement.confirm)
        else:
            await message.reply("<b>⚠️ Пожалуйста, введите целое число не меньше нуля.</b>", parse_mode="HTML")
    except ValueError:
        await message.reply("<b>❌ Введите корректное целое число.</b>", parse_mode="HTML")
        
@router.message(UserManagement.duration)
async def duration(message: Message, state: FSMContext):
    try:
        duration = int(message.text)

        if duration > 0:
            await state.update_data(duration=duration)

            data = await state.get_data()
            user_id = data.get('user_id')
            action = data.get('action')

            def days_declension(n):
                if 11 <= n % 100 <= 19:
                    return f"{n} дней"
                last_digit = n % 10
                if last_digit == 1:
                    return f"{n} день"
                elif 2 <= last_digit <= 4:
                    return f"{n} дня"
                else:
                    return f"{n} дней"

            duration_text = days_declension(duration)

            await message.answer(
                "<b>🔍 Пожалуйста, проверьте введенные данные:</b>\n\n"
                f"<b>🆔 ID пользователя:</b> <code>{user_id}</code>\n"
                f"<b>🛠️ Действие:</b> {action}\n"
                f"<b>⌛ Длительность подписки:</b> {duration_text}\n\n"
                "<b>➡️ Хотите продолжить?</b>",
                parse_mode="HTML",
                reply_markup=kb.confirm_gift_a_sub_yes_no)

            await state.set_state(UserManagement.confirm)
        else:
            await message.reply("<b>⚠️ Пожалуйста, введите положительное целое число.</b>", parse_mode="HTML")
    except ValueError:
        await message.reply("<b>❌ Введите корректное целое число.</b>", parse_mode="HTML")

@router.callback_query(UserManagement.confirm)
async def confirm(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('user_id')
    duration = data.get('duration')
    balance = data.get('balance')
    amount_new_balance = data.get('amount_new_balance')

    if callback.data == "confirm_gift_a_sub_yes":

        duration_in_seconds = duration * 86400
        current_timestamp = int(time.time())
        new_subscription_end = duration_in_seconds + current_timestamp

        current_subscription = await get_subscription_datetime(user_id)

        current_sub_date = datetime.fromtimestamp(current_subscription).strftime('%d.%m.%Y %H:%M:%S')

        if new_subscription_end <= current_subscription:
            await callback.message.answer(
                f"<b>⚠ Ошибка:</b> У пользователя уже есть подписка на больший или равный срок!\n\n"
                f"<b>📅 Текущая подписка активна до:</b> <code>{current_sub_date}</code>\n"
                f"<i>⏳ Попробуйте подарить подписку с большим сроком.</i>",
                parse_mode="HTML",
                reply_markup=kb.menu
            )
            return

        await add_subscription(new_subscription_end, user_id)

        await callback.message.answer(
            "<b>🎁 Подписка успешно подарена!✨</b>\n\n"
            f"⌛ Срок действия: {duration} дней.",
            parse_mode="HTML",
            reply_markup=kb.menu)

    elif callback.data == "confirm_gift_a_sub_no":
        await callback.message.answer(
            "<b>❌ Вы отменили процесс. Используйте кнопку ниже, чтобы начать заново.</b>",
            parse_mode="HTML",
            reply_markup=kb.main_admin)

        await state.clear()

    if callback.data == "confirm_change_balance_yes":

        await change_balance(amount_new_balance, user_id)

        await callback.message.answer(
            "<b>🔄 Баланс пользователя успешно обновлён!</b>\n\n"
            f"<b>📊 Старый баланс:</b> {balance} ₽\n"
            f"<b>🆕 Новый баланс:</b> {amount_new_balance} ₽\n\n"
            "<b>✅ Все изменения успешно внесены.</b>",
            parse_mode="HTML",
            reply_markup=kb.menu)

    elif callback.data == "confirm_change_balance_no":
        await callback.message.answer(
            "<b>❌ Вы отменили процесс. Используйте кнопку ниже, чтобы начать заново.</b>",
            parse_mode="HTML",
            reply_markup=kb.main_admin)

        await state.clear()
        
class AddBalance(StatesGroup):
    payment_system = State()
    amount = State()
    confirm = State()

@router.callback_query(F.data == "add_balance")
async def add_balance(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    await callback.message.answer(
        "💸 Выберите платежную систему:",
        parse_mode="HTML",
        reply_markup=kb.payment_systems)

    await state.set_state(AddBalance.payment_system)

@router.callback_query(AddBalance.payment_system)
async def get_payment_system(callback: CallbackQuery, state: FSMContext):
    
    payment_system = callback.data.split("|")[1]

    await state.update_data(payment_system=payment_system)

    await callback.message.answer(
        f"💸 Платежная система которую вы выбрали: {payment_system}\n\n"
        "💰 Теперь введите сумму для пополнения:",
        parse_mode="HTML",
        reply_markup=kb.cancel)
    
    await state.set_state(AddBalance.amount)

@router.message(AddBalance.amount)
async def enter_amount(message: Message, state: FSMContext):
    try:
        amount = int(message.text)

        data = await state.get_data()

        payment_system = data.get('payment_system')

        if int(amount) > 0:
            await state.update_data(amount=amount)

            await message.answer(
                "<b>🔍 Пожалуйста, проверьте введенные данные:</b>\n\n"
                f"💸 Платежная система: {payment_system}\n"
                f"💰 Сумма для пополнения: {amount} ₽\n\n"
                "➡️ Все указано верно?",
                parse_mode="HTML",
                reply_markup=kb.confirm_add_balance_yes_no)
            
            await state.set_state(AddBalance.confirm)
        else:
            await message.reply("⚠️ Пожалуйста, введите только чётное положительное число.")
    except ValueError:
        await message.reply("❌ Пожалуйста, введите корректную сумму в рублях (целое положительное число).")

@router.callback_query(F.data.startswith("CHECK|"))
async def check_invoice(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    data = await state.get_data()

    logger.info(f"Текущее состояние данных: {data}")

    amount = data.get('amount')
    payment_id = data.get('payment_id')
    invoice_id = int(callback.data.split("|")[1])
    user_id = callback.from_user.id

    logger.info(f"Запрос на проверку оплаты. ID счета: {invoice_id}, Сумма: {amount} ₽")

    try:
        invoice = await acp.get_invoices(invoice_ids=invoice_id)
        logger.info(f"Статус счета: {invoice.status}, ID счета: {invoice.invoice_id}")

    except Exception as e:
        logger.error(f"Ошибка при получении статуса счета: {str(e)}")
        await callback.answer(f"❌ Ошибка при получении статуса счета: {str(e)}")
        return

    if invoice.status == "paid":

        if await check_balance_updated(invoice_id):
            logger.info("Баланс уже обновлен, повторное обновление не требуется.")
            await callback.message.answer("✅ Баланс уже был обновлен ранее.")
            return
        
        logger.info(f"Счет {invoice_id} оплачен. Баланс пользователя будет обновлен.")

        await callback.answer("✅ Проверка завершена: статус оплаты подтвержден.")

        user_info = await get_user_info(user_id)
        _, _, balance, _ = user_info
        new_balance = int(balance) + int(amount)

        logger.info(f"Обновление баланса: новый баланс пользователя {user_id} - {new_balance} ₽")

        invoice_status = invoice.status

        await update_invoice_status(invoice_status, invoice_id)

        await balance_updated(invoice_id)

        await top_up_balance(new_balance, user_id)

        updated_data = await state.get_data()
        logger.info(f"Состояние после обновления: {updated_data}")

        await callback.message.answer(
            f"<b>🎉 Пополнение баланса успешно!</b>\n\n"
            f"<b>💸 Сумма пополнения:</b> {amount} ₽\n"
            f"<b>🆔 ID платежа:</b> <code>{payment_id}</code>\n\n"
            f"<b>🔄 Ваш баланс обновлен. 😄</b>",
            parse_mode="HTML",
            reply_markup=kb.menu)

    elif invoice.status == 'expired':
        logger.warning(f"Счет {invoice_id} истек.")
        await callback.answer("❌ Счет истек. Пожалуйста, создайте новый.")
    else:
        logger.info(f"Счет {invoice_id} еще не оплачен. Статус: {invoice.status}")
        await callback.answer("❌ Счет пока не оплачен. Пожалуйста, повторите проверку позже.")

@router.callback_query(AddBalance.confirm)
async def confirm(callback: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()

        payment_system = data.get('payment_system')
        amount = data.get('amount')

        if callback.data == "confirm_add_balance_yes":

            logger.info(f"Запрос на создание счета: Платежная система: {payment_system}, Сумма: {amount} ₽")

            invoice = await acp.create_invoice(
                currency_type='fiat',
                asset='USDT',
                fiat='RUB',
                amount=amount,
                description=f'Пополнение баланса на {amount} ₽'
            )

            logger.info(f"Счет успешно создан. ID счета: {invoice.invoice_id}, URL счета: {invoice.bot_invoice_url}")

            user_id = callback.from_user.id

            invoice_id = invoice.invoice_id
            invoice_status = invoice.status

            payment_id = str(uuid.uuid4())
            payment_amount = int(amount)
            payment_date = datetime.now().strftime('%d.%m.%Y %H:%M:%S')

            await log_payment(user_id, invoice_id, invoice_status, payment_id, payment_amount, payment_date)

            await state.update_data(invoice_id=invoice.invoice_id, payment_id=payment_id, amount=amount)

            pay_button = InlineKeyboardButton(text="💵 Оплатить", url=invoice.bot_invoice_url)
            payment_confirm_button = InlineKeyboardButton(text="✅ Проверить оплату", callback_data=f"CHECK|{invoice.invoice_id}")
            pay_markup = InlineKeyboardMarkup(inline_keyboard=[[pay_button], [payment_confirm_button]])

            await callback.message.answer(
                f"🏦 Информация о пополнении:\n\n"
                f"🔹 Платежная система: {payment_system}\n"
                f"🔹 Сумма к оплате: {amount} ₽\n"
                f"🔹 ID платежа: <code>{payment_id}</code>\n\n"
                "🔻 Для завершения операции нажмите кнопку ниже, чтобы произвести оплату:",
                parse_mode="HTML",
                reply_markup=pay_markup)

        elif callback.data == "confirm_add_balance_no":
            await callback.message.answer(
                "<b>❌ Вы отменили процесс. Используйте кнопку ниже, чтобы открыть главное меню.</b>",
                parse_mode="HTML",
                reply_markup=kb.menu)
            
            await state.clear()

    except Exception as e:
        logger.error(f"Ошибка при создании счета: {str(e)}")
        await callback.message.answer("❌ Произошла ошибка при создании счета. Попробуйте еще раз.")


