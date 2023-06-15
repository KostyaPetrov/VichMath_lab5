import math
import os
import matplotlib.pyplot as plt


def main():
    j = 0
    while j == 0:
        print(
            'Введите цифру 1, если хотите ввести данные с консоли. Введите 2, если хотите прочитать данные из файла.\n '
            'Введите 3, если хотите выбрать функцию')
        try:
            num_read = int(input())
            if num_read != 1 and num_read != 2 and num_read != 3:
                print("Вы должны ввести число 1, 2 или 3 в зависимости от способа чтения данных")
            else:
                j = 1
        except ValueError:
            print("Вы должны ввести число 1, 2 или 3")

    list_x, list_y, point = read_data(num_read)

    lagrange(list_x, list_y, point)

    gauss(list_x, list_y, int(len(list_x)), point)

    drow_data(list_x, list_y)

def drow_data(x, y):
    plt.scatter(x,y, label='Исходные данные')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid()
    plt.title('Функции интерпрояции')
    plt.plot(x,y, label='Заданая функция')

def lagrange(x, y, point):
    result = 0

    n=int(len(x))
    for i in range(0, n):
        numerator = 1
        denominator=1
        for j in range(0,n-1):
            if j!=i:
                numerator*=(point-x[j])
                denominator*=(x[i]-x[j])
        numerator*=y[i]
        result+=(numerator/denominator)

    print("Лагранж:")
    print(result)

def gauss(x, y, n, point):
    print("Гаусс:")
    check_points, hope = equally_spaced(x)
    if len(x)%2 == 0:
        print("Количество точек должно быть нечетным")
    elif not check_points:
        print("Точки должны быть равностоящими")
    else:

        center = (n - 1) // 2

        a = x[center]
        t = round((point - a) / hope,2)

        if point > a:
            x_more_a(x, y, n, t)
        elif point < a:
            x_less_a(x, y, n, t)
        else:
            print("Результат интерполяции методом Гаусса равен", y[center])


def find_finite_differences(x,y,n):
    finite_differences = []
    for i in range(0, len(x)):
        finite_differences.append(x[i])
    for i in range(0, len(x)):
        finite_differences.append(y[i])
    k=n
    for i in range(n - 1, -1, -1):
        for j in range(0,i):
            a=finite_differences[len(finite_differences) - k + 1]
            b=finite_differences[len(finite_differences) - k]
            delt_y= a - b
            finite_differences.append(delt_y)
        k=k-1

    print("| i | x | y | Δy ", end="|")
    for i in range(2, n):
        print(" Δy ^ ", i, " ", end="|")
    print()

    for i in range(0, n):
        print(" ",i, end="  ")
        k=n


        print(finite_differences[i],end="   ")
        print(finite_differences[n + i], end="   ")
        h = n + i + k
        for j in range(n-i-1, 0, -1):

            print(finite_differences[h],end="   ")
            k=k-1
            h+=k
        print()

    return finite_differences

def x_more_a(x, y, n, t):
    table=find_finite_differences(x,y,n)
    result=table[n+(n-1)//2]
    numerator=1
    h=int((n-5)/2)
    k=6+4*h
    start_position_first=int(2*n+(n-1)/2)
    start_position_second=start_position_first+n-2
    for i in range(1,n+1):
        numerator*=(t+(i-1))
        if (i-1)!=0:
            result += (numerator * table[start_position_first + (k - 4 * (i - 2))]) / math.factorial(2 * i - 1)
        else:
            result += (numerator * table[start_position_first]) / math.factorial(2 * i - 1)


        numerator*=(t-i)
        if (i-1)!=0:
            result += (numerator * table[start_position_second + (k - 2 - 4 * (i - 2))]) / math.factorial(2 * i)
        else:
            result += (numerator * table[start_position_second]) / math.factorial(2 * i)



    print("Результат интерполяции методом Гаусса равен", result)

def x_less_a(x, y, n, t):
    table = find_finite_differences(x, y, n)
    result = table[n + (n - 1) // 2]
    # print("t=",t)
    # print("y0=",result)
    numerator = 1

    h = int((n - 5) / 2)
    k = 6 + 4 * h
    start_position_first = int(2 * n + (n - 1) / 2 - 1)
    start_position_second = start_position_first + n - 2
    for i in range(1, n //2+1):
        numerator *= (t - (i - 1))
        # print("Числитель при первом слогаемом y"+ str(i-2)+" = ", numerator)
        if (i - 1) != 0:
            # yyy=table[start_position_first + (k - 4 * (i - 2))]
            # fak=math.factorial(2 * i - 1)
            result += (numerator * table[start_position_first + (k - 4 * (i - 2))]) / math.factorial(2 * i - 1)
            # print("delt y"+str(i-i*2)+"=", yyy)
            # print("factorial = ", fak)
        else:
            result += (numerator * table[start_position_first]) / math.factorial(2 * i - 1)
            # print("dy-1=", result)
            # print("fact=",math.factorial(2 * i - 1))

        numerator *= (t + i)
        # print("Числитель при втором слогаемом y" + str(i - 2*i) + " = ", numerator)
        if (i - 1) != 0:
            # yyy =table[start_position_second + (k - 2 - 4 * (i - 2))]
            # fak=math.factorial(2 * i)
            result += (numerator * table[start_position_second + (k - 2 - 4 * (i - 2))]) / math.factorial(2 * i)
            # print("delt y" + str(i - i * 2) + "=", yyy)
            # print("factorial = ", fak)

        else:
            result += (numerator * table[start_position_second]) / math.factorial(2 * i)
            # print("d2y0-1=", table[start_position_second])
            # print("fact=",math.factorial(2 * i))
    print("Результат интерполяции методом Гаусса равен", result)




def equally_spaced(x):
    check=True
    h=abs(x[1]-x[0])
    for i in range(1,len(x)-1):
        ras=abs(x[i+1]-x[i])
        if  round(ras,2)!= h:
            check=False
    return check, h

def read_data(type):
    if type == 1:
        j = 0
        while j != 1:
            j = 1
            print("Введите иксы через пробел:")
            line_x = input()
            line_x = line_x.replace(",", ".")

            print("Введите игрики через пробел:")
            line_y = input()
            line_y = line_y.replace(",", ".")

            line_x.strip()
            list_str_x = line_x.split()
            list_x = []

            coordinate = 0.0
            for i in range(0, len(list_str_x)):

                try:
                    coordinate = float(list_str_x[i])
                    if list_x.__contains__(coordinate):
                        j=0
                        print("Значения x должны быть уникальными")
                        break
                    list_x.append(coordinate)
                except ValueError:
                    print("Значения x должны быть числами")
                    j = 0
                    break

            line_y.strip()
            list_str_y = line_y.split()
            list_y = []
            for i in range(0, len(list_str_y)):
                try:
                    coordinate = float(list_str_y[i])
                    if list_y.__contains__(coordinate):
                        j=0
                        print("Значения y должны быть уникальными")
                        break
                    list_y.append(coordinate)
                except ValueError:
                    print("Значения y должны быть числами")
                    j = 0
                    break

            if len(list_str_x) != len(list_str_y):
                print("Количество значений x должно быть равно количеству значений y")
                j = 0

        j = 0
        while j != 1:
            print("Введите точку, в которой необходимо найти приближенное значние функции:")

            string_point = str(input())
            try:
                point = float(string_point)
                j = 1
            except ValueError:
                print("Введенное значение должно быть числом")
        return list_x, list_y, point
    elif type == 2:
        j = 0
        while j != 1:
            j = 1
            path = input('\nВведите путь до файла: ').strip()
            while not (os.path.isfile(path) and os.path.getsize(path) > 0):
                print('Файла не существует или он пустой')
                path = input('Повторите ввод: ').strip()

            with open(path, 'r') as file:

                file_line = file.readline()
                file_line = file_line.replace(",", ".")

                list_str_x = file_line.split()
                list_x = []
                coordinate = 0.0
                for i in range(0, len(list_str_x)):

                    try:
                        coordinate = float(list_str_x[i])
                        if list_x.__contains__(coordinate):
                            j = 0
                            print("Значения x должны быть уникальными")
                            break

                        list_x.append(coordinate)
                    except ValueError:
                        print("Значения x должны быть числами. Измените данные в файле или выберите другой файл")
                        j = 0
                        break

                file_line = file.readline()
                file_line = file_line.replace(",", ".")

                list_str_y = file_line.split()
                list_y = []
                for i in range(0, len(list_str_y)):

                    try:
                        coordinate = float(list_str_y[i])
                        if list_y.__contains__(coordinate):
                            j = 0
                            print("Значения y должны быть уникальными")
                            break
                        list_y.append(coordinate)
                    except ValueError:
                        print("Значения x должны быть числами. Измените данные в файле или выберите другой файл")
                        j = 0
                        break

                file_line = file.readline()
                file_line = file_line.replace(",", ".")
                try:
                    point = float(file_line)
                    j = 1
                except ValueError:
                    print("Введенное значение должно быть числом. Измените данные в файле или выберите другой файл")
        return list_x, list_y, point
    else:

        print("Выберите одно из уравнения и введите соответствующий номер:")
        print("1: x^2+2x+3")
        print("2: ln(x)+25x^2")
        print("3: 3^(x+5)")

        j = 0
        while j != 1:
            j = 1
            num_equation_str = input()

            if num_equation_str.isnumeric() == False:
                print("Вы должны ввести целое число")
                print("Повторите ввод:")
                j = 0
            else:
                num_equation=int(num_equation_str)
                if num_equation != 1 and num_equation != 2 and num_equation != 3:
                    j = 0
                    print("Вы должны ввести номер уравнения соответственно 1, 2 или 3")
                    print("Повторите ввод:")

        j=0
        while j!=1:
            j=1
            print("Введите через пробел границы, в которых будет осуществляться поиск точек:")
            str_borders = input()
            str_borders = str_borders.replace(",", ".")
            str_borders.strip()
            low_border_str = str_borders.split()[0]
            height_border_str = str_borders.split()[1]

            try:
                low_border=float(low_border_str)
            except ValueError:
                print("Нижняя граница интервала не является числом")
                j=0


            try:
                height_border = float(height_border_str)
            except ValueError:
                print("Верхняя граница интервала не является числом")
                j=0

            if j==0:
                print("Повторите ввод:")


        j=0
        while j!=1:
            j=1
            print("Введите количество точек:")
            num_points_str = str(input())
            list_x=[]
            list_y=[]
            if num_points_str.isnumeric() == True:
                num_points=int(num_points_str)
                if num_points>1:
                    list_x, list_y = find_points(low_border, height_border, num_points, num_equation)
                else:
                    print("Точек не может быть меньше двух")
                    j=0
            else:
                print("Вы должны ввести число")
                j=0


        j = 0
        while j != 1:
            print("Введите точку, в которой необходимо найти приближенное значние функции:")

            string_point = str(input())
            try:
                point = float(string_point)
                j = 1
            except ValueError:
                print("Введенное значение должно быть числом")
        return list_x, list_y, point


def find_points(low, height, num, func):
    h = abs(height - low) / (num - 1)
    x=[]
    y=[]
    current=low
    f=get_function(func)
    for i in range(0, num):
        x.append(current)
        y.append(f(current))
        current+=h

    return x,y
def get_function(num):
    if num == 1:
        return lambda x: x ** 2 + 2 * x + 3
    elif num == 2:
        return lambda x: math.log(x)+25 * x ** 2
    elif num == 3:
        return lambda x: 3 ** (x+5)
    else:
        return None

main()

# C:\\Users\\Kostya\\Desktop\\ITMO\\ITMO_4sem\\VichMath\\file.txt