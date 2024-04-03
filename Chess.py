from tkinter import *


class Chess:

    def __init__(self, board=None, tn=None, root=None, color="black", my_turn=False, time1=None, time2=None):
        self.row, self.column = 3, 3
        self.mesh = 100
        self.ratio = 0.9
        self.board_color = "#CDBA96"
        self.header_bg = "#CDC0B0"
        self.btn_font = ("黑体", 12, "bold")
        self.step = self.mesh / 2
        self.chess_r = self.step * self.ratio
        self.point_r = self.step * 0.2
        self.matrix = [[0 for y in range(self.column)] for x in range(self.row)]
        # self.is_start = False
        self.is_black = True
        self.last_p = None

        self.colorr = color
        self.is_start = my_turn
        self.myturn = my_turn
        self.time1 = time1
        self.time2 = time2

        if root:
            self.root = Toplevel(root)
        else:
            self.root = Tk()

        self.root.title("Tic-Tac-Toe")
        self.root.resizable(width=False, height=False)

        self.f_header = Frame(self.root, highlightthickness=0, bg=self.header_bg)
        self.f_header.pack(fill=BOTH, ipadx=10)

        self.l_info = Label(self.f_header, text="未开始", bg=self.header_bg, font=("楷体", 18, "bold"), fg="white")
        self.b_lose = Button(self.f_header, text="Resign", command=self.bf_lose, state=DISABLED, font=self.btn_font)

        self.b_refresh = Button(self.f_header, text="Refresh", command=self.bf_refresh, state=DISABLED,
                                font=self.btn_font)

        self.l_info.pack(side=LEFT, expand=YES, fill=BOTH, pady=20)

        self.b_lose.pack(side=RIGHT, padx=30)
        self.b_refresh.pack(side=RIGHT, padx=30)

        self.c_chess = Canvas(self.root, bg=self.board_color, width=(self.column + 1) * self.mesh,
                              height=(self.row + 1) * self.mesh, highlightthickness=0)
        self.draw_board()
        self.c_chess.bind("<Button-1>", self.cf_board)
        self.c_chess.pack()

        self.bf_start()

        if board:
            self.set(board)
        self.tn = tn

    def bf_refresh(self):
        self.tn.write(b"refresh\n\n")

    def draw_mesh(self, x, y):
        ratio = (1 - self.ratio) * 0.99 + 1
        center_x, center_y = self.mesh * (x + 1), self.mesh * (y + 1)
        self.c_chess.create_rectangle(center_y - self.step, center_x - self.step,
                                      center_y + self.step, center_x + self.step,
                                      fill=self.board_color, outline=self.board_color)
        a, b = [0, ratio] if y == 0 else [-ratio, 0] if y == self.row - 1 else [-ratio, ratio]
        c, d = [0, ratio] if x == 0 else [-ratio, 0] if x == self.column - 1 else [-ratio, ratio]
        self.c_chess.create_line(center_y + a * self.step, center_x, center_y + b * self.step, center_x)
        self.c_chess.create_line(center_y, center_x + c * self.step, center_y, center_x + d * self.step)
        if ((x == 3 or x == 11) and (y == 3 or y == 11)) or (x == 7 and y == 7):
            self.c_chess.create_oval(center_y - self.point_r, center_x - self.point_r,
                                     center_y + self.point_r, center_x + self.point_r, fill="black")

    def draw_chess(self, x, y, color):
        center_x, center_y = self.mesh * (x + 1), self.mesh * (y + 1)
        self.c_chess.create_oval(center_y - self.chess_r, center_x - self.chess_r,
                                 center_y + self.chess_r, center_x + self.chess_r,
                                 fill=color)

    def draw_board(self):
        [self.draw_mesh(x, y) for y in range(self.column) for x in range(self.row)]

    def center_show(self, text):
        width, height = int(self.c_chess['width']), int(self.c_chess['height'])
        self.c_chess.create_text(int(width / 2), int(height / 2), text=text, font=("黑体", 30, "bold"), fill="red")

    def bf_start(self):
        self.set_btn_state("start")
        self.is_start = True
        self.is_black = True
        self.matrix = [[0 for y in range(self.column)] for x in range(self.row)]
        self.draw_board()
        if self.colorr == "black":
            self.l_info.config(text=f"*Black:{self.time1}\nWhite:{self.time2}")
        else:
            self.l_info.config(text=f"Black:{self.time1}\n*White:{self.time2}")

    def bf_lose(self):
        self.tn.write(b"resign\n\n")
        self.set_btn_state("init")
        self.is_start = False

        if self.colorr == "black":
            text = "black resigns"
        else:
            text = "white resigns"

        self.l_info.config(text=text)

    def cf_board(self, e):
        if not self.myturn:
            print("Nooooooooooooooooooo")
            return

        x, y = int((e.y - self.step) / self.mesh), int((e.x - self.step) / self.mesh)

        center_x, center_y = self.mesh * (x + 1), self.mesh * (y + 1)

        distance = ((center_x - e.y) ** 2 + (center_y - e.x) ** 2) ** 0.5

        if distance > self.step * 0.95 or self.matrix[x][y] != 0:
            return

        color = self.ternary_operator("black", "white")
        tag = self.ternary_operator(1, -1)

        self.draw_chess(x, y, self.colorr)
        self.matrix[x][y] = tag
        self.last_p = [x, y]

        self.is_start = False
        self.parse(x, y)

    def parse(self, x, y):
        move = ""
        if x == 0:
            move += "a"
        elif x == 1:
            move += "b"
        else:
            move += "c"

        move += str(y + 1)
        # print(move)
        move += "\n\n"
        try:
            self.tn.write(move.encode('ascii'))

        except AttributeError:
            pass

    def set_btn_state(self, state):
        state_list = [NORMAL, DISABLED, DISABLED, DISABLED] if state == "init" else [DISABLED, NORMAL, NORMAL, NORMAL]
        self.b_lose.config(state=state_list[3])
        self.b_refresh.config(state=state_list[3])

    def ternary_operator(self, true, false):
        return true if self.is_black else false

    def set(self, lst: list):
        for i, j in enumerate(lst):
            x, y = i // 3, i % 3
            if j == 1:
                c = "white"
            elif j == 2:
                c = "black"
            else:
                c = None

            if c and self.matrix[x][y] == 0:
                self.draw_chess(x, y, c)
                self.matrix[x][y] = self.ternary_operator(1, -1)

    def update(self, board, my_turn, time1=None, time2=None):
        self.set(board)
        self.myturn = my_turn
        self.time1 = time1
        self.time2 = time2

        if self.colorr == "black":
            self.l_info.config(text=f"*Black:{self.time1}\nWhite:{self.time2}")
        else:
            self.l_info.config(text=f"Black:{self.time1}\n*White:{self.time2}")

    def destroy(self, content):
        self.l_info.config(text=f"{content}")


if __name__ == '__main__':
    c = Chess([1, 2, 0, 1])
