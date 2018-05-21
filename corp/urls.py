from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('', views.corp_home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name="register"),
    path('content/', views.corp_content, name="corp_content"),
    path('content/header/create/', views.header_create, name ='header_create'),
    path('content/header/delete/<id_corp>', views.header_delete, name ='header_delete'),
    path('content/header/<id_corp>', views.header_content, name ='header_content'),
    path('content/item/create/<id_corp>', views.item_create, name ='item_create'),
    path('content/item/delete/<id_item>', views.item_delete, name ='item_delete'),
    path('content/item/view_file/<id_item>', views.item_view_file, name ='item_view_file'),
    path('content/item/analyze_select/<id_item>', views.analyze_select, name ='analyze_select'),
    path('content/item/analyze/<id_item>', views.item_analyze, name ='analyze'),
]
