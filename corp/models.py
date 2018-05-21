from django.db import models
from django.utils import timezone
# Create your models here.

class Header(models.Model):
    class Meta:
        verbose_name = "Заголовок корпуса"
        verbose_name_plural = "Заголовки корпусов"
    id_corp = models.AutoField(primary_key=True, verbose_name="ID корпуса")
    name = models.CharField(max_length=100, verbose_name="Название корпуса")
    type = models.CharField(max_length=100, verbose_name="Тип корпуса")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

def texts_path(instance, filename):
    return 'texts/{0}/{1}'.format(instance.id_corp, filename)

class Item(models.Model):
    class Meta:
        verbose_name = "Позиция корпуса"
        verbose_name_plural = "Позиции корпусов"
    id_item = models.AutoField(primary_key=True, verbose_name="ID текста")
    id_corp = models.ForeignKey(Header, db_column='id_corp', verbose_name="ID корпуса", on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name="Название текста")
    author = models.CharField(max_length=100, verbose_name="Автор текста")
    theme = models.CharField(max_length=100, verbose_name="Тема текста")
    date = models.DateField(verbose_name="Дата текста")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")
    file = models.FileField(upload_to=texts_path, verbose_name="Текст")
    xml = models.FileField(upload_to='items/xml/', verbose_name="XML")

    def __str__(self):
        return self.title
