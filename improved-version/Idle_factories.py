
import pyxel
import os
from random import randint


pyxel.init(128, 128, title="Idle Factories", fps=60)
pyxel.load("Idle_factories.pyxres")

pyxel.mouse(True)

# unlock or not, price, multiplicator of lvl up, money per sec, lvl of factory, pos x, pos y

statut = "main"

# ==================== Save ====================

data_name_list = ["factory_lvl_1 : ", "factory_lvl_2 : ",
                  "factory_lvl_3 : ", "factory_lvl_4 : ", "factory_lvl_5 : ", "factory_lvl_6 : ", "money : ", "gems : ", "levels : ", "nb_clicks : ", "next_level : "]

if os.path.exists("sauvegarde.txt"):

    with open("sauvegarde.txt", "r") as sauvegarde:
        donnees = [elt.strip() for elt in sauvegarde]
    list_of_factories = []
    for ind in range(6):

        temp = (donnees[ind].replace(data_name_list[ind], "")).split("/")

        if temp[0] == "True":
            temp[0] = True
        else:
            temp[0] = False

        for ind in range(1, 7):
            temp[ind] = float(temp[ind])

        list_of_factories.append(temp)

    factory_lvl_1 = list_of_factories[0]
    factory_lvl_2 = list_of_factories[1]
    factory_lvl_3 = list_of_factories[2]
    factory_lvl_4 = list_of_factories[3]
    factory_lvl_5 = list_of_factories[4]
    factory_lvl_6 = list_of_factories[5]
    money = int(float(donnees[6].replace(data_name_list[6], "")))
    gems = int(donnees[7].replace(data_name_list[7], ""))
    levels = int(donnees[8].replace(data_name_list[8], ""))
    nb_clicks = int(donnees[9].replace(data_name_list[9], ""))
    next_level = int(float(donnees[10].replace(data_name_list[10], "")))
    
else:
    with open("sauvegarde.txt", "w") as sauvegarde:
        sauvegarde.write(
            "factory_lvl_1 : False/100/1.1/1/0/18/22\nfactory_lvl_2 : False/1000/1.25/2/0/101/22\nfactory_lvl_3 : False/5000/1.40/5/0/10/64\n")
        sauvegarde.write(
            "factory_lvl_4 : False/10000/1.5/10/0/60/50\nfactory_lvl_5 : False/25000/1.7/50/0/35/91\nfactory_lvl_6 : False/100000/1.75/200/0/77/91\n")
        sauvegarde.write(
            "money : 10\ngems : 5\nlevels : 1\nnb_clicks : 0\nnext_level : 10")
        
    factory_lvl_1 = [False, 100, 1.1, 1, 0, 18, 22]

    factory_lvl_2 = [False, 1000, 1.25, 2, 0, 101, 22]

    factory_lvl_3 = [False, 5000, 1.40, 5, 0, 10, 64]

    factory_lvl_4 = [False, 10000, 1.5, 10, 0, 60, 50]

    factory_lvl_5 = [False, 25000, 1.7, 50, 0, 35, 91]

    factory_lvl_6 = [False, 100000, 1.75, 200, 0, 77, 91]

    money = 10

    gems = 5

    levels = 1

    nb_clicks = 0

    next_level = 10

    progression = 0

    mouse_x = 0

    mouse_y = 0

factories_list = [factory_lvl_1, factory_lvl_2,
                  factory_lvl_3, factory_lvl_4, factory_lvl_5, factory_lvl_6]

# postion_x, posiition_y
table_craft = [42, 46]

shop = [104, 48]

# ==================== Boost's Part ====================
# Activated/Pos_x/Pos_y
boost_lightning = [False, 73, 81]
x2 = [False, 25, 81]

# Remainings seconds if activated
seconds_lightning = 0
seconds_x2 = 0

# Exit
# Pos_x/Pos_y
exit_pos = [105, 81]


def over():
    for nb_factory, factory in enumerate(factories_list):
        if mouse_x > factory[5] and mouse_x < factory[5] + 22 and mouse_y > factory[6] and mouse_y < factory[6] + 22:
            return True, nb_factory

    return False, nb_factory


def factories(money, x2):

    for factory in factories_list:
        if factory[0]:
            if x2[0]:
                money = money + ((factory[3] * factory[4]) * 2)
            else:
                money = money + (factory[3] * factory[4])
    return money


def buy_upgrade_factories(money):

    if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
        for factory in factories_list:

            if mouse_x > factory[5] and mouse_x < factory[5] + 22 and mouse_y > factory[6] and mouse_y < factory[6] + 22:
                if not factory[0] and money >= factory[1]:
                    money = money - factory[1]
                    factory[1] = int(factory[1] * factory[2])
                    factory[0] = True
                    factory[4] = factory[4] + 1

                elif money >= factory[1] and factory[4] < 30:
                    money = money - factory[1]
                    factory[1] = int(factory[1] * factory[2])
                    factory[4] = factory[4] + 1
    return money


def manual_money(money, levels, gems, nb_clicks, next_level):

    if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
        if mouse_x > table_craft[0] and mouse_x < table_craft[0] + 16 and mouse_y > table_craft[1] and mouse_y < table_craft[1] + 16:
            proba_gems = randint(0, 100)

            if proba_gems < 3:
                gems = gems + 1

            money = money + (1 * levels)
            nb_clicks = nb_clicks + 1
            levels, next_level, nb_clicks = upgrade_levels(
                nb_clicks, levels, next_level)

    return money, levels, gems, nb_clicks, next_level


def locked_factories(factories_list):

    locked_factories_list = []

    for nb_factory, factory in enumerate(factories_list):

        if not factory[0]:
            locked_factories_list.append(nb_factory)

    return locked_factories_list


def upgrade_levels(nb_clicks, levels, next_level):

    if nb_clicks >= next_level:
        levels = levels + 1
        nb_clicks = 0
        next_level = next_level * 1.5

    return levels, next_level, nb_clicks


def crossbar_level(nb_clicks, next_level):

    progression = 50 * nb_clicks/next_level

    return progression


def enter_shop(statut):

    if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) and mouse_x > shop[0] and mouse_x < shop[0] + 24 and mouse_y > shop[1] and mouse_y < shop[1] + 16:
        statut = "shop"

    return statut


def shops(boost_lightning, x2, statut, gems):

    if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) and mouse_x > x2[1] and mouse_x < x2[1] + 13 and mouse_y > x2[2] and mouse_y < x2[2] + 13 and gems >= 10 and not x2[0]:
        x2[0] = True
        gems = gems - 10

    elif pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) and mouse_x > boost_lightning[1] and mouse_x < boost_lightning[1] + 13 and mouse_y > boost_lightning[2] and mouse_y < boost_lightning[2] + 13 and gems >= 10 and not boost_lightning[0]:
        boost_lightning[0] = True
        gems = gems - 10

    elif pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) and mouse_x > exit_pos[0] and mouse_x < exit_pos[0] + 13 and mouse_y > exit_pos[1] and mouse_y < exit_pos[1] + 13:
        statut = "main"

    return boost_lightning, x2, statut, gems

# ____________________________________________________


def update():

    global factories_list, money, mouse_x, mouse_y, levels, gems, nb_clicks, next_level, progression, statut, afficher, nb_factory, locked_factories_list, boost_lightning, x2, seconds_lightning, seconds_x2
    mouse_x = pyxel.mouse_x
    mouse_y = pyxel.mouse_y

    if statut == "main":
        money = buy_upgrade_factories(money)
        money, levels, gems, nb_clicks, next_level = manual_money(
            money, levels, gems, nb_clicks, next_level)
        progression = crossbar_level(nb_clicks, next_level)
        statut = enter_shop(statut)
        afficher, nb_factory = over()
        locked_factories_list = locked_factories(factories_list)

    elif statut == "shop":
        boost_lightning, x2, statut, gems = shops(
            boost_lightning, x2, statut, gems)

    # Countdown in seconds of boosts if activated

    if x2[0]:
        if seconds_x2 < 5:
            if pyxel.frame_count % 60 == 0:
                seconds_x2 = seconds_x2 + 1
        else:
            x2[0] = False
            seconds_x2 = 0

    if boost_lightning[0]:
        if pyxel.frame_count % 30 == 0:
            money = factories(money, x2)
        if seconds_lightning < 15:
            if pyxel.frame_count % 60 == 0:
                seconds_lightning = seconds_lightning + 1
        else:
            boost_lightning[0] = False
            seconds_lightning = 0

    else:
        if pyxel.frame_count % 60 == 0:
            money = factories(money, x2)

    if pyxel.frame_count % 60 == 0:
        with open("sauvegarde.txt", "w") as sauvegarde:
            for ind1, data in enumerate(data_name_list):
                if ind1 < 6:
                    sauvegarde.write(data)
                    for ind2 in range(len(factories_list[ind1])-1):
                        sauvegarde.write(str(factories_list[ind1][ind2]))
                        sauvegarde.write("/")
                    sauvegarde.write(str(factories_list[ind1][len(factories_list)]))
                    sauvegarde.write("\n")
            sauvegarde.write(data_name_list[6])
            sauvegarde.write(str(money))
            sauvegarde.write("\n")
            sauvegarde.write(data_name_list[7])
            sauvegarde.write(str(gems))
            sauvegarde.write("\n")
            sauvegarde.write(data_name_list[8])
            sauvegarde.write(str(levels))
            sauvegarde.write("\n")
            sauvegarde.write(data_name_list[9])
            sauvegarde.write(str(nb_clicks))
            sauvegarde.write("\n")
            sauvegarde.write(data_name_list[10])
            sauvegarde.write(str(next_level))
            sauvegarde.write("\n")
    return None


# ____________________________________________________
def draw():
    pyxel.cls(0)
    


    if statut == "main":
        pyxel.blt(0, 0, 1, 0, 0, 128, 128)

        # crossbar
        pyxel.rectb(70, 17, 52, 3, 13)
        pyxel.rect(71, 18, progression, 1, 11)

        # levels factories
        if afficher and factories_list[nb_factory][0]:

            pyxel.circ(factories_list[nb_factory][5] + 11,
                       factories_list[nb_factory][6] + 13, 8, 13)
            pyxel.circ(factories_list[nb_factory][5] + 11,
                       factories_list[nb_factory][6] + 12, 8, 7)

            if factories_list[nb_factory][4] < 10:

                if money >= factories_list[nb_factory][1]:
                    pyxel.text(factories_list[nb_factory][5] + 10, factories_list[nb_factory]
                               [6] + 10, str(int(factories_list[nb_factory][4])), 11)
                else:
                    pyxel.text(factories_list[nb_factory][5] + 10, factories_list[nb_factory]
                               [6] + 10, str(int(factories_list[nb_factory][4])), 0)

            else:
                if money >= factories_list[nb_factory][1]:
                    pyxel.text(factories_list[nb_factory][5] + 8, factories_list[nb_factory]
                               [6] + 10, str(int(factories_list[nb_factory][4])), 11)
                else:
                    pyxel.text(factories_list[nb_factory][5] + 8, factories_list[nb_factory]
                               [6] + 10, str(int(factories_list[nb_factory][4])), 0)

        elif afficher and not factories_list[nb_factory][0] and factories_list[nb_factory][1] > money:

            pyxel.circ(factories_list[nb_factory][5] + 11,
                       factories_list[nb_factory][6] + 13, 8, 13)
            pyxel.circ(factories_list[nb_factory][5] + 11,
                       factories_list[nb_factory][6] + 12, 8, 7)
            pyxel.blt(factories_list[nb_factory][5] + 8,
                      factories_list[nb_factory][6] + 8, 1, 129, 0, 7, 9)

        elif afficher and not factories_list[nb_factory][0] and factories_list[nb_factory][1] <= money:

            pyxel.circ(factories_list[nb_factory][5] + 11,
                       factories_list[nb_factory][6] + 13, 8, 13)
            pyxel.circ(factories_list[nb_factory][5] + 11,
                       factories_list[nb_factory][6] + 12, 8, 7)
            pyxel.blt(factories_list[nb_factory][5] + 8,
                      factories_list[nb_factory][6] + 8, 1, 129, 9, 7, 9)
    elif statut == "shop":

        pyxel.blt(0, 0, 1, 0, 0, 128, 128)
        pyxel.blt(0, 0, 2, 0, 8, 128, 120)
        # crossbar
        pyxel.rectb(70, 12, 52, 3, 13)
        pyxel.rect(71, 13, progression, 1, 11)

    # stats
    pyxel.text(2, 2, "Money : " + str(int(money)), 2)
    pyxel.text(2, 9, "Gems : " + str(gems), 2)
    pyxel.text(75, 4, "Levels : " + str(levels), 2)
    return None


pyxel.run(update, draw)