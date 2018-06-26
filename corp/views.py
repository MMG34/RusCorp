from django.template.context_processors import csrf
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import Header, Item
from .forms import RegisterForm, HeaderForm, ItemForm

#Экстракторы ключевых слов
from natasha import (
    NamesExtractor,
    LocationExtractor,
    DatesExtractor,
    MoneyExtractor,
)
#Форматирование в JSON
from natasha.markup import (
    format_json
)
import copy

#Получение нужного экстрактора
def get_extractor( extract_type ):
    if extract_type == "name":
         #Экстрактор имён
         return NamesExtractor()
    elif extract_type == "location":
         #Экстрактор мест
         return LocationExtractor()
    elif extract_type == "date":
         #Экстрактор дат
         return DatesExtractor()
    elif extract_type == "money":
         #Экстрактор денежных сумм
         return MoneyExtractor()

# Create your views here.

#Регистрация пользователя
def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = RegisterForm()
    if request.POST:
        #Форма регистрации
        newuser_form = RegisterForm(request.POST)
        if newuser_form.is_valid():
            #Если форма не содержит ошибок -> сохраняем нового пользователя
            newuser_form.save()
            #И выполняем авторизацию под ним
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'],
                                        password=newuser_form.cleaned_data['password1'])
            auth.login(request, newuser)
            return HttpResponseRedirect("/")
        else:
            args['form'] = newuser_form
    return render_to_response('registration/register.html', args)

#Главная страница
def corp_home(request):
    #Если пользователь авторизован -> отображаем страницу с содержимым
    if auth.get_user(request).is_authenticated:
        return HttpResponseRedirect("/content/")
    else:
    #Иначе отображаем стартовую страницу
        return render( request, 'corp/base.html')

#Список копрусов
def corp_content(request):
    #Получение всех заголовков
    headers = Header.objects.all()
    #Рендер страницы с корпусами и передача списка заголовков
    return render(request, 'corp/corp_content.html', {'headers':headers})

#Тексты в корпусе
def header_content(request, id_corp=None):
    #Получение списка текстов в корпусе по ID корпуса
    items = Item.objects.filter(id_corp=id_corp)
    #Получение объекта заголовка корпуса по его ID
    corp = Header.objects.filter(id_corp=id_corp)
    #Рендер страницы с содержимым корпуса
    return render(request, 'corp/header_content.html', {'items':items, 'id_corp':id_corp, 'corp_name':corp[0].name })

#Создание корпуса
@login_required
def header_create(request):
    if request.method == "POST":
        form = HeaderForm(request.POST)
        if form.is_valid():
            header = form.save(commit=False)
            #Сохранение объекта заголовка корпуса
            header.save()
            return HttpResponseRedirect("/content/")
    else:
        form = HeaderForm()
    return render(request, 'corp/header_create.html', {'form': form})

#Удаление корпуса
@login_required
def header_delete(request, id_corp=None):
    #Получение заголовка по ID и возврат ошибки 404 в случае его отсутствия
    header = get_object_or_404(Header, id_corp=id_corp)
    #Удаление заголовка корпуса
    header.delete()
    #И перенаправление на страницу со списком корпусов
    return HttpResponseRedirect("/content/")

#Загрузка текста
@login_required
def item_create(request, id_corp=None):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            header = Header.objects.get(id_corp=id_corp)
            #При создании нового текста указываем объект заголовка для связи
            item.id_corp = header
            #И сохраняем его
            item.save()
            next = request.GET['next']
            return HttpResponseRedirect(next)
    else:
        form = ItemForm()
    return render(request, 'corp/item_create.html', {'form': form, 'id_corp': id_corp})

#Просмотр текста
@login_required
def item_view_file(request, id_item=None):
    item = get_object_or_404(Item, id_item=id_item)
    #Читаем файл на сервере с текстом
    file = open(item.file.path, "r")
    text = file.read()
    #Получаем из атрибутов запроса страницу для переадресации
    next = request.GET['next']
    #Рендерим страницу для просмотра текста
    return render(request, 'corp/item_view_file.html', { 'title': item.title, 'text': text, 'next': next })

#Удаление текста
@login_required
def item_delete(request, id_item=None):
    item = get_object_or_404(Item, id_item=id_item)
    next = request.GET['next']
    item.delete()
    return HttpResponseRedirect(next)

#Выбор анализа
@login_required
def analyze_select(request, id_item=None):
    if request.method == "POST":
        return item_analyze(request, id_item=id_item)
    next = request.GET['next']
    return render(request, 'corp/analyze_select.html', { 'id_item': id_item, 'next': next })

#Выполнение анализа
@login_required
def item_analyze(request, id_item=None):
    item = get_object_or_404(Item, id_item=id_item)
    file = open(item.file.path, "r")
    text = file.read()

    #Получение выбранного экстрактора (radio-button)
    extract_type = request.POST.get('extract')
    #Получение нужного экстрактора
    extractor = get_extractor( extract_type )
    #Выполнение анализа текста с помощью экстрактора
    matches = extractor(text)
    spans = [_.span for _ in matches]
    facts = [_.fact.as_json for _ in matches]
    #Выделяем уникальные ключевые слова и подсчитываем количество повторов
    uniq_facts = []
    uniq_count = []
    for x in facts:
        if x not in uniq_facts:
            uniq_facts.append(x)
            i = uniq_facts.index(x)
            uniq_count.append(copy.deepcopy(uniq_facts[i]))
            uniq_count[i]['count'] = 1
        else:
            i = uniq_facts.index(x)
            uniq_count[i]['count'] += 1
    #Форматируем результат в JSON
    result = format_json(uniq_count)
    next = request.GET['next']
    #Рендерим страницу для просмотра результата анализа
    return render(request, 'corp/item_analyze.html', { 'title': item.title, 'result': result, 'next': next })
