from django.db import models
from django.contrib.postgres.fields import JSONField

CHECK_TYPES = (("kitchen", "Kitchen"), ("client", "Client"))


class Printer(models.Model):
    name = models.CharField(max_length=250, verbose_name="Название принтера")
    api_key = models.CharField(unique=True, max_length=50, verbose_name="Ключ доступа к API")
    check_type = models.CharField(max_length=7, choices=CHECK_TYPES, verbose_name="Тип чека, который печатает принтер")
    point_id = models.IntegerField(verbose_name="Точка, к которой привязан принтер")

    def __str__(self):
        return str(self.api_key)

    class Meta:
        verbose_name = "Принтер"
        verbose_name_plural = "Принтеры"


class Check(models.Model):
    CHECK_STATES = (("new", "New"), ("render", "Render"), ("printed", "Printed"))
    printer_id = models.ForeignKey(Printer, on_delete=models.CASCADE, related_name='checks', verbose_name="ID принтера")
    self_type = models.CharField(max_length=7, choices=CHECK_TYPES, verbose_name="Тип чека")
    order = JSONField(verbose_name="Информация о заказе")
    status = models.CharField(max_length=7, choices=CHECK_STATES, verbose_name="Статус чека")
    pdf_file = models.FileField(upload_to='pdf', blank=True, verbose_name="Ссылка на созданный PDF-файл")

    def __str__(self):
        return f"Чек номер {self.pk}, печатается на {self.printer_id}"

    class Meta:
        verbose_name = "Чек"
        verbose_name_plural = "Чеки"
