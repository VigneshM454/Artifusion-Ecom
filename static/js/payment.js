const cname=document.getElementById('name');
const cnum=document.getElementById('num');
const cvc=document.getElementById('cvc');
const expy=document.getElementById('expyear');
const expm=document.getElementById('expmonth');

const cardnum=document.getElementById('cardnum');
const cardname=document.getElementById('cardname');
const expdate1=document.getElementById('cardexpdate1');
const expdate2=document.getElementById('cardexpdate2');
const ccvc=document.getElementById('cardcvc');
const btn=document.getElementById('verify');
const form1=document.getElementsByTagName('form')[0];
const namerr=document.getElementsByClassName('.namerr')[0];
const numerr=document.getElementsByClassName('.numerr')[0];
const daterr=document.getElementsByClassName('.dateerr')[0];
const cverr=document.getElementsByClassName('.cverr')[0];
const success=document.getElementById('success');
let inputs=document.querySelectorAll('.inputs');
const err=document.querySelectorAll('.err');
let iparr=[cname,cnum,expy,expm,cvc];
let oparr=[cardname,cardnum,expdate1,expdate2,ccvc];
let j=(g)=>{
  if(g<=1){
    return g;
  }
  else if(g===2||g===3){
    return 2;
  }
  else{
    return 3;
  }
}
let hasnumber=(str)=>{
  return /\d/.test(str);
}

for(let i=0;i<5;i++){
    iparr[i].oninput=function updatediv(){
        let va=iparr[i].value;
        oparr[i].textContent=va;
    }
}

let v=0;
btn.addEventListener('click',()=>{
  event.preventDefault();
  for (let i = 0; i < 5; i++) {
    if(iparr[i].value!==''){
     inputs[i].style.border='1px solid black';
      err[j(i)].style.display='none';
      if(hasnumber(cname.value)){
        err[0].style.display='flex'
        err[0].style.display = 'flex';
        err[0].innerHTML = 'Invalid input';
        inputs[0].style.border='1px solid red';
      }
      if (expm.value < 1 || expm.value > 12 || expy.value < 23 || expy.value > 45) {
        err[2].style.display = 'flex';
        err[2].innerHTML = 'Invalid input';
        inputs[2].style.border='1px solid red';
        inputs[3].style.border='1px solid red';
      }
      if(cnum.value.length<8||cnum.value.lenght>18){
        err[1].style.display = 'flex';
        err[1].innerHTML = 'Invalid input';
        inputs[1].style.border='1px solid red';
      }
      if (cvc.value < 100 || cvc.value > 10000) {
        err[3].style.display = 'flex';
        err[3].innerHTML = 'Invalid input';
        inputs[4].style.border='1px solid red';
      }
      else  if(!(hasnumber(cname.value)||expm.value < 1 || expm.value > 12 || expy.value < 23 || expy.value > 45||cnum.value.length<8||cnum.value.lenght>18||cvc.value < 100 || cvc.value > 10000)){
      setTimeout(() => {
        form1.style.display = 'none';
        success.style.display = 'flex';
      }, 2000);
      }
    } 
    else if (iparr[i].value==='') {
      err[j(i)].style.display='flex'
      inputs[i].style.border='1px solid red';
      err[j(i)].innerHTML = "Can't be blank";
    }
  }
  
});
