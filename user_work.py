from telegram import Update
from telegram.ext import ContextTypes
from constants import HOME_DIR, GO
import os


class User:
    def __init__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.update = update
        self.context = context
        self.username = self.update.effective_user.username
        self.first_name = self.update.effective_user.first_name
        self.last_name = self.update.effective_user.last_name
        self.dir_path = os.path.join(HOME_DIR, self.username)  # папка
        self.pet_file = os.path.join(self.dir_path, "name.txt")
        self.money_file = os.path.join(self.dir_path, "money.txt")
        
        
        self.pet = None
        self.money = self.read_money()

        self.init_dir()

    def init_dir(self):
        if not os.path.exists(self.dir_path):
            os.mkdir(self.dir_path)
        with open(self.pet_file, "a", encoding="utf-8") as file:
            pass
        with open(self.money_file, "a", encoding="utf-8") as file:
            pass
    
    def is_pet(self):
        with open(self.pet_file, "r", encoding="utf-8") as file:
            text = file.read().strip()  # убрать пробелы
        if text:
            self.pet = text
            return True
        return False
    
    async def write_pet_name(self, name: str):
        self.pet = name
        with open(self.pet_file, "w", encoding="utf-8") as file:
            file.write(self.pet)
        return self.pet
    
    def save_money(self):
        with open(self.money_file, mode="w", encoding="utf-8") as file:
            file.write(str(self.money))
    
    def read_money(self):
        with open(self.money_file, "r") as file:
            text = file.read()
            if text.strip() == "":
                return 0
            else:
                return int(text)



if __name__ == "__main__":
    dir_path = os.path.join(HOME_DIR, "romturino")
    print(dir_path)
    pet_file = os.path.join(dir_path, "name.txt")
    print(pet_file)
    with open(pet_file, "a", encoding="utf-8") as file:
        pass
