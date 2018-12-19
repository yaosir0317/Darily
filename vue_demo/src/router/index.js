import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home/Home'
import Course from '@/components/Course/Course'
import CourseDetail from '@/components/Course/CourseDetail'
import EasyCourse from '@/components/EasyCourse/EasyCourse'
import AcademicCourse from '@/components/AcademicCourse/AcademicCourse'
import QuestionBank from '@/components/QuestionBank/QuestionBank'
import PublishCourse from '@/components/PublishCourse/PublishCourse'
import TeachMaterials from '@/components/TeachMaterials/TeachMaterials'
import OldBoy from '@/components/OldBoy/OldBoy'
import Login from '@/components/Account/Login'
import ShopCart from '@/components/ShopCart/ShopCart'

Vue.use(Router);

export default new Router({
    mode: "history",  //  干掉地址栏里边的#号键
    linkActiveClass: 'is-active', //在路由的构造选项里配置默认类名为is-active
    routes:
        [
            {
                path: "/",
                redirect: "/home"

            },
            {
                path: "/home",
                name: "Home",
                component: Home
            },
            {
                path: "/course",
                name: "Course",
                component: Course,

            },
            {
                path: "/easy_course",
                name: "EasyCourse",
                component: EasyCourse,

            },
            {
                path: "/academic_course",
                name: "AcademicCourse",
                component: AcademicCourse,

            },
            {
                path: "/question_bank",
                name: "QuestionBank",
                component: QuestionBank,

            },
            {
                path: "/publish_course",
                name: "PublishCourse",
                component: PublishCourse,

            },
            {
                path: "/teach_materials",
                name: "TeachMaterials",
                component: TeachMaterials,

            },
            {
                path: "/old_boy",
                name: "OldBoy",
                component: OldBoy,

            },

            {
                path: "/courses/:detailId/details-introduce",
                name: "CourseDetail",
                component: CourseDetail,
            },

            {
                path: "/login",
                name: "Login",
                component: Login,
            },

            {
                path: "/purchase/shopping_cart",
                name: 'shop_cart',
                component: ShopCart
            }

        ]
})
