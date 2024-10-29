const imageinput=document.getElementById('cmt');
const selectedfile=imageinput.files[0];
imageinput.addEventListener('change', function (e) {
    const selectedFile = e.target.files[0];
let reader;
let imageData
    if (selectedFile) {
         reader = new FileReader();

        reader.onload = function (e) {
             imageData = e.target.result;
            //console.log(imageData);
        };

        reader.readAsArrayBuffer(selectedFile);
        //console.log(reader);
    }
});


function demo(){

    const name1=document.getElementById('name').value;


    if(!selectedfile){
        alert('please upload an image file of either jpeg or png')
        return
    }
    const maxsize=1*1024*1024
    //console.log(selectedfile);
    //console.log(selectedfile.size);
    if(selectedfile.size>maxsize){
        alert('image size exceeds maximum limit')
        return
    }
    const allowedext=['jpg','jpeg','png'];
    const fileext=selectedfile.name.split('.').pop().toLowerCase()
    if(!allowedext.includes(fileext)){
        alert('upload image of .png, .jpeg, .jpg')
        return 
    }


    
    var entry={
        name:name1,
        comment:selectedfile
    };
    fetch(`${window.origin}/guest/create-entry` ,{
        method:'POST',
        //credentials:'include',
        body:JSON.stringify(entry),
        //cache:'no-cache',
        headers:new Headers({
            'content-type':'application/json'
        })
    })
    .then(function(response){
        if(response.status!=200){
            alert('a similar account with same mail id already exist')
            //console.log(`REsponse status not 200 : ${response.status}`);
            return response;
        }
        response.blob().then(blob=>{
            const imgreturn=new Image()
            imgreturn.style='height:100px;width:100px'
            imgreturn.src=URL.createObjectURL(blob);
            document.body.appendChild(imgreturn)
        })
    })
    .catch(function(error) {
        //console.log(error);
    });
}

function hextobytes(hex){
    const bytes=new Uint8Array(Math.ceil(hex.length/2))
    for(let i=0;i<hex.length;i+=2){
        //bytes.push(parseInt(hex.substr(i,2),16))
        bytes[i/2]=parseInt(hex.substr(i,2),16)
    }
    //console.log(bytes);
    return bytes
}
