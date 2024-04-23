from crypt import methods
from locale import resetlocale
from sre_constants import SUCCESS
from xml.dom.pulldom import default_bufsize
import mysql.connector
from flask import Flask, render_template, request, redirect, session

import os
import smtplib
import random

from sympy import re

app = Flask(__name__)
app.secret_key = os.urandom(24)

# database connection
mydb = mysql.connector.connect(
    host="localhost", user="root", password="", database="login_data")
mycursor = mydb.cursor()
#########################


@app.route("/")
def login():
    return render_template('login.html')


@app.route("/home")
def home():
    if 'id' in session:
        return render_template('home.html')
    else:
        return redirect('/')


@app.route("/", methods=['POST'])
def logindata():
    error = None
    #success = None

    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        mycursor.execute(
            "SELECT * FROM `login_user` WHERE `Email` LIKE '{}' AND `Password` LIKE '{}'".format(email, password))
        login_user = mycursor.fetchall()

        if len(login_user) > 0:
            session['id'] = login_user[0][0]
            logindata.login_user = login_user[0][2]
            return redirect('/home')
        else:
            error = "Incorrect username/password!"

    return render_template('login.html', error=error)


@app.route("/signup")
def register():
    return render_template('signup.html')


@app.route("/signup", methods=['POST'])
def add_user():
    error = None
    success = None
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')
    mobile = request.form.get('con_num')

    if name == "":
        error = "Please, Enter your name!!"
    elif email == "":
        error = "Please,Enter your email!!"
    elif password == "":
        error = "Please, Enter the password!!"
    else:
        mycursor.execute("INSERT INTO `login_user` (`Name`,`Email`,`Contact number`,`Password`) VALUES ('{}','{}','{}','{}')".format(
            name, email, mobile, password))
        mydb.commit()
        success = "You are registered successfully."

    return render_template('signup.html', error=error, msg=success)


@app.route('/logout')
def logout():
    session.pop('id')
    return redirect('/')


@app.route('/contact')
def con():
    if 'id' in session:
        return render_template('contact.html')
    else:
        return redirect('/')


@app.route('/forgot')
def forgotpwd():
    if 'login' in session:
        return redirect('/')
    else:
        return render_template('forgot.html')


@app.route('/forgot', methods=['POST'])
def reset():

    error = None
    success = None
    reset.email_id = request.form.get('fgemail')
    email_id = [reset.email_id]

    if email_id == "":
        error = "Please, Enter your email for OTP verification to reset your password"
    else:
        mycursor.execute(
            "SELECT * FROM `login_user` WHERE `Email` = %s", email_id)
        row = mycursor.fetchone()
        if row == None:
            error = "Please,Enter the valid email address"
        else:
            reset.otp = ''.join([str(random.randint(0, 9))for i in range(4)])
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('beasthack2518@gmail.com',
                         password='prmqniatfnsgzvbm')
            subject = "Verify OTP"
            body = "Hello, This is your OTP to verify your account for to reset your password-" + \
                str(reset.otp)
            mess = "subject:{}\n\n{}".format(subject, body)
            server.sendmail('beasthack2518@gmail.com', email_id, mess)
            server.quit()
            success = "Please, check your mail to verify the otp."

    return render_template('forgot.html', error=error, msg=success)


@app.route('/reset', methods=['POST'])
def respwd():
    error1 = None
    success1 = None
    num = reset.otp
    email_id = reset.email_id
    mails = [email_id]
    newpwd = request.form.get('newpass')
    np = [newpwd]
    verify = request.form.get('verify')
    if verify == "":
        error1 = "Please, enter the OTP first which is sent on your entered email."
    elif verify != num:
        error1 = "Please, enter the valid OTP."
    elif newpwd == "":
        error1 = "Please, enter the new password to reset."
    else:
        mycursor.execute(
            "SELECT * FROM `login_user` WHERE `Email` = %s", mails)
        mycursor.fetchone()
        mycursor.execute(
            "UPDATE `login_user` SET `Password` = %s WHERE `Email`= %s", (np[0], mails[0]))
        mydb.commit()
        success1 = "Your password has sucessfully reset."

    return render_template('forgot.html', error1=error1, msg1=success1)


@app.route('/profile')
def profile():
    try:
        mail1 = logindata.login_user
        mail2 = mail1
        mail3 = [mail2]
        mycursor.execute("SELECT * FROM login_user WHERE Email = %s", mail3)
        data = mycursor.fetchall()
        return render_template('profile.html', value=data)
    except:
        return redirect('/')


@app.route("/report")
def report():
    return render_template('report.html')


@app.route('/report', methods=['POST'])
def report_case():
    try:
        error = None
        success = None
        cudefaultMail = logindata.login_user
        mycursor.execute(
            "select * from login_user where Email = %s", [cudefaultMail])
        dataExtract = mycursor.fetchall()
        cuaadharNumber = dataExtract[0][7]
        cudefaultStatus = "Pending"

        cuname = request.form.get('user_name')
        cunum = request.form.get('number')
        cumail = request.form.get('user_email')
        cuadd = request.form.get('address')
        custate = request.form.get('state')
        cucity = request.form.get('city')
        cucate = request.form.get('crime')
        cudesc = request.form.get('subject')
        cuzip = request.form.get('code')
        cufile = request.form.get('myfile')
        cudate = request.form.get('datetime')
        if cuname == "":
            error = "Please, Enter your name!!"

        elif cunum == "":
            error = "Please, Enter the number!!"

        elif cumail == "":
            error = "Please,Enter your email!!"

        elif cuadd == "":
            error = "Please, Enter the crime address!!"

        elif custate == "":
            error = "Please, Enter your state!!"

        elif cucity == "":
            error = "Please, Enter your city!!"

        elif cuzip == "":
            error = "Please, Enter your area zip code!!"

        elif cucate == "":
            error = "Please, Enter the crime categories!!"

        elif cufile == "":
            error = "Please, Upload the evidence files!!"

        elif cudate == "":
            error = "Please, Enter the date of crime!!"

        elif cudesc == "":
            error = "Please, describe about the crime!!"

        else:
            mycursor.execute("INSERT INTO `crime_form` (`User_name`,`cudefaultMail`,`User_number`, `User_mail`, `city`, `state`, `zip`,`crime_cate`,`crime_desc`, `crime_add`, `crime_date`, `proof`,`cuaadharNumber`,`currentCrimeStatus`) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                cuname, cudefaultMail, cunum, cumail, cucity, custate, cuzip, cucate, cudesc, cuadd, cudate, cufile, cuaadharNumber, cudefaultStatus))
            mydb.commit()
            success = "Form Submitted Sucessfully :)"

        return render_template('report.html', msg=success, error=error)
    except:
        return redirect('/')


@app.route("/cyber")
def cyber():
    return render_template('cyber.html')


@app.route('/cyber', methods=['POST'])
def cybercrime():

    try:
        error = None
        success = None
        cydefaultMail = logindata.login_user

        mycursor.execute(
            "select * from login_user where Email = %s", [cydefaultMail])
        dataExtract = mycursor.fetchall()
        cyaadharNumber = dataExtract[0][7]
        cydefaultStatus = "Pending"

        cyuname = request.form.get('cy_name')
        cyunum = request.form.get('cy_number')
        cyumail = request.form.get('cy_email')
        cyuadd = request.form.get('cy_address')
        cyustate = request.form.get('cy_state')
        cyucity = request.form.get('cy_city')
        cyucate = request.form.get('cy_crime')
        cyudesc = request.form.get('cy_subject')
        cyuzip = request.form.get('cy_code')
        cyufile = request.form.get('cy_myfile')
        cyudate = request.form.get('cy_datetime')
        if cyuname == "":
            error = "Please, Enter your name!!"

        elif cyunum == "":
            error = "Please, Enter the number!!"

        elif cyumail == "":
            error = "Please,Enter your email!!"

        elif cyuadd == "":
            error = "Please, Enter the crime address!!"

        elif cyustate == "":
            error = "Please, Enter your state!!"

        elif cyucity == "":
            error = "Please, Enter your city!!"

        elif cyuzip == "":
            error = "Please, Enter your area zip code!!"

        elif cyucate == "":
            error = "Please, Enter the crime categories!!"

        elif cyufile == "":
            error = "Please, Upload the evidence files!!"

        elif cyudate == "":
            error = "Please, Enter the date of crime!!"

        elif cyudesc == "":
            error = "Please, describe about the crime!!"

        else:
            mycursor.execute("INSERT INTO `cyber_form` (`Cycase_name`,`CydefaultMail`,`Cycase_number`,`Cycase_email`, `Cycase_address`, `Cycase_state`, `Cycase_city`, `Cycase_crime`, `Cycase_subject`, `Cycase_code`, `Cycase_datetime`,`Cycase_myfile`,`CyaadharNumber`,`currentCyberStatus`) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                cyuname, cydefaultMail, cyunum, cyumail, cyuadd, cyustate, cyucity, cyucate, cyudesc, cyuzip, cyudate, cyufile, cyaadharNumber, cydefaultStatus))
            mydb.commit()
            success = "Form Submitted Sucessfully :)"

        return render_template('cyber.html', msg=success, error=error)
    except:
        return redirect("/")


@app.route('/complainlist')
def complain():

    try:
        mail1 = logindata.login_user
        mail2 = [mail1]
        mycursor.execute(
            "SELECT * FROM crime_form WHERE cudefaultMail = %s", mail2)
        crime_data = mycursor.fetchall()
        mycursor.execute(
            "select * from cyber_form where CydefaultMail = %s", mail2)
        cyber_data = mycursor.fetchall()
        data = crime_data + cyber_data

        return render_template("list.html", value=data)
    except:
        return redirect("/")


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    mydb = mysql.connector.connect(
        host="localhost", user="root", password="", database="Admin")
    mycursor = mydb.cursor()
    error = None
    #success = None

    if request.method == 'POST' and 'username' in request.form and 'paswd' in request.form:
        admi_user = request.form['username']
        password = request.form['paswd']
        mycursor.execute(
            "SELECT * FROM `aduser` WHERE `User_name` LIKE '{}' AND `Password` LIKE '{}'".format(admi_user, password))
        addUser = mycursor.fetchall()

        if len(addUser) > 0:
            session['id'] = addUser[0][0]
            admin.addUser = addUser[0][1]
            return redirect('/welcome')
        else:
            error = "Incorrect username/password!"

    return render_template('adminlogin.html', error=error)


@app.route('/welcome')
def adminwelcome():
    if 'id' in session:
        mycursor.execute("select * from crime_form")
        totalCrimeCases = mycursor.fetchall()
        mycursor.execute("select * from cyber_form")
        totalCyberCases = mycursor.fetchall()
        mycursor.execute("select * from login_user")
        totalUsers = mycursor.fetchall()
        
                    
        pen = "Pending"
        con = "Confirmed"
        mycursor.execute("select * from crime_form where currentCrimeStatus = %s",[pen])
        totalCrimePending = mycursor.fetchall()

        mycursor.execute("select * from crime_form where currentCrimeStatus = %s",[con])
        totalCrimeConfirm = mycursor.fetchall()

        mycursor.execute("select * from cyber_form where currentCyberStatus = %s",[con])
        totalCyberConfirm = mycursor.fetchall()

        mycursor.execute("select * from cyber_form where currentCyberStatus = %s",[pen])
        totalCyberPending = mycursor.fetchall()

        total = [str(len(totalCrimePending) + len(totalCyberPending)), str(len(totalCrimeConfirm) + len(totalCyberConfirm))]
        print("total ",total)
     
        len_data = [len(totalCrimeCases) +
                        len(totalCyberCases) , str(len(totalUsers))  ]

        print("lenght", len_data)
        mycursor.execute(
            "select * from crime_form")
        crime_data = mycursor.fetchall()

        mycursor.execute(
            "select * from cyber_form")
        cyber_data = mycursor.fetchall()
        # len_data.append(total)

        data = [[len_data + total]] + crime_data + cyber_data
        print("data",data)

        return render_template('admin.html', value=data)

    else:
        return redirect('/admin')


@app.route('/edit_profile')
def edit_profile():
    mail1 = logindata.login_user
    mail2 = [mail1]
    mycursor.execute("select * from login_user where Email = %s", mail2)
    data = mycursor.fetchall()
    return render_template('edit_profile.html',value=data)


@app.route('/edit', methods=["GET", "POST"])
def edit():
    mail1 = logindata.login_user
    mail2 = [mail1]
    mycursor.execute("select * from login_user where Email = %s", mail2)
    data = mycursor.fetchall()
    # print(data)
    error = None
    success = None

    getNewName = request.form.get("newName")
    getNewMail = request.form.get("newMail")
    getNewNumber = request.form.get("newNumber")
    getNewAddress = request.form.get("newAddress")
    getNewAadhar = request.form.get("newAadhar")
    getNewCountry = request.form.get("newCountry")
    # getNewPasswd = request.form.get("newPasswd")

    # Aadhar Change
    mycursor.execute("select * from login_user where Email = %s", mail2)
    currentUserMail = mycursor.fetchone()
    print("Number Change : ", currentUserMail)
    mycursor.execute(
        "update login_user set Aadhar = %s where Email = %s", (getNewAadhar, mail2[0]))

    #Address Change
    mycursor.execute("select * from login_user where Email = %s", mail2)
    currentUserMail = mycursor.fetchone()
    mycursor.execute(
        "update login_user set Address = %s where Email = %s", (getNewAddress, mail2[0]))

    #Number Change
    mycursor.execute("select * from login_user where Email = %s", mail2)
    currentUserMail = mycursor.fetchone()
    mycursor.execute("update login_user set `Contact Number` = %s where Email = %s",(getNewNumber, mail2[0]))

    #Country Change
    mycursor.execute("select * from login_user where Email = %s", mail2)
    currentUserMail = mycursor.fetchone()
    mycursor.execute("update login_user set Country = %s where Email = %s",(getNewCountry, mail2[0]))

    #  #Password Change
    # mycursor.execute("select * from login_user where Email = %s", mail2)
    # currentUserMail = mycursor.fetchone()
    # mycursor.execute("update login_user set Password = %s where Email = %s", ([getNewPasswd], mail2))

    #Email Change
    # mycursor.execute("select * from login_user where Email = %s", mail2)
    # currentUserMail = mycursor.fetchone()
    # mycursor.execute('update login_user set Email = %s where Email = %s', (getNewMail, mail2[0]))

    #Name Change
    mycursor.execute("select * from login_user where Email = %s", mail2)
    currentUserMail = mycursor.fetchone()
    print("Name Change : ",currentUserMail)
    mycursor.execute("update login_user set Name = %s where Email = %s", (getNewName, mail2[0]))

    mydb.commit()
    return redirect("/profile")



    # #Email Change
    # mycursor.execute("select * from login_user where Email = %s", mail2)
    # currentUserMail = mycursor.fetchone()
    # print("EMail change : ",currentUserMail)
    # mycursor.execute('update login_user set Email = %s where Email = %s', ([getNewMail], mail2))
    # mydb.commit()

   
    # mydb.commit()
    # #Name Change
    # mycursor.execute("select * from login_user where Email = %s", mail2)
    # currentUserMail = mycursor.fetchone()
    # print("Name Change : ",currentUserMail)
    # mycursor.execute("update login_user set Name = %s where Email = %s", ([getNewName], mail2))
    # mydb.commit()

    #Number Change
    mycursor.execute("select * from login_user where Email = %s", mail2)
    currentUserMail = mycursor.fetchone()
    print("Number Change : ",currentUserMail)
    mycursor.execute("update login_user set Contact\ Number = %s where Email = %s",([getNewNumber], mail2))
    mydb.commit()

    # print(data)


@app.route('/anonymy')
def anonymy():
    return render_template('Annoy.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/feedback')
def feedback():
    return render_template('feed.html')


@app.route('/status')
def cmstatus():
    mail1 = logindata.login_user
    mail2 = [mail1]
    mycursor.execute(
        "select * from crime_form where cudefaultMail = %s", mail2)
    crime_data = mycursor.fetchall()

    mycursor.execute(
        "select * from cyber_form where CydefaultMail = %s", mail2)
    cyber_data = mycursor.fetchall()

    data = crime_data + cyber_data
    print("this", data)
    return render_template('status.html', value=data)

# @app.route('/update')
# def update():
   

    

#     mail1 = logindata.login_user
#     mail2 = [mail1]
#     mycursor.execute(
#         "select * from crime_form where cudefaultMail = %s", mail2)
#     crime_data = mycursor.fetchall()

#     mycursor.execute(
#         "select * from cyber_form where CydefaultMail = %s", mail2)
#     cyber_data = mycursor.fetchall()

#     data = crime_data + cyber_data
#     print(data)

#     return render_template('update_crime.html', value=data)

@app.route('/update')
def update():
      

    
    mycursor.execute(
        "select * from crime_form")
    crime_data = mycursor.fetchall()

    mycursor.execute(
        "select * from cyber_form")
    cyber_data = mycursor.fetchall()

    data = crime_data + cyber_data
    print("update seri",data)


    return render_template('update_crime.html', value=data)


@app.route('/updateCrime', methods=["POST"])
def fetchAll():
    caseNum = request.form.get('uniqueId')
    statusConf = request.form.get('statusConfirm')
    print("caseNum", caseNum)
    print("statusCon",statusConf)
    mycursor.execute("select * from crime_form where case_num = %s",[caseNum])
    mycursor.fetchone()
    mycursor.execute("update crime_form set currentCrimeStatus = %s where case_num = %s", (statusConf, caseNum))
    mydb.commit()
    mycursor.execute("select * from cyber_form where Cycase_id = %s",[caseNum])
    mycursor.fetchone()
    mycursor.execute("update cyber_form set currentCyberStatus = %s where Cycase_id = %s",(statusConf, caseNum))
    mydb.commit()
    # data = mycursor.fetchall()
    return redirect('/update')


if __name__ == '__main__':
    app.run(debug=True)
