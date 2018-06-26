from django.contrib import admin
from .models import Header #Импортируем модель "Заголовок"
from .models import Item   #Импортируем модель "Позиция"

#Регистрируем модели в механизме администрирования
admin.site.register(Header)
admin.site.register(Item)
