from django.contrib import admin
from django.contrib.auth.models import User, Group

from .models import *

# Пользователи и группы не используются в проекте; скрыты, чтобы не вводить пользователя в заблуждение
admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_key', 'check_type', 'point_id')  # Пункты, отображаемые в панели администратора
    list_display_links = list_display
    list_filter = ('point_id',)  # По каким критериям можно фильтровать
    search_fields = ('name', 'api_key', 'point_id')  # Поля для функции поиска
    ordering = ('api_key', 'point_id')  # сортировка по умолчанию


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ('pk', 'printer_id', 'self_type', 'status')  # Пункты, отображаемые в панели администратора
    list_display_links = list_display
    list_filter = ('printer_id', 'self_type', 'status')  # По каким критериям можно фильтровать
    search_fields = ('pk', 'printer_id')  # Поля для функции поиска
    ordering = ('pk',)  # сортировка по умолчанию
