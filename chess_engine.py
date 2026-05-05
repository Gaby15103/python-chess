class Piece:
    def __init__(self, color, name, position):
        self.color = color
        self.name = name
        self.position = position
        self.has_moved = False

    def __str__(self):
        return f"{self.color[0]}{self.name[0]}"

    def get_valid_moves(self, board_grid):
        raise NotImplementedError("Subclasses must implement get_valid_moves")

    def get_sliding_moves(self, board_grid, directions):
        """Helper for Rook, Bishop, and Queen"""
        moves = []
        r, c = self.position
        for dr, dc in directions:
            for i in range(1, 8):
                nr, nc = r + dr * i, c + dc * i
                if 0 <= nr < 8 and 0 <= nc < 8:
                    target = board_grid[nr][nc]
                    if target is None:
                        moves.append((nr, nc))
                    elif target.color != self.color:
                        moves.append((nr, nc)) # Capture
                        break
                    else:
                        break # Blocked by own piece
                else:
                    break # Off board
        return moves

class Pawn(Piece):
    def get_valid_moves(self, board_grid):
        moves = []
        r, c = self.position
        direction = -1 if self.color == 'white' else 1 # White moves up (lower index), Black moves down
        
        # 1. Move forward
        if 0 <= r + direction < 8:
            if board_grid[r + direction][c] is None:
                moves.append((r + direction, c))
                # 2. Initial double move
                if not self.has_moved:
                    if board_grid[r + (2 * direction)][c] is None:
                        moves.append((r + (2 * direction), c))

        # 3. Captures
        for dc in [-1, 1]:
            nr, nc = r + direction, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target = board_grid[nr][nc]
                if target is not None and target.color != self.color:
                    moves.append((nr, nc))
        return moves

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

class Bishop(Piece):
    def get_valid_moves(self, board_grid):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        return self.get_sliding_moves(board_grid, directions)

class Rook(Piece):
    def get_valid_moves(self, board_grid):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        return self.get_sliding_moves(board_grid, directions)

class Queen(Piece):
    def get_valid_moves(self, board_grid):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
        return self.get_sliding_moves(board_grid, directions)

class King(Piece):
    def __init__(self, color, name, position):
        super().__init__(color, name, position)
        self.castling_done = False

    def set_castling_done(self):
        self.castling_done = True

    def get_valid_moves(self, board_grid):
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
        r, c = self.position
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target = board_grid[nr][nc]
                if target is None or target.color != self.color:
                    moves.append((nr, nc))
        # Note: Castling logic usually goes in ChessEngine because it requires checking other pieces (Rooks)
        return moves


class ChessBoard:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup_pieces()

    def setup_pieces(self):
        # Black pieces at the TOP (Rows 0 and 1)
        for c in range(8):
            self.grid[1][c] = Pawn("black", "Pawn", (1, c))
        self.grid[0][0] = Rook("black", "Rook", (0, 0))
        self.grid[0][1] = Knight("black", "Knight", (0, 1))
        self.grid[0][2] = Bishop("black", "Bishop", (0, 2))
        self.grid[0][3] = Queen("black", "Queen", (0, 3))
        self.grid[0][4] = King("black", "King", (0, 4))
        self.grid[0][5] = Bishop("black", "Bishop", (0, 5))
        self.grid[0][6] = Knight("black", "Knight", (0, 6))
        self.grid[0][7] = Rook("black", "Rook", (0, 7))

        # White pieces at the BOTTOM (Rows 6 and 7)
        for c in range(8):
            self.grid[6][c] = Pawn("white", "Pawn", (6, c))
        self.grid[7][0] = Rook("white", "Rook", (7, 0))
        self.grid[7][1] = Knight("white", "Knight", (7, 1))
        self.grid[7][2] = Bishop("white", "Bishop", (7, 2))
        self.grid[7][3] = Queen("white", "Queen", (7, 3))
        self.grid[7][4] = King("white", "King", (7, 4))
        self.grid[7][5] = Bishop("white", "Bishop", (7, 5))
        self.grid[7][6] = Knight("white", "Knight", (7, 6))
        self.grid[7][7] = Rook("white", "Rook", (7, 7))

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
        self.board.setup_pieces()

    def make_move(self, start_sq, end_sq):
        if not self.is_legal(start_sq, end_sq):
            return False

        move = Move(start_sq, end_sq, self.board.grid)
        
        # Check if this move is a promotion
        is_promotion = False
        if move.piece_moved.name == "Pawn":
            if (move.piece_moved.color == "white" and end_sq[0] == 0) or \
               (move.piece_moved.color == "black" and end_sq[0] == 7):
                is_promotion = True

        if move.piece_moved and move.piece_moved.color == ("white" if self.white_to_move else "black"):
            self.board.move_piece(move)
            
            # If it's a promotion, replace the pawn
            if is_promotion:
                # We will pass a default or chosen piece type here
                self.promote_pawn(end_sq, move.piece_moved.color)
            
            self.move_log.append(move)
            self.white_to_move = not self.white_to_move
            return True
        return False

    def is_in_check(self, color):
        # 1. Find the King's position
        king_pos = None
        for r in range(8):
            for c in range(8):
                piece = self.board.grid[r][c]
                if piece and piece.name == "King" and piece.color == color:
                    king_pos = (r, c)
                    break
        
        # 2. Check if any enemy piece can attack that position
        enemy_color = "black" if color == "white" else "white"
        for r in range(8):
            for c in range(8):
                piece = self.board.grid[r][c]
                if piece and piece.color == enemy_color:
                    # Use get_valid_moves but be careful of infinite recursion
                    # For now, we check if king_pos is in their basic move set
                    if king_pos in piece.get_valid_moves(self.board.grid):
                        return True
        return False

    def check_game_over(self):
        """Returns 'checkmate', 'stalemate', or None"""
        color = "white" if self.white_to_move else "black"
        
        # 1. Check if the player has ANY legal moves
        has_legal_move = False
        for r in range(8):
            for c in range(8):
                piece = self.board.grid[r][c]
                if piece and piece.color == color:
                    valid_moves = piece.get_valid_moves(self.board.grid)
                    for move in valid_moves:
                        if self.is_legal((r, c), move):
                            has_legal_move = True
                            break
                if has_legal_move: break
            if has_legal_move: break

        # 2. Determine result
        if not has_legal_move:
            if self.is_in_check(color):
                return "checkmate"
            else:
                return "stalemate"
        
        return None

    def promote_pawn(self, pos, color, piece_type="Queen"):
        """Replaces the pawn at pos with a new piece."""
        r, c = pos
        # You can expand this logic to take user input
        if piece_type == "Queen":
            self.board.grid[r][c] = Queen(color, "Queen", pos)
        elif piece_type == "Rook":
            self.board.grid[r][c] = Rook(color, "Rook", pos)
        elif piece_type == "Bishop":
            self.board.grid[r][c] = Bishop(color, "Bishop", pos)
        elif piece_type == "Knight":
            self.board.grid[r][c] = Knight(color, "Knight", pos)

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
        return moves

    def undo_move(self):
        """Pops the last move from the log and reverts the board."""
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move

    def is_legal(self, start_sq, end_sq):
        r, c = start_sq
        piece = self.board.grid[r][c]
        
        # Basic validation
        if piece is None or piece.color != ("white" if self.white_to_move else "black"):
            return False
            
        # Check if the piece's own rules allow the move
        if end_sq not in piece.get_valid_moves(self.board.grid):
            return False

        # --- THE CHECK CHECK ---
        # 1. Simulate the move
        target_piece = self.board.grid[end_sq[0]][end_sq[1]]
        original_pos = piece.position
        
        self.board.grid[end_sq[0]][end_sq[1]] = piece
        self.board.grid[r][c] = None
        piece.position = end_sq
        
        # 2. See if the King is now under attack
        in_check = self.is_in_check(piece.color)
        
        # 3. Undo the simulation immediately
        self.board.grid[r][c] = piece
        self.board.grid[end_sq[0]][end_sq[1]] = target_piece
        piece.position = original_pos
        
        # If the move leaves the king in check, it is NOT legal
        return not in_check
