from django.urls import include, path
from . import views

urlpatterns = [
    #Домашняя страница
    path('', views.corp_home, name='home'),
    #Авторизация
    path('accounts/', include('django.contrib.auth.urls')),
    #Регистрация пользователя
    path('register/', views.register, name="register"),
    #Список корпусов
    path('content/', views.corp_content, name="corp_content"),
    #Созданине корпуса
    path('content/header/create/', views.header_create, name ='header_create'),
    #Удаление корпуса
    path('content/header/delete/<id_corp>', views.header_delete, name ='header_delete'),
    #Просмотр содержимого корпуса
    path('content/header/<id_corp>', views.header_content, name ='header_content'),
    #Загрузка текста
    path('content/item/create/<id_corp>', views.item_create, name ='item_create'),
    #Удаление текста
    path('content/item/delete/<id_item>', views.item_delete, name ='item_delete'),
    #Просмотр текста
    path('content/item/view_file/<id_item>', views.item_view_file, name ='item_view_file'),
    #Выбор вида анализа
    path('content/item/analyze_select/<id_item>', views.analyze_select, name ='analyze_select'),
    #Просмотр результатов анализа
    path('content/item/analyze/<id_item>', views.item_analyze, name ='analyze'),
]
