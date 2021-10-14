var product_content = new Vue({
    el: "#product-content",
    data: {
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
    }
})