import copy
"""
自定义分页
"""


class Pagination(object):

    def __init__(self, current_page_num, all_count, request, per_page_num=10, max_page_num=11):
        """
        封装分页相关数据
        :param current_page_num: 当前页码
        :param all_count: 数据总数
        :param per_page_num: 每页显示的数据条数
        :param max_page_num: 最大显示的页数
        """

        # 捕捉异常页码,异常则显示第一页
        try:
            current_page_num = int(current_page_num)
        except Exception as e:
            current_page_num = 1

        if current_page_num < 1:
            current_page_num = 1
        if current_page_num > all_count/per_page_num:
            all_pager, tmp = divmod(all_count, per_page_num)
            if tmp:
                current_page_num = all_pager+1
            else:
                current_page_num = all_pager

        self.current_page_num = current_page_num
        self.all_count = all_count
        self.per_page_num = per_page_num
        self.max_page_num = max_page_num

        # 计算总页数
        all_pager, tmp = divmod(all_count, per_page_num)
        if tmp:
            all_pager += 1
        self.all_pager = all_pager

        # 计算最多显示页数的一半,为了页数过多时,只实现一定的数量的实现做准备
        self.max_page_num_half = int((max_page_num-1)/2)

        # 保存搜索条件 获取{"a":"1","b":"2"}
        self.params = copy.deepcopy(request.GET)

    # 计算当前页所显示数据的起始索引
    @property
    def start(self):
        return (self.current_page_num - 1)*self.per_page_num

    # 计算当前页所显示数据的结束索引
    @property
    def end(self):
        return self.current_page_num * self.per_page_num

    # 自定义分页的逻辑函数
    def page_html(self):
        # 总页码数 < 最大显示页码数,即全部显示
        if self.all_pager < self.max_page_num:
            page_start = 1
            page_end = self.all_pager + 1

        # 总页码数 > 最大显示页码数,即显示最大页码数
        else:
            # 当前页 <= 最多显示页数的一半,即显示前max_page_num条
            if self.current_page_num <= self.max_page_num_half:
                page_start = 1
                page_end = self.max_page_num + 1

            # 当前页 > 最多显示页数的一半
            else:
                # 显示最后的max_page_num条
                if (self.current_page_num + self.max_page_num_half) > self.all_pager:
                    page_start = self.all_pager - self.max_page_num_half + 1
                    page_end = self.all_pager + 1

                # 显示中间的max_page_num条
                else:
                    page_start = self.current_page_num - self.max_page_num_half
                    page_end = self.current_page_num + self.max_page_num_half + 1

        # 上一页 首页 页码 尾页 下一页
        page_html_list = []

        # 当前页为第一页时不可点击,当前页大于第一页时点击时当前页码-1
        if self.current_page_num <= 1:
            prev_page = '<li class="disabled paginate_button"><a href="#">上一页</a></li>'
        else:
            self.params['page'] = self.current_page_num - 1
            prev_page = '<li class="paginate_button"><a href="?%s">上一页</a></li>' % (self.params.urlencode(),)
        page_html_list.append(prev_page)

        # 首页
        first_page = '<li class="paginate_button"><a href="?page=%s">首页</a></li>' % (1,)
        page_html_list.append(first_page)

        # 页码
        for i in range(page_start, page_end):
            self.params['page'] = i
            if i == self.current_page_num:
                temp = '<li class="active paginate_button"><a href="%s">%s</a></li>' % (self.params.urlencode(), i)
            else:
                temp = '<li class="paginate_button"><a href="?%s">%s</a></li>' % (self.params.urlencode(), i)
            page_html_list.append(temp)

        # 尾页
        last_page = '<li class="paginate_button"><a href="?page=%s">尾页</a></li>' % (self.all_pager,)
        page_html_list.append(last_page)

        # 当前页为尾页时不可点击,当前页小于尾页时点击时当前页码+1
        if self.current_page_num >= self.all_pager:
            next_page = '<li class="disabled paginate_button"><a href="#">下一页</a></li>'
        else:
            self.params['page'] = self.current_page_num + 1
            next_page = '<li class="paginate_button"><a href="?%s">下一页</a></li>' % (self.params.urlencode(),)
        page_html_list.append(next_page)
        return ''.join(page_html_list)

