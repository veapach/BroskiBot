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
    '⏳ Выгружаем список запланированного, это может занять некоторое время ⏳',
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
    
@router.message(Command('menu'))
async def cmd_menu(message: Message):
    await message.answer('Главное меню', reply_markup=kb.main)

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

@router.message(F.text == '🎲 Рандомайзер')
async def randomizer(message: Message):
    await rq.check_user(message.from_user.id)
    waiting_msg = await message.answer('⏳ Выгружаем список <b>запланированного</b>, это может занять некоторое время ⏳', parse_mode="html")
    
    task = asyncio.create_task(mp.get_list())
    
    while not task.done():
        for text in animation_texts:
            await waiting_msg.edit_text(text, parse_mode="html")
            await asyncio.sleep(1.5)  
            if task.done():
                break

    
    await task
    await waiting_msg.edit_text('Список запланированного подгружен!\nВыберите что вам показать:', reply_markup=kb.randomizer)
    
@router.callback_query(F.data == 'randomizer')
async def randomizer(callback: CallbackQuery):
    await callback.answer('Назад к рандомайзеру')
    await rq.check_user(callback.from_user.id)
    await callback.message.edit_text('Выберите что вам показать:', reply_markup=kb.randomizer)

@router.callback_query(F.data == 'random_serial')
async def random_serial(callback: CallbackQuery):
    await rq.check_user(callback.from_user.id)
    serial, url = await mp.get_random_serial()
    await callback.message.edit_text(f'🎲 Выпал сериал - <b>{serial}</b>\n Ссылка - {url}', reply_markup=kb.randomizer_menu, parse_mode="html")

@router.callback_query(F.data == 'random_movie')
async def random_movie(callback: CallbackQuery):
    await rq.check_user(callback.from_user.id)
    movie, url = await mp.get_random_movie()
    await callback.message.edit_text(f'🎲 Выпал фильм - <b>{movie}</b>\n Ссылка - {url}', reply_markup=kb.randomizer_menu, parse_mode="html")