import aiosqlite

# Функция для подключения к базе данных
async def connect_users_db():
    return await aiosqlite.connect('users.db')

# Функция для подключения к базе данных
async def connect_logs_payments_db():
    return await aiosqlite.connect('logs_payments.db')

# Инициализация базы данных (создание таблицы, если она еще не создана)
async def init_users_db():
    conn = await connect_users_db()
    cursor = await conn.cursor()
    await cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            registration_date TEXT,
            balance INTEGER DEFAULT 0,
            subscription_datetime INTEGER DEFAULT 0
        )
    ''')
    await conn.commit()
    await conn.close()

async def init_logs_payments_db():
    conn = await connect_logs_payments_db()
    cursor = await conn.cursor()
    await cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs_payments (
            user_id INTEGER,
            invoice_id TEXT,
            invoice_status TEXT,
            payment_id TEXT,
            payment_amount INTEGER,
            payment_date TEXT,
            balance_updated TEXT DEFAULT "false",
            PRIMARY KEY (user_id, payment_id)
        )
    ''')
    await conn.commit()
    await conn.close()

# Функция для добавления нового пользователя
async def add_user(user_id, registration_date):
    conn = await connect_users_db()
    cursor = await conn.cursor()
    await cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, registration_date) VALUES (?, ?)
    ''', (user_id, registration_date,))
    await conn.commit()
    await conn.close()

# Функция для проверки, существует ли пользователь в базе данных
async def user_exists(user_id):
    conn = await connect_users_db()
    cursor = await conn.cursor()
    await cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    user = await cursor.fetchone()
    await conn.close()
    return user is not None

# Функция для проверки подписки пользователя
async def get_subscription_datetime(user_id):
    conn = await connect_users_db()
    cursor = await conn.cursor()
    await cursor.execute('SELECT subscription_datetime FROM users WHERE user_id = ?', (user_id,))
    result = await cursor.fetchone()
    await conn.close()

    # Возвращаем Unix-время, если оно есть, или None
    return result[0] if result else None

# Функция для извлечения данных пользователя из базы данных
async def get_user_info(user_id):
    conn = await connect_users_db()
    cursor = await conn.cursor()
    
    await cursor.execute("SELECT user_id, registration_date, balance, subscription_datetime FROM users WHERE user_id = ?", (user_id,))
    
    user_info = await cursor.fetchone()
    return user_info

# Функция для добавления подписки пользователю
async def add_subscription(duration_result, user_id):
    conn = await connect_users_db()
    cursor = await conn.cursor()

    await cursor.execute("UPDATE users SET subscription_datetime = ? WHERE user_id = ?", (duration_result, user_id))

    await conn.commit()
    await conn.close()

# Функция для пополнения баланса
async def top_up_balance(payment_amount, user_id):
    conn = await connect_users_db()
    cursor = await conn.cursor()

    await cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (payment_amount, user_id))

    await conn.commit()
    await conn.close()

# Функция для списания баланса
async def subtract_balance(new_balance, user_id):
    conn = await connect_users_db()
    cursor = await conn.cursor()

    await cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (new_balance, user_id))

    await conn.commit()
    await conn.close()

# Функция для смены баланса
async def change_balance(amount_new_balance, user_id):
    conn = await connect_users_db()
    cursor = await conn.cursor()

    await cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (amount_new_balance, user_id))

    await conn.commit()
    await conn.close()

# Функция для проверки на существование пользователя в БД
async def user_exists(user_id):
    conn = await connect_users_db()
    cursor = await conn.cursor()
    await cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    user = await cursor.fetchone()
    await conn.close()
    return user is not None

# Функция для создания лога платежа
async def log_payment(user_id, invoice_id, invoice_status, payment_id, payment_amount, payment_date):
    conn = await connect_logs_payments_db()
    cursor = await conn.cursor()
    await cursor.execute('''
        INSERT OR IGNORE INTO logs_payments (user_id, invoice_id, invoice_status, payment_id, payment_amount, payment_date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, invoice_id, invoice_status, payment_id, payment_amount, payment_date))
    await conn.commit()
    await conn.close()

# Функция для обновления статуса счета
async def update_invoice_status(invoice_status, invoice_id):
    conn = await connect_logs_payments_db()
    cursor = await conn.cursor()
    await cursor.execute('UPDATE logs_payments SET invoice_status = ? WHERE invoice_id = ?', (invoice_status, invoice_id,))
    await conn.commit()
    await conn.close()

# Функция обновляет флаг баланса в базе данных для указанного счета на "true"
async def balance_updated(invoice_id):
    conn = await connect_logs_payments_db()
    cursor = await conn.cursor()
    await cursor.execute('UPDATE logs_payments SET balance_updated = "true" WHERE invoice_id = ?', (invoice_id,))
    await conn.commit()
    await conn.close()

# Функция проверяет, был ли обновлен баланс для указанного счета
async def check_balance_updated(invoice_id):
    conn = await connect_logs_payments_db()
    cursor = await conn.cursor()
    
    await cursor.execute('SELECT balance_updated FROM logs_payments WHERE invoice_id = ?', (invoice_id,))
    balance_updated = await cursor.fetchone()
    
    await conn.close()

    return balance_updated and balance_updated[0] == "true"
