from flask import Blueprint, Flask,render_template,request,jsonify,make_response,redirect,url_for ,session,flash
from functions import *
from cloudinary1 import storeImg,deleteImg
import math
admin_page=Blueprint(
    "artifusion/admin",__name__,static_folder="static",
    template_folder="templates")

@admin_page.route("/order")
@verify_role('admin')
def aorder():
    user_data= session.get('user',{}).get('data')
    ordertable=fetchallData('SELECT orderid, buyerid,shipping_addr,orderstatus,orderdate,proddetail,totamt,paymethod FROM demoorders ')    
    a=math.ceil(len(ordertable)/5)
    pagearr=[i for i in range(a)]
    print(pagearr)
    imgdata=user_data[-2] if  user_data[-2] is not None else 'https://res.cloudinary.com/dq67ufqzg/image/upload/v1728570558/w58iymkranlgvoxknibj.svg'
    return render_template("adminorder.html",ordertable=ordertable,user_data=user_data,imgdata=imgdata,a=a,pagearr=pagearr)

@admin_page.route("/product")
@verify_role('admin')
def aprod():
    user_data= session.get('user',{}).get('data')
    prodtable=fetchallData('SELECT prodimg1,prodname,prodprice,proddesc,qtyavail,sellerid,productid,qtysold FROM products1')
    prodtable1=[]
    tupletolist(prodtable,prodtable1)
    for i in range(len(prodtable1)):
        #4=4+7 qty=qtyavail+qtysold
        prodtable1[i][4]=prodtable1[i][4]+prodtable1[i][7]
    a=math.ceil(len(prodtable)/5)
    print(a)
    pagearr=[i for i in range(a)]
    print(pagearr)
    imgdata=user_data[-2] if  user_data[-2] is not None else 'https://res.cloudinary.com/dq67ufqzg/image/upload/v1728570558/w58iymkranlgvoxknibj.svg'
    return render_template("adminprod.html",prodtable=prodtable1,user_data=user_data,imgdata=imgdata,a=a,pagearr=pagearr)
   
@admin_page.route("/buyer")
@verify_role('admin')
def abuyer():
    user_data= session.get('user',{}).get('data')
    buyertable=fetchallData('SELECT * from users')    
    a=math.ceil(len(buyertable)/5)
    pagearr=[i for i in range(a)]
    print(pagearr)
    imgdata=user_data[-2] if  user_data[-2] is not None else 'https://res.cloudinary.com/dq67ufqzg/image/upload/v1728570558/w58iymkranlgvoxknibj.svg'    
    defaultImg='https://res.cloudinary.com/dq67ufqzg/image/upload/v1728570558/w58iymkranlgvoxknibj.svg'
    return render_template("adminbuyer.html",buyertable1=buyertable,user_data=user_data,imgdata=imgdata,a=a,pagearr=pagearr,defaultImg=defaultImg)

@admin_page.route("/seller")
@verify_role('admin')
def aseller():
    user_data= session.get('user',{}).get('data')
    sellertable=fetchallData("SELECT profile,firstname,lastname,phone,email,address,shopname,sellerid from sellers")    
    a=math.ceil(len(sellertable)/5)
    print("......................................")
    print(a)
    pagearr=[i for i in range(a)]
    print(pagearr)
    imgdata=user_data[-2] if  user_data[-2] is not None else 'https://res.cloudinary.com/dq67ufqzg/image/upload/v1728570558/w58iymkranlgvoxknibj.svg'
    defaultImg='https://res.cloudinary.com/dq67ufqzg/image/upload/v1728570558/w58iymkranlgvoxknibj.svg'
    return render_template("adminseller.html",sellertable1=sellertable,user_data=user_data,imgdata=imgdata,a=a,pagearr=pagearr,defaultImg=defaultImg)

@admin_page.route("/home")
@verify_role('admin')
def ahome():
    user_data= session.get('user',{}).get('data')
    cat_dict={'jewel':'Jewellry','furn':'Furnitures','toys':'Toys','pottery':'Pottery','artwork':'ArtWork','homedecor':'HomeDecor'}
    print(user_data) 
    countData=fetchoneData("SELECT (SELECT COUNT(*) FROM demoorders) as OrdersCount, (SELECT COUNT(*) FROM users ) as UsersCount, (SELECT COUNT(*) FROM sellers) as SellersCount, (SELECT COUNT(*) FROM products1 ) as ProductCount ")
    print(countData)
    catdata=fetchallData("SELECT COUNT(*) as ProdCount, category FROM products1 group by category")
    category_label= [cat_dict[c[1]] for c in catdata]
    category_count=[c[0] for c in catdata]    
    sumdata=fetchoneData('SELECT SUM(totamt) from demoorders')[0]
    print(sumdata)
    tot=0
    if countData[0]>0: #order count   
        orderprice=fetchallData("SELECT totamt FROM demoorders ")
        for i in range(len(orderprice)):
            tot+=orderprice[i][0]
    countorders,totamt=0,0
    paymethod_data,prodlabelarr,prodsalearr,prodqtarr=[],[],[],[]
    topselprod={'ProdName':[],'ProdPrice':[],'QuantitySold':[],'ProdImg':[]}

    if countData[3] >0: #prod count
        pdarr=fetchallData('SELECT productid,prodname,prodimg1,qtysold,prodprice FROM products1  ORDER BY qtysold DESC')
        print(pdarr)
        pdarr1=[]
        prodlabelarr=[]
        for i in pdarr:
            print('qty sold is -------------------')
            print(i[3])
            prodlabelarr.append(i[1])
            pdarr1.append(i[0])
            if i[3]>0:
                topselprod['ProdName'].append(i[1])
                topselprod['ProdPrice'].append(i[4])
                topselprod['QuantitySold'].append(i[3])
                topselprod['ProdImg'].append(i[2])
        print(pdarr1)
        count1=fetchallData('SELECT productid,totamt,paymethod,orderqty FROM demoorders  ORDER BY productid')
        totpayonorder,totpayondelivery=0,0
        prod_tot_rel,prodsalearr,prodqtarr=[],[],[]

        if len(count1)>0:
            count=[]
            tupletolist(count1,count)
            print(count)
            tot=0
            for i in range(len(count)):
                b=count[i][1]
                print(b)
                tot+=(b-(b*0.1))
                print("paymethod is ",count[i][2])
                if count[i][2]=='payonorder':
                    totpayonorder+=(b-(b*0.1))
                elif count[i][2]=='payondelivery':
                    totpayondelivery+=(b-(b*0.1))                                
                if i==0:
                    prod_tot_rel.append(count[i])
                elif i>0 and count[i][0]==count[i-1][0]:
                    prod_tot_rel[len(prod_tot_rel)-1][1]+=count[i][1]
                    prod_tot_rel[len(prod_tot_rel)-1][3]+=count[i][3]
                elif i>0 and count[i][0]!=count[i-1][0]:
                    prod_tot_rel.append(count[i])            
            print('prodtot rel is ')
            print(prod_tot_rel)   
            prodsalearr=[ (i[1]-i[1]*0.1) for i in prod_tot_rel]
            prodqtarr=[ i[3] for i in prod_tot_rel]
            # for i in prod_tot_rel:
            #     prodsalearr.append(i[1]-(i[1]*0.1))
            #     prodqtarr.append(i[3])
            print('prodqt arr is ')
            print(prodqtarr)
        paymethod_data=[totpayondelivery,totpayonorder]    
        print('total amt = ',tot)
        totamt='₹'+str(tot)
        print('tot amt on order = ',totpayonorder)
        print('tot amt on delivrty = ',totpayondelivery)
        countorders=len(count)
        print('countorders = ',countorders)
    imgdata=user_data[-2] if  user_data[-2] is not None else 'https://res.cloudinary.com/dq67ufqzg/image/upload/v1728570558/w58iymkranlgvoxknibj.svg'
    return render_template("adminhome.html",user_data=user_data,imgdata=imgdata,countData=countData,tot=math.floor(tot),category_count=category_count,category_label=category_label,paymethod_data=paymethod_data,prodlabel=prodlabelarr,prodsalearr=prodsalearr,prodqtarr=prodqtarr,topselprod=topselprod)

@admin_page.route("/userprofile")
@verify_role('admin')
def adminprofile():
    user_data=session.get('user',{}).get('data')
    imgdata=user_data[-2] if  user_data[-2] is not None else 'https://res.cloudinary.com/dq67ufqzg/image/upload/v1728570558/w58iymkranlgvoxknibj.svg'
    return render_template("adminprofile.html",user_data=user_data,imgdata=imgdata)

@admin_page.route("/userprofile/edit",methods=['POST'])
@verify_role('admin')
def editsadminprof():
    user_data=session.get('user',{}).get('data')
    if(request):
        print(request.files)
        print(request.form)
        fname,lname,phone,pwd=request.form.get('fname'),request.form.get('lname'),request.form.get('phone'),request.form.get('pwd')
        image=request.files.get('file')
        secureUrl,imgId=None,None
        if image:
            secureUrl,imgId=storeImg(image)
            if user_data[-1]:
                deleteImg(user_data[-1])
        query=''
        values=()
        if pwd=='':
            query="UPDATE admin SET firstname = %s,lastname = %s,phone = %s,profile = %s,profileId=%s   WHERE email= %s"
            values=(fname,lname,phone,secureUrl,imgId,user_data[4])
        else:
            query="UPDATE admin SET firstname = %s,lastname = %s,phone = %s,password = %s,profile = %s,profileId= %s  WHERE email= %s"
            values=(fname,lname,phone,pwd,secureUrl,imgId,user_data[4])
        update_logs=updateOrDelete(query,values,True)
        if update_logs is True:   
            session['user']={'data':getdata('admin',user_data[4]),'role':'admin'}
            session.permanent=True
            user_data=session.get('user',{}).get('data')
            return jsonify({'status_code': 200, 'imgdata': 'hi'})
        return jsonify({'status_code': 400, 'imgdata': 'hi'})
    
@admin_page.route('/product-delete',methods=['DELETE'])
@verify_role('admin')
def aDelProd():
    print("hey entered delete pr5oduct")
    req=request.get_json()
    if not req['prodId']:
        return jsonify({'status_code': 400, 'imgdata': 'No such product exist'})
    prodData=fetchoneData('SELECT imgId1,imgId2,imgId3 FROM products1 WHERE productid={}'.format(req['prodId']))
    res=deleteProd(prodData,req['prodId'])
    if res['status_code']:
        ''
    print(res['status_code'])# if its ok then send a mail
    return jsonify(res)           
        
@admin_page.route('/seller-delete',methods=['DELETE'])
@verify_role('admin')
def aDelSeller():
    print("hey entered delete seller")
    req=request.get_json()
    if not req['userMail']:
        return jsonify({'status_code': 400, 'imgdata': 'No such product exist'})
    sellerData=getdata('seller',req['userMail'])
    print(sellerData)
    if sellerData:
        res=delSellerData(sellerData,True)
        print(res['status_code'])
        return jsonify(res)

@admin_page.route("/buyer-delete",methods=['DELETE'])
@verify_role('admin')
def removeBuyer():
    print("hey entered buyer-delete")
    req=request.get_json()
    userId=req['userId']
    print(type(userId))
    if userId:
        userData=fetchoneData('SELECT * FROM users WHERE buyerid = {}'.format(userId))
        print(userData)
        if userData:
            delete_logs=updateOrDelete('DELETE FROM users WHERE buyerid = {}'.format(userId))
            print(delete_logs)
            if delete_logs:
                return jsonify({'status_code': 200, 'imgdata': 'User Deleted successfully'})                
    return jsonify({'status_code': 400, 'imgdata': 'hi'})

    '''    
    #0- orderid, 1-buyerid, 2-productid, 3-shiping_addr
    #4- proddetail, 5- totamt, 6- paymethod, 7- orderstatus, 
    #8- orderdate, 9- sellerid  
    #return render_template("sellorders.html",user_data=user_data,imgdata=imgdata,orderdata=orderdata)
    '''    