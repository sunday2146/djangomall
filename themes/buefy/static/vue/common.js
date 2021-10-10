// 获取cookie
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

// 提取地址栏中的查询字符串
function get_query_string(name) {
    var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
    var r = window.location.search.substr(1).match(reg);
    if (r != null) {
        return decodeURI(r[2]);
    }
    return null;
}

// 生成uuid
function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}

// axios发送请求
function request(config) {
    const instance = axios.create({
        // baseURL: 'https://some-domain.com/api/',
        timeout: 5000,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
    });
    

    // 拦截请求
    instance.interceptors.request.use(
        config => {
            // console.log(config)
            return config;
        }, err => {
            console.log(err);
        })
    
    // 拦截响应
    instance.interceptors.response.use(
        res => {
            // console.log(res)
            if (res.data.code == 10010) {
                alert(res.data.message);
                window.location.href = '/users/login/';
            }
            return res.data
        }, err => {
            console.log(err)
        }
    )

    return instance(config);
}