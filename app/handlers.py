import asyncio
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from concurrent.futures import ThreadPoolExecutor

import app.keyboards as kb
import app.must_parser as mp
import app.database.requests as rq

router = Router()
random_chosed = False

executor = ThreadPoolExecutor()

animation_texts = [
        '⏳ Еще выбираем... ⏳',
        '⏳ Осталось чуть-чуть.... ⏳',
        '⏳ Совсем скоро.... ⏳',
        '⏳ Уже вот-вот.... ⏳',
        '⏳ Последние проверки.... ⏳'
    ]

class Register(StatesGroup):
    must_nickname = State()


@router.message(CommandStart())
async def cmd_start(message:Message):
    await message.answer('Привет, броски! Для начала зарегистрируйся', reply_markup=kb.start_registration)
    
@router.callback_query(F.data == 'start_registration')
async def start_registration(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Начинаем регистрацию')
    await state.set_state(Register.must_nickname)
    await callback.message.edit_text('Отправь свой @ник в Must, только без "@", а просто текстом :)')
    
@router.message(Register.must_nickname)
async def registration_must(message: Message, state: FSMContext):
    await state.update_data(must_nickname=message.text)
    data = await state.get_data()
    await message.answer(f'Это ваш профиль?\n https://mustapp.com/@{data["must_nickname"]}', reply_markup=kb.confirm_registration)

@router.callback_query(F.data == 'confirm_reg_yes')
async def confirm_reg(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await rq.set_user(callback.from_user.id, data['must_nickname'])
    await state.clear()
    await callback.answer('Регистрация завершена')
    await callback.message.answer('Регистрация успешно завершена 🎉', reply_markup=kb.main)

@router.callback_query(F.data == 'confirm_reg_no')
async def confirm_reg_no(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('Начинаем регистрацию заново')
    await callback.message.edit_text(f'Начинаем регистрацию заново ❌', reply_markup=kb.start_registration)

@router.callback_query(F.data == 'backToMainMenu')
async def backToMainMeny(callback: CallbackQuery):
    await callback.answer('Возврат в главное меню')
    await callback.message.edit_text('Главное меню', reply_markup=kb.main)
    
    
@router.message(F.text == 'Профиль')
async def show_profile(message: Message):
    await rq.check_user(message.from_user.id)
    mp.must_rating()
    await message.answer(f'Ваш профиль:\nMust - https://mustapp.com/@{mp.must_nickname}/\nМесто в рейтинге - {mp.rating}', reply_markup=kb.profile)

@router.message(F.text == 'броски')
async def nice(message: Message):
    await message.answer('я броски ;)')
    
@router.message(F.text == 'Сериалы')
async def serials(message: Message):
    await rq.check_user(message.from_user.id)
    await message.answer('Тут будет список сериалов', reply_markup=kb.serials_menu)

@router.message(F.text == 'Фильмы')
async def movies(message: Message):
    await rq.check_user(message.from_user.id)
    await message.answer('Тут будет список фильмов', reply_markup=kb.movies_menu)
 
@router.callback_query(F.data == 'serials')
async def randomSerial(callback: CallbackQuery):
    await callback.answer('Назад к сериалам')
    await callback.message.edit_text('Тут будет список сериалов', reply_markup=kb.serials_menu)

@router.callback_query(F.data == 'movies')
async def randomSerial(callback: CallbackQuery):
    await callback.answer('Назад к сериалам')
    await callback.message.edit_text('Тут будет список сериалов', reply_markup=kb.movies_menu)

    
@router.callback_query(F.data == 'random_serial')
async def randomSerial(callback: CallbackQuery):
    await callback.answer('Выбор случайного сериала')
    await rq.check_user(callback.from_user.id)  
    waiting_msg = await callback.message.edit_text('⏳ Выбираем <b>сериал</b>, это может занять некоторое время ⏳', parse_mode="html")
    
    loop = asyncio.get_event_loop()
    task = loop.run_in_executor(executor, mp.random_project)
    
    while not task.done():
        for text in animation_texts:
            await asyncio.sleep(2)
            await waiting_msg.edit_text(text, parse_mode='html')         
            if task.done():
                break
    
    await task
    await callback.message.edit_text(f'🎲 Выпал сериал - <b>{mp.chosen_serial}</b>\n Ссылка - {mp.chosen_serial_url}',
                        reply_markup=kb.random_serial_menu, parse_mode="html")

@router.callback_query(F.data == 'random_movie')
async def randomMovie(callback: CallbackQuery):
    await callback.answer('Выбор случайного фильма')
    await rq.check_user(callback.from_user.id)
    waiting_msg = await callback.message.edit_text(f'⏳ Выбираем <b>фильм</b>, это может занять некоторое время ⏳', parse_mode="html")
    
    loop = asyncio.get_event_loop()
    task = loop.run_in_executor(executor, mp.random_project)
    
    while not task.done():
        for text in animation_texts:
            await asyncio.sleep(2)
            await waiting_msg.edit_text(text, parse_mode='html')
            if task.done():
                break
    
    await task
    await callback.message.edit_text(f'🎲 Выпал фильм - <b>{mp.chosen_movie}</b>\n Ссылка - {mp.chosen_movie_url}',
                        reply_markup=kb.random_movies_menu, parse_mode="html")
    
    
    
