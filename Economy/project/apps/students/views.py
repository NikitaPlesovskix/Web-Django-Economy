from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from cases.models import  Case, Section, Parameter, Period, Data, Formula, Variable, Job, Status
from cases.form import Create_Case_Form, Create_Period_Form, Create_Section_Form, Create_Parameter_Form, Edit_Case_Form, Edit_Section_Form

# Список всех кейсов
@login_required
def case_list(request):
    return render(request, 'cases/case_list.html', {'case_list': Case.objects.all()})