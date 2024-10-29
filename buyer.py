import json,math
from flask import Blueprint, Flask,render_template,request,jsonify,make_response,redirect,url_for ,session,flash
from functions import *
from cloudinary1 import storeImg,deleteImg
from datetime import datetime

buyer_page=Blueprint(
    "artifusion/buyer",__name__,static_folder="static",
    template_folder="templates")

@buyer_page.route("/")
@verify_role('buyer')
def buyhome():
    user_data= session.get('user',{}).get('data')
    if user_data:
        # print(user_data)
        products=fetchallData('SELECT productid,prodname,prodprice,prodimg1,category FROM products1 WHERE isdeleted=0')
        jewellery,pottery,toys,homedecor,artworks,furniture=[],[],[],[],[],[]
        for i in products:#jewel furn pottery homedecor toys 
            if i[-1]=='jewel':
                jewellery.append(i)
            elif i[-1]=='furn':
                furniture.append(i)
            elif i[-1]=='pottery':
                pottery.append(i)
            elif i[-1]=='homedecor':
                homedecor.append(i)
            elif i[-1]=='toys':
                toys.append(i)
            else:
                artworks.append(i)
        # print("Printing form /get mtethdkflfjk")
        productDict={
            "jwl":{"title":"Jewellery","prods":jewellery,"id":"jewelry"},
            "pot":{"title":"Pottery","prods":pottery,"id":"pottery"},
            "toys":{"title":"Toys","prods":toys,"id":"toys"},
            "decor":{"title":"Home Decor","prods":homedecor,"id":"homedecor"},
            "art":{"title":"Artworks","prods":artworks,"id":"artworks"},
            "furn":{"title":"Furniture","prods":furniture,"id":"furnitures"}
        }
        # print(productDict)
        imgdata=user_data[-2] if  user_data[-2] is not None else 'https://res.cloudinary.com/dq67ufqzg/image/upload/v1728570558/w58iymkranlgvoxknibj.svg'
        return render_template('home.html',user_data=user_data,imgdata=imgdata,productDict=productDict)
    return redirect('/')

@buyer_page.route("/order")
@verify_role('buyer')
def buyorder():
    user_data=session.get('user',{}).get('data')
    count=getcount('SELECT COUNT(*) FROM demoorders  WHERE   buyerid={0} '.format(user_data[0]))
    # print('count of orders is',count)
    orderdata=''
    proddata=[]
    err=''
    if count==0:
        err= ({'js':'demo','status_code':500})
    else:
        orderdata=fetchallData('SELECT  orderid, productid,orderstatus FROM demoorders WHERE buyerid = {0} ORDER BY orderid DESC'.format(user_data[0]))
        prodidarr=[order[1] for order in orderdata]
        for prodid in prodidarr:
            p=fetchoneData('SELECT prodimg1,prodname,prodprice,proddesc,qtyavail,sellerid FROM products1 WHERE productid = {0}'.format(prodid))
            proddata.append(p)
    imgdata=user_data[-2] if  user_data[-2] is not None else 'https://res.cloudinary.com/dq67ufqzg/image/upload/v1728570558/w58iymkranlgvoxknibj.svg'
    return render_template("order.html",user_data=user_data,imgdata=imgdata,orderdata1=orderdata,proddata1=proddata,err=err)

@buyer_page.route("/orderdetail/<int:oid>")
@verify_role('buyer')
def orderdetail(oid):
    user_data=session.get('user',{}).get('data')
    count=getcount('SELECT COUNT(*) FROM demoorders WHERE   orderid={0} and buyerid={1} '.format(oid,user_data[0]))
    err=''
    orderdetail,prodetail=[],[]
    if count==0:
        err= ({'ordermsg':"Sorry no such order exist",'status_code':404})
    else:
        orderdetail=fetchoneData('SELECT orderid, productid,shipping_addr,totamt,paymethod,orderstatus,orderdate,orderqty FROM demoorders WHERE orderid = {0}'.format(oid))
        # print(orderdetail)
        prodetail=fetchoneData('SELECT prodimg1,prodname,prodprice,proddesc,qtyavail,sellerid FROM products1 WHERE productid = {0}'.format(orderdetail[1]))
    imgdata=user_data[-2] if  user_data[-2] is not None else 'https://res.cloudinary.com/dq67ufqzg/image/upload/v1728570558/w58iymkranlgvoxknibj.svg'        
    return render_template('orderdetail.html',user_data=user_data,imgdata=imgdata,err=err,orderdetail2=orderdetail,prodetail1=prodetail)

@buyer_page.route("/searchdemo",methods=["POST"])
@verify_role('buyer')
def searchprods():
    req =request.get_json()
    if(req):
        match_Prod=fetchallData('SELECT productid, prodname, prodprice, prodimg1, category FROM products1 WHERE prodname LIKE %s and isdeleted=0', ('%' + req + '%',))
        dictarr=[]
        keys=['productid','prodname','prodprice','prodimg1','category']
        for i in  range(len(match_Prod)):#6,7,8
            dictarr.append(dict(zip(keys,match_Prod[i])))
        js1=json.dumps(dictarr)
        return ({'js':js1,'status_code':200})

@buyer_page.route("/wishlist")
@verify_role('buyer')
def wishlist():
    user_data= session.get('user',{}).get('data')  
    count=getcount('SELECT COUNT(*) FROM wishlist WHERE buyerid= {0}'.format(user_data[0]))
    # print(count)
    prods=[]
    if count!=0:
        prods=fetchallData('SELECT productid,prodname,prodprice,prodimg1,qtyavail FROM products1 WHERE productid IN (SELECT productid FROM wishlist WHERE buyerid= {0}) '.format(user_data[0]))
        # print(prods)
    imgdata=user_data[-2] if  user_data[-2] is not None else 'https://res.cloudinary.com/dq67ufqzg/image/upload/v1728570558/w58iymkranlgvoxknibj.svg'    
    return render_template("wishlist.html",user_data=user_data,imgdata=imgdata,count=count,prods=prods)


@buyer_page.route("/cart",methods=["GET","POST"])
@verify_role('buyer')
def cart():
    user_data= session.get('user',{}).get('data')
    if request.method=='POST':
        count=getcount('SELECT COUNT(*) FROM cart WHERE   buyerid={0}'.format(user_data[0]))
        # print(count)
        if count==0:
            return ({'js':'demo','status_code':500})
        js1=showprod('cart')
        return ({'js':js1,'status_code':200})
    imgdata=user_data[-2] if  user_data[-2] is not None else 'https://res.cloudinary.com/dq67ufqzg/image/upload/v1728570558/w58iymkranlgvoxknibj.svg'
    return render_template("cart.html",user_data=user_data,imgdata=imgdata)

@buyer_page.route("/cart/remove",methods=['POST'])
@verify_role('buyer')
def cartremove():
    req =request.get_json()
    user_data= session.get('user',{}).get('data')
    if req:    
        # print(req['productid'])  
        del_logs=updateOrDelete('DELETE  FROM cart WHERE productid = {0} AND  buyerid={1} '.format(req['productid'],user_data[0]))
        if del_logs is True:
            return jsonify({'status_code':200,'message':'success'})
        return jsonify({'status_code':400,'message':'Failure'})
    return jsonify({'status_code':400,'message':'success'})

@buyer_page.route("/cart/later",methods=['POST'])
@verify_role('buyer')
def cart2wishlist():
    req =request.get_json()
    user_data= session.get('user',{}).get('data')
    if req:
        del_logs=updateOrDelete('DELETE FROM cart WHERE productid = {} AND buyerid = {}'.format(req['productid'],user_data[0]))
        if del_logs is True:
            insertLogs=insertData('INSERT INTO wishlist (productid,buyerid) VALUES(%s,%s)',(req['productid'],user_data[0]))            
            return jsonify({'status_code':200,'message':'success'}) if insertLogs else   jsonify({'status_code':400,'message':'Issue in adding product to wishlist'})
        return jsonify({'status_code':400,'msg':'Error in moving product from cart to wishlist'})
    
@buyer_page.route("/prod/wish",methods=["POST"])
@verify_role('buyer')
def addwish():
    req =request.get_json()
    user_data= session.get('user',{}).get('data')
    if req:
        # print(req['productid'])
        count=getcount('SELECT COUNT(*) FROM cart WHERE productid = {0} AND  buyerid= {1}'.format(req['productid'],user_data[0]))
        count2=getcount('SELECT COUNT(*) FROM wishlist WHERE productid = {0} AND  buyerid= {1}'.format(req['productid'],user_data[0]))
        if count==0 and  count2==0:
            insertLogs=insertData('INSERT INTO wishlist (productid,buyerid) VALUES(%s,%s)',(req['productid'],user_data[0]))            
            return ({'status_code':200}) if insertLogs else ({'status_code':400})
        return ({'status_code':300})

@buyer_page.route("/prod/cart",methods=["POST"])
@verify_role('buyer')
def addcart():
    req =request.get_json()
    # print(req['productid'])
    user_data= session.get('user',{}).get('data')
    if req:
        count=getcount('SELECT COUNT(*) FROM cart WHERE productid = {0} AND  buyerid={1}'.format(req['productid'],user_data[0]))
        count2=getcount('SELECT COUNT(*) FROM wishlist WHERE productid = {0} AND  buyerid={1}'.format(req['productid'],user_data[0]))
        if count==0:#if it is not already present in cart 
            if count2>0:
                del_log=updateOrDelete(('DELETE  FROM wishlist WHERE productid = {0} AND  buyerid={1}'.format(req['productid'],user_data[0])))
                # print(del_log)
            insertLogs=insertData('INSERT INTO cart (productid,buyerid) VALUES(%s,%s)',(req['productid'],user_data[0]))            
            return jsonify({'status_code':200,'message':'success'}) if insertLogs else jsonify({'status_code':400,'message':'Issue in adding data to cart'})
        return jsonify({'status_code':300})

@buyer_page.route("/wishlist/remove",methods=["POST"])
@verify_role('buyer')
def deletewishlist():
    req =request.get_json()
    user_data= session.get('user',{}).get('data')
    if req:    
        del_logs=updateOrDelete('DELETE  FROM wishlist WHERE productid = {0} AND  buyerid={1}'.format(req['productid'],user_data[0]))
        if del_logs:
            return jsonify({'status_code':200,'message':'success'})
        return jsonify({'status_code':400,'message':'failure'})
                
@buyer_page.route("/checkout")
@verify_role('buyer')
def checkout():
    user_data=session.get('user',{}).get('data')
    imgdata=user_data[-2] if  user_data[-2] is not None else 'https://res.cloudinary.com/dq67ufqzg/image/upload/v1728570558/w58iymkranlgvoxknibj.svg'
    return render_template("checkout.html",user_data=user_data,imgdata=imgdata)
 
@buyer_page.route("/cart/checkout",methods=["POST"])
@verify_role('buyer')
def addcheckdata():
    req=request.get_json()
    a=json.dumps(req)
    if req:
        js1=showprod('cart')
        session['checkoutobj']=a
        return ({'js':js1,'object':a,'status_code':200})

@buyer_page.route("/product/checkout",methods=["POST"])
@verify_role('buyer')
def buyprod1():
    req=request.get_json()
    # print(req)
    object={str(req['pid']):req['pqty']}
    prod=fetchoneData('SELECT productid,prodname,prodprice,proddesc, qtyavail,qtysold,prodimg1,sellerid FROM  products1 WHERE productid = {0}'.format(req['pid']))
    # print(".................")
    dictarr=[]
    keys=['productid','prodname','prodprice','proddesc','qtyavail','qtysold','prodimg1','sellerid']
    dictarr.append(dict(zip(keys,prod)))
    js11=json.dumps(dictarr)
    return ({'js':js11,'object':object,'status_code':200})
   
@buyer_page.route("/product/checkrev",methods=['POST'])
@verify_role('buyer')
def checkeligible():
    user_data=session.get('user',{}).get('data')
    req=request.get_json()
    # print('req is ',req)
    # print('buyer id is ',user_data[0])
    count=getcount('SELECT COUNT(*) FROM demoorders WHERE buyerid = {0} and productid ={1}'.format(user_data[0],req))
    # print('orders count is ',count)
    if count>0:#the user already bought that particular product or not
        countrev=getcount('SELECT COUNT(*) FROM review WHERE buyerid ={0} and productid = {1}'.format(user_data[0],req))
        if countrev==0:#if the user already written a review or not
            # print('you are eligble to write review')
            return {'status_code':200} 
        # print('you are not eligble to write review')
        return {'status_code':400}             
    return {'status_code':300}

@buyer_page.route("/product/createrev",methods=["POST"])
@verify_role('buyer')
def createrev():
    user_data=session.get('user',{}).get('data')
    req=request.get_json()
    if req:
        sellerId=fetchoneData('SELECT sellerid from products1 WHERE productid= {0}'.format(req['rprod']))[0]
        # print(f'seller id is {sellerId}')
        insert_logs=insertData('INSERT INTO review (productid,rating,reviewtext,reviewtype,usertype,buyerid,sellerid) VALUES(%s,%s,%s,%s,%s,%s,%s)',(req['rprod'],req['rrating'],req['rdesc'],'review','buyer',user_data[0],sellerId))
        return {'status_code':200} if insert_logs else  {'status_code':400}
    #else:
    #    return{'status_code':404}

@buyer_page.route("/checkout/123",methods=['POST'])
@verify_role('buyer')
def checkoutGpdata():
    cartdata=showprod('cart')
    # print("am i executed")
    cobj=session.get('checkoutobj')
    session['checkoutobj']=None
    if cartdata and cobj:
        return ({'js':cartdata,'object':cobj,'status_code':200})
    return ({'js':cartdata,'object':'no object present','status_code':404})

@buyer_page.route("/checkout/buy",methods=['POST'])
@verify_role('buyer')
def placeorder():
    req =request.get_json()
    # print(req['ordertime'])
    user_data= session.get('user',{}).get('data')#prodid to be included
    if req: #prodqt to be added to qtysold and subtracted from qtyavail
        totamt,proddetailarr,prodqtarr,prodidarr,ordertime,shipaddr,paymethod,prodpricearr=req['totamt'],req['proddetailarr'],req['prodqtarr'],req['prodidarr'],format_datetime_for_mysql(req['ordertime']),req['shipaddr'],req['paymethod'],req['prodpricearr']
        count=getcount('SELECT COUNT(*) FROM cart WHERE productid = {0} AND  buyerid={1}'.format(prodidarr[0],user_data[0]))
        # print(count)
        prodqtdetail=fetchallData('SELECT qtyavail,qtysold  FROM products1 WHERE productid IN ({0})'.format(','.join(map(str,prodidarr))))
        # print(prodqtdetail)
        if count==0:#if it is not already present in cart # try:            
            # print(ordertime)
            insert_logs=insertData('INSERT INTO demoorders (buyerid,productid,shipping_addr,proddetail,totamt,paymethod,orderstatus,orderdate,orderqty) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)',(user_data[0],prodidarr[0],shipaddr,proddetailarr[0],totamt,paymethod,'yet to be delivered',ordertime,prodqtarr[0]))
            # print(insert_logs)
            if insert_logs is True:
                update_logs=updateOrDelete('UPDATE products1 SET qtyavail={} ,qtysold={} WHERE productid={}'.format(prodqtdetail[0][0]-prodqtarr[0],prodqtdetail[0][1]+prodqtarr[0],prodidarr[0]),None,True)
                if update_logs is True:
                    return jsonify({'status_code':200,'message':'success'})
            return jsonify({'status_code':404,'message':'error occured'})
        else: #try:
            for i in range(len(prodidarr)):
                insert_logs=insertData('INSERT INTO demoorders (buyerid,productid,shipping_addr,proddetail,totamt,paymethod,orderstatus,orderdate,orderqty) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)',(user_data[0],prodidarr[i],shipaddr,proddetailarr[i],prodpricearr[i],paymethod,'yet to be delivered',ordertime,prodqtarr[i]))
                if not insert_logs:
                    return jsonify({'status_code':300})                
                # print(insert_logs)
            for i in range(len(prodidarr)):
                del_logs=updateOrDelete('DELETE  FROM cart WHERE productid = {0} AND  buyerid={1}'.format(prodidarr[i],user_data[0]))
                update_logs=updateOrDelete('UPDATE products1 SET qtyavail={} ,qtysold={} WHERE productid={}'.format(prodqtdetail[i][0]-prodqtarr[i],prodqtdetail[i][1]+prodqtarr[i],prodidarr[i]),None,True)
                if not del_logs or not update_logs:
                    return jsonify({'status_code':300})
            return jsonify({'status_code':200,'message':'success'})
                
@buyer_page.route("/userprofile/edit",methods=['POST'])
@verify_role('buyer')
def editprof():
    user_data=session.get('user',{}).get('data')
    # print(request.files)
    # print(request)
    # print(request.form)
    if(request):
        secureUrl,imgId=None,None
        image=request.files.get('file')
        fname,lname,phone,addr,pwd=request.form.get('fname'),request.form.get('lname'),request.form.get('phone'),request.form.get('addr'),request.form.get('pwd')
        if image:
            # print('file is present')
            secureUrl,imgId=storeImg(image)
            if user_data[-1]:
                deleteImg(user_data[-1])
        query=''
        values=()
        if pwd=='':
            query="UPDATE users SET firstname = %s,lastname = %s,phone = %s,address = %s,profile = %s,profileId = %s   WHERE email= %s"
            values=(fname,lname,phone,addr,secureUrl,imgId,user_data[4])
        else:
            query="UPDATE users SET firstname = %s,lastname = %s,phone = %s,address = %s,password = %s,profile = %s, profileId= %s   WHERE email= %s"
            values=(fname,lname,phone,addr,pwd,secureUrl,imgId ,user_data[4])
        update_logs= updateOrDelete(query,values,True)
        if update_logs is True:
            session['user']={'data':getdata('buyer',user_data[4]),'role':'buyer'}
            session.permanent=True
            return jsonify({'status_code': 200, 'imgdata': 'hi'})            
        print('problem iruku')
        return jsonify({'status_code': 500, 'imgdata':''})

@buyer_page.route("/userprofile")
@verify_role('buyer')
def profile():
    user_data=session.get('user',{}).get('data')
    if not user_data:
        return redirect('/')
    imgdata=user_data[-2] if  user_data[-2] is not None else 'https://res.cloudinary.com/dq67ufqzg/image/upload/v1728570558/w58iymkranlgvoxknibj.svg'
    return render_template("userprofile.html",user_data=user_data,imgdata=imgdata)

@buyer_page.route("/product/<int:product_id>")
@verify_role('buyer')
def product(product_id):
    # print(product_id)
    user_data=session.get('user',{}).get('data')
    if not user_data:
        return redirect('/')#its not count its prod
    imgdata=user_data[-2] if  user_data[-2] is not None else 'https://res.cloudinary.com/dq67ufqzg/image/upload/v1728570558/w58iymkranlgvoxknibj.svg'
    defaultImg='https://res.cloudinary.com/dq67ufqzg/image/upload/v1728570558/w58iymkranlgvoxknibj.svg'
    product=fetchoneData('SELECT * FROM products1  WHERE productid = {0} and isdeleted=0'.format(product_id))    
    if not product:
        # print("There is no such product")
        return render_template("product.html",user_data=user_data,imgdata=imgdata,count=0)
    qtymax,sellerid=product[4],product[-6]
    keys=['productid','prodname','prodprice','proddesc','qtyavail','qtysold','prodimg1','prodimg2','prodimg3','sellerid','category']        
    sellerinfo=fetchoneData('SELECT firstname,lastname,profile FROM sellers WHERE sellerid = {0}'.format(sellerid))
    dictarr1=dict(zip(keys,product))

    reviews=fetchallData('SELECT * FROM review WHERE productid = {0} ORDER BY buyerid'.format(product_id))
    # print(reviews)
    # print('reviews length is ',len(reviews))
    reviews1,revidarr,revinfo=[],[],[]
    totrev,avgrev,revlen,favgrev=0,0.0,0,0
    slrid={'revid':[],'buyerid':[],'review':[],'rkey':{}} #1,8
    if len(reviews)>0: 
        for i in range(len(reviews)):
            if reviews[i][7]=='buyer':
                reviews1.append(reviews[i])
                revidarr.append(reviews[i][8])
                # print(i,revidarr)
                totrev+=reviews[i][2]
                revlen+=1
            elif reviews[i][7]=='seller':
                    slrid['revid'].append(i)
                    slrid['buyerid'].append(reviews[i][8])
                    slrid['review'].append(reviews[i][3])
                    slrid['rkey'][reviews[i][8]]=reviews[i][3]
        avgrev=totrev/revlen
        favgrev= math.floor(avgrev)
        revinfo=fetchallData('SELECT firstname,lastname,email,profile from users WHERE buyerid IN ({0}) '.format(','.join(map(str,revidarr))))            
        # print(revinfo)
        # print(len(revinfo))
    return render_template("product.html",user_data=user_data,imgdata=imgdata,count=len(product),proddata=dictarr1,qtymax=qtymax,reviews=reviews1,slrid=slrid,revinfo=revinfo,avgrev=avgrev,favgrev=favgrev,sellerinfo2=sellerinfo,defaultImg=defaultImg)
    
@buyer_page.route("/prod/buy",methods=['POST'])
@verify_role('buyer')
def buyprod():
    req=request.get_json()
    # print(req['productid'])
    return jsonify({'status_code':200,'message':'success'})

@buyer_page.route("/deleteAccount",methods=['DELETE'])
@verify_role('buyer')
def deleteAcc():
    user_data=session.get('user',{}).get('data')
    if user_data[-1] is not None:
        deleteImg(user_data[-1])#deleting user Profile Image from cloudinary
    values=(None,None,None,None,None,None,None,1,user_data[0])
    update_logs=updateOrDelete('UPDATE users set firstname = %s,lastname = %s,password = %s,phone = %s,address=%s,profile=%s,profileId=%s,isdeleted=%s  WHERE buyerid= %s',values,True)
    if update_logs is True:
        return jsonify({'status_code':200,'message':'success'})
    return jsonify({'status_code':400,'message':'Account deletion failed'})