from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ip = "XXX"
bot = Bot(token=ip)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
bt_1 = KeyboardButton(text = 'Рассчитать')
bt_2 = KeyboardButton(text = 'Информация')
bt_3 = KeyboardButton(text = 'start')
kb. add(bt_1)
kb. add(bt_2)
kb. add(bt_3)
#kb.row(bt_1, bt_2)

kb2 = InlineKeyboardMarkup()
bt1 = InlineKeyboardButton(text = 'Рассчитать норму калорий', callback_data='calories')
bt2 = InlineKeyboardButton(text = 'Формулы расчёта', callback_data='formulas')
kb2.row(bt1, bt2)
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=["start"])
async def hi_message(message):
    print('Привет! Я бот помогающий твоему здоровью.')
    await message.answer('Привет! Я бот помогающий твоему здоровью.')

@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup = kb2)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Формула рассчета калорий: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer(f'Введите свой возраст, пожалуйста')
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
    await message.answer(f'Ваша дневная норма {calories} калорий')
    await state.finish()

@dp.message_handler()
async def all_massages(message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer('Введите команду /start, чтобы начать общение.', reply_markup = kb2)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)