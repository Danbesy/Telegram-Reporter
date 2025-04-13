
#   ____                        _____                    _                          
#  |  _ \               ____   |  __ \                  | |                         
#  | |_) |  _   _      / __ \  | |  | |   __ _   _ __   | |__     ___   ___   _   _ 
#  |  _ <  | | | |    / / _` | | |  | |  / _` | | '_ \  | '_ \   / _ \ / __| | | | |
#  | |_) | | |_| |   | | (_| | | |__| | | (_| | | | | | | |_) | |  __/ \__ \ | |_| |
#  |____/   \__, |    \ \__,_| |_____/   \__,_| |_| |_| |_.__/   \___| |___/  \__, |
#            __/ |     \____/                                                  __/ |
#           |___/                                                             |___/ 
#
# Telegram - https://t.me/danbesy
# Telegram Channel - https://t.me/Danbesy_Dev
# Telegram Bio - https://Danbesy_Bio
# GitHub - https://github.com/Danbesy

import logging
import asyncio
import time
import uuid
import keyboards as kb
from config import *
from db import *
from datetime import datetime
from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiosmtplib import SMTP
from aiocryptopay import AioCryptoPay, Networks
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Настройки бота // Bot settings
bot = Bot(TOKEN)

router = Router()

# Иницилизация CryptoPay // Initialization of CryptoPay
acp = AioCryptoPay(token=CRYPTOPAY_TOKEN, network=Networks.MAIN_NET)

# Логирование // # Logging
logging.basicConfig(level=logging.INFO)

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):

    await state.clear()

    await init_users_db()
    await init_logs_payments_db()

    user_id = message.from_user.id
    user_link = f'tg://user?id={user_id}'

    user_language = await get_user_language(user_id)

    if user_language == "ru":
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

    elif user_language == "en":
        if user_id in ADMINS:
            await message.answer(
                f"<b>👋 Hello, </b><a href='{user_link}'>{message.from_user.full_name}</a> !\n\n"
                "<b>Welcome to the bot for automatic complaint submissions in Telegram! 🚀</b>\n\n"
                "<b>Use the buttons below to get started. 💼</b>",
                parse_mode="HTML",
                reply_markup=kb.main_admin_en)
        else:
            await message.answer(
                f"<b>👋 Hello, </b><a href='{user_link}'>{message.from_user.full_name}</a> !\n\n"
                "<b>Welcome to the bot for automatic complaint submissions in Telegram! 🚀</b>\n\n"
                "<b>Use the buttons below to get started. 💼</b>",
                parse_mode="HTML",
                reply_markup=kb.main_en)

    if not await user_exists(user_id):
        registration_date = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        await add_user(user_id, registration_date)

@router.callback_query(F.data == "menu")
async def menu(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    await state.clear()

    user_id = callback.from_user.id
    user_link = f'tg://user?id={user_id}'

    user_language = await get_user_language(user_id)

    if user_language == "ru":
        if user_id in ADMINS:
            await callback.message.answer(
                f"<b>👋 Приветствую, </b><a href='{user_link}'>{callback.from_user.full_name}</a> !\n\n"
                "<b>Добро пожаловать в бота для автоматической отправки жалоб в Telegram! 🚀</b>\n\n"
                "<b>Используйте кнопки ниже, чтобы начать. 💼</b>",
                parse_mode="HTML",
                reply_markup=kb.main_admin)  
        else:
            await callback.message.answer(
                f"<b>👋 Приветствую, </b><a href='{user_link}'>{callback.from_user.full_name}</a> !\n\n"
                "<b>Добро пожаловать в бота для автоматической отправки жалоб в Telegram! 🚀</b>\n\n"
                "<b>Используйте кнопки ниже, чтобы начать. 💼</b>",
                parse_mode="HTML",
                reply_markup=kb.main)

    elif user_language == "en":
        if user_id in ADMINS:
            await callback.message.answer(
                f"<b>👋 Hello, </b><a href='{user_link}'>{callback.from_user.full_name}</a>!\n\n"
                "<b>Welcome to the bot for automatic complaint submissions in Telegram! 🚀</b>\n\n"
                "<b>Use the buttons below to get started. 💼</b>",
                parse_mode="HTML",
                reply_markup=kb.main_admin_en)  
        else:
            await callback.message.answer(
                f"<b>👋 Hello, </b><a href='{user_link}'>{callback.from_user.full_name}</a>!\n\n"
                "<b>Welcome to the bot for automatic complaint submissions in Telegram! 🚀</b>\n\n"
                "<b>Use the buttons below to get started. 💼</b>",
                parse_mode="HTML",
                reply_markup=kb.main_en)

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

        user_language = await get_user_language(user_id)

        if user_language == "ru":

            await callback.answer()

            await callback.message.answer(
                "<b>📂 Выберите нужную категорию, для отправки жалоб:</b>",
                parse_mode="HTML",
                reply_markup=kb.category)
            await state.set_state(Mailing.category)

        elif user_language == "en":

            await callback.answer()

            await callback.message.answer(
                "<b>📂 Choose the necessary category to file complaints:</b>",
                parse_mode="HTML",
                reply_markup=kb.category_en)
            await state.set_state(Mailing.category)
    else:
        await callback.answer()

        await callback.message.answer(
            "<b>⛔ Доступ запрещен!</b>\n\n"
            "<b>У вас отсутствует активная подписка. Пожалуйста, оформите подписку, чтобы получить доступ.</b>",
            parse_mode="HTML",
            reply_markup=kb.subscription_buy)

@router.message(Command("language"))
async def change_language(message: Message):
    user_id = message.from_user.id

    user_language = await get_user_language(user_id)

    if user_language == "ru":
        await message.answer(
            "<b>🌐 Выберите язык для использования бота:</b>",
            parse_mode="HTML",
            reply_markup=kb.change_language_ru)
    elif user_language == "en":
        await message.answer(
            "<b>🌐 Select a language to use the bot:</b>",
            parse_mode="HTML",
            reply_markup=kb.change_language_en)

@router.callback_query(F.data == "select_language_ru")
async def set_language_ru(callback: CallbackQuery):

    await callback.answer("Вы успешно выбрали русский язык для использования бота! 🇷🇺")

    user_id = callback.from_user.id

    await select_language_ru(user_id)

@router.callback_query(F.data == "select_language_en")
async def set_language_en(callback: CallbackQuery):

    await callback.answer("You have successfully selected English to use the bot! 🇺🇸")

    user_id = callback.from_user.id

    await select_language_en(user_id)

@router.callback_query(F.data == "report_user")
async def report_user(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    user_id = callback.from_user.id

    user_language = await get_user_language(user_id)

    if user_language == "ru":
        await callback.message.answer(
            "<b>📝 Для начала введите Username пользователя:</b>",
            parse_mode="HTML",  
            reply_markup=kb.cancel)

        await state.set_state(ReportUser.username)

    elif user_language == "en":
        await callback.message.answer(
            "<b>📝 To get started, enter the user's Username:</b>",
            parse_mode="HTML",  
            reply_markup=kb.cancel_en)

        await state.set_state(ReportUser.username)

@router.message(ReportUser.username)
async def get_username(message: Message, state: FSMContext):

    username = message.text
    await state.update_data(username=username)

    user_id = message.from_user.id
    user_language = await get_user_language(user_id)

    if user_language == "ru":
        await message.answer(
            f"<b>👤 Введенный Вами Username:</b> <code>{username}</code>\n\n"
            "<b>📝 Теперь введите Telegram ID:</b>",
            parse_mode="HTML",
            reply_markup=kb.cancel)

        await state.set_state(ReportUser.telegram_id)

    elif user_language == "en":
        await message.answer(
            f"<b>👤 The Username you entered:</b> <code>{username}</code>\n\n"
            "<b>📝 Now enter the Telegram ID:</b>",
            parse_mode="HTML",
            reply_markup=kb.cancel_en)

        await state.set_state(ReportUser.telegram_id)

@router.message(ReportUser.telegram_id)
async def get_telegram_id(message: Message, state: FSMContext):

    telegram_id = message.text
    await state.update_data(telegram_id=telegram_id)

    data = await state.get_data()
    username = data.get('username')

    user_id = message.from_user.id
    user_language = await get_user_language(user_id)

    if user_language == "ru":
        await message.answer(
            f"<b>👤 Username:</b> <code>{username}</code>\n"
            f"<b>🆔 Telegram ID:</b> <code>{telegram_id}</code>\n\n"
            "<b>🔗 Введите ссылку (@username) или ID на чат с нарушением:</b>",
            parse_mode="HTML",
            reply_markup=kb.cancel)

        await state.set_state(ReportUser.chat_link)

    elif user_language == "en":
        await message.answer(
            f"<b>👤 Username:</b> <code>{username}</code>\n"
            f"<b>🆔 Telegram ID:</b> <code>{telegram_id}</code>\n\n"
            "<b>🔗 Enter the link (@username) or ID of the chat with the violation:</b>",
            parse_mode="HTML",
            reply_markup=kb.cancel_en)

        await state.set_state(ReportUser.chat_link)

@router.message(ReportUser.chat_link)
async def get_chat_link(message: Message, state: FSMContext):

    chat_link = message.text
    await state.update_data(chat_link=chat_link)

    data = await state.get_data()
    username = data.get('username')
    telegram_id = data.get('telegram_id')

    user_id = message.from_user.id
    user_language = await get_user_language(user_id)

    if user_language == "ru":
        await message.answer(
            f"<b>👤 Username:</b> <code>{username}</code>\n"
            f"<b>🆔 Telegram ID:</b> <code>{telegram_id}</code>\n"
            f"<b>🔗 Ссылка на чат:</b> <code>{chat_link}</code>\n\n"
            "<b>⚠️ Теперь укажите ссылку на нарушение:</b>",
            parse_mode="HTML",
            reply_markup=kb.cancel)

        await state.set_state(ReportUser.link_for_user)

    elif user_language == "en":
        await message.answer(
            f"<b>👤 Username:</b> <code>{username}</code>\n"
            f"<b>🆔 Telegram ID:</b> <code>{telegram_id}</code>\n"
            f"<b>🔗 Chat link:</b> <code>{chat_link}</code>\n\n"
            "<b>⚠️ Now provide the link to the violation:</b>",
            parse_mode="HTML",
            reply_markup=kb.cancel_en)

        await state.set_state(ReportUser.link_for_user)

@router.message(ReportUser.link_for_user)
async def get_link(message: Message, state: FSMContext):
    
    link_for_user = message.text
    await state.update_data(link_for_user=link_for_user)

    data = await state.get_data()

    username = data.get('username')
    telegram_id = data.get('telegram_id')
    chat_link = data.get('chat_link')

    user_id = message.from_user.id
    user_language = await get_user_language(user_id)

    if user_language == "ru":
        await message.answer(
            f"<b>👤 Username:</b> <code>{username}</code>\n"
            f"<b>🆔 Telegram ID:</b> <code>{telegram_id}</code>\n"
            f"<b>🔗 Ссылка на чат:</b> <code>{chat_link}</code>\n"
            f"<b>⚠️ Ссылка на нарушение:</b> <code>{link_for_user}</code>\n\n"
            "<b>📋 Выберите причину жалобы:</b>",
            parse_mode="HTML",
            reply_markup=kb.reasons_for_user)

        await state.set_state(ReportUser.reasons)

    elif user_language == "en":
        await message.answer(
            f"<b>👤 Username:</b> <code>{username}</code>\n"
            f"<b>🆔 Telegram ID:</b> <code>{telegram_id}</code>\n"
            f"<b>🔗 Chat link:</b> <code>{chat_link}</code>\n"
            f"<b>⚠️ Violation link:</b> <code>{link_for_user}</code>\n\n"
            "<b>📋 Choose the reason for the report:</b>",
            parse_mode="HTML",
            reply_markup=kb.reasons_for_user_en)

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

    user_id = callback.from_user.id
    user_language = await get_user_language(user_id)

    if user_language == "ru":
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

    elif user_language == "en":
        await callback.message.answer(
            "<b>🔍 Please check the entered information:</b>\n\n"
            f"<b>👤 Username:</b> <code>{username}</code>\n"
            f"<b>🆔 Telegram ID:</b> <code>{telegram_id}</code>\n"
            f"<b>🔗 Chat link:</b> <code>{chat_link}</code>\n"
            f"<b>⚠️ Violation link:</b> <code>{link_for_user}</code>\n"
            f"<b>📋 Reason for the report:</b> <code>{reason}</code>\n\n"
            "<b>➡️ Do you want to continue?</b>",
            parse_mode="HTML",
            reply_markup=kb.confirm_mailing_yes_no_en)
        
        await state.set_state(Mailing.confirm)

class ReportChannel(StatesGroup):
    channel = State()
    link_for_channel = State()
    reasons = State()

@router.callback_query(F.data == "report_channel")
async def report_channel(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    user_id = callback.from_user.id
    user_language = await get_user_language(user_id)

    if user_language == "ru":
        await callback.message.answer(
            "<b>📝 Для начала введите ссылку на канал (@username) или его ID:</b>",
            parse_mode="HTML",
            reply_markup=kb.cancel)
        
        await state.set_state(ReportChannel.channel)

    elif user_language == "en":
        await callback.message.answer(
            "<b>📝 To get started, enter the channel's link (@username) or its ID:</b>",
            parse_mode="HTML",
            reply_markup=kb.cancel_en)
        
        await state.set_state(ReportChannel.channel)

@router.message(ReportChannel.channel)
async def get_channel(message: Message, state: FSMContext):

    channel = message.text  
    await state.update_data(channel=channel)

    user_id = message.from_user.id
    user_language = await get_user_language(user_id)

    if user_language == "ru":
        await message.answer(
            f"<b>🔗 Введенная Вами ссылка на канал:</b> <code>{channel}</code>\n\n"
            "<b>⚠️ Теперь укажите ссылку на нарушение:</b>",
            parse_mode="HTML",
            reply_markup=kb.cancel)

        await state.set_state(ReportChannel.link_for_channel)

    elif user_language == "en":
        await message.answer(
            f"<b>🔗 The channel link you entered:</b> <code>{channel}</code>\n\n"
            "<b>⚠️ Now please provide the violation link:</b>",
            parse_mode="HTML",
            reply_markup=kb.cancel_en)

        await state.set_state(ReportChannel.link_for_channel)

@router.message(ReportChannel.link_for_channel)
async def get_link(message: Message, state: FSMContext):

    link_for_channel = message.text
    await state.update_data(link_for_channel=link_for_channel)

    data = await state.get_data()

    channel = data.get('channel')

    user_id = message.from_user.id
    user_language = await get_user_language(user_id)

    if user_language == "ru":
        await message.answer(
            f"<b>📢 Ссылка на канал:</b> <code>{channel}</code>\n"
            f"<b>🔗 Ссылка на нарушение:</b> <code>{link_for_channel}</code>\n\n"
            "<b>⚠️ Выберите причину жалобы:</b>",
            parse_mode="HTML",
            reply_markup=kb.reasons_for_channel)

        await state.set_state(ReportChannel.reasons)

    elif user_language == "en":
        await message.answer(
            f"<b>📢 Channel link:</b> <code>{channel}</code>\n"
            f"<b>🔗 Violation link:</b> <code>{link_for_channel}</code>\n\n"
            "<b>⚠️ Choose the reason for the report:</b>",
            parse_mode="HTML",
            reply_markup=kb.reasons_for_channel_en)

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

    user_id = callback.from_user.id
    user_language = await get_user_language(user_id)

    if user_language == "ru":
        await callback.message.answer(
            "<b>🔍 Пожалуйста, проверьте введенные данные:</b>\n\n"
            f"<b>📢 Ссылка на канал:</b> <code>{channel}</code>\n"
            f"<b>🔗 Ссылка на нарушение:</b> <code>{link_for_channel}</code>\n"
            f"<b>⚠️ Причина жалобы:</b> <code>{reason}</code>\n\n"
            "<b>➡️ Желаете продолжить?</b>",
            parse_mode="HTML",
            reply_markup=kb.confirm_mailing_yes_no)

        await state.set_state(Mailing.confirm)

    elif user_language == "en":
        await callback.message.answer(
            "<b>🔍 Please review the information entered:</b>\n\n"
            f"<b>📢 Channel link:</b> <code>{channel}</code>\n"
            f"<b>🔗 Violation link:</b> <code>{link_for_channel}</code>\n"
            f"<b>⚠️ Reason for the report:</b> <code>{reason}</code>\n\n"
            "<b>➡️ Would you like to continue?</b>",
            parse_mode="HTML",
            reply_markup=kb.confirm_mailing_yes_no_en)

        await state.set_state(Mailing.confirm)

class ReportBot(StatesGroup):
    username_bot = State()
    reasons = State()

@router.callback_query(F.data == "report_bot")
async def report_bot(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    user_id = callback.from_user.id
    user_language = await get_user_language(user_id)

    if user_language == "ru":
        await callback.message.answer(
            "<b>📝 Введите Username бота:</b>",
            parse_mode="HTML",
            reply_markup=kb.cancel)

        await state.set_state(ReportBot.username_bot)

    elif user_language == "en":
        await callback.message.answer(
            "<b>📝 Enter the bot's Username:</b>",
            parse_mode="HTML",
            reply_markup=kb.cancel_en)

        await state.set_state(ReportBot.username_bot)

@router.message(ReportBot.username_bot)
async def get_username_bot(message: Message, state: FSMContext):

    username_bot = message.text
    await state.update_data(username_bot=username_bot)

    user_id = message.from_user.id
    user_language = await get_user_language(user_id)

    if user_language == "ru":
        await message.answer(
            f"<b>🤖 Введенный вами Username бота:</b> <code>{username_bot}</code>\n\n"
            "<b>⚠️ Теперь выберите причину для жалобы:</b>",
            parse_mode="HTML",
            reply_markup=kb.reasons_for_bot)

        await state.set_state(ReportBot.reasons)

    elif user_language == "en":
        await message.answer(
            f"<b>🤖 The bot's Username you entered:</b> <code>{username_bot}</code>\n\n"
            "<b>⚠️ Now select the reason for the report:</b>",
            parse_mode="HTML",
            reply_markup=kb.reasons_for_bot_en)

        await state.set_state(ReportBot.reasons)

@router.callback_query(ReportBot.reasons)
async def get_reason(callback: CallbackQuery, state: FSMContext):

    callback_data = callback.data
    reason = callback_data.split("|")[1]
    await state.update_data(reason=reason)

    data = await state.get_data()
    username_bot = data.get('username_bot')

    user_id = callback.from_user.id
    user_language = await get_user_language(user_id)

    if user_language == "ru":
        await callback.message.answer(
            "<b>🔍 Пожалуйста, проверьте введенные данные:</b>\n\n"
            f"<b>🤖 Username бота:</b> <code>{username_bot}</code>\n"
            f"<b>⚠️ Причина жалобы:</b> <code>{reason}</code>\n\n"
            "<b>➡️ Хотите продолжить?</b>",
            parse_mode="HTML",
            reply_markup=kb.confirm_mailing_yes_no)

        await state.set_state(Mailing.confirm)

    elif user_language == "en":
        await callback.message.answer(
            "<b>🔍 Please verify the entered data:</b>\n\n"
            f"<b>🤖 Bot's Username:</b> <code>{username_bot}</code>\n"
            f"<b>⚠️ Reason for the report:</b> <code>{reason}</code>\n\n"
            "<b>➡️ Do you want to continue?</b>",
            parse_mode="HTML",
            reply_markup=kb.confirm_mailing_yes_no_en)

        await state.set_state(Mailing.confirm)

# Список почт для рассылки // Mailing list
mailing_list = [
    'sms@telegram.org',
    'dmca@telegram.org',
    'abuse@telegram.org',
    'sticker@telegram.org',
    'support@telegram.org'
]

# SMTP настройки // SMTP settings
DELAY = 5 # Задержка в секундах // Delay in seconds

@router.callback_query(F.data.startswith("confirm_mailing_"))
async def confirm_callback(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    user_id = callback.from_user.id

    user_language = await get_user_language(user_id)

    data = await state.get_data()
    username = data.get('username')
    telegram_id = data.get('telegram_id')
    chat_link = data.get('chat_link')
    link_for_user = data.get('link_for_user')
    channel = data.get('channel')
    link_for_channel = data.get('link_for_channel')
    username_bot = data.get('username_bot')
    reason = data.get('reason')

    # Словарь с текстами для репортов // Dictionary with texts for reports
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
    "pornography_channel": f"Здравствуйте, уважаемая поддержка Telegram. Я нашел канал, который распространяет порнографический контент. Ссылка на канал - {channel}, Ссылка на нарушение - {link_for_channel}. Пожалуйста, примите меры по блокировке данного канала.",
    "violence_channel": f"Здравствуйте, уважаемая поддержка Telegram. Я нашел канал, который распространяет контент, содержащий насилие или жестокое обращение. Ссылка на канал - {channel}, Ссылка на нарушение - {link_for_channel}. Пожалуйста, примите меры по блокировке данного канала.",
    "osint_bot": f"Здравствуйте, уважаемая поддержка Telegram. На вашей платформе я нашел бота, который осуществляет поиск по личным данным ваших пользователей. Ссылка на бота - {username_bot}. Пожалуйста, разберитесь и заблокируйте данного бота.",

    "spam_user_en": f"Здравствуйте, уважаемая поддержка. На вашей платформе я нашел пользователя, который отправляет много ненужных сообщений - СПАМ. Его юзернейм - {username}, его айди - {telegram_id}, ссылка на чат - {chat_link}, ссылка на нарушение/нарушения - {link_for_user}. Пожалуйста, примите меры по отношению к данному пользователю.",
    "personal_data_user_en": f"Здравствуйте, уважаемая поддержка. На вашей платформе я нашел пользователя, который распространяет чужие данные без их согласия. Его юзернейм - {username}, его айди - {telegram_id}, ссылка на чат - {chat_link}, ссылка на нарушение/нарушения - {link_for_user}. Пожалуйста, примите меры по отношению к данному пользователю путем блокировки его акккаунта.",
    "trolling_user_en": f"Здравствуйте, уважаемая поддержка Telegram. Я нашел пользователя, который открыто выражается нецензурной лексикой и спамит в чатах. Его юзернейм - {username}, его айди - {telegram_id}, ссылка на чат - {chat_link}, ссылка на нарушение/нарушения - {link_for_user}. Пожалуйста, примите меры по отношению к данному пользователю путем блокировки его акккаунта.",
    "delete_sessions_user_en": f"Здравствуйте, уважаемая поддержка. Я случайно перешел по фишинговой ссылке и утерял доступ к своему аккаунту. Его юзернейм - {username}, его айди - {telegram_id}. Пожалуйста, удалите аккаунт или обнулите сессии",
    "premium_user_en": f"Здравствуйте, уважаемая поддержка Telegram.! Аккаунт {username}, {telegram_id} приобрёл Premium подписку в вашем мессенджере, чтобы рассылать спам-сообщения и обходить ограничения Telegram. Прошу проверить данную жалобу и принять меры!",
    "virtual_number_user_en": f"Здравствуйте, уважаемая поддержка Telegram! Аккаунт {username}, {telegram_id} использует виртуальный номер купленный на сайте по активации номеров. Отношения к номеру он не имеет, номер никак к нему не относится. Пожалуйста, разберитесь с этим. Заранее спасибо!",
    "personal_data_channel_en": f"Здравствуйте, уважаемая поддержка Telegram. На вашей платформе я нашел канал, который распространяет личные данные невинных людей. Ссылка на канал - {channel}, Ссылка на нарушение - {link_for_channel}. Пожалуйста, заблокируйте данный канал.",
    "flaying_channel_en": f"Здравствуйте, уважаемая поддержка Telegram. На вашей платформе я нашел канал который распространяет жестокое обращение с животными. Ссылка на канал - {channel}, Ссылка на нарушение - {link_for_channel}. Пожалуйста, заблокируйте данный канал.",
    "cp_channel_en": f"Здравствуйте, уважаемая поддержка Telegram. На вашей платформе я нашел канал который распространяет порнографию с участием несовершеннолетних. Ссылка на канал - {channel}, Ссылка на нарушение - {link_for_channel}. Пожалуйста, заблокируйте данный канал.",
    "price_channel_en": f"Здравствуйте, уважаемый модератор Telegram. Хочу вам пожаловаться на канал, который продает услуги доксинга и сваттинга. Ссылка на телеграмм канал: {channel} Ссылка на нарушение: {link_for_channel} Просьба заблокировать данный канал.",
    "pornography_channel_en": f"Здравствуйте, уважаемая поддержка Telegram. Я нашел канал, который распространяет порнографический контент. Ссылка на канал - {channel}, Ссылка на нарушение - {link_for_channel}. Пожалуйста, примите меры по блокировке данного канала.",
    "violence_channel_en": f"Здравствуйте, уважаемая поддержка Telegram. Я нашел канал, который распространяет контент, содержащий насилие или жестокое обращение. Ссылка на канал - {channel}, Ссылка на нарушение - {link_for_channel}. Пожалуйста, примите меры по блокировке данного канала.",
    "osint_bot_en": f"Здравствуйте, уважаемая поддержка Telegram. На вашей платформе я нашел бота, который осуществляет поиск по личным данным ваших пользователей. Ссылка на бота - {username_bot}. Пожалуйста, разберитесь и заблокируйте данного бота."
    }

    # Маппинг для соответствия строк с эмодзи и другими значениями на правильные ключи в REPORT_TEXTS // Matching strings with emoji and other values ​​for keys in REPORT_TEXTS
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
        "🔞 Порнография (18+)": "pornography_channel",
        "🩸 Насилие": "violence_channel",
        "🕵️‍♂️ Осинт бот": "osint_bot",
        "📅 7 дней (70₽)": "7",
        "📅 14 дней (140₽)": "14",
        "📅 30 дней (210₽)": "30",
        "📅 60 дней (420₽)": "60",

        "🚫 Spam": "spam_user_en",
        "🔒 Personal data": "personal_data_user_en",
        "😈 Trolling": "trolling_user_en",
        "🗑️ Delete sessions": "delete_sessions_user_en",
        "💎 Premium": "premium_user_en",
        "🌐 Virtual number": "virtual_number_user_en",
        "🔐 Personal data in channel": "personal_data_channel_en",
        "🐾 Animal cruelty": "animal_cruelty_channel_en",
        "🚫 CP": "cp_channel_en",
        "📜 Price-list (DOX & SWAT)": "price_channel_en",
        "🔞 Pornography (18+)": "pornography_channel_en",
        "🩸 Violence": "violence_channel_en",
        "🕵️‍♂️ Osint bot": "osint_bot_en",
        "📅 7 days (70₽)": "7",
        "📅 14 days (140₽)": "14",
        "📅 30 days (210₽)": "30",
        "📅 60 days (420₽)": "60"
    }

    # Пример для добавления почты: // Example for adding mail:
    
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
    #     # Продолжайте добавлять данные для остальных почт // Continue adding data for other mails
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

                    if user_language == "ru":
                        await callback.message.answer(
                            f"Письмо отправлено с {account_email} на {recipient}",
                            parse_mode="HTML",
                            reply_markup=kb.stop)
                        
                    elif user_language == "en":
                        await callback.message.answer(
                            f"Email sent from {account_email} to {recipient}",
                            parse_mode="HTML",
                            reply_markup=kb.stop_en)

                except Exception as e:
                    from html import escape

                    if user_language == "ru":
                        await callback.message.answer(
                            f"❌ Не удалось отправить письмо с {account_email} на {recipient}: {escape(str(e))}",
                            parse_mode="HTML",
                            reply_markup=kb.stop)
                        
                    if user_language == "en":
                        await callback.message.answer(
                            f"❌ Failed to send email from {account_email} to {recipient}: {escape(str(e))}",
                            parse_mode="HTML",
                            reply_markup=kb.stop_en)                              

                    await asyncio.sleep(DELAY)  # Задержка между отправками // Delay between shipments

    if callback.data == "confirm_mailing_yes":

        if user_language == "ru":
            await callback.message.answer(
                "<b>✅ Отправка жалоб успешно начата!</b>",
                parse_mode="HTML",
                reply_markup=kb.stop)
        
        elif user_language == "en":
            await callback.message.answer(
                "<b>✅ Sending complaints started successfully!</b>",
                parse_mode="HTML",
                reply_markup=kb.stop_en)

        reason = reason_map.get(reason, reason)

        await distribute_emails(callback, reason, data)

        await state.clear()

    elif callback.data == "confirm_mailing_no":

        if user_language == "ru":
            await callback.message.answer(
                "<b>❌ Вы отменили процесс. Используйте кнопку ниже, чтобы начать заново.</b>",
                parse_mode="HTML",
                reply_markup=kb.start)
            
            await state.clear()

        elif user_language == "en":
            await callback.message.answer(
                "<b>❌ You have canceled the process. Use the button below to start again.</b>",
                    parse_mode="HTML",
                    reply_markup=kb.start_en)
                        
            await state.clear()

@router.callback_query(F.data == "cancel")
async def cancel(callback: CallbackQuery, state: FSMContext):

    user_id = callback.from_user.id

    user_language = await get_user_language(user_id)

    if user_language == "ru":
        await callback.message.answer(
            "<b>❌ Действие успешно отменено.</b>",
            parse_mode="HTML",
            reply_markup=kb.menu)
        
        await state.clear()
    
    elif user_language == "en":
        await callback.message.answer(
            "<b>❌ The action was successfully cancelled.</b>",
            parse_mode="HTML",
            reply_markup=kb.menu_en)
        
        await state.clear()

@router.callback_query(F.data == "stop")
async def stop(callback: CallbackQuery):

    await callback.answer()

    global stop_mailing
    stop_mailing = True

    user_id = callback.from_user.id

    user_language = await get_user_language(user_id)

    if user_language == "ru":
        await callback.message.answer(
            "<b>⛔ Рассылка успешно остановлена.</b>",
            parse_mode="HTML",
            reply_markup=kb.repeat)
        
    elif user_language == "en":
        await callback.message.answer(
            "<b>⛔️ Mailing stopped successfully.</b>",
            parse_mode="HTML",
            reply_markup=kb.repeat_en)
    
@router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery):

    await callback.answer()

    user_id = callback.from_user.id

    user_info = await get_user_info(callback.from_user.id)

    if user_info:
        user_id, registration_date, balance, subscription_date = user_info

    subscription_datetime = await get_subscription_datetime(user_id)
    
    current_timestamp = int(time.time())
    
    user_language = await get_user_language(user_id)

    if subscription_datetime > current_timestamp:
        subscription_date = datetime.fromtimestamp(subscription_datetime).strftime('%d.%m.%Y %H:%M:%S')
    
        if user_language == "ru":
            subscription_text = f"<b>💎 Активна до</b> {subscription_date}"
        elif user_language == "en":
            subscription_text = f"<b>💎 Active until</b> {subscription_date}"

    elif user_id in ADMINS:
        if user_language == "ru":
            subscription_text = "<b>💎 Активна</b>"
        elif user_language == "en":
            subscription_text = "<b>💎 Active</b>"
    else:
        if user_language == "ru":
            subscription_text = "<b>❌ Отсутствует</b>"
        elif user_language == "en":
            subscription_text = "<b>❌ Missing</b>"

    if user_language == "ru":
        await callback.message.answer(
            "<b>👤 Ваш профиль:</b>\n\n"
            f"<b>🆔 Ваш Telegram ID:</b> <code>{user_id}</code>\n"
            f"<b>📅 Дата регистрации:</b> {registration_date}\n"
            f"<b>💰 Баланс:</b> {balance} ₽\n"
            f"<b>🌟 Статус подписки:</b> {subscription_text}\n",
            parse_mode="HTML",
            reply_markup=kb.profile)

    elif user_language == "en":
        await callback.message.answer(
            "<b>👤 Your Profile:</b>\n\n"
            f"<b>🆔 Your Telegram ID:</b> <code>{user_id}</code>\n"
            f"<b>📅 Registration Date:</b> {registration_date}\n"
            f"<b>💰 Balance:</b> {balance} ₽\n"
            f"<b>🌟 Subscription Status:</b> {subscription_text}\n",
            parse_mode="HTML",
            reply_markup=kb.profile_en)

class SubscriptionBuy(StatesGroup):
    subscription_duration = State()
    pay = State()
    confirm = State()

@router.callback_query(F.data == "subscription_buy")
async def subscription_buy(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    user_id = callback.from_user.id

    user_language = await get_user_language(user_id)

    subscription_datetime = await get_subscription_datetime(user_id)
    
    current_timestamp = int(time.time())

    if subscription_datetime > current_timestamp or user_id in ADMINS:

        if user_language == "ru":
            await callback.message.answer(
                "<b>❌ У вас уже есть активная подписка. Попробуйте позже.</b>",
                parse_mode="HTML",
                reply_markup=kb.menu)
        elif user_language == "en":
            await callback.message.answer(
                "<b>❌ You already have an active subscription. Please try again later.</b>",
                parse_mode="HTML",
                reply_markup=kb.menu_en)
    else:
        if user_language == "ru":
            await callback.message.answer(
                "<b>💎 Оформите подписку и начните пользоваться всеми возможностями бота уже сегодня!</b>\n\n"
                "<b>⏳ Выберите подходящий срок подписки:</b>",
                parse_mode="HTML",
                reply_markup=kb.subscription_duration)

            await state.set_state(SubscriptionBuy.subscription_duration)

        elif user_language == "en":
            await callback.message.answer(
                "<b>💎 Subscribe now and start using all the bot's features today!</b>\n\n"
                "<b>⏳ Choose the subscription duration:</b>",
                parse_mode="HTML",
                reply_markup=kb.subscription_duration_en)

            await state.set_state(SubscriptionBuy.subscription_duration)

@router.callback_query(SubscriptionBuy.subscription_duration)
async def subscription_duration(callback: CallbackQuery, state: FSMContext):

    callback_data = callback.data

    user_id = callback.from_user.id

    user_language = await get_user_language(user_id)

    try:
        duration = callback_data.split("|")[0]
    except IndexError:
        if user_language == "ru":
            await callback.answer("❌ Произошла ошибка. Пожалуйста, выберите срок подписки еще раз.")
            return
        elif user_language == "en":
            await callback.answer("❌ An error occurred. Please select the subscription duration again.")
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
        if user_language == "ru":
            price = "❌ Неизвестная сумма"
        elif user_language == "en":
            price = "❌ Unknown amount"

    await state.update_data(duration=duration, price=price)

    if user_language == "ru":
        await callback.message.answer(
            "<b>🔍 Пожалуйста, проверьте введенные данные:</b>\n\n"
            f"<b>⏳ Срок для подписки: {duration} дней</b>\n"
            f"<b>💰 Сумма для оплаты:</b> {price} ₽\n\n"
            "<b>👇 Нажмите на кнопку ниже, чтобы оплатить. После этого подтвердите операцию.</b>",
            parse_mode="HTML",
            reply_markup=kb.pay)
        
        await state.set_state(SubscriptionBuy.pay)
    
    elif user_language == "en":
        await callback.message.answer(
            "<b>🔍 Please check the entered details:</b>\n\n"
            f"<b>⏳ Subscription duration: {duration} days</b>\n"
            f"<b>💰 Payment amount:</b> {price} ₽\n\n"
            "<b>👇 Click the button below to pay. After that, confirm the transaction.</b>",
            parse_mode="HTML",
            reply_markup=kb.pay_en)

        await state.set_state(SubscriptionBuy.pay)

@router.callback_query(SubscriptionBuy.pay)
async def pay(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()

    price = data.get('price')

    user_id = callback.from_user.id
    user_info = await get_user_info(user_id)
    _, _, balance, _ = user_info

    new_balance = int(balance) - int(price)

    user_language = await get_user_language(user_id)

    await state.update_data(user_id=user_id, new_balance=new_balance, balance=balance, price=price)

    if user_language == "ru":
        await callback.message.answer(
            "<b>📝 Детали оплаты:</b>\n\n"
            f"<b>💰 Ваш текущий баланс:</b> {balance} ₽\n"
            f"<b>📉 Баланс после оплаты:</b> {new_balance} ₽\n"
            f"<b>💵 Сумма к оплате:</b> {price} ₽\n\n"
            "<b>✅ Подтвердить оплату?</b>",
            parse_mode="HTML",
            reply_markup=kb.confirm_pay_yes_no)

        await state.set_state(SubscriptionBuy.confirm)

    elif user_language == "en":
        await callback.message.answer(
            "<b>📝 Payment details:</b>\n\n"
            f"<b>💰 Your current balance:</b> {balance} ₽\n"
            f"<b>📉 Balance after payment:</b> {new_balance} ₽\n"
            f"<b>💵 Amount to pay:</b> {price} ₽\n\n"
            "<b>✅ Confirm payment?</b>",
            parse_mode="HTML",
            reply_markup=kb.confirm_pay_yes_no_en)

        await state.set_state(SubscriptionBuy.confirm)

@router.callback_query(SubscriptionBuy.confirm)
async def confirm(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('user_id')
    duration = data.get('duration')
    new_balance = data.get('new_balance')
    balance = data.get('balance')
    price = data.get('price')

    my_user_id = callback.from_user.id

    user_language = await get_user_language(my_user_id)

    if callback.data == "confirm_pay_yes":
        if int(balance) >= int(price):
            duration_in_seconds = int(duration) * 86400
            current_timestamp = int(time.time())
            duration_result = duration_in_seconds + int(current_timestamp)

            await subtract_balance(new_balance, user_id)
            await add_subscription(duration_result, user_id)

            if user_language == "ru":
                await callback.message.answer(
                    f"<b>✅ Оплата успешно завершена!</b>\n\n"
                    f"<b>🆔 Ваш ID:</b> {user_id}\n"
                    f"<b>⏳ Срок подписки: {duration} дней</b>\n"
                    f"<b>💰 Новый баланс:</b> {new_balance} ₽\n\n"
                    "<b>🎉 Спасибо за оплату! Ваша подписка активирована. Если у вас возникнут вопросы, наша поддержка всегда на связи. 😊</b>",
                    parse_mode="HTML",
                    reply_markup=kb.menu)
            elif user_language == "en":
                await callback.message.answer(
                    f"<b>✅ Payment successfully completed!</b>\n\n"
                    f"<b>🆔 Your ID:</b> {user_id}\n"
                    f"<b>⏳ Subscription duration: {duration} days</b>\n"
                    f"<b>💰 New balance:</b> {new_balance} ₽\n\n"
                    "<b>🎉 Thank you for your payment! Your subscription is now active. If you have any questions, our support is always available. 😊</b>",
                    parse_mode="HTML",
                    reply_markup=kb.menu_en)
        else:
            if user_language == "ru":
                await callback.message.answer(
                    "<b>❌ Ошибка!</b>\n\n"
                    "<b>У вас недостаточно средств на балансе для завершения оплаты.</b> 💸\n"
                    "<b>Попробуйте пополнить баланс и повторите попытку.</b> 💳",
                    parse_mode="HTML",
                    reply_markup=kb.menu)
                
            elif user_language == "en":
                await callback.message.answer(
                    "<b>❌ Error!</b>\n\n"
                    "<b>You do not have enough funds in your balance to complete the payment.</b> 💸\n"
                    "<b>Please try adding funds to your balance and try again.</b> 💳",
                    parse_mode="HTML",
                    reply_markup=kb.menu_en)

    elif callback.data == "confirm_pay_no":
        if user_language == "ru":
            await callback.message.answer(
                "<b>❌ Вы отменили процесс. Используйте кнопку ниже, чтобы начать заново.</b>",
                parse_mode="HTML",
                reply_markup=kb.menu)

            await state.clear()
        
        elif user_language == "en":
            await callback.message.answer(
                "<b>❌ You have canceled the process. Use the button below to start over.</b>",
                parse_mode="HTML",
                reply_markup=kb.menu_en)

            await state.clear()

@router.callback_query(F.data == "admin_panel")
async def admin_panel(callback: CallbackQuery):

    await callback.answer()

    user_id = callback.from_user.id

    user_language = await get_user_language(user_id)

    if user_language == "ru":
        await callback.message.answer(
            "<b>💼 Добро пожаловать в Админ-Панель!</b>",
            parse_mode="HTML",
            reply_markup=kb.admin_panel)
        
    elif user_language == "en":
        await callback.message.answer(
            "<b>💼 Welcome to the Admin-Panel!</b>",
            parse_mode="HTML",
            reply_markup=kb.admin_panel_en)

class UserManagement(StatesGroup):
    user_id = State()
    action = State()
    duration = State()
    confirm = State()
    amount_new_balance = State()

@router.callback_query(F.data == "user_management")
async def user_management(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    user_id = callback.from_user.id

    user_language = await get_user_language(user_id)

    if user_language == "ru":
        await callback.message.answer(
            "<b>🔍 Введите ID пользователя:</b>",
            parse_mode="HTML",
            reply_markup=kb.cancel)

        await state.set_state(UserManagement.user_id)
    
    elif user_language == "en":
        await callback.message.answer(
            "<b>🔍 Enter the user ID:</b>",
            parse_mode="HTML",
            reply_markup=kb.cancel)

        await state.set_state(UserManagement.user_id)

@router.message(UserManagement.user_id)
async def get_user_id(message: Message, state: FSMContext):

    user_id = message.text

    my_user_id = message.from_user.id

    user_language = await get_user_language(my_user_id)    

    await state.update_data(user_id=user_id)

    if not await user_exists(user_id):
            
            if user_language == "ru":
                await message.answer(
                    "<b>🚫 Пользователь не найден! Возможно, ID указан с ошибкой.</b>",
                    parse_mode="HTML",
                    reply_markup=kb.menu)
                
            elif user_language == "en":
                await message.answer(
                    "<b>🚫 User not found! The ID might be incorrect.</b>",
                    parse_mode="HTML",
                    reply_markup=kb.menu_en)
    else:
        if user_language == "ru":

            await message.answer(
                f"<b>👤 Введеный ID пользователя:</b> <code>{user_id}</code>\n\n"
                "<b>🛠️ Выберите действие:</b>",
                parse_mode="HTML",
                reply_markup=kb.user_management)

            await state.set_state(UserManagement.action)

        elif user_language == "en":
            await message.answer(
                f"<b>👤 Entered user ID:</b> <code>{user_id}</code>\n\n"
                "<b>🛠️ Choose an action:</b>",
                parse_mode="HTML",
                reply_markup=kb.user_management_en)

            await state.set_state(UserManagement.action)

@router.callback_query(UserManagement.action)
async def action(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    user_id = data.get('user_id')
    action = callback.data.split("|")[1]

    await state.update_data(action=action)

    my_user_id = callback.from_user.id

    user_language = await get_user_language(my_user_id)

    if action == "🎁 Подарить подписку" or action == "🎁 Give a subscription":
        if user_language == "ru":
            await callback.message.answer(
                "📅 <b>Введите количество дней для подписки:</b>\n"
                "🔢 <b>Например: 7, 30 или 365.</b>",
            parse_mode="HTML")
            
            await state.set_state(UserManagement.duration)
        
        elif user_language == "en":
            await callback.message.answer(
                "📅 <b>Enter the number of days for the subscription:</b>\n"
                "🔢 <b>For example: 7, 30, or 365.</b>",
                parse_mode="HTML")

            await state.set_state(UserManagement.duration)

    if action == "💸 Изменить баланс" or action == "💸 Change balance":
        user_info = await get_user_info(user_id)
        _, _, balance, _ = user_info

        await state.update_data(balance=balance)

        if user_language == "ru":
            await callback.message.answer(
                f"<b>💰 Текущий баланс пользователя с ID: {user_id} - {balance} ₽</b>\n\n"
                "<b>💸 Введите новый баланс:</b>",
                parse_mode="HTML",
                reply_markup=kb.cancel)
            
            await state.set_state(UserManagement.amount_new_balance)

        elif user_language == "en":
            await callback.message.answer(
                f"<b>💰 Current balance of the user with ID: {user_id} - {balance} ₽</b>\n\n"
                "<b>💸 Enter the new balance:</b>",
                parse_mode="HTML",
                reply_markup=kb.cancel_en)

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

            my_user_id = message.from_user.id

            user_language = await get_user_language(my_user_id)

            if user_language == "ru":
                await message.answer(
                    "<b>🔍 Пожалуйста, проверьте введенные данные:</b>\n\n"
                    f"<b>🆔 ID пользователя:</b> <code>{user_id}</code>\n"
                    f"<b>🛠️ Действие:</b> {action}\n"
                    f"<b>💸 Обновленный баланс пользователя:</b> {amount_new_balance} ₽\n\n"
                    "<b>➡️ Хотите продолжить?</b>",
                    parse_mode="HTML",
                    reply_markup=kb.confirm_change_balance_yes_no)
                
                await state.set_state(UserManagement.confirm)

            elif user_language == "en":
                await message.answer(
                    "<b>🔍 Please check the entered data:</b>\n\n"
                    f"<b>🆔 User ID:</b> <code>{user_id}</code>\n"
                    f"<b>🛠️ Action:</b> {action}\n"
                    f"<b>💸 Updated user balance:</b> {amount_new_balance} ₽\n\n"
                    "<b>➡️ Do you want to continue?</b>",
                    parse_mode="HTML",
                    reply_markup=kb.confirm_change_balance_yes_no_en)

                await state.set_state(UserManagement.confirm)
        else:
            if user_language == "ru":
                await message.reply("<b>⚠️ Пожалуйста, введите целое число не меньше нуля.</b>", parse_mode="HTML")
            elif user_language == "en":
                await message.reply("<b>⚠️ Please enter a whole number greater than or equal to zero.</b>", parse_mode="HTML")
    except ValueError:
        if user_language == "ru":
            await message.reply("<b>❌ Введите корректное целое число.</b>", parse_mode="HTML")
        elif user_language == "en":
            await message.reply("<b>❌ Please enter a valid whole number.</b>", parse_mode="HTML")

@router.message(UserManagement.duration)
async def duration(message: Message, state: FSMContext):

    my_user_id = message.from_user.id
    user_language = await get_user_language(my_user_id)

    try:
        duration = int(message.text)

        if duration > 0:
            await state.update_data(duration=duration)

            data = await state.get_data()
            user_id = data.get('user_id')
            action = data.get('action')

            def days_declension(n, user_language):
                if user_language == "ru":

                    if 11 <= n % 100 <= 19:
                        return f"{n} дней"
                    last_digit = n % 10
                    if last_digit == 1:
                        return f"{n} день"
                    elif 2 <= last_digit <= 4:
                        return f"{n} дня"
                    else:
                        return f"{n} дней"
                elif user_language == "en":

                    if n == 1:
                        return f"{n} day"
                    else:
                        return f"{n} days"

            duration_text = days_declension(duration, user_language)

            if user_language == "ru":
                await message.answer(
                    "<b>🔍 Пожалуйста, проверьте введенные данные:</b>\n\n"
                    f"<b>🆔 ID пользователя:</b> <code>{user_id}</code>\n"
                    f"<b>🛠️ Действие:</b> {action}\n"
                    f"<b>⌛ Длительность подписки:</b> {duration_text}\n\n"
                    "<b>➡️ Хотите продолжить?</b>",
                    parse_mode="HTML",
                    reply_markup=kb.confirm_gift_a_sub_yes_no)

                await state.set_state(UserManagement.confirm)

            elif user_language == "en":
                await message.answer(
                    "<b>🔍 Please check the entered data:</b>\n\n"
                    f"<b>🆔 User ID:</b> <code>{user_id}</code>\n"
                    f"<b>🛠️ Action:</b> {action}\n"
                    f"<b>⌛ Subscription duration:</b> {duration_text}\n\n"
                    "<b>➡️ Do you want to continue?</b>",
                    parse_mode="HTML",
                    reply_markup=kb.confirm_gift_a_sub_yes_no_en)

                await state.set_state(UserManagement.confirm)
        else:
            if user_language == "ru":
                await message.reply("<b>⚠️ Пожалуйста, введите положительное целое число.</b>", parse_mode="HTML")
            elif user_language == "en":
                await message.reply("<b>⚠️ Please enter a positive integer.</b>", parse_mode="HTML")
    except ValueError:
        if user_language == "ru":
            await message.reply("<b>❌ Введите корректное целое число.</b>", parse_mode="HTML")
        elif user_language == "en":
            await message.reply("<b>❌ Please enter a valid integer.</b>", parse_mode="HTML")

@router.callback_query(UserManagement.confirm)
async def confirm(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('user_id')
    duration = data.get('duration')
    balance = data.get('balance')
    amount_new_balance = data.get('amount_new_balance')

    my_user_id = callback.from_user.id

    user_language = await get_user_language(my_user_id)

    if callback.data == "confirm_gift_a_sub_yes":

        duration_in_seconds = duration * 86400
        current_timestamp = int(time.time())
        new_subscription_end = duration_in_seconds + current_timestamp

        current_subscription = await get_subscription_datetime(user_id)

        current_sub_date = datetime.fromtimestamp(current_subscription).strftime('%d.%m.%Y %H:%M:%S')

        if new_subscription_end <= current_subscription:
            if user_language == "ru":
                await callback.message.answer(
                    f"<b>⚠ Ошибка:</b> У пользователя уже есть подписка на больший или равный срок!\n\n"
                    f"<b>📅 Текущая подписка активна до:</b> <code>{current_sub_date}</code>\n"
                    f"<i>⏳ Попробуйте подарить подписку с большим сроком.</i>",
                    parse_mode="HTML",
                    reply_markup=kb.menu)
                return
        
            elif user_language == "en":
                await callback.message.answer(
                    f"<b>⚠ Error:</b> The user already has a subscription with an equal or longer duration!\n\n"
                    f"<b>📅 Current subscription active until:</b> <code>{current_sub_date}</code>\n"
                    f"<i>⏳ Try gifting a subscription with a longer duration.</i>",
                    parse_mode="HTML",
                    reply_markup=kb.menu_en)
                return

        await add_subscription(new_subscription_end, user_id)

        if user_language == "ru":
            await callback.message.answer(
                "<b>🎁 Подписка успешно подарена!✨</b>\n\n"
                f"<i>⌛ Срок действия: {duration} дней.</i>",
                parse_mode="HTML",
                reply_markup=kb.menu)
        
        elif user_language == "en":
            await callback.message.answer(
                "<b>🎁 Subscription successfully gifted!✨</b>\n\n"
                f"<i>⌛ Duration: {duration} days.</i>",
                parse_mode="HTML",
                reply_markup=kb.menu_en)

    elif callback.data == "confirm_gift_a_sub_no":
        if user_language == "ru":
            await callback.message.answer(
                "<b>❌ Вы отменили процесс. Используйте кнопку ниже, чтобы начать заново.</b>",
                parse_mode="HTML",
                reply_markup=kb.menu)

            await state.clear()
        
        elif user_language == "en":
            await callback.message.answer(
                "<b>❌ You have cancelled the process. Use the button below to start over.</b>",
                parse_mode="HTML",
                reply_markup=kb.menu_en)

            await state.clear() 

    if callback.data == "confirm_change_balance_yes":

        await change_balance(amount_new_balance, user_id)

        if user_language == "ru":

            await callback.message.answer(
                "<b>🔄 Баланс пользователя успешно обновлён!</b>\n\n"
                f"<b>📊 Старый баланс:</b> {balance} ₽\n"
                f"<b>🆕 Новый баланс:</b> {amount_new_balance} ₽\n\n"
                "<b>✅ Все изменения успешно внесены.</b>",
                parse_mode="HTML",
                reply_markup=kb.menu)
        
        elif user_language == "en":
            await callback.message.answer(
                "<b>🔄 User's balance has been successfully updated!</b>\n\n"
                f"<b>📊 Old balance:</b> {balance} ₽\n"
                f"<b>🆕 New balance:</b> {amount_new_balance} ₽\n\n"
                "<b>✅ All changes have been successfully applied.</b>",
                parse_mode="HTML",
                reply_markup=kb.menu_en)
            
    elif callback.data == "confirm_change_balance_no":
        if user_language == "ru":
            await callback.message.answer(
                "<b>❌ Вы отменили процесс. Используйте кнопку ниже, чтобы начать заново.</b>",
                parse_mode="HTML",
                reply_markup=kb.menu)

            await state.clear()
        
        elif user_language == "en":
            await callback.message.answer(
                "<b>❌ You have canceled the process. Use the button below to start over.</b>",
                parse_mode="HTML",
                reply_markup=kb.menu_en)

            await state.clear()

class AddBalance(StatesGroup):
    payment_system = State()
    amount = State()
    confirm = State()

@router.callback_query(F.data == "add_balance")
async def add_balance(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    user_id = callback.from_user.id

    user_language = await get_user_language(user_id)

    if user_language == "ru":
        await callback.message.answer(
            "<b>💸 Выберите платежную систему:</b>",
            parse_mode="HTML",
            reply_markup=kb.payment_systems)

        await state.set_state(AddBalance.payment_system)
    
    elif user_language == "en":
        await callback.message.answer(
            "<b>💸 Choose a payment system:</b>",
            parse_mode="HTML",
            reply_markup=kb.payment_systems)

        await state.set_state(AddBalance.payment_system)

@router.callback_query(AddBalance.payment_system)
async def get_payment_system(callback: CallbackQuery, state: FSMContext):
    
    payment_system = callback.data.split("|")[1]

    user_id = callback.from_user.id

    user_language = await get_user_language(user_id)

    await state.update_data(payment_system=payment_system)

    if user_language == "ru":
        await callback.message.answer(
            f"<b>💸 Платежная система которую вы выбрали: {payment_system}</b>\n\n"
            "<b>💰 Теперь введите сумму для пополнения:</b>",
            parse_mode="HTML",
            reply_markup=kb.cancel)
        
        await state.set_state(AddBalance.amount)
    
    elif user_language == "en":
        await callback.message.answer(
            f"<b>💸 The payment system you selected: {payment_system}</b>\n\n"
            "<b>💰 Now, please enter the amount to top up:</b>",
            parse_mode="HTML",
            reply_markup=kb.cancel)

        await state.set_state(AddBalance.amount)

@router.message(AddBalance.amount)
async def enter_amount(message: Message, state: FSMContext):
    try:
        amount = int(message.text)

        data = await state.get_data()

        payment_system = data.get('payment_system')

        user_id = message.from_user.id

        user_language = await get_user_language(user_id)

        if int(amount) > 0:
            await state.update_data(amount=amount)

            if user_language == "ru":
                await message.answer(
                    "<b>🔍 Пожалуйста, проверьте введенные данные:</b>\n\n"
                    f"<b>💸 Платежная система: {payment_system}</b>\n"
                    f"<b>💰 Сумма для пополнения: {amount} ₽</b>\n\n"
                    "<b>➡️ Все указано верно?</b>",
                    parse_mode="HTML",
                    reply_markup=kb.confirm_add_balance_yes_no)
                
                await state.set_state(AddBalance.confirm)
            
            elif user_language == "en":
                await message.answer(
                    "<b>🔍 Please check the entered details:</b>\n\n"
                    f"<b>💸 Payment system: {payment_system}</b>\n"
                    f"<b>💰 Amount to top up: {amount} ₽</b>\n\n"
                    "<b>➡️ Is everything correct?</b>",
                    parse_mode="HTML",
                    reply_markup=kb.confirm_add_balance_yes_no_en)

                await state.set_state(AddBalance.confirm)
        else:
            if user_language == "ru":
                await message.reply("⚠️ Пожалуйста, введите только чётное положительное число.")
            elif user_language == "en":
                await message.reply("⚠️ Please enter only an even positive number.")
    except ValueError:
        if user_language == "ru":
            await message.reply("❌ Пожалуйста, введите корректную сумму в рублях (целое положительное число).")
        elif user_language == "en":
            await message.reply("❌ Please enter a valid amount in rubles (a positive whole number).")

@router.callback_query(F.data.startswith("CHECK|"))
async def check_invoice(callback: CallbackQuery, state: FSMContext):

    await callback.answer()

    data = await state.get_data()

    amount = data.get('amount')
    payment_id = data.get('payment_id')
    invoice_id = int(callback.data.split("|")[1])

    user_id = callback.from_user.id

    user_language = await get_user_language(user_id)

    try:
        invoice = await acp.get_invoices(invoice_ids=invoice_id)

    except Exception as e:
        if user_language == "ru":
            await callback.answer(f"❌ Ошибка при получении статуса счета: {str(e)}")
            return
        elif user_language == "en":
            await callback.answer(f"❌ Error while retrieving the account status: {str(e)}")
            return

    if invoice.status == "paid":
        if await check_balance_updated(invoice_id):
            if user_language == "ru":
                await callback.message.answer("✅ Баланс уже был обновлен ранее.")
                return
            elif user_language == "en":
                await callback.message.answer("✅ The balance has already been updated earlier.")
                return
            
        if user_language == "ru":
            await callback.answer("✅ Проверка завершена: статус оплаты подтвержден.")
        elif user_language == "en":
            await callback.answer("✅ Check completed: payment status confirmed.")

        user_info = await get_user_info(user_id)
        _, _, balance, _ = user_info
        new_balance = int(balance) + int(amount)

        invoice_status = invoice.status

        await update_invoice_status(invoice_status, invoice_id)

        await balance_updated(invoice_id)

        await top_up_balance(new_balance, user_id)

        if user_language == "ru":
            await callback.message.answer(
                f"<b>🎉 Пополнение баланса успешно!</b>\n\n"
                f"<b>💸 Сумма пополнения:</b> {amount} ₽\n"
                f"<b>🆔 ID платежа:</b> <code>{payment_id}</code>\n\n"
                f"<b>🔄 Ваш баланс обновлен. 😄</b>",
                parse_mode="HTML",
                reply_markup=kb.menu)
        
        elif user_language == "en":
            await callback.message.answer(
                f"<b>🎉 Balance top-up successful!</b>\n\n"
                f"<b>💸 Top-up amount:</b> {amount} ₽\n"
                f"<b>🆔 Payment ID:</b> <code>{payment_id}</code>\n\n"
                f"<b>🔄 Your balance has been updated. 😄</b>",
                parse_mode="HTML",
                reply_markup=kb.menu_en)

    elif invoice.status == 'expired':
        if user_language == "ru":
            await callback.answer("❌ Счет истек. Пожалуйста, создайте новый.")
        elif user_language == "en":
            await callback.answer("❌ The account has expired. Please create a new one.")
    else:
        if user_language == "ru":
            await callback.answer("❌ Счет пока не оплачен. Пожалуйста, повторите проверку позже.")
        elif user_language == "en":
            await callback.answer("❌ The account has not been paid yet. Please check again later.")

@router.callback_query(AddBalance.confirm)
async def confirm(callback: CallbackQuery, state: FSMContext):

    user_id = callback.from_user.id

    user_language = await get_user_language(user_id)

    try:
        data = await state.get_data()

        payment_system = data.get('payment_system')
        amount = data.get('amount')

        if callback.data == "confirm_add_balance_yes":

            if user_language == "ru":
                description = f'Пополнение баланса на {amount} ₽ 💵'
            elif user_language == "en":
                description = f'Balance top-up of {amount} ₽ 💵'

            invoice = await acp.create_invoice(
                currency_type='fiat',
                asset='USDT',
                fiat='RUB',
                amount=amount,
                description=description
            )

            invoice_id = invoice.invoice_id
            invoice_status = invoice.status

            payment_id = str(uuid.uuid4())
            payment_amount = int(amount)
            payment_date = datetime.now().strftime('%d.%m.%Y %H:%M:%S')

            await log_payment(user_id, invoice_id, invoice_status, payment_id, payment_amount, payment_date)

            await state.update_data(invoice_id=invoice.invoice_id, payment_id=payment_id, amount=amount)

            if user_language == "ru":

                pay_button = InlineKeyboardButton(text="💵 Оплатить", url=invoice.bot_invoice_url)
                payment_confirm_button = InlineKeyboardButton(text="✅ Проверить оплату", callback_data=f"CHECK|{invoice.invoice_id}")
                pay_markup = InlineKeyboardMarkup(inline_keyboard=[[pay_button], [payment_confirm_button]])

            elif user_language == "en":

                pay_button = InlineKeyboardButton(text="💵 Pay", url=invoice.bot_invoice_url)
                payment_confirm_button = InlineKeyboardButton(text="✅ Check Payment", callback_data=f"CHECK|{invoice.invoice_id}")
                pay_markup = InlineKeyboardMarkup(inline_keyboard=[[pay_button], [payment_confirm_button]])

            if user_language == "ru":
                await callback.message.answer(
                    f"<b>🏦 Информация о пополнении:</b>\n\n"
                    f"<i>🔹 Платежная система:</i> <b>{payment_system}</b>\n"
                    f"<i>🔹 Сумма к оплате:</i> <b>{amount} ₽</b>\n"
                    f"<i>🔹 ID платежа:</i> <b><code>{payment_id}</code></b>\n\n"
                    "<i>🔻 Для завершения операции нажмите кнопку ниже, чтобы произвести оплату:</i>",
                    parse_mode="HTML",
                    reply_markup=pay_markup)

            elif user_language == "en":
                await callback.message.answer(
                    f"<b>🏦 Top-up Information:</b>\n\n"
                    f"<i>🔹 Payment system:</i> <b>{payment_system}</b>\n"
                    f"<i>🔹 Amount to pay:</i> <b>{amount} ₽</b>\n"
                    f"<i>🔹 Payment ID:</i> <b><code>{payment_id}</code></b>\n\n"
                    "<i>🔻 To complete the operation, press the button below to make the payment:</i>",
                    parse_mode="HTML",
                    reply_markup=pay_markup)

            elif callback.data == "confirm_add_balance_no":
                if user_language == "ru":
                    await callback.message.answer(
                        "<b>❌ Вы отменили процесс.</b>\n"
                        "<i>Используйте кнопку ниже, чтобы открыть главное меню.</i>",
                        parse_mode="HTML",
                        reply_markup=kb.menu)
                    await state.clear()

                elif user_language == "en":
                    await callback.message.answer(
                        "<b>❌ You have canceled the process.</b>\n"
                        "<i>Use the button below to open the main menu.</i>",
                        parse_mode="HTML",
                        reply_markup=kb.menu)
                    await state.clear()

    except Exception as e:
        if user_language == "ru":
            await callback.message.answer("<b>❌ Произошла ошибка при создании счета. Попробуйте еще раз.</b>", parse_mode="HTML")
        elif user_language == "en":
            await callback.message.answer("<b>❌ An error occurred while creating the invoice. Please try again.</b>", parse_mode="HTML")

