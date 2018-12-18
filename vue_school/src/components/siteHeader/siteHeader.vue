<template>

    <el-container>
        <el-header height='80px'>
            <div class="header">
                <div class="nav-left">
                    <img src="https://www.luffycity.com/static/img/head-logo.a7cedf3.svg" alt="">
                </div>
                <div class="nav-center">
                    <ul>
                        <li @click="clickHander(item.id)" v-for="(item,index) in url_header" :key="item.id">
                            <router-link :to='{name:item.name}'>
                                {{ item.title }}
                            </router-link>
                        </li>
                    </ul>
                </div>

                <!-- <el-dropdown> -->
                <div class="nav-right" v-if="userInfo.access_token" @mouseenter="contentShow" @mouseleave="contentNone">
                    <span class='el-dropdown-link'>学习中心</span>
                    <span class="user">{{ userInfo.username }}</span>
                    <img :src="userInfo.avatar" alt="">
                    <ul class="my_account" v-show='isShow'>
                        <li>
                            我的账户
                            <i>></i>
                        </li>
                        <li>
                            我的订单
                            <i>></i>
                        </li>
                        <li>
                            我的优惠券
                            <i>></i>
                        </li>
                        <li>
                            我的消息<span class="msg">({{ userInfo.notice_num }})</span>
                            <i>></i>
                        </li>
                        <li @click='toShopCart'>
                            购物车<span class="count">({{ userInfo.shop_cart_num}})</span>
                            <i>></i>
                        </li>
                        <li @click="logout">
                            退出
                            <i>></i>
                        </li>
                    </ul>
                </div>
                <!-- </el-dropdown> -->
                <div class="nav-right" v-else>
                    <span @click="login">登录</span>
                    &nbsp;| &nbsp;
                    <span>注册</span>

                </div>
            </div>
        </el-header>
        <div>
            <router-view></router-view>
        </div>
    </el-container>


</template>

<script>
    export default {
        name: 'siteHeader',
        data() {
            return {
                url_header: [
                    {id: 0, title: '首页', name: "Home"},
                    {id: 1, title: '免费课程', name: "Course"},
                    {id: 2, title: '轻课', name: "EasyCourse"},
                    {id: 3, title: '学位课程', name: "AcademicCourse"},
                    {id: 4, title: '智能题库', name: "QuestionBank"},
                    {id: 5, title: '公开课', name: "PublishCourse"},
                    {id: 6, title: '内部教材', name: "TeachMaterials"},
                    {id: 7, title: '老男孩教育', name: "OldBoy"},
                ],
                header_id: 0,
                isShow: false,
            }
        },
        methods: {
            logout() {
                this.$cookies.remove("access_token");
                this.$store.state.userinfo = {}
            },
            contentShow() {
                this.isShow = true
            },
            contentNone() {
                this.isShow = false
            },
            clickHander(num) {
                this.header_id = num
            },
            login() {
                this.$router.push({
                    path: 'login',
                    name: 'Login',
                    params: {}

                })
            },
            toShopCart() {
                this.$router.push({
                    name: 'shop_cart'
                })
            }


        },
        components: {//局部注册组件这里，可能会定义多个组件，所以component这个单词加上“s”

        },
        computed: {
            userInfo() {
                console.log(this.$store.state.userinfo);
                // let userInfo = {
                //   access_token:this.$cookies.get('access_token'),
                //   notice_num:this.$cookies.get('notice_num'),
                //   shop_cart_num:this.$cookies.get('shop_cart_num'),
                //   avatar:this.$cookies.get('avatar'),
                //   username:this.$cookies.get('username')
                // }

                return this.$store.state.userinfo
            }
        }
    }
</script>

<style>

    .el-header {
        border-bottom: #c9c9c9;
        box-shadow: 0 0.5px 0.5px 0 #c9c9c9;
    }

    .header {
        width: 1200px;
        height: 80px;
        line-height: 80px;
        margin: 0 auto;
    }

    .nav-left {
        float: left;
        margin-top: 10px;
    }

    .nav-center {
        float: left;
        margin-left: 100px;

    }

    .nav-center ul {
        overflow: hidden;
    }

    .nav-center ul li {
        float: left;
        margin: 0 5px;
        /*width: 100px;*/
        padding: 0 15px;
        height: 80px;
        line-height: 80px;
        text-align: center;
    }

    .nav-center ul li a {
        color: #4a4a4a;
        width: 100%;
        height: 73px;
        display: inline-block;

    }

    .nav-center ul li a:hover {
        color: #B3B3B3;
    }

    .nav-right {
        float: right;
        position: relative;
        z-index: 100;

    }

    .nav-right span {
        cursor: pointer;
    }

    .nav-right .user {
        margin-left: 15px;
    }

    .nav-right img {
        width: 26px;
        height: 26px;
        border-radius: 50%;
        display: inline-block;
        vertical-align: middle;
        margin-left: 15px;
    }

    .nav-right ul {
        position: absolute;
        width: 221px;
        z-index: 100;
        font-size: 12px;
        top: 80px;
        background: #fff;
        border-top: 2px solid #d0d0d0;
        box-shadow: 0 2px 4px 0 #e8e8e8;
    }

    .nav-right ul li {
        height: 40px;
        color: #4a4a4a;
        padding-left: 30px;
        padding-right: 20px;
        font-size: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        cursor: pointer;
        transition: all .2s linear;
    }

    .nav-right ul li span.msg {
        margin-left: -80px;
        color: red;
    }

    .nav-right ul li span.count {
        margin-left: -100px;
        color: red;
    }

</style>
