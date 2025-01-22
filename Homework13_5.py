from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


ip = "XXX"
bot = Bot(token=ip)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
bt_1 = KeyboardButton(text = 'Рассчитать')
bt_2 = KeyboardButton(text = 'Информация')
kb. add(bt_1)
kb. add(bt_2)
#kb.row(bt_1, bt_2)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=["start"])
async def hi_message(message):
    print('Привет! Я бот помогающий твоему здоровью.')
    await message.answer('Привет! Я бот помогающий твоему здоровью.')

"""@dp.message_handler()
async def all_massages(message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer('Введите команду /start, чтобы начать общение.')"""

@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer(f'Введите свой возраст, пожалуйста')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(first = message.text)
    await message.answer('Введите свой рост, пожалуйста')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(second = message.text)
    await message.answer('Введите свой вес, пожалуйста')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(third = message.text)
    data = await state.get_data()
    calories = (int(10 * int(data['third']))) + (6.25 * int(data['second'])) - (5 * int(data['first']) - 161)
    await message.answer(f'Ваша норма {calories} калорий в день')
    await state.finish()

@dp.message_handler()
async def all_massages(message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer('Введите команду /start, чтобы начать общение.', reply_markup = kb)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)