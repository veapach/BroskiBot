from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, 
                           InlineKeyboardMarkup, InlineKeyboardButton)

main = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text='🎲 Рандомайзер')],
                                       [KeyboardButton(text='Профиль')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выбери что показать:')

start_registration = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Зарегистрироваться ✅', callback_data='start_registration')]])

confirm_registration = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Да ✅', callback_data='confirm_reg_yes')],
    [InlineKeyboardButton(text = 'Нет ❌', callback_data='confirm_reg_no')]],
                                            one_time_keyboard=True)

randomizer = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text= '🎲 Случайный сериал', callback_data='random_serial')],
    [InlineKeyboardButton(text= '🎲 Случайный фильм', callback_data='random_movie')]])

profile = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Перепривязать Must', callback_data='start_registration')]])  

randomizer_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Назад к рандомайзеру', callback_data='randomizer')]])