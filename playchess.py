from pychess import ChessEngine

class ChessGame:
    def __init__(self):
        self.engine = ChessEngine()
        self.current_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.player_side = 'w' 

    def display_board(self, fen):
        board, turn = self.engine.parse_fen(fen)
        print("\n  +------------------------+")
        for i, row in enumerate(board):
            print(f"{8 - i} |", end=" ")
            for piece in row:
                print(piece if piece else '.', end=" ")
            print("|")
        print("  +------------------------+")
        print("    a b c d e f g h")
        print(f"Na potezu: {'Bijeli' if turn == 'w' else 'Crni'}")

    def get_player_move(self):
        while True:
            move = input("\nTvoj potez: ").strip().lower()
            if len(move) == 4 and move[0] in 'abcdefgh' and move[2] in 'abcdefgh' and move[1] in '12345678' and move[3] in '12345678':
                return move
            print("Krivi format. Napisi u obliku a1a2, gdje je a1 polje s kojeg figura krece, a a2 polje gdje zavrsava nakon tvog poteza.")

    def play(self):
        print("        .__       .____________          __  .__                      _____          __  .__                 _________ .__                          ")
        print("  _____ |__| ____ |__\______   \___.__._/  |_|  |__   ____   ____    /     \ _____ _/  |_|  |__   ____  _____\_   ___ \|  |__   ____   ______ ______")
        print(" /     \|  |/    \|  ||     ___<   |  |\   __\  |  \ /  _ \ /    \  /  \ /  \\__  \\   __\  |  \ /  _ \/  ___/    \  \/|  |  \_/ __ \ /  ___//  ___/")
        print("|  Y Y  \  |   |  \  ||    |    \___  | |  | |   Y  (  <_> )   |  \/    Y    \/ __ \|  | |   Y  (  <_> )___ \\     \___|   Y  \  ___/ \___ \ \___ \ ")
        print("|__|_|  /__|___|  /__||____|    / ____| |__| |___|  /\____/|___|  /\____|__  (____  /__| |___|  /\____/____  >\______  /___|  /\___  >____  >____  >")
        print("      \/        \/              \/                \/            \/         \/     \/          \/           \/        \/     \/     \/     \/     \/ ")
        print("____   ________    _______       ___.           .____     ____ ____________ _________ .___   _____    _______    _______    _______  ___________    ")
        print("\   \ /   /_   |   \   _  \      \_ |__ ___.__. |    |   |    |   \_   ___ \\_   ___ \|   | /  _  \   \      \   \      \   \      \ \_   _____/    ")
        print(" \   Y   / |   |   /  /_\  \      | __ <   |  | |    |   |    |   /    \  \//    \  \/|   |/  /_\  \  /   |   \  /   |   \  /   |   \ |    __)_     ")
        print("  \     /  |   |   \  \_/   \     | \_\ \___  | |    |___|    |  /\     \___\     \___|   /    |    \/    |    \/    |    \/    |    \|        \    ")
        print("   \___/   |___| /\ \_____  /     |___  / ____| |_______ \______/  \______  /\______  /___\____|__  /\____|__  /\____|__  /\____|__  /_______  /    ")
        print("                 \/       \/          \/\/              \/                \/        \/            \/         \/         \/         \/        \/     ")
        print("\n\n\nBijela ili crna? (w/b)")
        while True:
            side = input().strip().lower()
            if side in ['w', 'b']:
                self.player_side = side
                break
            print("plz unesi w ili b")

        board, turn = self.engine.parse_fen(self.current_fen)
        self.display_board(self.current_fen)

        while True:
            board, current_turn = self.engine.parse_fen(self.current_fen)
            
            if self.is_game_over(board, current_turn):
                print("\ngotova igra!")
                break
                
            if current_turn == self.player_side:
                print("\ntvoj potez!")
                move = self.get_player_move()
                
                new_board = self.engine.make_move(board, move)
                next_turn = 'b' if current_turn == 'w' else 'w'
                self.current_fen = self.board_to_fen(new_board, next_turn)
            else:
                print("\nengine razmislja...")
                best_move = self.engine.get_best_move(self.current_fen, depth=3)
                print(f"engine je odigrao: {best_move}")
                
                new_board = self.engine.make_move(board, best_move)
                next_turn = 'b' if current_turn == 'w' else 'w'
                self.current_fen = self.board_to_fen(new_board, next_turn)
            
            self.display_board(self.current_fen)

    def board_to_fen(self, board, turn):
        fen_rows = []
        for row in board:
            fen_row = ""
            empty = 0
            for cell in row:
                if cell:
                    if empty > 0:
                        fen_row += str(empty)
                        empty = 0
                    fen_row += cell
                else:
                    empty += 1
            if empty > 0:
                fen_row += str(empty)
            fen_rows.append(fen_row)
        
        return "/".join(fen_rows) + f" {turn} - - 0 1"
    
    def is_game_over(self, board, turn):
        moves = self.engine.generate_moves(board, turn)
        if not moves:
            king = 'K' if turn == 'w' else 'k'
            king_found = False
            for row in board:
                if king in row:
                    king_found = True
                    break
                    
            if king_found:
                print("\nSah mat! " + ("Crni" if turn == 'w' else "Bijeli") + " pobjeduje!")
            else:
                print("\nPat! remi.")
            return True
        return False

if __name__ == "__main__":
    game = ChessGame()
    game.play()
