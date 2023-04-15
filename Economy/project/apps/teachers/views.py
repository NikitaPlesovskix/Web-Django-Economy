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
    # if request.user.groups.filter(name='Students').exists():
    user = request.user
    job = Job.objects.all()
    case_list = Case.objects.all()
    # user.job.case.all()
    # Case.objects.all()
        # return redirect('students:case_list')
    # elif request.user.is_superuser:
        # return redirect('admin/')
    # elif request.user.groups.filter(name='Teachers').exists():
        # return redirect('teachers:case_list')
    # else:
        # return redirect('login/')
    case_data = {
        'case_list': case_list,
        'users': user,
        'job': job,
    }
    return render(request, 'cases/case_list.html', case_data )