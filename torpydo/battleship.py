import random
import os
import colorama
import platform

from colorama import Fore, Back, Style
from torpydo.ship import Color, Letter, Position, Ship
from torpydo.game_controller import GameController
from torpydo.telemetryclient import TelemetryClient

print("Starting")

myFleet = []
enemyFleet = []


def main():
    TelemetryClient.init()
    TelemetryClient.trackEvent('ApplicationStarted', {
                               'custom_dimensions': {'Technology': 'Python'}})
    colorama.init()
    print(Fore.YELLOW + r"""
                                    |__
                                    |\/
                                    ---
                                    / | [
                             !      | |||
                           _/|     _/|-++'
                       +  +--|    |--|--|_ |-
                     { /|__|  |/\__|  |--- |||__/
                    +---------------___[}-_===_.'____                 /\
                ____`-' ||___-{]_| _[}-  |     |_[___\==--            \/   _
 __..._____--==/___]_|__|_____________________________[___\==--____,------' .7
|                        Welcome to Battleship                         BB-61/
 \_________________________________________________________________________|""" + Style.RESET_ALL)

    initialize_game()

    start_game()


def start_game():
    global myFleet, enemyFleet
    # clear the screen
    if(platform.system().lower() == "windows"):
        cmd = 'cls'
    else:
        cmd = 'clear'
    os.system(cmd)
    print(r'''
                  __
                 /  \
           .-.  |    |
   *    _.-'  \  \__/
    \.-'       \
   /          _/
   |      _  /
   |     /_\
    \    \_/
     """"""""''')
    while True:
        print()
        print(Fore.GREEN + "Player, it's your turn" + Style.RESET_ALL)
        position = parse_position(
            input(Fore.MAGENTA + "Enter coordinates for your shot:" + Style.RESET_ALL))
        is_hit = GameController.check_is_hit(enemyFleet, position)
        if is_hit:
            print(Fore.RED + r'''
                \          .  ./
              \   .:"";'.:..""   /
                 (M^^.^~~:.'"").
            -   (/  .    . . \ \)  -
               ((| :. ~ ^  :. .|))
            -   (\- |  \ /  |  /)  -
                 -\  \     /  /-
                   \  \   /  /''' + Style.RESET_ALL)

        print(Fore.RED + "Yeah ! Nice hit !" +
              Style.RESET_ALL if is_hit else Fore.BLUE + "Miss")

        isDestroyed = GameController.check_is_destroyed(enemyFleet)
        if isDestroyed:
            print(Fore.GREEN+"You sunk their " + isDestroyed+Style.RESET_ALL)
        ships_left = GameController.get_alive(enemyFleet)
        print(Fore.GREEN+', '.join(str(e) for e in ships_left)+Style.RESET_ALL)
        print(Fore.WHITE + "##################################################################################" + Style.RESET_ALL)
        TelemetryClient.trackEvent('Player_ShootPosition', {'custom_dimensions': {
                                   'Position': str(position), 'IsHit': is_hit}})

        position = get_random_position()
        is_hit = GameController.check_is_hit(myFleet, position)
        print()
        print(Fore.GREEN + f"Computer shoot in {str(position)}")
        if is_hit:
            print(Fore.RED + "and hits your Ship!")
        else:
            print(Fore.BLUE + "Miss")
        print(Fore.WHITE + "##################################################################################" + Style.RESET_ALL)
        TelemetryClient.trackEvent('Computer_ShootPosition', {'custom_dimensions': {
                                   'Position': str(position), 'IsHit': is_hit}})
        if is_hit:
            print(Fore.RED + r'''
                \          .  ./
              \   .:"";'.:..""   /
                 (M^^.^~~:.'"").
            -   (/  .    . . \ \)  -
               ((| :. ~ ^  :. .|))
            -   (\- |  \ /  |  /)  -
                 -\  \     /  /-
                   \  \   /  / ''' + Style.RESET_ALL)


def parse_position(input: str):
    letter = Letter[input.upper()[:1]]
    number = int(input[1:])
    position = Position(letter, number)

    return Position(letter, number)


def get_random_position():
    rows = 8
    lines = 8

    letter = Letter(random.randint(1, lines))
    number = random.randint(1, rows)
    position = Position(letter, number)

    return position


def initialize_game():
    initialize_myFleet()

    initialize_enemyFleet()


def initialize_myFleet():
    global myFleet

    myFleet = GameController.initialize_ships()

    print(Fore.GREEN + "Please position your fleet (Game board has size from A to H and 1 to 8) :" + Style.RESET_ALL)

    for ship in myFleet:
        print()
        print(Fore.GREEN +
              f"Please enter the positions for the {ship.name} (size: {ship.size})" + Style.RESET_ALL)

        for i in range(ship.size):
            is_valid = "invalid"
            while(is_valid != ""):
                position_input = input(Fore.MAGENTA +
                                       f"Enter position {i+1} of {ship.size} (i.e A3):"+Style.RESET_ALL)
                is_valid = validPosition(myFleet, position_input, ship)
                if (is_valid != ""):
                    print(is_valid)
            ship.add_position(position_input)
            TelemetryClient.trackEvent('Player_PlaceShipPosition', {'custom_dimensions': {
                                       'Position': position_input, 'Ship': ship.name, 'PositionInShip': i}})


def initialize_enemyFleet():
    global enemyFleet

    enemyFleet = GameController.initialize_ships()

    enemyFleet[0].positions.append(Position(Letter.B, 4))
    enemyFleet[0].positions.append(Position(Letter.B, 5))
    enemyFleet[0].positions.append(Position(Letter.B, 6))
    enemyFleet[0].positions.append(Position(Letter.B, 7))
    enemyFleet[0].positions.append(Position(Letter.B, 8))

    enemyFleet[1].positions.append(Position(Letter.E, 6))
    enemyFleet[1].positions.append(Position(Letter.E, 7))
    enemyFleet[1].positions.append(Position(Letter.E, 8))
    enemyFleet[1].positions.append(Position(Letter.E, 9))

    enemyFleet[2].positions.append(Position(Letter.A, 3))
    enemyFleet[2].positions.append(Position(Letter.B, 3))
    enemyFleet[2].positions.append(Position(Letter.C, 3))

    enemyFleet[3].positions.append(Position(Letter.F, 8))
    enemyFleet[3].positions.append(Position(Letter.G, 8))
    enemyFleet[3].positions.append(Position(Letter.H, 8))

    enemyFleet[4].positions.append(Position(Letter.C, 5))
    enemyFleet[4].positions.append(Position(Letter.C, 6))


def check_overlap(myFleet, new_position: Position):
    for ship in myFleet:
        for position in ship:
            if position == new_position:
                return False
    return True


def check_noGaps(current_ship: Ship, new_position: Position):
    return True


def check_correctSize(current_ship: Ship, new_position: Position):
    return True


def check_playingField(new_position: Position):
    return True


def validPosition(myFleet, new_position: Position, current_ship: Ship):
    return ""


if __name__ == '__main__':
    main()
