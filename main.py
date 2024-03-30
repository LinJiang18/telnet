from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
import telnetlib
import time

from PIL import Image, ImageTk

class Connect:
    def __init__(self):
        self.HOST = "170.106.117.254"
        self.PORT = 8081



class Login:
    def __init__(self,tn):
        self.tn = tn
        self.login_tk = Tk()
        self.username = None
        self.password = None

    def client_login(self):
        input_username = self.username.get()
        input_password = self.password.get()
        if len(input_username) == 0:
            showerror(title='hint', message='please input the username')
            self.login_tk.mainloop()
        elif len(input_password) == 0:
            showerror(title='hint', message='please input the password')
            self.login_tk.mainloop()
        else:
            pass

        self.tn.read_until(b'username (guest): ', timeout=0.1)
        self.tn.write(input_username.encode('ascii') + b"\n\n")
        self.tn.read_until(b"password: ", timeout=0.1)
        self.tn.write(input_password.encode('ascii') + b"\n\n")
        time.sleep(0.1)  # what is the usage of the time.sleep?
        system_feedback = self.tn.read_very_eager().decode('utf8')
        system_feedback_num = system_feedback.find("\n")
        system_feedback = system_feedback[:system_feedback_num]
        print(system_feedback)
        if system_feedback == "You have 0 unread message.":
            print('successful login！')
            showinfo(title='hint', message='successful login!')
            self.login_tk.destroy()
            print('Go to Sleep!')
        elif system_feedback != "You have 0 unread message.":
            showerror(title='hint', message='wrong username or password!')
            self.login_tk.mainloop()
        else:
            pass
    #
    # def connect(self):
    #     self.tn = Connect().tn
    #
    # def disconnect(self):
    #     self.tn.write(b"exit\n")

    def show_center(self):
        sw = self.login_tk.winfo_screenwidth()
        sh = self.login_tk.winfo_screenheight()
        ww = 600
        wh = 500
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        self.login_tk.geometry("%dx%d+%d+%d" % (ww, wh, x, y))

    def return_bind(self,event):
        self.client_login()
    def login_window(self):  # 设置登录窗口
        self.login_tk.title('User Login')
        self.show_center()
        self.login_tk.resizable(False, False)
        # 字样
        account_label = Label(self.login_tk, text='account',font=('Arial', 11))
        name_label = Label(self.login_tk, text='password',font=('Arial', 11))
        account_label.place(relx=0.19, rely=0.3, relwidth=0.2, relheight=0.05)
        name_label.place(relx=0.19, rely=0.47, relwidth=0.2, relheight=0.05)
        self.username = StringVar()
        self.password = StringVar()

        # 输入框
        username_input = ttk.Entry(self.login_tk, textvariable=self.username, font=('_Times New Roman', 13))
        password_input = ttk.Entry(self.login_tk, textvariable=self.password, font=('_Times New Roman', 13), show='●')
        username_input.place(relx=0.25, rely=0.35, relwidth=0.5, relheight=0.05)
        password_input.place(relx=0.25, rely=0.52, relwidth=0.5, relheight=0.05)

        # 图片
        load = Image.open('picture/TIC.gif')
        render = ImageTk.PhotoImage(load.resize(tuple([int(0.5 * x) for x in load.size])))

        img = Label(self.login_tk, image=render)
        img.image = render
        img.place(relx=0.28, rely=0.1)


        login_btn = ttk.Button(self.login_tk, text='Login', command=lambda: [self.client_login()])
        login_btn.place(relx=0.4, rely=0.72, relwidth=0.2, relheight=0.07)
        register_btn = ttk.Button(self.login_tk, text='Register', command=lambda: [self.client_login()])
        register_btn.place(relx=0.4, rely=0.82, relwidth=0.2, relheight=0.07)

        self.login_tk.bind('<Return>', self.return_bind)

        self.login_tk.mainloop()


if __name__ == "__main__":
    conn = Connect()
    tn = telnetlib.Telnet(host=conn.HOST, port=conn.PORT, timeout=10)
    login = Login(tn)
    login.login_window()
    # Login Interface
