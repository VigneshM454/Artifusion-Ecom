import json
from flask import jsonify ,session,redirect
from database1 import initialize_db
from functools import wraps
from datetime import datetime
from cloudinary1 import storeImg,deleteImg

db=initialize_db()

def format_datetime_for_mysql(iso_datetime):
    if isinstance(iso_datetime, str):
        dt = datetime.fromisoformat(iso_datetime.replace('Z', '+00:00'))
    else:
        dt = iso_datetime    
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def tupletolist(tuple,list):
    for elem in tuple:
        temp=[]
        for item in elem:
            temp.append(item)
        list.append(temp)

def verify_role(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args,**kwargs):
            if 'user' not in session or session['user'].get('role')!=role:
                if session['user'].get('role')=='buyer':
                    return redirect('/buyer')
                if session['user'].get('role')=='seller':
                    return redirect('/seller/home')
                if session['user'].get('role')=='admin':
                    return redirect('admin/home')
                return redirect('/')
            return f(*args,**kwargs)
        return wrapper
    return decorator


def fetchoneData(query):
    db1=initialize_db()
    cursor=db1.cursor()
    cursor.execute(query)
    data=cursor.fetchone()
    cursor.close()
    # print(data)
    return data

def fetchallData(query,var=None):
    cursor=db.cursor()
    cursor.execute(query) if not var else cursor.execute(query,var)
    data=cursor.fetchall()
    cursor.close()
    return data    

def getcount(query):
    count=fetchoneData(query)
    # print(f"Count from getcount is {count[0]}")
    return count[0]

def updateOrDelete(query,var=None,isUpdate=False):
    cursor=db.cursor()
    try:
        cursor.execute(query) if not var else cursor.execute(query,var)
        db.commit()
        return True
    except Exception as e:
        print(f'exception occured:: {e}')
        db.rollback()
        return False
    finally:
        cursor.close()

def deleteProd(prodData,prodId):
    orderCount=getcount('SELECT COUNT(*) FROM demoorders WHERE productid ={}'.format(prodId))
    if orderCount==0:
        # print('delete product')
        delete_logs=updateOrDelete('DELETE FROM products1 WHERE productid = {}'.format(prodId))
        for imgId in prodData:
            deleteImg(imgId)
        if delete_logs:
            return {'status_code':200,'message':'success'}
    else:
        print('entered update products')
        update_logs=updateOrDelete('UPDATE products1 SET isdeleted=%s WHERE productid=%s',(1,prodId,))
        if  update_logs:
            del1=updateOrDelete('DELETE FROM wishlist WHERE productid = %s',(prodId,))
            del2=updateOrDelete('DELETE FROM cart WHERE productid = %s',(prodId,))
            del3=updateOrDelete('DELETE FROM review WHERE productid = %s',(prodId,))
            print(del1,del2,del3)
            return {'status_code':200,'message':'success'}
    return {'status_code':300,'message':'Unable to delte product'}
    
def delSellerData(user_data,isDelete:bool):
    if user_data[-1] is not None:
        deleteImg(user_data[-1])#deleting user Profile Image from cloudinary
    if isDelete:
        update_logs=updateOrDelete('Delete FROM sellers WHERE sellerid = %s',(user_data[0],))
        # print(f"is user deleted {update_logs}")
    else:    
        print('updateing not deleting ........')
        values=(None,None,None,None,None,None,None,1,user_data[0])
        update_logs=updateOrDelete('UPDATE sellers set firstname = %s,lastname = %s,password = %s,phone = %s,address=%s,profile=%s,profileId=%s,isdeleted=%s  WHERE sellerid= %s',values,True)
    #here need to delete all products
    prodIdArr=fetchallData('SELECT productid FROM products1 WHERE sellerid = %s',(user_data[0],))
    prodIdArr= prodIdArr[0] if prodIdArr else None
    if not prodIdArr:
        return {'status_code':200,'message':'success'}       
    print(prodIdArr)#prodIdArr[0]
    for id in prodIdArr:
        orderCount=getcount('SELECT COUNT(*) FROM demoorders WHERE productid ={0}'.format(id))
        if orderCount==0:
            prodDetail=fetchoneData('SELECT imgId1,imgId2,imgId3 from products1 WHERE productid= {0}'.format(id))
            for imgId in prodDetail:
                deleteImg(imgId)
            delete_logs=updateOrDelete('DELETE FROM products1 WHERE productid = %s',(id,))
        else:
            update_logs2=updateOrDelete('UPDATE products1 SET isdeleted=%s WHERE productid=%s',(1,id,))
            if  update_logs2:
                del1=updateOrDelete('DELETE FROM wishlist WHERE productid = %s',(id,))
                del2=updateOrDelete('DELETE FROM cart WHERE productid = %s',(id,))
                del3=updateOrDelete('DELETE FROM review WHERE productid = %s',(id,))
                print(del1,del2,del3)
    if update_logs and (delete_logs or update_logs2) is True:
        return {'status_code':200,'message':'success'}
    return {'status_code':400,'message':'Account deletion failed'}            
    

def getdata(table,mail):
    if table=='buyer':    
        print("from getdata fn",table ,mail)
        udata=fetchoneData("SELECT buyerid,firstname,lastname,phone,email,address,profile,profileId FROM users WHERE email = '{}' ".format(mail) )
        # print(udata)
    elif table=='seller':#seller  
        print("from getdata fn",table ,mail)
        udata=fetchoneData("SELECT sellerid,firstname,lastname,phone,email,address,shopname,profile,category,profileId FROM sellers WHERE email = '{}' ".format(mail) )
        # print(udata)#udata is tuple no doubt
    else:#admin here change needed
        print("admin table")
        udata=fetchoneData("SELECT id,firstname,lastname,phone,email,profile,profileId FROM admin WHERE email = '{}' ".format(mail) )
        # print(udata)
    a=udata#0-id,1-firstname,2-lastname,3-phone,4-mail,5-pwd,6-prof 
    return a

def showprod(place):
    user_data= session.get('user',{}).get('data')  
    print(user_data[0],place)
    prods=fetchallData("SELECT productid FROM {} WHERE buyerid= '{}' ".format(place,user_data[0]))
    prodarr=[]
    if prods:
        prodarr=[prod[0] for prod in prods]
        placeholders = ', '.join(['%s'] * len(prodarr))
        query = f"SELECT * FROM products1 WHERE productid IN ({placeholders})"
        count=fetchallData(query,prodarr)
        dictarr,countlist=[],[]
        keys=['productid','prodname','prodprice','proddesc','qtyavail','qtysold','prodimg1','prodimg2','prodimg3','sellerid']
        for i in  range(len(count)):#6,7,8
            countlist.append(list(count[i]))
        for i in range(len(countlist)):            
            dictarr.append(dict(zip(keys,countlist[i])))
        js1=json.dumps(dictarr)
        return js1

def insertData(query,val):
    try:
        cursor=db.cursor()
        cursor.execute(query,val)
        db.commit()
        cursor.close()
    except Exception as e:
        print("excetption ",e)
        return False  #jsonify({'status_code':404,'message':'error occured'})
    return True #jsonify({'status_code':200,'message':'success'})