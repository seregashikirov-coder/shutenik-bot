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
    url = "https://openrouter.ai"
    headers = {
        "Authorization": f"Bearer {AI_KEY}",
        "Content-Type": "application/json"
    }
    # Используем Mistral — она стабильнее всего на OpenRouter
    data = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {"role": "system", "content": "Ты дерзкий комик. Отвечай на русском языке короткими саркастичными шутками. Подколы обязательны."},
            {"role": "user", "content": user_text}
        ]
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, json=data) as resp:
                if resp.status == 200:
                    res = await resp.json()
                    if 'choices' in res and len(res['choices']) > 0:
                        return res['choices'][0]['message']['content']
                    return "ИИ прислал пустой ответ, спроси еще раз."
                else:
                    return f"ИИ приуныл (код {resp.status})"
        except Exception:
            return "Что-то с сетью, я не смог придумать шутку."

@dp.message(Command("start"))
async def start(message: types.Message):
    # Твое название фото из репозитория
    photo_name = "IMG_20260419_225749_338.jpg" 
    
    if os.path.exists(photo_name):
        await message.answer_photo(
            photo=FSInputFile(photo_name), 
            caption="Привет! я шутник-бот! веселись!"
        )
    else:
        await message.answer("Привет! я шутник-бот! веселись!")

@dp.message(F.text)
async def chat(message: types.Message):
    # Получаем ответ от ИИ
    answer = await get_ai_answer(message.text)
    await message.reply(answer)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())






