from django.core.management.base import BaseCommand

from admin_panel.main import dp
import aiogram


class Command(BaseCommand):
    help = 'Бот'

    def handle(self, *args, **options):
        # Запуск тг бота
        aiogram.executor.start_polling(dp)
