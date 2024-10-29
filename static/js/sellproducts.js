const imgdivs = document.getElementById('imgdivs');
const imgip = document.getElementById('imageips');
const addnewprod=document.getElementById('addnewprod')
const addnew=document.getElementById('addnew')

const addMoreDiv=document.getElementById('addProddiv')
const closeBtn=document.getElementById('divclose1')
const pname=document.getElementById('pname')
const addInput=document.getElementById('addInput')

function updateProdCount(pid){
    document.getElementById('addBtn').addEventListener('click',()=>{
        if((addInput.value)>0 && addMoreDiv.style.display=='flex'){
            var pqty=parseInt(addInput.value)
            const prodinfo={pid,pqty}
            document.getElementById('addBtn').disabled=true
            fetch(`${window.origin}/seller/addMoreQty`,{
                method:'POST',
                headers:{
                    'content-Type':'application/json',
                },
                body:JSON.stringify(prodinfo)
            })
            .then(response=>response.json())
            .then(data=>{
                //console.log(data);
                //console.log(data.status_code);    
                if(data.status_code==200){
                    window.location.reload()
                    displayToast('More products added')
                }else{
                    displayToast("Sorry some issue in adding more products",'danger')
                }
            }).catch(err=>                     displayToast("Sorry some issue in adding more products",'danger'))
            .finally(()=> {
                addMoreDiv.style.display='none'
                document.getElementById('addBtn').disabled=false
            })
        }
    })
}


closeBtn.onclick=()=>{
    addMoreDiv.style.display='none'
}

let srcarr = [];
let tot_prod_listed=0;
let tot_prod_sold=0
const prodlisted=document.getElementById('prodlisted')
const prodsold=document.getElementById('prodsold')
//console.log(window.origin)
let formData=''
imgip.addEventListener('change', () => {
    formData=new FormData()
    srcarr=[]
    //console.log(imgdivs)
    //console.log(imgdivs.firstChild)
    while (imgdivs.hasChildNodes()) {
        imgdivs.removeChild(imgdivs.firstChild);
      }    
     if (imgip.files && imgip.files.length <= 3) {
        for (let i = 0; i < imgip.files.length; i++) {
            formData.append(`img${i+1}`,imgip.files[i])
            if (imgip.files[i]) {
                const reader = new FileReader();
                reader.onload = (function (index) {
                    return function (e) {
                        const img = document.createElement('img');
                        img.id = 'imgup' + index;
                        img.src = e.target.result;
                        srcarr.push(img.src);
                        img.style.width = '70px';
                        img.style.height = '70px';
                        imgdivs.appendChild(img);
                    };
                })(i);

                reader.readAsDataURL(imgip.files[i]);
            }
        }
    } else {
        displayToast('Upload at most 3 images only','warning');
    }
    //console.log(srcarr);

});
const prodname=document.getElementById('name')
const prodprice=document.getElementById('price')
const prodqty=document.getElementById('qty')
const proddesc=document.getElementById('proddesc')
const prodcatg=document.querySelectorAll('.checkboxgrp');

function addMoreQty(id,name){
    const pid=id
    //console.log(id);
    addMoreDiv.style.display='flex'
    pname.innerHTML=`<b>"${name}"</b>`
    updateProdCount(pid)
}

const sppar=document.getElementById('sppar')

addnewprod.addEventListener('submit',()=>{
    event.preventDefault()
    const npname=prodname.value;
    const npqty=  parseInt(prodqty.value);
    const npprice=prodprice.value;
    const npdesc=proddesc.value
    const imgarr=srcarr;
    let nprodcat=''
    //let democheck=document.getElementsByTagName('input[checkbox]')
    let categcon=false
    prodcatg.forEach((prod,i)=>{
        if(prod.checked){
            nprodcat=prod.value;
            categcon=true
            //alert(nprodcat)
        }
    })
    //alert(nprodcat)

    const newprod={
        pname:npname,
        pqty:npqty,
        pprice:npprice,
        pdesc:npdesc,
        pimgarr:imgarr,
        prodcat:nprodcat
    }
    formData.append('pname',npname)
    formData.append('pqty',npqty)
    formData.append('pprice',npprice)
    formData.append('pdesc',npdesc)
    formData.append('prodcat',nprodcat)
    //console.log(newprod);//&& categcon===true
    if(npname!=''&& npdesc!='' && npprice!='' && npqty>0 && imgarr.length>=1 && categcon===true){
        //alert('success') 
        //alert(srcarr[0])
        //console.log(srcarr[0]);
        //console.log(newprod);
        fetch(`${window.origin}/seller/products/create-new`,{
            method:'POST',
            /*
            headers:{
                'content-Type':'application/json',
            },*/
            body:formData,
        })
        .then(response=>response.json())
        .then(data=>{
            if(data.status_code==200){
                //window.location.href='/seller/products'
                displayToast('New product added!','success')
                location.reload()
            }else if(data.status_code==404){
                displayToast('Some probem in getting data from server','danger')
                window.location.href='/seller/products'
            }else{
                displayToast('Some issue in adding products','danger')
                window.location.href='/seller/products'
            }
        }).catch(error=>{displayToast('Some issue in adding products','danger')})      
    }
    else{
        displayToast('please fill out the necessary details')
    }
})
