from flask import *  
import sqlite3  
  
app = Flask(__name__)  
 
con=sqlite3.connect("employee.db")

@app.route("/")  
def index():  
    return render_template("index.html");  
 
 
@app.route("/savedetails",methods = ["POST","GET"])  
def saveDetails():  
    msg = "msg"  
    if request.method == "POST":  
        try:  
            name = request.form.get("name")  
            email = request.form.get("email")  
            address = request.form.get("address") 
            with sqlite3.connect("employee.db") as con:  
                cur = con.cursor()  
                cur.execute("INSERT into Employees (name, email, address) values (?,?,?)",(name,email,address))  
                con.commit()  
                msg = "Record successfully Added"  
        except:  
            with sqlite3.connect("employee.db") as con:
                con.rollback()  
                msg = "We can not add the employee to the list"  
        finally:
            with sqlite3.connect("employee.db") as con:  
                return render_template("success.html",msg = msg)  
                con.close()  
 
@app.route("/view")  
def view():  
    con = sqlite3.connect("employee.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from Employees")  
    rows = cur.fetchall()  
    return render_template("view.html",rows = rows)

@app.route("/view1",methods=["GET","POST"]) 
def view1():
    id = request.form.get("id")
    con = sqlite3.connect("employee.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute(f"select * from Employees where id={id}")  
    rows = cur.fetchall()  
    return render_template("view1.html",rows = rows)
 

@app.route("/fetch")  
def fetch():  
    return render_template("fetch.html") 
    
@app.route("/delete")  
def delete():  
    return render_template("delete.html")  
 
@app.route("/deleterecord",methods = ["POST"])  
def deleterecord():  
    id = request.form.get("id")  
    with sqlite3.connect("employee.db") as con:  
        try:  
            cur = con.cursor()  
            cur.execute(f"delete from Employees where id = {id}") 
            msg = "record successfully deleted"  
        except:  
            msg = "can't be deleted"  
        finally:  
            return render_template("delete_record.html",msg = msg)   

 
if __name__ == "__main__":  
    app.run(debug = True)  
