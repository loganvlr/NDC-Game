
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
    factories_list = data.get("factories_list")

    factory_lvl_1 = factories_list[0]
    factory_lvl_2 = factories_list[1]
    factory_lvl_3 = factories_list[2]
    factory_lvl_4 = factories_list[3]
    factory_lvl_5 = factories_list[4]
    factory_lvl_6 = factories_list[5]

    # Others data

    others_data_list = data.get("others_data_list")
    money = int(others_data_list[0])
    gems = int(others_data_list[1])
    levels = int(others_data_list[2])
    nb_clicks = int(others_data_list[3])
    next_level = int(others_data_list[4])
    progression = int(others_data_list[5])

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
status = "main"


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
            
            # If the factory is not unlocked
            if not factory_hovered[0] and money >= factory_hovered[1]:
                factory_hovered[0] = True

            if money >= factory_hovered[1]:
                money = money - factory_hovered[1]
                
                # Increases the cost of the improvement
                factory_hovered[1] = int(factory_hovered[1] * factory_hovered[2])
                
                # Increase the level of the factory
                factory_hovered[4] = factory_hovered[4] + 1
    return money


def manual_money(money, levels, gems, nb_clicks, next_level):
    """This function allows you to manage the money farm with mouse clicks on the farm factory, the levels up, and gems generation too.

    Args:
        money (int): we take the variable money to add the generated money to it.
        levels (int): to level up.
        gems (int): for the random generation of gems.
        nb_clicks (int): number of clicks made since the beginning of the last level.
        next_level (int): number of clicks needed to next level.

    Returns:
        int: to update all the variables imported in this function.
    """
    if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
        if mouse_x > farm_factory[0] and mouse_x < farm_factory[0] + 16 and mouse_y > farm_factory[1] and mouse_y < farm_factory[1] + 16:
            
            # 5% of chance to get a gem on click
            proba_gems = randint(0, 100)
            if proba_gems < 5:
                gems = gems + 1

            # Per exemple, if level 5, then 5 of money earned
            money = money + (1 * levels)
            
            nb_clicks = nb_clicks + 1
            levels, next_level, nb_clicks = upgrade_levels(
                nb_clicks, levels, next_level)

    return money, levels, gems, nb_clicks, next_level


def upgrade_levels(nb_clicks, levels, next_level):
    """This function allows to detect if the upper level is reached or not.

    Args:
        nb_clicks (int): number of clicks made since the beginning of the last level.
        levels (int): to level up.
        next_level (int): number of clicks needed to next level.

    Returns:
        int: to update all the variables imported in this function.
    """
    if nb_clicks >= next_level:
        levels = levels + 1
        nb_clicks = 0
        
        # The number of clicks needed to reach the next level increase that the experience is more difficult
        next_level = next_level * 1.2

    return levels, next_level, nb_clicks


def level_bar(nb_clicks, next_level):
    """This function is intended to set the display of the level bar.

    Args:
        nb_clicks (int): number of clicks made since the beginning of the last level.
        next_level (int): number of clicks needed to next level.

    Returns:
        int: a value to 0 to 50 for show the progression of the level
    """
    # 50 is the numebr of pixel of level bar display
    progression = 50 * nb_clicks/next_level

    return progression


def enter_shop(status):
    """This function detect when a click is made on the shop. If yes, we set status to "shop" to activate the shop display, all the shop function, etc.

    Args:
        status (str): actual status, where we are. 

    Returns:
        str: the status shop if clicked, actual status if not
    """
    if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) and mouse_x > shop[0] and mouse_x < shop[0] + 24 and mouse_y > shop[1] and mouse_y < shop[1] + 16:
        status = "shop"

    return status


def shops(boost_lightning, x2, status, gems):
    """This function is activated when the status is set on "shop". We can buy some boosts, or leave the shop.

    Args:
        boost_lightning (tuple): contain a bool (True if activated, False if not), and the position X and Y in the menu.
        x2 (tuple): contain a bool (True if activated, False if not), and the position X and Y in the menu.
        status (str): actual status, where we are.
        gems (int): to verify if we have enought gems to buy some boosts

    Returns:
        tuple, tuple, str, int: to update all the variables imported in this function.
    """
    if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) and mouse_x > x2[1] and mouse_x < x2[1] + 13 and mouse_y > x2[2] and mouse_y < x2[2] + 13 and gems >= 10 and not x2[0]:
        x2[0] = True
        gems = gems - 10

    elif pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) and mouse_x > boost_lightning[1] and mouse_x < boost_lightning[1] + 13 and mouse_y > boost_lightning[2] and mouse_y < boost_lightning[2] + 13 and gems >= 10 and not boost_lightning[0]:
        boost_lightning[0] = True
        gems = gems - 10

    elif pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) and mouse_x > exit_shop[0] and mouse_x < exit_shop[0] + 13 and mouse_y > exit_shop[1] and mouse_y < exit_shop[1] + 13:
        status = "main"

    return boost_lightning, x2, status, gems

# ==================== Upgate functions (Pyxel package) ====================

def update():

    global data, factories_list, money, mouse_x, mouse_y, levels, gems, nb_clicks, next_level, progression, status, show, nb_factory, boost_lightning, x2, seconds_lightning, seconds_x2
    mouse_x = pyxel.mouse_x
    mouse_y = pyxel.mouse_y

    if status == "main":
        money = buy_upgrade_factories(money)
        money, levels, gems, nb_clicks, next_level = manual_money(
            money, levels, gems, nb_clicks, next_level)
        progression = level_bar(nb_clicks, next_level)
        status = enter_shop(status)
        show, nb_factory = over()

    elif status == "shop":
        boost_lightning, x2, status, gems = shops(
            boost_lightning, x2, status, gems)

    # Countdown in seconds of boosts if activated

    if x2[0]:
        
        # 5 seconds of boost
        if seconds_x2 < 5:
            if pyxel.frame_count % 60 == 0:
                seconds_x2 = seconds_x2 + 1

        else:
            x2[0] = False
            seconds_x2 = 0

    if boost_lightning[0]:
        # Divides by 2 the time necessary for the production of money by the factories
        if pyxel.frame_count % 30 == 0:
            money = factories(money, x2)
            
        # 15 seconds of boost
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
    if pyxel.frame_count % 300 == 0:
        data = pickledb.load('sauvegarde.db', True)

        # Factories
        factories_list = [factory_lvl_1, factory_lvl_2, factory_lvl_3, factory_lvl_4, factory_lvl_5, factory_lvl_6]
        data.set('factories_list',factories_list)

        # Others data
        others_data_list = [str(int(money)), str(int(gems)), str(int(levels)), str(int(nb_clicks)), str(int(next_level)), str(int(progression))]
        data.set('others_data_list',others_data_list)
    return None


# ____________________________________________________
def draw():
    # Erase all the display
    pyxel.cls(0)

    # Display the map and all the informations (all factories informations when hovered)
    if status == "main":
        pyxel.blt(0, 0, 1, 0, 0, 128, 128)

        # Level bar
        pyxel.rectb(70, 17, 52, 3, 13)
        pyxel.rect(71, 18, progression, 1, 11)

        # Factory levels if hovered and factory unlocked
        if show and factories_list[nb_factory][0]:

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

        # Padlock locked if factory hovered but factory is locked and not enought money to buy it
        elif show and not factories_list[nb_factory][0] and factories_list[nb_factory][1] > money:

            pyxel.circ(factories_list[nb_factory][5] + 11,
                       factories_list[nb_factory][6] + 13, 8, 13)
            pyxel.circ(factories_list[nb_factory][5] + 11,
                       factories_list[nb_factory][6] + 12, 8, 7)
            pyxel.blt(factories_list[nb_factory][5] + 8,
                      factories_list[nb_factory][6] + 8, 1, 129, 0, 7, 9)

        # Padlock open if factory hovered but factory is locked and enought money to buy it
        elif show and not factories_list[nb_factory][0] and factories_list[nb_factory][1] <= money:

            pyxel.circ(factories_list[nb_factory][5] + 11,
                       factories_list[nb_factory][6] + 13, 8, 13)
            pyxel.circ(factories_list[nb_factory][5] + 11,
                       factories_list[nb_factory][6] + 12, 8, 7)
            pyxel.blt(factories_list[nb_factory][5] + 8,
                      factories_list[nb_factory][6] + 8, 1, 129, 9, 7, 9)
            
    # Display the shop menu
    elif status == "shop":

        pyxel.blt(0, 0, 1, 0, 0, 128, 128)
        pyxel.blt(0, 0, 2, 0, 8, 128, 120)
        # Level bar
        pyxel.rectb(70, 12, 52, 3, 13)
        pyxel.rect(71, 13, progression, 1, 11)

    # Stats (money, gems and levels)
    pyxel.text(2, 2, "Money : " + str(int(money)), 2)
    pyxel.text(2, 9, "Gems : " + str(gems), 2)
    pyxel.text(75, 4, "Levels : " + str(levels), 2)
    return None


pyxel.run(update, draw)
