#!/user/bin/python
#!-*- coding:UTF-8 -*-

from Tkinter import *
from ttk import *
import tkMessageBox
from register import *
import pymysql
import time,datetime

class loginPage(object):
    def __init__(self,master,info='Practise Fraud'):
        self.master = master
        self.mainlabel = Label(master,text=info,justify=CENTER)
        self.mainlabel.grid(row=0,columnspan=3)

        self.user = Label(master,text='username',borderwidth=2)
        self.user.grid(row=1,sticky=W)

        self.pwd = Label(master,text='password',borderwidth=2)
        self.pwd.grid(row=2,sticky=W)

        self.userEntry = Entry(master)
        self.userEntry.grid(row=1,column=1,columnspan=2)
        self.userEntry.focus_set()

        self.pwdEntry = Entry(master,show='*')
        self.pwdEntry.grid(row=2,column=1,columnspan=2)

        self.registerButton = Button(master,text='Register',borderwidth=2,command=self.register)
        self.registerButton.grid(row=3,column=0)

        self.loginButton = Button(master,text='Login',borderwidth=2,command=self.login)
        self.loginButton.grid(row=3,column=1)

        self.clearButton = Button(master, text='Clear', borderwidth=2, command=self.clear)
        self.clearButton.grid(row=3, column=2)

    def login(self):
        self.username = self.userEntry.get()
        self.passwd = self.pwdEntry.get()
        if len(self.username)==0 or len(self.passwd) == 0:
            tkMessageBox.showwarning('警告','用户名密码格式不正确')
            self.clear()
            self.userEntry.focus_set()
            return
        else:
            sql = "select * from sys_user where sys_name = '%s' "%self.username
            connect = connect_sql()
            conn = connect.getConnect()
            cursor = conn.cursor()
            cursor.execute(sql)
            res = cursor.fetchall()
            for re in res:
                pwd = base64.b64decode(re[2])
                # print re[1],self.username,re[2],self.username
                if re[1] == self.username and  pwd == self.passwd:
                    self.id = re[0]
                    self.mymainPage = mainPage(self.master,self.id)
                    return
                else:
                    tkMessageBox.showwarning('失败','Login Failed!')
                    self.clear()
                    self.userEntry.focus_set()
            conn.close()

    def register(self):
        self.rootR = Tk()
        self.rootR.title('RegisterPage')
        registerPage(self.rootR)

    def clear(self):
        self.userEntry.delete(0,END)
        self.pwdEntry.delete(0,END)
        self.userEntry.focus_set()

class mainPage(object):
    def __init__(self,master,id):
        self.master =master
        self.id = id

        self.walkDay = 0
        month_day = time.strftime("%m-%d",time.localtime())
        self.month = str(int(month_day.split('-')[0]))
        self.day = str(int(month_day.split('-')[1]))
        self.order_month_day =self.month+'-'+self.day

        self.mainPage = Toplevel(master)
        self.mainLable = Label(self.mainPage,text = 'MainPage',justify = CENTER)
        self.mainLable.grid(row =0,columnspan=4)

        self.btnAdd = Button(self.mainPage,text='Add',borderwidth=2,command=self.add)
        self.btnAdd.grid(row =1,column=0)

        self.btnYesterday = Button(self.mainPage,text='<-Yesterday',borderwidth=2,command=self.yesterday)
        self.btnYesterday.grid(row =1,column=1)

        self.btnTomorrow = Button(self.mainPage,text='Tomorrow->',borderwidth=2,command=self.tomorrow)
        self.btnTomorrow.grid(row =1,column=2)

        self.btnRefresh = Button(self.mainPage,text='Refresh',borderwidth=2,command=self.refresh)
        self.btnRefresh.grid(row =1,column=3)

        self.columns = ("月-天","时-分","科目","学校","价钱","做题人")
        # 定义中心列表区域

        self.tree = Treeview(self.mainPage, show="headings", height=18, columns=("z","a", "b", "c", "d", "e","f"))
        self.tree.grid(row =2,columnspan =4)
        self.vbar = Scrollbar(self.mainPage, orient=VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)
        # 表格的标题
        self.tree.column("z", width=50, anchor="center")
        self.tree.column("a", width=100, anchor="center")
        self.tree.column("b", width=100, anchor="center")
        self.tree.column("c", width=200, anchor="center")
        self.tree.column("d", width=200, anchor="center")
        self.tree.column("e", width=60, anchor="center")
        self.tree.column("f", width=150, anchor="center")
        self.tree.heading("z", text="编号")
        self.tree.heading("a", text="月-天")
        self.tree.heading("b", text="时-分")
        self.tree.heading("c", text="科目")
        self.tree.heading("d", text="学校")
        self.tree.heading("e", text="价格")
        self.tree.heading("f", text="做题人")
        self.tree_data(self.order_month_day)

    def yesterday(self):
        self.walkDay -= 1
        today = datetime.date.today()
        oneday = datetime.timedelta(days=self.walkDay)
        tomorrow = str(today + oneday)
        month = str(int(tomorrow.split('-')[1]))
        day = str(int(tomorrow.split('-')[2]))
        order_month_day =month+'-'+day
        self.order_month_day = order_month_day
        # self.tree_data(order_month_day)
        self.refresh()

    def tomorrow(self):
        self.walkDay += 1
        today = datetime.date.today()
        oneday = datetime.timedelta(days=self.walkDay)
        yesterday = str(today + oneday)
        month = str(int(yesterday.split('-')[1]))
        day = str(int(yesterday.split('-')[2]))
        order_month_day =month+'-'+day
        self.order_month_day = order_month_day
        # self.tree_data(order_month_day)
        self.refresh()

    def tree_data(self,order_month_day):

        print order_month_day
        connect = connect_sql()
        conn = connect.getConnect()
        sql = "select * from cheating_order where sys_id = '%d'and order_month_day = '%s'"%(self.id,order_month_day)
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            res = cursor.fetchall()
            i = 0
            for re in res:
                i += 1
                self.tree.insert('','end',values=(i,re[2],re[3],re[4],re[5],re[6],re[7],re[8]))
            # print res
        except Exception as e:
            print e

    def refresh(self):
        tree = self.tree.get_children()
        for i in tree:
            self.tree.delete(i)
        self.tree_data(self.order_month_day)

    def add(self):
        self.addPage = addPage(self.mainPage,self.id)

class addPage(object):
    def __init__(self,master,sys_id):

        self.master = Toplevel(master)
        self.labeladd = Label(self.master,text='AddPage',justify=CENTER)
        self.labeladd.grid(row = 0,columnspan = 3)

        self.labelmonth_day = Label(self.master,text='月-天', borderwidth=2)
        self.labelmonth_day.grid(row =1,column =0)
        self.labelhour_second = Label(self.master,text='时-分')
        self.labelhour_second.grid(row=2,column=0)
        self.labelsubject = Label(self.master,text='科目')
        self.labelsubject.grid(row=3,column=0)
        self.labelschool = Label(self.master,text='学校')
        self.labelschool.grid(row=4,column=0)
        self.labelmoney = Label(self.master,text='价格')
        self.labelmoney.grid(row=5,column=0)
        self.labelmaker = Label(self.master,text='做题人')
        self.labelmaker.grid(row=6,column=0)

        self.entrymonth_day = Entry(self.master)
        self.entrymonth_day.grid(row=1,column=1,columnspan =2)
        self.entrymonth_day.focus_set()
        self.entryhour_second =Entry(self.master)
        self.entryhour_second.grid(row=2,column=1)
        self.entrysubject =Entry(self.master)
        self.entrysubject.grid(row=3,column=1)
        self.entryschool =Entry(self.master)
        self.entryschool.grid(row=4,column=1)
        self.entrymoney =Entry(self.master)
        self.entrymoney.grid(row=5,column=1)
        self.entrymaker =Entry(self.master)
        self.entrymaker.grid(row=6,column=1)

        self.btnAdd = Button(self.master,text='AddOrder',command=self.addOrder)
        self.btnAdd.grid(row=7,columnspan=3)

        self.id = sys_id
        print sys_id
    def addOrder(self):
        sys_id = self.id
        month_day = self.entrymonth_day.get()
        hour_second = self.entryhour_second.get()
        subject = self.entrysubject.get()
        school = self.entryschool.get()
        money = self.entrymoney.get()
        maker = self.entrymaker.get()
        now = time.strftime('%Y-%m-%d %H:%M',time.localtime())

        connect = connect_sql()
        conn = connect.getConnect()

        cursor = conn.cursor()
        sql = "INSERT INTO cheating_order(sys_id,order_month_day,order_hour_second,order_subject,order_school,order_money,order_maker" \
              ",order_time) VALUES ('%d','%s','%s','%s','%s','%s','%s','%s')" % (sys_id, month_day,hour_second,subject,school,money,maker,now)
        try:
            cursor.execute(sql)
            tkMessageBox.showwarning('警告','AddOrder Success！')
            conn.commit()

        except Exception as e:
            print e
            conn.rollback()#事务回滚，一条插入错误那么都不插入，保证原子性
        conn.close()

class connect_sql(object):
    def getConnect(self):
        conn = pymysql.connect(host='202.194.14.145', port=3306, user='root', passwd='qlscadmin', db='cheating')
        return conn

if __name__ =='__main__':
    root = Tk()
    root .title('SecretForWhat')
    myLoginPage = loginPage(root)
    root.mainloop()