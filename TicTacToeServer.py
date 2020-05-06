import socket
import argparse

import threading

server_ip = '127.0.0.1'
server_port = 25560
board = [None] * 9
current_player = None


def read_arguments():
    global server_ip, server_port

    parser = argparse.ArgumentParser(description='Processing ip and port input.')
    parser.add_argument('-a', '--address', help='Used to identify an ip address')
    parser.add_argument('-p', '--port', help='Used to identify a port number', type=int)

    args = parser.parse_args()
    if args.address or args.port:
        if args.address:
            server_ip = args.address
        if args.port:
            server_port = args.port
    else:
        print('No IP or port given, defaulting to 127.0.0.1:25560')


def move(loc, player):
    global current_player

    if player is not current_player:
        raise Exception('INVALID Not your turn')
    elif player.opponent is None:
        raise Exception('INVALID Waiting for an opponent')
    elif board[loc] is not None:
        raise Exception('INVALID Illegal move, box already filled')
    elif loc < 0 or loc > 8:
        raise Exception('INVALID Illegal input, enter a valid move 0-8')
    board[loc] = current_player
    current_player = current_player.opponent


def full_board():
    for slot in board:
        if slot is None:
            return False
    return True


def winner():
    return (board[0] is not None and board[0] == board[1] and board[0] == board[2]) or (
            board[3] is not None and board[3] == board[4] and board[3] == board[5]) or (
                   board[6] is not None and board[6] == board[7] and board[6] == board[8]) or (
                   board[0] is not None and board[0] == board[3] and board[0] == board[6]) or (
                   board[1] is not None and board[1] == board[4] and board[1] == board[7]) or (
                   board[2] is not None and board[2] == board[5] and board[2] == board[8]) or (
                   board[0] is not None and board[0] == board[4] and board[0] == board[8]) or (
                   board[2] is not None and board[2] == board[4] and board[2] == board[6])


def RunPlayer(conn, client_ip, client_port, symbol):
    PlayerThread(conn, client_ip, client_port, symbol)


class PlayerThread:
    opponent = None
    player_input = None

    def __init__(self, conn, ip, port, symbol):
        self.ip = ip
        self.port = port
        self.symbol = symbol
        self.conn = conn
        self.run()

    def run(self):
        self.setup()
        self.read_command()

    def setup(self):
        global current_player

        self.conn.sendall(('Welcome Player ' + self.symbol).encode())
        if self.symbol == 'X':
            current_player = self
            self.conn.sendall('MSG Waiting for opponent to connect'.encode())
        else:
            self.opponent = current_player
            self.opponent.opponent = self
            self.opponent.conn.sendall('MSG Opponent connected'.encode())

    def read_command(self):
        while True:
            try:
                self.player_input = self.conn.recv(2048).decode()
                if self.player_input.startswith('QUIT'):
                    return
                elif self.player_input.startswith('MOVE'):
                    print('Player ' + current_player.symbol + ' input: ' + self.player_input)
                    self.process_move()
            except ConnectionResetError:
                self.opponent.conn.sendall('OTHER_PLAYER_LEFT'.encode())
            except OSError:
                print()

    def process_move(self):
        try:
            loc = int(self.player_input[5:])
            move(loc, self)
            self.conn.sendall('VALID_MOVE'.encode())
            if winner():
                print(current_player.opponent.symbol + ' has won the game')
                self.conn.sendall('VICTORY'.encode())
                self.opponent.conn.sendall('DEFEAT'.encode())
                self.opponent.conn.sendall(('OPPONENT_MOVED ' + str(loc)).encode())
                self.conn.close()
            elif full_board():
                print('Game ended in a tie')
                self.conn.sendall('TIE'.encode())
                self.opponent.conn.sendall('TIE'.encode())
                self.conn.close()
            self.opponent.conn.sendall(('OPPONENT_MOVED ' + str(loc)).encode())
        except Exception as e:
            self.conn.sendall(e.args[0].encode())


def main():
    global server_ip, server_port

    count = 0
    read_arguments()
    server_address = (server_ip, server_port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(server_address)
    print('Server now running on ' + server_ip + ':' + str(server_port))

    while True:
        sock.listen(1000)
        if count % 2 == 0:
            print('Waiting for players to join...')
            (conn, (client_ip, client_port)) = sock.accept()
            threading.Thread(target=RunPlayer, args=[conn, client_ip, client_port, 'X']).start()
            print('Player 1 joined')
            count += 1
        elif count % 2 ==  1:
            print('Waiting for player 2 to join...')
            (conn, (client_ip, client_port)) = sock.accept()
            threading.Thread(target=RunPlayer, args=[conn, client_ip, client_port, 'O']).start()
            print('Player 2 joined')
            count += 1


if __name__ == '__main__':
    main()
