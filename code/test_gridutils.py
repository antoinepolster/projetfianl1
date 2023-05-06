import unittest
import gridutils
import pytest

class TestUtils(unittest.TestCase):
    def test_turn_tile(self):
        assert gridutils.turn_tile({'N': True, 'E': True, 'S': False, 'W': False, 'item': 20}) == {'N': False, 'E': True, 'S': True, 'W': True, 'item': 20}

    def test_turn4(self):
        assert gridutils.turn4({'N': True, 'E': True, 'S': False, 'W': False, 'item': 12}) == [{'N': True, 'E': True, 'S': False, 'W': False, 'item': 12}, {'N': True, 'E': False, 'S': False, 'W': True, 'item': 12}, {'N': False, 'E': False, 'S': True, 'W': True, 'item': 12}, {'N': False, 'E': True, 'S': True, 'W': False, 'item': 12}]

    def test_new_postion(self):
        assert gridutils.new_position([0]) == 0

    def test_add(self):
        assert gridutils.add((0, 0), (-1, 0)) == (-1, 0)

    def test_index2coords(self):
        assert gridutils.index2coords(47) == (6, 5)

    #def isCoordsValid(self): 

    #def coords2index(self):

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtils)
    runner = unittest.TextTestRunner()
    exit(not runner.run(suite).wasSuccessful())