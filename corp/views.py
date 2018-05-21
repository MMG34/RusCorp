from django.template.context_processors import csrf
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.html import format_html
from .models import Header, Item
from .forms import RegisterForm, HeaderForm, ItemForm
import datetime

from natasha import (
    NamesExtractor,
    LocationExtractor,
    DatesExtractor,
    MoneyExtractor,
)
from natasha.markup import (
    format_json
)
import copy

def get_extractor( extract_type ):
    if extract_type == "name":
         return NamesExtractor()
    elif extract_type == "location":
         return LocationExtractor()
    elif extract_type == "date":
         return DatesExtractor()
    elif extract_type == "money":
         return MoneyExtractor()

# Create your views here.

def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = RegisterForm()
    if request.POST:
        newuser_form = RegisterForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'],
                                        password=newuser_form.cleaned_data['password1'])
            auth.login(request, newuser)
            return HttpResponseRedirect("/")
        else:
            args['form'] = newuser_form
    return render_to_response('registration/register.html', args)

def corp_home(request):
    if auth.get_user(request).is_authenticated:
        return HttpResponseRedirect("/content/")
    else:
        return render( request, 'corp/base.html')

def corp_content(request):
    headers = Header.objects.all()
    return render(request, 'corp/corp_content.html', {'headers':headers})

def header_content(request, id_corp=None):
    items = Item.objects.filter(id_corp=id_corp)
    corp = Header.objects.filter(id_corp=id_corp)
    return render(request, 'corp/header_content.html', {'items':items, 'id_corp':id_corp, 'corp_name':corp[0].name })

@login_required
def header_create(request):
    if request.method == "POST":
        form = HeaderForm(request.POST)
        if form.is_valid():
            header = form.save(commit=False)
            header.save()
            return HttpResponseRedirect("/content/")
    else:
        form = HeaderForm()
    return render(request, 'corp/header_create.html', {'form': form})

@login_required
def header_delete(request, id_corp=None):
    header = get_object_or_404(Header, id_corp=id_corp)
    header.delete()
    return HttpResponseRedirect("/content/")

@login_required
def item_create(request, id_corp=None):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            header = Header.objects.get(id_corp=id_corp)
            item.id_corp = header
            item.save()
            next = request.GET['next']
            return HttpResponseRedirect(next)
    else:
        form = ItemForm()
    return render(request, 'corp/item_create.html', {'form': form, 'id_corp': id_corp})

@login_required
def item_view_file(request, id_item=None):
    item = get_object_or_404(Item, id_item=id_item)
    file = open(item.file.path, "r")
    text = file.read()
    next = request.GET['next']
    return render(request, 'corp/item_view_file.html', { 'title': item.title, 'text': text, 'next': next })

@login_required
def item_delete(request, id_item=None):
    item = get_object_or_404(Item, id_item=id_item)
    next = request.GET['next']
    item.delete()
    return HttpResponseRedirect(next)

@login_required
def analyze_select(request, id_item=None):
    if request.method == "POST":
        return item_analyze(request, id_item=id_item)
    next = request.GET['next']
    return render(request, 'corp/analyze_select.html', { 'id_item': id_item, 'next': next })

@login_required
def item_analyze(request, id_item=None):
    item = get_object_or_404(Item, id_item=id_item)
    file = open(item.file.path, "r")
    text = file.read()

    extract_type = request.POST.get('extract')
    extractor = get_extractor( extract_type )
    matches = extractor(text)
    spans = [_.span for _ in matches]
    facts = [_.fact.as_json for _ in matches]
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
    result = format_json(uniq_count)
    next = request.GET['next']
    return render(request, 'corp/item_analyze.html', { 'title': item.title, 'result': result, 'next': next })
