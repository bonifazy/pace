from aiogram import types


digital_keyboard = types.InlineKeyboardMarkup(row_width=3)
digit_1 = types.InlineKeyboardButton(text='1', callback_data='digit_1')
digit_2 = types.InlineKeyboardButton(text='2', callback_data='digit_2')
digit_3 = types.InlineKeyboardButton(text='3', callback_data='digit_3')
digit_4 = types.InlineKeyboardButton(text='4', callback_data='digit_4')
digit_5 = types.InlineKeyboardButton(text='5', callback_data='digit_5')
digit_6 = types.InlineKeyboardButton(text='6', callback_data='digit_6')
digit_7 = types.InlineKeyboardButton(text='7', callback_data='digit_7')
digit_8 = types.InlineKeyboardButton(text='8', callback_data='digit_8')
digit_9 = types.InlineKeyboardButton(text='9', callback_data='digit_9')
digit_0 = types.InlineKeyboardButton(text='0', callback_data='digit_0')
digit_dummy = types.InlineKeyboardButton(text=' ', callback_data='digit_dummy_')
digital_keyboard.row(digit_1, digit_2, digit_3)
digital_keyboard.row(digit_4, digit_5, digit_6)
digital_keyboard.row(digit_7, digit_8, digit_9)
digital_keyboard.row(digit_dummy, digit_0, digit_dummy)

next_step_keyboard = types.InlineKeyboardMarkup()
next_interval = types.InlineKeyboardButton(text='/interval', callback_data='menu_interval')
next_tempo = types.InlineKeyboardButton(text='/tempo', callback_data='menu_tempo')
next_long = types.InlineKeyboardButton(text='/long', callback_data='menu_long')
next_competiotions = types.InlineKeyboardButton(text='/competitions', callback_data='menu_competitions')
next_distance = types.InlineKeyboardButton(text='/distance', callback_data='menu_distance')
next_step_keyboard.row(next_interval, next_tempo, next_long)
next_step_keyboard.row(next_competiotions, next_distance)

competitions_keyboard = types.InlineKeyboardMarkup()
competitions_3km = types.InlineKeyboardButton(text='3000 м.', callback_data='competitions_3km')
competitions_5km = types.InlineKeyboardButton(text='5000 м.', callback_data='competitions_5km')
competitions_10km = types.InlineKeyboardButton(text='10 км.', callback_data='competitions_10km')
competitions_21km = types.InlineKeyboardButton(text='21.1 км.', callback_data='competitions_21km')
competitions_42km = types.InlineKeyboardButton(text='42.2 км.', callback_data='competitions_42km')
competitions_keyboard.row(competitions_3km, competitions_5km)
competitions_keyboard.row(competitions_10km, competitions_21km, competitions_42km)

distance_training_keyboard = types.InlineKeyboardMarkup(row_width=4)
distance_training_400m = types.InlineKeyboardButton(text='400 м.', callback_data='distance_training_400m')
distance_training_500m = types.InlineKeyboardButton(text='500 м.', callback_data='distance_training_0500m')
distance_training_600m = types.InlineKeyboardButton(text='600 м.', callback_data='distance_training_0600m')
distance_training_800m = types.InlineKeyboardButton(text='800 м.', callback_data='distance_training_800m')
distance_training_1000m = types.InlineKeyboardButton(text='1000 м.', callback_data='distance_training_1000m')
distance_training_1200m = types.InlineKeyboardButton(text='1200 м.', callback_data='distance_training_1200m')
distance_training_1500m = types.InlineKeyboardButton(text='1500 м.', callback_data='distance_training_1500m')
distance_training_1600m = types.InlineKeyboardButton(text='1600 м.', callback_data='distance_training_1600m')
distance_training_2km = types.InlineKeyboardButton(text='2 км.', callback_data='distance_training_2km')
distance_training_3km = types.InlineKeyboardButton(text='3 км.', callback_data='distance_training_3km')
distance_training_4km = types.InlineKeyboardButton(text='4 км.', callback_data='distance_training_4km')
distance_training_5km = types.InlineKeyboardButton(text='5 км.', callback_data='distance_training_5km')
distance_training_keyboard.row(distance_training_400m, distance_training_500m, distance_training_600m,
                               distance_training_800m)
distance_training_keyboard.row(distance_training_1000m, distance_training_1200m, distance_training_1500m,
                               distance_training_1600m)
distance_training_keyboard.row(distance_training_2km, distance_training_3km, distance_training_4km,
                               distance_training_5km)

# кнопки для новостной рассылки администратором
first_news_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
first_news_keyboard.row('Редактировать', 'Дальше')
first_news_keyboard.row('Отменить')

second_news_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
second_news_keyboard.row('Редактировать', 'Отменить')
second_news_keyboard.row('Тестовая рассылка')
second_news_keyboard.row('Опубликовать всем')

