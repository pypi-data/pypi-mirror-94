
#import escapetheforest.player as player
from escapetheforest.player import Player



class action(object):
    def __init__(self, method, name, hotkey, **kwargs):
        self.method = method
        self.name = name
        self.hotkey = hotkey
        self.kwargs = kwargs

    def __str__(self):
        return "{}: {}".format(self.hotkey, self.name)


class moveNorth(action):
    def __init__(self):
        super(moveNorth,self).__init__(method=Player.move_north, name="Move north", hotkey = "n")

class moveSouth(action):
    def __init__(self):
        super(moveSouth,self).__init__(method=Player.move_south, name="Move south", hotkey = "s")

class moveEast(action):
    def __init__(self):
        super(moveEast,self).__init__(method=Player.move_east, name="Move east", hotkey = "e")

class moveWest(action):
    def __init__(self):
        super(moveWest,self).__init__(method=Player.move_west, name="Move west", hotkey = "w")


class viewInventory(action):
    #Prints the players inventory
    def __init__(self):
        super(viewInventory,self).__init__(method= Player.print_inventory, name = "view inventory", hotkey = "i")


#class viewHP(action):
#    #Prints the players inventory
#    def __init__(self):
#        super(viewHP,self).__init__(method= Player.print_hp, name = "view HP", hotkey = "h")

class viewStats(action):
    #Prints the players inventory
    def __init__(self):
        super(viewStats,self).__init__(method= Player.print_stats, name = "view stats", hotkey = "l")

class attack(action):
    def __init__(self, enemy):
        super(attack,self).__init__(method=Player.attack, name = "Attack!", hotkey = "a", enemy = enemy)


class flee(action):
    def __init__(self, tile):
        super(flee,self).__init__(method=Player.flee, name = "Flee", hotkey = "f", tile = tile)


        """New functionality"""

class sharpenStick(action):
    #Makes the player sharpen a stick and add the sharpenedStick weapon to the inventory
    def __init__(self):
        super(sharpenStick,self).__init__(method=Player.sharpen, name = "Sharpen the wooden stick", hotkey = "g")


class killSelf(action):
    def __init__(self):
        super(killSelf,self).__init__(method=Player.killSelfie, name = "This is no fun 😞", hotkey = "m")


## Add eat edible functionality:

class eatMushroom(action):
    def __init__(self):
        super(eatMushroom,self).__init__(method=Player.eatMushroom, name = "Eat mushroom", hotkey = "y")

# Add give money action

class giveAllMoney(action):
    def __init__(self, enemy):
        super(giveAllMoney, self).__init__(method=Player.giveAllMoney, name="Pay the money", hotkey = "p", enemy = enemy)


class giveTenG(action):
    def __init__(self, enemy):
        super(giveTenG, self).__init__(method=Player.giveTenG, name="Pay the money", hotkey = "p", enemy = enemy)



class sellMushroom(action):
    def __init__(self):
        super(sellMushroom, self).__init__(method=Player.sellAmushroom, name="Sell mushroom", hotkey = "g")
