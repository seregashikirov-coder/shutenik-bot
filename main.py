import asyncio
import os
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile

# Берем ключи из настроек Railway
# Убедись, что в Railway в Variables ты обновил TG_TOKEN на новый!
TG_TOKEN = os.getenv("TG_TOKEN")
AI_KEY = os.getenv("AI_KEY")

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

async def get_ai_answer(user_text):
    url = "https://openrouter.ai"
    headers = {
        "Authorization": f"Bearer {AI_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://railway.app", # Нужно для OpenRouter
    }
    # Используем Mistral — она самая стабильная среди бесплатных
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
                        return res['choices']['message']['content']
                    return "ИИ прислал пустой ответ, попробуй еще раз."
                else:
                    status_text = await resp.text()
                    return f"ИИ приуныл (ошибка {resp.status})"
        except Exception as e:
            return f"Ошибка связи: {str(e)[:40]}"

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
        # Если фото не найдено, бот просто пришлет текст
        await message.answer("Привет! я шутник-бот! веселись!")

@dp.message(F.text)
async def chat(message: types.Message):
    # Сначала бот может отправить уведомление, что он думает (по желанию)
    answer = await get_ai_answer(message.text)
    await message.reply(answer)

async def main():
    # Удаляем вебхуки, чтобы не было конфликтов (важно!)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())







