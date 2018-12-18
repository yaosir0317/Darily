<template>
    <div class="shopping-cart-wrap">
        <h3 class="shopping-cart-tit">
            我的购物车
            <small>共{{courseCount}}门课程</small>
        </h3>
        <div class="row">
            <el-table
                ref="multipleTable"
                :data="shopCartList"
                tooltip-effect="dark"
                style="width: 100%"
                @selection-change="handleSelectionChange"
            >
                <el-table-column type="selection" width="55"></el-table-column>
                <el-table-column label="课程" width="554">
                    <template slot-scope="scope">
                        <img :src="scope.row.courseImg" alt>
                        <a href="javascript:void(0)">{{scope.row.courseName}}</a>
                    </template>
                </el-table-column>
                <el-table-column prop="time" label="有效期" width="212">
                    <template slot-scope="scope">
                        <!-- 当select中的v-model的值 等于option的value值 默认选中 -->
                        <select v-model='scope.row.validPeriodId' @change='changeHandler(scope.row)'>
                            <option v-for='(item,index) in scope.row.validPeriodChoices' :key='index'
                                    :value='item.validPeriodId'>有效期{{item.validPeriod}}
                            </option>

                        </select>
                    </template>
                </el-table-column>
                <el-table-column prop="price" label="单价" show-overflow-tooltip>
                    <template slot-scope="scope">¥{{ scope.row.coursePrice}}</template>
                </el-table-column>
                <el-table-column prop="action" label="操作" show-overflow-tooltip>
                    <template slot-scope="scope">
                        <el-button
                            @click.native.prevent="deleteRow(scope.$index, shopCartList)"
                            type="text"
                            size="small"
                        >删除
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <div class="total">
            <el-button type="primary">去结算</el-button>
            <h3>总计: ¥{{totalPrice}}</h3>
        </div>
    </div>
</template>

<script>
    export default {
        name: "ShopCart",
        data() {
            return {
                shopCartList: [],
                multipleSelection: [],
                courseCount: 0
            };
        },
        computed: {
            totalPrice() {
                let total = 0;
                this.multipleSelection.forEach((el, index) => {

                    total += parseFloat(el.coursePrice)
                });
                return total;
            }
        },
        methods: {
            changeHandler(row) {

                //获取oldValidPeriodId
                let oldValidPeriodId;
                row.validPeriodChoices.forEach((el, index) => {
                    if (el.default) {
                        oldValidPeriodId = el.validPeriodId
                    }
                });
                //put请求的 请求体的数据
                let params = {
                    courseId: row.courseId,
                    newValidPeriodId: row.validPeriodId,
                    oldValidPeriodId: oldValidPeriodId
                };
                console.log(params);
                this.$https.shopCartUpdate(params)
                    .then(res => {
                        if (res.error_no === 0) {

                            //更改有效期 套餐，后端返回相应的课程套餐，将原来的 课程列表的数据替换掉
                            this.shopCartList.forEach((el, index) => {
                                console.log(el);
                                if (el.courseId == res.data.courseId) {
                                    //替换操作
                                    this.shopCartList.splice(index, 1, res.data)
                                }
                            });
                            console.log(this.shopCartList)

                        }


                    })
            },
            //单选或多选的时候事件
            handleSelectionChange(val) {
                this.multipleSelection = val;
                console.log(this.multipleSelection);
            },
            getShopCartList() {
                this.$https.shopCartList().then(res => {
                    console.log(res);
                    if (res.error_no === 0) {
                        this.shopCartList = res.data.myShopCart;
                        this.courseCount = res.data.total
                    }
                });
            },
            //删除课程事件
            deleteRow(index, rows) {
                console.log(rows[index].courseId)
                console.log(rows[index].validPeriodId)

                //   rows.splice(index, 1);
                //ajax
                //.then    this.getShopCartList()

                let params = {
                    removeShopFromCart: [
                        {
                            course_id: rows[index].courseId,
                            valid_period_id: rows[index].validPeriodId
                        }
                    ]
                };

                this.$https.shopCartRemove(params)
                    .then(res => {
                        console.log(res);
                        if (res.error_no === 0) {
                            this.$message('删除课程成功');
                            this.getShopCartList();
                        }
                    })
                    .catch(err => {
                        console.log(err)
                    })


            }
        },
        created() {
            this.getShopCartList();
        }
    };
</script>

<style lang="css" scoped>
    .shopping-cart-wrap {
        width: 100%;
    }

    .shopping-cart-wrap h3,
    .row {
        width: 1200px;
        margin: 0 auto;
    }

    .shopping-cart-wrap h3 {
        padding: 50px 0;
    }

    .el-table .warning-row {
        background: #22c8c5;
    }

    .cell img {
        vertical-align: middle;
        width: 170px;
    }

    .cell a {
        color: #000;
        margin-left: 30px;
    }

    select {
        border: 0;
        outline: none;
        font-size: 12px;
        color: #666;
        line-height: 18px;
        width: 117px;
        height: 28px;
        padding-left: 16px;
        border: 1px solid #d9d9d9;
        border-radius: 4px;
    }

    .total {
        width: 1200px;
        margin: 0 auto;
        /*display: flex;*/
        /*justify-content:flex-end;*/
    }

    .shopping-cart-wrap .total button {
        float: right;
        margin-top: 20px;
    }

    .shopping-cart-wrap .total h3 {
        padding: 0;
        float: right;
        width: 150px;
        height: 30px;
        margin-top: 30px;
    }
</style>
