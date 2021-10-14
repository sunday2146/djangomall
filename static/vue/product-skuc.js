//封装一个获取元素的id的函数
function byId(id) {
  return typeof (id) === "string" ? document.getElementById(id) : id;
}

if (byId("specs")) {
  var specs = byId("specs").innerText
  var productAttr = JSON.parse(specs)
}

if (byId("spec_sku")) {
  var spec_sku = byId("spec_sku").innerText
  var productValue = JSON.parse(spec_sku)
}

var product_skuc = new Vue({
  el: "#product-skuc",
  // 修改Vue变量的读取语法，避免与django冲突
  delimiters: ['[[', ']]'],
  data: {
    product_id: product_id,      // 当前商品id
    storeInfo: '',               // 商品数据
    productAttr: productAttr,
    productValue: productValue,
    attrSelected: [],
    attrValueSelected: null,
    default_image: '',
    count: 1,
    stock: 0,
    sales: 0,
    unique: "",
    market_price: 0,
    shop_price: 0,
    product_unit: '',
    sku_id: '',
    num: 1,
    min: 1,
    cart_id: '',
    text: '收藏',
  },

  methods: {
    getImageUrl(i) {
      this.default_image = this.storeInfo.slider_image[i]
    },
    defaultImageUrl() {
      this.default_image = this.storeInfo.image
    },

    addfav() {
	// 收藏事件
      request({
        url: '/users/add_fav/',
        method: 'post',
        data: "object_id=" + this.product_id
      }).then(res => {
        if (res.status == 100 && res.code == 'ok' || res.status == 200 && res.code == 'ok') {
          this.$buefy.toast.open({
            duration: 2000,
            message: res.message,
            type: 'is-success',
            pauseOnHover: true
          })
        };
		this.text = "已收藏";
      })
    },

    productDetailAddCart() {
      // 加入购物车方法
      let sendData = new URLSearchParams()
      let num = this.num;
      let spu = this.product_id;
      let sku = this.sku_id;
      sendData.append('num', num)
      sendData.append('spu', spu)
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

        } else if (res.data.code == 10010) {
          this.$buefy.toast.open({
            duration: 2000,
            message: res.data.message,
            type: 'is-danger'
          });
          // 2000毫秒后刷新页面
          setTimeout("window.location.href = '/users/login/'", 2000)
          // console.log(res)
        }
      }).catch(err => {
        console.log(err)
      })
    },

    // sku立即购买
    productDetailBuyNow() {
      // 加入购物车方法
      let sendData = new URLSearchParams()
      let num = this.num;
      let spu = this.product_id;
      let sku = this.sku_id;
      sendData.append('num', num)
      sendData.append('spu', spu)
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
          //   this.$buefy.toast.open({
          //     duration: 2000,
          //     message: res.data.message,
          //     type: 'is-success'
          //   });
          this.cart_id = res.data.cart_id;
          window.location.href = "/order/buynow/" + '?cart_id=' + this.cart_id;
        } else if (res.data.code == 10010) {
          this.$buefy.toast.open({
            duration: 2000,
            message: res.data.message,
            type: 'is-danger'
          });
          // 2000毫秒后刷新页面
          setTimeout("window.location.href = '/users/login/'", 2000)
          // console.log(res)
        }
        // setTimeout("window.location.reload()", 2000)
      }).catch(err => {
        console.log(err)
      })
    }
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
            this.sales = value.sku_sales;
            // this.unique = value.unique;
          } else {
            this.stock = 0;
          }
        }
      }
    }
  },

  created() {
    var self = this;
    axios.get('/product/product/' + self.product_id + '/json/').then(res => {
      self.storeInfo = res.data.storeInfo;
      // self.productAttr = res.data.productAttr;
      // self.productValue = res.data.productValue;
      self.default_image = res.data.storeInfo.image;
    })
  },

  mounted() {
    // 查看当前商品是否已经收藏
    request({
      url: '/users/get_fav/' + this.product_id + '/',
      method: 'get',
    }).then(res => {
      // console.log(res.text) 
      this.text = res.text
    })
  },
})
