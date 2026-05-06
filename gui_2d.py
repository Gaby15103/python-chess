from ursina import *

class Scrollable:

    def __init__(self, **kwargs):
        super().__init__()
        self.max = inf
        self.min = -inf
        self.scroll_speed = .05
        self.scroll_smoothing = 16
        self.axis = 'y'
        self.target_value = None

        for key, value in kwargs.items():
            setattr(self, key, value)



    def update(self):
        # lerp position
        if self.target_value:
            setattr(self.entity, self.axis, lerp(getattr(self.entity, self.axis), self.target_value, time.dt * self.scroll_smoothing))



    def input(self, key):
        if not mouse.hovered_entity:
            return

        if not self.target_value:
            self.target_value = getattr(self.entity, self.axis)

        if self.entity.hovered or mouse.hovered_entity.has_ancestor(self.entity):
            # print(key)
            if key == 'scroll up':
                self.target_value -= self.scroll_speed
            if key == 'scroll down':
                self.target_value += self.scroll_speed


            self.target_value = max(min(self.target_value, self.max), self.min)


if __name__ == '__main__':
    '''
    This will make target entity move up or down when you hover the entity/its children
    while scrolling the scroll wheel.
    '''

    app = Ursina()
    p = Button(model='quad', scale=(.4, .8), collider='box')
    for i in range(8):
        Button(parent=p , scale_y=.05, text=f'giopwjoigjwr{i}', origin_y=.5, y=.5-(i*.05))

    p.add_script(Scrollable())
    app.run()

class Square(Button):
    def __init__(self, row, col, engine, gui):
        super().__init__(
            parent=scene,
            position=(col, 7-row),
            model='quad',
            origin=(-.5, -.5),
            color=color.light_gray if (row + col) % 2 == 0 else color.dark_gray,
            highlight_color=color.lime,
            scale=1,
        )
        self.row = row
        self.col = col
        self.engine = engine
        self.gui = gui

    def on_click(self):
        self.gui.handle_square_click(self.row, self.col)

    def disable_square(self):
        self.collider = None
        self.color = color.light_gray if (self.row + self.col) % 2 == 0 else color.dark_gray
        
    def enable_square(self):
        self.collider = 'box'

class ChessGui2D():
    def __init__(self, engine, mode='2d'):
        self.app = Ursina()

        window.title = "Python Chess"
        window.borderless = False
        window.fps_counter.enabled = False
        window.exit_button.enabled = False
        window.color = color.dark_gray

        self.engine = engine
        self.selected_sq = None
        self.squares = []
        self.piece_entities = {}
        self.move_history = []

        self.board_size = 8
        self.setup_ui()

        center = self.board_size / 2
        camera.orthographic = True
        camera.fov = 10
        camera.position = (center, center, -10)

        self.create_board()
        self.update_board_visuals()
        self.update_status()

    def setup_ui(self):
        # 1. The Frame (The dark box on the left)
        self.move_panel = Entity(
            parent=camera.ui, model='quad', color=color.black66, 
            scale=(0.25, 0.6), position=(-0.7, 0),
            collider='box' # Needed for the scroll script to detect the mouse
        )
        Text("History", parent=self.move_panel, position=(-0.45, 0.48), scale=1.5)

        # 2. The "Paper" (This is what actually moves)
        # We attach the Scrollable script here
        self.history_container = Entity(parent=self.move_panel, position=(0,0))
        self.history_container.add_script(Scrollable(min=0, max=2)) # Adjust max based on game length

        self.history_text = Text(
            text="", 
            parent=self.history_container, 
            position=(-0.4, 0.4), # Start at the top of the panel
            scale=1.2,
            line_height=1.1
        )

        # --- Right Side: Status Panel (Same as before) ---
        self.status_panel = Entity(parent=camera.ui, model='quad', color=color.black66, 
                                   scale=(0.25, 0.6), position=(0.7, 0))
        self.turn_text = Text(text="Turn: White", parent=self.status_panel, 
                              position=(-0.4, 0.4), scale=2)
        self.selected_piece_display = Entity(
            parent=self.status_panel, model='quad', scale=0.4,
            position=(0, -0.2), color=color.clear
        )

    def update_status(self):
        current_turn = "White" if self.engine.white_to_move else "Black"
        self.turn_text.text = f"Turn: {current_turn}"
        self.turn_text.color = color.white if self.engine.white_to_move else color.gray

    def update_move_list(self, move_str):
        self.move_history.append(move_str)
        self.history_text.text = "\n".join(self.move_history)

    def handle_square_click(self, r, c):
        for sq in self.squares:
            sq.color = color.light_gray if (sq.row + sq.col) % 2 == 0 else color.dark_gray

        if self.selected_sq is None:
            piece = self.engine.board.grid[r][c]
            current_turn = "white" if self.engine.white_to_move else "black"
            if piece and piece.color == current_turn:
                self.selected_sq = (r, c)
                img_path = f"assets/pieces-basic-png/{piece.color}-{piece.name.lower()}"
                self.selected_piece_display.texture = img_path
                self.selected_piece_display.color = color.white
                
                for sq in self.squares:
                    if sq.row == r and sq.col == c:
                        sq.color = color.cyan
        else:
            start = self.selected_sq
            end = (r, c)
            moving_piece = self.engine.board.grid[start[0]][start[1]]

            if self.engine.make_move(start, end):
                # Format move for list (e.g., "W-Pawn: (6,4) -> (4,4)")
                move_text = f"{moving_piece.color[0].upper()}-{moving_piece.name}: {start}->{end}"
                self.update_move_list(move_text)
                self.update_board_visuals()
                self.update_status()
            
            status = self.engine.check_game_over()
            if status:
                self.show_game_over(status)
            
            self.selected_sq = None
            self.selected_piece_display.texture = None
            self.selected_piece_display.color = color.clear

    def create_board(self):
        self.board_bg = Entity(
            model='quad', color=color.black, scale=8.2,
            position=(-0.1, -0.1, 0.1), origin=(-.5, -.5)
        )
        for r in range(8):
            for c in range(8):
                sq = Square(r, c, self.engine, self)
                self.squares.append(sq)

    def update_board_visuals(self):
        for p in self.piece_entities.values():
            destroy(p)
        self.piece_entities.clear()
        for r in range(8):
            for c in range(8):
                piece = self.engine.board.grid[r][c]
                if piece:
                    img_path = f"assets/pieces-basic-png/{piece.color}-{piece.name.lower()}"
                    self.piece_entities[(r,c)] = Entity(
                        parent=scene, model='quad', texture=img_path,
                        position=(c, 7-r, -0.01), origin=(-.5, -.5), scale=0.9
                    )

    def show_game_over(self, status):
        for sq in self.squares:
            sq.disable_square()
        self.overlay = Entity(parent=camera.ui, model='quad', scale=(2, 1), color=color.black66, z=-1)
        winner = "Black" if self.engine.white_to_move else "White"
        winner_text = f"CHECKMATE!\n{winner} Wins!" if status == "checkmate" else "STALEMATE!"
        self.result_text = Text(text=winner_text, parent=camera.ui, origin=(0, 0), scale=3, position=(0, 0.1))
        self.restart_button = Button(text='Play Again', parent=camera.ui, scale=(0.3, 0.1), 
                                     position=(0, -0.2), color=color.azure, on_click=self.restart_game)

    def restart_game(self):
        self.engine.__init__() 
        destroy(self.overlay)
        destroy(self.result_text)
        destroy(self.restart_button)
        self.selected_sq = None
        self.history_list.options = []
        self.history_list.render()
        for sq in self.squares:
            sq.color = color.light_gray if (sq.row + sq.col) % 2 == 0 else color.dark_gray
            sq.enable_square()
        self.update_board_visuals()
        self.update_status()

    def run(self):
        self.app.run()