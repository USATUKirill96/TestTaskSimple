import json

from django.http import JsonResponse
from django.views import View

from .models import Check, Printer
from .tasks import create_pdf


# Create your views here.
class CreateChecks(View):

    def post(self, request):

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
            create_pdf(check)
            #create_pdf.delay(check)



def new_checks(request):
    pass


def check(request):
    pass
