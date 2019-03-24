import Vue from 'vue'
/*
1、导入对象
2.Vue.use()
3.创建store对象
4.挂载

*/
import Vuex from 'vuex'

Vue.use(Vuex);
const store = new Vuex.Store({
    state: {
        userinfo: {},//存储用户信息
    },
    mutations: {
        get_user(state, data) {
            state.userinfo = data;
        }
    },
    actions: {
        getUser(context, data) {
            context.commit('get_user', data);
        }
    }
});
export default store;
