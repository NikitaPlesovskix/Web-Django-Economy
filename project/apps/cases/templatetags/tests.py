

def is_right_value(first_value, second_value):
    print(round(first_value, 2))
    print(round(second_value, 2))
    return round(first_value, 2) == round(second_value, 2)


def is_right_value_tests():
    num1 = section_id
    num2 = 1.016

    expected = True

    result = is_right_value(num1, num2)
    print(expected == result)

    num1 = 1.12
    num2 = 1.116

    expected = True

    result = is_right_value(num1, num2)

    print(expected == result)

    num1 = 1.114
    num2 = 1.124

    expected = False

    result = is_right_value(num1, num2)

    print(expected == result)


if __name__ == '__main__':
    is_right_value_tests()
