$(document).ready(function() {
    var accunt = document.getElementById('accunt')
    var pass = document.getElementById('pass')
    var passwd = document.getElementById('passwd')

    var accunterr = document.getElementById('accunterr')
    var checkerr = document.getElementById('checkerr')
    var passerr = document.getElementById('passerr')
    var passwderr = document.getElementById('passwderr')

    accunt.addEventListener("focus", function () { /* 聚焦到这里accunterr checkerr消失*/
        accunterr.style.display = "none"
        checkerr.style.display = "none"
    }, false)
    accunt.addEventListener("blur", function () { /* 离焦到这里做一些验证*/
        var inputStr = this.value
        if (inputStr.length < 6 || inputStr.length > 12) {
            accunterr.style.display = "block"
            return
        }
        $.post("/checkuserid/",{"userid":inputStr}, function (data) {
            if (data.status == "error"){
                checkerr.style.display = "block"
            }
        })
    }, false)



    pass.addEventListener("focus", function () { /* 聚焦到这里accunterr checkerr消失*/
        passerr.style.display = "none"
    }, false)
    pass.addEventListener("blur", function () { /* 离焦到这里做一些验证*/
        var inputStr = this.value
        if (inputStr.length < 6 || inputStr.length > 16) {
            passerr.style.display = "block"
            return
        }
    }, false)



    passwd.addEventListener("focus", function () { /* 聚焦到这里accunterr checkerr消失*/
        passwderr.style.display = "none"
    }, false)
    passwd.addEventListener("blur", function () { /* 离焦到这里做一些验证*/
        var inputStr = this.value
        if (inputStr != pass.value) {
            passwderr.style.display = "block"
            return
        }
    }, false)

})
