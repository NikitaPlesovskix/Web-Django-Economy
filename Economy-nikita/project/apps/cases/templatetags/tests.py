from array import *
import math

# def is_right_value(first_value, second_value):
#     print(round(first_value, 2))
#     print(round(second_value, 2))
#     return round(first_value, 2) == round(second_value, 2)

def cos(num):
    return math.cos(math.radians(num))
 
 
def sin(num):
    return math.sin(math.radians(num))
 
 
def tg(num):
    return math.tan(math.radians(num))
 
 
def ctg(num):
    return 1 / math.tan(math.radians(num))
 
 
def ln(num):
    return math.log(math.radians(num))

def tests(case_id, var_name):
    # case = Case.objects.get(Case_ID = case_id)
    # flag = False
    # for section in case.section_set.all():
    #     for parameter in section.parameter_set.all():
    #         if (parameter.variable.Variable_Name ==var_name):
    #             flag = True
    # if(flag):
    #     print(1)
    # Исходные данные:
    Formula_Expression = "V1 / V11 ^ V3"
    Variable_Name = ["V1", "V11", "V3"]
    Variable = array('f',[10, 25, 30])

    # Перебор всех переменных
    for i_var in range(0, len(Variable_Name)): 
        if (Formula_Expression.find(Variable_Name[i_var]) != -1):  # Если переменная найдена
            Formula_Expression = Formula_Expression.replace(Variable_Name[i_var], str(Variable[i_var])) # То перезаписываем ее на цифру - либо на ID 

    # Далее уже идет вычисление из строки
    Formula_Expression.split() # Удаляем пробелы
    Formula_Expression = Formula_Expression.replace("^", "**") # Заменяем степени

    return eval(Formula_Expression) # Вычисляем строку


    # strig_pars = strig_pars[:-1].replace(' ', '') 
    # num1 = section_id
    # num2 = 1.016

    # expected = True

    # result = is_right_value(num1, num2)
    # print(expected == result)

    # num1 = 1.12
    # num2 = 1.116

    # expected = True

    # result = is_right_value(num1, num2)

    # print(expected == result)

    # num1 = 1.114
    # num2 = 1.124

    # expected = False

    # result = is_right_value(num1, num2)

    # print(expected == result)


if __name__ == '__main__':
    tests(5, 'V2')
