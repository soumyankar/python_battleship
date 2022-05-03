from re import X
from inputimeout import inputimeout, TimeoutOccurred
import random
import time
import os

class BattleshipBoard():
    """Class to maintain state and information about the running game"""
    battle_board = []
    user_guesses = []
    user_time_out = False
    game_over = False
    ships = {} # dict containing placements
    ship_hit_counter = 0
    num_of_ships_destroyed = 0
    y_axis = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self):
        self.battle_board_size = int(os.environ.get("GRID_SIZE", 8))
        self.num_battleships = 5
        self.battleship_size = int(os.environ.get("SHIP_SIZE", 4))
        self.bomb_count = 50
        self.debug = (int(os.environ.get("DEBUG", 0)) == 1) #Set to 1 for debug logging
        random.seed(time.time())


    @property
    def is_running(self):
        if self.game_over:
            return False
        if self.user_time_out:
            return False

        return True

    def display_message(self,message):
        print("")
        print("------------------------------------------------------------------------------------------")
        print(message)
        print("------------------------------------------------------------------------------------------")

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
                    return self.place_ship() # recursively move to next iteration
                else:
                    placement_positions.append(f"{y+i}{x}")
            else:
                if f"{y}{x+i}" in self.ships:
                    return self.place_ship()
                else:
                    placement_positions.append(f"{y}{x+i}")

        # no collisions, we can place the ship
        for s in range(len(placement_positions)):
            self.ships[placement_positions[s]] = True
    
        return True

    # So initially the battle_board should be initialized as:
    # 1 1 1 1 1 1
    # 1 1 1 1 1 1
    # ...
    # 1 1 1 1 1 1
    # Something like that, and when a element is bombed by user,
    # the element value changnes from 1 to 0.
    # Initial function to just print the battle_board
    def print_battle_board(self):
        """Will print the grid with rows A-J and columns 0-9"""

        # TODO: Determine what to print when: bombed water, bombed ship,
        # or not yet guessed by player
        
        for i in range(self.battle_board_size):
            print(self.y_axis[i], end=") ")
            for j in range(self.battle_board_size):
                # print(self.battle_board[i][j])
                if self.battle_board[i][j] == "O":
                    print(".", end=" ")
                elif self.debug and f"{i}{j}" in self.ships: # print ship placement
                    print("S", end=" ")
                else:
                    print(self.battle_board[i][j], end=" ")
            print("")

        print("  ", end=" ") # This signifies the x_axis spacing because the rows above will have "A) ", and thus we need a character spacign of 3 characters
        # Now we print the x_axis coordinates on the bottom of the board
        for i in range(len(self.battle_board[0])):
            print(str(i+1), end=" ")
        # The line below is done because of some random printing bug, this fixed it. Unsure how, can take a look further on.
        print("")

    def check_bomb_placement_validity(self, usr_input):
        usr_input = str(usr_input).upper()
        is_valid_bomb_target = False
        error_message = 'ERROR: Please Enter a valid row(A-H) and column(0-7). Example: A5'
        while is_valid_bomb_target is False:
            ## checks if the user_input if the length of user input is 2 or not
            if(len(usr_input) != 2):
                self.display_message(error_message)
                self.handle_user_input()
                break
            row = usr_input[0]
            col = usr_input[1]
            ## checks if the row is an alphabet and column is a number
            if(not row.isalpha() or not col.isnumeric()):
                self.display_message(error_message)
                self.handle_user_input()
                break
            row = self.y_axis.find(row)
            ##checks if the user entered row is outside of the battleboard
            if not (-1 < row < self.battle_board_size):
                self.display_message(error_message)
                self.handle_user_input()
                break
            col = int(col)
            ##checks if the user entered column is outside of the battleboard
            if not (-1 < col < self.battle_board_size):
                self.display_message(error_message)
                self.handle_user_input()
                break
            if self.battle_board[row][col] == "#" or self.battle_board[row][col] == "X":
                self.display_message("You have already shot a bomb here, pick somewhere else")
                self.handle_user_input()
                break
            if self.battle_board[row][col] == ".":
                is_valid_bomb_target = True
                self.bomb_count = self.bomb_count - 1
        return row,col


    ## updates the 8x8 board and the bomb count after the bomb is hit
    def update_battle_board_and_bomb_count(self, usr_input):
        row,col = self.check_bomb_placement_validity(usr_input)

        #checks if the row,col value matches the key is ships dictionary
        if (str(row)+str(col)) in self.ships:
            self.display_message("It's a hit!! A battleship was hit by your bomb.")
            self.ship_hit_counter += 1
            self.battle_board[row][col] = "X"
            if self.check_for_ship_destroyed(row, col):
                self.display_message("Hell Yeah!! A ship was completely destroyed!")
                self.num_of_ships_destroyed += 1
        else:
            self.display_message("It's a miss!! No battleship was hit.")
            self.battle_board[row][col] = "#"
        
    ## TODO checks if a ship is completely destroyed
    def check_for_ship_destroyed(self, row, col):
        """If all parts of a shit have been shot it is destroyed we increment the num_of_ships_destroyed counter by 1"""
        print("Hello I am a TODO")
       

    # 60 second timeout. Ideally input is stored in a (y, x) tuple but I aint yo momma
    def handle_user_input(self):
        self.nseconds = 60
        try:
            print(f'You have {self.bomb_count} bomb(s) left to take down {self.num_battleships} battleships')
            self.print_battle_board()
            usr_input = inputimeout(prompt='"Enter row (A-H) and column (0-7) such as A5: " ', timeout=self.nseconds)
            self.update_battle_board_and_bomb_count(usr_input)
            
        except TimeoutOccurred:
            print('timeout!',self.nseconds,'seconds passed')
            self.user_time_out = True

    def main_game_loop(self):
        """Main entry point of application that runs the game loop"""
        
        self.make_battle_board()    
        
        ## removed make_battle_board from the main game loop to prevent creating new board on every loop instance
        while self.is_running:
            # print("Attempt #1 at Battleships")
            self.handle_user_input()

            # self.bomb_count = 1 # temp debug code
            self.check_for_game_end_scenario()

    def check_for_game_end_scenario(self):
        if(self.ship_hit_counter >= self.num_battleships * self.battleship_size):
            print('Congratulations!! You have destroyed all the enemy battleships.')
            self.game_over = True
        elif(self.bomb_count <= 0):
            print('Game Over.You have depleted all of your remaining bombs.')
            self.game_over = True         


if __name__ == '__main__':
    battleship = BattleshipBoard()
    battleship.main_game_loop()
    

    
