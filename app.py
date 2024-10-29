#import base64 ,import math ,import time
import bcrypt, random, os,logging
from flask import Flask,render_template,request,jsonify,make_response,redirect,url_for ,session,flash,g
from flask_mail import Mail,Message
from functions import *
from database1 import initialize_db #,db_connection_alive
from admin import admin_page
from buyer import buyer_page
from seller import seller_page
from dotenv import load_dotenv
from datetime import timedelta
from flask_session import Session
from itsdangerous import URLSafeTimedSerializer
from flask_sqlalchemy import SQLAlchemy
load_dotenv()

app=Flask(__name__)
app.config['SECRET_KEY']=os.getenv('APP_SECRET_KEY')

db=initialize_db()

#configuring session 
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI').replace("mysql://", "mysql+pymysql://")
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,    # Refresh stale connections
    'pool_recycle': 1800       # Recycle connections every 30 minutes
}
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
sessionDb=SQLAlchemy(app)
app.config['SESSION_SQLALCHEMY'] = sessionDb
Session(app) #app.permanent_session_lifetime=timedelta(days=7)

#configuring mail service
app.config['MAIL_SERVER'] ='smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] =True
app.config['MAIL_USERNAME']  = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

serializer=URLSafeTimedSerializer(app.secret_key)

app.register_blueprint(admin_page,url_prefix="/admin")
app.register_blueprint(buyer_page,url_prefix="/buyer")
app.register_blueprint(seller_page,url_prefix="/seller")

def send_mail(recvr,rotp,title,msgBody='Your one time password for signing into Artifusion is'):
    mail = Mail(app) #otp = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    msg_title=title#heading your otp 
    sender='Artifusion454@gmail.com'#common
    email=recvr#user mail
    msg=Message(msg_title,sender=sender,recipients=[email])
    msg.html=render_template("email.html",otp=rotp,msgBody=msgBody)#inside html enter opt
    try:
        mail.send(msg)
        return 'email send '
    except Exception as e:
        print(e)
        return "the email was not send {e}"         
            
@app.before_request
def check_session():
    global db
    if request.endpoint=='static':
        return
    if 'user' not in session and request.endpoint not in ['home','checkdata','verifyotp','handledata','checksellerdata','testadmin','handlesellerdata','verifyAdmin','forgotPass','resetPassword']:
        return redirect(url_for('home'))
    if 'user' in session and request.endpoint in ['home','checkdata','verifyotp','handledata','checksellerdata','testadmin','handlesellerdata','verifyAdmin','forgotPass','resetPassword']:
        if session['user'].get('role')=='buyer':
            return redirect('/buyer')
        elif session['user'].get('role')=='seller':
            return redirect('/seller/home')
        elif session['user'].get('role')=='admin':
            return redirect('/admin/home')
        return redirect('/') 

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login-user",methods=['POST'])
def checkdata():
    req=request.get_json()
    if(req):
        tem,pwd=req['testemail'],req['testpwd']
        # print(tem, pwd)
        userData=fetchoneData("SELECT * FROM users WHERE email='{0}' ".format(tem))
        if not userData:
             res=make_response(jsonify({'message':'No such user exist'}),400)
             return res
        # print(userData)
        if userData[-1]==1: #user account is deleted
            return make_response(jsonify({'message':'Do the account creation step using same email to retrive your account'}),300)
        if not bcrypt.checkpw(pwd.encode('utf-8'),userData[6]):
            return make_response(jsonify({'message':'Incorrect login details'}),400)
        # print('Successfully loged in')
        session['user']= {'data':getdata('buyer',tem),'role':'buyer'} #getdata('buyer',tem)
        session.permanent=True
        # print(session.get('user',{}).get('data'))
        flash("Buyer Login success|success")
        return make_response(jsonify({'message':'Json Received in user login account'}),200)

@app.route('/verify-admin',methods=['POST'])
def verifyAdmin():
    req=request.get_json()
    temp=session.get('tempAdmin')
    if not temp[1] or not temp[0] or not req['otp']:
        return jsonify({'message':"Some Fields are missing ",'status_code':300})        
    if not bcrypt.checkpw(str(req['otp']).encode(),temp[1]):
        return jsonify({'message':"Invalid Otp ",'status_code':400})
    print('otp check ok')
    session.clear()
    session['user']={'data':getdata('admin',temp[0]),'role':'admin'}
    session.permanent=True
    flash('Admin Login success !')
    return jsonify({'message':"demo message",'status_code':200})
        
@app.route("/verify-otp",methods=['POST'])
def verifyotp():
    req=request.get_json()
    requser=req['user']
    isDeleted=session['isdeleted']
    temp=session.get('tempdata')
    hashOtp=temp[-1]
    # print(temp)
    if bcrypt.checkpw(str(req['otp']).encode(),hashOtp):
        # print('both the req and tempotp[0] are equal')
        insert_logs,update_logs=False,False
        if requser=='buyer':#,profile  #,%s  #,demoimg
            query="INSERT INTO users (firstname,lastname,email,password,phone,address) VALUES(%s,%s,%s,%s,%s,%s)"
            values=(temp[0],temp[1],temp[2],temp[3],temp[4],temp[5])
            # print('validity user ok ')  
            query2='UPDATE users set firstname = %s,lastname = %s,password = %s,phone = %s,address=%s,isdeleted=%s  WHERE email= %s'
            values2=(temp[0],temp[1],temp[3],temp[4],temp[5],1,temp[2])
        elif requser=='seller':  #,profile  #,%s  #,demoimg
            query="INSERT INTO sellers (firstname,lastname,email,password,phone,address,shopname,category) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            values=(temp[0],temp[1],temp[2],temp[3],temp[4],temp[5],temp[6],temp[7])
            query2='UPDATE sellers set firstname = %s,lastname = %s,password = %s,phone = %s,address = %s,shopname = %s,category = %s,isdeleted = %s WHERE email= %s' 
            values2=(temp[0],temp[1],temp[3],temp[4],temp[5],temp[6],temp[7],1,temp[2])
        if isDeleted==1:
            update_logs=updateOrDelete(query2,values2,True)
        else:      
            insert_logs=insertData(query,values)
        if insert_logs is True or update_logs is True:
            session['user']={'data':getdata(requser,temp[2]),'role':requser}
            session.permanent=True
            # print(session.get('user',{}).get('data'))
            flash('Account verified Successfully')
            return jsonify({'status_code': 200})
        return jsonify({'status_code': 400, 'user_data':"demo", 'redirect_url': url_for('home'),'res':'json receied-'})            
    return jsonify({'status_code':404})
                
@app.route("/create-user",methods=['POST'])
def handledata():
    req =request.get_json()
    if req:
        # print(req)
        # print(req['firstname'])
        count=fetchoneData("SELECT COUNT(*),isdeleted FROM users WHERE email= '{}' ".format(req['emailid']))
        print(count)
        if count[0] > 0 and count[1] ==0:#res=make_response(jsonify({'message':'Json Received in user create account'}),404)
            return jsonify({'status_code': 404, 'user_data':'', 'redirect_url': url_for('home')})
        # print('User is not already in database ')
        otp = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        try:
            if count[1]==1:
                send_mail(req['emailid'],otp,'Artifusion Buyer Access: Use This OTP to Get Started','Your one time password for retrieving your Artifusion buyer account is')
            else:
                send_mail(req['emailid'],otp,'Artifusion Buyer Access: Use This OTP to Get Started')
            hashOtp=bcrypt.hashpw(otp.encode(),bcrypt.gensalt())
            hashPasswd=bcrypt.hashpw(req['passwd'].encode('utf-8'),bcrypt.gensalt())
            session['tempdata']=[req['firstname'],req['lastname'],req['emailid'],hashPasswd,req['phoneno'],req['address'],hashOtp]            
            session['isdeleted']=count[1]        
        except Exception as e:
            print('excetpion',e)
            return jsonify({'status_code': 400, 'user_data':"demo", 'redirect_url': url_for('home'),'res':'json receied-'})
        # print('session tempdata is ',session.get('tempdata'))
        return jsonify({'status_code': 200})
    #return jsonify({'status_code': 500, 'user_data':'', 'redirect_url': url_for('home')})
        
@app.route("/login-seller",methods=['POST'])
def checksellerdata():
    req=request.get_json()
    if(req):
        print(req) #tem=req['testemail'] pwd=req['testpwd']
        userData=fetchoneData("SELECT * FROM sellers WHERE email= '{0}' ".format(req['testemail']))
        # print(userData)
        if not userData:
             print("No such user")
             return make_response(jsonify({'message':'So such seller Email exist'}),400)
        if userData[-1]==1:
             return make_response(jsonify({'message':'Do the account creation steop'}),300)            
        if not bcrypt.checkpw(req['testpwd'].encode('utf-8'),userData[6]):
            print('Invalid password')
            res=make_response(jsonify({'message':'Invalid password'}),400)
            return res
        print('Successfully loged in')
        session['user']={'data':getdata('seller',req['testemail']),'role':'seller'}
        session.permanent=True
        # print(session.get('user',{}).get('data'))
        res=make_response(jsonify({'message':'Json Received in seller login account'}),200)
        return res
          
@app.route("/create-seller",methods=['POST'])
def handlesellerdata():
    req =request.get_json()
    # print(req)
    if req:
        print(req)
        em=req['emailid']
        count=fetchoneData("SELECT COUNT(*),isdeleted FROM sellers WHERE email='{}' ".format(em))
        # print(count)
        if count[0]>0 and count[1]==0:
            return make_response(jsonify({'message':'An account with same mail id  already exist'}),300)
        # print('seller is not already in database ')
        otp = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        try:
            if count[1]==1:
                send_mail(req['emailid'],otp,'Your One-Time Password to Set Up as a Seller on Artifusion')
            else:
                send_mail(req['emailid'],otp,'Your One-Time Password to Set Up as a Seller on Artifusion')
            hashOtp=bcrypt.hashpw(otp.encode(),bcrypt.gensalt())
            hashPasswd=bcrypt.hashpw(req['passwd'].encode('utf-8'),bcrypt.gensalt())
            session['tempdata']=[req['firstname'],req['lastname'],req['emailid'],hashPasswd,req['phoneno'],req['address'],req['shop'],req['category'],hashOtp]            
            session['isdeleted']=count[1]        
        except Exception as e:
            print('excetpion',e)
            return jsonify({'status_code': 400, 'user_data':"demo", 'redirect_url': url_for('home'),'res':'json receied-'})

        print('session temp data is ',session.get('tempdata'))
        return jsonify({'status_code': 200})

@app.route("/admintest", methods=['POST'])
def testadmin():
    # print('Entered admintest')
    req=request.get_json()
    if req:
        print(req)
        em=req['testemail']
        pd=req['testpwd']
        adminData=fetchoneData("SELECT * FROM admin WHERE email= '{0}' ".format(em))
        if not adminData:
            # print('admin data present')
            return jsonify({'message':"demo message",'status_code':300})
        if not bcrypt.checkpw(pd.encode('utf-8'),adminData[4]):
            # print('nvalid passwd')
            return jsonify({'message':"demo message",'status_code':300})   
        print('Admin Password verified')
        otp = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        send_mail(req['testemail'],otp,'Your OTP for Admin Portal Access - Artifusion')
        hashOtp=bcrypt.hashpw(otp.encode(),bcrypt.gensalt())
        session['tempAdmin']=[req['testemail'],hashOtp]
        flash("Admin login success")
        return jsonify({'message':"demo message",'status_code':200})

@app.route('/forgotPass',methods=['POST'])
def forgotPass():
    print(request.form)
    email=request.form.get('resetEmail')
    userType=request.form.get('userType')
    print(email,userType)
    if not email or (userType not in ['buyer' ,'seller']):
        flash('Invalid userType or email', 'warning')
        # print('failed in if conditn')
        return redirect(url_for('home'))
    table='users' if userType=='buyer' else 'sellers'
    count=fetchoneData( f'SELECT COUNT(*),isdeleted FROM {table} WHERE email = %s ',(email,))
    print(f'count is {count}' )
    if count[0] ==0:
        return redirect(url_for('home'))
    if count[1]==1:
        flash('Your account has been deleted, revive your account by doing account creation step with same email?|warning')        
        return redirect(url_for('home'))
    data={"email":email,"userType":table}
    token=serializer.dumps(data,salt=os.getenv('SERIALIZER_SALT'))
    resetUrl=url_for('resetPassword',token=token,_external=True)
    send_mail(email,resetUrl,f'Artifusion {userType} ','Use the below link to reset your password')
    # print(email)
    # print(userType)
    return redirect(url_for('/'))

@app.route('/resetPassword/<token>',methods=['GET',"POST"])
def resetPassword(token):
    print("Entered reset Pass route")
    try:
        data = serializer.loads(token, salt=os.getenv('SERIALIZER_SALT'), max_age=600)
        print(data)
        email,table=data['email'],data['userType']
    except Exception as e:
        print('The reset link is invalid or has expired.',e)
        return redirect(url_for('forgotPass'))
    if request.method=='POST':
        # print(request.form)
        passwd,confirmPass=request.form.get('passwd'),request.form.get('cPasswd')
        if passwd!=confirmPass:
            print("password and confirm passwd not same")#if possible need to send in alert
        hashPasswd=bcrypt.hashpw(passwd.encode('utf-8'),bcrypt.gensalt())
        update_logs=updateOrDelete(f'UPDATE  {table} SET password = %s WHERE email = %s',(hashPasswd,email),True)
        print('Password updated successfully')
        return redirect(url_for('home'))
    return render_template('resetPassword.html')    
   
@app.route("/about")
def about():
    user_data=session.get('user',{}).get('data')
    imgdata=user_data[-2] if  user_data[-2] is not None else 'https://res.cloudinary.com/dq67ufqzg/image/upload/v1728570558/w58iymkranlgvoxknibj.svg'
    return render_template("about.html",user_data=user_data,imgdata=imgdata)

@app.route('/logout')
def user_logout():
    session.clear()
    flash('Logout success |danger')
    return redirect('/')

@app.route("/payment")
def payment():
    return render_template('payment.html')

if __name__ == '__main__':
    with app.app_context():
        sessionDb.create_all()    
    app.run(host="0.0.0.0",debug=True,port=3000)