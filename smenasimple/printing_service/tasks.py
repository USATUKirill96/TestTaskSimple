"""Generates PDF files using HTML templates and order_info. Uses django-rq to manage queue, wkhtmltopdf - to
generate files. Files are stored in /media/ folder, HTML templates are stored in /templates/ folder"""
import requests
import json
import base64
from django.template.loader import render_to_string
from django_rq import job
from smenasimple.settings import BASE_DIR

@job
def create_pdf(check):
    context = {
        'order': check.order,
    }
    if check.self_type == "kitchen":
        html = render_to_string('kitchen-check.html', context=context)
    else:
        html = render_to_string('client-check.html', context=context)
    url = 'http://localhost:8088/'
    utf = html.encode('utf-8')
    base = base64.b64encode(utf)
    html = base.decode('utf-8')
    data = {
        'contents': html,
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        file_path = f"{BASE_DIR}/media/pdf/{check.order['id']}_{check.self_type}.pdf"
        with open(file_path, 'wb') as f:
            f.write(response.content)
        check.status = "render"
        check.pdf_file = file_path
        check.save()
    except Exception as e:
        print(e)
