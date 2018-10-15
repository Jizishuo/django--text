$(document).ready(function(){

    var addShoppings = document.getElementsByClassName("addShopping")
    var subShoppings = document.getElementsByClassName("subShopping")

    for (var i = 0; i < subShoppings.length; i++) {
        addShoppings[i].addEventListener("click",function(){
            sid = this.getAttribute("ga") //拿到prudictid
            $.post("/changcart/0/", {"productid":sid}, function(data){
                //console.log("222222222222222")
                if (data.status == "success"){
                    //添加成功
                    document.getElementById(sid).innerHTML = data.data
                    console.log("数量：",data.data)
                    document.getElementById(sid+"price").innerHTML = '￥'+data.price +'元'

                }
            })
        },false)



        subShoppings[i].addEventListener("click",function(){
            sid = this.getAttribute("ga")
            $.post("/changcart/1/", {"productid":this.getAttribute("ga")}, function(data){
                if (data.status == "success"){
                    document.getElementById(sid).innerHTML = data.data
                    console.log("数量：",data.data)
                    document.getElementById(sid+"price").innerHTML = '￥'+data.price +'元'
                    if (data.data == 0){
                        //window.location.href = "http://127.0.0.1:8000/cart/"
                        var li = document.getElementById(sid+"li")
                        li.parentNode.removeChild(li)
                    }
                }
            })
        },false)
    }



    var ischoses = document.getElementsByClassName("ischose")
    for (var j = 0; j < ischoses.length; j++) {

        ischoses[j].addEventListener("click", function(){
            ssid = this.getAttribute("goodsid")
            $.post("/changcart/2/", {"productid":ssid}, function(data){
                if (data.status == "success"){
                    //var s = document.getElementById(ssid+"a")
                    document.getElementById(ssid+"a").innerHTML = data.data
                }
            })
        }, false)
    }



    var ok = document.getElementById("ok")

    ok.addEventListener("click",function(){
        var f = confirm("是否确认下单？")
        if (f){
            $.get("/saveorder/",function(data){
            if (data.status == "error"){
                console.log("订单失败")
            } else {
                console.log("订单成功")
                window.location.reload()
            }
        })
        }

    })

})