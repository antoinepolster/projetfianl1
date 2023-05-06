import unittest
import clienttestpath
import pytest
import json

class TestUtils(unittest.TestCase):
    def test_pong(self):
        assert clienttestpath.pong() == json.dumps({'response': 'pong'}).encode()
        #pass

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtils)
    runner = unittest.TextTestRunner()
    exit(not runner.run(suite).wasSuccessful())
    #runner.run(suite)