import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile
from openai import AsyncOpenAI

# Берем ключи из настроек Railway
TG_TOKEN = os.getenv("TG_TOKEN")
AI_KEY = os.getenv("AI_KEY")

# Упрощенная настройка клиента
client = AsyncOpenAI(
    api_key=AI_KEY,
    base_url="https://groq.com"
)

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    # Поиск любого фото в папке
    photo = next((f for f in os.listdir() if f.lower().endswith(('.jpg', '.png', '.jpeg'))), None)
    if photo:
        await message.answer_photo(photo=FSInputFile(photo), caption="Привет! я шутник-бот! веселись!")
    else:
        await message.answer("Привет! я шутник-бот! (фото не нашел)")

@dp.message(F.text)
async def chat(message: types.Message):
    try:
        # Пробуем другую модель, иногда 70b капризничает на бесплатных аккаунтах
        response = await client.chat.completions.create(
            model="llama3-8b-8192", 
            messages=[
                {"role": "system", "content": "Ты дерзкий комик. Отвечай коротко и смешно на русском."},
                {"role": "user", "content": message.text}
            ]
        )
        await message.reply(response.choices.message.content)
    except Exception as e:
        await message.reply(f"Все еще ошибка: {str(e)[:100]}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



