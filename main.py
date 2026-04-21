import asyncio
import os
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile

# Твой НОВЫЙ токен (уже вписан)
TG_TOKEN = "8725311183:AAG_Tpng3Xkny2kxaluNMf5P1ZAugtstZE0"

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

async def get_ai_answer(user_text):
    # Используем самый стабильный бесплатный канал
    url = f"https://pollinations.ai на русском языке как дерзкий, саркастичный и острый на язык комик. Используй молодежный сленг. Ответь коротко на фразу: {user_text}"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=20) as resp:
                if resp.status == 200:
                    answer = await resp.text()
                    return answer if answer else "Я так сильно смеялся, что забыл ответ. Еще раз?"
                return f"ИИ приуныл (код {resp.status})"
        except Exception:
            return "Сеть барахлит, но я прорвусь! Напиши еще раз."

@dp.message(Command("start"))
async def start(message: types.Message):
    # Ищем твою картинку (любую в папке)
    photo = next((f for f in os.listdir() if f.lower().endswith(('.jpg', '.png', '.jpeg'))), None)
    if photo:
        await message.answer_photo(photo=FSInputFile(photo), caption="Привет! я шутник-бот! веселись!")
    else:
        await message.answer("Привет! я шутник-бот! веселись!")

@dp.message(F.text)
async def chat(message: types.Message):
    # Получаем дерзкую шутку
    answer = await get_ai_answer(message.text)
    await message.reply(answer)

async def main():
    # Эта строка убивает все старые запросы, чтобы не было ошибок
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())















