
"""
This is the player file, having a single class called player, where all the methods (activities) of the character is coded!!
"""

import escapetheforest.items as items, escapetheforest.world as world

import random


class Player(object):
    def __init__(self):
        self.inventory = [items.gold(10), items.fists()]
        self.hp = 20
        self.strength= 2
        self.location_x, \
        self.location_y = world.starting_position
        self.victory = False



    def has_wstick(self):
            for item in self.inventory:
                if item.name is "Wooden stick":
                    return True


    def is_alive(self):
        return self.hp > 0

    def print_inventory(self):
        if len(self.inventory) == 1 and (self.inventory[0].name == "Fists"):
            print("You open your backpack and find nothing inside","\n")
        else:
            print("You open your backpack and find the following items:","\n")
            for item in self.inventory:
                if item.name is not "Fists":
                    print(item, "\n")

        #The following code finds an instance of an object in a list of objects with list comprehension easily:
        # if (x for x in self.inventory if x.name == "Knife"):
        #     print("Hi")


    def print_stats(self):
        print("Your HP is: " + str(self.hp), "\n")
        print("Your Strength is: " + str(self.strength), "\n")

    def flee(self, tile):
        available_moves = tile.adjacent_moves()
        r = random.randint(0, len(available_moves) - 1)
        self.do_action(available_moves[r])

    def move(self, dx, dy):
        self.location_x += dx
        self.location_y += dy
        #The following prints the intro text at the current tile where the player is located:
        #print(world.tile_exists(self.location_x, self.location_y).intro_text())

    def move_north(self):
        self.move(dx=0, dy=-1)

    def move_south(self):
        self.move(dx=0, dy=1)

    def move_east(self):
        self.move(dx=1, dy=0)

    def move_west(self):
        self.move(dx=-1, dy=0)

    def sellAmushroom(self):
        global goldExists
        goldExists = False
       # while token == 0:
        #Check for mushroom and remove it(its sold after all)
        for j in self.inventory:
            if isinstance(j, items.mushRoom):
                self.inventory.remove(j)

        #Check for gold, if gold exists, return: add value of the mushroom to the gold.
        for i in self.inventory:
            if isinstance(i, items.gold):
                goldExists=True
                print("Mushroom sold for", j.value)
                i.value += j.value
                if i.value >= 50:
                    print("Oooh, I sense you have much gold in your pockets human! It would be a shame if the bandits of this forest took it... Allow me to teleport you out of this horrible place and into your warm and safe bed instead!")
                    print("You give the 50 gold to the elf and win the game!")
                    self.victory = True
        if goldExists == False:
            self.inventory.append(items.gold(j.value))
            print("Mushroom sold for {}g".format(j.value))

    def giveAllMoney(self, enemy):

        for i in self.inventory:
            if isinstance(i, items.gold) and (i.amt >= 30):
                global givenAmt
                givenAmt = i.amt
                self.inventory.remove(i)
                print("You give out all your money")
                if enemy.isaggressive == True:
                    enemy.calm()
                print("He calmed down")
                break
            elif isinstance(i, items.gold)and (i.amt < 30):
                print("The money isn't enough...")
                enemy.provoke()
                break
            else:
                print("When I reach into my pocket I cant find any money!")
                enemy.provoke()
                break


    def giveTenG(self, enemy):

        for i in self.inventory:
            if isinstance(i, items.gold) and (i.amt >= 10):
                i.amt-= 10
                print("You pay 10G")
                if enemy.isaggressive == True:
                    enemy.calm()
                print("Your enemy has calmed down")
                break
            elif isinstance(i, items.gold)and (i.amt < 10):
                print("The money isn't enough...")
                enemy.provoke()
                break
            else:
                print("When I reach into my pocket I cant find any money!")
                enemy.provoke()
                break

    def returnMoney(self):
        self.inventory.append(items.gold(givenAmt))
        print("You took back your money")


    def attack(self, enemy):
        if not enemy.isaggressive:
            print("You surprise the enemy by attacking it.")
            enemy.provoke()
        best_weapon = None
        max_dmg = 0

        for i in self.inventory:
            if isinstance(i, items.weapon):
                if i.damage > max_dmg:
                    max_dmg = i.damage
                    best_weapon = i

        curdmg = random.randint(best_weapon.damage - best_weapon.rangy, best_weapon.damage)
        curdmg += self.strength
        enemy.hp -= curdmg
        print("You use {0} against {1}, causing {2} damage".format(best_weapon.name, enemy.name, curdmg))

        if not enemy.is_alive():
            print("Wham! You smite the {0} to the ground and remain victorious!".format(enemy.name))

        else:
            print("{0} hp is {1}".format(enemy.name, enemy.hp))

    def do_action(self, action, **kwargs):
        action_method = getattr(self, action.method.__name__)
        if action_method:
            action_method(**kwargs)

    def sharpen(self):
        hassharp = False
        val = len(self.inventory)
        i = 0
        while i < val:
            if self.inventory[i].name == "Wooden stick":
                del self.inventory[i]
                val = -1
                i = -1
            # elif self.inventory[i].name == "Sharpened stick":
            #     hassharp=True
            i = i + 1
        if hassharp == False:
            self.inventory.append(items.sharpenedStick())
        print("You use the knife to sharpen the wooden stick into something a bit more dangerous.""\n")

    def killSelfie(self):
        self.hp = 0

    def eatMushroom(self):
        val = len(self.inventory)
        i = 0
        healthEffect = 0
        strengthEffect = 0

        while i < val:
            if self.inventory[i].name == "Mushroom":
                healthEffect = self.inventory[i].hpadd
                strengthEffect = self.inventory[i].dmgadd
                del self.inventory[i]
                break

            i = i + 1

        self.hp += healthEffect
        self.strength += strengthEffect

        print("You eat the strange mushroom in one big bite. You feel healthy, and your arms seem bigger!""\n")


