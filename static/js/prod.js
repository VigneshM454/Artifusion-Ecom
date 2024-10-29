const dynprod=document.getElementById('dynprod');
const params=new URLSearchParams(window.location.search);
const encodeddata=params.get('data');
//console.log(encodeddata);
let data;
let data1;
const prodqt=document.getElementById('qt')
const qtymax=document.getElementById('qty-max').value;
const writereview=document.getElementById('writerev')
const revform=document.getElementById('revform')
function add_prod(){
  let i=parseInt(prodqt.textContent);
  if(i<parseInt(qtymax)){
    i++;
    prodqt.innerText=i;   
  }
}
function sub_prod(){
  let i=parseInt(prodqt.textContent);
  if(i>1){
    i--;
    prodqt.innerText=i; 
  }     
}
let prodname =document.getElementById('prodname').textContent;
let prodprice =document.getElementById('prodprice').value;
let prodimg1 =document.getElementById('img1').src;
let prodid=document.getElementById('prod-id').value
const pb={
  'productid':prodid,
  'prodname':prodname,
  'prodprice':prodprice,
  'qtyavail':qtymax,
  'prodimg1':prodimg1,
}


const addcart=document.getElementById('addcart')
const buynow=document.getElementById('buynow')
const wish=document.getElementById('addwish')
        
addcart.addEventListener('click',()=>{
   event.preventDefault();
    if(qtymax>0){
      //alert('add to cart')
      ////console.log(data);
      fetch(`${window.origin}/buyer/prod/cart`,{
        method:"POST",
        headers:{
          "content-Type":"application/json",
        },
        body:JSON.stringify(pb),
      })
      .then(response=>response.json())
      .then(data=>{
        if(data.status_code==200){
          displayToast('Added to cart successfully','success')
          window.location.href='/buyer/'
        }else if(data.status_code==300){
          displayToast('Product is already in cart','warning')
        }else{
          displayToast('Some error has occured'+data.status_code,'danger')
        } 
      }).catch(error=>{
        displayToast('Some error has occured'+data.status_code,'danger')
      })
    }else{
      displayToast('Sorry this product have been sold out, please check again later','info')
    }
  })
  

  wish.addEventListener('click',()=>{
    event.preventDefault();
    // alert('add to wishlist')
    //console.log(pb);
    fetch(`${window.origin}/buyer/prod/wish`,{
     method:"POST",
     headers:{
       "content-Type":"application/json",
     },
     body:JSON.stringify(pb),
    })
   .then(response=>response.json())
   .then(data=>{
      if(data.status_code==200){
        displayToast('Product added to wishlist','success')
        window.location.href='/buyer/'
      }else if(data.status_code==300){
        displayToast('Product already in cart or wishlist','warning')
      }else{
        displayToast('Some error has occured'+data.status_code,'danger')
      }
   }).catch(error=>{
    displayToast('Some error has occured'+data.status_code,'danger')
  })
     // window.location.href=`wishlist?data=${encodeddata}`;
  })

writereview.addEventListener('click',()=>{
  //product/checkrev
  let produrl=window.location.pathname
  let prodid=parseInt(produrl.replace('/buyer/product/',''))
  //console.log(prodid);
  //alert(prodid)
  
  fetch(`${window.origin}/buyer/product/checkrev`,{
    method:"POST",
    headers:{
      "content-Type":"application/json",
    },
    body:JSON.stringify(prodid),
  })
  .then(response=>response.json())
  .then(data=>{
    //console.log(data.status_code);
    if(data.status_code==200){
      //console.log('eligible to add review')
      revform.classList.remove('hide')
      revform.classList.add('show')
      const addrev=document.getElementById('addrev')
      addrev.addEventListener('submit',()=>{
        event.preventDefault()
        //console.log('hi ');
        const revdesc=document.getElementById('revdesc').value
        const revrating=document.getElementById('revrating').value
        //console.log(typeof revrating);
        //console.log(revdesc)
        //console.log(revrating);
        //console.log(revdesc.length);
      if(revdesc!=''&& revrating!='' && revdesc.length<=1000){
          //console.log('ok you are elibible');
          writereview.style.display='none'
          let reviewer={
            rdesc:revdesc,
            rrating:revrating,
            rprod:prodid
           }
           //console.log(reviewer);

           fetch(`${window.origin}/buyer/product/createrev`,{
            method:'POST',
            headers:{
              'content-Type':'application/json'
            },
            body:JSON.stringify(reviewer)
           })
           .then(res=>res.json())
           .then(data=>{
              if(data.status_code==200){
                displayToast('Review added successfully','success')
                window.location.reload()
              }else{
                displayToast('Some error occured','danger')              }
           }).catch(err=>displayToast('Some error occured','danger'))
        }else if(revdesc.length>1000){
          displayToast('Sorry max review length is 150 characters','warning')
        }else if (revrating >5 && revrating<1){
          displayToast('rating should be in range of 1 to 5','warning')
        }else{
          displayToast('Some inputs are missing','danger')
        }
      })
    //  function addrev(){
      //}
    }else if(data.status_code==300){
      displayToast('Sorry only after buying the product you can enter your review','warning')
    }else if(data.status_code==400){
      displayToast('You have already given your review','info')
    }else{
      displayToast('some error has occured'+data.status_code,'danger')
    } 
  }).catch(error=> displayToast('some error has occured'+data.status_code,'danger') )
})

  buynow.addEventListener('click',()=>{
    event.preventDefault();
    if(qtymax>0){
      var orderqty=parseInt(prodqt.textContent);
      let object1={}
      object1['pid']=prodid
      object1['pqty']=orderqty
      //console.log(object1);
      const encode2=encodeURIComponent(JSON.stringify(object1));
      // alert('keep on going')
      window.location.href=`/buyer/checkout?data=${encode2}`;
    }else{
      displayToast("Sorry the current product is currently sold out, please try again after sometime",'info')
    }
  })