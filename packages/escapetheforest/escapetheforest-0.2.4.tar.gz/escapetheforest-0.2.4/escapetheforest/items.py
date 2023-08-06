
"""item classes are found in this script"""

class item(object):
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value

    def __str__(self):
        return "{0}\n Value is:{1}\n {2}\n".format(self.name, self.value, self.description)



class book(item):
    def __init__(self, title):
        self.title = title
        super(book, self).__init__(name = "Book",
                                   description="An old dusty book",
                                   title = "How to get strong with 5 easy tricks",
                                   value = 20)



class gold(item):
    def __init__(self, amt):
        self.amt = amt
        super(gold, self).__init__(name="Gold",
                                   description="Gold coins.".format(str(self.amt)),
                                   value=self.amt)


class weapon(item):
    def __init__(self, name, description, value, damage, rangy):
        self.damage = damage
        self.rangy = rangy
        super(weapon, self).__init__(name, description, value)

    def __str__(self):
        return "{0}\n {1}\n Value is: {2}\n Damage: {3}\n".format(self.name, self.description, self.value, self.damage)


class fists(weapon):
    def __init__(self):
        super(fists, self).__init__(name="Fists",
                                    description="Your medium sized fists",
                                    value=0,
                                    damage=1,
                                    rangy=2)

class knife(weapon):
    def __init__(self):
        super(knife, self).__init__(name="Knife",
                                    description="A shorter type knife suitable for wood carving",
                                    value=5,
                                    damage=4,
                                    rangy=1)


class sharpenedStick(weapon):
    def __init__(self):
        super(sharpenedStick, self).__init__(name="Sharpened stick",
                                             description="A long stick of hard wood, sharpened to be pointy in one end.",
                                             value=0,
                                             damage=6,
                                             rangy=3)


class stick(weapon):
    def __init__(self):
        super(stick, self).__init__(name="Wooden stick",
                                    description="Just a piece of wood",
                                    value=0,
                                    damage=3,
                                    rangy=1)


## Make a new class of edibles?? 

class edible(item):
    def __init__(self, name, description, value, hpadd, dmgadd):
        self.hpadd = hpadd
        self.dmgadd = dmgadd
        super(edible, self).__init__(name, description, value)

    def __str__(self):
        return "{0}\n {1}\n Value is: {2}\n Hp add: {3}\n Damage add: {4}\n".format(self.name,
                                                                                    self.description,
                                                                                    self.value,
                                                                                    self.hpadd,
                                                                                    self.dmgadd)


class mushRoom(edible):
    def __init__(self):
        super(mushRoom, self).__init__(
            name="Mushroom",
            description="An odd looking mushroom...",
            value=10,
            hpadd=2,
            dmgadd=2

        )
