//console.log('hi');
function createreplydiv(id){
    const parentrev=document.getElementById(id)
    if(parentrev.childElementCount==5){
        //console.log(id);
        //console.log(parentrev.childElementCount);
        let btnid=String(id).replace('rev','')
        const inputdiv=`
        <div class="m-0  row mb-3  mx-1 d-flex flex-row gap-2" >
        <input type="text" required=""  class="form-control col-7" id="msg${btnid}" placeholder="Reply..."  name="revreply" style="width:75%!important; max-width:500px">

        <button type="submit"   onclick="addreply(${btnid})"  id="${'btn'+btnid}" class="btn btn-primary col-3 d-flex align-items-center justify-content-center" style="max-width: 50px !important; min-width: 50px;">
            <img src="/static/images/send1.png" alt="" style="width:80%;height:80%">

        </button>
        </div>        
        `
        const replydiv=document.createElement('div')
        replydiv.classList.add('reply')
        replydiv.id='child'+id
        replydiv.innerHTML=inputdiv
        parentrev.append(replydiv)
        //console.log(parentrev.childElementCount);    
    }
    else{
        var child=document.getElementById('child'+id)
        parentrev.removeChild(child)
    }
}
function addreply(id){
    let inpdiv=document.getElementById('msg'+id)
    if(inpdiv.value.length>=5){
        //alert(inpdiv.value)
        //console.log(id);//reviewid 
        let inpval=inpdiv.value;//revtext
        //console.log(inpval);
        let reply={
            'reply':inpval,
            'revid':id
        }
        //console.log(reply);
        inpdiv.value=''   
        
        fetch(`${window.origin}/seller/review/reply`,{
            method:"POST",
            headers:{
              "content-Type":"application/json",
            },
            body:JSON.stringify(reply),
          })
          .then(response=>response.json())
          .then(data=>{
            //console.log(data.status_code);
           const replies= document.querySelectorAll('.reply')
           replies.forEach((elem)=>{
            elem.style='display:none;'
           })
            if(data.status_code==200){
              window.location.reload()
              //console.log('Reply added successfully')
              displayToast('Reply added ','success')
              // revform.classList.remove('hide')
              // revform.classList.add('show')      
            //  function addrev(){
              //}
            }else if(data.status_code==404){
              displayToast('You have already given your reply to this review','info')
            }else{
              displayToast('Some error has occured'+data.status_code,'danger')
            } 
          }).catch(error=>displayToast('Some error has occured','danger'))

    }else{
        displayToast('Review should have atleast 5 character','warning')
    }
}