import asyncio
import os
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile

# Твой новый токен (вписан напрямую для надежности)
TG_TOKEN = "8444795988:AAG8rq4RlZKq55IE7m7x3PlY8X92W75Djuc"

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

async def get_ai_answer(user_text):
    # Прямой запрос к бесплатному ИИ-шлюзу (без ключей!)
    url = f"https://pollinations.ai на русском как дерзкий и саркастичный комик на фразу: {user_text}"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=20) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    return text if text else "Я так сильно смеялся, что забыл ответ. Спроси еще раз!"
                return f"ИИ взял перекур (код {resp.status})"
        except Exception:
            return "Сеть всё еще барахлит. Но я попробую пробиться через 5 секунд, напиши еще раз!"

@dp.message(Command("start"))
async def start(message: types.Message):
    # Ищем любое фото в папке
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
    # Очищаем старые сообщения
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())














