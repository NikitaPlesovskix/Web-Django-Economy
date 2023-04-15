from django.forms import ModelForm, TextInput
from .models import  Case, Section, Parameter, Period, Data, Formula, Variable
from django import forms
import datetime

class Create_Case_Form(forms.Form):
	Case_Name = forms.CharField(max_length = 50, label = "Название кейса")
	Case_Comment = forms.CharField(max_length = 150, label = "Комментарий к кейсу")

class Create_Period_Form(forms.Form):
	Period_Name = forms.CharField(max_length = 100, label = "Период")

class Create_Section_Form(forms.Form):
	Section_Name = forms.CharField(max_length=100, label = "Название раздела")

class Create_Parameter_Form(forms.Form):
	Parameter_Name = forms.CharField(max_length = 100, label = "Название")
	Parameter_Comment = forms.CharField(label = "Коментарий")

class Edit_Case_Form(forms.Form):
	Case_Name = forms.CharField(max_length = 50, label = "Название кейса")
	Case_Comment = forms.CharField(max_length = 150, label = "Комментарий к кейсу")

class Edit_Section_Form(forms.Form):
	Section_Name = forms.CharField(max_length=100, label = "Название раздела")
	Parameter_Name = forms.CharField(max_length=100, label = "Название параметра")
    # Variable_Name = forms.CharField(max_length=100, label = "Переменная")
	# case_id="Case_ID"
    # section_id="Section_ID"
	
# class Create_Case_Form(ModelForm):
# 	class Meta:
# 		model = Case
# 		fields = ['Case_Name', 'Case_Comment']

	# Case_Name = forms.CharField(max_length = 50, label = "Название кейса")
	# Case_Comment = forms.CharField(max_length = 150, label = "Комментарий к кейсу")

# class DetailForm(forms.Form):
# 	param_name = forms.CharField()
# 	param_value = forms.IntegerField()
# 	param_period = forms.DateField()

# class UploadFileForm(forms.Form):
# 	title = forms.CharField(max_length = 50)
# 	file = forms.FileField()

# class CaseForm(forms.Form):
# 	Case_Name = forms.CharField( max_length = 50, label = "Название кейса")
# 	Case_Comment = forms.CharField(max_length = 150, label = "Комментарий к кейсу")

# class CreateJobForm(forms.Form):

# 	Case_Name = forms.CharField(max_length = 100, label = "Предприятие")
# 	Case_Comment = forms.CharField(max_length = 300, label = "Описание")

# 	Case_Header = forms.CharField(max_length = 50, label= "Заголовок")
# 	Case_Params = forms.CharField(max_length = 100, label= "Параметры")
# 	Params_Period = forms.IntegerField(min_value = 1900 , max_value = datetime.datetime.now().year, label = "Даты")

