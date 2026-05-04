class Piece:
    def __init__(self, color, name, position):
        self.color = color
        self.name = name
        self.position = position
        self.has_moved = False

    def __str__(self):
        return f"{self.color[0]}{self.name[0]}"

class Knight(Piece):
    def get_valid_moves(self, board_grid):
        moves = []
        directions = [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]
        r, c = self.position
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target = board_grid[nr][nc]
                if target is None or target.color != self.color:
                    moves.append((nr, nc))
        return moves

class Pawn(Piece):
    def get_valid_moves(self, board_grid):
        # Basic pawn logic would go here
        return []

cclass ChessBoard:
    def __init__(self):
        # The grid is the "physical" source of truth
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup_pieces()

    def setup_pieces(self):
        # Example: Placing Knights
        self.grid[0][1] = Knight('white', 'Knight', (0, 1))
        self.grid[0][6] = Knight('white', 'Knight', (0, 6))
        self.grid[7][1] = Knight('black', 'Knight', (7, 1))
        self.grid[7][6] = Knight('black', 'Knight', (7, 6))

    def move_piece(self, move):
        # Physically update the grid
        self.grid[move.start_row][move.start_col] = None
        self.grid[move.end_row][move.end_col] = move.piece_moved
        # Update the piece object itself
        move.piece_moved.position = (move.end_row, move.end_col)
        move.piece_moved.has_moved = True

    def undo_piece_move(self, move):
        self.grid[move.start_row][move.start_col] = move.piece_moved
        self.grid[move.end_row][move.end_col] = move.piece_captured
        move.piece_moved.position = (move.start_row, move.start_col)

class Move:
    def __init__(self, start_sq, end_sq, grid):
        self.start_row, self.start_col = start_sq
        self.end_row, self.end_col = end_sq
        self.piece_moved = grid[self.start_row][self.start_col]
        self.piece_captured = grid[self.end_row][self.end_col]

class ChessEngine:
    def __init__(self):
        self.board = ChessBoard()
        self.white_to_move = True
        self.move_log = []

    def reset_board(self):
        """Places pieces in their starting positions."""
        # This is where you would fill self.board[0][0], etc.
        pass

    def make_move(self, start_sq, end_sq):
        move = Move(start_sq, end_sq, self.board.grid)

        # Check turn logic
        if move.piece_moved and move.piece_moved.color == ('white' if self.white_to_move else 'black'):
            self.board.move_piece(move)
            self.move_log.append(move)
            self.white_to_move = not self.white_to_move
            return True
        return False

   def undo(self):
        if self.move_log:
            move = self.move_log.pop()
            self.board.undo_piece_move(move)
            self.white_to_move = not self.white_to_move

    def get_valid_moves(self):
        """
        The 'Heavy Lifter'. It looks at every piece and
        returns a list of legal moves, accounting for 'Check'.
        """
        moves = []
        # 1. Generate all 'suggested' moves for the current player
        # 2. Filter out moves that leave your King in danger
        return moves

    def undo_move(self):
        """Pops the last move from the log and reverts the board."""
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move

