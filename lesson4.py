def gcd(a, b):

    while a != 0 and b != 0:

        if a <= b:

            b = b % a

        else:

            a = a % b

    print('Наибольший общий делитель:', a + b)





gcd(30, 18)