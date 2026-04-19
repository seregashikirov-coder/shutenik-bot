import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile
from openai import AsyncOpenAI

# Получаем ключи из переменных Railway
TG_TOKEN = os.getenv("TG_TOKEN")
AI_KEY = os.getenv("AI_KEY")

# Настройка под Groq
client = AsyncOpenAI(
    api_key=AI_KEY,
    base_url="https://groq.com"
)

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

PROMPT = "Ты дерзкий комик. Отвечай короткими, саркастичными шутками на русском языке. Будь острым, используй сленг, подкалывай пользователя в тему сообщения."

@dp.message(Command("start"))
async def start(message: types.Message):
    # Пытаемся отправить фото, если оно есть в папке
    if os.path.exists("logo.jpg"):
        photo = FSInputFile("logo.jpg")
        await message.answer_photo(photo=photo, caption="Привет! я шутник-бот! веселись!")
    else:
        await message.answer("Привет! я шутник-бот! веселись!")

@dp.message(F.text)
async def chat(message: types.Message):
    try:
        response = await client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{"role": "system", "content": PROMPT}, {"role": "user", "content": message.text}]
        )
        await message.reply(response.choices.message.content)
    except Exception as e:
        await message.reply("Я бы пошутил, но чет ИИ приуныл...")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
