import unittest
import pytest
import client
import json


def test_pong():
    assert client.pong == b'{"response": "pong"}'

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_pong)
    runner = unittest.TextTestRunner()
    exit(not runner.run(suite).wasSuccessful())