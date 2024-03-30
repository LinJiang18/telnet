from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
USENAME = 'zhangsan'
PASSWORD = '123'


class Center:  # 窗口居中方法
    @staticmethod
    def show_center(self_tk):
        sw = self_tk.winfo_screenwidth()
        sh = self_tk.winfo_screenheight()
        ww = 600
        wh = 500
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        self_tk.geometry("%dx%d+%d+%d" % (ww, wh, x, y))


def login():  # 设置登录窗口
    login_tk = Tk()
    login_tk.title('用户登录')
    Center.show_center(login_tk)
    login_tk.resizable(False, False)  # 不可调整大小和最大化
    # 字样
    no_label = Label(login_tk, text='账号')
    name_label = Label(login_tk, text='密码')
    no_label.place(relx=0.17, rely=0.3, relwidth=0.2, relheight=0.05)
    name_label.place(relx=0.17, rely=0.47, relwidth=0.2, relheight=0.05)
    username = StringVar()
    password = StringVar()

    # 输入框
    username_input = ttk.Entry(login_tk, textvariable=username, font=('Microsoft yahei', 11))
    password_input = ttk.Entry(login_tk, textvariable=password, font=('_Times New Roman', 11), show='●')
    username_input.place(relx=0.25, rely=0.35, relwidth=0.5, relheight=0.05)
    password_input.place(relx=0.25, rely=0.52, relwidth=0.5, relheight=0.05)


    login_btn = ttk.Button(login_tk, text='登    录', command=lambda: [user()])
    login_btn.place(relx=0.4, rely=0.72, relwidth=0.2, relheight=0.07)

    # 按钮事件
    def btn_bind(self):
        user()

    # 绑定按钮
    login_tk.bind("<Return>", btn_bind)  # 绑定回车键

    login_tk.mainloop()

    def user():
        username_txt = username.get()
        password_txt = password.get()

        # 账号密码
        if username_txt == USENAME and password_txt == PASSWORD:
            print('登录成功！')
            showinfo(title='提示', message='登录成功')
            login_tk.destroy()
            # class_.Main.main()  ,此处换成你所需要调用的函数即可
        elif len(username_txt) == 0:
            showerror(title='提示', message='请输入账号！')
            login_tk.mainloop()
        elif len(password_txt) == 0:
            showerror(title='提示', message='请输入密码！')
            login_tk.mainloop()
        elif username_txt != USENAME or password_txt != PASSWORD:
            showerror(title='提示', message='请输入正确的账号与密码！')
            login_tk.mainloop()
        else:
            login_tk.quit()

if __name__ == '__main__':
    login()