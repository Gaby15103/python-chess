from chess_engine import ChessEngine
from cli_manager import CLIManager


def main():

    engine = ChessEngine()  # This is the "Brain"
    ui = CLIManager(engine)
    view_mode = "CLI"

    while True:
        ui.clear_screen()
        ui.draw_board()

        status = engine.check_game_over()
        if status == "checkmate":
            winner = "Black" if engine.white_to_move else "White"
            print(f"CHECKMATE! {winner} wins!")
            break
        elif status == "stalemate":
            print("STALEMATE! It's a draw.")
            break

        move_str = ui.get_user_input()

        if move_str == "q":
            print("Thanks for playing!")
            break

        coords = ui.parse_coordinates(move_str)

        if coords:
            start, end = coords
            # Try to make the move
            piece = engine.board.grid[start[0]][start[1]]
            promotion_choice = "Queen"
            if piece and piece.name == "Pawn" and (end[0] == 0 or end[0] == 7):
                promotion_choice = input("Promote to (Q/R/B/N): ").upper()
                mapping = {"Q": "Queen", "R": "Rook", "B": "Bishop", "N": "Knight"}
                promotion_choice = mapping.get(promotion_choice, "Queen")
            success = engine.make_move(start, end)
            if not success:
                input("Invalid move! Press Enter to try again...")
        else:
            input("Format error (use e2e4)! Press Enter to try again...")

    def handle_click(self, x, y):
        if self.engine.is_legal(start, end):
            self.engine.make_move(start, end)
            self.redraw_board()


if __name__ == "__main__":
    main()
