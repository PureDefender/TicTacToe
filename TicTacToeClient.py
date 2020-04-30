import sys
import socket

MSG_LEN = 2048

class ClientInterface:
    def get_move(self):
        move = input('Where do you want to move?')
        return move

    def show_msg(self, msg):
        print(msg)

class TicTacToeClient:
    def __init__(self, server_address):
        #super().__init__()
        self.conn = socket.create_connection(server_address)
        self.io = ClientInterface()
    
    def play(self):
        response : str = self.recv_msg()
        mark = response[8]
        opponent_mark = 'O' if mark == 'X' else 'X'
        self.io.show_msg('You are player ' + mark)
        if mark == 'O':
            self.play_move()
        while 1:
            response = self.recv_msg()
            if response == '':
                self.io.show_msg('connection was interrupted')
                break
            if response.startswith('VALID_MOVE'):
                self.io.show_msg('Valid move, please wait for opponent.')
                # update board using self.current_square
            elif response.startswith('OPPONENT_MOVED'):
                loc = int(response[15:])
                # update board using loc
                self.io.show_msg('MOVE: ' + loc)
                self.io.show_msg('Opponent moved, your turn.')
            elif response.startswith('MSG'):
                self.io.show_msg(response[4:])
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

            self.play_move()
        
        self.io.show_msg('Game has ended.')

    def play_move(self):
        self.current_square = self.io.get_move()
        msg = 'MOVE' + self.current_square
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
