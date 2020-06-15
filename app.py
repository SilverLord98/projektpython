from flask import Flask,render_template,request,Response,redirect,url_for,session,abort
import sqlite3 as sql
from flask_login import LoginManager,UserMixin,login_required,login_user,logout_user,current_user
from datetime import datetime
import os
import time
from werkzeug import secure_filename

app=Flask(__name__)

# config
app.config.update(
        DEBUG =True,
        SECRET_KEY ='sekretny_klucz'
)
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
# ustawienie flask-login
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"

#model uzytkownika
class User(UserMixin):
    def __init__(self,id):
        self.id =id
        self.name =str(id)
        self.password=self.name 
    def __repr__(self):
            return"%s"%(self.name)
#generacja uzytkownikow
users =[User(id)for id in range(1,10)]
@app.route("/")
def main():
    return render_template('index.html')
@app.route("/aboutdiff/<login>")
@login_required
def aboutdiff(login):
    con =sql.connect("database.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("SELECT imie,nazwisko,adres,opis FROM users where name=?",(login,))
    rekordy =cur.fetchall()
    return render_template('omniediff.html',rekordy=rekordy,login=login)
@app.route('/time_feed')
def time_feed():
    def generate():
        yield datetime.now().strftime("%Y.%m.%d    %H:%M:%S") 
    return Response(generate(), mimetype='text')      
@app.route("/about")
@login_required
def about_me():
    login=str(current_user)
    print(login)
    con =sql.connect("database.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("SELECT imie,nazwisko,adres,opis FROM users where name=?",(login,))
    rekordy =cur.fetchall()
    return render_template('omnie.html',rekordy=rekordy)
@app.route("/abouteedit")
@login_required
def abouteedit():
    login=str(current_user)
    print(login)
    con =sql.connect("database.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("SELECT imie,nazwisko,adres,opis FROM users where name=?",(login,))
    rekordy =cur.fetchall()
    return render_template('omnieedit.html',rekordy=rekordy)
@app.route('/edit',methods =['POST','GET'])
def edit():
    if request.method=='POST':
        try:
           login=str(current_user)
           imie=request.form['imie']
           nazwisko=request.form['nazwisko']
           adres=request.form['adres']
           opis=request.form['opis']
           with sql.connect("database.db") as con:
                cur=con.cursor()
                cur.execute("update users set imie=?,nazwisko=?,adres=?,opis=? where name=?",(imie,nazwisko,adres,opis,login))
                con.commit()
                msg="Edycja zapisana"
        except:
            con.rollback()
            msg="Blad edycja"
        finally:
            return render_template('rezultat.html',msg=msg)
            con.close()
@app.route("/register")
def register():
    return render_template('register.html')
@app.route('/adduser',methods =['POST','GET'])
def adduser():
    if request.method=='POST':
        try:
           login=request.form['login']
           password=request.form['password']
           con =sql.connect("database.db")
           cur=con.cursor()
           cur.execute("SELECT name,password FROM users where name=?",(login,))
           while True:
                  row = cur.fetchone()
                  if row == None:
                      print("cos")
                      cur=con.cursor()
                      cur.execute("INSERT INTO users(name,password) VALUES (?,?)",(login,password))
                      con.commit()
                      msg="Zarejestrowany"
                      break
                  else:
                      msg="Login istnieje"
                      return render_template('rezultat.html',msg=msg)
                      con.close()
                      break
           
        except:
            con.rollback()
            msg="Blad przy rejestracji"
        finally:
            return render_template('rezultat.html',msg=msg)
            con.close()
@app.route("/galeria")
def galeria():
    tab={"1.jpg","2.jpg","3.jpg","4.jpg","5.jpg","6.jpg"}
    return render_template("galeria.html",tab=tab)
@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader',methods = ['GET','POST'])
def uploader_file():
    if request.method =='POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],"6.jpg"))
            return render_template('rezultat.html',msg="Wysłane")
@app.route("/info")
@login_required
def info_me():
    con =sql.connect("database.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute('SELECT * FROM posty')
    rekordy =cur.fetchall()
    return render_template('informacje.html',rekordy=rekordy)
@app.route('/addpost',methods =['POST','GET'])
def addpost():
    if request.method=='POST':
        try:
           user =request.form['user']
           tekst=request.form['tekst']
           with sql.connect("database.db") as con:
                cur=con.cursor()
                cur.execute("INSERT INTO posty(user,tekst) VALUES (?,?)",(user,tekst))
                con.commit()
                msg="Rekord zapisany"
        except:
            con.rollback()
            msg="Blad przy dodawaniu rekordu"
        finally:
            con =sql.connect("database.db")
            con.row_factory=sql.Row
            cur=con.cursor()
            cur.execute('SELECT * FROM posty')
            rekordy =cur.fetchall();
            return render_template('informacje.html',rekordy=rekordy)
            con.close()
@app.route("/login",methods=["GET","POST"])
def login():
    tytul='Zaloguj się'
    if request.method=='POST':

        username=request.form['username']
        password=request.form['password']
        con =sql.connect("database.db")
        cur=con.cursor()
        cur.execute("SELECT name,password FROM users where name=?",(username,))
        while True:
              row = cur.fetchone()
              print(username)
              if row == None:
                  print("cos")
                  break
              print(type(row[1]))
              password2=row[1]
              print(type(password))
              print(password2)
        
        if password2==password:
            id =username.split()[0]
            user=User(id)
            login_user(user)
            return render_template('loginin.html')
        else:
            return abort(401)
    else:
        return render_template('formularz_logowania.html')
@app.errorhandler(401)
def page_not_found(e):
    tytul="Coś poszło nie tak..."
    blad="401"
    return render_template('blad.html',tytul=tytul,blad=blad)
@app.route("/logout")
@login_required
def logout():
    logout_user()
    tytul="Wylogowanie"
    return render_template('logout.html',tytul=tytul)
@login_manager.user_loader
def load_user(userid):
    return User(userid)

if __name__ == "__main__":
    app.run()
    
    
