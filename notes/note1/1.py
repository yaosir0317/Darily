"""


 　　　　　　　 ┏┓　 ┏┓+ +
 　　　　　　　┏┛┻━━━┛┻┓ + +
 　　　　　　　┃　　　　　　┃ 　
 　　　　　　　┃　　　━　　 ┃ ++ + + +
 　　　　　　 ████━████  ┃+
 　　　　　　　┃　　　　　　　┃ +
 　　　　　　　┃　　　┻　　　┃
 　　　　　　　┃　　　　　　┃ + +
 　　　　　　　┗━┓　　　┏━┛
 　　　　　　　　 ┃　　　┃　　　　　　　　　　　
 　　　　　　　　 ┃　　　┃ + + + +
 　　　　　　　　 ┃　　　┃　　　　Code is far away from bug with the animal protecting　　　　　　　
 　　　　　　　　 ┃　　　┃ + 　　　　神兽保佑,代码无bug　　
 　　　　　　　　 ┃　　　┃
 　　　　　　　　 ┃　　　┃　　+　　　　　　　　　
 　　　　　　　　 ┃　 　 ┗━━━┓ + +
 　　　　　　　　 ┃ 　　　　   ┣┓
 　　　　　　　　 ┃ 　　　　　 ┏┛
 　　　　　　　　 ┗┓┓┏━┳┓┏┛ + + + +
 　　　　　　　　  ┃┫┫ ┃┫┫
 　　　　　　　　  ┗┻┛ ┗┻┛+ + + +
           
"""
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 import random
li = [i for i in range(0, 1000, 13)]


def move(a, b):  # 将盘子从a移动到b
    print("from %s -> to %s" % (a, b))


def hanoi(n, a, b, c):  # 将n个盘子从a搬到c
    if n == 1:  # 只有一个盘子的情况
        move(a, c)
    else:  # 有一个以上盘子的情况
        hanoi(n-1, a, c, b)  # 将上方的n-1个盘子从a搬到b
        move(a, c)  # 将第n个盘子从a轻松愉快地移动到c
        hanoi(n-1, b, a, c)  # 擦屁股，将b上的n-1个盘子搬到c上


# 台阶, n个台阶共有count(n)种方式
def count(n):
    if n == 1:
        return 1
    elif n == 2:
        return 2
    else:
        return count(n-1) + count(n-2)


# 二分有序
def bin_search(data_set, num):
    high = len(data_set) - 1
    low = 0
    while low <= high:
        mid = (high+low)//2
        if data_set[mid] < num:
            low = mid + 1
        elif data_set[mid] > num:
            high = mid - 1
        else:
            return "索引为: %d" % mid
    else:
        return -1


# 递归二分
def bin_search_rec(data_set, low, high, num):
    if low <= high:
        mid = (high + low)//2
        if data_set[mid] == num:
            return mid
        elif data_set[mid] < num:
            return bin_search_rec(data_set, mid+1, high, num)
        else:
            return bin_search_rec(data_set, low, mid-1, num)
    else:
        return -1


'''
冒泡排序
选择排序
插入排序

快速排序
堆排序
归并排序

基数排序
希尔排序
桶排序
'''


# 冒泡
def bubble_sort(_li):
    # 从前到后依次取索引
    for i in range(len(_li) - 1):
        # 判断本次是否有数字交换(没有则说明已排序完成)
        change = False
        # 循环从0到 总长度-i 取索引,每冒泡排i次,前面无序区长度会少i
        for j in range(len(_li) - i - 1):
            # 前 > 后则交换
            if _li[j] > _li[j+1]:
                _li[j], _li[j+1] = _li[j+1], _li[j]
                change = True
        if not change:
            break


# 最小数
def min_num(data_list):
    _min = 0
    for i in range(1, len(data_list)):
        if data_list[_min] > data_list[i]:
            _min = i
    return _min


# 选择
def select_sort(data_list):
    # 循环0-总长-1,取索引,因每次取余下的最下值,因此最后剩余最大值,所以不用再取最后一个索引
    for i in range(len(data_list)-1):
        # 将循环取到的索引暂定为最下值
        min_index = i
        # 便利剩余的元素,取最小值的索引
        for j in range(i+1, len(data_list)):
            if data_list[min_index] > data_list[j]:
                # 更新最小值的索引
                min_index = j
        # 最小值不是默认的索引位的值,则将最小数换到当前的最前索引位
        if min_index != i:
            data_list[i], data_list[min_index] = data_list[min_index], data_list[i]


# 插入
def insert_sort(data_list):
    # 从1-总长,依次取其索引
    for insert_num_index in range(1, len(data_list)):
        # 选出的插入值
        insert_num = data_list[insert_num_index]
        # 与选出值的进行比较的索引位
        b_index = insert_num_index - 1
        # 比较索引位为0或大于0,且当选出值<比较索引位的值
        while b_index >= 0 and insert_num < data_list[b_index]:
            # 将比较索引位的值向后移一位
            data_list[b_index+1] = data_list[b_index]
            # 更新比较索引位
            b_index -= 1
        data_list[b_index+1] = insert_num


random.shuffle(li)
insert_sort(li)
print(li)
