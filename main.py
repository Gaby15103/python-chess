from chess_engine import ChessEngine
from cli_manager import CLIManager
import subprocess

def main():
    subprocess.run(["clear"])
    # 1. Ask the user for the display mode
    print("Select View Mode:")
    print("1. CLI (Terminal)")
    print("2. 2D (Ursina)")
    print("3. 3D (Ursina)")
    choice = input("Enter choice (1/2/3): ").strip()

    engine = ChessEngine()

    if choice == "1":
        run_cli_mode(engine)
    elif choice == "2":
        from gui_2d import ChessGui2D  # Create this file for Ursina 2D
        gui = ChessGui2D(engine, mode='2d')
        gui.run()
    elif choice == "3":
        from gui_3d import ChessGui3D  # Create this file for Ursina 3D
        gui = ChessGui3D(engine, mode='3d')
        gui.run()
    else:
        print("Invalid choice, defaulting to CLI.")
        run_cli_mode(engine)

def run_cli_mode(engine):
    ui = CLIManager(engine)
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
            break

        coords = ui.parse_coordinates(move_str)
        if coords:
            start, end = coords
            success = engine.make_move(start, end)
            if not success:
                input("Invalid move! Press Enter to try again...")
        else:
            input("Format error (use e2e4)! Press Enter to try again...")

if __name__ == "__main__":
    main()