from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
import threading
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
            user_inter = UserInter(tn,input_username,input_password)
            user_inter.main_window()
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

def window_show_center(login_tk,length = 500, width = 300):
    sw = login_tk.winfo_screenwidth()
    sh = login_tk.winfo_screenheight()
    ww = length
    wh = width
    x = (sw - ww) / 2
    y = (sh - wh) / 2
    login_tk.geometry("%dx%d+%d+%d" % (ww, wh, x, y))

class UserInter:
    def __init__(self,tn,name,password):
        self.tn = tn
        self.login_tk = Tk()
        self.username = name
        self.userpassward = password
        self.thread = None

    def show_center(self):
        sw = self.login_tk.winfo_screenwidth()
        sh = self.login_tk.winfo_screenheight()
        ww = 1200
        wh = 800
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        self.login_tk.geometry("%dx%d+%d+%d" % (ww, wh, x, y))

        # utility function
    def who_window(self):
        who_window = Toplevel(self.login_tk)
        window_show_center(who_window)
        who_window.title('Show All the Users')
        self.tn.write(b"who\n\n")
        time.sleep(0.1)
        contents = self.tn.read_very_eager()
        content_list = contents.splitlines()
        content_list_one = content_list[0].decode('utf-8')
        print(content_list_one)
        content_index = content_list_one.find('total:')
        online_user_num = content_list_one[content_index + len("total:") + 1]
        text1 = Label(who_window,text=f'current online users: {online_user_num}',font=('Arial',18,'bold'))
        text1.place(relx=0.05, rely=0.1)
        text2 = Label(who_window,text= 'current online user accounts:',font=('Arial',18,'bold'))
        text2.place(relx=0.05, rely=0.3)
        var = StringVar()
        content_list_two = content_list[1].decode('utf-8')
        content_list_two = content_list_two.replace(' ',', ')
        content_list_two = content_list_two[:-2]
        var.set(content_list_two)
        l = Label(who_window, textvariable=var, font=('Arial', 23))
        l.place(relx=0.05, rely=0.45)
    def exit_window(self):
        tn.write(b"quit\n")
        time.sleep(0.1)
        tn.write(b"exit\n")
        self.login_tk.destroy()

    def help_window(self):
        help_window = Toplevel(self.login_tk)
        window_show_center(help_window,1500,1200)
        help_window.title('Help')
        self.tn.write(b"help\n\n")
        time.sleep(0.1)
        contents = self.tn.read_very_eager()
        var = StringVar()
        var.set(contents)
        l = Label(help_window, textvariable=var, font=('Arial', 20))
        l.place(relx=0.05, rely=0.05)

    def main_window(self):
        self.tn.write(b"shout test\n\n")


    def monitor(self):
        origin_content = ''
        while(True):
            content = self.tn.read_very_eager().decode('utf-8')
            content = content[8:]
            if len(content) == 0:
                content = origin_content
            else:
                origin_content = content
            message1 = Label(self.login_tk, text=content, bg='grey', font=('Arial', 20), width=30, height=2)
            message1.place(relx=0.4, rely=0.1)
            time.sleep(2)

    def main_window(self):


        self.login_tk.title('User Interface')
        self.show_center()
        self.login_tk.resizable(False, False)

        # user profile
        load1 = Image.open('picture/userprofile.png')
        render1 = ImageTk.PhotoImage(load1.resize(tuple([int(0.9 * x) for x in load1.size])))
        img1 = Label(self.login_tk, image=render1)
        img1.image = render1
        img1.place(relx=0.05, rely=0.1)
        text1 = ttk.Label(self.login_tk, text=f"User Name:  {self.username}",font=('Arial', 18))
        text1.place(relx=0.063, rely=0.37)


        # function area
        who_btn = Button(self.login_tk, text='who', command=lambda: [self.who_window()],font=('_Times New Roman', 18))
        who_btn.place(relx=0.8, rely=0.1, relwidth=0.15, relheight=0.07)

        help_btn = Button(self.login_tk, text='help', command=lambda: [self.help_window()], font=('_Times New Roman', 18))
        help_btn.place(relx=0.8, rely=0.3, relwidth=0.15, relheight=0.07)

        exit_btn = Button(self.login_tk, text='exit',command=lambda: [self.exit_window()],font=('_Times New Roman', 18))
        exit_btn.place(relx=0.8, rely=0.20, relwidth=0.15, relheight=0.07)

        mail_btn = Button(self.login_tk, text='mail', command=lambda: [self.main_window()],font=('_Times New Roman', 18))
        mail_btn.place(relx=0.8, rely=0.40, relwidth=0.15, relheight=0.07)



        # open a thread to parallel computing
        thread = threading.Thread(target=self.monitor)
        thread.start()



        self.login_tk.mainloop()







if __name__ == "__main__":
    conn = Connect()
    tn = telnetlib.Telnet(host=conn.HOST, port=conn.PORT, timeout=10)
    login = Login(tn)
    login.login_window()
    # Login Interface
