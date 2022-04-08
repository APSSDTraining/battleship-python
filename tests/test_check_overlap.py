import unittest
from torpydo import battleship
from torpydo.game_controller import GameController
from torpydo.ship import Color, Letter, Position, Ship


def init_ship(ship: Ship, positions: list):
    ship.positions = positions
    return ship


class TestCheckIsHorizontalVertical(unittest.TestCase):
    def test_OverlapEmpty_NewPositionA2_Valid(self):
        myFleet = []
        newPosition = Position(Letter.A, 2)
        self.assertTrue(battleship.check_overlap(myFleet, newPosition))

    def test_OverlapA1A2_NewPositionA2_Valid(self):
        myFleet = []
        ship = init_ship(Ship("Test", 5, Color.RED), [
            Position(Letter.A, 1), Position(Letter.A, 2)])
        myFleet.append(ship)
        newPosition = Position(Letter.A, 2)
        self.assertFalse(battleship.check_overlap(myFleet, newPosition))

    # def test_ShipA1A2_NewPositionB2_Invalid(self):
    #     ship = init_ship(Ship("Test", 5, Color.RED), [Position(Letter.A,1), Position(Letter.A,2)])
    #     newPosition = Position(Letter.B, 2)
    #     self.assertFalse(GameController.check_is_horizontal_vertical(ship, newPosition))
    # def test_Empty_NewPositionB2_Valid(self):
    #     ship = init_ship(Ship("Test", 5, Color.RED), [])
    #     newPosition = Position(Letter.B, 2)
    #     self.assertTrue(GameController.check_is_horizontal_vertical(ship, newPosition))


if '__main__' == __name__:
    unittest.main()
