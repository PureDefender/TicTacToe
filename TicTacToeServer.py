import socket
import argparse

import threading
from threading import Thread

server_ip = '127.0.0.1'
server_port = 25560
board = [None] * 9
current_player = None
threads = []
client_lock = threading.Lock()


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
        player.conn.send('MSG Not your turn'.encode())
    elif player.opponent is None:
        player.conn.send('MSG Waiting for an opponent'.encode())
    elif board[loc] is not None:
        player.conn.send('MSG Illegal move, box already filled'.encode())
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


class PlayerThread(Thread):
    opponent = None
    player_input = None

    def __init__(self, conn, ip, port, symbol):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.symbol = symbol
        self.conn = conn

    def run(self):
        self.setup()
        self.read_command()

    def setup(self):
        global current_player

        self.player_input = self.conn.recv(2048).decode()
        self.conn.send(('Welcome Player ' + self.symbol).encode())
        if self.symbol == 'X':
            current_player = self
            self.conn.send('MSG Waiting for opponent to connect'.encode())
        else:
            opponent = current_player
            opponent.opponent = self
            self.conn.send('MSG Your turn'.encode())

    def read_command(self):
        if self.player_input.startswith('QUIT'):
            return
        elif self.player_input.startswith('MOVE'):
            self.process_move()

    def process_move(self):
        loc = int(self.player_input[5:])
        move(loc, self)
        move_message = ('OPPONENT_MOVED ' + str(loc)).encode()
        self.conn.send(move_message)
        if winner():
            self.conn.send('Victory'.encode())
            self.opponent.conn.send('DEFEAT'.encode())
        elif full_board():
            self.conn.send('TIE'.encode())
            self.opponent.conn.send('TIE'.encode())


def main():
    global server_ip, server_port, threads

    read_arguments()
    server_address = (server_ip, server_port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(server_address)
    print('Server now running on ' + server_ip + ':' + str(server_port))

    while len(threads) < 2:
        sock.listen(5)
        print('Waiting for players to join...')
        (conn, (client_ip, client_port)) = sock.accept()
        if len(threads) == 1:
            new_thread = PlayerThread(conn, client_ip, client_port, 'X')
        else:
            new_thread = PlayerThread(conn, client_ip, client_port, 'O')
        new_thread.start()
        threads.append(new_thread)

    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
