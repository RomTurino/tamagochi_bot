import random
from constants import *
import os

class Pet:
    def __init__(self, username:str):
        self.username = username
        self.love = random.randint(0, 100)
        self.satiety = random.randint(0, 100)
        self.happiness = random.randint(0, 100)
        self.energy = random.randint(0, 100)
        self.is_alive = True
        
        self.read_save()
    
    def be_dead(self):
        os.remove(f"users/{self.username}.txt")
    
    def write_file(self):
        if not os.path.exists("users"):
            os.mkdir("users")
        with open(f"users/{self.username}.txt", "w", encoding="utf-8") as file:
            file.write(f"{self.love}\n")
            file.write(f"{self.satiety}\n")
            file.write(f"{self.happiness}\n")
            file.write(f"{self.energy}\n")
    
    def read_save(self):
        if not os.path.exists(f"users/{self.username}.txt"):
            return None    
        with open(f"users/{self.username}.txt", "r", encoding="utf-8") as file:
            stats = file.read().strip().split("\n")
            self.love = int(stats[0])
            self.satiety = int(stats[1])
            self.happiness = int(stats[2])
            self.energy = int(stats[3])
    
    def set_one_limit(self, stat:int):
        if stat < 0:
            stat = 0
        if stat > 100:
            stat = 100
        return stat
        
    def set_limits(self):
        self.love = self.set_one_limit(self.love)
        self.satiety = self.set_one_limit(self.satiety)
        self.happiness = self.set_one_limit(self.happiness)
        self.energy = self.set_one_limit(self.energy)
        self.write_file()
        
    def decrease_stats(self, carousel:bool = False):
        vars = ["сытость", "энергия"]
        if carousel:
            vars += ["любовь", "счастье"]
        option = random.choice(vars)
        minus = random.randint(1, 5)
        if option == "сытость":
            self.satiety -= minus
        elif option == 'энергия':
            self.energy -= minus
        elif option == "любовь":
            self.love -= minus
        else:
            self.happiness -= minus
        
    def hello(self):
        """приветствие"""
        sticker = random.choice(HELLO_STICKERS)
        message = random.choice(HELLO_PHRASES)
        return sticker, message
    
    
    def increase_love(self): 
        """гладить"""
        self.love += random.randint(5,10)
        self.happiness += random.randint(1,2)
        self.decrease_stats()
        self.set_limits()
        sticker = random.choice(LOVE_STICKERS)
        message = random.choice(LOVE_PHRASES)
        return sticker, message
        
    
    def increase_happiness(self):
        """играть"""
        self.happiness += random.randint(5,10)
        self.satiety -= random.randint(5, 10)
        self.love += random.randint(1,3)
        self.decrease_stats()
        self.set_limits()   
        sticker = random.choice(PLAY_STICKERS)
        message = random.choice(PLAY_PHRASES)
        return sticker, message
    
    
    def increase_satiety(self):
        """кормить"""
        self.satiety += random.randint(10, 20)
        self.happiness += random.randint(1, 3)
        self.decrease_stats(True)
        self.set_limits()
        sticker = random.choice(FOOD_STICKERS)
        message = random.choice(FOOD_PHRASES)
        return sticker, message
    
    def increase_energy(self):
        """уложить спать"""
        self.energy += random.randint(1, 100)
        for i in range(random.randint(1,4)):
            self.decrease_stats(True)
        self.set_limits()