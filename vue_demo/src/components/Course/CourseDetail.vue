<template>
    <div class="wrap">
        <div class="web-course-banner">
            <div class="container">
                <div class="title">
                    <img src="../../../static/images/play.png" height="67" width="67" alt="">
                    <h1 class="course-title">{{ course_info.name }}</h1>
                </div>
                <span class="course-text">{{ course_info.course_slogan }}</span>
                <div class="course-list">
                    <ul>
                        <li class="detail-item">
                            难度：{{ course_content.level }}
                        </li>
                        <li class="sep"></li>
                        <li class=detail-item>时长：{{ course_content.studyalltime }}小时</li>
                        <li class="sep"></li>
                        <li class=detail-item>学习人数：{{ course_content.learnnumber }}人</li>
                        <li class="sep"></li>
                        <li class=detail-item>评分 {{ course_info.course_review }}</li>
                    </ul>
                </div>
            </div>
        </div>
        <div class="course-review">
            <ul class="review-head-wrap">
                <li class="head-item">课程概述</li>
                <li class="head-item">课程章节</li>
                <li class="head-item">用户评价(10)</li>
                <li class="head-item">常见问题</li>

            </ul>
        </div>
        <!-- 课程详情 -->
        <div class="course-detail">
            <div class="container">
                <div class="course-detail-text">
                    <h3>课程概述</h3>
                    <p>
                        {{ course_content.brief }}
                    </p>
                </div>
                <div class="course-img">
                    <img src="https://www.luffycity.com/static/img/web-introduce.d075499.png" alt="">
                </div>
            </div>
        </div>
        <div class="course-price">
            <div class="container">
                <span>可以根据不同的学习情况购买不一样的学习套餐哦！</span>
                <ul class="course-price-item">
                    <li @click="courseClick(index)" v-for="(item,index) in course_content.prices" :key="item.id"
                        :class="{active:index===currentCourse_id}">
                        <p class="price" :class="{active:index===currentCourse_id}">¥{{ item.price }}</p>
                        <p class="time" :class="{active:index===currentCourse_id}">有效期{{ item.valid_period_name }}</p>
                    </li>
                </ul>
                <div class="course-action">
                    <button class="left">购买</button>
                    <button class="right" @click="addShopCart">加入购物车</button>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
    export default {

        name: 'CourseDetail',
        data() {
            return {
                course_content: {},
                currentCourse_id: null,
                course_info: {},
                prices:[], //价格套餐
            }
        },
        methods: {
            ajaxrequest() {
                let course_id = this.$route.params.courseId;
                this.$http.courseDetail(course_id)
                    .then((res) => {
                        console.log(res);
                        if (res.error_no === 0) {
                            this.course_content = res.data;
                            this.prices = res.data.prices;
                        }
                    })
                    .catch((err) => {
                        console.log('获取列表失败', err)
                    })
            },
            courseClick(index) {
                if (index === this.currentCourse_id) {
                    this.currentCourse_id = null
                } else {
                    this.currentCourse_id = index
                }
            },
            addShopCart() {
                //1.如果用户没有选中价格套餐，提示用户 “您没有选择要加入的套餐哦”
                //2.点击购物车按钮,如果用户选中套餐（判断当前用户有登录(token)  vue-cookies）
                // 2.1 如果用户未登录（未产生token）
                //编程式导航 跳转登录页面
                if (this.currentCourse_id !== null) {
                    if (this.$cookies.isKey("access_token")) {
                        let params = {
                            courseId: this.$route.params.courseId,
                            validPeriodId: this.prices[this.currentCourse_id].valid_period
                        };
                        /**后端的逻辑 难点 */
                        this.$https.shopCart(params)
                            .then(res => {
                                if (res.error_no === 10) {
                                    this.$message({
                                        message: "更新套餐成功",
                                        type: 'success',
                                        duration: 1200
                                    });
                                }
                                if (res.error_no === 0) {
                                    this.$message({
                                        message: "加入购物车成功",
                                        type: 'success',
                                        duration: 1200
                                    });
                                }
                            })

                    } else {
                        this.login()
                    }


                } else {
                    this.$message({
                        message: '还未选择套餐',
                        type: 'warning',
                        duration: 1200
                    });
                }
            },
            login() {
                this.$router.push({
                    path: 'login',
                    name: 'Login',
                    params: {}

                })
            },
            courseInfo() {
                let course_id = this.$route.params.courseId;
                this.$https.courseDetailInfo(course_id)
                    .then((res) => {
                        console.log(res);
                        if (res.error_no === 0) {
                            this.course_info = res.data;
                        }
                    })
                    .catch((err) => {
                        console.log('获取列表失败', err)
                    })
            }


        },
        created() {
            this.ajaxrequest();
            this.courseInfo()
        }

    };
</script>

<style lang="css" scoped>
    .wrap {
        width: 100%;
    }

    .web-course-banner {
        width: 100%;
        height: 512px;
        background: url(../../../static/images/web-banner.1402933.png) no-repeat;
        background-size: 100% 100%;
        text-align: center;
        overflow: hidden;
    }

    .container {
        width: 1200px;
        margin: 182px auto 0;
        text-align: left;
    }

    .container img {
        vertical-align: middle;
    }

    .container h1 {
        display: inline-block;
        font-size: 48px;
        color: #4a4a4a;
        letter-spacing: .37px;
        margin-left: 40px;
        font-family: PingFangSC-Light;
        font-weight: 500;
        line-height: 1.1;
        position: relative;
        top: 10px;
    }

    .course-text {
        width: 464px;
        display: inline-block;
        font-size: 22px;
        color: #4a4a4a;
        letter-spacing: .17px;
        line-height: 36px;
        margin-top: 33px;
    }

    .course-list {
        width: 100%;
    }

    .course-list ul {
        margin-top: 63px;
        display: flex;
        align-items: center;
        justify-content: flex-start;
    }

    .course-list ul li.detail-item {
        font-size: 18px;
        color: #4a4a4a;
        letter-spacing: .74px;
        height: 26px;
        padding: 0 20px;
    }

    .course-list ul li.sep {
        width: 2px;
        height: 14px;
        border-left: 1px solid #979797;
    }

    .course-review {
        width: 100%;
        height: 80px;
        background: #fafbfc;
        border-top: 1px solid #e8e8e8;
        box-shadow: 0 1px 0 0 #e8e8e8;
    }

    .review-head-wrap {
        width: 590px;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
    }

    .review-head-wrap .head-item {
        height: 80px;
        line-height: 80px;
        font-size: 16px;
        color: #555;
        cursor: pointer;
    }

    .course-detail {
        width: 100%;
        padding-top: 90px;

    }

    .course-detail .container {
        width: 1200px;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
    }

    .course-detail-text {
        width: 500px;
        text-align: left;

    }

    .course-detail-text h3 {
        padding: 20px 0;
    }

    .course-detail-text p {
        width: 100%;
        height: 196px;
        font-size: 14px;
        color: #4A4A4A;
        letter-spacing: 1.83px;
        line-height: 30px;
        text-align: left;
    }

    .course-price {
        width: 100%;
        background: #FAFAFA;

    }

    .course-price .container {
        width: 1200px;
        margin: 0 auto;
        text-align: center;
    }

    .course-price span {
        font-size: 12px;
        color: #9b9b9b;
        letter-spacing: 1.57px;
        display: inline-block;
        margin-top: 102px
    }

    .course-price ul {
        /*width: 800px;*/
        margin: 50px auto;

        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
    }

    .course-price ul li {
        cursor: pointer;
        width: 200px;
        height: 112px;
        border: 1px solid #979797;
    }

    .course-price ul li.active {
        background: #7ed321;
    }

    .course-price ul li p:first-child {
        font-size: 24px;
        letter-spacing: 1.92px;
        color: #333;
        margin-top: 17px;
    }

    .course-price ul li p:nth-child(2) {

        color: #9b9b9b;
        font-size: 20px;
        letter-spacing: 1.6px;
        margin-top: 9px;
    }

    .course-price ul li p.active {
        color: #fff;
    }

    .course-action {
        width: 1000px;
        margin: 0 auto;
        padding-bottom: 80px;
        display: flex;
        justify-content: center;
    }

    .course-action button {
        border: none;
        outline: none;
        cursor: pointer;
        display: inline-block;
        width: 181px;
        height: 51px;
        font-size: 14px;
        color: #fff;
        letter-spacing: 1.12px;
        text-align: center;
        background: #f5a623;
        border-radius: 82px;
    }

    .course-action button.left {
        background: #7ed321;
        box-shadow: 0 2px 4px 0 #e8e8e8;
        color: #fff;
        margin-right: 48px;
        padding: 0 20px;
    }

    .course-action button.right {
        background: #f5a623 url() no-repeat 125px 15px !important;
    }


</style>
