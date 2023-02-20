from django.db import models


# Create your models here.
class TgUser(models.Model):
    telegram_id = models.IntegerField(verbose_name='Телеграмм id')
    user_name = models.CharField(max_length=150, verbose_name='Имя пользователя')
    user_phone_number = models.CharField(max_length=13, verbose_name='Номер телефона')

    def __str__(self):
        return self.user_phone_number

    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"

class Service(models.Model):
    service_name = models.CharField(max_length=75)
    service_added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.service_name

    class Meta:
        verbose_name = "Услуги"
        verbose_name_plural = "Услуги"

class TgOrders(models.Model):
    telegram_id = models.ForeignKey(TgUser, on_delete=models.CASCADE)
    user_service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.telegram_id)

    class Meta:
        verbose_name = "Заявки от пользователя"
        verbose_name_plural = "Заявки от пользователя"

