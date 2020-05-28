from tkinter import *  # for all widgets of tkinter
from tkinter import messagebox  # for messagebox
import sqlite3 as s  # for database
import requests as r  # for sending requests to the server
import bs4  # for web scraping
import os  # for creating folders
from PIL import ImageTk,Image  # for image processing 
from io import BytesIO  # for binary data storing
import shutil  # for folder deleting if it is not empty
try:
    client=s.connect("D://proj.db")
    cu=client.cursor()
    cu.execute("create table info(name varchar(50),emailid varchar(50),password varchar(50),contactno int)")
except:
    pass

def login():
    global scr,scr1
    try:
        scr1.destroy()
    except:
        pass
    scr=Tk()
    scr.title("Medical Assistance")
    scr.geometry('300x300')
    l=Label(scr,text="Login Page",bg="blue",fg='yellow')
    l.pack(side=TOP,fill=X)
    l1=Label(scr,text="Username")
    l1.pack()
    e1=Entry(scr)
    e1.pack()
    l2=Label(scr,text="Password")
    l2.pack()
    e2=Entry(scr,show="*")
    e2.pack()
    def b1():
        cu.execute("select count(*) from info where emailid=%r and password=%r"%(e1.get(),e2.get()))
        a=cu.fetchall()
        if a[0][0]==1:
            messagebox.showinfo("Successful","Login Successfull....!")
            main()
        else:
            messagebox.showerror("Login Failed","Username & Password did not match..")
    b1=Button(scr,text="Login",command=b1)
    b1.pack()
    def b2():
        register()
    b2=Button(scr,text="Register",command=register)
    b2.pack()
    scr.mainloop()

def register():
    global scr,scr1
    try:
        scr.destroy()
    except:
        pass
    scr1=Tk()
    scr1.title("Medical Assistance")
    scr1.geometry('300x300')
    l=Label(scr1,text="Registration Page",bg="blue",fg='yellow')
    l.pack(side=TOP,fill=X)
    l1=Label(scr1,text="Name")
    l1.pack()
    e1=Entry(scr1)
    e1.pack()
    l2=Label(scr1,text="EmailId")
    l2.pack()
    e2=Entry(scr1)
    e2.pack()
    l3=Label(scr1,text="Password")
    l3.pack()
    e3=Entry(scr1)
    e3.pack()
    l4=Label(scr1,text="Contactno")
    l4.pack()
    e4=Entry(scr1)
    e4.pack()
    def b1():
        cu.execute("insert into info values(%r,%r,%r,%d)"%(e1.get(),e2.get(),e3.get(),int(e4.get())))
        client.commit()
        messagebox.showinfo("Register",'Registration Successfull..!')
        login()
    b1=Button(scr1,text="Submit",command=b1)
    b1.pack()
    scr1.mainloop()
    

def main():
    global scr
    try:
        scr.destroy()
    except:
        pass
    scr3=Tk()
    scr3.title("Medical Assistance")
    scr3.geometry('600x600')
    l=Label(scr3,text="Main Page",bg="blue",fg='yellow')
    l.pack(side=TOP,fill=X)
    l1=Label(scr3,text="Enter Medicine Name")
    l1.pack()
    e1=Entry(scr3)
    e1.pack()
    m=Message(scr3,width=300)
    imglabel=Label(scr3)
    m1=Message(scr3)
    def fun():
        img=Image.open('c://download//'+str(next(imgg)))
        img=img.resize((400,400),Image.ANTIALIAS)
        pic=ImageTk.PhotoImage(img)
        imglabel.config(image=pic)
        scr.mainloop()
    def scrap():
        try:
            shutil.rmtree("C://download")
        except:
            pass
        os.chdir('C://')
        try:
            os.mkdir('download')
        except:
            pass
        os.chdir('C://download')
        
        n=0
        lst=[]
        lbl=[]
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
                            for l in s1.findAll('div',{'class':'col-xs-10 ProductImage__preview-container___2oTeX'}):
                                for im in l.findAll('img'):
                                    if im.get('src').startswith('https'):
                                        ig=r.request('get',im.get('src'))
                                        open('img{}.jpg'.format(n),'wb').write(BytesIO(ig.content).read())
                                        n+=1
                            for k in s1.findAll('h1',{'class':'ProductTitle__product-title___3QMYH'}):
                                try:
                                    lbl.append(k.text)
                                except:
                                    pass
                            for j in s1.findAll('div'):
                                if j.get('class'):
                                    if len([x for x in j.get('class') if '_product-description' in x])>0:
                                    
                                        try:
                                            lst.append(j.text)    
                                        except:
                                            lst.append('Inforamtion Hidden')
                                        
                                    elif  len([x for x in j.get('class') if 'DrugOverview__container' in x])>0:
                                    
                                        try:
                                            lst.append(j.text)
                                        except:
                                            lst.append('Information Hidden')
                        except:
                            pass
        os.chdir(r"C:\download")
        new=[]
        for imm in range(len(os.listdir())):
            new.append('img'+str(imm)+'.jpg')
        global data,title,imgg
        imgg=iter(new)
        title=iter(lbl)
        data=iter(lst)
        m.config(text=next(title),bg='white')
        m1.config(text=next(data),bg='white')
        fun()
    b1=Button(scr3,text="Search",command=scrap)
    b1.pack()
    def b2():
        try:
            m.config(text=(next(title)),bg='white')
        except:
            m.config(text='')
        try:
            m1.config(text=(next(data)),bg='white')
        except:
            m1.config(text='Inforamtion Hidden/Finished',bg='white')
        try:
            fun()
        except:
            pass
    m.pack()
    m1.pack()
    imglabel.place(x=20,y=100)
    b2=Button(scr3,text="Next",command=b2)
    b2.pack(side=BOTTOM)
    scr3.mainloop()

login()
