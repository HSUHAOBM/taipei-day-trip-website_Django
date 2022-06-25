let oderprice = 0

// 讀取訂單API
function loadapi() {
    let url = "/api/book"
    fetch(url, {
        method: "GET",
        headers: {
            'Content-Type': 'application/json',
            "X-Requested-With": "XMLHttpRequest",
        }
    }).then(function(response) {
        return response.json();
    }).then(function(result) {
        console.log(result)
        if (result.error) { goindex(); }
        if (result.data == null) {
            notaipdata();
        }
        if (result.data != null) {
            addbody(result);
            getaipdata();
        }
        getuserorder();
    });
}
loadapi();
//畫面
function addbody(result) {
    document.querySelector('.righttext1').textContent = "台北一日遊：" + result.data.order_trip.name;
    document.querySelector('.righttext2>div').textContent = result.data.order_date;
    if ( result.data.order_time == "morning") {
        document.querySelector('.righttext3>div').textContent = "早上 9 點到下午 4 點";
        document.querySelector('.righttext4>div').textContent = "新台幣 2000 元";
        document.querySelector('.mainfinsh>a').textContent = "總價：新台幣 2000 元";
        oderprice = 2000
    }
    if ( result.data.order_time == "afternoon") {
        document.querySelector('.righttext3>div').textContent = "下午 2 點到下午 9 點";
        document.querySelector('.righttext4>div').textContent = "新台幣 2500 元";
        document.querySelector('.mainfinsh>a').textContent = "總價：新台幣 2500 元";
        oderprice = 2500

    }
    document.querySelector('.righttext5>div').textContent =  result.data.order_trip.address;
    document.querySelector('.leftimg>img').src = "http://" + result.data.order_trip.images.split('http://')[1].split(',')[0];
    document.querySelector('.leftimg>img').title = result.data.order_trip.name;
}
//刪除訂單
function clearapi() {
    let url = "/api/book"
    fetch(url, {
        method: "DELETE",
        headers: {
            'Content-Type': 'application/json',
            "X-Requested-With": "XMLHttpRequest",
        }
    }).then(function(response) {
        return response.json();
    }).then(function(result) {
        data = result;
        // console.log(data)
        if (data.ok) {
            window.location.reload();
        }
    });
}

//無訂單資料
function notaipdata() {
    document.querySelector('.order').style.display = "none";
    document.querySelector('.mainfinsh').style.display = "none";

    document.querySelector('.infortext').hidden = false;

    document.querySelector('.maincenter').hidden = true;
    document.querySelector('.form-group').hidden = true;
    document.querySelector('#hr1').hidden = true;
    document.querySelector('#hr2').hidden = true;
    document.querySelector('#hr3').hidden = true;
    document.querySelector('.footer').style.height = "865px"

}

//有訂單資料
function getaipdata() {
    document.querySelector('.order').style.display = "flex";
    document.querySelector('.mainfinsh').style.display = "flex";

    document.querySelector('.infortext').hidden = true;

    document.querySelector('.maincenter').hidden = false;
    document.querySelector('.form-group').hidden = false;
    document.querySelector('#hr1').hidden = false;
    document.querySelector('#hr2').hidden = false;
    document.querySelector('#hr3').hidden = false;
    document.querySelector('.footer').style.height = "104px"

    setfrontend()



}

//------------//



function setfrontend() {
    // TPDirect.setupSDK(20409, 'app_KYrqKVHwBAtCqEdevKIrZCIfWbNgCUHCgOZwg5O8f3t3hKofm2nvlOOQF6Op', 'sandbox')
    TPDirect.setupSDK('124909', 'app_uXL5abTRd0ZfSeq0paS0B2Zrjt1CerP1OQFt3UHOj65wkFiUWiFaIBmJZacA', 'sandbox')

    TPDirect.card.setup({
        fields: {
            number: {
                element: '.form-control.card-number',
                placeholder: '4242 4242 4242 4242'
            },
            expirationDate: {
                element: '.form-control.expiration-date',
                placeholder: '01 / 23'
            },
            ccv: {
                element: '.form-control.cvc',
                placeholder: '123'
            }
        },
        styles: {
            'input': {
                'color': 'gray'
            },
            'input.ccv': {
                // 'font-size': '16px'
            },
            ':focus': {
                'color': 'black'
            },
            '.valid': {
                'color': 'green'
            },
            '.invalid': {
                'color': 'red'
            },
            '@media screen and (max-width: 400px)': {
                'input': {
                    'color': 'orange'
                }
            }
        }
    })
    TPDirect.card.onUpdate(function(update) {
        // update.canGetPrime === true
        // --> you can call TPDirect.card.getPrime()
        let submitButton = document.querySelector('.btn.btn-default')
        if (update.canGetPrime) {
            // Enable submit Button to get prime.
            submitButton.removeAttribute('disabled')
        } else {
            // Disable submit Button to get prime.
            submitButton.setAttribute('disabled', true)
        }

        // cardTypes = ['mastercard', 'visa', 'jcb', 'amex', 'unionpay','unknown']
        // if (update.cardType === 'visa') {
        //     // Handle card type visa.

        // }
        if (update.cardType != "unknown") {
            // Handle card type visa.
            document.querySelector('#cardtype').textContent = update.cardType;
        }
        if (update.cardType == "unknown") {
            // Handle card type visa.
            document.querySelector('#cardtype').textContent = " ";
        }


        // number 欄位是錯誤的
        if (update.status.number === 2) {
            // setNumberFormGroupToError()
        } else if (update.status.number === 0) {
            // setNumberFormGroupToSuccess()
        } else {
            // setNumberFormGroupToNormal()
        }

        if (update.status.expiry === 2) {
            // setNumberFormGroupToError()
        } else if (update.status.expiry === 0) {
            // setNumberFormGroupToSuccess()
        } else {
            // setNumberFormGroupToNormal()
        }

        if (update.status.ccv === 2) {
            // setNumberFormGroupToError()
        } else if (update.status.ccv === 0) {
            // setNumberFormGroupToSuccess()
        } else {
            // setNumberFormGroupToNormal()
        }
    })
    let form = document.getElementById('formtappay');

    form.addEventListener('submit', function(event) {

        // 取得 TapPay Fields 的 status
        const tappayStatus = TPDirect.card.getTappayFieldsStatus()
            // console.log(tappayStatus)
        event.preventDefault()

        // 確認是否可以 getPrime
        if (tappayStatus.canGetPrime === false) {
            // alert('can not get prime')
            document.querySelector('#message').textContent = "檢查輸入資料是否正確";
            return
        }

        // Get prime
        TPDirect.card.getPrime((result) => {
            // console.log(result)
            if (result.status !== 0) {
                alert('get prime error ' + result.msg)
                return
            }
            console.log('result',result)
            alert('get prime 成功，prime: ' + result.card.prime)
            bookinggotobackend(result.card.prime)
                // send prime to your server, to pay with Pay by Prime API .
                // Pay By Prime Docs: https://docs.tappaysdk.com/tutorial/zh/back.html#pay-by-prime-api

        })
    })
}

//傳送定單
function bookinggotobackend(getprime) {
    let bookingdata = {}
    bookingdata = {
        "prime": getprime,
        "order": {
            "price": oderprice,
            "contact": {
                "name": document.querySelector('.maincenterinput1>input').value,
                "email": document.querySelector('.maincenterinput2>input').value,
                "phone": document.querySelector('.maincenterinput3>input').value
            }
        }
    }
    fetch("/api/order", {
            method: "PATCH",
            body: JSON.stringify(bookingdata),
            headers: {
                'Content-Type': 'application/json',
                "X-Requested-With": "XMLHttpRequest",
            }
        }).then(res => {
            return res.json();
        })
        .then(result => {
            // console.log(result);
            if (result.data.payment.message == "已付款") {
                // alert("成功付款")
                gothankyou(result.data.number)
            }
        });
}

function gothankyou(ordernumber) {
    location.href = '/thanks/number=' + ordernumber
}

let orderbox = document.querySelector('.orderbox');

function getuserorder() {
    let src = "/api/order";
    fetch(src, {
        method: "GET",
        headers: {
            'Content-Type': 'application/json',
            "X-Requested-With": "XMLHttpRequest",
        }
    }).then(function(response) {
        return response.json();
    }).then(function(result) {
        console.log(result)
        if (result.error) {
            document.querySelector('.welcometext.a').style.display = "none";
        } else {

            //畫面
            for (let i = 1; i < result.data.length; i++) {
                let newdiv_box = document.createElement("div")
                newdiv_box.className = "userorderbox";
                orderbox.appendChild(newdiv_box)

                newdiv_box.onclick = function() {
                    location.href = '/thanks/number=' + result.data[i].order.id
                };

                date = result.data[i].order.trip_date.split('', 10)
                date = date.toString().replace(/,/g,"")

                let a_box3 = document.createElement("a")
                a_box3.textContent = date + "－";
                a_box3.className = "a_box a1";
                newdiv_box.appendChild(a_box3)

                let a_box2 = document.createElement("a")
                a_box2.textContent = result.data[i].trip_data.stitle;
                a_box2.className = "a_box a2";
                newdiv_box.appendChild(a_box2)
            }
        }
        document.getElementById("loadgif").style.display = "none";
        document.getElementById("loadgif2").style.display = "none";
    });
}
