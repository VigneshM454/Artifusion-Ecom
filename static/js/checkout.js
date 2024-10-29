const productname=document.getElementById("productname");
const productprice=document.getElementById('productprice');
const changeaddr=document.getElementById("changeaddr");
const addr=document.getElementById('addr');
const bill=document.getElementById('bill')

const subtotal=document.getElementById('subtotal');
const tax=document.getElementById('tax');
const total=document.getElementById('total');

const payform=document.getElementById('form');
payform.style.display='none'
//const placeorder=document.getElementById('placeorder')

const params=new URLSearchParams(window.location.search);
const encodeddata=params.get('data');

function showcheckout(data123,dataobj){
  let stot=0
  if(data123 && dataobj){
      var datajs1=JSON.parse(data123)
      var dataobj1= typeof dataobj=='string'? JSON.parse(dataobj):dataobj
      //console.log(datajs1);
      //console.log(dataobj1);
      datajs1.forEach((d,i)=>{
          //dataarr.push(d)
          const pname=document.createElement('p');
          const pprice=document.createElement('p');
          const prodimage=document.createElement('img')
          const productdiv=document.createElement('div')
          //console.log(data);
          var qty= parseInt(dataobj1[d.productid]);
          //console.log( qty);
          var price=d.prodprice;
          prodqtarr.push(qty)
          prodidarr.push(d.productid)                
          //console.log(typeof d.prodprice);
          prodimage.src=d.prodimg1;
          prodimage.style.cssText='height:50px; width:50px; border-radius:10px; border:1px solid black;'
          pname.innerText=d.prodname+` ${'('+price +' x '+ qty +')'}`;
          pname.classList.add('m-0')
          var pp=price*qty;
          pprice.innerText='₹'+pp;
          pprice.classList.add('m-0','py-3')
          pprice.style.cssText='line-height:40px;'
          productdiv.append(prodimage,pname)
          productdiv.classList.add('d-flex','align-items-center','gap-4','py-3')
          productname.append(productdiv);
          proddetailarr.push(pname.innerText)
          productprice.append(pprice)
          stot+=pp
          prodpricearr.push(pp+pp*0.1)
      })
   
      //console.log(stot);
      subtotal.innerText='₹'+stot;
      tax.innerText='₹'+(stot*0.1)
      var x=(stot)+(stot*0.1)
      total.innerText='₹'+x
      proddetail['totamt']=x
      proddetail['proddetailarr']=proddetailarr;
      proddetail['prodqtarr']=prodqtarr
      proddetail['prodidarr']=prodidarr
      proddetail['prodpricearr']=prodpricearr
      //console.log(proddetail);
  }else{
    displayToast('data not receveid','danger');
  }    
}
let data;
//let dataarr=[];
//prodid, buyerid,shipadd,paymethod,totamt,
//proddetail-> prod name,price(id),quantity
//let prodnamearr=[]
let proddetailarr=[]
let proddetail={} 
let prodidarr=[],prodpricearr=[],prodqtarr=[]
//console.log(encodeddata);
if(encodeddata){
    data=JSON.parse(decodeURIComponent(encodeddata))
    //console.log(data);
    object1=data
    //dataarr.push(data)
    fetch(`${window.origin}/buyer/product/checkout`,{
      method:"POST",
      headers:{
        "content-Type":"application/json",
      },body:JSON.stringify(object1),
    })
    .then(response=>response.json())
    .then((data)=>{
      if(data.status_code==200){
          //console.log('from product page whose val is ');
          showcheckout(data.js,data.object)
      }else{
        displayToast('Some error has occured'+data.status_code,'danger')
      }
    }).catch(error=>displayToast('Some error has occured'+data.status_code,'danger'))
}

else{
    let demotxt='hackylazy'
    fetch(`${window.origin}/buyer/checkout/123`,{
        method:"POST",
        headers:{
          "content-Type":"application/json",
        },
        body:JSON.stringify(demotxt),
      })
      .then(response=>response.json())
      .then(data=>{
        if(data.status_code==200){
            showcheckout(data.js,data.object)
        }else if(data.status_code==454){
          wishtable.innerHTML=`<h1>YOU have no products in your wishlit</h1>`;
        }else{
          displayToast('Some error occured','danger')
          window.location.href='/buyer/cart'
        } 
      }).catch(error=>displayToast("Some error occured",'danger'))
}

function placeorder(){
  //console.log('in placeorder');
  let demotxt='hackylazy'
  fetch(`${window.origin}/buyer/checkout/buy`,{
      method:"POST",
      headers:{
        "content-Type":"application/json",
      },
      body:JSON.stringify(proddetail),
    })
    .then(response=>response.json())
    .then(data=>{
      if(data.status_code==200){
        window.location.href='/buyer/order'
        displayToast("Your order has been placed",'success')
      }else{
        window.location.href='/buyer/cart'
        displayToast('Some error has occured','danger')
      }
    }).catch(error=>console.log(err))
}

const orderbtn=document.getElementById('placeorder');
orderbtn.addEventListener('click',()=>{
    let paynow =document.getElementById('pn');
    let payonDeliv=document.getElementById('pd');
    //console.log(addr.textContent);
    var d=new Date()
    //d.setMinutes(d.getMinutes() - currentUtcDatetime.getTimezoneOffset())
    proddetail['ordertime']=d
    proddetail['shipaddr']=addr.textContent
    if(paynow.checked){
        //console.log('you are redirected to payment page')
        payform.style.display='flex';
        orderbtn.classList.add('disabled')
        paynow.classList.add('disabled')
        payonDeliv.classList.add('disabled')
        proddetail['paymethod']="payonorder"
    }
    if(payonDeliv.checked){
        payform.style.display='none'
        proddetail['paymethod']="payondelivery"
        //console.log('your order has been placed , you can pay when you receive the product')
        placeorder()
        //window.location.href='/buyer'
    }
    //console.log(proddetail);
    //console.log(proddetailarr);
})

changeaddr.addEventListener('click',()=>{
    addr.setAttribute("contenteditable",'true');
    let contedit;
    let contdiv;
    function createUpdAddr(){
      contdiv=document.createElement('div')
      contdiv.classList.add('row', 'm-0' ,'d-flex', 'align-items-center' ,'justify-content-center')
      contedit= document.createElement('button');
      contedit.innerText="Update Address"
      contedit.classList.add('btn' ,'mt-3','bg-header','text-white');
      contedit.id='updateaddr';
      contdiv.append(contedit)
      bill.append(contdiv)  
    }
    document.getElementById('updateaddr') ?{}:createUpdAddr()
    
    let upaddr=document.querySelector('#updateaddr');
    upaddr.addEventListener('click',()=>{
        addr.setAttribute("contenteditable",'false');
        contedit.remove()
    })

})

let v=0;

function validatepay(){
  placeorder()
}
