import unittest
import main

class Tests(unittest.TestCase):

    def setUp(self):
        main.app.testing = True
        self.app = main.app.test_client()

    def test_home(self):
        result = self.app.get('/')
        #testing False Negative
        self.assertFalse(result)

    def test_tables(self):
        result = self.app.get('/tables')
        self.assertTrue(result)
    
    def test_profiles(self):
        result = self.app.get('/profiles')
        self.assertTrue(result)

    def test_sortWin(self):
        result = self.app.get('/sort_win')
        self.assertTrue(result)

    def test_sortValue(self):
        result = self.app.get('/sort_value')
        self.assertTrue(result)

    def test_calculation(self):
        result = main.Player.calculateMarketValue()
        self.assertTrue(result)
    
if __name__ == '__main__':
    unittest.main()