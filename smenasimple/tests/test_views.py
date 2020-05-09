import os

from django.test import TestCase

from printing_service.models import Printer, Check
from printing_service.views import CreateChecks
from smenasimple.settings import BASE_DIR

"""Usage of this test may override current check data. be careful and use it on dev server only"""

check_data = {
    "id": 1,
    "price": 780,
    "items": [
        {
            "name": "Вкусная пицца",
            "quantity": 2,
            "unit_price": 250
        },
        {
            "name": "Не менее вкусные роллы",
            "quantity": 1,
            "unit_price": 280
        }
    ],
    "address": "г. Уфа, ул. Ленина, д. 42",
    "client": {
        "name": "Иван",
        "phone": 9173332222
    },
    "point_id": 1
}


class CreateChecksTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        printer = Printer.objects.create(name="test printer", api_key=1, check_type="client", point_id=1)
        Printer.objects.create(name="test printer", api_key=2, check_type="kitchen", point_id=1)
        CreateChecks.create_checks(check_data)
        Check.objects.create(printer_id=printer, self_type='client', order=check_data, status='render')

    def test_errors_check_exists(self):
        print("Method: function errors_check_exists")
        input_json = {'point_id': 1, 'id': 1}
        error = CreateChecks.get_errors(check_data=input_json)
        self.assertNotEqual(error, None)

    def test_errors_no_printer_exist(self):
        print("Method: function errors_no_printer_exists")
        input_json = {'point_id': 0, 'id': 0}
        error = CreateChecks.get_errors(check_data=input_json)
        self.assertNotEqual(error, None)

    def test_errors_everything_alright(self):
        print("Method: function errors_everything_alright")
        input_json = {'point_id': 1, 'id': 0}
        error = CreateChecks.get_errors(check_data=input_json)
        self.assertEqual(error, None)

    def test_checks_created(self):
        print("Method: check generation")
        result_client = os.path.exists(f"{BASE_DIR}/media/pdf/1_client.pdf")
        result_kitchen = os.path.exists(f"{BASE_DIR}/media/pdf/1_kitchen.pdf")
        self.assertEqual(result_client, True)
        self.assertEqual(result_kitchen, True)




