// 用于从cookie中匹配 csrftoken值
var regex = /.*csrftoken=([^;.]*).*$/;  


//封装一个获取元素的id的函数
function byId(id){
	return typeof(id) === "string"?document.getElementById(id):id;	
}

if (byId("cart_json")){
    var cart_json = byId("cart_json").innerText
    var data = JSON.parse(cart_json)
}
if (byId("specs")) {
    var specs = byId("specs").innerText
    var productAttr = JSON.parse(specs)
}

if (byId("spec_sku")) {
    var spec_sku = byId("spec_sku").innerText
    console.log(spec_sku)
    var productValue = JSON.parse(spec_sku)
}

new Vue({
    el: '#app',
    // 修改Vue变量的读取语法，避免与django冲突
    delimiters: ['<<', '>>'],
    data: {
        // head
        navigation: 'home',
        // navbar
        hoverable: true,
        // index banner
        pauseHover: true,  // 鼠标移动到轮播图是否暂停 
        pauseInfo: false,  // 鼠标移动到轮播图是否显示暂停提示文字
        indicatorStyle: 'is-lines', // 轮播指示器的样式 is-boxes[方形], is-dots[圆形],is-lines[长方形]
        // 商品详情评分 good_content rate
        rate: 4.6,
        maxs: 5,
        sizes: '',
        packs: 'mdi',
        icons: 'star',
        score: true,
        custom: '',
        text: false,
        texts: ['Very bad', 'Bad', 'Good', 'Very good', 'Awesome'],
        isRtl:false,
        isSpaced: false,
        isDisabled: true,
        locale: undefined, // Browser locale
        // 商品详情 good_content tabs
        activeTab: 0,
        showBooks: false,
        // 商品详情购买起始数量 good_price
        num: 1,
        // 全站顶部购物车 cart
        open: false,
        overlay: true,
        fullheight: true,
        fullwidth: false,
        right: true,
        // product-detail
        checkboxGroup: [],
        radioButton: '',
        // productAttr: spec_json,
        productAttr: productAttr,
        productValue: productValue,
        attrSelected: [],
        attrValueSelected: null,
        count: 1,
        stock: 1,
        market_price: 0,
        shop_price:0,
        product_unit:'',
        sku_id:''
    },

    watch: {
        productAttr: {
          immediate: true,
          handler(attr) {
            attr.forEach((value, index) => {
              this.attrSelected[index] = value.spec_options[0];
            });
          }
        },
        attrSelected: {
          immediate: true,
          handler(attr) {
            if (attr.length) {
              let name = attr.join(),
                value = this.productValue[name];
              if (value) {
                this.attrValueSelected = value;
                this.stock = value.sku_stock;
                this.market_price = value.sku_market_price;
                this.shop_price = value.sku_shop_price;
                this.product_unit = value.sku_product_unit;
                this.sku_id = value.sku_id;
                // this.unique = value.unique;
              }
            } else {
              this.stock = this.storeInfo.stock;
            }
          }
        }
      },

    methods: {
        // 封装axios
        request(config){
            const instance = axios.create({
                // baseURL: 'https://some-domain.com/api/',
                timeout: 5000,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1],
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                }
            });
            return instance(config)
        },
        // 封装axios END

        /************ 商品详情页加入购物车 *************/
        goodDetailAddCart(){
            // 加入购物车方法
            let sendData= new URLSearchParams()
            let num = this.num;
            let goods = byId("id_goods").value;
            sendData.append('num', num)
            sendData.append('sku', goods)
            this.request({
                url: "/order/shoping_cart_create/",
                method: 'post',
                data: sendData
            }).then(res => {
                // console.log(res)
                if (!res.data.code && typeof res.data == 'string'){
                    this.$buefy.toast.open({
                        duration: 5000,
                        message: '宝贝，请登陆后再操作哟！',
                        type: 'is-danger'
                    })
                }else if (res.data.code == 2001 && res.data.message || res.data.code == 10010) {
                    this.$buefy.toast.open({
                        duration: 5000,
                        message: res.data.message,
                        type: 'is-success'
                    });
                    // window.location.reload();
                } 
            }).catch(err => {
                console.log(err.response)
            })
        },
        /************ 商品详情页加入购物车 END *************/
        
        ceshi(){
            console.log(this.productAttr)
        }


    },
})

