const wishtable=document.querySelector('#wishtable')
const params=new URLSearchParams(window.location.search);
const encodeddata=params.get('data');
let data;
let dataarr=[];
//        <td>In Stock</td>
let demotxt="hacky"
function addcartfn(i,maxqty){
    //console.log(i);
    if(maxqty>0){
      var id={'productid':i}

      fetch(`${window.origin}/buyer/prod/cart`,{
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
              localStorage.setItem('alertMsg','added to cart successfully')
              localStorage.setItem('msgType','success')
  
              location.reload()
          }else if(data.status_code==300){
            displayToast('the product is already in cart or wishlist','warning')
          }else{
            displayToast('Some error has occured'+data.status_code,'danger')
          }
        }).catch(error=>{ displayToast('Some error has occured','danger') })
    }
    else{
      displayToast('Sorry the product have been sold out , please try again later','info')
    }

}

function removefn(i){
    var id={"productid":i}
    fetch(`${window.origin}/buyer/wishlist/remove`,{
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
            displayToast('Product removed from wishlist','success')
            // localStorage.setItem('alertMsg','removed from wishlist  successfully')
            // localStorage.setItem('msgType','alert')
            location.reload()
        }else{
          displayToast('some error has occured'+data.status_code,'danger')
        }
      }).catch(error=>{
        displayToast('some error has occured'+data.status_code,'danger')
      })
}
/*
window.onload=()=>{
  //location.reload()
    fetch(`${window.origin}/buyer/wishlist`,{
        method:"POST",
        headers:{
          "content-Type":"application/json",
        },
        body:JSON.stringify(demotxt),
      })
      .then(response=>response.json())
      .then(data=>{
        if(data.status_code==200){
           // //console.log(data.js);
            let data123=data.js
            ////console.log(data)
            if(data123){
                data=JSON.parse(data123)
                data.forEach((d,i)=>{
                    const tr=document.createElement('tr')
                    const trinside=`
                        <td>${i+1}</td>
                        <td><img src="${d.prodimg1}" alt="" height="50px" width="50px" style="border:2px solid black; border-radius:10px"></td>
                        <td>${d.prodname}</td>
                        <td>${'₹'+d.prodprice} /-</td>
                        <td>
                            <div class="pe-2 ">
                                <button id="addcart-${d.productid}" onclick="addcartfn(${d.productid},${d.qtyavail})" class=" btn bg-header text-light col-12 m-1 col-md-5 col-lg-5 h-100 btn1 p-md-2  p-lg-2">Add_Cart</button>    
                                <button id="remove-${d.productid}" onclick="removefn(${d.productid})" class=" btn bg-header text-light col-12 m-1 col-md-5 col-lg-5 h-100 p-md-2 p-lg-2  btn1">Remove</button>        
                            </div>
                        </td>   
                    `
                    tr.innerHTML=trinside;
                    tr.classList.add("btn1")
                    tr.id=d.productid
                    wishtable.append(tr)    
                })
              //  dataarr.push(data)
            }
            // else{
            //   alert('data not receveid');
            // }
        }else if(data.status_code==500){
          const wishtable2=document.getElementById('wishtable2')
          wishtable2.innerHTML=`
          <div class=" p-3 mt-5 d-flex align-items-center justify-content-center text-center h1 text-color"> Wishlist is empty!</div>
          `
          document.getElementById('wtable').style.display='none'
          document.getElementById('whead').style.display='none'
        }else if(data.status_code==454){
          //alert('some error has occured'+data.status_code)
          wishtable.innerHTML=`<h1>YOU have no products in your wishlit</h1>`
        }
      })
      .catch(error=>{
        //console.log('Some error occured')
      })
}*/