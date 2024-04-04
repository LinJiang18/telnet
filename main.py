import copy
import telnetlib
import threading
import time
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo

from PIL import Image, ImageTk

from Chess import Chess


class Connect:
    def __init__(self):
        self.HOST = "170.106.117.254"
        self.PORT = 8081


class Login:
    def __init__(self, tn):
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
        if (system_feedback_one != -1) and (system_feedback_two != -1):
            print('successful login！')
            showinfo(title='hint', message='successful login!')
            self.login_tk.destroy()
            user_inter = UserInter(tn, input_username, input_password, message_num)
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

    def return_bind(self, event):
        self.client_login()

    def register(self):
        register_window = Toplevel(self.login_tk)
        window_show_center(register_window)
        register_window.title('Register')

        self.tn.read_until(b'username (guest): ', timeout=0.1)
        self.tn.write(b'guest\n\n')
        time.sleep(0.1)

        message1 = Label(register_window, text='Username:', font=('Arial', 16, 'bold'))
        message1.place(relx=0.05, rely=0.2)
        message2 = StringVar()
        cmb1 = ttk.Entry(register_window, textvariable=message2, font=('Arial', 14))
        cmb1.place(relx=0.3, rely=0.18, relwidth=0.4, relheight=0.12)

        message3 = Label(register_window, text='Password:', font=('Arial', 16, 'bold'))
        message3.place(relx=0.05, rely=0.4)
        message4 = StringVar()
        cmb2 = ttk.Entry(register_window, textvariable=message4, font=('Arial', 14))
        cmb2.place(relx=0.3, rely=0.38, relwidth=0.4, relheight=0.12)


        def register_send():
            self.tn.read_until(b'< guest: 0 > ', timeout=0.1)
            self.tn.write(b'register ' + message2.get().encode('ascii') + b' ' + message4.get().encode('ascii') + b'\n\n')
            print(message4.get())
            print(len(message4.get()))
            print(message4.get()[-1])
            time.sleep(0.1)

            comment5 = self.tn.read_very_eager().decode('utf-8')
            print(comment5)
            print(len(comment5))
            print(comment5[-1])
            if comment5[:-1] == "user name already exists.":
                showinfo('hint','User Name Already Registered.')
            else:
                showinfo('hint','Successful Registration!')

            time.sleep(0.5)
            self.tn.write(b'logout\n\n')
            register_window.destroy()

        register_btn = Button(register_window, text='Register', command=lambda: [register_send()],font=('Arial', 16))
        register_btn.place(relx=0.35, rely=0.72, relwidth=0.3, relheight=0.15)




    def login_window(self):  # 设置登录窗口
        self.login_tk.title('User Login')
        self.show_center()
        self.login_tk.resizable(False, False)
        # 字样
        account_label = Label(self.login_tk, text='account', font=('Arial', 11))
        name_label = Label(self.login_tk, text='password', font=('Arial', 11))
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
        register_btn = ttk.Button(self.login_tk, text='Register', command=lambda: [self.register()])
        register_btn.place(relx=0.4, rely=0.82, relwidth=0.2, relheight=0.07)

        self.login_tk.bind('<Return>', self.return_bind)

        self.login_tk.mainloop()


def window_show_center(login_tk, length=500, width=300):
    sw = login_tk.winfo_screenwidth()
    sh = login_tk.winfo_screenheight()
    ww = length
    wh = width
    x = (sw - ww) / 2
    y = (sh - wh) / 2
    login_tk.geometry("%dx%d+%d+%d" % (ww, wh, x, y))


class UserInter:
    def __init__(self, tn, name, password, message_num):
        self.tn = tn
        self.login_tk = Tk()
        self.username = name
        self.userpassward = password
        self.message_num = message_num
        self.thread = None
        self.accept_number = 1

        self.chess = None

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
        text1 = Label(who_window, text=f'current online users: {online_user_num}', font=('Arial', 18, 'bold'))
        text1.place(relx=0.05, rely=0.1)
        text2 = Label(who_window, text='current online user accounts:', font=('Arial', 18, 'bold'))
        text2.place(relx=0.05, rely=0.3)
        var = StringVar()
        content_list_two = content_list[1].decode('utf-8')
        content_list_two = content_list_two.replace(' ', ', ')
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
        window_show_center(help_window, 1500, 1200)
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
            self.tn.write(temp_shout_content)
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
        send_btn = Button(shout_window, text='send', command=lambda: [shout_send()], font=('Arial', 15))
        send_btn.place(relx=0.40, rely=0.75, relwidth=0.2, relheight=0.1)

    def mail_window(self):
        mail_window = Toplevel(self.login_tk)
        window_show_center(mail_window, 800, 500)
        mail_window.title('Mail')

        mail_people_label = Label(mail_window, text='Sent to: ', font=('Arial', 16, 'bold'))
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
        mail_content_text = Text(mail_window, width=37, height=3, font=('_Times New Roman', 15))
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
            time.sleep(0.5)
            mail_window.destroy()

        mail_btn = Button(mail_window, text='send', command=lambda: [sent_mail_window()], font=('_Times New Roman', 18))
        mail_btn.place(relx=0.8, rely=0.1, relwidth=0.15, relheight=0.07)

    def stat_window(self):
        stat_window = Toplevel(self.login_tk)
        window_show_center(stat_window)
        stat_window.title('Stat Info')

        stat_label = Label(stat_window, text='User Name:', font=('Arial', 16, 'bold'))
        stat_label.place(relx=0.05, rely=0.135)
        temp_info = copy.copy(self.username)
        stat_info = StringVar(value=temp_info)
        stat_entry = ttk.Entry(stat_window, textvariable=stat_info, font=('_Times New Roman', 15))
        stat_entry.place(relx=0.35, rely=0.135, relwidth=0.3, relheight=0.1)

        def sent_stat_window():
            self.tn.write(b'stats ' + stat_info.get().encode('ascii') + b'\n\n')
            time.sleep(0.1)

            contents = self.tn.read_very_eager()
            var = StringVar()
            var.set(contents)
            l = Label(stat_window, textvariable=var, font=('Arial', 16))
            l.place(relx=0.2, rely=0.27)

        mail_btn = Button(stat_window, text='send', command=lambda: [sent_stat_window()], font=('_Times New Roman', 18))
        mail_btn.place(relx=0.7, rely=0.14, relwidth=0.15, relheight=0.1)

    def block(self):
        block_window = Toplevel(self.login_tk)
        window_show_center(block_window)
        block_window.title('block')

        block_label = Label(block_window, text='block User: ', font=('Arial', 18, 'bold'))
        block_label.place(relx=0.1, rely=0.15)

        block_name = StringVar()
        block_entry = ttk.Entry(block_window, textvariable=block_name, font=('_Times New Roman', 15))
        block_entry.place(relx=0.1, rely=0.35, relwidth=0.3, relheight=0.13)

        def block_function():
            name = block_name.get()
            self.tn.write(b'block ' + name.encode('ascii') + b'\n\n')
            time.sleep(0.5)
            showinfo(title='Hint', message='Successful Block！')


        un_block_btn = Button(block_window, text='block', command=lambda: [block_function()],
                                font=('_Times New Roman', 18, 'bold'))
        un_block_btn.place(relx=0.15, rely=0.6, relwidth=0.2, relheight=0.15)

        un_block_label = Label(block_window, text='unblock User: ', font=('Arial', 18, 'bold'))
        un_block_label.place(relx=0.6, rely=0.15)

        un_block_name = StringVar()
        un_block_entry = ttk.Entry(block_window, textvariable=un_block_name, font=('_Times New Roman', 15))
        un_block_entry.place(relx=0.6, rely=0.35, relwidth=0.3, relheight=0.13)

        def un_block_function():
            name = un_block_name.get()
            self.tn.write(b'unblock ' + name.encode('ascii') + b'\n\n')
            time.sleep(0.5)
            showinfo(title='Hint', message='Successful Unblock！')

        un_block_btn = Button(block_window, text='unblock', command=lambda: [un_block_function()],
                           font=('_Times New Roman', 18, 'bold'))
        un_block_btn.place(relx=0.65, rely=0.6, relwidth=0.2, relheight=0.15)


    def mail_check_window(self):
        mail_check_window = Toplevel(self.login_tk)
        window_show_center(mail_check_window, 800, 600)
        mail_check_window.title('Check Mail')

        tn.write(b"listmail\n\n")
        time.sleep(0.1)
        unread_mail_info = tn.read_very_eager().decode('utf-8')
        unread_mail_info_list = unread_mail_info.split('\n')
        unread_mail_info_list = [x for x in unread_mail_info_list if x != '']
        message_num = unread_mail_info_list[0][-1]
        unread_mail_info_list = unread_mail_info_list[1:]

        text1 = Label(mail_check_window, text=f'you have {message_num} mails', font=('Arial', 20, 'bold'))
        text1.place(relx=0.35, rely=0.05)

        content = ""

        if not unread_mail_info_list:
            mail_check_window.destory()
            self.mail_check_window()

        for one_info in unread_mail_info_list:
            one_info = one_info.split('\t')
            one_info = [x.split(' ') for x in one_info]
            one_info = [x for y in one_info for x in y]
            one_info = [x for x in one_info if x != '']
            one_info = one_info[0] + '   ' + one_info[2] + '   ' + one_info[3] + '   ' + one_info[7] + ' | ' + one_info[
                5] + ' ' + one_info[6] + ' | ' + one_info[8]
            content += one_info
            content += '\n'
        message = Label(mail_check_window, text=content, bg='white', font=('Arial', 18), width=40, height=8)
        message.place(relx=0.16, rely=0.15)



        check_mail_label = Label(mail_check_window, text='Check Mail: ', font=('Arial', 19, 'bold'))
        check_mail_label.place(relx=0.1, rely=0.55)

        check_mail_num = StringVar()
        cmb1 = ttk.Combobox(mail_check_window, textvariable=check_mail_num, font=('Arial', 20))
        cmb1.place(relx=0.3, rely=0.55,relwidth=0.15, relheight=0.05)
        cmb1['value'] = list(range(len(unread_mail_info_list)))

        def show_mail_window():
            num = int(check_mail_num.get())
            show_mail_window = Toplevel(self.login_tk)
            window_show_center(show_mail_window)
            show_mail_window.title('Show Mail')
            writecontent = f"readmail {num}\n\n"
            self.tn.write(writecontent.encode('ascii'))
            print(writecontent)
            time.sleep(0.1)
            contents = self.tn.read_very_eager().decode('utf-8')
            var = StringVar()
            var.set(contents)
            l = Label(show_mail_window, textvariable=var, font=('Arial', 20))
            l.place(relx=0.05, rely=0.05)


        check_mail_btn = Button(mail_check_window, text='check', command=lambda: [show_mail_window()], font=('_Times New Roman', 18, 'bold'))
        check_mail_btn.place(relx=0.2, rely=0.65, relwidth=0.15, relheight=0.07)

        delete_mail_label = Label(mail_check_window, text='Delete Mail: ', font=('Arial', 19, 'bold'))
        delete_mail_label.place(relx=0.5, rely=0.55)

        delete_mail_num = StringVar()
        cmb2 = ttk.Combobox(mail_check_window, textvariable=delete_mail_num, font=('Arial', 20))
        cmb2.place(relx=0.7, rely=0.55,relwidth=0.15, relheight=0.05)
        cmb2['value'] = list(range(len(unread_mail_info_list)))

        def delete_mail_window():
            num = int(delete_mail_num.get())
            writecontent = f"deletemail {num}\n\n"
            self.tn.write(writecontent.encode('ascii'))
            showinfo(title='Hint', message='Successful Delete！')
            time.sleep(0.5)
            mail_check_window.destroy()

        delete_mail_btn = Button(mail_check_window, text='delete', command=lambda: [delete_mail_window()], font=('_Times New Roman', 18, 'bold'))
        delete_mail_btn.place(relx=0.6, rely=0.65, relwidth=0.15, relheight=0.07)

    def send_match_info(self):
        matching_window = Toplevel(self.login_tk)
        window_show_center(matching_window)
        matching_window.title('Matching Window')

        tn.write(b"who\n\n")
        time.sleep(0.1)
        online_user_info = tn.read_very_eager().decode('utf-8')
        online_user_info = online_user_info.split('\n')
        online_user_info = online_user_info[1]
        online_user_info_list = online_user_info.split(' ')
        online_user_info_list = [x for x in online_user_info_list if x != '']
        online_user_info_list = [x for x in online_user_info_list if x != self.username]

        message1 = Label(matching_window, text='opponent:', font=('Arial', 16, 'bold'))
        message1.place(relx=0.10, rely=0.15)

        opponent = StringVar()
        cmb1 = ttk.Combobox(matching_window, textvariable=opponent, font=('Arial', 18))
        cmb1.place(relx=0.35, rely=0.15)
        cmb1['value'] = online_user_info_list

        message2 = Label(matching_window, text='side:', font=('Arial', 16, 'bold'))
        message2.place(relx=0.10, rely=0.35)

        side = StringVar()
        cmb2 = ttk.Combobox(matching_window, textvariable=side, font=('Arial', 14))
        cmb2.place(relx=0.25, rely=0.35, relwidth=0.22, relheight=0.10)
        cmb2['value'] = ['white', 'black']

        message3 = Label(matching_window, text='duration:', font=('Arial', 16, 'bold'))
        message3.place(relx=0.50, rely=0.35)
        duration = StringVar()
        cmb3 = ttk.Entry(matching_window, textvariable=duration, font=('Arial', 14))
        cmb3.place(relx=0.70, rely=0.35, relwidth=0.22, relheight=0.10)

        def send_match_info_to_sb():
            o = opponent.get()
            s = side.get()
            if s == 'white':
                s = 'w'
            elif s == 'black':
                s = 'b'
            else:
                pass
            d = duration.get()
            send_message = f"match {o} {s} {d}\n\n".encode('ascii')
            self.tn.write(send_message)
            print(send_message)
            time.sleep(0.5)
            matching_window.destroy()

        send_btn = Button(matching_window, text='send', command=lambda: [send_match_info_to_sb()],
                          font=('_Times New Roman', 22))
        send_btn.place(relx=0.4, rely=0.60, relwidth=0.2, relheight=0.1)

    def accept_the_game(self, content):
        self.accept_number = 1
        accept_window = Toplevel(self.login_tk)
        window_show_center(accept_window)
        accept_window.title('Matching Window')

        message1 = Label(accept_window, text=content[:content.find("<") - 1], font=('Arial', 22, 'bold'))
        message1.place(relx=0.18, rely=0.2)

        def yes_function():
            self.accept_number = 0
            send_content = content[content.find("<") + 1:content.find(">")]
            self.tn.write(send_content.encode('ascii') + b'\n\n')
            time.sleep(0.5)
            accept_window.destroy()

        def no_function():
            self.accept_number = 0
            time.sleep(0.5)
            accept_window.destroy()

        yes_btn = Button(accept_window, text='Yes', command=lambda: [yes_function()],
                         font=('_Times New Roman', 20))
        yes_btn.place(relx=0.2, rely=0.50, relwidth=0.2, relheight=0.1)

        No_btn = Button(accept_window, text='No', command=lambda: [no_function()],
                        font=('_Times New Roman', 20))
        No_btn.place(relx=0.6, rely=0.50, relwidth=0.2, relheight=0.1)

        while self.accept_number:
            time.sleep(1)

    def game(self, content):
        # Hai, you can write here
        print(content)
        content_list = content.split("\n")
        board = []
        no_count = 9
        for i in [5, 6, 7]:
            c = content_list[i].split(" ")
            for j in [2, 4, 6]:
                if c[j] == ".":
                    board.append(0)
                    no_count -= 1
                elif c[j] == "O":
                    board.append(1)
                else:
                    board.append(2)
        time_ = content_list[2].split()
        time1, time2 = time_[1], time_[3]
        d = content_list[1].split()
        black, white = d[1], d[3]
        me = False
        if (no_count % 2 == 0 and black == self.username) or (no_count % 2 == 1 and white == self.username):
            me = True

        if black == self.username:
            color = "black"
        else:
            color = "white"

        print("me:", me)
        if not self.chess:
            self.chess = Chess(board=board, tn=self.tn, root=self.login_tk, color=color, my_turn=me, time1=time1,
                               time2=time2)
        else:
            self.chess.update(board=board, my_turn=me, time1=time1, time2=time2)

        # print("game end")
        # c.root.destroy()

    def quiet(self):
        self.tn.write(b'quiet\n\n')

    def nonquiet(self):
        self.tn.write(b'nonquiet\n\n')

    def tell_window(self):
        tell_window = Toplevel(self.login_tk)
        window_show_center(tell_window)
        tell_window.title('Mail')

        tell_people_label = Label(tell_window, text='Tell: ', font=('Arial', 16, 'bold'))
        tell_people_label.place(relx=0.05, rely=0.335)
        tell_people_info = StringVar()
        tell_people_entry = ttk.Entry(tell_window, textvariable=tell_people_info, font=('_Times New Roman', 15))
        tell_people_entry.place(relx=0.18, rely=0.325, relwidth=0.3, relheight=0.1)

        tell_content_label = Label(tell_window, text='Contents: ', font=('Arial', 16, 'bold'))
        tell_content_label.place(relx=0.05, rely=0.635)
        tell_content_text = StringVar()
        tell_content_entry = ttk.Entry(tell_window, textvariable=tell_content_text, font=('_Times New Roman', 15))
        tell_content_entry.place(relx=0.30, rely=0.635, relwidth=0.6, relheight=0.1)

        def tell():
            people = tell_people_info.get()
            contents = tell_content_text.get()
            self.tn.write(b'tell ' + people.encode('ascii') + b' ' + contents.encode('ascii') + b'\n\n')
            time.sleep(0.1)
            tell_window.destroy()

        tell_btn = Button(tell_window, text='send', command=lambda: [tell()], font=('_Times New Roman', 20))
        tell_btn.place(relx=0.68, rely=0.30, relwidth=0.25, relheight=0.15)


    def monitor(self):
        origin_content = ''
        while True:
            content = self.tn.read_very_eager().decode('utf-8')
            usernameString = content[content.find(f'<{self.username}: '):content.find(f'<{self.username}: ') + 6 + len(
                self.username)]
            content = content.replace(usernameString, '')

            if content.find('invite you for a game') != -1:
                self.accept_the_game(content)

            if content.find('You Win') != -1 or content.find('You Lose') != -1:
                # time.sleep(2)
                # self.login_tk.after(2000, self.chess.destroy())
                self.chess.destroy(content)
                time.sleep(5)
                self.chess.root.destroy()
                self.chess = None


            else:
                if content.find('Black') != -1 and content.find('White') != -1:
                    self.game(content)

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
        text1 = ttk.Label(self.login_tk, text=f"User Name:  {self.username}", font=('Arial', 18, 'bold'))
        text1.place(relx=0.063, rely=0.37)

        # function area

        match_btn = Button(self.login_tk, text='begin the game', command=lambda: [self.send_match_info()],
                           font=('_Times New Roman', 22))
        match_btn.place(relx=0.4, rely=0.40, relwidth=0.2, relheight=0.1)

        stat_check_btn = Button(self.login_tk, text='stat info', command=lambda: [self.stat_window()],
                                font=('_Times New Roman', 18))
        stat_check_btn.place(relx=0.07, rely=0.46, relwidth=0.15, relheight=0.07)

        who_btn = Button(self.login_tk, text='who', command=lambda: [self.who_window()], font=('_Times New Roman', 18))
        who_btn.place(relx=0.8, rely=0.05, relwidth=0.15, relheight=0.07)

        help_btn = Button(self.login_tk, text='help', command=lambda: [self.help_window()],
                          font=('_Times New Roman', 18))
        help_btn.place(relx=0.8, rely=0.25, relwidth=0.15, relheight=0.07)

        exit_btn = Button(self.login_tk, text='exit', command=lambda: [self.exit_window()],
                          font=('_Times New Roman', 18))
        exit_btn.place(relx=0.8, rely=0.15, relwidth=0.15, relheight=0.07)

        shout_btn = Button(self.login_tk, text='shout', command=lambda: [self.shout_window()],
                           font=('_Times New Roman', 18))
        shout_btn.place(relx=0.8, rely=0.35, relwidth=0.15, relheight=0.07)

        mail_btn = Button(self.login_tk, text='send mail', command=lambda: [self.mail_window()],
                          font=('_Times New Roman', 18))
        mail_btn.place(relx=0.8, rely=0.45, relwidth=0.15, relheight=0.07)

        mail_check_btn = Button(self.login_tk, text='check mail', command=lambda: [self.mail_check_window()],
                                font=('_Times New Roman', 18))
        mail_check_btn.place(relx=0.8, rely=0.55, relwidth=0.15, relheight=0.07)

        tell_btn = Button(self.login_tk, text='tell', command=lambda: [self.tell_window()],
                                font=('_Times New Roman', 18))
        tell_btn.place(relx=0.8, rely=0.65, relwidth=0.15, relheight=0.07)

        block_btn = Button(self.login_tk, text='block', command=lambda: [self.block()],
                           font=('_Times New Roman', 18))
        block_btn.place(relx=0.8, rely=0.75, relwidth=0.15, relheight=0.07)

        match_btn = Button(self.login_tk, text='quiet', command=lambda: [self.quiet()],
                           font=('_Times New Roman', 18))
        match_btn.place(relx=0.75, rely=0.85, relwidth=0.10, relheight=0.07)

        match_btn = Button(self.login_tk, text='nonquiet', command=lambda: [self.nonquiet()],
                           font=('_Times New Roman', 18))
        match_btn.place(relx=0.88, rely=0.85, relwidth=0.10, relheight=0.07)



        # open a thread to parallel computing
        t = threading.Thread(target=self.monitor)
        t.daemon = True
        t.start()

        self.login_tk.mainloop()


if __name__ == "__main__":
    conn = Connect()
    tn = telnetlib.Telnet(host=conn.HOST, port=conn.PORT, timeout=10)
    login = Login(tn)
    login.login_window()
    # Login Interface
