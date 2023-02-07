from django.contrib import admin
from .models import  Case, Section, Parameter, Period, Data

class SectionInline(admin.TabularInline): # Список Разделов
    classes = ('collapse',) # Свернуто по умолчанию
    extra = 0 # Не показывать дополнительные
    model = Section # На основе модели разделов
    verbose_name_plural = "Разделы"
    show_change_link = True

class ParameterInline(admin.TabularInline): # Список Параметров
    classes = ('collapse',)
    extra = 0
    model = Parameter.section.through # Множественный выбор - т.к. связь многие ко многим

class PeriodInline(admin.TabularInline): # Список Периодов
    classes = ('collapse',)
    extra = 0
    model = Period

class DataInline(admin.TabularInline): # Список Данных
    classes = ('collapse',)
    extra = 0
    model = Data

@admin.register(Case) 
class Case_Admin(admin.ModelAdmin): # Отображение списка Кейсов в админке
    list_display = ('Case_ID','Case_Name','Case_Comment')
    list_display_links = ('Case_Name',)
    search_fields = ('Case_ID','Case_Name','Case_Comment') 
    inlines = [ SectionInline, ] # Отображение списка связанных с ним Разделов

@admin.register(Section)
class Section_Admin(admin.ModelAdmin): # Отображение списка Разделов в админке
    list_display = ('Section_ID','Section_Name','case')
    list_display_links = ('Section_Name','case',)
    search_fields = ('Section_ID','case','Section_Name')
    inlines = [ ParameterInline, ] # Отображение списка связанных с ним Параметров

@admin.register(Parameter)
class Parameter_Admin(admin.ModelAdmin): # Отображение списка Параметров в админке
    list_display = ('Parameter_ID','Parameter_Name','Parameter_Comment','Parameter_Sort')
    list_display_links = ('Parameter_Name',)
    search_fields = ('Parameter_ID','Parameter_Name','Parameter_Comment','Parameter_Sort')
    inlines = [ DataInline, ] # Отображение списка связанных с ним Данных

@admin.register(Period)
class Period_Admin(admin.ModelAdmin): # Отображение списка Периодов в админке
    list_display = ('Period_ID','Period_Name','case','Period_Sort')
    list_display_links = ('Period_Name','case',)
    search_fields = ('Period_ID','Period_Name','case','Period_Sort')
    inlines = [ DataInline, ] # Отображение списка связанных с ним Данных

@admin.register(Data) # Отображение списка Данных в админке
class Data_Admin(admin.ModelAdmin):
    list_display = ('Data_ID','parameter','period','Data_Value')
    list_display_links = ('parameter','period')   
    search_fields = ('Data_ID','parameter','period','Data_Value')