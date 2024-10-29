/*search  */
const search=document.getElementById("searchbtn");
const sdisplaydiv=document.getElementById('sdisplaydiv');
const inputbar=document.getElementById('inp');
search.addEventListener('click',()=>{
    let searchprod=[]
    sdisplaydiv.innerHTML=""
    //console.log("before if else : ",searchprod);
    if(inputbar.value==""){
        sdisplaydiv.innerHTML=`<h3 id="searchpresent">please enter product name to search</h3>`
    }
    else{
        a='hi'
        b=inputbar.value
        fetch(`${window.origin}/buyer/searchdemo`,{
            method:'POST',
            headers:{
                'content-Type':'application/json',
            },
            body:JSON.stringify(b),
        })
        .then(response=>response.json())
        .then(data=>{
            if(data.status_code==200){
                let proddata= JSON.parse(data.js)
                //console.log(proddata);
                if(proddata.length<1)
                    return sdisplaydiv.innerHTML=`<h3 id="searchpresent">No such product exist!</h3>`
                proddata.forEach((e,i)=>{
                    searchprod.push(e);
                    //console.log("after data fetched : ",searchprod);
                })
                createElem(sdisplaydiv,searchprod);
            }
            else if(data.status_code==404){
                displayToast('the json data is not received has some problem','danger')
                window.location.href='/buyer'
            }
            else{
                displayToast('Some error in fetching data from server','danger')
                window.location.href='/buyer'
            }
        })  
        .catch(error=>{
    
        })      
    }
})


function createElem(parent,dataarr){
    //console.log('inside createElem')
    //console.log(parent)
    //console.log(dataarr[0].prodname)
    dataarr.forEach((e,i)=>{
        //console.log(e)
        const prod1=''    
        const prod=document.createElement("div")
        prod.innerHTML=`
            <div class="prod d-flex flex-column justify-content-center p-2 col-9 col-md-3 col-lg-3 col-xl-2">
                <div class="col d-flex flex-column">
                    <img class="img-rad" src="${e.prodimg1}" alt="product img"  />
                </div>
                <div>
                    <h5 class="text-center">${e.prodname}</h5>
                    <p class="text-center"><b>₹${e.prodprice}</b></p>
                    <a class="prodbtn btn btn-dark w-100" id="${e.productid}$" href="product/${e.productid}">View Product</a>
                </div>
            </div>            
        ` ;

        parent.appendChild(prod);               
    })
} 