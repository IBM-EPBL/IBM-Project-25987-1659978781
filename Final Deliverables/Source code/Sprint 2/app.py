import bcrypt
import ibm_db
from sendmail import *
from flask import Flask, redirect, render_template, request, session, url_for

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=2d46b6b4-cbf6-40eb-bbce-6251e6ba0300.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32328;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=tll03894;PWD=tG6gZMNmEM2J6IJ7",'','')



app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/",methods=['GET'])
def home():
    if 'email' not in session:
      return redirect(url_for('index'))
    return render_template('index.html',name='Home')
@app.route("/index")
def index():
  return render_template('index.html')
@app.route("/index1")
def index1():
  return render_template('index1.html')

@app.route("/job_details")
def  job_details():
  return render_template('job_details.html')


@app.route("/job_details1")
def  job_details1():
  return render_template('job_details1.html')

@app.route("/job_details2")
def  job_details2():
   return render_template('job_details2.html')

@app.route("/job_details3")
def  job_details3():

  return render_template('job_details3.html')
   
@app.route("/job_details4")
def  job_details4():
  return render_template('job_details4.html')

@app.route("/job_details5")
def job_details5():
  return render_template('job_details5.html')

@app.route("/job_details6")
def job_details6():
  return render_template('job_details6.html')

@app.route("/job_listing")
def job_listing():
  return render_template('job_listing.html')

@app.route("/about")
def about():
  return render_template('about.html')







@app.route("/registeration",methods=['GET','POST'])
def registeration():
  if request.method == 'POST':
    name = request.form['name']
    email = request.form['email']
    phn = request.form['phn']
    psw = request.form['psw']

    if not name or not email or not phn or not psw:
      return render_template('registeration.html',error='Please fill all fields')
    hash=bcrypt.hashpw(psw.encode('utf-8'),bcrypt.gensalt())
    query = "SELECT * FROM user_detail WHERE name=?"
    stmt = ibm_db.prepare(conn, query)
    ibm_db.bind_param(stmt,1,name)
    ibm_db.execute(stmt)
    print(stmt)
    isUser = ibm_db.fetch_assoc(stmt)
    if not isUser:
      insert_sql = "INSERT INTO user_detail(name, email, phn, psw) VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, email)
      ibm_db.bind_param(prep_stmt, 3, phn)
      ibm_db.bind_param(prep_stmt, 4, psw)
      ibm_db.execute(prep_stmt)


      sendMailUsingSendGrid(API,from_email,to_emails,subject,html_content)
      return render_template('registeration.html',success="You can login")
    else:
      return render_template('registeration.html',error='Invalid Credentials')

  return render_template('registeration.html',name='Home')

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
      email = request.form['email']
      psw = request.form['psw']

      if not email or not psw:
        return render_template('login.html',error='Please fill all fields')
      query = "SELECT * FROM user_detail WHERE email=?"
      stmt = ibm_db.prepare(conn, query)
      ibm_db.bind_param(stmt,1,email)
      ibm_db.execute(stmt)
      isUser = ibm_db.fetch_assoc(stmt)
      print(isUser,psw)

      if not isUser:
        return render_template('login.html',error='Invalid Credentials')
      
      isPasswordMatch = 1 if psw==isUser['PSW'] else 0 #bcrypt.checkpw(psw.encode('utf-8'),isUser['PSW'].encode('utf-8'))

      if not isPasswordMatch:
        print("wrong psw")
        return render_template('login.html',error='Invalid Credentials')
      print("correct psw")
      session['email'] = isUser['EMAIL']
      return redirect(url_for('home'))

    return render_template('login.html',name='Home')

@app.route("/apply",methods=['GET','POST'])
def apply():
  if request.method == 'POST':
    name = request.form['name']
    email = request.form['email']
    psw = request.form['password']
    age = request.form['age']
    job = request.form['job']
    interest = request.form['interest']
  

    if not name or not email or not psw:
      return render_template('apply.html',error='Please fill all fields')
    hash=bcrypt.hashpw(psw.encode('utf-8'),bcrypt.gensalt())
    query = "SELECT * FROM applyform WHERE email=? OR psw=?"
    stmt = ibm_db.prepare(conn, query)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.bind_param(stmt,2,psw)
    ibm_db.execute(stmt)
    isUser = ibm_db.fetch_assoc(stmt)
    if not isUser:
      insert_sql = "INSERT INTO admin_detail(name, email, psw,age,job,interest) VALUES (?,?,?,?,?,?)"
      
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, email)
      ibm_db.bind_param(prep_stmt, 3, psw)
      ibm_db.bind_param(prep_stmt, 4, age)
      ibm_db.bind_param(prep_stmt, 5, job)
      ibm_db.bind_param(prep_stmt, 6, interest)
      ibm_db.execute(prep_stmt)
      return render_template('apply.html',success="You can login")
    else:
      return render_template('apply.html',error='Invalid Credentials')

  return render_template('apply.html',name='Home')


if __name__ == "__main__":
    app.run(debug=True)
