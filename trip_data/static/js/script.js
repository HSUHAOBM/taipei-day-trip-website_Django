let div_main = document.createElement("div");
div_main.className = "main";
let div_content = document.createElement("div");
div_content.className = "content";
div_main.appendChild(div_content);
let warp = document.querySelector('.warp');
warp.appendChild(div_main)



let page = 0;
let keyword = null;
let checkonload = true;
let nextpage = null;
let data;

//讀取資料
function loadapi() {
    data = null;
    let src = "api/trip_data/page=" + String(page) + "/keyword=" + keyword;
    // let src = "api/trip_data/page=" + String(page);

    // let src='api/trip_data/page=3'
    console.log(src)
    fetch(src, {
        method: "GET",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        }
      }).then(function(response) {
        return response.json();
    }).then(function(result) {
        console.log(result)
        if (result.error) {
            alert("無資料");
            page = 0;
            keyword = "";
            loadapi();
        } else {
            data = result;
            addbody();
            document.getElementById("loadgif").style.display = "none";

        }
    });
}

//資料>畫面
function addbody() {
    for (let i = 0; i < data.data.length; i++) {
        // console.log("http://" +result.data[i].images[0].split('http://')[1].split(',')[0])
        let div_box = document.createElement("div")
        div_box.className = "box";
        div_content.appendChild(div_box)

        let div_imgbox = document.createElement("div")
        div_imgbox.className = "imgbox";
        div_box.appendChild(div_imgbox);

        let a_href = document.createElement("a")
        a_href.href = "/attraction/" + String(data.data[i].id)
        div_imgbox.appendChild(a_href)

        let img_imgboximg = document.createElement("img")
        img_imgboximg.className = "imgboximg";
        img_imgboximg.src = "http://" + data.data[i].images.split('http://')[1].split(',')[0];
        a_href.appendChild(img_imgboximg);
        // stitle
        let div_text1 = document.createElement("div")
        div_text1.className = "text1";
        div_text1.textContent = data.data[i].stitle
        div_box.appendChild(div_text1);

        let div_textbox = document.createElement("div")
        div_textbox.style = "display: flex;";
        div_box.appendChild(div_textbox);

        //mrt
        let div_text2 = document.createElement("div")
        div_text2.className = "text2";
        div_text2.textContent = data.data[i].mrt
        div_textbox.appendChild(div_text2);

        //category
        let div_text3 = document.createElement("div")
        div_text3.className = "text3";
        div_text3.textContent = data.data[i].category
        div_textbox.appendChild(div_text3);

    }
    nextpage = data.nextpage
        // console.log("nextpage", nextpage)
    checkonload = true

}

//畫面讀取初始
window.onload = function() {
    loadapi();
    // initPage();
}


//功能1-畫面捲動監聽
window.addEventListener('scroll', function() {

    let webwarp = document.querySelector('.warp');
    if (10 > (webwarp.scrollHeight - window.pageYOffset - window.innerHeight) & checkonload == true & nextpage != null) {
        checkonload = false;
        page += 1;
        document.getElementById("loadgif").style.display = "flex";
        loadapi();
    }
})

//功能2-取得關鍵資料
function addkeydata() {
    page = 0;
    let inputkeyword = document.querySelector('.searchtext');
    // console.log(inputkeyword.value)
    keyword = inputkeyword.value
    div_content.innerHTML = "";
    document.getElementById("loadgif").style.display = "flex";

    loadapi();
}


