import asyncio
import os
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile

# Берем ключи из настроек Railway
TG_TOKEN = os.getenv("TG_TOKEN")
AI_KEY = os.getenv("AI_KEY")

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

async def get_ai_answer(user_text):
    # Прямой запрос к OpenRouter
    url = "https://openrouter.ai"
    headers = {
        "Authorization": f"Bearer {AI_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "google/gemma-2-9b-it:free", # Мощная бесплатная модель
        "messages": [
            {"role": "system", "content": "Ты дерзкий комик. Отвечай на сообщения короткими, нестандартными шутками на русском. Твой юмор — смесь сарказма и хайпа. Подколы обязательны."},
            {"role": "user", "content": user_text}
        ]
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, json=data) as resp:
                if resp.status == 200:
                    res = await resp.json()
                    return res['choices']['message']['content']
                else:
                    return f"Ошибка ИИ (код {resp.status})"
        except Exception as e:
            return f"Ошибка сети: {str(e)[:50]}"

@dp.message(Command("start"))
async def start(message: types.Message):
    # Твое название фото, которое мы видели на скриншоте
    photo_name = "IMG_20260419_225749_338.jpg" 
    
    if os.path.exists(photo_name):
        await message.answer_photo(
            photo=FSInputFile(photo_name), 
            caption="Привет! я шутник-бот! веселись!"
        )
    else:
        # Если вдруг фото не найдено, бот просто напишет текст
        await message.answer("Привет! я шутник-бот! веселись!")

@dp.message(F.text)
async def chat(message: types.Message):
    # Получаем дерзкую шутку от ИИ
    answer = await get_ai_answer(message.text)
    await message.reply(answer)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())





