
import pickledb
import pyxel
import os
from random import randint


pyxel.init(128, 128, title="Idle Factories", fps=60)
pyxel.load("Idle_factories.pyxres")
pyxel.mouse(True)

# ==================== Save ====================

if os.path.exists("sauvegarde.db"):

    # Data recovery
    data = pickledb.load('sauvegarde.db', True)

    # Factories
    factory_lvl_1 = data.get("factory_lvl_1")
    factory_lvl_2 = data.get("factory_lvl_2")
    factory_lvl_3 = data.get("factory_lvl_3")
    factory_lvl_4 = data.get("factory_lvl_4")
    factory_lvl_5 = data.get("factory_lvl_5")
    factory_lvl_6 = data.get("factory_lvl_6")

    # Others data
    money = int(data.get("money"))
    gems = int(data.get("gems"))
    levels = int(data.get("levels"))
    nb_clicks = int(data.get("nb_clicks"))
    next_level = int(data.get("next_level"))
    progression = int(data.get("progression"))

else:
    # Data initialisation

    # Factories
    # Unlocked or not, Price to buy/upgrade, Multiplicator of price to upgrade, Money produced per seconds, Level of factory (max = 30), Position X, Position Y
    factory_lvl_1 = [False, 100, 1.1, 1, 0, 18, 22]
    factory_lvl_2 = [False, 1000, 1.25, 2, 0, 101, 22]
    factory_lvl_3 = [False, 5000, 1.40, 5, 0, 10, 64]
    factory_lvl_4 = [False, 10000, 1.5, 10, 0, 60, 50]
    factory_lvl_5 = [False, 25000, 1.7, 50, 0, 35, 91]
    factory_lvl_6 = [False, 100000, 1.75, 200, 0, 77, 91]

    # Others data
    money = 10
    gems = 5
    levels = 1
    nb_clicks = 0
    next_level = 10
    progression = 0

# ==================== Boost's Part ====================

# Activated, Position X, Position Y
boost_lightning = [False, 73, 81]
x2 = [False, 25, 81]

# Remainings seconds if activated
seconds_lightning = 0
seconds_x2 = 0

# ==================== Others variables ====================
# Position X, Position Y
farm_factory = [42, 46]
shop = [104, 48]
exit_shop = [105, 81]
factories_list = [factory_lvl_1, factory_lvl_2,
                  factory_lvl_3, factory_lvl_4, factory_lvl_5, factory_lvl_6]
statut = "main"


def over():
    """This function checks if the mouse cursor is hovering over one of the factories.
    If so, it returns True and the factory number. If not, it returns False with the factory number (the latter will not be used).

    Returns:
        bool : True if mouse cursor is hovering a factory, False if not.
        int : number of the factory (unused if mouse cursor isn't hovering a factory).
    """
    for nb_factory, factory in enumerate(factories_list):
        if mouse_x > factory[5] and mouse_x < factory[5] + 22 and mouse_y > factory[6] and mouse_y < factory[6] + 22:
            return True, nb_factory

    return False, nb_factory


def factories(money, x2):
    """This function adds the money produced by the different factories to the money already obtained.

    Args:
        money (int): money already obtained.
        x2 (tuple): contain a bool (True if activated, False if not), and the position X and Y in the menu (unused here).

    Returns:
        int: total money owned.
    """
    for factory in factories_list:
        # If factory unlocked
        if factory[0]:
            # If boost activated
            if x2[0]:
                money = money + ((factory[3] * factory[4]) * 2) # Money already obtained + ((money earned when factory is level 1 * level of the factory) * 2 for the boost)
            else:
                money = money + (factory[3] * factory[4]) # Money already obtained + (money earned when factory is level 1 * level of the factory)
    return money


def buy_upgrade_factories(money):
    """This function allows you to buy a factory, or to improve it if you have already bought it before.

    Args:
        money (int): the money is necessary to know if we have enough money to buy/improve the factory or not.

    Returns:
        int: money after bought something or not.
    """
    if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
        hovering, nb_factory = over()
        
        if hovering:
            factory_hovered = factories_list[nb_factory]
            
            if not factory_hovered[0] and money >= factory_hovered[1]:
                
                money = money - factory_hovered[1]
                factory_hovered[1] = int(factory_hovered[1] * factory_hovered[2])
                factory_hovered[0] = True
                factory_hovered[4] = factory_hovered[4] + 1

            elif money >= factory_hovered[1] and factory_hovered[4] < 30:
                
                money = money - factory_hovered[1]
                factory_hovered[1] = int(factory_hovered[1] * factory_hovered[2])
                factory_hovered[4] = factory_hovered[4] + 1
    return money


def manual_money(money, levels, gems, nb_clicks, next_level):

    if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
        if mouse_x > farm_factory[0] and mouse_x < farm_factory[0] + 16 and mouse_y > farm_factory[1] and mouse_y < farm_factory[1] + 16:
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

    elif pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) and mouse_x > exit_shop[0] and mouse_x < exit_shop[0] + 13 and mouse_y > exit_shop[1] and mouse_y < exit_shop[1] + 13:
        statut = "main"

    return boost_lightning, x2, statut, gems

# ____________________________________________________


def update():

    global data, factories_list, money, mouse_x, mouse_y, levels, gems, nb_clicks, next_level, progression, statut, afficher, nb_factory, locked_factories_list, boost_lightning, x2, seconds_lightning, seconds_x2
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

# Save's part (it save the party every seconds)
    if pyxel.frame_count % 60 == 0:
        data = pickledb.load('sauvegarde.db', True)

        # Factories
        data.lcreate('factory_lvl_1')
        data.lcreate('factory_lvl_2')
        data.lcreate('factory_lvl_3')
        data.lcreate('factory_lvl_4')
        data.lcreate('factory_lvl_5')
        data.lcreate('factory_lvl_6')
        data.lextend('factory_lvl_1', factory_lvl_1)
        data.lextend('factory_lvl_2', factory_lvl_2)
        data.lextend('factory_lvl_3', factory_lvl_3)
        data.lextend('factory_lvl_4', factory_lvl_4)
        data.lextend('factory_lvl_5', factory_lvl_5)
        data.lextend('factory_lvl_6', factory_lvl_6)

        # Others data
        data.set('money', str(int(money)))
        data.set('gems', str(int(gems)))
        data.set('levels', str(int(levels)))
        data.set('nb_clicks', str(int(nb_clicks)))
        data.set('next_level', str(int(next_level)))
        data.set('progression', str(int(progression)))

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
