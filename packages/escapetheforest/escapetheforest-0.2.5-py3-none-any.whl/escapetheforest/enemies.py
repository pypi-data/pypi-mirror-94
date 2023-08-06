

"""This is where all the enemies reside """

class NPC(object):
    def __init__(self, name, hp):
        self.name=name
        self.hp = hp

    def is_alive(self):
        return self.hp > 0

# THe following are NPCs:

class trader(NPC):
    def __init__(self):
        super(trader, self).__init__(name="Tradesman", hp=10)



#Following are enemy class and enemies:
class enemy(object):
    def __init__(self, name, hp, damage, isaggressive):
        self.isaggressive = isaggressive
        self.name = name
        self.hp = hp
        self.damage = damage

        
    def is_alive(self):
        return self.hp > 0

    def provoke(self):
        self.isaggressive = True
        print("You have provoked the enemy to aggression!")

    def calm(self):
        self.isaggressive = False
        print("Enemy has calmed down and is no longer prone to attacking")

class bandit(enemy):
    def __init__(self):
        super(bandit,self).__init__(name = "Bandit", hp = 10, damage = 3, isaggressive=False)

class ringLeader(enemy):
    def __init__(self):
        super(ringLeader, self).__init__(name = "Bandit ringleader", hp = 15, damage = 4, isaggressive=False)

class bigSpider(enemy):
    def __init__(self):
        super(bigSpider, self).__init__(name="Big spider", hp=6, damage=2, isaggressive=True)

class crazyOldMan(enemy):
    def __init__(self):
        super(crazyOldMan,self).__init__(name = "Crazy old man", hp = 10, damage = 5, isaggressive=True)
        

