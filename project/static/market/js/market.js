$(document).ready(function(){

    var yellowSlide = document.getElementById("yellowSlide")
    var alltypebtn = document.getElementById("alltypebtn")/* 找到全部类型  综合排序的div 4个 */
    var showsortbtn = document.getElementById("showsortbtn")

    var typediv = document.getElementById("typediv")
    var sortdiv = document.getElementById("sortdiv")

    typediv.style.display = "none"/* 默认不显示*/
    sortdiv.style.display = "none"
    yellowSlide.style.display = "none"

    yellowSlide.addEventListener("click",function(){ /* 点击消失（不显示）*/
        this.style.display = "none"
    },false)

    alltypebtn.addEventListener("click",function(){ /* 点击显示*/
        typediv.style.display = "block" /*显示*/
        sortdiv.style.display = "none" /* 不显示*/
    },false)

    showsortbtn.addEventListener("click",function(){
        typediv.style.display = "none"
        sortdiv.style.display = "block"
    },false)

    typediv.addEventListener("click",function(){ /* 点击消失（不显示）*/
        this.style.display = "none"
    },false)
    sortdiv.addEventListener("click",function(){
        this.style.display = "none"
    },false)


    var sortas  = document.getElementsByClassName("sorta")
    for (var i = 0; i < sortas.length; i++){
        var str = window.location.href
        var str1 = str.split(":")[2]
        var arr2 = str1.split("/")
        hrefstr = "/" + arr2[1] + "/" + arr2[2] + "/" + arr2[3] + "/" + i + "/"
        sortas[i].href = hrefstr
    }



//    添加购物车
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
                } else {
                    if (data.data == -1) {
                        //说明没登录
                        //console.log("333333333333333")
                        window.location.href = "http://127.0.0.1:8000/login/"
                    }
                }
            })
        },false)



        subShoppings[i].addEventListener("click",function(){
            sid = this.getAttribute("ga")
            $.post("/changcart/1/", {"productid":this.getAttribute("ga")}, function(data){
                if (data.status == "success"){
                    document.getElementById(sid).innerHTML = data.data
                    console.log("数量：",data.data)
                } else {
                    if (data.data == '0') {
                        window.location.href = "http://127.0.0.1:8000/login/"
                    }
                }
            })
        },false)
    }




})

