var pricenum = new Vue({
    el: '#product-spuc',
    data: {
        num: 1,
        cart_id: ''
    },
    methods: {

        // 加入购物车
        goodDetailAddCart(){
            // 加入购物车方法
            let sendData= new URLSearchParams()
            let num = this.num;
            let goods = document.getElementById("id_goods").value;
            let sku = document.getElementById("id_sku").value;
            sendData.append('num', num)
            sendData.append('spu', goods)
            sendData.append('sku', sku)
            let url = '/order/cart_create/'
            axios.post(url, sendData, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                }
            }).then(res => {
                if (res.data.code == 2001 && res.data.message) {
                    this.$buefy.toast.open({
                        duration: 2000,
                        message: res.data.message,
                        type: 'is-success'
                    });
                    // 2000毫秒后刷新页面
                    setTimeout("window.location.reload()", 2000)
                } else if (res.data.code == 10010) {
                    this.$buefy.toast.open({
                        duration: 2000, 
                        message: res.data.message,
                        type: 'is-success'
                    });
                    // 2000毫秒后刷新页面
                    setTimeout("window.location.href = '/users/login/'", 2000)
                }
            }).catch(err => {
                console.log(err.response)
            })
        },

        // 加入购物车直接跳转到下单页面
        productBuyCart(){
            // 加入购物车方法
            let sendData= new URLSearchParams()
            let num = this.num;
            let goods = document.getElementById("id_goods").value;
            let sku = document.getElementById("id_sku").value;
            sendData.append('num', num)
            sendData.append('spu', goods)
            sendData.append('sku', sku)
            let url = '/order/cart_create/'
            axios.post(url, sendData, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                }
            }).then(res => {
                if (res.data.code == 2001 && res.data.message) {
                    this.cart_id = res.data.cart_id;
                    window.location.href="/order/buynow/" + '?cart_id=' + this.cart_id ;
                } else if (res.data.code == 10010) {
                    this.$buefy.toast.open({
                        duration: 2000, 
                        message: res.data.message,
                        type: 'is-danger'
                    });
                    // 2000毫秒后跳转到登录页
                    setTimeout("window.location.href = '/users/login/'", 2000)
                    // console.log(res)
                }
            }).catch(err => {
                console.log(err.response)
            })
            
        },
    },
});


// 商品收藏
var productfav = new Vue({
    el: "#product-fav",
    delimiters: ['[[', ']]'],
    data: {
        product_id: '',
        text: '收藏',
    },
    methods: {
        addfav() {
            request({
                url: '/users/add_fav/',
                method: 'post',
                data: "object_id="+this.product_id
            }).then(res => {
                if (res.status == 100 && res.code == 'ok'|| res.status == 200 && res.code == 'ok') {
                    this.$buefy.toast.open({
                        duration: 2000,
                        message: res.message,
                        type: 'is-success',
                        pauseOnHover: true
                    })
                };
                this.text = "已收藏";
            })
        }
    },
    mounted() {
        this.product_id = document.getElementById("id_goods").value;
        request({
            url: '/users/get_fav/'+this.product_id+'/',
            method: 'get',
        }).then(res => {
            // console.log(res.text)
            this.text = res.text
        })
    },
})