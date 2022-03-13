def bathroom():
    print('\nСейчас вы в ванной, куда пойдем? \n1 - спальня \n2 - коридор')
    choice = int(input('Выберите направление: '))
    if choice == 1:
        bedroom()
    elif choice == 2:
        hall()


def bedroom():
    print('\nСейчас вы в спальне, куда пойдем? \n1 - ванна \n2 - коридор')
    choice = int(input('Выберите направление: '))
    if choice == 1:
        bathroom()
    elif choice == 2:
        hall()


def hall():
    print('\nСейчас вы в коридоре, куда пойдем? \n1 - спальня \n2 - ванна \n3 - кухня \n4 - Вы видите непонятную дверь')
    choice = int(input('Выберите направление: '))
    if choice == 1:
        bedroom()
    elif choice == 2:
        bathroom()
    elif choice == 3:
        kitchen()
    elif choice == 4:
        print('\nПоздравляю вы выбрались из квартиры, удчно вам добраться домой')
        endgame()


def kitchen():
    print(
        '\nСейчас вы в кухне, что выберите? \n1 - пойдем в коридор \n2 - вы видите открытое окно \n3 - вы видите кран')
    choice = int(input('Выберите направление: '))
    if choice == 1:
        hall()
    elif choice == 2:
        print('\nВы неудачно высунулись в окно, упали и разбились. Сожалеем')
        endgame()
    elif choice == 3:
        print('\nВы открыли кран, но воды к сожалению нет')
        kitchen()


def endgame():
    print('\nКонец игры')


print(
    'Привет, после клевой вечеринки вы проснулись в незнакомой квартире и вам очень хочется пить и вам нужно найти выход')
bathroom()
