from tkinter import *
from tkinter.ttk import Combobox
import random
import pyperclip
import sqlite3
import json
from tkinter import messagebox
import re

conn = sqlite3.connect('PasswordManager.db')
# Create cursor
c = conn.cursor()

try:
    c.execute("""CREATE TABLE user (
            email text,
            m_password text
        )
        """)
except:
    pass

try:
    c.execute("""CREATE TABLE acc_info (
            acc text,
            website text,
            password text,
            uid text
        )
        """)
except:
    pass


class PasswordDefender(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)


        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.title('Password Defender')
        self.geometry('600x400')
        self.resizable(False, False)
        self.configure(background='#F2F2F2')
        global line
        line = PhotoImage(file='images/line.png')
        global s_logo
        s_logo= PhotoImage(file='images/defaultLogo.png')
        global back_Btn_pic
        back_Btn_pic= PhotoImage(file='images/Back.png')

        self.frames = {}
        for F in (FirstPage, LoginPage, RegisterPage, OptionsPage, GenPassPage, GenPassPage1, GenSavePage, GetPassPage,UpdateFirstPage, VerifyPage, UpdateLastPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("FirstPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()



class FirstPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        t1 = Label(self, text='Password Defender', font=('Roboto Slab Bold', 18), fg='#00B0F0', bg='#F2F2F2')
        t1.place(x=190, y=150)

        motto = Label(self, text='A better place to safe your information', font=('Roboto Slab Bold', 9), fg='#7C7C7C',bg='#F2F2F2')
        motto.place(x=190, y=180)

        self.b_logopic = PhotoImage(file='images/logo.png')
        logo = Button(self, image=self.b_logopic, border=0)
        logo.place(x=250, y=30)

        self.img_button = PhotoImage(file='images/loginBtn.png')
        b1 = Button(self, image=self.img_button, border=0, command=lambda: controller.show_frame("LoginPage"))
        b1.place(x=180, y=250)

        self.img_button2 = PhotoImage(file='images/RegBtn.png')
        b1 = Button(self, image=self.img_button2, border=0, command=lambda: controller.show_frame("RegisterPage"))
        b1.place(x=320, y=250)



class LoginPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        t1 = Label(self, text='Password Defender', font=('Roboto Slab Bold', 18), fg='#00B0F0', bg='#F2F2F2')
        t1.place(x=200, y=27)

        motto = Label(self, text='A better place to safe your information', font=('Roboto Slab Bold', 9), fg='#7C7C7C',bg='#F2F2F2')
        motto.place(x=198, y=55)

        lt1 = StringVar("")
        lt2 = StringVar("")
        t1 = Label(self, text='Login your Account', font=('Roboto Slab Bold', 15), fg='#00B0F0', bg='#F2F2F2')
        t1.place(x=205, y=80)

        logo = Button(self, image=s_logo, border=0)
        logo.place(x=150, y=27)

        email = Label(self, text='Email Address       :', font=('Roboto Slab Medium', 13), fg='#034961', bg='#F2F2F2')
        email.place(x=100, y=160)

        l1 = Label(self, image=line, border=0)
        l1.place(x=253, y=180)

        self.e_input = Entry(self, font=('Roboto Slab', 9), text=lt1, bg='#F2F2F2', border=0, width=35)
        self.e_input.place(x=260, y=165)

        pwd = Label(self, text='Master Password :', font=('Roboto Slab Medium', 13), fg='#034961', bg='#F2F2F2')
        pwd.place(x=100, y=210)

        
        l2 = Label(self, image=line, border=0)
        l2.place(x=253, y=227)

        self.pass_input = Entry(self, show='*', font=('Roboto Slab', 9), text=lt2, bg='#F2F2F2', border=0, width=35)
        self.pass_input.place(x=260, y=210)
        self.pass_input.bind('<Return>',self.login)

        self.img_button2 = PhotoImage(file='images/loginBtn.png')
        self.b1 = Button(self, cursor='hand2', image=self.img_button2, border=0, command=lambda: self.login())
        self.b1.place(x=370, y=270)
        

        back = Button(self, cursor='hand2', image=back_Btn_pic, border=0, command=lambda: self.backFn())
        back.place(x=12, y=360)

    def login(self, event=None):
        global uId
        global m_password
        login_email = self.e_input.get()
        login_mpass = self.pass_input.get()
        
        c.execute("SELECT rowid, * FROM user WHERE email = ?", (login_email,))
        info = c.fetchall()
        if login_email == '' or login_mpass == '':
            messagebox.showerror("Error", "Please fill up all required field.")
        elif len(info) >= 1:
            uId = str(info[0][0])
            m_password = login_mpass
            self.controller.show_frame("OptionsPage")
        else:
            messagebox.showerror("Error", "Your Email or Master Password is incorrect!Try Again.")

    def backFn(self):
        self.e_input.delete(0, "end")
        self.pass_input.delete(0, "end")
        self.controller.show_frame("FirstPage")


class RegisterPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        t1 = Label(self, text='Password Defender', font=('Roboto Slab Bold', 18), fg='#00B0F0', bg='#F2F2F2')
        t1.place(x=200, y=27)

        motto = Label(self, text='A better place to safe your information', font=('Roboto Slab Bold', 9), fg='#7C7C7C',bg='#F2F2F2')
        motto.place(x=198, y=55)

        rt1 = StringVar("")
        rt2 = StringVar("")
        rt3 = StringVar("")
        t1 = Label(self, text='Create Account', font=('Roboto Slab Bold', 15), fg='#00B0F0', bg='#F2F2F2')
        t1.place(x=220, y=80)

        logo = Button(self, image=s_logo, border=0)
        logo.place(x=150, y=27)

        email = Label(self, text='Email Address        :', font=('Roboto Slab Medium', 11), fg='#034961', bg='#F2F2F2')
        email.place(x=85, y=140)

        l1 = Label(self, image=line, border=0)
        l1.place(x=230, y=158)

        self.e_input = Entry(self, font=('Roboto Slab', 9), text=rt1, bg='#F2F2F2', border=0, width=35)
        self.e_input.place(x=234, y=143)

        pwd = Label(self, text='Master Password   :', font=('Roboto Slab Medium', 11), fg='#034961', bg='#F2F2F2')
        pwd.place(x=85, y=180)

        l2 = Label(self, image=line, border=0)
        l2.place(x=230, y=198)

        self.pass_input = Entry(self, show='*', font=('Roboto Slab', 9), text=rt2, bg='#F2F2F2', border=0, width=35)
        self.pass_input.place(x=234, y=183)

        cpwd = Label(self, text='Confirm Password :', font=('Roboto Slab Medium', 11), fg='#034961', bg='#F2F2F2')
        cpwd.place(x=85, y=220)

        l3 = Label(self, image=line, border=0)
        l3.place(x=230, y=238)

        self.cpass_input = Entry(self, show='*', font=('Roboto Slab', 9), text=rt3, bg='#F2F2F2', border=0, width=35)
        self.cpass_input.place(x=234, y=223)
        self.cpass_input.bind('<Return>',self.register)

        self.img_button2 = PhotoImage(file='images/RegBtn.png')
        b1 = Button(self, cursor='hand2', image=self.img_button2, border=0, command=lambda: self.register())
        b1.place(x=370, y=270)

        back = Button(self, cursor='hand2', image=back_Btn_pic, border=0, command=lambda: self.backFn())
        back.place(x=12, y=360)

    def register(self, event=None):
        email = self.e_input.get()
        mpass = self.pass_input.get()
        cpass = self.cpass_input.get()
        c.execute("SELECT rowid, * FROM user WHERE email = ?", (email,))
        info = c.fetchall()
        regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        comp = re.compile(regex)        
    
        if email == '' or mpass == '' or cpass == '':
            messagebox.showerror("Error", "Please fill up all required field.")
        elif len(info) >= 1:
            messagebox.showwarning("Warning!", "There is already exist an account with this email. Please login or use another email.")
        elif mpass != cpass:
            messagebox.showerror("Error", "Master Password & Confirm Password are not matched!")
        elif len(mpass)<12:
            messagebox.showerror("Error", "Master Password must have at least 12 characters.")
        elif re.search(comp, mpass) == None:
            messagebox.showerror("Error", "***Include Symbols, Uppercase, Numbers.")
        else:
            c.execute("INSERT INTO user VALUES (?,?)", (email, mpass))
            conn.commit()
            messagebox.showinfo("Success", "Successfully Registered!")
            self.e_input.delete(0, "end")
            self.pass_input.delete(0, "end")
            self.cpass_input.delete(0, "end")
            self.controller.show_frame("LoginPage")

    def backFn(self):
        self.e_input.delete(0, "end")
        self.pass_input.delete(0, "end")
        self.cpass_input.delete(0, "end")
        self.controller.show_frame("FirstPage")


class OptionsPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller


        sc1 = StringVar("")
        t1 = Label(self, text='Password Defender', font=('Roboto Slab Bold', 18), fg='#00B0F0', bg='#F2F2F2')
        t1.place(x=200, y=27)

        motto = Label(self, text='A better place to safe your information', font=('Roboto Slab Bold', 9), fg='#7C7C7C',bg='#F2F2F2')
        motto.place(x=198, y=55)

        sc1 = StringVar("")
        sc2 = StringVar("")
        t1 = Label(self, text='Choose an option', font=('Roboto Slab Bold', 15), fg='#00B0F0', bg='#F2F2F2')
        t1.place(x=217, y=80)

        logo = Button(self, image=s_logo, border=0)
        logo.place(x=150, y=27)

        self.op1 = PhotoImage(file='images/op1.png')
        o1 = Button(self, cursor='hand2', image=self.op1, border=0,command=lambda: controller.show_frame("GenPassPage"))
        o1.place(x=90, y=160)

        ot1 = Label(self, text='Generate\nPassword', font=('Roboto Slab Bold', 9), fg='#7C7C7C', bg='#F2F2F2')
        ot1.place(x=90, y=230)

        self.op2 = PhotoImage(file='images/op2.png')
        o2 = Button(self, cursor='hand2', image=self.op2, border=0, command=lambda: controller.show_frame("GenSavePage"))
        o2.place(x=200, y=160)

        ot2 = Label(self, text='Generate &\n Save Password', font=('Roboto Slab Bold', 9), fg='#7C7C7C', bg='#F2F2F2')
        ot2.place(x=186, y=230)

        self.op3 = PhotoImage(file='images/op3.png')
        o3 = Button(self, cursor='hand2', image=self.op3, border=0,command=lambda: controller.show_frame("GetPassPage"))
        o3.place(x=310, y=160)

        ot3 = Label(self, text='Get Your\nPassword', font=('Roboto Slab Bold', 9), fg='#7C7C7C', bg='#F2F2F2')
        ot3.place(x=312, y=230)

        self.op4 = PhotoImage(file='images/op4.png')
        o4 = Button(self, cursor='hand2', image=self.op4, border=0,command=lambda: controller.show_frame("UpdateFirstPage"))
        o4.place(x=420, y=160)

        ot4 = Label(self, text='Update Your\nPassword', font=('Roboto Slab Bold', 9), fg='#7C7C7C', bg='#F2F2F2')
        ot4.place(x=415, y=230)


        self.vault_btn = PhotoImage(file='images/vault.png')
        vault = Button(self, cursor='hand2', image=self.vault_btn, border=0)
        vault.place(x=515, y=355)


class GenPassPage(Frame):
    gt1 = ""

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.gt1 = StringVar("")

        t1 = Label(self, text='Password Defender', font=('Roboto Slab Bold', 18), fg='#00B0F0', bg='#F2F2F2')
        t1.place(x=200, y=27)

        motto = Label(self, text='A better place to safe your information', font=('Roboto Slab Bold', 9), fg='#7C7C7C',bg='#F2F2F2')
        motto.place(x=198, y=55)

        t1 = Label(self, text='Generate Your Password', font=('Roboto Slab Bold', 15), fg='#00B0F0', bg='#F2F2F2')
        t1.place(x=187, y=80)

        logo = Button(self, image=s_logo, border=0)
        logo.place(x=150, y=27)

        gen_pass = Label(self, text='Password :', font=('Roboto Slab Medium', 13), fg='#034961', bg='#F2F2F2')
        gen_pass.place(x=90, y=140)


        l1 = Label(self, image=line, border=0)
        l1.place(x=185, y=159)

        self.p_input = Entry(self, state='readonly', font=('Roboto Slab Bold', 11), text=self.gt1, bg='#F2F2F2',fg='#034961', border=0, width=27)
        self.p_input.place(x=187, y=140)

        length = Label(self, text='Length      :', font=('Roboto Slab Medium', 13), fg='#034961', bg='#F2F2F2')
        length.place(x=90, y=180)

        l2 = Label(self, image=line, border=0)
        l2.place(x=185, y=199)

        self.l_input = Entry(self, font=('Roboto Slab', 9), bg='#F2F2F2', border=0, width=35)
        self.l_input.place(x=187, y=184)
        self.l_input.bind('<Return>',self.gen)

        t4 = Label(self, text='Strength  :', font=('Roboto Slab Medium', 13), fg='#034961', bg='#F2F2F2')
        t4.place(x=90, y=225)

        self.c2 = Combobox(self, font=('Roboto Slab', 10), width=18)
        self.c2['values'] = ('Average', 'Strong', 'Very Strong')
        self.c2['state'] = 'readonly'
        self.c2.current(1)
        self.c2.place(x=187, y=230)

        self.img_button = PhotoImage(file='images/btn.png')
        b1 = Button(self, cursor='hand2', image=self.img_button, border=0, command=lambda: self.gen())
        b1.place(x=350, y=280)

        back = Button(self, cursor='hand2', image=back_Btn_pic, border=0, command=lambda: self.backFn(controller))
        back.place(x=12, y=360)

    def gen(self,event=None):
        self.gt1.set("")
        passw = ""
        length = self.l_input.get()
        average = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        strong = '0123456789@#$%&*' + average
        very_strong = "~!_-+=`|(){}[]:;'<>,.?/" + strong
        if self.l_input.get() == "":
            messagebox.showerror("Error", "Please fill up Length it's required.")
        elif self.c2.get() == 'Average':
            for i in range(0,int(length)):
                passw = passw + random.choice(average)
            self.gt1.set(passw)

        elif self.c2.get() == 'Strong':
            for i in range(0, int(length)):
                passw = passw + random.choice(strong)
            self.gt1.set(passw)

        elif self.c2.get() == 'Very Strong':
            for i in range(0, int(length)):
                passw = passw + random.choice(very_strong)
            self.gt1.set(passw)
        if passw!="":
            pyperclip.copy(passw)
            messagebox.showinfo("Success", "Password Copied to clipboard!")

    def backFn(self, controller):
        self.gt1.set('')
        self.l_input.delete(0, "end")
        controller.show_frame("OptionsPage")


class GenPassPage1(Frame):
    gt1 = ""

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.gt1 = StringVar("")

        t1 = Label(self, text='Password Defender', font=('Roboto Slab Bold', 18), fg='#00B0F0', bg='#F2F2F2')
        t1.place(x=200, y=27)

        motto = Label(self, text='A better place to safe your information', font=('Roboto Slab Bold', 9), fg='#7C7C7C',bg='#F2F2F2')
        motto.place(x=198, y=55)

        t1 = Label(self, text='Generate Your Password', font=('Roboto Slab Bold', 15), fg='#00B0F0', bg='#F2F2F2')
        t1.place(x=187, y=80)

        logo = Button(self, image=s_logo, border=0)
        logo.place(x=150, y=27)

        gen_pass = Label(self, text='Password :', font=('Roboto Slab Medium', 13), fg='#034961', bg='#F2F2F2')
        gen_pass.place(x=90, y=140)

        l1 = Label(self, image=line, border=0)
        l1.place(x=185, y=159)

        self.p_input = Entry(self, state='readonly', font=('Roboto Slab Bold', 11), text=self.gt1, bg='#F2F2F2', fg='#034961', border=0, width=27)
        self.p_input.place(x=187, y=140)

        length = Label(self, text='Length      :', font=('Roboto Slab Medium', 13), fg='#034961', bg='#F2F2F2')
        length.place(x=90, y=180)

        l2 = Label(self, image=line, border=0)
        l2.place(x=185, y=199)

        self.l_input = Entry(self, font=('Roboto Slab', 9), bg='#F2F2F2', border=0, width=35)
        self.l_input.place(x=187, y=184)
        self.l_input.bind('<Return>',self.gen)


        t4 = Label(self, text='Strength  :', font=('Roboto Slab Medium', 13), fg='#034961', bg='#F2F2F2')
        t4.place(x=90, y=225)

        self.c2 = Combobox(self, font=('Roboto Slab', 10), width=18)
        self.c2['values'] = ('Average', 'Strong', 'Very Strong')
        self.c2['state'] = 'readonly'
        self.c2.current(1)
        self.c2.place(x=187, y=230)


        self.img_button = PhotoImage(file='images/btn.png')
        b1 = Button(self, cursor='hand2', image=self.img_button, border=0, command=lambda: self.gen())
        b1.place(x=350, y=280)

        back = Button(self, cursor='hand2', image=back_Btn_pic, border=0, command=lambda: self.backFn(controller))
        back.place(x=12, y=360)

    def gen(self,event=None):
        self.gt1.set("")
        passw = ""
        length = self.l_input.get()
        average = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        strong = '0123456789@#$%&*' + average
        very_strong = "~!_-+=`|(){}[]:;'<>,.?/" + strong
        if self.l_input.get() == "":
            messagebox.showerror("Error", "Please fill up Length it's required.")
        elif self.c2.get() == 'Average':
            for i in range(0,int(length)):
                passw = passw + random.choice(average)
            self.gt1.set(passw)

        elif self.c2.get() == 'Strong':
            for i in range(0, int(length)):
                passw = passw + random.choice(strong)
            self.gt1.set(passw)

        elif self.c2.get() == 'Very Strong':
            for i in range(0, int(length)):
                passw = passw + random.choice(very_strong)
            self.gt1.set(passw)
        if passw !="":
            pyperclip.copy(passw)
            messagebox.askokcancel("Question", "Password Copied to clipboard!\nDo you want to save this password?")
            self.gt1.set('')
            self.l_input.delete(0, "end")
            self.controller.show_frame("GenSavePage")
   

    def backFn(self, controller):
        self.gt1.set('')
        self.l_input.delete(0, "end")
        controller.show_frame("GenSavePage")



class GenSavePage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        t1 = Label(self, text='Password Defender', font=('Roboto Slab Bold', 18), fg='#00B0F0', bg='#F2F2F2')
        t1.place(x=200, y=27)

        motto = Label(self, text='A better place to safe your information', font=('Roboto Slab Bold', 9), fg='#7C7C7C', bg='#F2F2F2')
        motto.place(x=198, y=55)

        lt1 = StringVar("")
        lt2 = StringVar("")
        lt3 = StringVar("")
        t1 = Label(self, text='Generate & Save Password', font=('Roboto Slab Bold', 15), fg='#00B0F0', bg='#F2F2F2')
        t1.place(x=175, y=80)

        logo = Button(self, image=s_logo, border=0)
        logo.place(x=150, y=27)

        uname = Label(self, text='Username :', font=('Roboto Slab Medium', 13), fg='#034961', bg='#F2F2F2')
        uname.place(x=100, y=125)

        l1 = Label(self, image=line, border=0)
        l1.place(x=195, y=143)

        self.u_input = Entry(self, font=('Roboto Slab', 9), text=lt1, bg='#F2F2F2', border=0, width=35)
        self.u_input.place(x=199, y=128)

        wsite = Label(self, text='Website     :', font=('Roboto Slab Medium', 13), fg='#034961', bg='#F2F2F2')
        wsite.place(x=100, y=168)

        l2 = Label(self, image=line, border=0)
        l2.place(x=194, y=185)

        self.w_input = Entry(self, font=('Roboto Slab', 9), text=lt2, bg='#F2F2F2', border=0, width=35)
        self.w_input.place(x=197, y=170)

        pwd = Label(self, text='Password :', font=('Roboto Slab Medium', 13), fg='#034961', bg='#F2F2F2')
        pwd.place(x=100, y=211)

        l3 = Label(self, image=line, border=0)
        l3.place(x=192, y=229)

        self.p_input = Entry(self,show="*", font=('Roboto Slab', 9), text=lt3, bg='#F2F2F2', border=0, width=35)
        self.p_input.place(x=197, y=214)
        self.p_input.bind('<Return>',self.save)

        note = Label(self,text='N.B [You can make your own password here or you can use generated password by clicking on',font=('Roboto Slab', 8), fg='#7C7C7C', bg='#F2F2F2')
        note.place(x=40, y=250)
        note1 = Label(self,text='"Generate" Button. To create password please follow: At least 8 characters, Must include lower',font=('Roboto Slab', 8), fg='#7C7C7C', bg='#F2F2F2')
        note1.place(x=40, y=269)
        note2 = Label(self, text='case, uppercase & digit. For more security, you can add symbols]',font=('Roboto Slab', 8), fg='#7C7C7C', bg='#F2F2F2')
        note2.place(x=95, y=286)

        self.img_button2 = PhotoImage(file='images/saveBtn.png')
        b1 = Button(self, cursor='hand2', image=self.img_button2, border=0, command=lambda: self.save())
        b1.place(x=390, y=315)

        self.gen_btn = PhotoImage(file='images/genBtn.png')
        gen = Button(self, cursor='hand2', image=self.gen_btn, border=0,
                     command=lambda: controller.show_frame("GenPassPage1"))
        gen.place(x=450, y=195)

        back = Button(self, cursor='hand2', image=back_Btn_pic, border=0,
                      command=lambda: controller.show_frame("OptionsPage"))
        back.place(x=12, y=360)

    def save(self, event=None):
        p = self.p_input.get()
        user = self.u_input.get()
        website = self.w_input.get()
        c.execute("SELECT * FROM acc_info WHERE website = ? AND uid = ?", (website,uId))
        infos = c.fetchall()
        if p == "" or user == "" or website == "":
            messagebox.showerror("Error", "Please fill up all required field.")
        elif len(infos) >= 1:
            messagebox.showwarning("Warning","This Website is already exists, Please try to give a different name like: Website-2!")
        else:
            c.execute("INSERT INTO acc_info VALUES (?,?,?,?)", (user, website, p, uId))
            conn.commit()
            messagebox.showinfo("Success", "Successfully Saved for {}".format(website))
            self.p_input.delete(0, "end")
            self.u_input.delete(0, "end")
            self.w_input.delete(0, "end")
            self.controller.show_frame("OptionsPage")


class GetPassPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        t1 = Label(self, text='Password Defender', font=('Roboto Slab Bold', 18), fg='#00B0F0', bg='#F2F2F2')
        t1.place(x=200, y=27)

        motto = Label(self, text='A better place to safe your information', font=('Roboto Slab Bold', 9), fg='#7C7C7C',bg='#F2F2F2')
        motto.place(x=198, y=55)

        lt1 = StringVar("")
        lt2 = StringVar("")
        t1 = Label(self, text='Get Your Password', font=('Roboto Slab Bold', 15), fg='#00B0F0', bg='#F2F2F2')
        t1.place(x=205, y=80)

        logo = Button(self, image=s_logo, border=0)
        logo.place(x=150, y=27)

        website = Label(self, text='Website :', font=('Roboto Slab Medium', 13), fg='#034961', bg='#F2F2F2')
        website.place(x=130, y=185)

        l1 = Label(self, image=line, border=0)
        l1.place(x=207, y=203)

        self.w_input = Entry(self, font=('Roboto Slab', 9), text=lt1, bg='#F2F2F2', border=0, width=35)
        self.w_input.place(x=212, y=187)
        self.w_input.bind('<Return>',self.get_pass)

        self.getBtn = PhotoImage(file='images/getBtn.png')
        g1 = Button(self, cursor='hand2', image=self.getBtn, border=0, command=lambda: self.get_pass())
        g1.place(x=370, y=270)

        back = Button(self, cursor='hand2', image=back_Btn_pic, border=0, command=lambda: self.backFn(controller))
        back.place(x=12, y=360)

    def get_pass(self, event=None):
        website = self.w_input.get()
        c.execute("SELECT * FROM acc_info WHERE website = ? AND uid=?", (website, uId))
        infos = c.fetchall()
        if website == "":
            messagebox.showerror("Error", "Please fill up all required field.")
        elif len(infos) >= 1:
            pyperclip.copy(infos[0][2])
            messagebox.showinfo("Success", "Password Copied to clipboard!")
        else:
            messagebox.showerror("Error", "This website is not exist in your account.")

    def backFn(self, controller):
        self.w_input.delete(0, "end")
        controller.show_frame("OptionsPage")


class UpdateFirstPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        t1 = Label(self, text='Password Defender', font=('Roboto Slab Bold', 18), fg='#00B0F0', bg='#F2F2F2')
        t1.place(x=200, y=27)

        motto = Label(self, text='A better place to safe your information', font=('Roboto Slab Bold', 9), fg='#7C7C7C', bg='#F2F2F2')
        motto.place(x=198, y=55)

        lt1 = StringVar("")
        t1 = Label(self, text='Update Password', font=('Roboto Slab Bold', 15), fg='#00B0F0', bg='#F2F2F2')
        t1.place(x=215, y=80)

        logo = Button(self, image=s_logo, border=0)
        logo.place(x=150, y=27)

        website = Label(self, text='Website :', font=('Roboto Slab Medium', 13), fg='#034961', bg='#F2F2F2')
        website.place(x=130, y=185)

        l1 = Label(self, image=line, border=0)
        l1.place(x=207, y=203)

        self.w_input = Entry(self, font=('Roboto Slab', 9), text=lt1, bg='#F2F2F2', border=0, width=35)
        self.w_input.place(x=212, y=187)
        self.w_input.bind('<Return>',self.verifyPage)

        self.nextBtn = PhotoImage(file='images/NextBtn.png')
        n1 = Button(self, cursor='hand2', image=self.nextBtn, border=0, command=lambda: self.verifyPage(controller))
        n1.place(x=370, y=270)

        back = Button(self, cursor='hand2', image=back_Btn_pic, border=0, command=lambda: self.back(controller))
        back.place(x=12, y=360)


    def verifyPage(self,event=None):
        global update_website
        website = self.w_input.get()
        c.execute("SELECT * FROM acc_info WHERE website = ? AND uid = ?", (website, uId))
        infos = c.fetchall()
        if website == "":
            messagebox.showerror("Error", "Please fill up all required field.")
        elif len(infos) >= 1:
            update_website = website
            self.controller.show_frame("VerifyPage")
        else:
            messagebox.showerror("Error", "Website not found.")

    def back(self,controller):
        controller.show_frame("OptionsPage")




class VerifyPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        t1 = Label(self, text='Password Defender', font=('Roboto Slab Bold', 18), fg='#00B0F0', bg='#F2F2F2')
        t1.place(x=200, y=27)

        motto = Label(self, text='A better place to safe your information', font=('Roboto Slab Bold', 9), fg='#7C7C7C',bg='#F2F2F2')
        motto.place(x=198, y=55)

        lt1 = StringVar("")
        lt2 = StringVar("")
        t1 = Label(self, text='Verify Master Password', font=('Roboto Slab Bold', 15), fg='#00B0F0', bg='#F2F2F2')
        t1.place(x=190, y=80)

        instruction = Label(self, text='*Type Your Master Password', font=('Roboto Slab Bold', 9), fg='#7F7D79',
                            bg='#F2F2F2')
        instruction.place(x=220, y=110)

        logo = Button(self, image=s_logo, border=0)
        logo.place(x=150, y=27)


        eu_input = Entry(self, font=('Roboto Slab', 9), text=lt1, bg='#F2F2F2', border=0, width=35)
        eu_input.place(x=210, y=167)

        Mpwd = Label(self, text='Master Password :', font=('Roboto Slab Medium', 13), fg='#034961', bg='#F2F2F2')
        Mpwd.place(x=100, y=190)

        l2 = Label(self, image=line, border=0)
        l2.place(x=253, y=207)

        self.pass_input = Entry(self, show="*", font=('Roboto Slab', 9), text=lt2, bg='#F2F2F2', border=0, width=35)
        self.pass_input.place(x=260, y=190)
        self.pass_input.bind("<Return>",self.update_last_page)

        self.next_btn = PhotoImage(file='images/NextBtn.png')
        Next = Button(self, cursor='hand2', image=self.next_btn, border=0,command=lambda: self.update_last_page())
        Next.place(x=390, y=270)

        back = Button(self, cursor='hand2', image=back_Btn_pic, border=0,command=lambda: controller.show_frame("UpdateFirstPage"))
        back.place(x=12, y=360)

    def update_last_page(self, event=None):
        m_pass = self.pass_input.get()
        if m_pass=="":
            messagebox.showerror("Error", "Please fill up required field.")
        if m_password == m_pass:
            self.controller.show_frame("UpdateLastPage")
        else:
            messagebox.showerror("Error", "Master Password not matched. Try Again!")


class UpdateLastPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        t1 = Label(self, text='Password Defender', font=('Roboto Slab Bold', 18), fg='#00B0F0', bg='#F2F2F2')
        t1.place(x=200, y=27)

        motto = Label(self, text='A better place to safe your information', font=('Roboto Slab Bold', 9), fg='#7C7C7C',bg='#F2F2F2')
        motto.place(x=198, y=55)

        lt1 = StringVar("")
        lt2 = StringVar("")
        t1 = Label(self, text='Update Password', font=('Roboto Slab Bold', 15), fg='#00B0F0', bg='#F2F2F2')
        t1.place(x=215, y=80)

        instruction = Label(self, text='*Type Here Your New Username & Password', font=('Roboto Slab Bold', 9),
                            fg='#7F7D79', bg='#F2F2F2')
        instruction.place(x=165, y=110)

        logo = Button(self, image=s_logo, border=0)
        logo.place(x=150, y=27)

        eu = Label(self, text='Username :', font=('Roboto Slab Medium', 13), fg='#034961', bg='#F2F2F2')
        eu.place(x=110, y=165)


        l1 = Label(self, image=line, border=0)
        l1.place(x=206, y=182)

        self.eu_input = Entry(self, font=('Roboto Slab', 9), text=lt1, bg='#F2F2F2', border=0, width=35)
        self.eu_input.place(x=210, y=167)

        psd = Label(self, text='Password  :', font=('Roboto Slab Medium', 13), fg='#034961', bg='#F2F2F2')
        psd.place(x=110, y=208)

        l2 = Label(self, image=line, border=0)
        l2.place(x=205, y=226)

        self.p_input = Entry(self,show="*", font=('Roboto Slab', 9), text=lt2, bg='#F2F2F2', border=0, width=35)
        self.p_input.place(x=209, y=211)
        self.p_input.bind("<Return>",self.updating)

        self.saveBtn = PhotoImage(file='images/SaveBtn.png')
        s1 = Button(self, cursor='hand2', image=self.saveBtn, border=0, command=lambda: self.updating())
        s1.place(x=370, y=270)

        back = Button(self, cursor='hand2', image=back_Btn_pic, border=0, command=lambda: controller.show_frame("UpdateFirstPage"))
        back.place(x=12, y=360)


    def updating(self,event=None):
        p = self.p_input.get()
        user = self.eu_input.get()
        website = update_website
        c.execute("DELETE from acc_info where website = ? AND uid = ?",(website,uId))
        if p == "" or user == "":
            messagebox.showerror("Error", "Please fill up all required field.")
        else:
            c.execute("INSERT INTO acc_info VALUES (?,?,?,?)", (user, website, p, uId))
            conn.commit()
            messagebox.showinfo("Success", "Successfully Updated for {}".format(website))
            self.controller.show_frame("OptionsPage")



if __name__ == "__main__":
    app = PasswordDefender()
    app.mainloop()