// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import router from './router'
import '../static/common.css'
//导入全局的geetest.js
import '../static/gt.js'
//引入axios
import Axios from 'axios'
import * as api from './restful/api'

//将siteHeader 注册成全局组件
import siteHeader from '@/components/siteHeader/siteHeader'

Vue.component(siteHeader.name, siteHeader);
//将axios挂载到api上
Vue.prototype.$http = api;

Vue.config.productionTip = false;

Vue.use(ElementUI);
//引入vue-cookies
import VueCookies from 'vue-cookies'

//导入store实例
import store from './store/index'

Vue.use(VueCookies);
/* eslint-disable no-new */

//全局导航守卫
router.beforeEach((to, from, next) => {
    // ...

    if (VueCookies.isKey('access_token')) {
        let user = {
            username: VueCookies.get('username'),
            shop_cart_num: VueCookies.get('shop_cart_num'),
            access_token: VueCookies.get('access_token'),
            avatar: VueCookies.get('avatar'),
            notice_num: VueCookies.get('notice_num')
        };
        store.dispatch('getUser', user)
    }
    next()

});

new Vue({
    el: '#app',
    router,
    store,
    components: {App},
    template: '<App/>'
});
