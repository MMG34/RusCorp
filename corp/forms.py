from django import forms #Формы Django
from django.contrib.auth.forms import UserCreationForm #Форма создания пользователя
from django.contrib.auth.models import User #Модель пользователя Django
from .models import Header, Item

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Обязательно. Укажите действущий email адрес.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class HeaderForm(forms.ModelForm):
    class Meta:
        model = Header
        fields = ('name', 'type')

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('title', 'author', 'theme', 'date', 'file')
        widgets = { 'date': forms.widgets.DateInput(attrs={'type': 'date'})}
