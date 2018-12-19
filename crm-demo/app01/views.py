import random
from django import forms
from django.urls import reverse
from django.views import View
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.forms.models import modelformset_factory

import datetime
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from app01.utils.page import Pagination
from rbac.utils.rbac import initial_sesson
from app01.utils.form import UserInfoModelForm, CustomerModelForm, ConsultRecordModelForm,\
                                ClassStudyRecordModelForm, StudentStudyRecordModelForm
from app01.models import UserInfo, Customer, ConsultRecord, ClassStudyRecord,\
                                StudentStudyRecord, Permission, Role
from django.db.models import Count

# Create your views here.


# 登录装饰器

def login_required(func):
    def inner(request):
        if not request.user.id:
            return redirect("/login/")
        else:
            ret = func(request)
            return ret

    return inner


# 首页视图
@login_required
def index(request):
    return render(request, 'base/index.html', locals())


# 登录视图
def login(request):
    if request.method == 'GET':
        return render(request, 'base/login.html')
    else:
        # 获取用户名和密码
        username = request.POST.get("username")
        password = request.POST.get("password")
        code = request.POST.get("code")
        # 数据库查询该用户是否存在
        # authenticate去auth_user查询记录，查询成功返回用户对象，查询失败返回None
        # Ajax请求返回一个字典
        response = {"user": None, "err_user": "", "err_code": ""}
        if code.upper() == request.session.get("keep_str").upper():
            user_obj = auth.authenticate(username=username, password=password)
            if user_obj:
                # 保存用户状态信息
                auth.login(request, user_obj)
                initial_sesson(username, request)
                response["user"] = username
            else:
                response['err_user'] = "用户名或者密码错误！"

        else:
            response["err_code"] = "验证码错误！"
        return JsonResponse(response)


# 验证码视图
def get_valid_img(request):
    # 随机颜色
    def get_random_color():
        return (
            random.randint(
                0, 255), random.randint(
                0, 255), random.randint(
                0, 255))

    #
    # img=Image.new("RGB",(350,38),get_random_color())
    # f=open("valid.png","wb")
    # img.save(f,"png")
    # with open("valid.png","rb") as f:
    #     data=f.read()

    # 方式3：
    # img=Image.new("RGB",(350,38),get_random_color())
    # f=BytesIO()
    # img.save(f,"png")
    # data=f.getvalue()

    # # 方式4:完善文本
    #
    # img=Image.new("RGB",(350,38),get_random_color())
    # draw=ImageDraw.Draw(img)
    # font=ImageFont.truetype("static/font/kumo.ttf",32)
    # draw.text((0,0),"python!",get_random_color(),font=font)
    #
    # # 写与读
    # f=BytesIO()
    # img.save(f,"png")
    # data=f.getvalue()

    # 方式5:
    # 颜色方式  宽高  颜色值
    img = Image.new("RGB", (130, 40), get_random_color())
    # 图片上写文字
    draw = ImageDraw.Draw(img)
    # 文字的字体类型与字号
    font = ImageFont.truetype("static/font/kumo.ttf", 32)

    keep_str = ""
    # 生成字母数字混合验证码 n 位
    n = 5
    for i in range(n):
        random_num = str(random.randint(0, 9))  # 数字
        random_lowalf = chr(random.randint(97, 122))  # 小写字母
        random_upperalf = chr(random.randint(65, 90))  # 大写字母
        random_char = random.choice(
            [random_num, random_lowalf, random_upperalf])
        # 图片中文字的位置(x,y)  文字内容   颜色   字体
        draw.text((i * 25, 0), random_char, get_random_color(), font=font)
        # 字符串拼接用于登录时校验---验证码
        keep_str += random_char

    # 添加噪点
    width = 130
    height = 40
    # 线
    for i in range(3):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=get_random_color())

    # 点
    for i in range(5):
        draw.point([random.randint(0, width), random.randint(
            0, height)], fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())
    # 写与读
    f = BytesIO()  # 内存
    img.save(f, "png")  # 保存图片到内存中
    data = f.getvalue()  # 读取图片

    print('keep_str', keep_str)

    # 将验证码存在各自的session中

    request.session['keep_str'] = keep_str

    return HttpResponse(data)


# 注册信息校验
class UserForm(forms.Form):
    # 错误提示
    msg = {"min_length": "长度不能小于5", "required": "内容不能为空"}
    # 用户名校验
    username = forms.CharField(
        min_length=5,
        error_messages={
            "min_length": "长度不能小于5",
            "required": "用户名不能为空"},
    )
    # 密码校验
    password = forms.CharField(error_messages=msg,
                               min_length=5,
                               )
    # 二次密码
    r_pwd = forms.CharField(error_messages=msg,
                            min_length=5,
                            )
    # 邮箱校验
    email = forms.EmailField(
        error_messages={
            "invalid": "邮箱格式错误",
            "required": "内容不能为空",
            "min_length": "长度不能小于5"},
        min_length=5,
    )

    # 钩子校验用户名是否存在
    def clean_username(self):
        val = self.cleaned_data.get("username")
        ret = UserInfo.objects.filter(username=val).first()
        if not ret:
            return val
        else:
            raise ValidationError("用户名已存在！")

    # 钩子校验密码格式
    def clean_password(self):
        val = self.cleaned_data.get("password")
        if val.isdigit():
            raise ValidationError("密码不能是纯数字！")
        else:
            return val

    # 钩子校验邮箱格式
    # def clean_email(self):
    #
    #     val = self.cleaned_data.get("email")
    #     ret = re.search(r'.*(@163.com)', val)
    #     if not ret:
    #         raise ValidationError("请输入163邮箱")
    #     else:
    #         return val

    # 全局钩子校验两次密码是否一致
    def clean(self):

        pwd = self.cleaned_data.get("password")
        r_pwd = self.cleaned_data.get("r_pwd")

        if pwd and r_pwd:
            if pwd == r_pwd:
                return self.cleaned_data
            else:
                raise ValidationError("两次密码不一致！")
        else:
            return self.cleaned_data


# 注册视图
def register(request):
    if request.method == "POST":
        print(request.POST)

        # 数据校验
        form = UserForm(request.POST)
        if form.is_valid():  # 注册信息校验通过
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            print('================', form.cleaned_data)
            # 信息写入数据库
            UserInfo.objects.create_user(
                username=username,
                password=password,
                email=email)
            response = {"state": 1001}
            return JsonResponse(response)
        else:  # 注册信息校验未通过

            errors = form.errors
            response = {"state": 1002, 'errors': errors}
            print("------>", form.errors.get("__all__"))
            # 获取错误信息
            if form.errors.get('username'):
                username_error = form.errors.get('username')[0]
            else:
                username_error = ''
            if form.errors.get('email'):
                email_error = form.errors.get('email')[0]
            else:
                email_error = ''
            if form.errors.get('password'):
                password_error = form.errors.get('password')[0]
            else:
                password_error = ''
            if form.errors.get('r_pwd'):
                r_pwd = form.errors.get('r_pwd')[0]
            else:
                r_pwd = ''
            print(username_error, email_error, password_error, r_pwd)
            response = {
                "state": 1002,
                'errors': errors,
                'g_error': "",
                'username_error': username_error,
                'email_error': email_error,
                'password_error': password_error,
                'r_pwd': r_pwd}
            if form.errors.get("__all__"):
                g_error = form.errors.get("__all__")[0]
                response = {
                    "state": 1002,
                    'errors': errors,
                    'g_error': g_error,
                    'username_error': username_error,
                    'email_error': email_error,
                    'password_error': password_error,
                    'r_pwd': r_pwd}
            return JsonResponse(response)

    else:
        form = UserForm()
        return render(request, 'base/login.html', locals())


# 退出登录视图
def logout(request):
    auth.logout(request)
    return redirect("home")


# modelform注册
def model(request):
    if request.method == 'GET':
        form = UserInfoModelForm()
        return render(request, 'base/register.html', {'form': form})
    else:
        form = UserInfoModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request, 'base/register.html', {'form': form})


# 客户展示
class CustomerTableView(View):

    # 过滤显示公共客户以及所属当前账号的客户
    @method_decorator(login_required)
    def get(self, request):
        if reverse("customer_table") == request.path:
            label = 'Publish Customer List'
            customer_list = Customer.objects.filter(consultant__isnull=True)
        else:
            label = 'My Customer List'
            customer_list = Customer.objects.filter(consultant=request.user)

        # 搜索
        val = request.GET.get('q')  # 获取搜索条件
        field = request.GET.get('field')  # 获取搜索范围
        if val:
            q = Q()
            q.children.append((field + "__contains", val))  # 注意必须是元组
            customer_list = customer_list.filter(q)

        # 分页 注意分页应用了切片,但是一旦切片就不能再filter
        current_page_num = request.GET.get("page")
        pagination = Pagination(
            current_page_num,
            customer_list.count(),
            request,
            per_page_num=5)
        customer_list = customer_list[pagination.start:pagination.end]

        # 返回请求路径的获取
        path = request.path
        next_path = "?next=%s" % path

        return render(request,
                      'customer/site_customer_table.html',
                      {"customer_list": customer_list,
                       "pagination": pagination,
                       'next_path': next_path,
                       'label': label})

    # 批量处理
    def post(self, request):
        func_str = request.POST.get('action')  # 获取批量处理的函数名
        data = request.POST.getlist('selected_pk_list')  # 获取批量处理的客户列表
        # 不存在此函数
        if not hasattr(self, func_str):
            return HttpResponse('非法输入')
        # 有此函数执行
        else:
            func = getattr(self, func_str)
            queryset = Customer.objects.filter(pk__in=data)
            res = func(request, queryset)
            if res == 101:
                return HttpResponse('手慢了!,已经被抢走了')
            elif res == 102:
                return HttpResponse('他已经给不了你更多了!')
            elif res == 103:
                return HttpResponse('他已经没人要了你还想怎样!')
            else:
                return redirect(request.path)

    # 批量删除映射函数
    def patch_delete(self, request, queryset):
        queryset.delete()

    # 批量公共客户转换私人客户映射函数
    def patch_reverse(self, request, queryset):
        if queryset.filter(consultant=None):
            queryset.update(consultant=request.user)
        elif queryset.filter(consultant=request.user):
            return 102
        else:
            return 101

    # 批量私人客户转换公共客户映射函数
    def patch_remove(self, request, queryset):
        if queryset.filter(consultant=None):
            return 103
        else:
            queryset.update(consultant=None)


@login_required
def customer_table_all(request):
    cus_list = Customer.objects.all()
    return render(request, 'customer/all_customer.html', {'cus_list': cus_list})


# 添加/删除客户
class AddEditCustomerTable(View):

    # edit_id为空则是添加,不为空则为编辑
    def get(self, request, edit_id=None):
        edit_obj = Customer.objects.filter(pk=edit_id).first()
        form = CustomerModelForm(instance=edit_obj)
        return render(request, 'customer/customer_add_edit.html', {
                      'form': form, "edit_obj": edit_obj})

    def post(self, request, edit_id=None):
        edit_obj = Customer.objects.filter(pk=edit_id).first()
        form = CustomerModelForm(request.POST, instance=edit_obj)
        if form.is_valid():
            form.save()
            return redirect(request.GET.get("next"))
        else:
            return render(
                request, 'customer/customer_add_edit.html', {
                    'form': form, "edit_obj": edit_obj})


# 删除客户
class CustomerTableDelete(View):

    @method_decorator(login_required)
    def get(self, request, del_id):
        Customer.objects.filter(pk=del_id).delete()
        print(request.path)
        return redirect('/customer_table/')


# 跟进记录展示
class ConsultRecordView(View):

    @method_decorator(login_required)
    def get(self, request):
        # 返回请求路径的获取
        path = request.path
        next_path = "?next=%s" % path
        consult_record_list = ConsultRecord.objects.filter(
            consultant=request.user)
        customer_id = request.GET.get("customer_id")
        if customer_id:
            consult_record_list = consult_record_list.filter(
                customer_id=customer_id)

        return render(
            request, "consultrecord/consultrecord.html", {
                "consult_record_list": consult_record_list, "next_path": next_path})


# 添加/编辑跟进记录
class AddEditConsultRecords(View):

    # edit_id为空则是添加,不为空则为编辑
    def get(self, request, edit_id_record=None):
        edit_obj = ConsultRecord.objects.filter(pk=edit_id_record).first()
        edit_record = ''
        if edit_obj:
            edit_record = edit_obj.customer.pk  # 当前编辑的记录所属客户的id
        form = ConsultRecordModelForm(
            request, edit_record, instance=edit_obj)  # 实例化转给form
        return render(request, 'consultrecord/consultrecord_add_edit.html',
                      {'form': form, "edit_obj": edit_obj})

    def post(self, request, edit_id_record=None):
        edit_obj = ConsultRecord.objects.filter(pk=edit_id_record).first()
        edit_record = ''
        if edit_obj:
            edit_record = edit_obj.customer.pk  # 当前编辑的记录所属客户的id
        form = ConsultRecordModelForm(
            request,
            edit_record,
            request.POST,
            instance=edit_obj)  # 实例化转给form
        if form.is_valid():
            form.save()
            return redirect(request.GET.get("next"))
        else:
            return render(
                request, 'consultrecord/consultrecord_add_edit.html', {
                    'form': form, "edit_obj": edit_obj})


# 记录删除
class ConsultRecordsDelete(View):

    def get(self, request, del_id):
        ConsultRecord.objects.filter(pk=del_id).delete()
        return redirect(reverse('ConsultRecordView'))


# 班级课程记录
class ClassStudyRecordView(View):

    def get(self, request):
        path = request.path
        next_path = "?next=%s" % path
        class_study_list = ClassStudyRecord.objects.all()
        return render(
            request, "study/ClassStudy.html", {
                "class_study_list": class_study_list, "next_path": next_path})

    # 批量处理
    def post(self, request):
        func_str = request.POST.get('action')  # 获取批量处理的函数名
        data = request.POST.getlist('selected_pk_list')  # 获取批量处理的课程列表
        # 不存在此函数
        if not hasattr(self, func_str):
            return HttpResponse('非法输入')
        # 有此函数执行
        else:
            func = getattr(self, func_str)
            func(request, data)
            return self.get(request)

    # 批量生成学生学习记录
    def patch_generate(self, request, data):
        # 批量创建学生学习记录
        try:
            for class_study_record_pk in data:
                class_study_record_obj = ClassStudyRecord.objects.filter(pk=class_study_record_pk).first()
                student_list = class_study_record_obj.class_obj.students.all()
                print("student_list", student_list)

                for student in student_list:
                    StudentStudyRecord.objects.create(student=student, classstudyrecord=class_study_record_obj)
        except Exception as e:
            pass

    # 批量删除学生学习记录
    def patch_detete(self, request, queryset):
        pass


# 添加/班级班级课程记录
class AddEditClassStudyRecord(View):

    # edit_id为空则是添加,不为空则为编辑
    def get(self, request, edit_id_record=None):
        edit_obj = ClassStudyRecord.objects.filter(pk=edit_id_record).first()
        form = ClassStudyRecordModelForm(instance=edit_obj)  # 实例化转给form
        return render(
            request, 'study/ClassStudyRecord_add_edit.html', {
                'form': form, "edit_obj": edit_obj})

    def post(self, request, edit_id_record=None):
        edit_obj = ClassStudyRecord.objects.filter(pk=edit_id_record).first()
        form = ClassStudyRecordModelForm(
            request.POST, instance=edit_obj)  # 实例化转给form
        if form.is_valid():
            form.save()
            return redirect(request.GET.get("next"))
        else:
            return render(
                request, 'study/ClassStudyRecord_add_edit.html', {
                    'form': form, "edit_obj": edit_obj})


# 删除班级课程记录
class ClassStudyRecordDelete(View):

    def get(self, request, del_id):
        ClassStudyRecord.objects.filter(pk=del_id).delete()
        return redirect(reverse('ClassStudyRecordView'))


# 给当前课程的学生批量添加成绩/批语
class AddStudentStudyRecord(View):

    def get(self, request, class_study_record_id):
        model_formset_cls = modelformset_factory(model=StudentStudyRecord, form=StudentStudyRecordModelForm, extra=0)
        # extra用户扩展添加为0则不显示添加
        queryset = StudentStudyRecord.objects.filter(classstudyrecord=class_study_record_id)
        formset = model_formset_cls(queryset=queryset)
        return render(request, "study/StudentScore.html", {"formset": formset})

    def post(self, request, class_study_record_id):
        model_formset_cls = modelformset_factory(model=StudentStudyRecord, form=StudentStudyRecordModelForm, extra=0)
        queryset = StudentStudyRecord.objects.filter(classstudyrecord=class_study_record_id)
        print("request.POST", request.POST)
        formset = model_formset_cls(request.POST, queryset=queryset)
        if formset.is_valid():
            formset.save()
        print(formset.errors)

        return redirect(request.path)


# 根据日期统计数量
class StatisticsView(View):

    def get(self, request):
        date = request.GET.get("date", "today")  # 获取查询区间,无则为当天
        now = datetime.datetime.now().date()  # 当天的 年-月-日
        delta1 = datetime.timedelta(days=1)  # 前一天的 年-月-日
        delta2 = datetime.timedelta(weeks=1)  # 一周前的 年-月-日
        delta3 = datetime.timedelta(weeks=4)  # 四周前的 年-月-日

        # 相应时间对应的过滤条件
        condition = {
            "today": [{"deal_date": now}, {"customers__deal_date": now}],
            "yesterday": [{"deal_date": now - delta1}, {"customers__deal_date": now - delta1}],
            "week": [{"deal_date__gte": now - delta2, "deal_date__lte": now},
                     {"customers__deal_date__gte": now - delta2, "customers__deal_date__lte": now}
                     ],
            "recent_month": [{"deal_date__gte": now - delta3, "deal_date__lte": now},
                             {"customers__deal_date__gte": now - delta3, "customers__deal_date__lte": now}
                             ],
        }
        # 根据时间段过滤出的客户列表
        customer_list = Customer.objects.filter(**(condition.get(date)[0]))
        # 根据时间段,过滤出销售人及其在此时间段的销售数量
        ret = UserInfo.objects.all().filter(**(condition.get(date)[1])).annotate(c=Count("customers")).values_list(
            "username", "c")
        # ↓↓↓图标所需的数据结构↓↓↓
        list_x = []
        list_y = []
        list_circle = []
        for item in list(ret):
            dict_circle = {}
            list_x.append(item[0])
            list_y.append(item[1])
            dict_circle["value"] = item[1]
            dict_circle["name"] = item[0]
            list_circle.append(dict_circle)
        print(list_circle)
        # ↑↑↑图标所需的数据结构↑↑↑
        # 图表所对应的模板
        if request.path == "/customer_statistics/charts/":
            return render(request, "customer/charts.html", locals())
        # 统计表所对应的模板
        return render(request, "customer/statistics.html", locals())


def permission_distribute(request):
    """
       分配权限
       :param request:
       :return:
       """
    uid = request.GET.get('uid')  # 获取用户id
    user = UserInfo.objects.filter(pk=uid)  # 当前选择用户对象
    current_user = UserInfo.objects.filter(pk=uid).values("username").first()  # 前端显示当前选择的用户名
    rid = request.GET.get('rid')  # 获取角色id
    current_role = Role.objects.filter(pk=rid).values("title").first()  # 前端显示当前选择的角色名
    # 获取为当前用户所选择的的角色
    if request.method == "POST" and request.POST.get('postType') == 'roles':
        lst = request.POST.getlist("roles")
        print("lst========", lst)
        # 更新角色信息
        user.first().roles.set(lst)

    # 获取为当前角色所选择的的权限
    if request.method == "POST" and request.POST.get('postType') == 'permission':
        lit = request.POST.getlist("permission_id")
        print("lit==========", lit)
        # 更新权限信息
        Role.objects.filter(pk=rid).first().permissions.set(lit)

    # 所有用户
    user_list = UserInfo.objects.all()
    # 所有角色
    user_has_roles = user.values('id', 'roles')
    role_list = Role.objects.all()

    if uid:  # 选择了用户
        # 用户的所有角色
        role_id_list = UserInfo.objects.get(pk=uid).roles.all().values_list("pk")
        role_id_list = [item[0] for item in role_id_list]
        if rid:
            per_id_list = Role.objects.filter(pk=rid).values_list("permissions__pk").distinct()
        else:
            # 无角色默认展示当前用户所有权限
            per_id_list = UserInfo.objects.get(pk=uid).roles.values_list("permissions__pk").distinct()
        per_id_list = [item[0] for item in per_id_list]
        print("==========per_id_list", per_id_list)

    if rid:  # 选择了角色
        # 角色的所有权限
        per_id_list = Role.objects.filter(pk=rid).values_list("permissions__pk").distinct()
        per_id_list = [item[0] for item in per_id_list]

    return render(request, 'permission/permission.html', locals())


# ajax请求的路由所对应的视图
def permission_tree(request):
    # 将所有权限信息返回给ajax
    permissions = Permission.objects.values("pk", "title", "url", "menu__title", "menu__pk", "pid_id")

    return JsonResponse(list(permissions), safe=False)
