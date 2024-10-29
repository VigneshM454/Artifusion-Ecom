const wishtable=document.querySelector('#wishtable')
const prodcontain=document.getElementById('products');
const prodcount=document.getElementsByName('prod-count')
const totalprice=document.getElementById('tot-price');
const buyAllbtn=document.getElementById('buyAll')

let data;
let pricearr=[];
let dataarr=[];

let idarr=[];
let qtarr=[]

function caltot(rqarr){
  //console.log('im called');
  //console.log(rqarr.length);
  let tot=0
  rqarr.forEach((elem,i)=>{
    var id= elem.id;  
    b=id.slice(2);
    //console.log('b '+b)
    //console.log('id = '+id);
    idarr.push(b);
    //console.log(idarr)
    var specific_qty=getVal(id);
    qtarr.push(specific_qty)
    //console.log(qtarr)
    tot+=qtarr[i]*pricearr[i]
    //console.log(tot)
  })
  totalprice.innerText='₹'+tot
}

function saveForLater(i){
    //console.log(i);
    var id={'productid':i}

    fetch(`${window.origin}/buyer/cart/later`,{
        method:"POST",
        headers:{
          "content-Type":"application/json",
        },
        body:JSON.stringify(id),
      })
      .then(response=>response.json())
      .then(data=>{
        if(data.status_code==200){
            //console.log(data.js);
            location.reload()
            displayToast('Saved for later successfully!','info')

        }else{
          displayToast('Some error has occured, try again later','danger')
          // displayToast('Some error has occured, try again later','danger')
        }
      })
      .catch(error=>displayToast("Some error in adding cart item to wishlist ","danger"))
}

function deleteItem(i){
    var id={"productid":i}
    fetch(`${window.origin}/buyer/cart/remove`,{
        method:"POST",
        headers:{
          "content-Type":"application/json",
        },
        body:JSON.stringify(id),
      })
      .then(response=>response.json())
      .then(data=>{
        if(data.status_code==200){
            //console.log(data.js);
            displayToast('Removed from cart successfully!','success')
            location.reload()
        }else{
          displayToast('Some error has occured, try again later','danger')
        }
      })
      .catch(error=>displayToast("error da ",'danger'))
}

buyAllbtn.addEventListener('click',()=>{
  //console.log('cart to buy clicked')
  let reqarr=document.querySelectorAll('.req-qt');
  //console.log(reqarr);
  if(reqarr.length==0){
    displayToast('Please add some items to cart to buy','warning')
  }
  let object={}
  reqarr.forEach((r,i)=>{
    var id= r.id;
    b=id.slice(2);
    //console.log('id = '+id);
    idarr.push(b);
    var specific_qty=getVal(id);
    qtarr.push(specific_qty);
    object[b]=specific_qty
  })
  //console.log(idarr);
  //console.log(qtarr);
  //console.log(object);

  fetch(`${window.origin}/buyer/cart/checkout`,{
    method:"POST",
    headers:{
      "content-Type":"application/json",
    },
    body:JSON.stringify(object),
  })

  .then(response=>response.json())
  .then((data)=>{    
    //console.log(data);
    if(data.status_code==200){
        window.location.href='/buyer/checkout'        
    }else if(data.status_code==404){
     displayToast('no product is present in cart','warning')
   }else{
      displayToast('some error has occured'+data.status_code,'danger')
    }
  })
  .catch(error=>console.log(error))
})

function buy(data,id ){
  event.preventDefault();
  //console.log('Hey buy clicked ______________________________')
  b=id.slice(2);
  idarr.push(b)
  var orderqty=getVal(id)
  //console.log("orderqty");
  //console.log(orderqty);
  data['orderqty']=orderqty;
  //var orderqty=parseInt(prodqt.textContent);
  let object1={}
  object1['pid']=b
  object1['pqty']=orderqty
  //console.log(object1);
  const encode2=encodeURIComponent(JSON.stringify(object1));
  window.location.href=`/buyer/checkout?data=${encode2}`;
}

function getVal(id){
  var a=document.getElementById(id);
  return parseInt(a.innerText)
}

function add_prod(id,max){
  let reqarr1=document.querySelectorAll('.req-qt');
  //console.log("addprod pressed");
  var a=document.getElementById(id);
  var q=parseInt(a.innerText);
  if(q<max){
    q++;
    a.innerText=q;
  }
  caltot(reqarr1)
}
function sub_prod(element){
  let reqarr1=document.querySelectorAll('.req-qt');
  //console.log("subprod pressed")
  var a=document.getElementById(element)
  var q=parseInt(a.innerText);
  if(q>1){
    q--;
    a.innerText=q;
  }
  caltot(reqarr1)
}

function createdropItems(quantity) {
    let dropdownContent = '';
    for (let i = 0; i <= quantity; i++) {
        dropdownContent += `<li><a class="dropdown-item qty-dd" onclick="cartqty(${i})" href="#" id=${i}>${i}</a></li>`;
    }
    return dropdownContent;
}

function cartqty(i){
    const ddbtn=document.getElementById("dropdownMenuButton")
    ddbtn.innerText="Quantity : "+i
}

window.onload=()=>{
  fetch(`${window.origin}/buyer/cart`,{
      method:"POST",
      headers:{
        "content-Type":"application/json",
      },
      body:JSON.stringify("hi"),
    })
    .then(response=>response.json())
    .then((data)=>{
      //console.log(data);
      if(data.status_code==200 && data.js!==null){
            let data123=JSON.parse(data.js)
              //console.log(data123);
              prodcount.forEach((p)=> p.innerText=data123.length)//
              data123.forEach((d,i)=>{
                d.proddesc=d.prodimg2=d.prodimg3=''
                //console.log(d);
                pricearr.push(d.prodprice)
                let product=document.createElement('div');
                let line=document.createElement('hr')
                line.classList.add("text-light")
                product.classList.add("row","mx-0",'my-2','d-flex','align-items-center','justify-content-start')
                product.innerHTML= `
                  <div class="col-12 col-lg-3 col-md-3 d-flex align-items-center justify-content-center">
                      <img src="${d.prodimg1}" style="width: 160px; height: 160px; border-radius: 25px;">
                  </div>
                  <div class="col-9 col-lg-9 col-md-9 p-1 d-flex flex-column align-items-start justify-content-center">
                      <h3 class="my-2" style="text-decoration:underline; text-align:center">${d.prodname}</h3>
                      <h1 class='my-2'>${'₹'+d.prodprice}/-</h1>

                      <div class="d-flex  ">
                        <h4 >Quantity : </h4> 
                        <div  class="mx-2 d-flex flex-row">
                          <button class="btn btn-light" id="subbtn" onclick="sub_prod('qt${d.productid}' )" >-</button>
                          <span id="qt${d.productid}" class="p-2 req-qt">1</span>
                          <button class="btn btn-light" id="addbtn" onclick="add_prod('qt${d.productid}',${d.qtyavail})" >+</button>
                        </div>    
                      </div>
                      <br/>
                      <div class="cartopt dropdown col d-flex flex-wrap  col-lg-8 col-md-10 col-12 gap-1" style="min-width:260px;">
                        <button id="buyBtn" class="btn col btn-outline-dark" onclick='buy( ${JSON.stringify(d)},"qt${d.productid}" )'>Buy</button>
                        <div class=" vlcol"> <div class="vertical-line"></div> </div>
                        <button id="deleteBtn" class="btn col btn-outline-dark" onclick="deleteItem(${d.productid})">Delete</button>
                        <div class=" vlcol"> <div class="vertical-line"></div> </div>
                        <button id="saveBtn" class="btn btn-outline-dark col" onclick="saveForLater(${d.productid})">Save for later</button>
                        <div class=" vlcol"> <div class="vertical-line"></div> </div>
                      </div>
                    </div>`
                let tot=0;
                pricearr.forEach((elem,i)=>{
                  tot+=elem;
                })
                totalprice.innerText='₹'+tot;
                prodcontain.append(product,line)  // caltot()
              })
              let reqarr1=document.querySelectorAll('.req-qt');
              caltot(reqarr1) //  }
      }else{
        document.getElementById('scart').style.display='none'
        document.getElementById('tcart').style.display='none'
        prodcontain.innerHTML=` <div class="p-3 mt-5 d-flex align-items-center justify-content-center text-center h1 text-color">Cart is empty!</div>`
     }
    })
    .catch(error=>displayToast("Some error occured",'danger'))
}
