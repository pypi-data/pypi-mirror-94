"""
This module will handle logic pertaining to calculation of control of
white and black over each square in the board
"""
import glob
from chess import pgn
from chess import parse_square
from chess import Board
from chess import WHITE
from chess import BLACK
from chess import SQUARE_NAMES
from chess import Move
from chess import KING

class ChessUtil:
    """Class to publish (num_white_control,num_black_control) tuple
    for each square for each ply"""

    @staticmethod
    def generate_ply_info_list_for_game(game):
        """Returns a dict which contains the list of tasks to
        be run and the number of plies for the game."""
        board = Board()
        ply_no = 0
        game_tasks = []
        for ply in game.mainline_moves():
            board.push(ply)
            for square in SQUARE_NAMES:
                new_board = board.copy()
                parsed_square = parse_square(square)
                ply_info = {"ply_no": ply_no, "square": parsed_square, "board": new_board}
                game_tasks.append(ply_info)
            ply_no = ply_no + 1

        return {"ply_info_list": game_tasks, "ply_count": ply_no}

    @staticmethod
    def find_control_for_square_for_color(ply_info, color):
        "Calculate the number of attackers for each square for a ply"
        board = ply_info["board"]
        parsed_square = ply_info["square"]
        attackers = board.attackers(color, parsed_square)
        if len(attackers) == 0:
            return 0

        power_of_square = 0
        new_board = board.copy()
        while len(attackers) != 0:
            attacker_list = list(attackers)
            attacking_square = attacker_list[0]

            if new_board.piece_type_at(attacking_square) == KING and len(attackers) > 1:
                attacking_square = attacker_list[1]
            elif new_board.piece_type_at(attacking_square) == KING and len(attackers) == 1:
                power_of_square = power_of_square + 1
                break
            new_board.remove_piece_at(attacking_square)
            power_of_square = power_of_square + 1
            attackers = new_board.attackers(color, parsed_square)
        return power_of_square

    @staticmethod
    def find_control_for_square(ply_info):
        "Find control for Black and White"
        power_of_square = {}
        power_of_square['square'] = ply_info['square']
        power_of_square["white"] = ChessUtil.find_control_for_square_for_color(ply_info, WHITE)
        power_of_square["black"] = ChessUtil.find_control_for_square_for_color(ply_info, BLACK)
        power_of_square['ply'] = ply_info['ply_no']
        return power_of_square

    @staticmethod
    def get_games_from_pgn_files():
        "Parse PGN files in the current directory and return a list of parsed game objects"
        game_list = []
        for file in glob.glob("resources/input/*.pgn"):
            file_handle = open(file)
            while True:
                game = pgn.read_game(file_handle)
                if game is None:
                    break
                game_list.append(game)
        return game_list
