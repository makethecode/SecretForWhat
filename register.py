#!/user/bin/python
#! -*- coding:UTF-8 -*-

from Tkinter import *
import base64
import pymysql
import tkMessageBox

class registerPage(object):
    def __init__(self,master):
        self.master = master
        self.label = Label(self.master,text='Register',justify=CENTER)
        self.label.grid(row=0,columnspan=3)

        self.labeluser = Label(self.master,text='username',borderwidth=2)
        self.labeluser.grid(row=1,column=0)

        self.labelpwd = Label(self.master,text = 'password',borderwidth=2)
        self.labelpwd.grid(row=2,column=0)

        self.usernameR = Entry(self.master)
        self.usernameR.grid(row = 1,column=1,columnspan=2)
        self.usernameR.focus_set()

        self.passwordR = Entry(self.master,show='*')
        self.passwordR.grid(row=2,column=1,columnspan=2)

        self.btnRegister = Button(self.master,text = 'Register',command=self.register)
        self.btnRegister.grid(row=3,column=1)

    def register(self):
        username = self.usernameR.get()
        password = self.passwordR.get()
        secretpwd = base64.b64encode(password)
        if username != '' and password != '':
            # self.connect(username,secretpwd)
            conn = pymysql.connect(host='202.194.14.145', port=3306, user='root', passwd='qlscadmin', db='cheating')
            cursor = conn.cursor()
            sql = "INSERT INTO sys_user(sys_name,sys_pwd) VALUES ('%s','%s')" % (username, secretpwd)
            try:
                cursor.execute(sql)
                tkMessageBox.showwarning('警告','Register Success!')
                conn.commit()
            except Exception as e:
                tkMessageBox.showwarning('警告','Register Error!')
                conn.rollback()
            conn.close()

        # print username,secretpwd,base64.b64decode(secretpwd)


    # def connect(self,username,password):
    #
    #     # print cursor

if __name__ == '__main__':
    root = Tk()
    root .title('SecretForWhat')
    myRegisterPage = registerPage(root)
    root.mainloop()

