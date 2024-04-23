from tkinter import *
from PIL import Image, ImageTk, ImageDraw
from datetime import *
import time
from math import *
import pymysql
from tkinter import messagebox, ttk


class clock:
    def __init__(self, root):
        self.root = root
        self.root.title("Clock")
        self.root.geometry("1350x700+0+0")
        # self.root.config(bg="#398AB9")
        self.bg = ImageTk.PhotoImage(file=r"images/pic1.jpg")
        lb1 = Label(self.root, image=self.bg)
        lb1.place(x=0, y=0, relwidth=1, relheight=1)

        frame1 = Frame(self.root, bg="#506D84")
        frame1.place(x=650, y=150, width=360, height=460)

        pro = Image.open(r"images/profile.png")
        pro = pro.resize((140, 140), Image.ANTIALIAS)
        self.img1 = ImageTk.PhotoImage(pro)
        lbimg = Label(image=self.img1, bg="black", borderwidth=0)
        lbimg.place(x=770, y=170, width=100, height=100)

        get_str = Label(frame1, text="LOGIN HERE", font=(
            "times new roman", 20, "bold"), fg="white", bg="#506D84")
        get_str.place(x=87, y=125)

        u_name = Label(frame1, text="Email", font=(
            "times new roman", 20, "bold"), fg="white", bg="#506D84")
        u_name.place(x=50, y=190)
        self.txtu_name = ttk.Entry(
            frame1, font=("times new roman", 15, "bold"))
        self.txtu_name.place(x=20, y=230, width=280)

        pasw = Label(frame1, text="Password", font=(
            "times new roman", 20, "bold"), fg="white", bg="#506D84")
        pasw.place(x=50, y=280)
        self.txtpasw = ttk.Entry(frame1, font=(
            "times new roman", 15, "bold"), show="*")
        self.txtpasw.place(x=20, y=320, width=280)

        #====Icon Image=====#
        userimg = Image.open(r"images/profile.png")
        userimg = userimg.resize((53, 53), Image.ANTIALIAS)
        self.img2 = ImageTk.PhotoImage(userimg)
        lbimg1 = Label(image=self.img2, bg="black", borderwidth=0)
        lbimg1.place(x=660, y=338, width=40, height=40)

        pasimg = Image.open(r"images/pass.png")
        pasimg = pasimg.resize((43, 43), Image.ANTIALIAS)
        self.img3 = ImageTk.PhotoImage(pasimg)
        lbimg2 = Label(image=self.img3, bg="black", borderwidth=0)
        lbimg2.place(x=660, y=428, width=40, height=40)

        # Button
        logbtn = Button(frame1, text="Login", cursor="hand2",command=self.login ,font=("times new roman", 15, "bold"),
                        bd=3, relief=RIDGE, fg="white", bg="red", activeforeground="white", activebackground="red")
        logbtn.place(x=205, y=387, width=120, height=35)

        signbtn = Button(frame1, text="New User?Register Here:)", cursor="hand2", command=self.regwin, font=(
            "times new roman", 10, "bold"), borderwidth=0, fg="white", bg="#506D84")
        signbtn.place(x=20, y=350, width=150)

        forgbtn = Button(frame1, text="Forgot Password?",command=self.forgot, cursor="hand2", font=(
            "times new roman", 10, "bold"), borderwidth=0, fg="white", bg="#506D84")
        forgbtn.place(x=217, y=422, width=100)

        self.lb = Label(self.root, bg="#008080", bd=0)
        self.lb.place(x=300, y=150, width=350, height=460)
        self.work()

    def regwin(self):
        self.root.destroy()
        import register

    def clear(self):
        self.txtu_name.delete(0, END)
        self.txtpasw.delete(0, END)

    def login(self):
        if self.txtu_name.get() == "" or self.txtpasw.get() == "":
            messagebox.showerror("Error", "All Fields are Required!!",parent=self.root)
        else:
            try:
                con = pymysql.connect(
                    host="localhost", user="root", password="", database='users')
                cur = con.cursor()
                cur.execute("select * from customers where email=%s and pwd=%s",
                            (self.txtu_name.get(), self.txtpasw.get()))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Invalid Email & Password", parent=self.root)
                    self.clear()
                else:
                    messagebox.showinfo("Success", "Welcome", parent=self.root)
                    self.root.destroy()
                    import encode_decode
                    con.close()
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Error Due to: {str(e)}", parent=self.root)
                self.clear()

    def clockimg(self, h, m, s,):
        clock = Image.new("RGB", (400, 400), (0, 128, 128))
        draw = ImageDraw.Draw(clock)
        bg = Image.open("images/color.png")
        bg = bg.resize((300, 300), Image.ANTIALIAS)
        clock.paste(bg, (50, 50))
        # To rotate the clock

        # line of hour
        origin = 200, 200
        draw.line((origin, 200+50*sin(radians(h)), 200-50 *
                  cos(radians(h))), fill="black", width=4)
        # line of min
        draw.line((origin, 200+80*sin(radians(m)), 200-80 *
                  cos(radians(m))), fill="black", width=3)
        # line of sec
        draw.line((origin, 200+100*sin(radians(s)), 200 -
                  100*cos(radians(s))), fill="black", width=2)
        draw.ellipse((195, 195, 210, 210), fill="#072227")
        clock.save("images/clocknew.png")

    def work(self):
        hr = datetime.now().time().hour
        mi = datetime.now().time().minute
        sec = datetime.now().time().second
        h = (hr/12)*360
        m = (mi/60)*360
        s = (sec/60)*360
        self.clockimg(h, m, s)
        self.img = ImageTk.PhotoImage(file="images/clocknew.png")
        self.lb.config(image=self.img)
        self.lb.after(200, self.work)


    def reset(self):
        if self.combo.get()=="Select":
            messagebox.showerror("Error","Select the security question",parent=self.root2)
        elif self.ans.get()=="":
            messagebox.showerror("Error","Please enter the answer",parent=self.root2)
        elif self.new.get()=="":
            messagebox.showerror("Error","Please enter the new password",parent=self.root2)
        else:
            try:
                con = pymysql.connect(host="localhost", user="root", password="", database="users")
                cur = con.cursor()
                cur.execute("select * from customers where email=%s and question=%s answer=%s",self.txtu_name.get(),self.combo.get(),self.ans.get())
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error","Please enter correct Answer",parent=self.root2)
                else:
                    cur.execute("update customers set password=%s where email=%s",self.new.get(),self.txtu_name.get())
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success","Your password has been reset,please login with new password",parent=self.root2)
                    self.root2.destroy()
                    self.reset_clear()
            except Exception as e:
                messagebox.showerror("Error",f"Error Due to {str(e)}",parent=self.root2)

    def reset_clear(self):
        self.combo.current(0)
        self.txtpasw("")
        self.ans("")
        self.txtu_name("")
        self.new("")


    def forgot(self):
        if self.txtu_name.get()=="":
            messagebox.showerror("Error","Please Enter the email address to reset your password",parent=self.root)
        else:
            con = pymysql.connect(host="localhost", user="root", password="", database="users")
            cur = con.cursor()
            cur.execute("select * from customers where email=%s",self.txtu_name.get())
            row = cur.fetchone()
            if row == None:
                messagebox.showerror("Error", "Please enter the valid email", parent=self.root)
            else:
                con.close()
                self.root2 = Toplevel()
                self.root2.title("Forgot Password")
                self.root2.geometry("340x450+610+170")

                lb2 = Label(self.root2,text="Forgot Password",font=("times new roman",12,"bold"),bg="white",fg="red")
                lb2.place(x=0,y=10,relwidth=1)

                ques = Label(self.root2, text=" Select Security Questions", font=("times new roman", 15, "bold"), bg="white", fg="black")
                ques.place(x=50, y=80)
                self.combo = ttk.Combobox(self.root2,font=("times new roman",15,"bold"),state="readonly")
                self.combo["values"]=("Select","Your Birth Place","Your Pet Name","Your Favorite Hero Name")
                self.combo.place(x=50,y=110,width=250)
                self.combo.current(0)

                sec_ans = Label(self.root2, text="Security Answer", font=("times new roman", 15, "bold"), bg="white", fg="black")
                sec_ans.place(x=50, y=150)
                self.ans = ttk.Entry(self.root2, font=("times new roman", 15))
                self.ans.place(x=50, y=180, width=250)

                new_pass = Label(self.root2, text="New Password", font=("times new roman", 15, "bold"), bg="white", fg="black")
                new_pass.place(x=50, y=220)
                self.new = ttk.Entry(self.root2, font=("times new roman", 15))
                self.new.place(x=50, y=250, width=250)

                btn_forgot = Button(self.root2,text="Reset",command=self.reset,cursor="hand2",font=("times new roman",15,"bold"),fg="white",bg="green")
                btn_forgot.place(x=80,y=290,width=180)


root = Tk()
obj = clock(root)
root.mainloop()
