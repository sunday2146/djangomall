function showpic(winpic){
    if(!document.getElementById('MainPicture')) return false;
    var source = winpic.getAttribute('src');
    var oImg = document.getElementById('MainPicture');
    if(oImg.nodeName !='IMG') return false;
    oImg.setAttribute('src',source);
    // if(document.getElementById('description')){
    //     var description = document.getElementById('description');
    //     var text = winpic.getAttribute('title');
    //     description.firstChild.nodeValue = text;
    //     //description.innerHTML = text;
    // }
    return true;
}

function prepareGallery(){
    if(!document.getElementsByTagName) return false;
    if(!document.getElementById) return false;
    if(!document.getElementById('GoodsBanners')) return false;
    var gallery = document.getElementById('GoodsBanners');
    var links = gallery.getElementsByTagName('img');
    for(var i=0;i<links.length;i++){
        links[i].onmouseover = function(){
           //return showpic(this) ? return : false;
           showpic(this);
           return false;
        }
    }
}

prepareGallery();