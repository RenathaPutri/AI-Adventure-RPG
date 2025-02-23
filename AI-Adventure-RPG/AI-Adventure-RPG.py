"""
This file contains code for the game "AI Adventure RPG".

Authors:
1. Renatha Putri
2. SoftwareApkDev
"""


# Game version: 1


# Importing necessary libraries


import sys
import uuid
import pickle
import copy
import google.generativeai as genai
import random
import os
from dotenv import load_dotenv
from mpmath import mp, mpf
from google.ai.generativelanguage_v1 import GenerateContentResponse
from google.generativeai import GenerativeModel
mp.pretty = True


# Creating static functions to be used in this game.


def is_number(string: str) -> bool:
    try:
        mpf(string)
        return True
    except ValueError:
        return False


def ai_response(model: GenerativeModel, prompt: str) -> str:
    response: GenerateContentResponse = model.generate_content(prompt)
    return response.text


def check_status(player, enemy):
    # type: (Player, Enemy) -> None
    print(f"\nPlayer HP: {player.curr_hp}/{player.max_hp}, Stamina: {player.stamina}/{player.MAX_STAMINA}, XP: {player.exp}, Level: {player.level}, Gold: {player.gold}")
    print(f"Enemy HP: {enemy.curr_hp}/{enemy.max_hp}")


def battle(player, enemy):
    # type: (Player, Enemy) -> None
    print("\nYou encountered an enemy!")
    while player.curr_hp > 0 and enemy.curr_hp > 0:
        action = input("\nDo you want to 'attack', 'use sword', 'defend', 'use armor', or 'use potion'? ")
        if action.lower() == "attack":
            if player.stamina >= 10:
                damage = random.randint(10, player.attack_power)
                enemy.curr_hp -= damage
                player.stamina -= 10
                print(f"You attack and deal {damage} damage!")
            else:
                print("Not enough stamina to attack!")
        if action.lower() == "use sword":
            print("Using sword with higher damage")
            if player.stamina >= 20:
                damage = random.randint(20, player.attack_power * 2)
                enemy.curr_hp -= damage
                player.stamina -= 20
                print(f"You use sword and deal {damage} damage!")
                player.inventory.remove_item("Sword Upgrade")
            else:
                print("Not enough stamina to use sword!")
        elif action.lower() == "defend":
            print("You defend, reducing incoming damage.")
        elif action.lower() == "use armor":
            print("You use armor, reducing incoming damage.")
            player.inventory.remove_item("Armor")
        elif action.lower() == "use potion" and "Potion" in [item.name for item in player.inventory.get_items()]:
            player.curr_hp += 30
            if player.curr_hp >= player.max_hp:
                player.curr_hp = player.max_hp

            player.inventory.remove_item("Potion")
            print("You use a potion and restore 30 HP!")
        else:
            print("Invalid action or no potions left!")
            continue

        if enemy.curr_hp > 0:
            enemy_damage = random.randint(10, enemy.attack_power)
            if action.lower() == "defend":
                enemy_damage //= 2
            elif action.lower() == "use armor":
                enemy_damage //= 4

            player.curr_hp -= enemy_damage
            print(f"Enemy attacks and deals {enemy_damage} damage!")

        check_status(player, enemy)

    if player.curr_hp <= 0:
        print("You have been defeated!")
        enemy.exp += 20
        level_up(enemy)
        player.recover()
    else:
        print("You defeated the enemy!")
        player.exp += 20
        player.gold += 30
        level_up(player)
        enemy.recover()


def level_up(player):
    # type: (Player) -> None
    if player.exp >= player.required_exp:
        player.level += 1
        player.attack_power += 5
        player.max_hp += 20
        player.required_exp = player.level * mpf("50")
        print("\nCongratulations! You leveled up!")


def shop_system(shop, player):
    # type: (Shop, Player) -> None
    print("\nWelcome to the shop! Items available:")
    for item in shop.get_items_sold():
        print(f"{item.name}: {item.gold_cost} Gold")
    choice = input("What do you want to buy? (or type 'exit' to leave) ")
    item: Item or None = None
    for curr_item in shop.get_items_sold():
        if curr_item.name == choice:
            item = curr_item
            break
    if isinstance(item, Item) and player.gold >= item.gold_cost:
        player.gold -= item.gold_cost
        player.inventory.add_item(item)
        print(f"You bought {item.name}!")
    else:
        print("Not enough gold or invalid item!")


def load_game_data(file_name):
    # type: (str) -> SavedGameData
    return pickle.load(open(file_name, "rb"))


def save_game_data(game_data, file_name):
    # type: (SavedGameData, str) -> None
    pickle.dump(game_data, open(file_name, "wb"))


def clear():
    # type: () -> None
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows System
    else:
        os.system('clear')  # For Linux System


# Creating necessary classes.


class GameCharacter:
    """
    This class contains attributes of a game character.
    """

    def __init__(self, name):
        # type: (str) -> None
        self.character_id: str = str(uuid.uuid1())
        self.name: str = name

    def clone(self):
        # type: () -> GameCharacter
        return copy.deepcopy(self)


class NPC(GameCharacter):
    """
    This class contains attributes of an NPC (non-player character) in this game.
    """

    def __init__(self, name):
        # type: (str) -> None
        GameCharacter.__init__(self, name)


class Player(GameCharacter):
    """
    This class contains attributes of the player in this game.
    """

    MAX_STAMINA: mpf = mpf("100")

    def __init__(self, name):
        # type: (str) -> None
        GameCharacter.__init__(self, name)
        self.level: int = 1
        self.max_hp: mpf = mpf(random.randint(100, 150))
        self.curr_hp: mpf = self.max_hp
        self.stamina: mpf = self.MAX_STAMINA
        self.attack_power: mpf = mpf(random.randint(20, 30))
        self.exp: mpf = mpf("0")
        self.required_exp: mpf = mpf("50")
        self.gold: mpf = mpf("50")
        self.inventory: Inventory = Inventory()

    def recover(self):
        # type: () -> None
        self.curr_hp = self.max_hp


class Enemy(Player):
    """
    This class contains attributes of an enemy in this game
    """

    def __init__(self, name):
        # type: (str) -> None
        Player.__init__(self, name)


class Inventory:
    """
    This class contains attributes of an item inventory.
    """

    def __init__(self):
        # type: () -> None
        self.__items: list = []

    def get_items(self):
        # type: () -> list
        return self.__items

    def add_item(self, item):
        # type: (Item) -> None
        self.__items.append(item)

    def remove_item(self, item_name):
        # type: (str) -> bool
        for item in self.__items:
            if item.name == item_name:
                self.__items.remove(item)
                return True
        return False

    def clone(self):
        # type: () -> Inventory
        return copy.deepcopy(self)


class Item:
    """
    This class contains attributes of an item in this game.
    """

    def __init__(self, name, gold_cost):
        # type: (str, mpf) -> None
        self.name: str = name
        self.gold_cost: mpf = gold_cost

    def clone(self):
        # type: () -> Item
        return copy.deepcopy(self)


class Shop:
    """
    This class contains attributes of an item shop.
    """

    def __init__(self, items_sold=None):
        # type: (list) -> None
        if items_sold is None:
            items_sold = []
        self.name: str = "ITEM SHOP"
        self.__items_sold = items_sold

    def get_items_sold(self):
        # type: () -> list
        return self.__items_sold

    def clone(self):
        # type: () -> Shop
        return copy.deepcopy(self)


class SavedGameData:
    """
    This class contains attributes of the saved game data in this game.
    """

    def __init__(self, player_name, player_data, enemy, shop):
        # type: (str, Player, Enemy, Shop) -> None
        self.player_name: str = player_name
        self.player_data: Player = player_data
        self.enemy: Enemy = enemy
        self.shop: Shop = shop

    def clone(self):
        # type: () -> SavedGameData
        return copy.deepcopy(self)

# Main game loop
def main():
    print("Welcome to AI Adventure!")
    print("This is an interactive text-based RPG where you explore, fight enemies, and buy items.")

    # Loading Gemini API Key
    load_dotenv()
    genai.configure(api_key=os.environ['GEMINI_API_KEY'])

    # Gemini Generative Model
    model: GenerativeModel = genai.GenerativeModel("gemini-pro")

    # Saved Game Data
    game_data: SavedGameData = SavedGameData("", Player(""), Enemy(""), Shop([]))

    game_started: bool = False
    print("Enter \"Y\" for yes.")
    print("Enter anything else for no.")
    load_game: str = input("Do you want to load saved game data? ")
    while not game_started:
        if load_game.upper() == "Y":
            saved_game_files: list = [f for f in os.listdir("../saved")]
            if len(saved_game_files) == 0:
                print("No saved game data available.")
                load_game = "N"
            else:
                clear()
                player_name: str = input("Please enter name of player you want to load saved game data from: ")
                game_data = load_game_data(os.path.join("../saved", player_name))
                game_started = True
        else:
            clear()

            # Player stats
            name: str = input("Please enter your name: ")
            player: Player = Player(name)
            enemy: Enemy = Enemy("CPU")

            # Shop items
            shop: Shop = Shop([Item("Potion", mpf("20")), Item("Sword Upgrade", mpf("50")),
                               Item("Armor", mpf("40"))])
            game_data = SavedGameData(name, player, enemy, shop)
            game_started = True

    while True:
        clear()
        print("Commands you can use:")
        print("- 'go north': Explore the northern area.")
        print("- 'go south': Enter a battle.")
        print("- 'attack': Attack an enemy in battle.")
        print("- 'use sword': Use sword to increase damage.")
        print("- 'defend': Reduce damage in battle.")
        print("- 'use armor': Use armor to reduce incoming damage.")
        print("- 'use potion': Heal yourself if you have a potion.")
        print("- 'check status': View your HP, Stamina, XP, and Gold.")
        print("- 'shop': Visit the shop to buy items.")
        print("- 'exit': Save game data and quit the game.")
        print("\nLet the adventure begin!")

        context: str = "You are in a mysterious forest. There is a path to the north and a dark cave to the south. What do you want to do?"

        print("\nAI: ", context)
        user_input: str = input("\n>> ")
        
        if user_input.lower() == "exit":
            save_game_data(game_data, game_data.player_data.name)
            print("\nThanks for playing!")
            break
        elif user_input.lower() == "go north":
            context = "You find a hidden village. People here seem friendly."
        elif user_input.lower() == "go south":
            battle(game_data.player_data, game_data.enemy)
            context = "After the battle, you find a treasure chest."
        elif user_input.lower() == "check status":
            check_status(game_data.player_data, game_data.enemy)
            continue
        elif user_input.lower() == "shop":
            shop_system(game_data.shop, game_data.player_data)
            continue
        else:
            prompt = f"{context}\nPlayer chooses: {user_input}. What happens next?"
            context = ai_response(model, prompt)

if __name__ == "__main__":
    main()
