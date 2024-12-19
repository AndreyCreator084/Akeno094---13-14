from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = "тут находится мой ключ, а вам не покажу xD"
bot = Bot(token = api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup()
button1 = KeyboardButton(text = 'Рассчитать', resize_keyboard = True)
button2 = KeyboardButton(text = 'Информация', resize_keyboard = True)
kb.add(button1)
kb.add(button2)

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.'
                         ' Для того чтобы узнать кол-во калорий, '
                         'нажми кнопку "Рассчитать".', reply_markup = kb)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State() # Добавил дополнительное состояние на определение пола человека

@dp.message_handler(text = 'Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def set_gender(message, state):           # Дополнинительная функция (не относится к ДЗ)
    await state.update_data(weight = message.text)
    await message.answer('Введите свой пол (мужской/женский):')
    await UserState.gender.set()

@dp.message_handler(state = UserState.gender)
async def send_calories(message, state):
    await state.update_data(gender = message.text)
    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    gender = data['gender']
    if gender.lower() == 'мужской':
        calories = (10 * weight) + (6.25 * growth) - (5 * age) + 5
    elif gender.lower() == 'женский':
        calories = (10 * weight) + (6.25 * growth) - (5 * age) - 161
    else:
        await message.answer('Некорректный ввод пола. Пожалуйста, введите "мужской" или "женский".')
        return
    await message.answer(f'Ваша норма калорий: {calories}')
    await state.finish()

@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)