import unittest
import clienttestpath
import pytest

def test_pong():
    assert clienttestpath.pong() == b'{"response": "pong"}'

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_pong)
    runner = unittest.TextTestRunner()
    exit(not runner.run(suite).wasSuccessful())