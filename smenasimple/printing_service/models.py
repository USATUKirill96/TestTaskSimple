import json

from django.db import models
from django.contrib.postgres.fields import JSONField
from pydantic import BaseModel, Json

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


# Pydantic models used to parse and validate data

class CheckData(BaseModel):
    id: int
    price: int
    items: Json
    address: str
    client: Json
    point_id: int

    @staticmethod
    def parse_request(request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        check_data_raw = {
            'id': body['id'],
            'price': body['price'],
            'items': json.dumps(body['items']),
            'address': body['address'],
            'client': json.dumps(body['client']),
            'point_id': body['point_id'],
        }
        return CheckData(**check_data_raw)


class NewChecksData(BaseModel):
    api_key: int

    @staticmethod
    def parse_request(request):
        api_key = request.GET.get('api_key')
        return NewChecksData(api_key=api_key)


class CheckToPrintData(BaseModel):
    api_key: int
    check_id: int

    @staticmethod
    def parse_request(request):
        data = {
            'api_key': request.GET.get('api_key'),
            'check_id': request.GET.get('check_id')
        }
        return CheckToPrintData(**data)
