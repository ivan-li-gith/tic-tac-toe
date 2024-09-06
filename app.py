from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

class TicTacToe:
    def __init__(self):
        self.board = [' ']*9
        self.current_player = 'X'
        self.winning_combos = [
            (0,1,2), (3,4,5), (6,7,8), #Rows
            (0,3,6), (1,4,7), (2,5,8), #Columns
            (0,4,8), (2,4,6)           #Diagonal
        ]

    def make_move(self,position):
        if self.board[position] == ' ':
            self.board[position] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False
        #     if(self.current_player == 'X'):
        #         self.current_player = 'O'
        #     else:
        #         self.current_player = 'X'
        #     return True
        # return False

    def check_winner(self):
        for x in self.winning_combos:
            if self.board[x[0]] == self.board[x[1]] == self.board[x[2]] != ' ':
                return self.board[x[0]]
        
        if ' ' not in self.board:
            return 'Tie'
        
        return None
    
    def get_winning_combination(self):
        for x in self.winning_combos:
            if self.board[x[0]] == self.board[x[1]] == self.board[x[2]] != ' ':
                return x
        return None

    
    def reset_board(self):
        self.board = [' ']*9

game = TicTacToe()
            

@app.route('/')
def index():
    return render_template('index.html', board=game.board)

@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.get_json()
    position = data['position']
    if game.make_move(position):
        winner = game.check_winner()
        winning_combination = game.get_winning_combination()
        return jsonify({'status': 'success', 'winner': winner, 'board': game.board, 'winning_combination': winning_combination})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid Move'})
    
@app.route('/restart', methods=['POST'])
def clear():
    game.reset_board()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)