import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
import logging
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import sqlite3
from config import TOKEN


async def main():
    bot = Bot(token=TOKEN)  # Создание экземпляра бота с указанием токена
    dp = Dispatcher()  # Создание диспетчера для обработки сообщений

    logging.basicConfig(level=logging.INFO)

    class Form(StatesGroup):
        name = State()
        age = State()
        grade = State()

    @dp.message(CommandStart())
    async def start(message: Message, state: FSMContext):
        await message.answer("Привет! Как тебя зовут?")
        await state.set_state(Form.name)

    @dp.message(Form.name)
    async def name(message: Message, state: FSMContext):  # Обработчик ввода имени
        await state.update_data(name=message.text)
        await message.answer("Сколько тебе лет?")
        await state.set_state(Form.age)

    @dp.message(Form.age)
    async def age(message: Message, state: FSMContext):  # Обработчик ввода возраста
        await state.update_data(age=message.text)
        await message.answer("На каком курсе ты учишься?")
        await state.set_state(Form.grade)

    @dp.message(Form.grade)
    async def city(message: Message, state: FSMContext):   # Обработчик ввода курса студента
        await state.update_data(grade=message.text)
        await message.answer("А я телебот. Я тебя запомнил.")
        user_data = await state.get_data()

        with sqlite3.connect('school_data.db') as conn:
            cur = conn.cursor()
            cur.execute('''
            CREATE TABLE IF NOT EXISTS students (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT,
               age INTEGER,
               grade TEXT)
            ''')

            cur.execute('''
               INSERT INTO students (name, age, grade) VALUES (?, ?, ?)''',
                        (user_data['name'], user_data['age'], user_data['grade']))
            conn.commit()
            # conn.close()

    await dp.start_polling(bot)  # Запуск обработчиков и начало получения сообщений

if __name__ == "__main__":
    asyncio.run(main())
