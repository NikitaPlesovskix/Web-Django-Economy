from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .models import  Case, Section, Parameter, Period, Data, Formula, Variable, Job, Status
from .form import Create_Case_Form, Create_Period_Form, Create_Section_Form, Create_Parameter_Form, Edit_Case_Form, Edit_Section_Form

# Список всех кейсов
@login_required
def case_list(request):
    case_data = {
        'case_list': Case.objects.all(),
    }
    return render(request, 'cases/case_list.html', case_data )

# Создание нового кейса
@login_required
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
@login_required
def case_view(request, case_id):
    try: case = Case.objects.get(Case_ID = case_id)
    except: raise Http404("Кейс " + str(case_id) + " не найден")
    case_data = {
        'case': case,} 
    return render(request, 'cases/case_view.html', case_data)

# Редактирование кейса
@login_required
def case_edit(request, case_id):
    # try: case = Case.objects.get(Case_ID = case_id)
    # except: raise Http404("Кейс " + str(case_id) + " не найден")
    case = Case.objects.get(Case_ID = case_id)
    if request.method == "POST":
        case_save(request, case)
        form = Edit_Case_Form(request.POST, case_id)
        if request.POST.get("save_case"): #Сохранение
            return redirect('cases:case_edit', case.Case_ID)        
        elif request.POST.get("period_add"): #Добавление периода
            period_add_in_table(case)
            return redirect('cases:case_edit', case.Case_ID)
        elif request.POST.get("section_add"): #Добавление периода
            section_add_in_table(case)
            return redirect('cases:case_edit', case.Case_ID)
        elif request.POST.get("formula_calculate"): #Расчет формул
            formula_calc = formula_calculate(request, case)
            if formula_calc:
                messages.error(request, formula_calc)
            else: return redirect('cases:case_edit', case.Case_ID)
        else:
            for section in case.section_set.all(): #Добавление параметров
                if request.POST.get("parameter_add_in_" + str(section.Section_ID)):
                    parameter_add_in_table(case, section)
                    return redirect('cases:case_edit', case.Case_ID)
                    # setattr(section, "Section_Name", new_data)
            section_parameter_in_table(request, case)
            return redirect('cases:case_edit', case.Case_ID)
    form = Edit_Case_Form()
    case_data = {
        'case': case,
        'form': form,        
        'parameter_in_case': parameter_in_case(case),
        'section_in_case': case.section_set.all()
        }
    return render(request, 'cases/case_edit.html', case_data)

# Сохранение кейса
def case_save(request, case):
    case.Case_Name = request.POST.get("Case_" + str(case.Case_ID))
    case.Case_Comment = request.POST.get("Case_Comment_" + str(case.Case_ID))
    case.save()
    for section in case.section_set.all():
        if not section.Section_Name == "__default":
            section.Section_Name = request.POST.get("Section_" + str(section.Section_ID))
            section.save()
        for parameter in section.parameter_set.all():
            parameter_save(request, parameter, case)
    for period in case.period_set.all():
        period.Period_Name = request.POST.get("Period_" + str(period.Period_ID))
        period.save()

    # Исходные данные:
    # Перебор всех переменных
    # for i_var in range(0, len(Variable_Name)): 
        # if (Formula_Expression.find(Variable_Name[i_var]) != -1):  # Если переменная найдена
            # Formula_Expression = Formula_Expression.replace(Variable_Name[i_var], str(Variable[i_var])) # То перезаписываем ее на цифру - либо на ID 

    # Далее уже идет вычисление из строки
    # Formula_Expression.split() # Удаляем пробелы
    # Formula_Expression = Formula_Expression.replace("^", "**") # Заменяем степени

    # return eval(Formula_Expression) # Вычисляем строку

# Создание сеции по умолчанию
def section_default_add(case):
    section = Section(
        case = case,
        Section_Name = "__default",
        Section_Sort = sorting_weight_section(case))
    section.save()

# ID дефолтной секции
def default_section(case):
    for section in case.section_set.all():
        if section.Section_Name == "__default":
            return section.Section_ID

# Добавлние секции
def section_add_in_table(case):
    section = Section.objects.create(
        case = case,
        Section_Name = '',
        Section_Sort = sorting_weight_section(case))
    section.save()

# Добавлние секции
# def section_add(request, case_id):
#     case = Case.objects.get(Case_ID = case_id)
#     if request.method == "POST":        
#         form = Create_Section_Form(request.POST, case_id)
#         # if form.is_valid():
#         section = Section(
#             case = case,
#             Section_Name = request.POST.get("Section_"))
#         # section.case.add(case) #Создание связи с кейсом
#         section.save()
#         return redirect('cases:section_edit', case.Case_ID, section.Section_ID)
#     form = Create_Section_Form()
#     section_data = {
#         'form': form,
#         'case': case,
#     }
#     return render(request, 'cases/section_add.html', section_data)

# # Просмотр секции
# # def section_view(request, case_id, section_id):
#     case = Case.objects.get(Case_ID = case_id)   
#     section = Section.objects.get(Section_ID = section_id)
#     section_data = {
#         'case': case, 
#         'section': section,
#         }    
#     return render(request, 'cases/section_view.html', section_data)

# Редактирование секции
def section_edit(request, case_id, section_id):
    case = Case.objects.get(Case_ID = case_id)
    section = Section.objects.get(Section_ID = section_id)
    if request.method == "POST":
        form = Edit_Section_Form(request.POST, case_id, section_id)
        section.Section_Name = request.POST.get("Section_" + str(section.Section_ID))
        section.save(update_fields=['Section_Name'])
        for parameter in section.parameter_set.all():
            parameter_save(request, parameter, case)
    form = Edit_Section_Form()
    section_data = {
        'form': form,
        'case': case,
        'section': section,
    }
    return render(request, 'cases/section_edit.html', section_data)

# Редактирование связи парамеров и секций в таблице
def section_parameter_in_table(request, case):
    for parameter in parameter_in_case(case): #Перебираем по очереди все параметры в кейсе
        for section in case.section_set.all(): #Перебираем все секции в кейсе, для проверки связи
            if not section.Section_Name == "__default":
                if request.POST.get(str(section.Section_ID) + "_" + str(parameter.Parameter_ID), None):
                    parameter.section.add(section)
                    parameter.save()
                elif parameter.section.filter(Section_ID = section.Section_ID).count(): # Проверка связи параметра с разделом
                    parameter.section.remove(section)
                    parameter.save()

# Редактирование связи парамеров и секций
# def section_parameter(request, case_id): 
#     case = Case.objects.get(Case_ID = case_id)
#     if request.method == "POST":
#         for parameter in parameter_in_case(case): #Перебираем по очереди все параметры в кейсе
#             for section in case.section_set.all(): #Перебираем все секции в кейсе, для проверки связи
#                 if not section.Section_Name == "__default":
#                     if request.POST.get(str(section.Section_ID) + "_" + str(parameter.Parameter_ID), None):
#                         parameter.section.add(section)
#                         parameter.save()
#                     elif parameter.section.filter(Section_ID = section.Section_ID).count(): # Проверка связи параметра с разделом
#                         parameter.section.remove(section)
#                         parameter.save()
#         return redirect('cases:section_parameter', case.Case_ID)
#     section_parameter_data = {
#         'case': case,
#         'parameter_in_case': parameter_in_case(case),
#         'section_in_case': case.section_set.all()
#     }
#     return render(request, 'cases/section_parameter.html', section_parameter_data) 

# Вывод всех параметров в кейсе
def parameter_in_case(case):
    return Section.objects.get(Section_ID = default_section(case)).parameter_set.all()

# Добавление параметра в таблице
def parameter_add_in_table(case, section):
    parameter = Parameter.objects.create(
        Parameter_Name = '', 
        Parameter_Comment = '',
        Parameter_Sort = sorting_weight_parameters(case))
    parameter.section.add(section) #Создание связи с секцией
    parameter.section.add(Section.objects.get(Section_ID = default_section(case)))
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

# Добавление параметра
# def parameter_add(request, case_id):
#     case = Case.objects.get(Case_ID = case_id)
#     section = Section.objects.get(Section_ID = default_section(case))
#     if request.method == "POST":
#         form = Create_Parameter_Form(request.POST)
#         parameter = Parameter.objects.create(
#             Parameter_Name = request.POST.get("Parameter_"), 
#             Parameter_Comment = '', 
#             Parameter_Sort = sorting_weight_parameters(section))
#         parameter.section.add(section) #Создание связи с секцией
#         parameter.save()
#         variable = Variable(
#             parameter = parameter, 
#             Variable_Name = request.POST.get("Variable_"))
#         variable.save()
#         formula = Formula(
#             parameter = parameter,
#             Formula_Name = request.POST.get("Formula_"))
#         formula.save()
#         for period in case.period_set.all():
#             data_value = request.POST.get("Data_" + str(period.Period_ID))
#             if not data_value:
#                 data_value = None
#             data = Data(
#                 parameter = parameter,
#                 period = period,
#                 Data_Value = data_value)
#             data.save()
#         return redirect('cases:case_edit', case.Case_ID)
#     form = Create_Parameter_Form()
#     parameter_data = {
#         'form': form,
#         'case': case,
#         'section': section}
#     return render(request, 'cases/parameter_add.html', parameter_data)


# Сохранение параметра
def parameter_save(request, parameter, case):
    parameter.Parameter_Name = request.POST.get("Parameter_" + str(parameter.Parameter_ID))
    # if parameter.Parameter_Name:
    parameter.save(update_fields=['Parameter_Name'])
    parameter.variable.Variable_Name = request.POST.get("Variable_" + str(parameter.variable.Variable_ID)) 
    # if parameter.variable.Variable_Name:
    parameter.variable.save()
    parameter.formula.Formula_Name = request.POST.get("Formula_" + str(parameter.formula.Formula_ID))
    # if parameter.formula.Formula_Name:
    parameter.formula.save()
    for period in case.period_set.all():
        for data in parameter.data_set.all():
            if data.period.Period_ID == period.Period_ID and request.POST.get("Data_" + str(data.Data_ID)):
                data.Data_Value = request.POST.get("Data_" + str(data.Data_ID))
                # if data.Data_Value:
                data.save(update_fields=['Data_Value'])

# Добавление периода в таблице
def period_add_in_table(case):
    period = Period(
        case = case,
        Period_Name = '',
        Period_Sort = sorting_weight_periods(case))
    period.save()
    for section in case.section_set.all():
        for parameter in section.parameter_set.all():
            data = Data(
                parameter = parameter,
                period = period,
                Data_Value = None)
            data.save()

# Добавление периода
# def period_add(request, case_id):
#     case = Case.objects.get(Case_ID = case_id)
#     if request.method == "POST":        
#         form = Create_Period_Form(request.POST, case_id)
#         period = Period(
#             case = case,
#             Period_Name = request.POST.get("Period_"),
#             Period_Sort = sorting_weight_periods(case))
#         period.save()
#         return redirect('cases:case_edit', case.Case_ID)
#     form = Create_Period_Form()
#     period_data = {
#         'form': form,
#         'case': case,
#     }
#     return render(request, 'cases/period_add.html', period_data)

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

# Установка веса для сортировки параметров
def sorting_weight_parameters(case):
    parameters_count = 0
    for section in case.section_set.all():
        parameters = section.parameter_set.all()
        parameters_count += parameters.count()
    return (parameters_count + 1) * 10

# Установка веса для сортировки разделов
def sorting_weight_section(case):
    section = case.section_set.all()
    return (section.count() + 1) * 10

# Установка веса для сортировки периодов
def sorting_weight_periods(case):
    periods = case.period_set.all()
    return (periods.count() + 1) * 10

# Расчет формул
def formula_calculate(request, case):
    formula_error_result = ""
    for section in case.section_set.all():
        for parameter in section.parameter_set.all():
            formula = request.POST.get("Formula_" + str(parameter.formula.Formula_ID))
            if formula and formula_chek(formula):
                formula_save(formula, parameter)
                for data in parameter.data_set.all():
                    formula_result = formula_calc_result(formula, data.period, case)
                    try: 
                        data.Data_Value = formula_result
                        data.save(update_fields=['Data_Value'])
                    except:                 
                        formula_error_result = formula_result
                        data.Data_Value = 0
                        data.save(update_fields=['Data_Value'])
    if formula_error_result:
        return "Переменная не найдена, проверьте выражение " + formula_error_result

# Проверка корректности формул - доделать
def formula_chek(formula):
    return True

# Сохранение формул - переделать под хранение *ID
def formula_save(formula, parameter):
    parameter.formula.Formula_Name = formula
    parameter.formula.save()
    
# Расчет
def formula_calc_result(formula, period, case):
    initial_formula = formula
    for parameter in parameter_in_case(case): #проверяем все параметры в кейсе
        if (formula.find(parameter.variable.Variable_Name) != -1):  # Если переменная найдена, то передаем далее этот параметр
            data = get_data(parameter, period) #получаем значение
            if formula.find("/") != -1 and data == 0: # Проверяем, если в формуле есль деления и значение равно 0 
                return 0 # то возвращаем 0
            else: # иначе, в формуле заменяем переменную на ее значение
                formula = formula.replace(parameter.variable.Variable_Name, str(data))
    try: 
        return round(eval(formula),2) #и возвращаем результат вычислений (eval - считает строку) округленный до 2 цифр
    except: 
        return initial_formula

# Получить значение по параметру и периоду
def get_data(parameter, period):
    for data in parameter.data_set.all():
        if data.period.Period_ID == period.Period_ID:
            if data.Data_Value: # На случай если в поле хранится None
                return data.Data_Value
            else: return 0 # то возвращаем 0

# Проверяем наличие переменной в кейсе - не используется, но надо будет применить в formula_chek
def has_var(case, var_name):
    flag = False
    for section in case.section_set.all():
        for parameter in section.parameter_set.all():
            if (parameter.variable.Variable_Name == var_name):
                flag = True
    return flag

# Пример из тест.py, потом удалю
def get_var(case, var_name):
    for i_var in range(0, len(var_name)): 
        if (Formula_Expression.find(var_name[i_var]) != -1):  # Если переменная найдена
            Formula_Expression = Formula_Expression.replace(var_name[i_var], str(Variable[i_var])) # То перезаписываем ее на цифру - либо на ID 
    # flag = False
    # for section in case.section_set.all():
    #     for parameter in section.parameter_set.all():
    #         if (parameter.variable.Variable_Name == var_name):
    #             flag = True
    return True