import os


class CLIManager:
    def __init__(self, engine):
        self.engine = engine
        # Map pieces to clean terminal icons
        self.icons = {
            "white": {
                "Pawn": "♙",
                "Rook": "♖",
                "Knight": "♘",
                "Bishop": "♗",
                "Queen": "♕",
                "King": "♔",
            },
            "black": {
                "Pawn": "♟",
                "Rook": "♜",
                "Knight": "♞",
                "Bishop": "♝",
                "Queen": "♛",
                "King": "♚",
            },
        }

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def draw_board(self):
        grid = self.engine.board.grid
        print("\n    a b c d e f g h")
        print("  +-----------------+")
        for r in range(8):
            row_str = f"{8 - r} | "
            for c in range(8):
                piece = grid[r][c]
                if piece:
                    row_str += self.icons[piece.color][piece.name] + " "
                else:
                    row_str += ". "
            print(row_str + f"| {8 - r}")
        print("  +-----------------+")
        print("    a b c d e f g h\n")

        if self.engine.is_in_check("white"):
            print(">>> WHITE KING IS IN CHECK! <<<")
        elif self.engine.is_in_check("black"):
            print(">>> BLACK KING IS IN CHECK! <<<")

    def get_user_input(self):
        turn = "White" if self.engine.white_to_move else "Black"
        move_str = input(f"{turn}'s move (e.g., e2e4) or 'q' to quit: ").strip().lower()
        return move_str

    def parse_coordinates(self, move_str):
        """Converts algebraic 'e2e4' to array indices ((6, 4), (4, 4))"""
        try:
            col_map = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
            start_col = col_map[move_str[0]]
            start_row = 8 - int(move_str[1])
            end_col = col_map[move_str[2]]
            end_row = 8 - int(move_str[3])
            return (start_row, start_col), (end_row, end_col)
        except Exception:
            return None
