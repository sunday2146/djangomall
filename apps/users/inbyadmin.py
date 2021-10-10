from django.contrib import admin
from dadmin.byadmin import BaseOwnerStackInline, BaseOwnerTabularInline
# Register your models here.
from dadmin.models import ADContent


class ADContentStackedInline(BaseOwnerStackInline):
    # 规格值
    model = ADContent
    extra = 1