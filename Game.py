import numpy as np
import os

ROWS = 10
COLUMNS = 10
# TO-DO: Properly inherit Game.rows and Game.columns
# for Player.board


class Game:
    def __init__(self):
        self.rows = ROWS
        self.columns = COLUMNS

        self.players = []

        self.states = self.set_states()

    def set_players(self):
        """
        Function: set_players
        Output: A list of 2 Player objects whose names are set by user input.
        """
        for _ in range(2):
            name = input("Please enter your name, Player {}: ".format(_ + 1))
            self.players.append(Player(name))
        return None

    def allowed_ships(self):
        """
        Function: allowed_ships
        Output: 5 types of ships based on Milton Bradley's version
                of the rules of the game.
        Reference: https://en.m.wikipedia.org/wiki/Battleship_(game)
        """
        ships = {
            "Carrier": {"Length": 5, "Quantity": 1},
            "Battleship": {"Length": 4, "Quantity": 1},
            "Cruiser": {"Length": 3, "Quantity": 1},
            "Submarine": {"Length": 3, "Quantity": 1},
            "Destroyer": {"Length": 2, "Quantity": 1}
        }
        return ships

    def set_states(self):
        return {"Empty": 0,
                "Occupied": 1,
                "Miss": 2,
                "Hit": 3}

    def play(self):
        done = False
        while not done:
            for index in enumerate(self.players):
                print("It is now {}'s turn.\n"
                      .format(self.players[index].name))
                row = -1
                column = -1
                while not ((0 <= row <= 9) or (0 <= column <= 9)):
                    row, column = input("Please choose a tile to attack"
                                        "(row, column): ")
                self.players[(index + 1) % 2].board = self.attack(self,
                                                                  turn=index,
                                                                  row=row,
                                                                  column=column)
                print(self.players[(index + 1) % 2])
                print("End of turn.")

    def attack(self, turn, row, column):
        #   Get board of player being attacked
        #   Recall that index can be 0 or 1
        to_attack = self.players[(turn + 1) % 2].board
        if to_attack[(row, column)] == self.states["Empty"]:
            print("Nothing here!")
            to_attack[(row, column)] = self.states["Miss"]
        else:
            if to_attack[(row, column)] == self.states["Occupied"]:
                print("This tile was occupied! Good job!")
                to_attack[(row, column)] = self.states["Hit"]
        return to_attack


class Player(Game):
    def __init__(self, name):
        self.name = name

        self.fleet = Game.allowed_ships(Game)
        for ship in self.fleet:
            self.fleet[ship]["Sunk"] = 0

        self.board = np.zeros((ROWS, COLUMNS), dtype=np.int8)

    def set_board(self):
        print("We will not set the board for: ", self.name)
        choice = input("Type 'yes' if you would like to randomly populate"
                       " your board, or anything else to populate it yourself:"
                       " ")

        for ship in self.fleet:
            print("We will place your {}, whose size is: {}."
                  .format(ship, self.fleet[ship]['Length']))
            if choice.lower() == 'yes':
                pass
            else:
                occupied = False
                while not occupied:
                    row = -1
                    while not (0 <= row <= 9):
                        try:
                            row = int(input("Please enter the row you want"
                                            " this ship to start in: "))
                        except ValueError:
                            pass

                    column = -1
                    while not (0 <= column <= 9):
                        try:
                            column = int(input("Now the column: "))
                        except ValueError:
                            pass

                    if self.board[(row, column)] == 0:
                        self.board[(row, column)] = 1
                        occupied = True
                    else:
                        print("This tile is occupied by another ship."
                              " You need to pick another one.\n")
                orientation = input("Enter 'h' to place it horizontally,"
                                    "or anything else to do it "
                                    "vertically: ")
                if orientation.lower() == 'h':
                    for i in range(self.fleet[ship]['Length']):
                        self.board[(row, column + i)] = 1
                else:
                    for i in range(self.fleet[ship]['Length']):
                        self.board[(row + i, column)] = 1
            os.system('clear')
        print(self.board)


if __name__ == '__main__':
    game = Game()
    game.set_players()
    for player in game.players:
        player.set_board()
