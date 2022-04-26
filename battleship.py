import random
import time
# Global variable for battle_board
battle_board = [[]]
# Global variable for battle board size
# As per the assignment, we need a 8x8 board hence:
battle_board_size = 8
# Global variable for number of battleships to place
# As per assignment, we need to place 5 ships on board
num_of_battleships = 5
# Global variable for bombs_count
bomb_count = 50
# Global variable for game over
game_over = False
# Global variable for number of battle-ships destroyed
num_of_battleships_destroyed = 0
# Global variable for battleship_coordinates
battleship_coordinates = [[]]
# Cool way of printing a board with characters
# Global variable for y_axis
y_axis = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# So initially the battle_board should be initialized as:
# 1 1 1 1 1 1
# 1 1 1 1 1 1
# ...
# 1 1 1 1 1 1
# Something like that, and when a element is bombed by user,
# the element value changnes from 1 to 0.
# Initial function to just print the battle_board
def print_battle_board():
    """Will print the grid with rows A-J and columns 0-9"""
    global battle_board
    global y_axis

    # Splitting the Y_axis variables dependinng on how large the board size will be.
    y_axis = y_axis[0: len(battle_board) + 1]

    for i in range(len(battle_board)):
        print(y_axis[i], end=") ")
        for j in range(len(battle_board[i])):
            if battle_board[i][j] == "O":
                    print(".", end=" ")
            else:
                print(battle_board[i][j], end=" ")
        print("")

    print("  ", end=" ") # This signifies the x_axis spacing because the rows above will have "A) ", and thus we need a character spacign of 3 characters
    # Now we print the x_axis coordinates on the bottom of the board
    for i in range(len(battle_board[0])):
        print(str(i), end=" ")
    # The line below is done because of some random printing bug, this fixed it. Unsure how, can take a look further on.
    print("")

def make_battle_board():
    global battle_board
    global battle_board_size
    global num_of_battleships
    global battleship_coordinates

    random.seed(time.time())

    rows, cols = (battle_board_size, battle_board_size)

    battle_board = []
    for i in range(rows):
        new_row = []
        for j in range(cols):
            new_row.append(".")
        battle_board.append(new_row)

def main():
    """Main entry point of application that runs the game loop"""
    global game_over

    print("Attempt #1 at Battleships")
    print('You have %d bomb(s) left to take down %d battleships' % (bomb_count, num_of_battleships))

    make_battle_board()
    print_battle_board()
    # while game_over is False:
    #     print_grid()
    #     print("Number of ships remaining: " + str(num_of_ships - num_of_ships_sunk))
    #     print("Number of bullets left: " + str(bullets_left))
    #     shoot_bullet()
    #     print("----------------------------")
    #     print("")
    #     check_for_game_over()


if __name__ == '__main__':
    main()
