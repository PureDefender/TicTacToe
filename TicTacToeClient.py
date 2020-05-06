import os
import socket
import threading
from tkinter import *
from tkinter import messagebox
# Set message length
MSG_LEN = 2048


# creating gui frame
def raise_frame(frame):
    serverAddress.set(serverAddressEntry.get())
    serverPort.set(serverPortEntry.get())
    frame.tkraise()


root = Tk()
serverAddress = StringVar()
serverPort = StringVar()
# establish window size
root.geometry("325x465")
# set the title for frame
root.title("Tic Tac Toe")


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        os._exit(1)



root.protocol("WM_DELETE_WINDOW", on_closing)

menu = Frame(root)
boardGame = Frame(root)

for frame in (menu, boardGame):
    frame.grid(row=0, column=0, sticky='news')
mainlabel = Label(menu, text="Please Enter Server Address and Port")
lableOne = LabelFrame(menu, text="Server Address")
lableTwo = LabelFrame(menu, text="Server Port")
submit_info_button = Button(menu, text="Submit", padx=10, pady=10, command=lambda: raise_frame(boardGame))

serverAddressEntry = Entry(lableOne)
serverPortEntry = Entry(lableTwo)

serverAddressEntry.grid(row=0, column=3)
serverPortEntry.grid(row=1, column=3)
lableOne.grid(row=2, column=3)
lableTwo.grid(row=3, column=3)
mainlabel.place(relx=.5, rely=.1, anchor=CENTER)
lableOne.place(relx=0.5, rely=0.2, anchor=CENTER)
lableTwo.place(relx=0.5, rely=0.3, anchor=CENTER)
submit_info_button.grid(row=4, column=3)
submit_info_button.place(relx=0.5, rely=0.5, anchor=CENTER)

raise_frame(menu)
# object for holding the move integer for get_move() function
move_object = IntVar()
playerXIcon = PhotoImage(file="./resources/x.png").subsample(8, 8)
playerOIcon = PhotoImage(file="resources/o.png").subsample(4, 4)
emptySpaceIcon = PhotoImage(file="resources/square.png").subsample(4, 4)
serverMessages = Entry(boardGame, width=20, borderwidth=30, state=DISABLED)
boardButton_0 = Button(boardGame, text="0", image=emptySpaceIcon, padx=30, pady=20,
                       command=lambda: boardButtonClicked(0))
boardButton_1 = Button(boardGame, text="1", image=emptySpaceIcon, padx=30, pady=20,
                       command=lambda: boardButtonClicked(1))
boardButton_2 = Button(boardGame, text="2", image=emptySpaceIcon, padx=30, pady=20,
                       command=lambda: boardButtonClicked(2))
boardButton_3 = Button(boardGame, text="3", image=emptySpaceIcon, padx=30, pady=20,
                       command=lambda: boardButtonClicked(3))
boardButton_4 = Button(boardGame, text="4", image=emptySpaceIcon, padx=30, pady=20,
                       command=lambda: boardButtonClicked(4))
boardButton_5 = Button(boardGame, text="5", image=emptySpaceIcon, padx=30, pady=20,
                       command=lambda: boardButtonClicked(5))
boardButton_6 = Button(boardGame, text="6", image=emptySpaceIcon, padx=30, pady=20,
                       command=lambda: boardButtonClicked(6))
boardButton_7 = Button(boardGame, text="7", image=emptySpaceIcon, padx=30, pady=20,
                       command=lambda: boardButtonClicked(7))
boardButton_8 = Button(boardGame, text="8", image=emptySpaceIcon, padx=30, pady=20,
                       command=lambda: boardButtonClicked(8))

quitButton_0 = Button(boardGame, text="Quit", padx=30, pady=30, command=lambda: quitButton())
serverMessages.grid(columnspan=3, ipadx=70, ipady=20)
boardButton_0.grid(row=1, column=0)
boardButton_1.grid(row=1, column=1)
boardButton_2.grid(row=1, column=2)
boardButton_3.grid(row=2, column=0)
boardButton_4.grid(row=2, column=1)
boardButton_5.grid(row=2, column=2)
boardButton_6.grid(row=3, column=0)
boardButton_7.grid(row=3, column=1)
boardButton_8.grid(row=3, column=2)
quitButton_0.grid(row=6, column=0, pady=10, columnspan=30)


def quitButton():
    root.destroy()
    os._exit(1)


def boardButtonClicked(move):
    move_object.set(move)


def updateServerMessage(msg):
    serverMessages.configure(state=NORMAL)
    serverMessages.delete(0, END)
    serverMessages.insert(0, msg)
    serverMessages.configure(state=DISABLED)


class ClientInterface:
    def get_move(self):
        root.wait_variable(move_object)
        move = move_object.get()
        return move

    def show_msg(self, msg):
        updateServerMessage(msg)
        print(msg)

    def show_board(self, board):
        for i in range(3):
            for j in range(3):

                if i == 0 and j == 0 and board[i * 3 + j] == "X":
                    boardButton_0.configure(image=playerXIcon)
                elif i == 0 and j == 0 and board[i * 3 + j] == "O":
                    boardButton_0.configure(image=playerOIcon)

                if i == 0 and j == 1 and board[i * 3 + j] == "X":
                    boardButton_1.configure(image=playerXIcon)
                elif i == 0 and j == 1 and board[i * 3 + j] == "O":
                    boardButton_1.configure(image=playerOIcon)

                if i == 0 and j == 2 and board[i * 3 + j] == "X":
                    boardButton_2.configure(image=playerXIcon)
                elif i == 0 and j == 2 and board[i * 3 + j] == "O":
                    boardButton_2.configure(image=playerOIcon)

                if i == 1 and j == 0 and board[i * 3 + j] == "X":
                    boardButton_3.configure(image=playerXIcon)
                elif i == 1 and j == 0 and board[i * 3 + j] == "O":
                    boardButton_3.configure(image=playerOIcon)

                if i == 1 and j == 1 and board[i * 3 + j] == "X":
                    boardButton_4.configure(image=playerXIcon)
                elif i == 1 and j == 1 and board[i * 3 + j] == "O":
                    boardButton_4.configure(image=playerOIcon)

                if i == 1 and j == 2 and board[i * 3 + j] == "X":
                    boardButton_5.configure(image=playerXIcon)
                elif i == 1 and j == 2 and board[i * 3 + j] == "O":
                    boardButton_5.configure(image=playerOIcon)

                if i == 2 and j == 0 and board[i * 3 + j] == "X":
                    boardButton_6.configure(image=playerXIcon)
                elif i == 2 and j == 0 and board[i * 3 + j] == "O":
                    boardButton_6.configure(image=playerOIcon)

                if i == 2 and j == 1 and board[i * 3 + j] == "X":
                    boardButton_7.configure(image=playerXIcon)
                elif i == 2 and j == 1 and board[i * 3 + j] == "O":
                    boardButton_7.configure(image=playerOIcon)

                if i == 2 and j == 2 and board[i * 3 + j] == "X":
                    boardButton_8.configure(image=playerXIcon)
                elif i == 2 and j == 2 and board[i * 3 + j] == "O":
                    boardButton_8.configure(image=playerOIcon)

                print(board[i * 3 + j])


class TicTacToeClient:

    def __init__(self, server_address):
        # super().__init__()
        self.conn = socket.create_connection(server_address)
        self.io = ClientInterface()
        self.board = ['+'] * 9

    def play(self):
        response: str = self.recv_msg()
        mark = response.split(' ')[2]
        opponent_mark = 'O' if mark == 'X' else 'X'
        self.io.show_msg('You are player ' + mark)
        root.title("Tic Tac Toe - Player " + mark)

        if mark == 'X':
            response: str = self.recv_msg()
            self.io.show_msg(response[4:])
            response: str = self.recv_msg()
            self.io.show_msg(response[4:])
            self.play_move()
        else:
            self.io.show_msg('Waiting for opponent to move...')  # This will show in the Entry Widget
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
                response: str = self.recv_msg()
                loc = int(response[15:])
                self.board[loc] = opponent_mark
                self.io.show_board(self.board)
                self.io.show_msg('You lose!')
                break
            elif response.startswith('TIE'):
                self.io.show_msg('It was a tie.')
                break
            elif response.startswith('OTHER_PLAYER_LEFT'):
                self.io.show_msg('Other player left.')
                break

        self.send_msg('QUIT')
        # self.io.show_msg('Game has ended.')

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
    # if len(sys.argv) != 3:
    #   print('Usage:\n' + sys.argv[0] + ' server_ip server_port')
    #  sys.exit()
    root.wait_variable(serverAddress)
    address = (serverAddress.get(), serverPort.get())
    client = TicTacToeClient(address)
    clientThread = threading.Thread(target=client.play)
    clientThread.start()
root.mainloop()
