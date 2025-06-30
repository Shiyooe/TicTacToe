import random
import time

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # 3x3 board
        self.current_winner = None
    
    def print_board(self):
        # Print board dengan format yang bagus
        print("\n   |   |   ")
        print(f" {self.board[0]} | {self.board[1]} | {self.board[2]} ")
        print("___|___|___")
        print("   |   |   ")
        print(f" {self.board[3]} | {self.board[4]} | {self.board[5]} ")
        print("___|___|___")
        print("   |   |   ")
        print(f" {self.board[6]} | {self.board[7]} | {self.board[8]} ")
        print("   |   |   \n")
    
    def print_board_nums(self):
        # Print board dengan nomor posisi untuk panduan
        print("\nPanduan nomor posisi:")
        print("   |   |   ")
        print(" 0 | 1 | 2 ")
        print("___|___|___")
        print("   |   |   ")
        print(" 3 | 4 | 5 ")
        print("___|___|___")
        print("   |   |   ")
        print(" 6 | 7 | 8 ")
        print("   |   |   \n")
    
    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']
    
    def empty_squares(self):
        return ' ' in self.board
    
    def num_empty_squares(self):
        return self.board.count(' ')
    
    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False
    
    def winner(self, square, letter):
        # Check baris
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True
        
        # Check kolom
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        
        # Check diagonal
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]  # diagonal kiri atas ke kanan bawah
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]  # diagonal kanan atas ke kiri bawah
            if all([spot == letter for spot in diagonal2]):
                return True
        
        return False

class HumanPlayer:
    def __init__(self, letter):
        self.letter = letter
    
    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(f"Giliran {self.letter}. Pilih posisi (0-8): ")
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print("Posisi tidak valid! Pilih angka 0-8 yang masih kosong.")
        return val

class BotPlayer:
    def __init__(self, letter):
        self.letter = letter
    
    def get_move(self, game):
        # Bot menggunakan strategi minimax dengan alpha-beta pruning
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())  # Random move pertama
        else:
            # Minimax algorithm
            square = self.minimax(game, self.letter)['position']
        return square
    
    def minimax(self, state, player):
        max_player = self.letter  # Bot
        other_player = 'O' if player == 'X' else 'X'
        
        # Base case
        if state.current_winner == other_player:
            return {'position': None,
                    'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)}
        elif not state.empty_squares():  # Tie
            return {'position': None, 'score': 0}
        
        if player == max_player:
            best = {'position': None, 'score': -1000}  # Maximize
        else:
            best = {'position': None, 'score': 1000}  # Minimize
        
        for possible_move in state.available_moves():
            # Make move
            state.make_move(possible_move, player)
            # Recurse
            sim_score = self.minimax(state, other_player)
            # Undo move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move
            
            if player == max_player:  # Maximize
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:  # Minimize
                if sim_score['score'] < best['score']:
                    best = sim_score
        
        return best

def play_game(mode='bot'):
    t = TicTacToe()
    
    if mode == 'bot':
        x_player = HumanPlayer('X')
        o_player = BotPlayer('O')
        print("=== SELAMAT DATANG DI TIC TAC TOE ===")
        print("Kamu adalah X, Bot adalah O")
    else:
        x_player = HumanPlayer('X')
        o_player = HumanPlayer('O')
        print("=== SELAMAT DATANG DI TIC TAC TOE ===")
        print("Player 1: X, Player 2: O")
    
    t.print_board_nums()
    
    letter = 'X'  # X selalu mulai duluan
    
    while t.empty_squares():
        if letter == 'O' and mode == 'bot':
            print("Bot sedang berpikir...")
            time.sleep(1)  # Delay untuk efek dramatis
            square = o_player.get_move(t)
            print(f"Bot memilih posisi {square}")
        else:
            square = x_player.get_move(t) if letter == 'X' else o_player.get_move(t)
        
        if t.make_move(square, letter):
            t.print_board()
            
            if t.current_winner:
                if mode == 'bot':
                    if t.current_winner == 'X':
                        print("🎉 SELAMAT! Kamu menang!")
                    else:
                        print("🤖 Bot menang! Coba lagi!")
                else:
                    print(f"🎉 SELAMAT! Player {t.current_winner} menang!")
                return t.current_winner
            
            letter = 'O' if letter == 'X' else 'X'  # Switch player
    
    print("🤝 SERI! Permainan berakhir imbang!")
    return None

def main():
    print("=== TIC TAC TOE GAME ===")
    print("1. Lawan Bot (Sulit)")
    print("2. Lawan Player")
    
    while True:
        try:
            choice = int(input("\nPilih mode (1/2): "))
            if choice == 1:
                play_game('bot')
                break
            elif choice == 2:
                play_game('player')
                break
            else:
                print("Pilihan tidak valid! Pilih 1 atau 2.")
        except ValueError:
            print("Input tidak valid! Masukkan angka 1 atau 2.")
    
    # Tanya apakah mau main lagi
    while True:
        play_again = input("\nMau main lagi? (y/n): ").lower()
        if play_again == 'y':
            main()
            break
        elif play_again == 'n':
            print("Terima kasih sudah bermain! 👋")
            break
        else:
            print("Input tidak valid! Ketik 'y' untuk ya atau 'n' untuk tidak.")

if __name__ == '__main__':
    main()