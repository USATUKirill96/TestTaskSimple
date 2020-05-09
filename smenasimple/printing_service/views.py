import json

from django.http import JsonResponse, HttpResponse
from django.views import View
from django.db.models import Q
from wsgiref.util import FileWrapper

from .models import Check, Printer
from .tasks import create_pdf


class CreateChecks(View):

    def post(self, request):
        # Parse data from request body
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        check_data = {
            'id': int(body['id']),
            'price': int(body['price']),
            'items': body['items'],
            'address': body['address'],
            'client': body['client'],
            'point_id': int(body['point_id']),
        }

        data_errors = self.get_errors(check_data)
        if data_errors:
            return data_errors

        self.create_checks(check_data)
        feedback = 'Чеки успешно созданы'
        return JsonResponse({'ok': feedback}, status=200)

    @staticmethod
    def get_errors(check_data):
        if Check.objects.filter(order__id=check_data['id']).first():
            feedback = 'Для данного заказа уже созданы чеки'
            return JsonResponse({'error': feedback}, status=400)
        if not Printer.objects.filter(point_id=check_data['point_id']).first():
            feedback = 'Для данной точки не настроено ни одного принтера'
            return JsonResponse({'error': feedback}, status=400)
        return None

    @staticmethod
    def create_checks(check_data):
        printers = Printer.objects.filter(point_id=check_data['point_id'])
        for printer in printers:
            check = Check.objects.create(printer_id=printer,
                                         self_type=printer.check_type,
                                         order=check_data,
                                         status='new')
            create_pdf.delay(check)  # used with async worker only. Use create_pdf(check) if you're not going to run it


class NewChecks(View):
    def get(self, request):
        api_key = request.GET.get('api_key')
        if not Printer.objects.filter(api_key=api_key):
            feedback = 'Ошибка авторизации'
            return JsonResponse({'error': feedback}, status=401)
        rendered_checks = Printer.objects.get(api_key=api_key).checks.filter(status='render')
        data = []  # container for key-value pairs to return
        for check in rendered_checks:
            data.append({'id': check.pk})
        return JsonResponse({'checks': data}, status=200)


class CheckToPrint(View):
    def get(self, request):
        api_key = request.GET.get('api_key')
        check_id = request.GET.get('check_id')

        error = self.errors(api_key, check_id)
        if error:
            return error
        check = Check.objects.get(pk=check_id)
        with open(check.pdf_file.name, 'rb') as file:
            response = HttpResponse(FileWrapper(file), content_type='application/pdf', status=200)
        check.status = 'printed'
        check.save()
        return response

    @staticmethod
    def errors(api_key, check_id):
        if not Printer.objects.filter(api_key=api_key):
            feedback = 'Ошибка авторизации'
            return JsonResponse({'error': feedback}, status=401)
        if not Check.objects.filter(Q(pk=check_id) & Q(status='render')):
            feedback = """При создании чеков произошла одна из ошибок: 
                            1. Данного чека не существует
                            2. Для данного чека не сгенерирован PDF-файл"""
            return JsonResponse({'error': feedback}, status=400)
