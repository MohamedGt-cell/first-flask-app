# Lybraries
from flask import Flask , render_template , request , redirect , session
from cs50 import SQL
import os

#App Flask
app=Flask(__name__)
app.secret_key = os.urandom(24)

#SQL CALL
db=SQL("sqlite:///data.db")

##You are noy apply for 1sessions (Cookies for remembring the user) and for 2Mail,Messages and for 3searching button and for 4Direstring Idea!!

# CONSTANTS
registrants = db.execute("SELECT * FROM registrants") #SQL
AGES=[]
for age in range (1, 100):
    AGES.append(str(age))
WEB="/Stop-Temp.html"
ADMIN_USERNAME="mohammedgt"
ADMIN_PASSWORD="01042007m"

#Variables
LoginStatus=False
Admin=False

#______________________________________________________________Program Run__________________________________________________#

#To Login Page
@app.route("/" , methods=["POST","GET"])
def index():
    return render_template("index-tem.html",message1="",message2="")

#To Sign Up Page
@app.route("/register",methods=["POST","GET"])
def register():
    global Admin
    global LoginStatus
    # Get Inputs
    session["username"] = request.form.get("username")
    session["password"] = request.form.get("password")
    # Erors
    if (not session.get("username") or not session.get("password")):
        print(1)
        return redirect("/Eror")
    elif ((len(session.get("password"))<8) or (len(session.get("password"))>20) or (len(session.get("username"))<4) or (len(session.get("username"))>18)) :
        print(2)
        print(len(session.get("password")))
        print(len(session.get("username")))
        return redirect("/Eror")
    # No Erors
    else:
        session["username"]=session["username"].lower()
        session["password"]=session["password"].lower()
        # Sign Up checkin
        for register in registrants:
            if ((session.get("username") == register["username"]) and not (session.get("password") == register["password"])):
                return render_template("index-tem.html",message1=f"Hello {session.get('username')}",message2= "You entered wrong password!")
            if ((session.get("username") == register["username"]) and (session.get("password") == register["password"])):
                #No Sign up , Login only
                LoginStatus=True
                if(session.get("username")==ADMIN_USERNAME and session.get("password")==ADMIN_PASSWORD): #Admin Checking
                    Admin=True
                return redirect("/notes")
        # YOu will Sign up
        return render_template("/registered.html" , ages=AGES)
            
        

        

#Main Page
@app.route("/notes",methods=("GET","POST"))
def notes():
    global LoginStatus
    global registrants
    # if not login in before
    if (not LoginStatus):
        #Get Inputs
        session["name"]=request.form.get("name")
        session["email"]=request.form.get("email")
        session["surename"]=request.form.get("surename")
        session["age"]=request.form.get("age")
        # Erors
        if ((not session.get("name")) or (not session.get("email")) or (not session.get("surename")) or (not session.get("age")) or (session.get("age") not in AGES)):
            return redirect("/Eror")
        #No Erors - Sing up Section
        else:
            session["name"]=request.form.get("name").lower()
            session["email"]=request.form.get("email").lower()
            session["surename"]=request.form.get("surename").lower()
            session["age"]=request.form.get("age").lower()
            db.execute("INSERT INTO registrants (username , name , surename , age , email , password) VALUES (?,?,?,?,?,?)"
                      ,session.get("username"),
                      session.get("name"),
                      session.get("surename"),
                      session.get("age"),
                      session.get("email"),
                      session.get("password"))
            registrants = db.execute("SELECT * FROM registrants") #SQL
            return render_template(WEB,message="You Sign Up Successfully!")
    # Already Login in
    else:
        LoginStatus=False
        if(Admin):
            return redirect("/Admin")
        else:
            return render_template(WEB,message="You Login in Successfully!")

#Eror Page
@app.route("/Eror")
def notSupproted():
    return render_template("/not-registered.html")

#Admin Page
@app.route("/Admin")
def Adminef():
    global registrants , Admin
    Admin=False
    return render_template("/admin.html",registrants=registrants)