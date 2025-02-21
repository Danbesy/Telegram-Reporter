# Telegram-Reporter
**✨ Telegram Reporter ✨ — бот для автоматической отправки жалоб на пользователей, каналы и ботов в Telegram. 🚨📲**
<hr>

🔥 Возможности бота:

📩 Автоматическая отправка жалоб

Бот автоматически отправляет жалобы через письма в поддержку Telegram, что повышает эффективность и скорость блокировки нарушителей.

💰 Монетизация через CryptoBot

Для использования бота пользователям необходимо приобрести подписку прямо в боте через платежную систему CryptoBot. 

Это удобный и безопасный способ оплаты, который автоматизирует процесс доступа к функционалу.

🛠 Админ-панель

Мощная панель управления для администраторов, которая позволяет:

🔹 Изменять баланс пользователей 💵

🔹 Выдавать подписки вручную 🎁

<hr>

📄 Инструкция:

1️⃣ Для запуска бота откройте файл main.py 📂

2️⃣ Для добавления своих почт измените значения в строках начиная с 450 в файле handlers.py (следуя примеру) 💻

3️⃣ Измените TOKEN на токен вашего бота, полученный от @BotFather и CRYPTOPAY_TOKEN на ваш токен CryptoPay в @CryptoBot, в файле configs.py 💰

4️⃣ Добавьте айди пользователей (админов) в переменную ADMINS в файле configs.py 🛠️

🆔 Чтобы получить свой ID, используйте бота @getmyid_bot: откройте его в Telegram и нажмите Start — он отправит ваш ID. 🆔

<hr>

✨ Для успешной работы бота необходимы следующие библиотеки:

🔹 aiogram3 — для взаимодействия с Telegram Bot API.

🔹 aiosmtplib — для отправки email через SMTP.

🔹 aiocryptopay — для работы с платежами через CryptoBot.

🔹 aiosqlite — для работы с базой данных SQLite.
<hr>

📦 Установка:

1️⃣ Убедитесь, что у вас установлен Python 3.8+ 🐍

2️⃣ Установите необходимые библиотеки, выполнив команду:
```
pip install aiogram aiosmtplib aiocryptopay aiosqlite
```
3️⃣ Клонируйте репозиторий проекта с помощью команды:
```
git clone https://github.com/Danbesy/Telegram-Reporter
```
4️⃣ Перейдите в директорию проекта:
```
cd Telegram-Reporter
```
5️⃣ Запустите код командой:
```
python3 main.py
```
<hr>

❗ Termux – Если при попытке установить Aiogram происходит ошибка, то нужно установить Rust, команда:
```
pkg install libc++ rust
```
<hr>

🔗 GitHub: https://github.com/Danbesy/Telegram-Reporter

🚀 Быстро, удобно и эффективно!
