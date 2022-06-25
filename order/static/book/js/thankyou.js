let ordernumber = location.href.split("number=");
order_number = ordernumber[ordernumber.length - 1]
console.log(order_number)

function loadorderdataapi() {

    bookingdata={
            'order_number':order_number}

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
        console.log(result)
        if (result.error) {
            console.log('result')
            location.href = '/'
        } else {
            addorderdata(result);
            document.getElementById("loadgif").style.display = "none";
        }
    });
}
loadorderdataapi()

function addorderdata(result) {
    // console.log(result.order.trip.attraction.image)
    if (result.data.order.trip_time == "morning") {
        ordertimetext = "早上 9 點到下午 4 點";
    }
    if (result.data.order.trip_time == "afternoon") {
        ordertimetext = "下午 2 點到下午 9 點";
    }

    date = result.data.order.trip_date.split('', 10)
    date = date.toString().replace(/,/g,"")

    img_src =  result.data.trip_data.images.split(',', 1)

    document.querySelector('.order.number').textContent = "訂單編號： " + order_number;
    document.querySelector('.order.title').textContent = "導覽行程： 台北－" + result.data.trip_data.stitle + "－導覽一日遊";
    document.querySelector('.order.address').textContent = "導覽地點： " + result.data.trip_data.address;

    document.querySelector('.order.time').textContent = "導覽時間： " + date + "－" + ordertimetext

    document.querySelector('.order.name').textContent = "訂購姓名： " + result.data.order.contact_name;
    document.querySelector('.order.phone').textContent = "聯絡電話： " + result.data.order.contact_phone;
    document.querySelector('.order.email').textContent = "聯絡信箱： " + result.data.order.contact_email;
    document.querySelector('.orderimg>img').src = img_src[0];
    document.querySelector('.orderimg>img').title = result.data.trip_data.stitle;

}