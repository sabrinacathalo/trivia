import unittest
from trivia import Game
import datetime

class TestGameMethods(unittest.TestCase):

    def test_rock_at_12_hours(self):

        game = Game()
        
        class NewDate(datetime.datetime):
            @classmethod
            def now(cls):
                return cls(2010, 1, 1, 12)
        datetime.datetime = NewDate
        now = datetime.datetime.now()

        game.places = [3]
        game.current_player = 0

        print(now)
        print(game._current_category)

        self.assertEqual(game._current_category, "Rock")

if __name__ == '__main__':
    unittest.main()