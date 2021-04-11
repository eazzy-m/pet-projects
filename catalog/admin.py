from django.contrib import admin
from django import forms
from django.forms import ModelChoiceField

# Register your models here.
from catalog.models import *


class MobTelAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'product_category':
            return ModelChoiceField(CategoryGoods.objects.filter(slug='mobtel'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class TelevisionAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'product_category':
            return ModelChoiceField(CategoryGoods.objects.filter(slug='television'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



admin.site.register(CategoryFirst)
admin.site.register(CategoryGoods)
admin.site.register(CategorySecond)
admin.site.register(MobTel, MobTelAdmin)
admin.site.register(Television, TelevisionAdmin)
admin.site.register(Basket)
admin.site.register(Goods_in_basket)
admin.site.register(Order)