import random

from torpydo.ship import Color, Letter, Position, Ship


class GameController(object):
    def check_is_hit(ships: list, shot: Position):
        if ships is None:
            raise ValueError('ships is null')

        if shot is None:
            raise ValueError('shot is null')

        for ship in ships:
            for position in ship.positions:
                if position == shot:
                    ship.hitPositions.append(shot)
                    if(len(ship.hitPositions) == len(ship.positions)):
                        ship.isDestroyed = True
                    
                    return True

        return False

    def get_alive(ships: list):
        if ships is None:
            raise ValueError('ships is null')

        alive_ships = []
        for ship in ships:
           if not ship.isDestroyed:
               alive_ships.append(ship.name)

        return alive_ships


    def check_is_destroyed(ships: list):
        if ships is None:
            raise ValueError('ships is null')

        for ship in ships:
            if(len(ship.hitPositions) == len(ship.positions)):
                return True

        return False

    def initialize_ships():
        return [
            Ship("Aircraft Carrier", 5, Color.CADET_BLUE),
            Ship("Battleship", 4, Color.RED),
            Ship("Submarine", 3, Color.CHARTREUSE),
            Ship("Destroyer", 3, Color.YELLOW),
            Ship("Patrol Boat", 2, Color.ORANGE)]

    def is_ship_valid(ship: Ship):
        is_valid = len(ship.positions) == ship.size

        return is_valid

    def get_random_position(size: int):
        letter = random.choice(list(Letter))
        number = random.randrange(size)
        position = Position(letter, number)

        return position
