from flask import Blueprint, Flask,render_template,request,jsonify,make_response,redirect,url_for ,session,flash
import math
from functions import *
from cloudinary1 import storeImg,deleteImg

seller_page=Blueprint(
    "artifusion/seller",__name__,static_folder="static",
    template_folder="templates")

@seller_page.route("/home")
@verify_role('seller')
def sellerhome():
    user_data= session.get('user',{}).get('data')
    # print(user_data)
    sellerid=user_data[0]
    prodscount,countorders,totamt=0,0,0
    paymethod_data,prodlabelarr,prodsalearr,prodqtarr=[],[],[],[]
    prodscount=getcount('SELECT COUNT(*) FROM products1 WHERE sellerid= {0} and isdeleted= 0'.format(sellerid))
    # print('prodscount',prodscount)
    topselprod={'ProdName':[],'ProdPrice':[],'QuantitySold':[],'ProdImg':[],'QuantityListed':[]}
    #totprod=0
    if prodscount>0:
        pdarr=fetchallData('SELECT productid,prodname,prodimg1,qtysold,prodprice,qtyavail FROM products1 WHERE sellerid ={0} and isdeleted= 0 ORDER BY qtysold DESC'.format(sellerid))
        # print(pdarr)
        pdarr1=[]
        prodlabelarr=[]
        for i in pdarr:
            # print(i[3])
            prodlabelarr.append(i[1])
            pdarr1.append(i[0])
            #totprod+=i[3]+i[5]
            if i[3]>0:
                topselprod['ProdName'].append(i[1])
                topselprod['ProdPrice'].append(i[4])
                topselprod['QuantitySold'].append(i[3])
                topselprod['ProdImg'].append(i[2])
                topselprod['QuantityListed'].append(i[3]+i[5])
        # print(pdarr1)
        #print(topselprod)
        # print(len(topselprod['ProdName']))
        count1=fetchallData('SELECT productid,totamt,paymethod,orderqty FROM demoorders WHERE productid IN  {0} ORDER BY productid'.format(tuple(pdarr1)))
        count=[]
        tupletolist(count1,count)
        tot,totpayonorder,totpayondelivery,prod_tot_rel=0,0,0,[]
        for i in range(len(count)):
            b=count[i][1]
            # print(b)
            tot+=(b-(b*0.1))
            # print("paymethod is ",count[i][2])
            if count[i][2]=='payonorder':
                totpayonorder+=(b-(b*0.1))
            if count[i][2]=='payondelivery':
                totpayondelivery+=(b-(b*0.1))                                
            if i==0:
                prod_tot_rel.append(count[i])
            if i>0 and count[i][0]==count[i-1][0]:
                prod_tot_rel[len(prod_tot_rel)-1][1]+=count[i][1]
                prod_tot_rel[len(prod_tot_rel)-1][3]+=count[i][3]
            if i>0 and count[i][0]!=count[i-1][0]:
                prod_tot_rel.append(count[i])
        
        # print(prod_tot_rel)   
        prodsalearr=[]
        prodqtarr=[]
        for i in prod_tot_rel:
            prodsalearr.append(i[1]-(i[1]*0.1))
            prodqtarr.append(i[3])
        # print('prodqt arr is ')
        # print(prodqtarr)
        paymethod_data=[totpayondelivery,totpayonorder]    
        # print('total amt = ',tot)
        totamt='₹'+str(tot)
        # print('tot amt on order = ',totpayonorder)
        # print('tot amt on delivrty = ',totpayondelivery)
        countorders=len(count)
        # print('countorders = ',countorders)    
    imgdata=user_data[-3] if  user_data[-3] is not None else 'https://res.cloudinary.com/dq67ufqzg/image/upload/v1728570558/w58iymkranlgvoxknibj.svg'    
    return render_template("sellerhome.html",user_data=user_data,imgdata=imgdata,countorders=countorders,totamt=totamt,prodscount=prodscount,paymethod_data=paymethod_data,prodlabel=prodlabelarr,prodsalearr=prodsalearr,prodqtarr=prodqtarr,topselprod=topselprod)

@seller_page.route("/order")
@verify_role('seller')
def order():
    user_data= session.get('user',{}).get('data')
    sellerid=user_data[0]
    pdarr=fetchallData('SELECT productid FROM products1 WHERE sellerid ={0}'.format(sellerid))
    isempty=True
    # print('len of pdarr is :')
    # print(len(pdarr))
    imgdata=user_data[-3] if  user_data[-3] is not None else 'https://res.cloudinary.com/dq67ufqzg/image/upload/v1728570558/w58iymkranlgvoxknibj.svg'
    if len(pdarr)!=0:
        pdarr1=[p[0] for p in pdarr]
        # print(pdarr1)
        orderdata=fetchallData('SELECT buyerid,productid,shipping_addr,proddetail,totamt,paymethod,orderstatus,orderdate FROM demoorders WHERE productid IN  {0}'.format(tuple(pdarr1)))
        if len(orderdata)>0:
            isempty=False
        a=math.ceil(len(orderdata)/5)
        pagearr=[i for i in range(a)]
        return render_template("sellorders.html",user_data=user_data,imgdata=imgdata,isempty=isempty,orderdata=orderdata,a=a,pagearr=pagearr)
    else:
        return render_template("sellorders.html",user_data=user_data,imgdata=imgdata,isempty=isempty)

@seller_page.route("/products")
@verify_role('seller')
def products():
    user_data= session.get('user',{}).get('data')
    imgdata=user_data[-3] if  user_data[-3] is not None else 'https://res.cloudinary.com/dq67ufqzg/image/upload/v1728570558/w58iymkranlgvoxknibj.svg'
    if not user_data:
        return redirect('/')
    sellerid=user_data[0]
    prodqtarr=fetchallData('SELECT productid,qtysold FROM products1 WHERE sellerid ={0} and isdeleted = 0 ORDER BY qtysold DESC'.format(sellerid))
    # print(prodqtarr)
    Qtysold=0
    for i in range(len(prodqtarr)):
        if prodqtarr[i][1]>0:
            Qtysold+=prodqtarr[i][1]
    # print(Qtysold)
    c=getcount('SELECT COUNT(*) FROM products1 WHERE sellerid= {0} and isdeleted= 0'.format(sellerid))
    sellerProd={'ProdName':[],'ProdPrice':[],'QuantitySold':[],'ProdImg':[],'QuantityListed':[],'ProdDesc':[],'ProdId':[]}
    a=0
    pagearr=[]
    totprodlisted=0

    if c>0:
        pdarr=fetchallData(('SELECT productid,prodname,prodimg1,qtysold,prodprice,qtyavail,proddesc FROM products1 WHERE sellerid ={0} and isdeleted= 0 ORDER BY qtysold DESC'.format(sellerid)))
        pdarr1=[]
        for i in pdarr:
            # print('qty sold is -------------------')
            # print(i[3])
            #prodlabelarr.append(i[1])
            pdarr1.append(i[0])
            #totprod+=i[3]+i[5]
            sellerProd['ProdId'].append(i[0])
            sellerProd['ProdName'].append(i[1])
            sellerProd['ProdPrice'].append(i[4])
            sellerProd['QuantitySold'].append(i[3])
            sellerProd['ProdImg'].append(i[2])
            sellerProd['QuantityListed'].append(i[3]+i[5])
            totprodlisted+=i[3]+i[5]
            sellerProd['ProdDesc'].append(i[6])
        #print(pdarr1)
        # print(len(sellerProd['ProdName']))
        a=math.ceil(len(sellerProd['ProdName'])/5)
        # print(a)
        pagearr=[i for i in range(a)]
    return render_template("sellproducts.html",user_data=user_data,imgdata=imgdata,Qtysold=Qtysold,sellerProd=sellerProd,a=a,pagearr=pagearr,totprodlisted=totprodlisted)

@seller_page.route("/addMoreQty",methods=['POST'])
@verify_role('seller')
def addmoreqty():
    # print("hi hello welcome")
    req=request.get_json()
    if req:
        user_data= session.get('user',{}).get('data')
        # print(req)
        # print(type(req['pid']))
        # print(req['pqty'])
        a=fetchoneData('SELECT qtyavail FROM products1 WHERE productid= {0} AND sellerid = {1}'.format(req['pid'],user_data[0]))
        newqty=req['pqty']+a[0]
        update_logs=updateOrDelete(("UPDATE products1 SET qtyavail = {0} WHERE productid = {1}".format(newqty,req['pid'])),None,True)
        if update_logs is True:
            return {'status_code':200}
        return {'status_code':404}

@seller_page.route("/products/create-new",methods=['POST'])
@verify_role('seller')
def createnewprod():
    # print(request)
    # print(request.files)
    # print(request.form)
    if(request):
        if 'img1' not in request.files or 'img2' not in request.files or 'img3' not in request.files:
            return jsonify({'status_code': 500, 'imgdata':''})

        img1,imgId1=storeImg(request.files['img1'])
        img2,imgId2=storeImg(request.files['img2'])
        img3,imgId3=storeImg(request.files['img3'])
        pname,pprice,pdesc,pqty,prodcat=request.form.get('pname'),request.form.get('pprice'),request.form.get('pdesc'),request.form.get('pqty'),request.form.get('prodcat')
        user_data= session.get('user',{}).get('data')
        query="INSERT INTO products1  (prodname,prodprice,proddesc,qtyavail,qtysold,prodimg1,prodimg2,prodimg3,sellerid,category,imgId1,imgId2,imgId3) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values=(pname,pprice,pdesc,pqty,0,img1,img2,img3,user_data[0],prodcat,imgId1,imgId2,imgId3)
        insert_logs=insertData(query,values)
        if insert_logs is True:
            return jsonify({'status_code': 200, 'imgdata':'hello hi' })    
    # print('problem iruku')
    return jsonify({'status_code': 500, 'imgdata':''})
   
@seller_page.route("/review")
@verify_role('seller')
def review():
    user_data= session.get('user',{}).get('data')
    imgdata=user_data[-3] if  user_data[-3] is not None else 'https://res.cloudinary.com/dq67ufqzg/image/upload/v1728570558/w58iymkranlgvoxknibj.svg'
    return render_template("sellreview.html",user_data=user_data,imgdata=imgdata)

@seller_page.route("/userprofile")
@verify_role('seller')
def sellerprofile():
    user_data=session.get('user',{}).get('data')
    imgdata=user_data[-3] if  user_data[-3] is not None else 'https://res.cloudinary.com/dq67ufqzg/image/upload/v1728570558/w58iymkranlgvoxknibj.svg'    
    return render_template("sellerprofile.html",user_data=user_data,imgdata=imgdata)

@seller_page.route("/userprofile/edit",methods=['POST'])
@verify_role('seller')
def editsprof():
    user_data=session.get('user',{}).get('data')
    # print(request.files)
    # print(request.form)
    if(request):
        if 'file' in request.files:
            fname,lname,phone,addr,pwd,shop=request.form.get('fname'),request.form.get('lname'),request.form.get('phone'),request.form.get('addr'),request.form.get('pwd'),request.form.get('shop')
            image=request.files.get('file')
            secureUrl,imgId=storeImg(image)
            if user_data[-1]:
                deleteImg(user_data[-1])
            query=''
            values=()
            if pwd=='':
                query="UPDATE sellers SET firstname = %s,lastname = %s,phone = %s,address = %s,shopname=%s,profile = %s,profileId=%s   WHERE email= %s"
                values=(fname,lname,phone,addr,shop,secureUrl,imgId ,user_data[4])
            else:
                query="UPDATE sellers SET firstname = %s,lastname = %s,phone = %s,address = %s,password = %s,shopname=%s,profile = %s,profileId=%s   WHERE email= %s"
                values=(fname,lname,phone,addr,pwd,shop,secureUrl,imgId,user_data[4])
            update_logs=updateOrDelete(query,values,True)
   
            if update_logs is True:
                session['user']={'data':getdata('seller',user_data[4]),'role':'seller'}
                session.permanent=True
                user_data=session.get('user',{}).get('data')
                return ({'status_code': 200, 'imgdata': 'hi'})
        print('problem iruku')
        return ({'status_code': 500, 'imgdata':''})   

@seller_page.route("/review/<int:product_id>")
@verify_role('seller')
def product(product_id):
    user_data=session.get('user',{}).get('data')
    # print(user_data[0])
    reviews=fetchallData('SELECT * FROM review WHERE productid = {0}   ORDER BY buyerid'.format(product_id))
    # print(reviews)
    reviews1=[]
    reviews2=[]
    revidarr=[]
    revidarr2=()
    totrev=0
    avgrev=0.0
    favgrev=0
    revinfo=[]
    slrid={'revid':[],'buyerid':[],'review':[],'rkey':{}}
    #1,8
    if len(reviews)>0: 
        l=0
        for i in range(len(reviews)):
            if reviews[i][7]=='buyer':
                reviews1.append(reviews[i])
                revidarr.append(reviews[i][8])
                # print(i,revidarr)
                totrev+=reviews[i][2]
                l+=1
            elif reviews[i][7]=='seller':
                # print("seller spotted")
                slrid['revid'].append(i)
                slrid['buyerid'].append(reviews[i][8])
                slrid['review'].append(reviews[i][3])
                slrid['rkey'][reviews[i][8]]=reviews[i][3]
        avgrev=totrev/l
        favgrev= math.floor(avgrev)
        
        revinfo=fetchallData('SELECT firstname,lastname,email,profile from users WHERE buyerid IN ({0}) '.format(','.join(map(str,revidarr))))        
        # print(len(revinfo))
    imgdata=user_data[-3] if  user_data[-3] is not None else 'https://res.cloudinary.com/dq67ufqzg/image/upload/v1728570558/w58iymkranlgvoxknibj.svg'        
    defaultImg='https://res.cloudinary.com/dq67ufqzg/image/upload/v1728570558/w58iymkranlgvoxknibj.svg'
    return render_template("sellreview.html",defaultImg=defaultImg,user_data=user_data,imgdata=imgdata,reviews=reviews1,slrid=slrid,revinfo=revinfo,avgrev=avgrev,favgrev=favgrev)

@seller_page.route('/review/reply',methods=['POST'])
@verify_role('seller')
def sendreply():
    user_data=session.get('user',{}).get('data')
    req=request.get_json()
    if req:
        # print(req)
        rdetails=fetchoneData('SELECT productid,buyerid FROM review WHERE reviewid = {0}'.format(req['revid']))
        count=0
        if len(rdetails)!=0:
            count=getcount('SELECT COUNT(*) FROM review WHERE productid = {0} and buyerid = {1}'.format(rdetails[0],rdetails[1]))
        if count==1:
            insert_logs=insertData('INSERT INTO review (productid,reviewtext,reviewtype,usertype,buyerid,sellerid) VALUES(%s,%s,%s,%s,%s,%s)',(rdetails[0],req['reply'],'reply','seller',rdetails[1],user_data[0]))
            return {'status_code':200} if insert_logs else {'status_code':300}
        else:
            return{'status_code':404}

@seller_page.route('/deleteProd',methods=['DELETE'])
@verify_role('seller')
def sdeleteProd():
    user_data=session.get('user',{}).get('data')
    req=request.get_json()
    prodData=fetchoneData('SELECT imgId1,imgId2,imgId3 FROM products1 WHERE productid={} and sellerid= {}'.format(req['prodId'],user_data[0]))
    if prodData:#perfrom prod deletion
        res=deleteProd(prodData,req['prodId'])
        return jsonify(res)
    return jsonify({'status_code':400,'message':'No such product exist'})

@seller_page.route('/deleteAccount',methods=['DELETE'])
@verify_role('seller')
def deleteSellerAcc():
    user_data=session.get('user',{}).get('data')
    res=delSellerData(user_data,False)
    return jsonify(res)
