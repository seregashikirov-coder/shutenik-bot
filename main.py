import asyncio
import os
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile

# Твои данные (вставлены напрямую)
TG_TOKEN = "8444795988:AAG8rq4RlZKq55IE7m7x3PlY8X92W75Djuc"
AI_KEY = "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"

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

async def get_ai_answer(user_text):
    url = "https://openrouter.ai"
    headers = {
        "Authorization": f"Bearer {AI_KEY}",
        "HTTP-Referer": "https://railway.app",
        "X-Title": "JokeBot",
        "Content-Type": "application/json"
    }
    # Используем модель Zephyr — она самая безотказная среди бесплатных
    data = {
        "model": "huggingfaceh4/zephyr-7b-beta:free",
        "messages": [
            {"role": "system", "content": "Ты дерзкий комик. Отвечай очень коротко, саркастично и на русском языке."},
            {"role": "user", "content": user_text}
        ]
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, json=data, timeout=30) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    if 'choices' in result and len(result['choices']) > 0:
                        return result['choices'][0]['message']['content']
                    return "ИИ прислал пустоту. Попробуй еще раз."
                else:
                    return f"Ошибка ИИ (код {resp.status})"
        except Exception as e:
            return "Связь барахлит. Напиши мне еще раз!"

@dp.message(Command("start"))
async def start(message: types.Message):
    # Бот ищет любое фото в папке
    photo = next((f for f in os.listdir() if f.lower().endswith(('.jpg', '.png', '.jpeg'))), None)
    if photo:
        await message.answer_photo(photo=FSInputFile(photo), caption="Привет! я шутник-бот! веселись!")
    else:
        await message.answer("Привет! я шутник-бот! веселись!")

@dp.message(F.text)
async def chat(message: types.Message):
    # Получаем и отправляем ответ
    answer = await get_ai_answer(message.text)
    await message.reply(answer)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())










