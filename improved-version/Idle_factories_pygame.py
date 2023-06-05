
import pickledb
import pygame
import os
import time
from random import randint


def click(factories_list, mouse_x, mouse_y, money):
    """This function checks if the mouse cursor is hovering over one of the factories.
    If so, then it executes the "buy_upgrade_factories" function. Otherwise, it simply returns "money" without any modifications.

    Returns:
        bool : True if mouse cursor is hovering a factory, False if not.
        int : number of the factory (unused if mouse cursor isn't hovering a factory).
    """
    for nb_factory, factory in enumerate(factories_list):
        if mouse_x > factory[5] and mouse_x < factory[5] + 60 and mouse_y > factory[6] and mouse_y < factory[6] + 60:
            money = buy_upgrade_factories(nb_factory, money)
            return money, True, nb_factory
    return money, False, nb_factory


def factories(money, x2, factories_list):
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
                # Money already obtained + ((money earned when factory is level 1 * level of the factory) * 2 for the boost)
                money = money + ((factory[3] * factory[4]) * 2)
            else:
                # Money already obtained + (money earned when factory is level 1 * level of the factory)
                money = money + (factory[3] * factory[4])
    return money


def buy_upgrade_factories(nb_factory, money):
    """This function allows you to buy a factory, or to improve it if you have already bought it before.

    Args:
        money (int): the money is necessary to know if we have enough money to buy/improve the factory or not.

    Returns:
        int: money after bought something or not.
    """
    # We take the factory clicked
    factory_hovered = factories_list[nb_factory]

    # If the factory is not unlocked
    if not factory_hovered[0] and money >= factory_hovered[1]:
        factory_hovered[0] = True

    if money >= factory_hovered[1] and factory_hovered[4] < 30:
        money = money - factory_hovered[1]

        # Increases the cost of the improvement
        factory_hovered[1] = int(factory_hovered[1] * factory_hovered[2])

        # Increase the level of the factory
        factory_hovered[4] = factory_hovered[4] + 1
    return money


def manual_money(money, levels, gems, nb_clicks, next_level, farm_factory, mouse_x, mouse_y, progression):
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
    # If the mouse is on the farm factory
    if mouse_x > farm_factory[0] and mouse_x < farm_factory[0] + 60 and mouse_y > farm_factory[1] and mouse_y < farm_factory[1] + 60:

        # 5% of chance to get a gem on click
        proba_gems = randint(0, 100)
        if proba_gems < 5:
            gems = gems + 1

        # For example, if level 5, then 5 of money earned
        money = money + (1 * levels)
        nb_clicks = nb_clicks + 1
        
        # Execute the function to upgrade levels if the number of clicks is greater than the number of clicks needed to reach the next level
        if nb_clicks >= next_level:
            levels, next_level, nb_clicks = upgrade_levels(nb_clicks, levels, next_level)
        
        # Progression of level bar
        progression = level_bar(nb_clicks, next_level)
        
    return money, levels, gems, nb_clicks, next_level, progression


def upgrade_levels(nb_clicks, levels, next_level):
    """This function allows to detect if the upper level is reached or not.

    Args:
        nb_clicks (int): number of clicks made since the beginning of the last level.
        levels (int): to level up.
        next_level (int): number of clicks needed to next level.

    Returns:
        int: to update all the variables imported in this function.
    """
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
    progression = 100 * nb_clicks/next_level

    return progression

# ==================== INITIALISATION ====================

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
    factory_lvl_1 = [False, 100, 1.1, 1, 0, 10, 10]
    factory_lvl_2 = [False, 1000, 1.25, 2, 0, 80, 10]
    factory_lvl_3 = [False, 5000, 1.40, 5, 0, 150, 10]
    factory_lvl_4 = [False, 10000, 1.5, 10, 0, 220, 10]
    factory_lvl_5 = [False, 25000, 1.7, 50, 0, 290, 10]
    factory_lvl_6 = [False, 100000, 1.75, 200, 0, 360, 10]

    # Others data
    money = 1000000
    gems = 5000
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
farm_factory = [460, 10]
factories_list = [factory_lvl_1, factory_lvl_2,
                  factory_lvl_3, factory_lvl_4, factory_lvl_5, factory_lvl_6]
status = "main"


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
font = pygame.font.SysFont("consolas", 20)
production = 0
color_factory_1 = "red"
color_factory_2 = "blue"
color_factory_3 = "green"
color_factory_4 = "magenta"
color_factory_5 = "yellow"
color_factory_6 = "cyan"
color_factory_7 = "black"
color_list = [color_factory_1, color_factory_2, color_factory_3, color_factory_4, color_factory_5, color_factory_6, color_factory_7]
factories_clicked = False
nb_factory = 0

# ==================== MAIN PROGRAM ====================

# ==================== Main loop ====================
while running:
    
    # ==================== Event detection ====================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            money, factories_clicked, nb_factory = click(factories_list, mouse_x, mouse_y, money) # Click on factories or not
            money, levels, gems, nb_clicks, next_level, progression = manual_money(money, levels, gems, nb_clicks, next_level, farm_factory, mouse_x, mouse_y, progression)
    
    # When a factory is clicked, its color changes to white
    if factories_clicked:
        start_time = time.time()
        color_temp = color_list[nb_factory]
        color_list[nb_factory] = "white"
        factories_clicked = False
    
    # The color of the factory returns to its original color after 0.1 seconds
    if color_list[nb_factory] == "white":
        if time.time() - start_time > 0.1:
            color_list[nb_factory] = color_temp
            
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if production % 60 == 0:
        # Every 60 frames, the factories produce money
        money = factories(money, x2, factories_list)
        production = 0
        # ==================== Save ====================
        data = pickledb.load('sauvegarde.db', True)

        # Factories
        factories_list = [factory_lvl_1, factory_lvl_2, factory_lvl_3, factory_lvl_4, factory_lvl_5, factory_lvl_6]
        data.set('factories_list',factories_list)

        # Others data
        others_data_list = [str(int(money)), str(int(gems)), str(int(levels)), str(int(nb_clicks)), str(int(next_level)), str(int(progression))]
        data.set('others_data_list',others_data_list)
    production += 1
    
    # ==================== Display ====================
    screen.fill("purple")
    
    money4 = font.render(str(money), 1, (255, 255, 255))
    gems_text = font.render(str(gems), 1, (255, 255, 255))
    screen.blit(money4, (100, 100))
    screen.blit(gems_text, (100, 150))    

    pygame.draw.rect(screen, color_list[0], (10, 10, 60, 60), 60)
    pygame.draw.rect(screen, color_list[1], (80, 10, 60, 60), 60)
    pygame.draw.rect(screen, color_list[2], (150, 10, 60, 60), 60)
    pygame.draw.rect(screen, color_list[3], (220, 10, 60, 60), 60)
    pygame.draw.rect(screen, color_list[4], (290, 10, 60, 60), 60)
    pygame.draw.rect(screen, color_list[5], (360, 10, 60, 60), 60)
    pygame.draw.rect(screen, color_list[6], (460, 10, 60, 60), 60)
    pygame.draw.rect(screen, "green", (560, 30, progression, 5), 5)
    pygame.draw.rect(screen, "white", (558, 28, 104, 9), 2)
    clock.tick(60) # 60 FPS limit
    
    pygame.display.flip()
