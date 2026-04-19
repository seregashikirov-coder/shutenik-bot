import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile
from openai import AsyncOpenAI

# Берем ключи из настроек Railway
TG_TOKEN = os.getenv("TG_TOKEN")
AI_KEY = os.getenv("AI_KEY")

# Исправленный клиент для Groq
client = AsyncOpenAI(
    api_key=AI_KEY,
    base_url="https://groq.com"
)

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

PROMPT = "Ты дерзкий комик. Отвечай короткими, саркастичными шутками на русском языке. Будь острым, используй сленг, подкалывай пользователя."

@dp.message(Command("start"))
async def start(message: types.Message):
    photo_name = "IMG_20260419_225749_338.jpg" 
    if os.path.exists(photo_name):
        await message.answer_photo(photo=FSInputFile(photo_name), caption="Привет! я шутник-бот! веселись!")
    else:
        await message.answer("Привет! я шутник-бот! веселись!")

@dp.message(F.text)
async def chat(message: types.Message):
    try:
        # Используем максимально стабильную модель Llama 3
        response = await client.chat.completions.create(
            model="llama3-70b-8192", 
            messages=[
                {"role": "system", "content": PROMPT},
                {"role": "user", "content": message.text}
            ]
        )
        await message.reply(response.choices.message.content)
    except Exception as e:
        # Если снова будет ошибка, мы увидим её подробнее
        await message.reply(f"Ошибка: {str(e)}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


