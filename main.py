import asyncio
import os
import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile

# Твой токен (вписан напрямую)
TG_TOKEN = "8444795988:AAG8rq4RlZKq55IE7m7x3PlY8X92W75Djuc"

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()

async def get_ai_answer(user_text):
    # Используем бесплатный сервис без ключей
    url = "https://pollinations.ai"
    system_prompt = "Ты дерзкий комик. Отвечай коротко и саркастично на русском."
    full_prompt = f"{system_prompt}\nПользователь: {user_text}"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{url}{full_prompt}") as resp:
                if resp.status == 200:
                    return await resp.text()
                return "ИИ взял перерыв. Попробуй еще раз!"
        except:
            return "Проблема со связью, но я не сдаюсь!"

@dp.message(Command("start"))
async def start(message: types.Message):
    # Ищем любую картинку в папке
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
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())












