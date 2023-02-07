from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .models import  Case, Section, Parameter, Period, Data

def case_list(request):
    case_list = Case.objects.all()
    return render(request, 'cases/case_list.html', {'case_list': case_list})

def case_view(request, case_id):
    try: case = Case.objects.get(Case_ID = case_id)
    except: raise Http404("Кейс " + str(case_id) + " не найден" + Case.objects.get(Case_ID = case_id) )
    return render(request, 'cases/case_view.html', {
        'case': case, 
        'section_line_in_case': case.section_set.all(), 
        'period_column_in_case': case.period_set.all()
        })
    
# def section_list(request):
#     return render(request, 'cases/section_list.html', {
#         'section_list': Section.objects.all()
#         })
    
# def section_view(request, case_id, section_id):
#     try: section = Section.objects.get(id = section_id)
#     except: raise Http404("Раздел не найден")
#     return render(request, 'cases/section_view.html', {'case': Case.objects.get(id = case_id), 'section': section, 'caseparam_list_in_section': section.caseparam_set.all()})

# def caseparam_view(request, case_id, section_id, caseparam_id):
#     try: caseparam = CaseParam.objects.get(id = caseparam_id)
#     except: raise Http404("Раздел не найден")
#     return render(request, 'cases/caseparam_view.html', {'case': Case.objects.get(id = case_id), 'section': Section.objects.get(id = section_id), 'caseparam': caseparam, 'dateparam_list_in_caseparam': caseparam.dateparam_set.all()})

