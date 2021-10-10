// 导航
var navbar = new Vue({
    el: "#header",
    delimiters: ['<<', '>>'],
    data: {
        isRouterAlive: true,  // 控制视图是否显示
        navigation: 'home',
        // navbar
        hoverable: true,
        keyword: '',   // 搜索词
        // index banner
        pauseHover: true,  // 鼠标移动到轮播图是否暂停 
        pauseInfo: false,  // 鼠标移动到轮播图是否显示暂停提示文字
        indicatorStyle: 'is-lines', // 轮播指示器的样式 is-boxes[方形], is-dots[圆形],is-lines[长方形]
        // 全站顶部购物车 cart
        open: false,
        overlay: true,
        fullheight: true,
        fullwidth: false,
        right: true,
    },
    
    methods: {
        // 退出登录确认弹窗
        logout() {
            this.$buefy.dialog.confirm({
                message: '你确定要退出吗？',
                cancelText: '取消',
                confirmText: '确认',
                onConfirm: () => {
                    axios.get('/users/logout/').then(() => {
                        this.$buefy.toast.open('退出成功!')
                        setTimeout("window.location.reload()", 2000)
                        // window.location.href = '/users/login/';
                    })
                }
            })
        },

        // 搜索视图
        search() {
            axios.get("/users/search/",{
                params: {
                  keyword: this.keyword
                }
              }).then(res => {
                  console.log(res)
              })
        }
    },
});