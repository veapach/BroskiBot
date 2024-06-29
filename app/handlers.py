import asyncio
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.must_parser as mp
import app.database.requests as rq

router = Router()

animation_texts = [
    '⏳ Еще выгружаем... ⏳',
    '⏳ Осталось чуть-чуть.... ⏳',
    '⏳ Совсем скоро.... ⏳',
    '⏳ Уже вот-вот.... ⏳',
    '⏳ Последние проверки.... ⏳'
]

class Register(StatesGroup):
    must_nickname = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
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
    await callback.message.edit_text('Начинаем регистрацию заново ❌', reply_markup=kb.start_registration)

@router.message(F.text == 'Профиль')
async def show_profile(message: Message):
    await rq.check_user(message.from_user.id)
    rating = await mp.must_rating()
    await message.answer(f'Ваш профиль:\nMust - https://mustapp.com/@{mp.must_nickname}/\nМесто в рейтинге - {rating}', reply_markup=kb.profile)

@router.message(F.text == 'Сериалы')
async def serials(message: Message):
    await rq.check_user(message.from_user.id)
    await message.answer('⏳ Выгружаем список <b>сериалов</b>, это может занять некоторое время ⏳', parse_mode="html")
    global serials_list
    serials_list = await mp.get_serials()
    serials_text = '\n'.join([f'➜ {name} - https://mustapp.com{url}' for name, url in serials_list])
    await message.answer(f'<b>Список запланированных сериалов:\n\n</b>{serials_text}', reply_markup=kb.serials_menu, parse_mode="html", disable_web_page_preview=True)

@router.message(F.text == 'Фильмы')
async def movies(message: Message):
    await rq.check_user(message.from_user.id)
    await message.answer('⏳ Выгружаем список <b>фильмов</b>, это может занять некоторое время ⏳', parse_mode="html")
    global movies_list
    movies_list = await mp.get_movies()
    movies_text = '\n'.join([f'➜ {name} - https://mustapp.com{url}' for name, url in movies_list])
    await message.answer(f'<b>Список запланированных фильмов:\n\n</b>{movies_text}', reply_markup=kb.movies_menu, parse_mode="html", disable_web_page_preview=True)

@router.callback_query(F.data == 'random_serial')
async def random_serial(callback: CallbackQuery):
    await rq.check_user(callback.from_user.id)
    serial, url = await mp.get_random_serial()
    await callback.message.edit_text(f'🎲 Выпал сериал - <b>{serial}</b>\n Ссылка - {url}', reply_markup=kb.random_serial_menu, parse_mode="html")

@router.callback_query(F.data == 'random_movie')
async def random_movie(callback: CallbackQuery):
    await rq.check_user(callback.from_user.id)
    movie, url = await mp.get_random_movie()
    await callback.message.edit_text(f'🎲 Выпал фильм - <b>{movie}</b>\n Ссылка - {url}', reply_markup=kb.random_movies_menu, parse_mode="html")

@router.callback_query(F.data == 'serials')
async def serials_menu(callback: CallbackQuery):
    await callback.answer('Назад к сериалам')
    serials_text = '\n'.join([f'➜ {name} - https://mustapp.com{url}' for name, url in serials_list])
    await callback.message.answer(f'<b>Список запланированных сериалов:\n\n</b>{serials_text}', reply_markup=kb.serials_menu, parse_mode="html", disable_web_page_preview=True)

@router.callback_query(F.data == 'movies')
async def movies_menu(callback: CallbackQuery):
    await callback.answer('Назад к фильмам')
    movies_text = '\n'.join([f'➜ {name} - https://mustapp.com{url}' for name, url in movies_list])
    await callback.message.answer(f'<b>Список запланированных фильмов:\n\n</b>{movies_text}', reply_markup=kb.movies_menu, parse_mode="html", disable_web_page_preview=True)