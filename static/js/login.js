const buyer=document.getElementById('buy1');
const seller=document.getElementById('sell1');
const user_sign=document.getElementById('signin-form');
const user_login=document.getElementById('login-form');

const dynamo=document.getElementById('dynamo');
const refer=document.getElementById('refer');
const h2=document.getElementById('h2');
const p=document.getElementById('p');
let id=1;// 1-> buyer, 2-> seller
const signupText=document.getElementById('signup-text')
const signinText=document.getElementById('signin-text')
const loginTitle=document.getElementById('loginTitle')

const resetdiv=document.getElementById('resetdiv')
const otpdiv=document.getElementById('otpdiv')
const otpinput=document.getElementById('otpinput')
const otpBtn=document.getElementById('otpBtn')
const otpTitle=document.getElementById('otpTitle')

document.getElementById('otpclose').onclick=()=>{
    otpdiv.style.display='none'
}

function verifyOtp(user){// this is used while creating new buyer/ seller accounts
    otpBtn.addEventListener('click',()=>{
        if((otpinput.value).length===8 && otpdiv.style.display=='flex'){
            var otp=parseInt(otpinput.value)
            //console.log(otp)
            const verifydata={user,otp}
            fetch(`${window.origin}/verify-otp`,{
                method:'POST',
                headers:{
                    'content-Type':'application/json',
                },
                body:JSON.stringify(verifydata)
            })
            .then(response=>response.json())
            .then(data=>{
                if(data.status_code==200){
                    window.location.href= user==='buyer'?'/buyer':'/seller/home'
                    var text= user==='buyer'?'Buyer signup success !':'Seller signup success'
                }else{
                    displayToast("Invalid Otp, please enter valid otp",'danger')
                }
            }).catch(err=> displayToast('Some error occured','danger'))    
        }
    })
}

function verifyAdmin(){
    otpBtn.addEventListener('click',()=>{
        if((otpinput.value).length===8 && otpdiv.style.display=='flex'){
            var otp=parseInt(otpinput.value)
            //console.log(otp)
            const verifydata={otp}
            fetch(`${window.origin}/verify-admin`,{
                method:'POST',
                headers:{
                    'content-Type':'application/json',
                },
                body:JSON.stringify(verifydata)
            })
            .then(response=>response.json())
            .then(data=>{
                if(data.status_code==200){
                    
                    window.location.href= '/admin/home'
                }else{
                    displayToast("Invalid Admin Otp",'danger')
                }
            }).catch(err=> displayToast('Some error occured','danger'))    
        }
    })
}

document.getElementById('resetclose').onclick=()=>{
    resetdiv.style.display='none'
}
document.getElementById('forgotPass').onclick=()=>{
    resetdiv.style.display='flex'
}

signinText.onclick=()=>{
    user_login.classList.remove('hide')
    user_sign.classList.add('hide')
}

signupText.onclick=()=>{
    user_login.classList.add('hide')
    user_sign.classList.remove('hide')
}
//single signin and login form are used for seller ,buyer,admin
buyer.onclick=()=>{
    loginTitle.innerText='Buyer Login'
    buyer.classList.add('useractive')
    seller.classList.remove('useractive')
    user_sign.removeChild(dynamo)
    dynamo.style.display='none'
    id=1;
    user_login.classList.remove('demo')
    user_sign.classList.remove('demo')
}
seller.onclick=()=>{
   loginTitle.innerText='Seller Login'
   buyer.classList.remove('useractive')
   seller.classList.add('useractive')
   p.innerText='By continuing, you agree to Our Conditions of Use and Privacy Policy as a Seller'
    dynamo.style.display='block'
    user_sign.appendChild(dynamo)
    user_sign.insertBefore(dynamo,refer)
    id=2;
    user_sign.classList.add('demo')
    user_login.classList.add('demo')
}

const fname =user_sign.querySelector('#fname');
const lname=user_sign.querySelector('#lname');
const phone=user_sign.querySelector('#phoneno')
const email=user_sign.querySelector('#email')
const addr=user_sign.querySelector('#addr')
const pwd=user_sign.querySelector('#pwd');
const terms=user_sign.querySelector('#terms')
let checked=false;

let nameregx=/[A-Za-z\s]+/;
let emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
let phregx=/^(\+\d{1,3}\s?)?\d{10}$/

let checkbox;
const shop=user_sign.querySelector('#shop')
checkbox=user_sign.querySelectorAll('input[name="d"]');

user_sign.addEventListener('submit',()=>{
    event.preventDefault();
    let f=nameregx.test(fname.value)
    let l=nameregx.test(lname.value)
    let p= phregx.test(phone.value)
    let e=emailRegex.test(email.value)  
    
    const data1={
        firstname:fname.value,
        lastname:lname.value,
        phoneno:phone.value,
        emailid:email.value,
        passwd:pwd.value,
        address:addr.value
    }

    let arr=[f,l,p,e]
    let arr2=[fname,lname,phone,email]
    if(id==2){
        let shopvalue=shop.value;
        data1['shop']=shopvalue;
        data1['category']=''
        let charr=[]
        checkbox.forEach((ch)=>{
            if(ch.checked){//  ch=1
             data1['category']=ch.value
            }
            charr.push(ch)
        })
    }
    //console.log(data1);
    //console.log(id);
    //console.log(pwd.value.length);
    let expr=f&&l&&p&&e&&terms.checked&&(pwd.value.length>5);
    //console.log(expr)
    if(expr && id==1 ){//buyer        
        fetch(`${window.origin}/create-user`,{
            method:'POST',
            headers:{
                'content-Type':'application/json',
            },
            body:JSON.stringify(data1),
        })
        .then(response=>response.json())
        .then(data=>{
            if(data.status_code==200){//window.location.href='/buyer'
                otpdiv.style.display='flex'
                verifyOtp('buyer')
            }else if(data.status_code==404){
                displayToast('This mail id already exist','warning') //window.location.href='/'
            }else{
                displayToast('Some error occured','danger') //window.location.href='/'
            }
        }).catch(error=>displayToast('Some error occured','danger'))      
    }
    else if(expr && shop && shop.value!=='' && data1['category']!=''){
        //seller
        //console.log('hi');
        //console.log(data1);
        fetch(`${window.origin}/create-seller`,{
            method:'POST',
            headers:{
                'content-Type':'application/json',
            },
            body:JSON.stringify(data1),
        })
        .then(response=>response.json())
        .then(data=>{
            //console.log('data is -------------------');
            //console.log(data)
            if(data.status_code==200){//window.location.href='/seller'
                otpdiv.style.display='flex'
                verifyOtp('seller')
            }else if(data.status_code==404){
                displayToast('This mail id already exist','warning')
            }else{
                displayToast('Some error occured','danger')
            }
        }).catch(error=>displayToast('Some error occured','danger'))      
    }else{
        displayToast('Please enter necessary inputs','danger')
        for(var i=0;i<arr.length;i++){
            if(arr[i]==false){
                arr2[i].classList.add('border-danger')
            }else{
                arr2[i].classList.remove('border-danger')
            }
        }
    }
})

const email2=user_login.querySelector('#email');
const pwd2=user_login.querySelector('#pwd');

user_login.addEventListener('submit',(event)=>{
    event.preventDefault();
    let count=1;
    var e2=emailRegex.test(email2.value)
    var p2=pwd2.value.length>5;
    if(e2 && p2){
        const testdata1={
            testemail:email2.value,
            testpwd:pwd2.value
        }
        //console.log(window.origin);
        fetch(`${window.origin}/admintest`,{
            method:'POST',
            headers:{
            'content-Type':'application/json',
            },
            body:JSON.stringify(testdata1),
        })
        .then(response=>response.json())
        .then((data)=>{
        //console.log(data.status_code);  // data=JSON.parse(data)
        if(data.status_code==200){
            otpTitle.innerText='Admin OTP verification'
            otpdiv.style.display='flex'
            verifyAdmin()
        }else{
            let url1,url2;
            if(id==1){
                url1='/login-user'
                url2='/buyer'
            }else{
                url1='/login-seller'
                url2='/seller/home'    
            }
            fetch(`${window.origin}${url1}`,{
                method:'POST',
                headers:{
                    'content-Type':'application/json',
                },
                body:JSON.stringify(testdata1),
            })
            .then(function(response){
                if(response.status!=200){
                    if(response.status==300){
                        displayToast('Do the account creation step using same email to retrive your account','Info')
                    }else{
                        displayToast('Incorrect credentials','danger')
                    }
                    //console.log(response)
                    //console.log(`REsponse login  status not 200 : ${response}`);
                    return response;
                }
                response.json().then(function(data){
                    //console.log(data);
                    window.location.replace(url2)
                    var text= url2==='/buyer'?'Buyer login success !':'Seller login success !'
                })
            })
            .catch(function(){
                //console.log('no response');
            })        
        }

        })    
        .catch((err,data)=>{
            //console.log(err);
            //console.log(data);
        })        
   //console.log('im outside of fetch');
    }
})