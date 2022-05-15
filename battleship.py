from inputimeout import inputimeout, TimeoutOccurred
import random
import time
import os
import sys


class BattleshipBoard():
    """Class to maintain state and information about the running game"""
    battle_board = []
    user_guesses = []
    user_time_out = False
    game_over = False
    ships = {}  # dict containing placements
    num_of_ships_destroyed = 0
    y_axis = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self):
        self.battle_board_size = int(os.environ.get("GRID_SIZE", 8))
        self.num_battleships = 5
        self.battleship_size = int(os.environ.get("SHIP_SIZE", 4))
        self.bomb_count = 50
        self.debug = (int(os.environ.get("DEBUG", 0)) ==
                      1)  # Set to 1 for debug logging
        self.writer = BoardPrinter()
        random.seed(time.time())

    @property
    def is_running(self):
        if self.game_over:
            return False
        if self.user_time_out:
            return False

        return True

    def display_message(self, message):

        self.writer.add_message_line(
            "------------------------------------------------------------------------------------------")
        self.writer.add_message_line(message)
        if self.num_of_ships_destroyed > 0:
            self.writer.add_message_line(
                f'Ships destroyed: {self.num_of_ships_destroyed}/5')
        self.writer.add_message_line(
            "------------------------------------------------------------------------------------------")

    def make_battle_board(self):
        rows, cols = (self.battle_board_size, self.battle_board_size)

        for i in range(rows):
            new_row = []
            for j in range(cols):
                new_row.append(".")
            self.battle_board.append(new_row)

        for i in range(self.num_battleships):
            self.place_ship()

    # Random roll between 0-1 to determine verticality, then place ship
    # at either ([y][x], [y+1][x]), or ([y][x], [y][x+1])
    # after checking if a ship is in that position and the board bounds
    def place_ship(self):
        # don't allow out of bounds, by only allowing placement at border - N - 1
        y = random.randrange(self.battle_board_size-(self.battleship_size-1))
        x = random.randrange(self.battle_board_size-(self.battleship_size-1))
        is_vertical = (random.choice([0, 1]) == 1)
        placement_positions = []

        for i in range(self.battleship_size):
            if is_vertical:
                # if a ship exists in the spot then reroll
                if f"{y+i}{x}" in self.ships:
                    return self.place_ship()  # recursively move to next iteration
                else:
                    placement_positions.append(f"{y+i}{x}")
            else:
                if f"{y}{x+i}" in self.ships:
                    return self.place_ship()
                else:
                    placement_positions.append(f"{y}{x+i}")

        # no collisions, we can place the ship
        # Ship values are the entire array of positions,
        # this is so each key returns the full ship
        for s in range(len(placement_positions)):
            self.ships[placement_positions[s]] = {
                "hit": False,
                "positions": placement_positions
            }

        return True

    # So initially the battle_board should be initialized as:
    # 1 1 1 1 1 1
    # 1 1 1 1 1 1
    # ...
    # 1 1 1 1 1 1
    # Something like that, and when a element is bombed by user,
    # the element value changes from 1 to 0.
    # Initial function to just print the battle_board
    def print_battle_board(self):
        """Will print the grid with rows A-J and columns 0-9"""

        # TODO: Determine what to print when: bombed water, bombed ship,
        # or not yet guessed by player

        for i in range(self.battle_board_size):
            board_line = ""
            board_line += self.y_axis[i] + ") "
            for j in range(self.battle_board_size):
                if self.battle_board[i][j] == "O":
                    board_line += ". "
                # print ship placement
                elif self.debug and f"{i}{j}" in self.ships and not self.ships[f"{i}{j}"]["hit"]:
                    board_line += "S "
                else:
                    board_line += self.battle_board[i][j] + " "
            self.writer.add_line(board_line)

        board_line = ""
        board_line += "   "  # This signifies the x_axis spacing because the rows above will have "A) ", and thus we need a character spacign of 3 characters
        # Now we print the x_axis coordinates on the bottom of the board
        for i in range(len(self.battle_board[0])):
            board_line += str(i+1) + " "

        self.writer.add_line(board_line)
        # The line below is done because of some random printing bug, this fixed it. Unsure how, can take a look further on.
        self.writer.write()

    def user_input_valid(self, usr_input, message):
        # not valid, should only have size 1 for letter, and 1 for number
        if(len(usr_input) < 2):
            self.display_message(message)
            return False

        return True

    def bomb_placement_valid(self, row, col, message):
        # checks if the row is an alphabet and column is a number
        if(not row.isalpha() or not col.isnumeric()):
            self.display_message(message)
            return False

        row = self.y_axis.find(row)
        # checks if the user entered row is outside of the battleboard
        if not (-1 < row < self.battle_board_size):
            self.display_message(message)
            return False

        col = int(col)-1  # off by one
        # checks if the user entered column is outside of the battleboard
        if not (-1 < col < self.battle_board_size):
            self.display_message(message)
            return False

        if self.battle_board[row][col] == "#" or self.battle_board[row][col] == "X":
            self.display_message(
                "You have already shot a bomb here, pick somewhere else")
            return False

        if self.battle_board[row][col] == ".":
            return True

        return False

    # updates the 8x8 board and the bomb count after the bomb is hit
    def update_battle_board_and_bomb_count(self, usr_input):
        error_message = 'ERROR: Please Enter a valid row(A-H) and column(1-8). Example: A5'
        if not self.user_input_valid(usr_input, error_message):
            return

        usr_input = str(usr_input).upper()
        row = usr_input[0]
        col = usr_input[1:]
        if not self.bomb_placement_valid(row, col, error_message):
            return
        else:
            self.bomb_count = self.bomb_count - 1

        row = self.y_axis.find(row)
        col = int(col)-1  # off by one

        # checks if the row,col value matches the key is ships dictionary
        if (str(row)+str(col)) in self.ships:
            self.display_message(
                "It's a hit!! A battleship was hit by your bomb.")
            self.battle_board[row][col] = "X"
            self.ships[f"{row}{col}"]["hit"] = True
            if self.check_for_ship_destroyed(row, col):
                self.num_of_ships_destroyed += 1
                self.display_message(
                    "Hell Yeah!! A ship was completely destroyed!")
        else:
            self.display_message("It's a miss!! No battleship was hit.")
            self.battle_board[row][col] = "#"

    # TODO checks if a ship is completely destroyed
    def check_for_ship_destroyed(self, row, col):
        """If all parts of a ship have been shot it is destroyed we increment the num_of_ships_destroyed counter by 1"""
        for pos in self.ships[f"{row}{col}"]["positions"]:
            if not self.ships[pos]["hit"]:
                return False

        return True

    def handle_user_input(self):
        self.nseconds = 60
        try:
            self.writer.add_line(
                f'You have {self.bomb_count} bomb(s) left to take down {self.num_battleships} battleships')
            self.print_battle_board()
            usr_input = inputimeout(
                prompt='"Enter row (A-H) and column (1-8) such as A5: " ', timeout=self.nseconds)
            self.update_battle_board_and_bomb_count(usr_input)

        except TimeoutOccurred:
            print('timeout!', self.nseconds, 'seconds passed')
            self.user_time_out = True

        # User has hit ctrl+c to exit the game
        except KeyboardInterrupt:
            self.writer.clear()
            self.writer.add_line("\n")
            self.display_message("Thanks for playing!")
            self.writer.write()
            self.game_over = True

    def main_game_loop(self):
        """Main entry point of application that runs the game loop"""

        self.make_battle_board()

        # removed make_battle_board from the main game loop to prevent creating new board on every loop instance
        while self.is_running:
            self.writer.add_line("Attempt #1 at Battleships")
            self.handle_user_input()

            # self.bomb_count = 1 # temp debug code
            self.check_for_game_end_scenario()

    def check_for_game_end_scenario(self):
        if(self.num_of_ships_destroyed >= self.num_battleships):
            print(
                f'Congratulations!! You have destroyed all the 5 enemy battleships with {self.bomb_count} bombs remaining.')
            self.game_over = True
        elif(self.bomb_count <= 0):
            print('Game Over. You have depleted all of your remaining bombs.')
            self.game_over = True


class BoardPrinter:
    lines = []
    message = []

    def add_line(self, line):
        self.lines.append(line)

    def add_message_line(self, line):
        self.message.append(line)

    def clear(self):
        self.lines = []
        self.message = []

    def write(self):
        for _ in range(50):  # 50 is arbitrary, but enough
            # move up cursor and delete whole line
            sys.stdout.write("\x1b[1A\x1b[2K")

        for i in range(len(self.lines)):
            sys.stdout.write(self.lines[i] + "\n")

        # write message after printing board
        for m in range(len(self.message)):
            sys.stdout.write(self.message[m] + "\n")

        # reset for next run
        self.clear()


if __name__ == '__main__':
    battleship = BattleshipBoard()
    battleship.main_game_loop()
