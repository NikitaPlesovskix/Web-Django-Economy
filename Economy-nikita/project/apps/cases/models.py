from django.db import models
# from django.contrib.auth.models import User
# from django.db.models import Q
# import datetime

# Модели: Case, Section, Parameter, Period, Data

# Модель Кейс - это самая главная модель которая содержит в себе все параметры, работы, файлы, и т.д
class Case(models.Model):
    Case_ID = models.AutoField(primary_key=True)
    Case_Name = models.CharField('Название кейса', max_length=50)
    Case_Comment = models.TextField('Коментарий')
    Case_Parent = models.IntegerField('Родительский кейс', default=-1)
    Image = models.FileField(upload_to= 'uploads/product_images/', blank=True, null=True)

    def __str__(self):
        return self.Case_Name

    def get_absolute_url(self):  # Отвечает за ссылку 'Смотреть на сайте' - переход от админки на сайт
        return f'/cases/{self.Case_ID}/'

    class Meta:
        verbose_name = 'Кейс'
        verbose_name_plural = 'Кейсы'


# Раздел кейса, нужен для того чтобы обозначать имена разделов, если такие понадобятся
# Содержит в себе параметры
class Section(models.Model):    
    Section_ID = models.AutoField(primary_key=True)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    Section_Name = models.CharField('Название раздела', max_length=100)

    def __str__(self):
        return self.Section_Name

    def get_absolute_url(self):  # Отвечает за ссылку 'Смотреть на сайте' - переход от админки на сайт
        return f'/cases/section/{self.Section_ID}/'

    class Meta:
        verbose_name = 'Раздел кейса'
        verbose_name_plural = 'Разделы кейса'


# Параметр кейса, нужен для того чтобы отображать имя, комментарий
class Parameter(models.Model): # Бывший CaseParam
    Parameter_ID = models.AutoField(primary_key=True)
    section = models.ManyToManyField(Section) # Cвязь многие ко многим
    Parameter_Name = models.CharField('Название', max_length=100)
    Parameter_Comment = models.TextField('Коментарий')
    Parameter_Sort = models.FloatField('Вес при сортировке', default=Parameter_ID, null=True) # По умолчанию равен ID - то есть в порядке создания
    # Parameter_Var = models.CharField('Название переменной', max_length=100) отделяем название переменной, как отдельную сущноть

    def __str__(self):
        return self.Parameter_Name

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'


# Период сбора данных - периоды в промежутках которых были собранны данные
class Period(models.Model):
    Period_ID = models.AutoField(primary_key=True)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    Period_Name = models.CharField('Период', max_length=100)
    Period_Sort = models.FloatField('Вес при сортировке', default=Period_ID, null=True) # По умолчанию равен ID - то есть в порядке создания
    
    def __str__(self):
        return self.Period_Name

    class Meta:
        verbose_name = 'Период'
        verbose_name_plural = 'Периоды'


# Данные - значения параметра за определенный период
class Data(models.Model):
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)    
    Data_ID = models.AutoField(primary_key=True)
    Data_Value = models.FloatField('Значение', default=0, null=True, blank=True)
    
    def __str__(self):
        return str(self.Data_Value)

    class Meta:
        verbose_name = 'Значение'
        verbose_name_plural = 'Значения'
        

# Переменные
class Variable(models.Model):
    Variable_ID = models.AutoField(primary_key=True)
    parameter = models.OneToOneField(Parameter, on_delete=models.CASCADE)
    Variable_Name = models.CharField('Переменная', max_length= 100)

    def __str__(self):
        return self.Variable_Name

    class Meta:
        verbose_name = 'Переменная'
        verbose_name_plural = 'Переменные'


# Формулы - модель для связи формулы с Переменными
class Formula(models.Model):
    Formula_ID = models.AutoField(primary_key=True)
    parameter = models.OneToOneField(Parameter, on_delete=models.CASCADE)    
    variable = models.ManyToManyField(Variable) # Cвязь многие ко многим
    Formula_Name = models.CharField('Формула', max_length= 100)

    def __str__(self):
        return self.Formula_Name
    
    class Meta:
        verbose_name = 'Формула'
        verbose_name_plural = 'Формулы'
