import numpy as np;
EQUATION = '../data/equation.txt'


def lite_to_dict(line):
    print(line)
    left, right = map(lambda x: x.strip(), line.split('='))
    return {
        'left': left,
        'right': int(right)
    }


def map_to_array_left_dict(item):
    left_arr = item['left'].split()

    dict_exp = {}
    res_array = []
    for value in left_arr:
        if value.isdigit():
            dict_exp['coef'] = int(value)
        elif value == '+':
            if 'coef' not in dict_exp:
                dict_exp['coef'] = 1
        elif value == '-':
            if 'coef' not in dict_exp:
                dict_exp['coef'] = 1
            dict_exp['coef'] *= -1
        else:
            if 'coef' not in dict_exp:
                dict_exp['coef'] = 1
            dict_exp['var'] = value
            res_array.append(dict_exp)
            dict_exp = {}
    return res_array


def map_to_array_right(item):
    return item['right']


def sort_place(items):
    items.sort(key=lambda x: x['var'])
    return items


def main():
    file = open(EQUATION, "r")
    lines = file.readlines()

    array_of_dict = list(map(lite_to_dict, lines))

    a_dict = list(map(map_to_array_left_dict, array_of_dict))
    exp_array = [item for sublist in a_dict for item in sublist]
    a_sorted = list(map(sort_place, a_dict))

    a = list(map(lambda x: list(map(lambda y: y['coef'], x)), a_sorted))
    b = list(map(map_to_array_right, array_of_dict))

    res = np.linalg.solve(a, b)
    variables = sorted(list(set(map(lambda x: x['var'], exp_array))))

    string = ''
    for key, value in enumerate(variables):
        string = string + value + ': ' + str(res[key]) + ', '

    print(string)


if __name__ == "__main__":
    main()
