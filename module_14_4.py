from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import get_all_products

products = get_all_products()


api = "7912537365:AAFVuKQlhFGeWz-9ioWESsvgzO5Efb2JsVo"
bot = Bot(token = api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(
    keyboard=[
        [
                KeyboardButton(text='Рассчитать'),
                KeyboardButton(text='Информация'),
                KeyboardButton(text='Купить')
        ]
    ], resize_keyboard=True
)


Ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')],
        [InlineKeyboardButton(text='Формулы расчета', callback_data='formulas')],
    ]
)


catalog_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Продукт 1', callback_data='product_buying')],
        [InlineKeyboardButton(text='Продукт 2', callback_data='product_buying')],
        [InlineKeyboardButton(text='Продукт 3', callback_data='product_buying')],
        [InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')]
    ]
)

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.'
                         ' Для того чтобы узнать кол-во калорий, '
                         'нажми кнопку "Рассчитать".', reply_markup = kb)

@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup = Ikb)

@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer('Мужчины: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5\n'
                         ' Женщины: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161 ')

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State() # Добавил дополнительное состояние на определение пола человека

@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
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

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for product in products:
        product_name = product[1]
        product_description = product[2]
        product_price = product[3]
        product_info = f'Название: {product_name} | Описание: {product_description} | Цена: {product_price}'
        with open('photo/{}.png'.format(product[0]), 'rb') as img:
            await message.answer_photo(img, product_info, reply_markup=kb)
    await message.answer('Выберите продукт для покупки:', reply_markup=catalog_kb)

@dp.callback_query_handler(text= 'product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)