from django.db import models #Импортируем модели Django

#Объект "Заголовок"
class Header(models.Model):
    #Метаданные (текстовые описания)
    class Meta:
        verbose_name = "Заголовок корпуса"
        verbose_name_plural = "Заголовки корпусов"
    id_corp = models.AutoField(primary_key=True, verbose_name="ID корпуса")
    #Автоинкрементное поле. primary_key - первичный ключ таблицы, verbose_name - тестовое описание
    name = models.CharField(max_length=100, verbose_name="Название корпуса")
    #Текстовое поле. max_length - длина.
    type = models.CharField(max_length=100, verbose_name="Тип корпуса")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    #Поле дата/время. auto_now_add - автоматическая установка текущей даты и времени при создании объекта.

    def __str__(self):
        return self.name

def texts_path(instance, filename):
    #Функция для получения пути файла для сохранения
    return 'texts/{0}/{1}'.format(instance.id_corp, filename)

#Объект "Позиция"
class Item(models.Model):
    class Meta:
        verbose_name = "Позиция корпуса"
        verbose_name_plural = "Позиции корпусов"
    id_item = models.AutoField(primary_key=True, verbose_name="ID текста")
    id_corp = models.ForeignKey(Header, db_column='id_corp', verbose_name="ID корпуса", on_delete=models.CASCADE)
    #Поле внешнего ключа. Ссылается на модель Header, столбец "id_corp"(db_column). Задано каскадное удаление.
    title = models.CharField(max_length=100, verbose_name="Название текста")
    author = models.CharField(max_length=100, verbose_name="Автор текста")
    theme = models.CharField(max_length=100, verbose_name="Тема текста")
    date = models.DateField(verbose_name="Дата текста")
    #Поле типа дата
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")
    file = models.FileField(upload_to=texts_path, verbose_name="Текст")
    #Поле типа файл. Содержит в себе путь до файла с текстом на сервере.

    def __str__(self):
        return self.title
