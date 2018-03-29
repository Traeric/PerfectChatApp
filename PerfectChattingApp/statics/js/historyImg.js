(function(){
    window.onload = function(){
        waterfall();
        activeEvent();
        changeEvent();
    };
    // lazyLoad();
}());


// 将图片按照瀑布流的方式排版
function waterfall(){
    // 计算一排能排几张图片
    // 父容器宽度
    var pWidth = document.querySelector("#wrapper .w_body").offsetWidth;
    // 计算一行能够容纳几张图片
    var count = Math.floor(pWidth / 340);
    // 获取所有的包裹照片的div
    var boxDom = document.querySelectorAll("#wrapper .w_body .box");
    // 转换成数组
    var arrBox = [].slice.call(boxDom);
    // 拿到每行的高度
    var Height = [];
    arrBox.forEach(function(item, index){
        if(index < count){
            Height.push(item.offsetHeight);
        }
    });
    // 开始排版
    boxDom.forEach(function(item, index){
        // 第一排
        if(index < count){
            item.style.cssText = `top: 0px; left: ${index * 340}px`;
        }else{
            // 其他排
            // 拿到高度最小的行的索引
            var ind = Height.indexOf(Math.min.apply(null, Height));
            // 从最短的图片开始插入
            item.style.cssText = `top: ${Height[ind]}px; left: ${ind*340}px`;
            // 刷新该列高度
            Height[ind] += item.offsetHeight;
        }
    });
    // 得到最高的列的高度
    var maxHeight = Math.max.apply(null, Height);
    // 为w_body设置高度
    document.querySelector("#wrapper .w_body").style.height = maxHeight + 'px';
}


// 点击图片选中
var name = document.getElementsByClassName("img_now")[0].src.split("/").pop();
function activeEvent(){
    var lastDom = document.querySelector('#wrapper .w_body .box');
    // 得到父div节点
    var bodyDom = document.querySelector("#wrapper .w_body");
    bodyDom.addEventListener('click', function(event){
        var e = event || window.event;
        // 得到当前点击的节点
        var target = e.target || e.srcElement;
        if(target.localName === "img"){
            // 得到父节点
            var boxDom = target.parentElement;
            // 改变父节点样式
            boxDom.style.cssText += `background-color: rgba(255, 0, 0, 0.5);`;
            // 清除上次选中的节点
            lastDom.style.cssText += `background-color: #fff;`;
            // 拿到文件名
            name = target.dataset.img;
            lastDom = boxDom;
        }
    });
}


// 点击更换按钮更换图片
function changeEvent(){
    var changeButton = document.getElementsByClassName("change")[0];
    var confirmButton = document.getElementsByClassName("confirm")[0];
    var str = document.getElementById("name").innerHTML;
    changeButton.onclick = function(){
        // 更换显示图片
        var img_now = document.getElementsByClassName("img_now")[0];
        // 更换
        img_now.src = "/static/user_head/" + str  + '/' + name;
    };

    confirmButton.onclick = function(){
        var aDom = document.getElementsByClassName("a_confirm")[0];
        // 给a标签设置href属性
        aDom.href = '/chat/homelogin/?img=' + name;
    };
}

// // 进行图片懒加载
// function lazyLoad(){
//     // 拿到所有box
//     var boxDom = document.querySelectorAll("#wrapper .w_body .box");
//     var arrBox = [].slice.call(boxDom);
//
// }