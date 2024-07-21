import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN, OPENWEATHER_API_KEY  # Не забудьте добавить ваш OpenWeather API ключ в config.py

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять комманды: \n /start \n /help \n /weather ')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет!')

@dp.message(Command('weather'))
async def weather(message: Message):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://api.openweathermap.org/data/2.5/weather?q=Moscow&appid={OPENWEATHER_API_KEY}&units=metric') as response:
            data = await response.json()
            if response.status == 200:
                temp = data['main']['temp']
                await message.answer(f'Сейчас в Москве {temp}°C')
            else:
                await message.answer('Не удалось получить данные о погоде. Попробуйте позже.')


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())