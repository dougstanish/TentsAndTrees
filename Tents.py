import random

import numpy as np

def find_valid_tents(board, tree_location):

    valid_tent_location = []

    board_size = len(board)

    y = tree_location[0]
    x = tree_location[1]

    # Up
    if y-1 >= 0:

        # If the location is empty
        if board[y-1, x] == '':
            up = np.clip((y-1) - 1, 0, board_size)
            down = np.clip((y-1) + 2, 0, board_size)
            left = np.clip(x - 1, 0, board_size)
            right = np.clip(x + 2, 0, board_size)
            surrounding_area = board[up:down, left:right]

            # If any contain a tent, return false
            if '^' not in surrounding_area:
                valid_tent_location.append((y-1, x))

    pass

def solver(board):

    col_sums = np.delete(board[len(board)-1], len(board)-1)

    print(board)

    board = np.delete(board, len(board)-1, axis=0)

    row_sums = board[:, len(board[0])-1]

    board = np.delete(board, len(board[0])-1, axis=1)





    pass


def get_change(cur_dir):
    """
    Based off of direction, returns the correct offset in X and Y
    @param cur_dir: The direction, with 0 being up, 1 being right, etc
    @return: The offset in Y and X
    """
    if cur_dir == 0:  # If direction is up
        return -1, 0
    elif cur_dir == 1:  # If direction is right
        return 0, 1
    elif cur_dir == 2:  # If direction is down
        return 1, 0
    else:  # If direction is left
        return 0, -1


def check_valid(board, random_pos, direction, board_size):
    """
    Checks a given location, and return if the tree and tent can be placed
    :param board: The tents and trees board
    :param random_pos: The position to place the tree
    :param direction: Which side of the tree to add the tent to
    :param board_size: The size of the board
    :return: True if it is a valid move, false otherwise
    """

    # If the pos is not a tent or tree
    if board[random_pos] == '':

        # Find offset, and the x and y values of the proposed tent
        offset = get_change(direction)
        y = random_pos[0] + offset[0]
        x = random_pos[1] + offset[1]

        # If the proposed tent is off the board, return false
        if y < 0 or y >= board_size or x < 0 or x >= board_size:
            return False
        else:

            # If the proposed tent location is not empty, return false
            if board[(y, x)] != '':
                return False

            # Check for tents around tent
            else:

                # Get values within 1 away from tent location
                up = np.clip(y-1, 0, board_size)
                down = np.clip(y+2, 0, board_size)
                left = np.clip(x-1, 0, board_size)
                right = np.clip(x+2, 0, board_size)
                surrounding_area = board[up:down, left:right]

                # If any contain a tent, return false
                if '^' in surrounding_area:
                    return False
                else:  # Otherwise valid move
                    return True
    else:
        return False


def generate_puzzle(boardsize=8, num_trees=12):
    valid_board = False

    board = np.zeros((boardsize, boardsize), dtype=str)

    random.seed(8675309)

    remaining_trees = num_trees

    while remaining_trees > 0:

        # remaining_trees = num_trees

        while remaining_trees >= 0:

            possible_directions = [0, 1, 2, 3]
            random.shuffle(possible_directions)

            tree_placed = False

            while len(possible_directions) != 0 and tree_placed is False:

                direction = possible_directions.pop()

                possible_indices = np.ndindex((boardsize, boardsize))
                possible_indices = list(possible_indices)
                random.shuffle(possible_indices)

                valid_placement = False

                while len(possible_indices) > 0 and not valid_placement:

                    random_pos = possible_indices.pop()

                    valid_placement = check_valid(board, random_pos, direction, boardsize)

                    if valid_placement:
                        board[random_pos] = 'T'

                        offset = get_change(direction)

                        y = random_pos[0] + offset[0]
                        x = random_pos[1] + offset[1]

                        board[(y, x)] = '^'

                        tree_placed = True

                        remaining_trees += -1

    column_tents = np.count_nonzero(board == '^', axis=0)
    row_tents = np.count_nonzero(board == '^', axis=1)

    board = np.append(board, [column_tents], axis=0)
    board = np.c_[board, np.append(row_tents, '')]


    solver(board)

    pass

def main():
    # TODO Verify num trees is valid

    generate_puzzle()


if __name__ == '__main__':
    main()
