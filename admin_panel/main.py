from aiogram import Bot, Dispatcher

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from . import buttons
from . import models

### Для работы с ботом ###
import os

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


#########################


##### Этапы бота ######
class Registration(StatesGroup):
    getting_name = State()
    getting_number = State()
    getting_service = State()
    getting_meet_format = State()


################

# Bot() - подключиться к тг боту
# Dispatcher() - Создает обработчик входящих данных в наш бот
# executor - Запускает бот


bot = Bot(token='6145391722:AAF2bmKREP6KMxADzL0mtgyla1QlaPYpldw')
dp = Dispatcher(bot=bot, storage=MemoryStorage())


# Обработчик команды /start
@dp.message_handler(commands=['start'], state='*')
async def start_message(message):
    checker = models.TgUser.objects.filter(telegram_id=message.from_user.id).exists()

    if not checker:  # Если нет пользователя в базе
        # Ответ
        await message.answer('Привет, отправь свое имя')

        # Переход на этап получения имени
        await Registration.getting_name.set()

    else:  # Если есть пользователь
        await message.answer('Какую услугу хотите заказать?', reply_markup=buttons.send_service_button())

        # Переход на этап получения услуги
        await Registration.getting_service.set()


# Этап получения имени пользователя
@dp.message_handler(content_types=['text'], state=Registration.getting_name)
async def text_messages(message, state: Registration.getting_name):
    name = message.text

    # Сохраняем данные
    await state.update_data(username=name)

    # Ответ
    await message.answer('Теперь отправь свой номер', reply_markup=buttons.number_button())

    # Переход на этап получения номера телефона
    await Registration.getting_number.set()


# Этап получения номера телефона пользователя
@dp.message_handler(content_types=['text', 'contact'], state=Registration.getting_number)
async def get_user_number(message, state: Registration.getting_number):
    phone_number = message.text or message.contact.phone_number

    # Сохраняем данные
    await state.update_data(phone_number=phone_number)

    # Ответ
    await message.answer('Теперь выбери услугу', reply_markup=buttons.send_service_button())

    # Переход на этап выбора услуги
    await Registration.getting_service.set()


# Этап получения услуги и оформления заказа
@dp.message_handler(content_types=['text'], state=Registration.getting_service)
async def get_user_service(message, state: Registration.getting_service):
    user_service = message.text
    all_services = [i.service_name for i in models.Service.objects.all()]

    if user_service in all_services:
        checker = models.TgUser.objects.filter(telegram_id=message.from_user.id).exists()
        service_from_db = models.Service.objects.get(service_name=user_service)

        # Ответ
        await message.answer('Заявка успешно создана, ожидайте ответа оператора')

        # Получаем все введенные раннее данные
        get_all_data = await state.get_data()

        if not checker:
            user_name = get_all_data['username']
            user_number = get_all_data['phone_number']

            user = models.TgUser(telegram_id=message.from_user.id,
                                 user_name=user_name,
                                 user_phone_number=user_number).save()

            models.TgOrders(telegram_id=user, user_service=service_from_db).save()

        else:
            user = models.TgUser.objects.get(telegram_id=message.from_user.id)
            models.TgOrders(telegram_id=user, user_service=service_from_db).save()

        # Отправка заявки админу
        await bot.send_message(311527050, 'Новый заказ')

        await state.finish()

    else:
        await message.answer('Ошибка в данных\nОтправьте команду /start')

        await state.finish()
# Запуск
