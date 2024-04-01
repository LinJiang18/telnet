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
        system_feedback_one = system_feedback.find("You have")
        system_feedback_two = system_feedback.find("unread message.")
        message_num = system_feedback[system_feedback_one + 9]
        print(system_feedback_one)
        print(system_feedback_two)
        print(message_num)
        if (system_feedback_one != -1) and (system_feedback_two != -1):
            print('successful login！')
            showinfo(title='hint', message='successful login!')
            self.login_tk.destroy()
            user_inter = UserInter(tn,input_username,input_password)
            user_inter.main_window()
        elif system_feedback_one == -1 or system_feedback_two == -1:
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

    def shout_window(self):
        def shout_send():
            input_shout_content = shout_content.get()
            temp_shout_content = b"shout " + input_shout_content.encode('ascii') + b"\n\n"
            print(temp_shout_content)
            tn.write(temp_shout_content)
            time.sleep(0.1)
            shout_window.destroy()

        shout_window = Toplevel(self.login_tk)
        window_show_center(shout_window)
        shout_window.title('Shout')
        shout_label = Label(shout_window, text='shout contents: ', font=('Arial', 16, 'bold'))
        shout_label.place(relx=0.25, rely=0.3, relwidth=0.35, relheight=0.05)
        shout_content = StringVar()
        shout_input = ttk.Entry(shout_window, textvariable=shout_content, font=('_Times New Roman', 15))
        shout_input.place(relx=0.25, rely=0.4, relwidth=0.5, relheight=0.12)
        send_btn = Button(shout_window, text='send', command=lambda: [shout_send()],font=('Arial', 15))
        send_btn.place(relx=0.40, rely=0.75, relwidth=0.2, relheight=0.1)





    def mail_window(self):
        mail_window = Toplevel(self.login_tk)
        window_show_center(mail_window,800,500)
        mail_window.title('Mail')

        mail_people_label = Label( mail_window, text='Sent to: ',font=('Arial', 16,'bold'))
        mail_people_label.place(relx=0.05, rely=0.135, relwidth=0.15, relheight=0.05)
        mail_people_info = StringVar()
        mail_people_entry = ttk.Entry(mail_window, textvariable=mail_people_info, font=('_Times New Roman', 15))
        mail_people_entry.place(relx=0.20, rely=0.125, relwidth=0.3, relheight=0.08)

        mail_title_label = Label(mail_window, text='Title: ', font=('Arial', 16, 'bold'))
        mail_title_label.place(relx=0.05, rely=0.335, relwidth=0.2, relheight=0.05)
        mail_title_info = StringVar()
        mail_title_entry = ttk.Entry(mail_window, textvariable=mail_title_info, font=('_Times New Roman', 15))
        mail_title_entry.place(relx=0.20, rely=0.325, relwidth=0.5, relheight=0.08)

        mail_content_label = Label(mail_window, text='Contents: ', font=('Arial', 16, 'bold'))
        mail_content_label.place(relx=0.02, rely=0.535, relwidth=0.2, relheight=0.05)
        mail_content_text = Text(mail_window,width=37,height=3,font=('_Times New Roman', 15))
        mail_content_text.place(relx=0.20, rely=0.525)

        def sent_mail_window():
            mail_people = mail_people_info.get()
            mail_title = mail_title_info.get()
            mail_content = (mail_content_text.get("0.0", "end")).split("\n")
            mail_content.pop()
            send_message = b"mail " + mail_people.encode('ascii') + b" " + mail_title.encode('ascii') + b'\n\n'
            print(send_message)
            self.tn.write(send_message)
            time.sleep(0.1)
            for content in mail_content:
                self.tn.write(content.encode('ascii') + b"\n\n")
                time.sleep(0.05)
                print(content.encode('ascii') + b"\n\n")
            self.tn.write(b".\n\n")
            print(b".\n\n")
            showinfo(title='hint', message='Message sent!')
            time.sleep(1)
            mail_window.destroy()


        mail_btn = Button(mail_window, text='send', command=lambda: [sent_mail_window()], font=('_Times New Roman', 18))
        mail_btn.place(relx=0.8, rely=0.1, relwidth=0.15, relheight=0.07)



    def monitor(self):
        origin_content = ''
        while(True):
            content = self.tn.read_very_eager().decode('utf-8')
            usernameString = content[content.find(f'<{self.username}: '):content.find(f'<{self.username}: ') + 5 + len(self.username)]
            content = content.replace(usernameString, '')
            # if '<' + self.username in content:
            #     content = content[8:]
            if len(content) == 0:
                content = origin_content
            else:
                origin_content = content
            message_label = Label(self.login_tk, text='Message Box', font=('Arial', 14, 'bold'))
            message_label.place(relx=0.42, rely=0.06, relwidth=0.15, relheight=0.08)
            message = Label(self.login_tk, text=content, bg='white', font=('Arial', 20), width=30, height=4)
            message.place(relx=0.30, rely=0.14)
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
        text1 = ttk.Label(self.login_tk, text=f"User Name:  {self.username}",font=('Arial', 18, 'bold'))
        text1.place(relx=0.063, rely=0.37)


        # function area
        who_btn = Button(self.login_tk, text='who', command=lambda: [self.who_window()],font=('_Times New Roman', 18))
        who_btn.place(relx=0.8, rely=0.1, relwidth=0.15, relheight=0.07)

        help_btn = Button(self.login_tk, text='help', command=lambda: [self.help_window()], font=('_Times New Roman', 18))
        help_btn.place(relx=0.8, rely=0.3, relwidth=0.15, relheight=0.07)

        exit_btn = Button(self.login_tk, text='exit',command=lambda: [self.exit_window()],font=('_Times New Roman', 18))
        exit_btn.place(relx=0.8, rely=0.20, relwidth=0.15, relheight=0.07)

        shout_btn = Button(self.login_tk, text='shout', command=lambda: [self.shout_window()],font=('_Times New Roman', 18))
        shout_btn.place(relx=0.8, rely=0.40, relwidth=0.15, relheight=0.07)

        mail_btn = Button(self.login_tk, text='send mail', command=lambda: [self.mail_window()],font=('_Times New Roman',18))
        mail_btn.place(relx=0.8, rely=0.50, relwidth=0.15, relheight=0.07)



        # open a thread to parallel computing
        t = threading.Thread(target=self.monitor)
        t.daemon=True
        t.start()




        self.login_tk.mainloop()







if __name__ == "__main__":
    conn = Connect()
    tn = telnetlib.Telnet(host=conn.HOST, port=conn.PORT, timeout=10)
    login = Login(tn)
    login.login_window()
    # Login Interface
