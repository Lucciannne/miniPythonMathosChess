import re
import numpy as np

class ChessEngine:
    def __init__(self):
        self.piece_values = {
            'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 10000,
            'p': -100, 'n': -320, 'b': -330, 'r': -500, 'q': -900, 'k': -10000
        }
        
        self.pst = {
            'P': np.array([
                [0, 0, 0, 0, 0, 0, 0, 0],
                [50, 50, 50, 50, 50, 50, 50, 50],
                [10, 10, 20, 30, 30, 20, 10, 10],
                [5, 5, 10, 25, 25, 10, 5, 5],
                [0, 0, 0, 20, 20, 0, 0, 0],
                [5, -5, -10, 0, 0, -10, -5, 5],
                [5, 10, 10, -20, -20, 10, 10, 5],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ]),
            'N': np.array([
                [-50, -40, -30, -30, -30, -30, -40, -50],
                [-40, -20, 0, 0, 0, 0, -20, -40],
                [-30, 0, 10, 15, 15, 10, 0, -30],
                [-30, 5, 15, 20, 20, 15, 5, -30],
                [-30, 0, 15, 20, 20, 15, 0, -30],
                [-30, 5, 10, 15, 15, 10, 5, -30],
                [-40, -20, 0, 5, 5, 0, -20, -40],
                [-50, -40, -30, -30, -30, -30, -40, -50]
            ]),
            'B': np.array([
                [-20, -10, -10, -10, -10, -10, -10, -20],
                [-10, 0, 0, 0, 0, 0, 0, -10],
                [-10, 0, 5, 10, 10, 5, 0, -10],
                [-10, 5, 5, 10, 10, 5, 5, -10],
                [-10, 0, 10, 10, 10, 10, 0, -10],
                [-10, 10, 10, 10, 10, 10, 10, -10],
                [-10, 5, 0, 0, 0, 0, 5, -10],
                [-20, -10, -10, -10, -10, -10, -10, -20]
            ]),
            'R': np.array([
                [0, 0, 0, 0, 0, 0, 0, 0],
                [5, 10, 10, 10, 10, 10, 10, 5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [0, 0, 0, 5, 5, 0, 0, 0]
            ]),
            'Q': np.array([
                [-20, -10, -10, -5, -5, -10, -10, -20],
                [-10, 0, 0, 0, 0, 0, 0, -10],
                [-10, 0, 5, 5, 5, 5, 0, -10],
                [-5, 0, 5, 5, 5, 5, 0, -5],
                [0, 0, 5, 5, 5, 5, 0, -5],
                [-10, 5, 5, 5, 5, 5, 0, -10],
                [-10, 0, 5, 0, 0, 0, 0, -10],
                [-20, -10, -10, -5, -5, -10, -10, -20]
            ]),
            'K': np.array([
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-20, -30, -30, -40, -40, -30, -30, -20],
                [-10, -20, -20, -20, -20, -20, -20, -10],
                [20, 20, 0, 0, 0, 0, 20, 20],
                [20, 30, 10, 0, 0, 10, 30, 20]
            ])
        }
        
    def parse_fen(self, fen):
        board = [['' for _ in range(8)] for _ in range(8)]
        parts = fen.split()
        rows = parts[0].split('/')
        
        for i, row in enumerate(rows):
            col_idx = 0
            for char in row:
                if char.isdigit():
                    col_idx += int(char)
                else:
                    board[i][col_idx] = char
                    col_idx += 1
                    
        turn = parts[1]
        return board, turn

    def generate_moves(self, board, turn):
        moves = []
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if (turn == 'w' and piece.isupper()) or (turn == 'b' and piece.islower()):
                    moves.extend(self.get_piece_moves(board, r, c))
        return moves

    def get_piece_moves(self, board, row, col):
        piece = board[row][col].upper()
        moves = []
        
        if piece == 'P':
            direction = -1 if board[row][col].isupper() else 1
            start_row = 6 if board[row][col].isupper() else 1

            if 0 <= row + direction < 8 and not board[row + direction][col]:
                moves.append(self.create_move_str(row, col, row + direction, col))
                
                if row == start_row and not board[row + 2*direction][col]:
                    moves.append(self.create_move_str(row, col, row + 2*direction, col))
            
            for dc in [-1, 1]:
                if 0 <= col + dc < 8 and 0 <= row + direction < 8:
                    target = board[row + direction][col + dc]
                    if target and ((target.isupper() and board[row][col].islower()) or 
                                  (target.islower() and board[row][col].isupper())):
                        moves.append(self.create_move_str(row, col, row + direction, col + dc))
        
        elif piece == 'N':
            for dr, dc in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), 
                          (1, -2), (1, 2), (2, -1), (2, 1)]:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = board[new_row][new_col]
                    if not target or (target.isupper() and board[row][col].islower()) or \
                       (target.islower() and board[row][col].isupper()):
                        moves.append(self.create_move_str(row, col, new_row, new_col))
        
        elif piece == 'K':
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    new_row, new_col = row + dr, col + dc
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        target = board[new_row][new_col]
                        if not target or (target.isupper() and board[row][col].islower()) or \
                           (target.islower() and board[row][col].isupper()):
                            moves.append(self.create_move_str(row, col, new_row, new_col))
        
        return moves

    def create_move_str(self, r1, c1, r2, c2):
        return f"{chr(97 + c1)}{8 - r1}{chr(97 + c2)}{8 - r2}"

    def make_move(self, board, move):
        c1, r1, c2, r2 = move[0], move[1], move[2], move[3]
        from_col, from_row = ord(c1) - 97, 8 - int(r1)
        to_col, to_row = ord(c2) - 97, 8 - int(r2)
        
        new_board = [row[:] for row in board]
        piece = new_board[from_row][from_col]
        new_board[to_row][to_col] = piece
        new_board[from_row][from_col] = ''
        return new_board

    def evaluate_board(self, board):
        score = 0
        
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if not piece:
                    continue
                
                score += self.piece_values[piece]
                
                if piece.upper() in self.pst:
                    table = self.pst[piece.upper()]
                    row = r if piece.isupper() else 7 - r
                    score += table[row][c] if piece.isupper() else -table[row][c]
        
        return score

    def alpha_beta(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0:
            return self.evaluate_board(board), None
        
        turn = 'w' if maximizing_player else 'b'
        moves = self.generate_moves(board, turn)
        
        if not moves:
            return -100000 if maximizing_player else 100000, None
        
        best_move = None
        
        if maximizing_player:
            max_eval = float('-inf')
            for move in moves:
                new_board = self.make_move(board, move)
                eval_val, _ = self.alpha_beta(new_board, depth - 1, alpha, beta, False)
                
                if eval_val > max_eval:
                    max_eval = eval_val
                    best_move = move
                
                alpha = max(alpha, eval_val)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in moves:
                new_board = self.make_move(board, move)
                eval_val, _ = self.alpha_beta(new_board, depth - 1, alpha, beta, True)
                
                if eval_val < min_eval:
                    min_eval = eval_val
                    best_move = move
                
                beta = min(beta, eval_val)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def get_best_move(self, fen, depth=6):
        board, turn = self.parse_fen(fen)
        _, best_move = self.alpha_beta(
            board, 
            depth, 
            float('-inf'), 
            float('inf'), 
            turn == 'w'
        )
        return best_move

if __name__ == "__main__":
    engine = ChessEngine()
    
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    best_move = engine.get_best_move(fen)
    print(f"bestmove: {best_move}")
    
    fen = "2b5/p2NBp1p/1bp1nPPr/3P4/2pRnr1P/1k1B1Ppp/1P1P1pQP/Rq1N3K b - - 0 1"
    best_move = engine.get_best_move(fen)
    print(f"bestmove: {best_move}")
