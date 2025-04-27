import math

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # 3x3 board
        self.current_winner = None  # Track winner

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False
    def empty_squares(self):
        return ' ' in self.board
    def num_empty_squares(self):
        return self.board.count(' ')


    def winner(self, square, letter):
        # Check row
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([s == letter for s in row]):
            return True

        # Check column
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([s == letter for s in column]):
            return True

        # Check diagonals
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0,4,8]]
            if all([s == letter for s in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2,4,6]]
            if all([s == letter for s in diagonal2]):
                return True

        return False


class AIPlayer:
    def __init__(self, letter):
        self.letter = letter  # 'X' or 'O'

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            # Random first move if board is empty
            square = 0
        else:
            # Run minimax
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter  # AI is trying to maximize itself
        other_player = 'O' if player == 'X' else 'X'

        # Check if previous move is a winner
        if state.current_winner == other_player:
            return {'position': None,
                    'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)}
        
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}  # maximize
        else:
            best = {'position': None, 'score': math.inf}  # minimize

        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)  

            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score

        return best

def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board()

    letter = 'X'  
    while game.empty_squares():
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            valid_square = False
            while not valid_square:
                square = input(f"{letter}'s turn. Input move (0-8): ")
                try:
                    square = int(square)
                    if square not in game.available_moves():
                        raise ValueError
                    valid_square = True
                except ValueError:
                    print("Invalid move. Try again.")

        game.make_move(square, letter)

        if print_game:
            print(letter + f' makes a move to square {square}')
            game.print_board()
            print('')  

        if game.current_winner:
            if print_game:
                print(letter + ' wins!')
            return letter  

        # Switch players
        letter = 'O' if letter == 'X' else 'X'

    if print_game:
        print('It\'s a tie!')


if __name__ == '__main__':
    game = TicTacToe()
    x_player = None  # Human player
    o_player = AIPlayer('O')  # AI playing as 'O'

    play(game, x_player, o_player)
