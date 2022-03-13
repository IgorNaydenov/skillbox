import random


def rock_paper_scissors():
    print('\nСыграем в КНБ \n1 - камень \n2 - ножницы \n3 - бумага')
    player = int(input('Сделайте выбор: '))
    comp = random.randint(1, 3)
    print('Выбор компьютера -', comp)
    if player == comp:
        print('Ничия')
    elif (player == 1 and comp == 2) or (player == 2 and comp == 3) or (player == 3 and comp == 1):
        print('Победил игрок')
    else:
        print('Победил компьютер')


def guess_the_number():
    num = random.randint(1, 100)
    print('\nВам загадали число от 1 до 100, попробуйте отгадать')
    count_attempts = 0
    while True:
        num1 = int(input('введите число: '))
        count_attempts += 1
        if num1 == num:
            print('Поздравляю вы угадали, число попыток:', count_attempts)
            break
        elif num1 > num:
            print('Число больше, чем нужно. Попробуйте ещё раз!')
        else:
            print('Число меньше, чем нужно. Попробуйте ещё раз!')


def mainMenu():
    while True:
        print('\n1 - Игра "Камень, ножницы, бумага" \n2 - Игра "Угадай число" \n0 - Выход')
        choice = int(input('Выберите пункт: '))
        if choice == 1:
            rock_paper_scissors()
        elif choice == 2:
            guess_the_number()
        elif choice == 0:
            break
        else:
            print('Ошибка ввода')


mainMenu()