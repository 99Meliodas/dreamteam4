import inspect
from requests import get
from bs4 import BeautifulSoup
from pprint import pprint
from time import sleep
from requests import get
from pprint import pprint
from datetime import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


bot_token = 'token'

bot = Bot(bot_token)
dp = Dispatcher(bot)

def get_data(url):
    r = get(url).content
    soup = BeautifulSoup(r, 'html.parser')
    items = soup.findAll('div', class_='pull-right rel')
    return items
def get_parse(items):
    result = []
    info = []
    info_proc = []
    info_ram = []
    info_ssd = []
    ssd_info = []
    k = 0
    for item in items:
        proc = []
        info_proc.append(item.find('div', class_='product_text pull-left').get_text().replace('\n', '').replace(';',
                                                                                                                ' ').strip().split(
            ' '))
        all_info = item.find('div', class_='product_text pull-left').get_text().replace('\n', ' ').strip().replace(';',
                                                                                                                   ' ').split(
            ' ')
        for i in range(len(all_info)):
            if 'SSD' in all_info or 'SSD:' in all_info:
                if all_info[i] == 'SSD':
                    ssd_info.append(all_info[i - 1].replace('GB', ''))
                elif all_info[i] == 'SSD:':
                    ssd_info.append(all_info[i + 1])
            elif 'SSD' not in all_info and 'SSD:' not in all_info:
                ssd_info.append('0')
        for i in info_proc:
            for j in range(len(i)):
                if 'Процессор' in i[j]:
                    proc.append(f'{i[j + 1]} {i[j + 2]} {i[j + 3]}')
                elif 'процессор' in i[j]:
                    proc.append(f'{i[j + 1]} {i[j + 2]} {i[j + 3]}')
        info.append(item.find('div', class_='product_text pull-left').get_text().replace('\n', '').strip().split(' '))
        size = []
        matrix = []
        a = item.find('div', class_='listbox_price text-center')
        for i in info:
            for j in range(len(i)):
                if 'экрана:' not in i and 'экран' not in i:
                    size.append('Отсутствует информация')
                    matrix.append('Отсутствует информация')
                elif i[j] == 'экрана:':
                    size.append(f'{i[j + 1]} {i[j + 2]} {i[j + 3][0:2]}')
                    matrix.append('Отсутствует информация')
                elif i[j] == 'экран':
                    size.append(f'{i[j + 1]} {i[j + 2]} {i[j + 3]}')
                    matrix.append(f'{i[j + 2]}')
        ram = []
        info_ram.append(
            item.find('div', class_='product_text pull-left').get_text().replace('\n', '').strip().split(' '))
        for i in info_ram:
            for j in range(len(i)):
                if 'памяти:' not in i and 'память' not in i:
                    ram.append('Отсутствует информация')
                if i[j] == 'памяти:':
                    if i[j + 3][0:3] == 'нак':
                        ram.append(f'{i[j + 1]}')
                    else:
                        ram.append(f'{i[j + 1]}')
                elif i[j] == 'память':
                    if i[j + 3][0:3] == 'нак':
                        ram.append(f'{i[j + 1][0]}')
                    else:
                        ram.append(f'{i[j + 1][0]}')
        info_ssd.append(
            item.find('div', class_='product_text pull-left').get_text().replace('\n', '').strip().split(' '))
        result.append({
            'Производитель': item.find('div', class_='product_text pull-left').get_text().replace('\n', '').strip().split(' ')[1],
            'Размер экрана': size[k],
            'Тип матрицы': matrix[k],
            'Цена': a.find('strong').get_text().replace('\n', '').split()[0],
            'Процессор': proc[k],
            'ОЗУ': ram[k],
            'SSD': ssd_info[k]
        })
        k += 1
    return result


@dp.message_handler(commands=['start'])
async def starter(message: types.Message):
    btn1 = InlineKeyboardButton("Цена", callback_data='Цена')
    btn2 = InlineKeyboardButton("Озу", callback_data='ОЗУ')
    btn3 = InlineKeyboardButton("Процессор", callback_data='Процессор')
    btn4 = InlineKeyboardButton("SSd", callback_data='Ssd')
    btn5 = InlineKeyboardButton("Производитель", callback_data='Производитель')
    btn6 = InlineKeyboardButton("Тип матрицы", callback_data='Тип матрицы')
    btn7 = InlineKeyboardButton("Разрешение экрана", callback_data='Разрешение экрана')
    inline_kb_full = InlineKeyboardMarkup(row_width=4).add(btn1, btn2,
                                                           btn3, btn4,
                                                           btn5, btn6,
                                                           btn7)
    await message.reply('''Я парсер страницы kivano.kg
    По чему будем искать 
    (Цена/объем оперативной памяти/
    процессор/объем SSD/
    производитель (Apple, Xiaomi, HP и т.д.)
    тип матрицы/размер экрана''', reply_markup=inline_kb_full)

@dp.callback_query_handler()
async def reply(callback_query: types.CallbackQuery):
    global code
    code = callback_query.data
    if code == 'Цена':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Укажите цену')
    if code == 'ОЗУ':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Укажите ОЗУ')
    if code == 'Процессор':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Укажите процессор')
    if code == 'Ssd':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Укажите ssd')
    if code == 'Производитель':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Укажите производителя')
    if code == 'Тип матрицы':
        await bot.send_message(chat_id=callback_query.from_user.id, text='Укажите тип матрицы')
    if code == 'Разрешение экрана':
        await bot.send_message(chat_id=callback_query.from_user.id, text='укажите разрешение экрана')

@dp.message_handler()
async def get_user_message(message: types.Message):
    code1 = code
    for i in range(1,5):
        url = 'https://www.kivano.kg/noutbuki?page='+ str(i)
        items = get_data(url)
        result = get_parse(items)
        for j in range(len(result)):
            if code1 == 'Цена':
                if str(result[j]['Цена']) == str(message.text):
                    await message.reply(str(result[j]))
            if code1 == 'ОЗУ':
                if str(result[j]['ОЗУ']) == str(message.text):
                    await message.reply(str(result[j]))
            if code1 == 'Процессор':
                if str(result[j]['Процессор']) == str(message.text):
                    await message.reply(str(result[j]))
            if code1 == 'Ssd':
                if str(result[j]['SSD']) == str(message.text):
                    await message.reply(str(result[j]))
            if code1 == 'Производитель':
                if str(result[j]['Производитель']) == str(message.text):
                    await message.reply(str(result[j]))
            if code1 == 'Тип матрицы':
                if str(result[j]['Тип матрицы']) == str(message.text):
                    await message.reply(str(result[j]))
            if code1 == 'Разрешение экрана':
                if str(result[j]['Размер экрана']) == str(message.text):
                    await message.reply(str(result[j]))

executor.start_polling(dp)
