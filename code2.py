import time

def print_slow(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.05)
    print()

def introduction():
    print_slow("Welcome to the Adventure Game!")
    print_slow("You find yourself in a mysterious forest.")
    print_slow("Your goal is to find the treasure hidden deep within.")
    print_slow("Let the adventure begin!")

def choose_path():
    print_slow("You come to a fork in the road. Do you go left or right?")
    choice = input("Enter 'left' or 'right': ").lower()
    if choice == 'left':
        print_slow("You head left and stumble upon a river.")
        return 'river'
    elif choice == 'right':
        print_slow("You go right and find an old bridge.")
        return 'bridge'
    else:
        print_slow("Invalid choice. Please enter 'left' or 'right'.")
        return choose_path()

def explore_river():
    print_slow("You approach the river and see a boat.")
    print_slow("Do you want to take the boat or swim across?")
    choice = input("Enter 'boat' or 'swim': ").lower()
    if choice == 'boat':
        print_slow("You take the boat and safely reach the other side.")
        return 'cave'
    elif choice == 'swim':
        print_slow("You decide to swim but get caught in a strong current.")
        print_slow("You're swept away and can't continue.")
        return 'game_over'
    else:
        print_slow("Invalid choice. Please enter 'boat' or 'swim'.")
        return explore_river()

def explore_bridge():
    print_slow("You cautiously walk across the creaky bridge.")
    print_slow("Halfway through, the bridge starts to collapse!")
    print_slow("Do you run back or try to jump to the other side?")
    choice = input("Enter 'run' or 'jump': ").lower()
    if choice == 'run':
        print_slow("You run back just in time, avoiding the collapse.")
        return 'forest'
    elif choice == 'jump':
        print_slow("You take a leap of faith and barely make it to the other side.")
        return 'cave'
    else:
        print_slow("Invalid choice. Please enter 'run' or 'jump'.")
        return explore_bridge()

def explore_cave():
    print_slow("You enter a dark cave with a faint glow deeper inside.")
    print_slow("You can hear water droplets echoing.")
    print_slow("Do you want to proceed deeper into the cave or turn back?")
    choice = input("Enter 'proceed' or 'turn back': ").lower()
    if choice == 'proceed':
        print_slow("You venture deeper and find a chest full of treasure!")
        return 'victory'
    elif choice == 'turn back':
        print_slow("You decide to turn back and exit the cave.")
        return 'forest'
    else:
        print_slow("Invalid choice. Please enter 'proceed' or 'turn back'.")
        return explore_cave()

def main():
    introduction()
    current_location = choose_path()

    if current_location == 'river':
        current_location = explore_river()

    if current_location == 'bridge':
        current_location = explore_bridge()

    if current_location == 'cave':
        current_location = explore_cave()



if __name__ == "__main__":
    main()
