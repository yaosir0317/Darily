import Axios from 'axios'
import VueCookies from 'vue-cookies'
//设置公共的url
Axios.defaults.baseURL = 'http://127.0.0.1:8000/api/v1';
const categoryListUrl = '/course_sub/category/list/';
const courseListUrl = '/courses/?sub_category=';
const courseDetailUrl ='/courses/';
const courseDetailInfoUrl ='/coursedetailtop/?courseid=';
const slideCheckUrl ='/captcha_check/';
const loginUrl = '/account/login/';
const user_shop_cart_url = '/user/shop_cart/create/';
const shop_cart_list_url = '/user/shop_cart/list/';
const shop_cart_update_url = '/user/shop_cart/update/';
const shop_cart_remove_url = '/user/shop_cart/remove/';


//请求拦截器
Axios.interceptors.request.use(function (config) {
    // 在发送请求之前做些什么
    if(VueCookies.isKey('access_token')){
        //有问题？
       config.headers.Authorization = VueCookies.get('access_token');
    }

    return config;
  }, function (error) {
    // 对请求错误做些什么
    return Promise.reject(error);
  });


export function categoryList(){
    return  Axios.get(categoryListUrl).then(res=>res.data)
}
export function courseList(categoryId){
    return  Axios.get(`${courseListUrl}${categoryId}`).then(res=>res.data)
}
export function courseDetail(courseId){
    return  Axios.get(`${courseDetailUrl}${courseId}/details-introduce`).then(res=>res.data)
}
export function courseDetailInfo(courseId){
    return  Axios.get(`${courseDetailInfoUrl}${courseId}`).then(res=>res.data)
}
export function slideToCheck(){
    return  Axios.get(slideCheckUrl).then(res=>res.data)
}
export function login(params){
    return Axios.post(`${loginUrl}`,params).then(res=>res.data)
}
export function shopCart(parmas){
    return Axios.post(`${user_shop_cart_url}`,parmas).then(res=>res.data)
}
//购物车列表的api
export function shopCartList(){
    return Axios.get(shop_cart_list_url).then(res=>res.data)
}
export function shopCartUpdate(params){
    return Axios.put(shop_cart_update_url,params).then(res=>res.data)
}
export function shopCartRemove(params){
    return Axios.delete(shop_cart_remove_url,{data:params}).then(res=>res.data)
}
