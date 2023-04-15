from django import template
# # from django.contrib.auth.models import User
import os

register = template.Library()


# @register.filter(name='is_validate_param')
# def is_validate_param(Param):
#     users = []
#     for user in User.objects.all():
#         if user.groups.filter(name='Преподаватель').exists() and user.first_name != '':
#             users.append(user)
#     for user in users:
#         if user.first_name in Param.Param_Name\
#                 or Param.section.Name_Section[:10] in Param.Param_Name[:10]\
#                 or "Уральская сталь" in Param.Param_Name \
#                 or "Контрагент 1" in Param.Param_Name:
#             return False
#     return True


@register.filter(name='has_var')
def has_var(case, var_name):
    flag = False
    for section in case.section_set.all():
        for parameter in section.parameter_set.all():
            if (parameter.variable.Variable_Name == var_name):
                flag = True
    return flag


@register.filter(name='get_var')
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


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name='default_section') 
def default_section(case):
    for section in case.section_set.all():
        if section.Section_Name == "__default":
            return section.Section_ID
        
        
@register.filter(name='is_default_section') 
def is_default_section(section):
    if section.Section_Name == "__default":
        return True
        

@register.filter(name='parameter_in_section') 
def parameter_in_section(section, parameter):
    flag = False
    for parameters in section.parameter_set.all():
        if parameters == parameter:
            flag = True 
            return flag
        else: flag = False
    return flag


@register.filter(name='is_right_value')
def is_right_value(first_value, second_value):
    if (round(abs(first_value - second_value), 3) <= 0.005):
        return True
    else:
        return False
        # return round(first_value, round_count) == round(second_value, round_count) or first_value == round(second_value, round_count) or round(first_value, round_count) == second_value


@register.filter(name='has_group_two')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).order_by(group_name).exists()


@register.filter(name='has_type')
def has_type(first, second):
    return first.description == second


@register.filter(name='dev')
def has_group(value1, value2):
    return int((value1 / value2) * 100)


@register.filter(name='HasThisChoice')
def has_group(section, Description):
    return section.caseparam_set.last().choice.description == Description


@register.filter(name='HasThisChoiceId')
def has_group(section, Section_id):
    # print( vars(section))
    # print( section_id)
    return section.caseparam_set.last().choice.section_id == Section_id


@register.filter(name='Bigger')
def Bigger(first, second):
    return first < second


@register.filter(name='GetResultForTeacher') #Проверка преподавателя для подсветки ячейки
def GetResult(section, Year):
    caseparams = section.caseparam_set.all()
    result = 100 * (caseparams.count() - 2 - SumDateParamForPrep(section.caseparam_set.all(), Year)) / (
            caseparams.count() - 2)
    if result >= 30:
        return False
    return True


@register.filter(name='GetResultForStudent') #Проверка студента для подсветки ячейки
def GetResult(section, Year):
    caseparams = section.caseparam_set.all()
    result = 100 * (caseparams.count() - 2 - SumDateParamForStudent(section.caseparam_set.all(), Year)) / (
            caseparams.count() - 2)
    if result >= 30:
        return False
    return True


@register.filter(name='GetResultForTeacherOrStudent') #Проверка результирующей оценки преподавателя/студента для подсветки ячейки
def SumDateParamForTest(section, Year):
    caseparams = section.caseparam_set.all()
    x = True
    for caseparam in caseparams:
        if caseparam.Param_Name != 'Итого' and caseparam.Param_Name != 'Результирующая оценка':
            for dateparam in caseparam.dateparam_set.all():
                if dateparam.Param_Period.year == int(Year):
                    if dateparam.Param_Undang_Prep != dateparam.Param_Undang: #Сравниваем ответы преподавателя и ученика
                        x = False #И если есть хотябы один неправильный ответ - то выходим их цикла
                        break 
    return x


@register.filter(name='SumDateParamForPrep') #Подсчет ответов преподавателя
def SumDateParamForPrep(caseparams, Year):
    sum = 0
    for caseparam in caseparams:
        if caseparam.Param_Name != 'Итого' and caseparam.Param_Name != 'Результирующая оценка':
            for dateparam in caseparam.dateparam_set.all():
                if dateparam.Param_Period.year == int(Year):
                    if dateparam.Param_Undang_Prep:
                        sum = sum + 1
    return sum


@register.filter(name='SumDateParamForStudent') #Подсчет ответов студента
def SumDateParamForStudent(caseparams, Year):
    sum = 0
    for caseparam in caseparams:
        if caseparam.Param_Name != 'Итого' and caseparam.Param_Name != 'Результирующая оценка':
            for dateparam in caseparam.dateparam_set.all():
                if dateparam.Param_Period.year == int(Year):
                    if dateparam.Param_Undang:
                        sum = sum + 1
    return sum


@register.filter(name='SumDateParamDangForPrep')
def SumDateParamDangForPrep(caseparams, Year):
    sum = 0
    for caseparam in caseparams:
        if caseparam.Param_Name != 'Итого' and caseparam.Param_Name != 'Результирующая оценка':
            for dateparam in caseparam.dateparam_set.all():
                if dateparam.Param_Period.year == int(Year):
                    if not dateparam.Param_Undang_Prep:
                        sum = sum + 1
    return sum


@register.filter(name='SumDateParamDangForStudent')
def SumDateParamDangForStudent(caseparams, Year):
    sum = 0
    for caseparam in caseparams:
        if caseparam.Param_Name != 'Итого' and caseparam.Param_Name != 'Результирующая оценка':
            for dateparam in caseparam.dateparam_set.all():
                if dateparam.Param_Period.year == int(Year):
                    if not dateparam.Param_Undang:
                        sum = sum + 1
    return sum


@register.filter(name='minus')
def minus(first, second):
    return first - second


@register.filter(name='GetId')
def values(item):
    return item.id


@register.filter(name='Get_Name_Section')
def values(section):
    return section.Name_Section


@register.filter(name='scoreForTeacher')
def scoreForTeacher(section, nameAge):
    sum = 0
    for caseparam in section.caseparam_set.all():
        if caseparam.Param_Name == 'Итого баллов':
            for dateparam in caseparam.dateparam_set.all():
                if dateparam.Param_Period.year == nameAge:
                    sum += dateparam.Param_Value;                    
    if sum > 2:
        return "Высокий"
    elif sum == 2:
        return "Средний"
    else:
        return "Низкий"


@register.filter(name='GetCase')
def GetCase(Jobs, NameCase):
    try:
        print(Jobs)
        if Jobs:
            job = Jobs.filter(Job_Title=NameCase).last()
        else:
            return None
        if job != None:
            return job.Job_Param.Case
    except:
        return None
    return None


@register.filter(name='Is_evaluated')
def Is_evaluated(Case):
    if Case:
        params_job = Case.jobparam_set.all()
        if params_job:
            jobs = params_job.first().job_set.all()
            if jobs:
                return jobs.first().Job_is_evaluated
    return None


@register.filter(name='scoreForStudent')
def scoreForStudent(section, nameAge):
    sum = 0
    for caseparam in section.caseparam_set.all():
        if caseparam.Param_Name == 'Итого баллов':
            for dateparam in caseparam.dateparam_set.all():
                if dateparam.Param_Period.year == nameAge:
                    sum += dateparam.Param_UserValue

    if sum > 2:
        return "Высокий"
    elif sum == 2:
        return "Средний"
    else:
        return "Низкий"


@register.filter(name='replace')
def values(item):
    return str(item).replace(',', '.')


# @register.filter(name='GetDate')
# def GetDate(case):
#     for caseparam in case.caseparam_set.all():
#         if caseparam.dateparam_set.count() != 0:
#             return caseparam.dateparam_set.all()
#     return None


@register.filter(name='GetDate')
def GetDate(section):
    for caseparam in section.caseparam_set.all():
        if caseparam.dateparam_set.count() != 0:
            return caseparam.dateparam_set.all()
    return None


@register.filter(name='getAfter')
def getAfter(request):
    return request.META.get('HTTP_REFERER')


@register.filter(name='getMax')
def getMax(items, name):
    return items.order_by(name).last()


@register.filter(name='getMin')
def getMin(items, name):
    return items.order_by(name).first()


@register.filter(name='getParam_Value')
def getParam_Value(item):
    return item.Param_Value


@register.filter(name='getParam_UserValue')
def getParam_UserValue(item):
    return item.Param_UserValue


@register.filter()
def values(items, attr_name):
    return [getattr(i, attr_name) for i in items]


@register.filter()
def distinct(items):
    return set(items)


@register.filter()
def qs_distinct(qs, field_names):
    return qs.distinct(field_names)


@register.filter(name='sort')
def sort(user, group_name):
    return user.order_by(group_name)


@register.filter(name='printAll')
def printAll(items):
    string = ' '
    for item in items:
        string = string + str(item) + ' '
    return string


@register.filter(name='sortOnYear')
def sortOnYear(user, group_name):
    return user.order_by('Year')


@register.filter(name='getEmpty')
def getEmpty(items):
    for item in items:
        if item.dateparam_set.count() == 0:
            return item
    return None


@register.filter(name='getSection')
def getSection(item):
    string = ' '
    for ch in item.choice.all():
        string += ch.description + ' '
    return string


# @register.filter(name='getChoice')
# def getChoices(item):
#     return item.choice


@register.filter(name='getname')
def getname(self):
    return os.path.basename(self.file.name)


@register.filter(name='get')
def get(collection, name):
    return collection.filter(Param_Name=name)
