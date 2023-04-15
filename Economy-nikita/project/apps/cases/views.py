from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from .models import  Case, Section, Parameter, Period, Data, Formula, Variable
from .form import Create_Case_Form, Create_Period_Form, Create_Section_Form, Create_Parameter_Form, Edit_Case_Form, Edit_Section_Form
from  django.shortcuts import render
from .form import UploadFileForm

# Список всех кейсов
def case_list(request):
    return render(request, 'cases/case_list.html', {'case_list': Case.objects.all()})

# Создание нового кейса
def case_add(request):
    if request.method == "POST":
        form = Create_Case_Form(request.POST)
        if form.is_valid():
            case = Case(
                Case_Name=form.cleaned_data['Case_Name'], 
                Case_Comment=form.cleaned_data['Case_Comment'])
            case.save()
            section_default_add(case) #При создании кейса создаем дефолтную секцию
            return redirect('cases:case_edit', case.Case_ID)
    form = Create_Case_Form()
    case_data = {
        'form': form,
    }
    return render(request, 'cases/case_add.html', case_data)

# Просмотр кейса
def case_view(request, case_id):
    try: case = Case.objects.get(Case_ID = case_id)
    except: raise Http404("Кейс " + str(case_id) + " не найден")
    case_data = {
        'case': case,
        'section_line_in_case': case.section_set.all()} 
    return render(request, 'cases/case_view.html', case_data)

# Редактирование кейса
def case_edit(request, case_id):
    try: case = Case.objects.get(Case_ID = case_id)
    except: raise Http404("Кейс " + str(case_id) + " не найден")    
    if request.method == "POST":
        if request.POST.get("save_case"):
            form = Edit_Case_Form(request.POST, case_id)
            case.Case_Name = request.POST.get("Case_" + str(case.Case_ID))
            case.Case_Comment = request.POST.get("Case_Comment_" + str(case.Case_ID))
            case.save()
            for section in case.section_set.all():
                for parameter in section.parameter_set.all():
                    save_parameter(request, parameter, case)
            return redirect('cases:case_view', case.Case_ID)
        elif request.POST.get("parameter_add"):
            section = Section.objects.get(Section_ID = default_section(case))
            parameter_add_in_table(case, section)
            return redirect('cases:case_edit', case.Case_ID)
        elif request.POST.get("period_add"):
            period_add_in_table(case)
            return redirect('cases:case_edit', case.Case_ID)        
    form = Edit_Case_Form()
    case_data = {
        'case': case,
        'form': form,
        } 
    return render(request, 'cases/case_edit.html', case_data)

        
    # Исходные данные:
    # Перебор всех переменных
    # for i_var in range(0, len(Variable_Name)): 
        # if (Formula_Expression.find(Variable_Name[i_var]) != -1):  # Если переменная найдена
            # Formula_Expression = Formula_Expression.replace(Variable_Name[i_var], str(Variable[i_var])) # То перезаписываем ее на цифру - либо на ID 

    # Далее уже идет вычисление из строки
    # Formula_Expression.split() # Удаляем пробелы
    # Formula_Expression = Formula_Expression.replace("^", "**") # Заменяем степени

    # return eval(Formula_Expression) # Вычисляем строку

# Добавление периода
def period_add(request, case_id):
    case = Case.objects.get(Case_ID = case_id)
    if request.method == "POST":        
        form = Create_Period_Form(request.POST, case_id)
        period = Period(
            case = case,
            Period_Name = request.POST.get("Period_"),
            Period_Sort = sorting_weight_periods(case))
        period.save()
        return redirect('cases:case_edit', case.Case_ID)
    form = Create_Period_Form()
    period_data = {
        'form': form,
        'case': case,
    }
    return render(request, 'cases/period_add.html', period_data)

# Создание сеции по умолчанию
def section_default_add(case):
    section = Section(
        case = case,
        Section_Name = "__default" )#+ str(case.Case_ID))
    section.save()

# ID дефолтной секции
def default_section(case):
    for section in case.section_set.all():
        if section.Section_Name == "__default":
            return section.Section_ID

# Добавлние секции
def section_add(request, case_id):
    case = Case.objects.get(Case_ID = case_id)
    if request.method == "POST":        
        form = Create_Section_Form(request.POST, case_id)
        # if form.is_valid():
        section = Section(
            case = case,
            Section_Name = request.POST.get("Section_"))
        # section.case.add(case) #Создание связи с кейсомв
        section.save()
        return redirect('cases:section_edit', case.Case_ID, section.Section_ID)
    form = Create_Section_Form()
    section_data = {
        'form': form,
        'case': case,
    }
    return render(request, 'cases/section_add.html', section_data)

# Просмотр секции
def section_view(request, case_id, section_id):
    case = Case.objects.get(Case_ID = case_id)   
    section = Section.objects.get(Section_ID = section_id)
    section_data = {
        'case': case, 
        'section': section,
        }    
    return render(request, 'cases/section_view.html', section_data)

# Редактирование секции
def section_edit(request, case_id, section_id):
    case = Case.objects.get(Case_ID = case_id)
    section = Section.objects.get(Section_ID = section_id)
    if request.method == "POST":
        form = Edit_Section_Form(request.POST, case_id, section_id)
        section.Section_Name = request.POST.get("Section_" + str(section.Section_ID))
        section.save()
        for parameter in section.parameter_set.all():
            save_parameter(request, parameter, case)
    form = Edit_Section_Form()
    section_data = {
        'form': form,
        'case': case,
        'section': section,
    }
    return render(request, 'cases/section_edit.html', section_data)

# Добавление параметра
def parameter_add(request, case_id):
    case = Case.objects.get(Case_ID = case_id)
    section = Section.objects.get(Section_ID = default_section(case))
    if request.method == "POST":
        form = Create_Parameter_Form(request.POST)
        parameter = Parameter.objects.create(
            Parameter_Name = request.POST.get("Parameter_"), 
            Parameter_Comment = '', 
            Parameter_Sort = sorting_weight_parameters(section))
        parameter.section.add(section) #Создание связи с секцией
        parameter.save()
        variable = Variable(
            parameter = parameter, 
            Variable_Name = request.POST.get("Variable_"))
        variable.save()
        formula = Formula(
            parameter = parameter,
            Formula_Name = request.POST.get("Formula_"))
        formula.save()
        for period in case.period_set.all():
            data_value = request.POST.get("Data_" + str(period.Period_ID))
            if not data_value:
                data_value = None
            data = Data(
                parameter = parameter,
                period = period,
                Data_Value = data_value)
            data.save()
        return redirect('cases:case_edit', case.Case_ID)
    form = Create_Parameter_Form()
    parameter_data = {
        'form': form,
        'case': case,
        'section': section}
    return render(request, 'cases/parameter_add.html', parameter_data)

# Установка веса для сортировки параметров
def sorting_weight_parameters(section):
    parameters = section.parameter_set.all()
    return (parameters.count() + 1) * 10

# Установка веса для сортировки периодов
def sorting_weight_periods(case):
    periods = case.period_set.all()
    return (periods.count() + 1) * 10

# Добавление параметра в таблице
def parameter_add_in_table(case, section):
    parameter = Parameter.objects.create(
        Parameter_Name = '', 
        Parameter_Comment = '',
        Parameter_Sort = sorting_weight_parameters(section))
    parameter.section.add(section) #Создание связи с секцией
    parameter.save()
    variable = Variable(
        parameter = parameter, 
        Variable_Name = '')
    variable.save()
    formula = Formula(
        parameter = parameter,
        Formula_Name = '')
    formula.save()
    for period in case.period_set.all():
        data = Data(
            parameter = parameter,
            period = period,
            Data_Value = None)
        data.save()

# Добавление периода в таблице
def period_add_in_table(case):
        period = Period(
            case = case,
            Period_Name = '',
            Period_Sort = sorting_weight_periods(case))
        period.save()

# Сохранение параметра
def save_parameter(request, parameter, case):
    parameter.Parameter_Name = request.POST.get("Parameter_" + str(parameter.Parameter_ID))
    parameter.save()
    parameter.variable.Variable_Name = request.POST.get("Variable_" + str(parameter.variable.Variable_ID)) 
    parameter.variable.save()
    parameter.formula.Formula_Name = request.POST.get("Formula_" + str(parameter.formula.Formula_ID)) 
    parameter.formula.save()
    for period in case.period_set.all(): 
        for data in parameter.data_set.all():
            if data.period.Period_ID == period.Period_ID and request.POST.get("Data_" + str(data.Data_ID)):
                data.Data_Value = request.POST.get("Data_" + str(data.Data_ID)) 
                data.save()

def page(request):
    form = UploadFileForm()
    return render(request, "page.html", {"form": form})

def page(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        save_path = '/uploads/product_images/' # папка для сохранения файлов
        if form.is_valid():
            # сохранение файла
            with open(save_path+request.FILES['file'].name, 'wb+') as destination:
                for chunk in request.FILES['file'].chunks():
                    destination.write(chunk)
    else:
        form = UploadFileForm()
    return render(request, "page.html", {'form': form})

# def case_view_all(request):
#     return render(request, 'cases/case_view_all.html')
    
# def section_list(request):
#     return render(request, 'cases/section_list.html', {
#         'section_list': Section.objects.all()
#         })
# def caseparam_view(request, case_id, section_id, caseparam_id):
#     try: caseparam = CaseParam.objects.get(id = caseparam_id)
#     except: raise Http404("Раздел не найден")
#     return render(request, 'cases/caseparam_view.html', {'case': Case.objects.get(id = case_id), 'section': Section.objects.get(id = section_id), 'caseparam': caseparam, 'dateparam_list_in_caseparam': caseparam.dateparam_set.all()})