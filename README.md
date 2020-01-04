from Tkinter import *
from tkinter import messagebox
import sqlite3 as s
import requests as r
import bs4

try:
    client=s.connect("E://project.db")
    cu=client.cursor()
    cu.execute("create table std(name varchar(50),contactno int,emailid varchar(50),password varchar(25))")
except:
    pass

def login():
    global scr,scr1
    try:
        scr1.destroy()
    except:
        pass
    scr=Tk()
    scr.geometry('300x400')
    scr.title('login_Page')
    l=Label(scr,text='Login Page',font=('times',20,'bold'),bg='blue',fg='yellow')
    l.pack(side=TOP,fill=X)
    l1=Label(scr,text='Username',font=('times',16,'italic'))
    l1.pack()
    e1=Entry(scr,font=('default',16,'italic'))
    e1.pack()
    l2=Label(scr,text='Password',font=('times',16,'italic'))
    l2.pack()
    e2=Entry(scr,font=('default',16,'italic'),show='*')
    e2.pack()
    def b():
        cu.execute("select count(*) from std where emailid=%r and password=%r"%(e1.get(),e2.get()))
        a=cu.fetchall()
        if a[0][0]==1:
            messagebox.showinfo('Login','Login successfull..')
            main()
        else:
            messagebox.showerror('Login','Username and Password does not match.')
            
    b=Button(scr,text='Login',font=('times',20,'italic'),bg='green',fg='white',command=b)
    b.pack()
    b1=Button(scr,text='Register',font=('times',20,'italic'),bg='red',fg='white',command=register)
    b1.pack()


def register():
    global scr,scr1
    scr.destroy()
    scr1=Tk()
    scr1.geometry('300x400')
    scr1.title('Registration_Page')
    l=Label(scr1,text='Register Page',font=('times',20,'bold'),bg='blue',fg='yellow')
    l.pack(side=TOP,fill=X)
    l1=Label(scr1,text='Name',font=('times',16,'italic'))
    l1.pack()
    e1=Entry(scr1,font=('default',16,'italic'))
    e1.pack()
    l2=Label(scr1,text='Contact Number',font=('times',16,'italic'))
    l2.pack()
    e2=Entry(scr1,font=('default',16,'italic'))
    e2.pack()
    l3=Label(scr1,text='Email-Id',font=('times',16,'italic'))
    l3.pack()
    e3=Entry(scr1,font=('default',16,'italic'))
    e3.pack()
    l4=Label(scr1,text='Password',font=('times',16,'italic'))
    l4.pack()
    e4=Entry(scr1,font=('default',16,'italic'))
    e4.pack()
    def b():
        try:
            cu.execute("insert into std(name,contactno,emailid,password) values(%r,%d,%r,%r)"%(e1.get(),int(e2.get()),e3.get(),e4.get()))
            client.commit()
            messagebox.showinfo('Register',"Registration Successfull..")
            login()
        except:
            messagebox.showerror('Registration','Registration Failed..')
    b=Button(scr1,text='Submit',font=('times',20,'italic'),bg='green',fg='white',command=b)
    b.pack()

def main():
    global scr,m
    scr.destroy()
    scr2=Tk()
    scr2.title('Medical Assistance')
    l=Label(scr2,text='Main Page',font=('times',20,'bold'),bg='blue',fg='yellow')
    l.pack(side=TOP,fill=X)
    l1=Label(scr2,text='Enter the name of medicine',font=('times',16,'italic'))
    l1.pack()
    e1=Entry(scr2,font=('default',16,'italic'))
    e1.pack()
    m=Message(scr2)
    def scrap():
        lst=[]
        dt=r.request('get','https://www.1mg.com/search/all?name=%s'%(e1.get()))
        s=bs4.BeautifulSoup(dt.text,'html.parser')
        for i in s.findAll('div'):
            if i.get('class'):
                if len([x for x in i.get('class') if 'style__container__' in x])>0:
                    if i.find('a'):
                        x=i.find('a')
                        try:
                    
                            dts=r.request('get','https://www.1mg.com'+x.get('href'))
                            s1=bs4.BeautifulSoup(dts.text,'html.parser')
                            for j in s1.findAll('div'):
                                if j.get('class'):
                                    if len([x for x in j.get('class') if '_product-description' in x])>0:
                                    
                                        try:
                                            lst.append(j.text)    
                                        except:
                                            pass
                                        
                                    elif  len([x for x in j.get('class') if 'DrugOverview__container' in x])>0:
                                    
                                        try:
                                            lst.append(j.text)
                                        except:
                                            pass
                        except:
                            pass

        global data                        
        data=iter(lst)
        m.config(text=next(data),bg='yellow')
    
    b=Button(scr2,text='Search',font=('times',20,'italic'),bg='green',fg='white',command=scrap)
    b.pack()
    m.pack()
    def nxt():
        global data,m
        try:
            m.config(text=next(data),bg='yellow')
        except:
            m.config(text='Finish Information',bg='yellow')
    b1=Button(scr2,text='Next',font=('times',20,'italic'),bg='Cyan',fg='black',command=nxt)
    b1.pack(side=BOTTOM)
    

login()
