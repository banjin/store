from django.contrib import admin

# Register your models here.
from .models import Person,Question,Choice
admin.site.register(Person)
admin.site.register(Choice)
admin.site.register(Question)