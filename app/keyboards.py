from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, 
                           InlineKeyboardMarkup, InlineKeyboardButton)

main = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text='Сериалы')],
                                       [KeyboardButton(text='Фильмы')],
                                       [KeyboardButton(text='Профиль')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выбери что показать:')

start_registration = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Зарегистрироваться ✅', callback_data='start_registration')]])

confirm_registration = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Да ✅', callback_data='confirm_reg_yes')],
    [InlineKeyboardButton(text = 'Нет ❌', callback_data='confirm_reg_no')]],
                                            one_time_keyboard=True)

profile = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Перепривязать Must', callback_data='start_registration')]])  

serials_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = '🎲 Случайный запланированный сериал', callback_data='random_serial')]])

movies_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = '🎲 Случайный запланированный фильм', callback_data='random_movie')]])

random_serial_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Назад к сериалам', callback_data='serials')]])

random_movies_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Назад к фильмам', callback_data='movies')]])