from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox,ttk
import pymysql


class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration Form")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="white")
        # Background image
        self.bg = ImageTk.PhotoImage(file="images/pic7.jpg")
        bglb = Label(self.root, image=self.bg)
        bglb.place(x=0, y=0, relwidth=1, relheight=1)

        # left image
        self.left = ImageTk.PhotoImage(file="images/pic4.jpg")
        left = Label(self.root, image=self.left)
        left.place(x=100, y=100, width=400, height=470)


        frame2 = Frame(self.root, bg="white")
        frame2.place(x=500, y=100, width=680, height=470)
        title = Label(frame2, text="REGISTER HERE", font=("times new roman", 25, "bold", "underline"), bg="white", fg="cyan")
        title.place(x=20, y=10)

         # Feilds
        fname = Label(frame2, text="First Name", font=("times new roman", 15, "bold"), bg="white", fg="black").place(x=50, y=100)
        self.first = ttk.Entry(frame2, font=("times new roman", 15))
        self.first.place(x=50, y=130, width=250)

        lname = Label(frame2, text="Last Name", font=("times new roman", 15, "bold"), bg="white", fg="black").place(x=370, y=100)
        self.last = ttk.Entry(frame2, font=("times new roman", 15))
        self.last.place(x=370, y=130, width=250)

        contact = Label(frame2, text="Phone Number", font=("times new roman", 15, "bold"), bg="white", fg="black").place(x=50, y=170)
        self.call = ttk.Entry(frame2, font=("times new roman", 15))
        self.call.place(x=50, y=200, width=250)

        email = Label(frame2, text="Email", font=("times new roman", 15, "bold"), bg="white", fg="black").place(x=370, y=170)
        self.mail = ttk.Entry(frame2, font=("times new roman", 15))
        self.mail.place(x=370, y=200, width=250)

        pwd = Label(frame2, text="Password", font=("times new roman",15, "bold"), bg="white", fg="black").place(x=50, y=240)
        self.txt_pwd = ttk.Entry(frame2, font=("times new roman", 15),show="*")
        self.txt_pwd.place(x=50, y=270, width=250)

        confpwd = Label(frame2, text="Confirm Password", font=("times new roman", 15, "bold"), bg="white", fg="black").place(x=370, y=240)
        self.txt_confpwd = ttk.Entry(frame2, font=("times new roman", 15),show="*")
        self.txt_confpwd.place(x=370, y=270, width=250)

        ques = Label(frame2, text=" Select Security Questions", font=("times new roman", 15, "bold"), bg="white", fg="black").place(x=45, y=310)
        self.combo = ttk.Combobox(frame2,font=("times new roman",15,"bold"),state="readonly")
        self.combo["values"]=("Select","Your Birth Place","Your Pet Name","Your Favorite Hero Name")
        self.combo.place(x=50,y=340,width=250)
        self.combo.current(0)

        sec_ans = Label(frame2, text="Security Answer", font=("times new roman", 15, "bold"), bg="white", fg="black").place(x=370, y=310)
        self.ans = ttk.Entry(frame2, font=("times new roman", 15))
        self.ans.place(x=370, y=340, width=250)

        ##### Buttons #####

        self.var_chek = IntVar()
        chek = Checkbutton(frame2, text="I Agree The Terms & Conditions", variable=self.var_chek,  onvalue=1, offvalue=0, font=("times new roman", 12), bg='white').place(x=50, y=370)

        regisimg = Image.open(r"images/reg.jpg")
        regisimg = regisimg.resize((160,45),Image.ANTIALIAS)
        self.imgreg = ImageTk.PhotoImage(regisimg)
        btnsignup = Button(frame2, image=self.imgreg,borderwidth=0, command=self.signup,cursor="hand2", font=("times new roman", 15,"bold"))
        btnsignup.place(x=480, y=400, width=150)

        logimg = Image.open(r"images/log.jpg")
        logimg = logimg.resize((160,56),Image.ANTIALIAS)
        self.imglog = ImageTk.PhotoImage(logimg)
        btnlogin = Button(self.root,image=self.imglog, cursor="hand2",command=self.logwin, font=("times new roman", 15,"bold"),borderwidth=0)
        btnlogin.place(x=225, y=480, width=150, height=50)

    def clear(self):
        self.first.delete(0, END)
        self.last.delete(0, END)
        self.mail.delete(0, END)
        self.txt_pwd.delete(0, END)
        self.txt_confpwd.delete(0, END)
        self.call.delete(0, END)
        self.ans.delete(0,END)

    def signup(self):
        if self.first.get() == "" or self.last.get() == "" or self.mail.get() == "" or self.call.get() == "" or self.txt_pwd.get() == "" or self.txt_confpwd.get() == "" or self.ans.get()== "" or self.combo.get()=="Select":
            messagebox.showerror("Error", "All Fields are required", parent=self.root)

        elif self.txt_pwd.get() != self.txt_confpwd.get():
            messagebox.showerror("Error", "Password and Confirm Password Should Match!!", parent=self.root)

        elif self.var_chek.get() == 0:
            messagebox.showerror("Error", "Please Agree out terms & conditions", parent=self.root)

        else:
            try:
                con = pymysql.connect(host="localhost", user="root", password="", database="users")
                cur = con.cursor()
                cur.execute("select * from customers where email=%s",
                self.mail.get())
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "User already exists!!Please use another name:)", parent=self.root)
                else:
                    cur.execute("insert into customers (fname,lname,email,contact,pwd,question,answer) values(%s,%s,%s,%s,%s,%s,%s)",
                                (
                                    self.first.get(), self.last.get(),self.mail.get(),
                                    self.call.get(), self.txt_pwd.get(),self.combo.get(),self.ans.get()
                                ))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success", "Registered Successfully :) Now, click on LOGIN button to log into your account!!", parent=self.root)
                    self.clear()
            except Exception as e:
                messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)

    def logwin(self):
        self.root.destroy()
        import login


root = Tk()
obj = Register(root)
root.mainloop()
