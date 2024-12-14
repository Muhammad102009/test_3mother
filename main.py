from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
import logging
import sqlite3
import asyncio
import random
from config import token

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher()

connection = sqlite3.connect("user.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS kitay (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    usersurname TEXT NOT NULL,
    phone TEXT NOT NULL,
    personal_code TEXT NOT NULL
);
""")
connection.commit()
CHINA_WAREHOUSE_ADDRESS = "г. Ош, ул. Курманжан Датка, склад №1"


def generate_personal_code():
    random_number = random.randint(100, 999)
    return f"KRE-{random_number}"

@dp.message(Command('start'))
async def start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}! Отправь мне свои данные в формате:\nФамилия Имя Телефон")

@dp.message()
async def save_client_data(message: Message):
    try:
        data = message.text.split()
        if len(data) != 3:
            await message.answer("Пожалуйста, отправьте данные в формате: Фамилия Имя Телефон")
            return

        surname, name, phone = data

        personal_code = generate_personal_code()
        cursor.execute(
            "INSERT INTO kitay (username, usersurname, phone, personal_code) VALUES (?, ?, ?, ?)",
            (name, surname, phone, personal_code)
        )
        connection.commit()

        await message.answer(f"Спасибо, {name} {surname}!\nВаш персональный код: {personal_code}\n\nАдрес склада в Китае: {CHINA_WAREHOUSE_ADDRESS}\n\n\nСохраните этот код для дальнейшего использования."
        )

    except:
        await(f"Произошла ошибкаа!!")

async def main():
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())
