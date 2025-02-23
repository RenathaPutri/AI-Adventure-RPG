"""
This file contains code for the game "AI Adventure RPG".

Authors:
1. Renatha Putri
2. SoftwareApkDev
"""


# Game version: 1


# Importing necessary libraries


import google.generativeai as genai
import random
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ['GEMINI_API_KEY'])

def ai_response(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

# Player stats
player = {"HP": 100, "Stamina": 100, "Attack": 20, "XP": 0, "Level": 1, "Gold": 50, "Inventory": []}
enemy = {"HP": 80, "Attack": 15}

# Shop items
shop = {"Potion": 20, "Sword Upgrade": 50, "Armor": 40}

def check_status():
    print(f"\nPlayer HP: {player['HP']}, Stamina: {player['Stamina']}, XP: {player['XP']}, Level: {player['Level']}, Gold: {player['Gold']}")
    print(f"Enemy HP: {enemy['HP']}")

def battle():
    print("\nYou encountered an enemy!")
    while player["HP"] > 0 and enemy["HP"] > 0:
        action = input("\nDo you want to 'attack', 'defend', or 'use potion'? ")
        if action.lower() == "attack":
            if player["Stamina"] >= 10:
                damage = random.randint(10, player["Attack"])
                enemy["HP"] -= damage
                player["Stamina"] -= 10
                print(f"You attack and deal {damage} damage!")
            else:
                print("Not enough stamina to attack!")
        elif action.lower() == "defend":
            print("You defend, reducing incoming damage.")
        elif action.lower() == "use potion" and "Potion" in player["Inventory"]:
            player["HP"] += 30
            player["Inventory"].remove("Potion")
            print("You use a potion and restore 30 HP!")
        else:
            print("Invalid action or no potions left!")
            continue

        if enemy["HP"] > 0:
            enemy_damage = random.randint(5, enemy["Attack"])
            if action.lower() == "defend":
                enemy_damage //= 2
            player["HP"] -= enemy_damage
            print(f"Enemy attacks and deals {enemy_damage} damage!")

        check_status()

    if player["HP"] <= 0:
        print("You have been defeated!")
    else:
        print("You defeated the enemy!")
        player["XP"] += 20
        player["Gold"] += 30
        level_up()


def level_up():
    if player["XP"] >= player["Level"] * 50:
        player["Level"] += 1
        player["Attack"] += 5
        player["HP"] += 20
        print("\nCongratulations! You leveled up!")

def shop_system():
    print("\nWelcome to the shop! Items available:")
    for item, price in shop.items():
        print(f"{item}: {price} Gold")
    choice = input("What do you want to buy? (or type 'exit' to leave) ")
    if choice in shop and player["Gold"] >= shop[choice]:
        player["Gold"] -= shop[choice]
        player["Inventory"].append(choice)
        print(f"You bought {choice}!")
    else:
        print("Not enough gold or invalid item!")

# Main game loop
def main():
    print("Welcome to AI Adventure!")
    print("This is an interactive text-based RPG where you explore, fight enemies, and buy items.")
    print("Commands you can use:")
    print("- 'go north': Explore the northern area.")
    print("- 'go south': Enter a battle.")
    print("- 'attack': Attack an enemy in battle.")
    print("- 'defend': Reduce damage in battle.")
    print("- 'use potion': Heal yourself if you have a potion.")
    print("- 'check status': View your HP, Stamina, XP, and Gold.")
    print("- 'shop': Visit the shop to buy items.")
    print("- 'exit': Quit the game.")
    print("\nLet the adventure begin!")
    
    context = "You are in a mysterious forest. There is a path to the north and a dark cave to the south. What do you want to do?"
    
    while True:
        print("\nAI: ", context)
        user_input = input("\n>> ")
        
        if user_input.lower() == "exit":
            print("\nThanks for playing!")
            break
        elif user_input.lower() == "go north":
            context = "You find a hidden village. People here seem friendly."
        elif user_input.lower() == "go south":
            battle()
            context = "After the battle, you find a treasure chest."
        elif user_input.lower() == "check status":
            check_status()
            continue
        elif user_input.lower() == "shop":
            shop_system()
            continue
        else:
            prompt = f"{context}\nPlayer chooses: {user_input}. What happens next?"
            context = ai_response(prompt)

if __name__ == "__main__":
    main()
