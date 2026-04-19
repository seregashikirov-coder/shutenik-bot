import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile
from openai import AsyncOpenAI

# Ключи берем из переменных Railway
TG_TOKEN = os.getenv("TG_TOKEN")
AI_KEY = os.getenv("AI_KEY")

client = AsyncOpenAI(
    api_key=AI_KEY,
    base_url="https://groq.com"
)

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

PROMPT = "Ты дерзкий комик. Отвечай короткими, саркастичными шутками на русском языке. Используй сленг и подколы."

@dp.message(Command("start"))
async def start(message: types.Message):
    # Заменил название на твое из сообщения
    photo_name = "IMG_20260419_225749_338.jpg" 
    
    if os.path.exists(photo_name):
        await message.answer_photo(
            photo=FSInputFile(photo_name), 
            caption="Привет! я шутник-бот! веселись!"
        )
    else:
        await message.answer("Привет! я шутник-бот! (фото под именем IMG_... не найдено в папке)")

@dp.message(F.text)
async def chat(message: types.Message):
    try:
        response = await client.chat.completions.create(
            model="llama3-8b-8192", 
            messages=[{"role": "system", "content": PROMPT}, {"role": "user", "content": message.text}]
        )
        await message.reply(response.choices.message.content)
    except Exception as e:
        await message.reply(f"Ошибка ИИ: {str(e)[:100]}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

