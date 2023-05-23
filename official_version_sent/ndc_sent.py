
import pyxel
from random import randint

pyxel.init(128, 128, title="Idle Factories")
pyxel.load("world1.pyxres")

pyxel.mouse(True)

# unlock or not, price, multiplicator of lvl up, money per sec, lvl of factory, pos x, pos y
statut_list = ["main", "shop"]

statut = "main"

factory_lvl_1 = [False,100,1.1,1,0,16,16]

factory_lvl_2 = [False,1000,1.25,2,0,98,18]

factory_lvl_3 = [False,5000,1.5,5,0,8,60]

factory_lvl_4 = [False,10000,1.75,10,0,56,48]

factory_lvl_5 = [False,25000,2,100,0,32,88]

factory_lvl_6 = [False,100000,2.5,500,0,72,88]

factories_list = [factory_lvl_1,factory_lvl_2,factory_lvl_3,factory_lvl_4,factory_lvl_5,factory_lvl_6]

#postion_x, posiition_y
table_craft = [40,40]

shop = [104,48]

money = 100

gems = 20

levels = 1

mouse_x = 0

mouse_y = 0

nb_clicks = 0

next_level = 100

progression = 0

#boost
boost_lightning = False
#pos
boost_lightning_pos = []
seconds_lightning = 0

x2 = False
#pos
x2_pos = []
seconds_x2 = 0

#pos
exit_pos = []

def over():
    for nb_factory, factory in enumerate (factories_list):
        if mouse_x > factory[5] and mouse_x < factory[5] + 32 and mouse_y > factory[6] and mouse_y < factory[6] + 32:
            if factory[0]:
                return True, nb_factory
    return False, nb_factory

def factories(money):
    for factory in factories_list:
        if factory[0]:
            money = money + (factory[3] * factory[4])
    return money

def buy_upgrade_factories(money):
    if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
        for factory in factories_list:
            if mouse_x > factory[5] and mouse_x < factory[5] + 32 and mouse_y > factory[6] and mouse_y < factory[6] + 32:
                if not factory[0] and money >= factory[1]:
                    money = money - factory[1]
                    factory[1] = int(factory[1] * factory[2])
                    factory[0] = True
                    factory[4] = factory[4] + 1
                    #Cadenas à enlever
                elif money >= factory[1] and factory[4] < 30:
                    money = money - factory[1]
                    factory[1] = int(factory[1] * factory[2])
                    factory[4] = factory[4] + 1
    return money

def manual_money(money, levels, gems, nb_clicks, next_level):
    
    if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
        if mouse_x > table_craft[0] and mouse_x < table_craft[0] + 16 and mouse_y > table_craft[1] and mouse_y < table_craft[1] + 16:
            proba_gems = randint(0,100)
            if proba_gems < 3:
                gems = gems + 1
            money = money + (1 * levels)
            nb_clicks = nb_clicks + 1
            levels, next_level, nb_clicks = upgrade_levels(nb_clicks, levels, next_level)
            
            return money, levels, gems, nb_clicks, next_level
    
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
        next_level = next_level * levels
    return levels, next_level, nb_clicks

def crossbar_level(nb_clicks, next_level):
    progression = 50 * nb_clicks/next_level
    return progression

def enter_shop(statut):
    if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) and mouse_x > shop[0] and mouse_x < shop[0] + 24 and mouse_y > shop[1] and mouse_y < shop[1] + 16:
        statut = statut_list[1]
    return statut

def shops(boost_lightning, x2, statut,gems):
    if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) and mouse_x > 25 and mouse_x < 38 and mouse_y > 81 and mouse_y < 94 and gems >= 10:
        gems = gems - 10
        boost_lightning = True
    elif pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) and mouse_x > 73 and mouse_x < 86 and mouse_y > 21 and mouse_y < 94 and gems >= 10:
        x2 = True
        gems = gems - 10
    elif pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) and mouse_x > 104 and mouse_x < 119 and mouse_y > 80 and mouse_y < 94:
        statut = "main"
    return boost_lightning, x2, statut, gems

#____________________________________________________
def update():
    global factories_list, money, mouse_x, mouse_y, levels, gems, nb_clicks, next_level, progression, statut, statut_list, afficher, nb_factory, locked_factories_list, boost_lightning, x2, seconds_lightning, seconds_x2
    
    mouse_x = pyxel.mouse_x
    mouse_y = pyxel.mouse_y
    if statut == "main":
        money = buy_upgrade_factories(money)
        money, levels, gems, nb_clicks, next_level = manual_money(money, levels, gems, nb_clicks, next_level)
        progression = crossbar_level(nb_clicks, next_level)
        statut = enter_shop(statut)
        afficher, nb_factory = over()
        locked_factories_list = locked_factories(factories_list)
    
    elif statut == "shop":
        boost_lightning, x2, statut, gems = shops(boost_lightning, x2, statut, gems)

    if x2:
        if pyxel.frame_count % 15 == 0:
            money = factories(money)
    elif boost_lightning:
        if pyxel.frame_count % 30 == 0:
            money = factories(money) * 2
    else:
        if pyxel.frame_count % 30 == 0:
            money = factories(money)
    
    if boost_lightning:
        if seconds_lightning < 15:
            if pyxel.frame_count % 30 == 0:
                seconds_lightning = seconds_lightning + 1
        if seconds_lightning == 15:
            boost_lightning = False
            seconds_lightning = 0
    
    if x2:
        if seconds_x2 < 3:
            if pyxel.frame_count % 30 == 0:
                seconds_x2 = seconds_x2 + 1
        if seconds_x2 == 15:
            x2 = False
            seconds_x2 = 0
    return None


#____________________________________________________
def draw():
    pyxel.cls(0)
    if statut == "main":
        pyxel.blt(0,0,1,0,0,128,128)
        
        #stats
        pyxel.text(2,2,"Money : " + str(money),2)
        pyxel.text(2,9,"Gems : " + str(gems),2)
        pyxel.text(75,9,"Levels : " + str(levels),2)

        #crossbar
        pyxel.rectb(70,17,52,3,13)
        pyxel.rect(71,18,progression,1,11)
        
        #locked_factories
        for nb_factory_locked in locked_factories_list:
            pyxel.blt(factories_list[nb_factory_locked][5] + 10,factories_list[nb_factory_locked][6] + 16,2,1,0,6,8)
        
        #levels factories
        if afficher and factories_list[nb_factory][4] < 10:
            pyxel.circ(factories_list[nb_factory][5] + 13, factories_list[nb_factory][6] + 18, 8, 7)
            pyxel.text(factories_list[nb_factory][5] + 12, factories_list[nb_factory][6] + 16, str(factories_list[nb_factory][4]), 0)
        elif afficher:
            pyxel.circ(factories_list[nb_factory][5] + 13, factories_list[nb_factory][6] + 18, 8, 7)
            pyxel.text(factories_list[nb_factory][5] + 10, factories_list[nb_factory][6] + 16, str(factories_list[nb_factory][4]), 0)


    elif statut == "shop":
        
        pyxel.blt(0,0,1,0,0,128,128)
        pyxel.blt(0,0,2,0,8,128,120)
        #stats
        pyxel.text(2,2,"Money : " + str(money),2)
        pyxel.text(2,9,"Gems : " + str(gems),2)
        pyxel.text(75,4,"Levels : " + str(levels),2)
        
        #crossbar
        pyxel.rectb(70,12,52,3,13)
        pyxel.rect(71,13,progression,1,11)
        
        return None

pyxel.run(update,draw)