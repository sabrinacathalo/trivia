#!/usr/bin/env python3

class Game:
    def __init__(self):
        self.players = []
        self.players_leaderboard = []
        self.places = [0] * 6
        self.purses = [0] * 6
        self.in_penalty_box = [0] * 6
        self.pop_questions = []
        self.science_questions = []
        self.sports_questions = []
        self.rock_questions = []
        self.number_correct_question = [];

        self.jocker_was_used = dict()

        self.current_player = 0
        self.nextCategory = None
        self.is_getting_out_of_penalty_box = False

        for i in range(50):
            self.pop_questions.append("Pop Question %s" % i)
            self.science_questions.append("Science Question %s" % i)
            self.sports_questions.append("Sports Question %s" % i)
            self.rock_questions.append(self.create_rock_question(i))

    def create_rock_question(self, index):
        return "Rock Question %s" % index

    def is_playable(self):
        return self.how_many_players >= 2

    def add(self, player_name):
        self.players.append(player_name)
        self.places[self.how_many_players] = 0
        self.purses[self.how_many_players] = 0
        self.in_penalty_box[self.how_many_players] = False
        self.number_correct_question.append(0)
        self.jocker_was_used[self.how_many_players-1] = False
        print(player_name + " was added")
        print("They are player number %s" % len(self.players))

        return True

    @property
    def how_many_players(self):
        return len(self.players)

    def roll(self, roll):
        print("%s is the current player" % self.players[self.current_player])
        print("They have rolled a %s" % roll)

        if self.in_penalty_box[self.current_player]:
            if roll % 2 != 0:
                self.is_getting_out_of_penalty_box = True

                print("%s is getting out of the penalty box" % self.players[self.current_player])
                self.places[self.current_player] = self.places[self.current_player] + roll
                if self.places[self.current_player] > 11:
                    self.places[self.current_player] = self.places[self.current_player] - 12

                print(self.players[self.current_player] + \
                            '\'s new location is ' + \
                            str(self.places[self.current_player]))
                print("The category is %s" % self._current_category)
                self._ask_question()
            else:
                print("%s is not getting out of the penalty box" % self.players[self.current_player])
                self.is_getting_out_of_penalty_box = False
        else:
            self.places[self.current_player] = self.places[self.current_player] + roll
            if self.places[self.current_player] > 11:
                self.places[self.current_player] = self.places[self.current_player] - 12

            print(self.players[self.current_player] + \
                        '\'s new location is ' + \
                        str(self.places[self.current_player]))
            print("The category is %s" % self._current_category)
            self._ask_question()

    def _ask_question(self):
        if self._current_category == 'Pop': print(self.pop_questions.pop(0))
        if self._current_category == 'Science': print(self.science_questions.pop(0))
        if self._current_category == 'Sports': print(self.sports_questions.pop(0))
        if self._current_category == 'Rock': print(self.rock_questions.pop(0))

    @property
    def _current_category(self):

        if self.nextCategory is not None: return self.nextCategory

        if self.places[self.current_player] == 0: return 'Pop'
        if self.places[self.current_player] == 4: return 'Pop'
        if self.places[self.current_player] == 8: return 'Pop'
        if self.places[self.current_player] == 1: return 'Science'
        if self.places[self.current_player] == 5: return 'Science'
        if self.places[self.current_player] == 9: return 'Science'
        if self.places[self.current_player] == 2: return 'Sports'
        if self.places[self.current_player] == 6: return 'Sports'
        if self.places[self.current_player] == 10: return 'Sports'
        return 'Rock'

    def was_jocker_used(self):

        if (self.jocker_was_used[self.current_player] == False):
            if self.in_penalty_box[self.current_player]:
                if self.is_getting_out_of_penalty_box:
                    print('Question was skipped')
                    self.jocker_was_used[self.current_player] = True
                    winner = self._did_player_win()
                    self.current_player += 1
                    if self.current_player == len(self.players): self.current_player = 0


                    return winner
                else:
                    self.current_player += 1
                    if self.current_player == len(self.players): self.current_player = 0
                    return True
            else:
                print("Question was skipped")
                winner = self._did_player_win()
                self.jocker_was_used[self.current_player] = True
                self.current_player += 1
                if self.current_player == len(self.players): self.current_player = 0
                return winner

        if self.jocker_was_used[self.current_player]:
            print("You have already use your jocker")
            return True

    def was_correctly_answered(self):
        self.nextCategory = None
        if self.in_penalty_box[self.current_player]:
            if self.is_getting_out_of_penalty_box:
                print('Answer was correct!!!!')
                self.purses[self.current_player] += 1
                print(self.players[self.current_player] + \
                    ' now has ' + \
                    str(self.purses[self.current_player]) + \
                    ' Gold Coins.')

                winner = self._did_player_win()
                self.current_player += 1
                if self.current_player == len(self.players): self.current_player = 0

                return winner
            else:
                self.current_player += 1
                if self.current_player == len(self.players): self.current_player = 0
                return True

        else:

            print("Answer was correct!!!!")
            self.number_correct_question[self.current_player] += 1;
            if(self.number_correct_question[self.current_player]==3):
                    choosenPlayerName = ""
                    while choosenPlayerName not in self.players:
                        print("Choose a player to send in prison between "+str(self.players));
                        choosenPlayerName = input("Choose ? : "+str(self.players))
                        try:
                            if self.current_player == self.players.index(choosenPlayerName):
                                print("You can't send yourself to penalty box !")
                                choosenPlayerName = ""
                        except ValueError:
                            print("Write a valid choice")
                    print(self.players[self.players.index(choosenPlayerName)] + " was sent to the penalty box")
                    self.in_penalty_box[self.players.index(choosenPlayerName)] = True
                    self.number_correct_question[self.current_player] = 0
            self.purses[self.current_player] += 1
            print(self.players[self.current_player] + \
                ' now has ' + \
                str(self.purses[self.current_player]) + \
                ' Gold Coins.')

            winner = self._did_player_win()
            self.current_player += 1
            if self.current_player == len(self.players): self.current_player = 0

            return winner

    def wrong_answer(self):
        print('Question was incorrectly answered')

        while self.nextCategory not in ["Pop", "Science", "Sports", "Rock"]:
            self.nextCategory = input("next category ? : [Pop, Science, Sports, Rock]" )

        print(self.players[self.current_player] + " was sent to the penalty box")
        self.in_penalty_box[self.current_player] = True

        self.current_player += 1
        if self.current_player == len(self.players): self.current_player = 0
        return True

    def _did_player_win(self):
        if self.purses[self.current_player] == 6:
            self.players_leaderboard.append(self.current_player)
            print(self.players[(self.current_player)] + ' a gagné !!!')

        return not (self.purses[self.current_player] == 6 and len(self.players_leaderboard) == len(self.players))

from gettext import bind_textdomain_codeset
from random import randrange

if __name__ == '__main__':
    not_a_winner = False

    game = Game()
        
    game.add('Chet')
    game.add('Pat')
    game.add('Sue')

    while True:

        game.roll(randrange(5) + 1)

        if game.jocker_was_used[game.current_player]:
            jocker = 'N'
        else:
            jocker = input('skip question ? (Y/N) : ')
            print(jocker)

        if jocker == 'Y':
            not_a_winner = game.was_jocker_used()

        if jocker == 'N':
            if randrange(9) == 7:
                not_a_winner = game.wrong_answer()
            else:
                not_a_winner = game.was_correctly_answered()

        if not not_a_winner: break
        
    for x in game.players_leaderboard:
        print(str(x+1) + 'st : ' + str(game.players[game.players_leaderboard[x-1]])) 
  
