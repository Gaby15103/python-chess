from engine import ChessEngine

class ChessApp:
    def __init__(self):
        self.engine = ChessEngine() # This is the "Brain"
        self.view_mode = "2D"

    def handle_click(self, x, y):
        # 1. Translate click to (row, col)
        # 2. Ask engine: "Can I move here?"
        if self.engine.is_legal(start, end):
            self.engine.make_move(start, end)
            self.redraw_board()
