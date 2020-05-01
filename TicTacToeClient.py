import sys
import socket

MSG_LEN = 2048

class ClientInterface:
    def get_move(self):
        try:
            move = int(input('Where do you want to move?\n'))
            if move < 0 or move > 9:
                move = -1
        except ValueError:
            move = -1
        return move

    def show_msg(self, msg):
        print(msg)

    def show_board(self, board):
        for i in range(3):
            for j in range(3):
                print(board[i * 3 + j], end=' ')
            print()

class TicTacToeClient:
    def __init__(self, server_address):
        #super().__init__()
        self.conn = socket.create_connection(server_address)
        self.io = ClientInterface()
        self.board = ['+'] * 9
    
    def play(self):
        response : str = self.recv_msg()
        mark = response.split(' ')[2]
        opponent_mark = 'O' if mark == 'X' else 'X'
        self.io.show_msg('You are player ' + mark)

        if mark == 'X':
            response: str = self.recv_msg()
            self.io.show_msg(response[4:])
            response: str = self.recv_msg()
            self.io.show_msg(response[4:])
            self.play_move()
        else:
            self.io.show_msg('Waiting for opponent to move...')
        while 1:
            response = self.recv_msg()
            if response == '':
                self.io.show_msg('connection was interrupted')
                break
            if response.startswith('VALID_MOVE'):
                self.io.show_msg('Valid move, please wait for opponent.')
                self.board[self.current_square] = mark
                self.io.show_board(self.board)
            elif response.startswith('OPPONENT_MOVED'):
                loc = int(response[15:])
                self.board[loc] = opponent_mark
                self.io.show_msg('Opponent moved, your turn.')
                self.io.show_board(self.board)
                self.play_move()
            elif response.startswith('MSG'):
                self.io.show_msg(response[4:])
            elif response.startswith('INVALID'):
                self.io.show_msg(response[8:])
                self.play_move()
            elif response.startswith('VICTORY'):
                self.io.show_msg('You win!')
                break
            elif response.startswith('DEFEAT'):
                self.io.show_msg('You lose!')
                break
            elif response.startswith('TIE'):
                self.io.show_msg('It was a tie.')
                break
            elif response.startswith('OTHER_PLAYER_LEFT'):
                self.io.show_msg('Other player left.')
                break
        
        self.send_msg('QUIT')
        self.io.show_msg('Game has ended.')

    def play_move(self):
        move = self.io.get_move()
        msg = 'MOVE ' + str(move)
        self.current_square = move
        self.send_msg(msg)



    def send_msg(self, msg: str):
        self.conn.sendall(msg.encode())

    def recv_msg(self):
        return self.conn.recv(MSG_LEN).decode()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage:\n'+ sys.argv[0] + ' server_ip server_port')
        sys.exit()
    address = (sys.argv[1], sys.argv[2])
    client = TicTacToeClient(address)
    client.play()
