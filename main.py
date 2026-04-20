import asyncio
import os
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile

# Твои ключи (вставлены напрямую для надежности)
TG_TOKEN = "8444795988:AAG8rq4RlZKq55IE7m7x3PlY8X92W75Djuc"
AI_KEY = "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"

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

async def get_ai_answer(user_text):
    url = "https://openrouter.ai"
    headers = {
        "Authorization": f"Bearer {AI_KEY}",
        "HTTP-Referer": "https://github.com", # Обязательно для OpenRouter
        "X-Title": "Joke Bot",
        "Content-Type": "application/json"
    }
    # Используем Mistral 7B — она самая стабильная на бесплатном тарифе
    data = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {"role": "system", "content": "Ты дерзкий комик. Отвечай коротко и саркастично на русском."},
            {"role": "user", "content": user_text}
        ]
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, json=data) as resp:
                if resp.status == 200:
                    try:
                        res = await resp.json()
                        if 'choices' in res and len(res['choices']) > 0:
                            return res['choices']['message']['content']
                        return "ИИ промолчал. Попробуй еще раз!"
                    except:
                        return "Ошибка в данных от ИИ. Попробуй позже."
                else:
                    return f"ИИ занят (код {resp.status})"
        except Exception as e:
            return f"Проблема с сетью: {str(e)[:30]}"

@dp.message(Command("start"))
async def start(message: types.Message):
    # Ищем фото в папке (любое)
    photo = next((f for f in os.listdir() if f.lower().endswith(('.jpg', '.png', '.jpeg'))), None)
    if photo:
        await message.answer_photo(photo=FSInputFile(photo), caption="Привет! я шутник-бот! веселись!")
    else:
        await message.answer("Привет! я шутник-бот! веселись!")

@dp.message(F.text)
async def chat(message: types.Message):
    answer = await get_ai_answer(message.text)
    await message.reply(answer)

async def main():
    # Очищаем очередь сообщений, чтобы не было ошибок
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())








