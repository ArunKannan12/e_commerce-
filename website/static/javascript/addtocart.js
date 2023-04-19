document.addEventListener("DOMContentLoaded",function(event){
    let btnPlus=document.getElementById('btnPlus')
    let btnMinus=document.getElementById('btnMinus')
    let txtQty=document.getElementById('txtQty')
    let pid=document.getElementById("pid")
    // let tkn=document.querySelector('[name="csrfmiddlewaretoken"]').value;
    let btnCart=document.getElementById("btnCart");
    btnPlus.addEventListener('click',function(){
        let qty=parseInt(txtQty.value,10);
        qty=isNaN(qty)?0:qty;
        if (qty<10) {
            qty++;
            txtQty.value=qty
        }
    })
    btnMinus.addEventListener('click',function(){
        let qty=parseInt(txtQty.value,10);
        qty=isNaN(qty)?0:qty;
        if (qty>1) {
            qty--;
            txtQty.value=qty
        }
    })

    btnCart.addEventListener('click',function(){
        let qty=parseInt(txtQty.value,10);
        qty=isNaN(qty)?0:qty;
        if (qty>0) {
            let postObj={
                'product_qty':qty,
                'pid':pid.value
            }
            console.log(postObj);
            let url = "/cart/"
            fetch(url,{
                method:'POST',
                credentials:'same-origin',
                headers:{
                    'Accept': 'application/json',
                    'X-Requested-With':'XMLHttpRequest',
                    'X-CSRFToken':'{{ csrf_token }}',
                },
                body:JSON.stringify(postObj)
            })
            .then((response) => {
                return response.json() 
            })
            .then((data) => {
                console.log('data:', data);
                location.reload()
            });
            
        }else{
            alert("please enter the quantity")
        }
    });
});
