import time


def outer(fun):
    def inner(*args, **kwargs):
        start = time.time()
        ret = fun(*args, **kwargs)
        end = time.time()
        print(start, end, end - start)
        return ret
    return inner


@outer
def quicksort(list):
    if len(list) < 2:
        return list
    else:
        mid_num = list[0]
        large_num = [i for i in list[1:] if i > mid_num]
        sm_num = [i for i in list[1:] if i <= mid_num]
        result = quicksort(sm_num) + [mid_num] + quicksort(large_num)
        return result


# quicksort([1, 8, 4, 6, 7, 12, 9, 5, 478, 92, 5, 6, 5, 4, 1, 8, 4, 6, 7, 12, 9, 5, 478, 92, 5, 6, 5, 4])

# 0.0009999275207519531

# @outer
# class Solution(object):
#     def twoSum(self, nums, target):
#         """
#         :type nums: List[int]
#         :type target: int
#         :rtype: List[int]
#         """
#         n = 0
#         result = []
#         while n < len(nums):
#             a = nums[n]
#             for num in nums[n + 1:]:
#                 if (a + num) == target:
#                     ret = []
#                     for i, j in enumerate(nums):
#                         if j == a or j == num:
#                             ret.append(i)
#                     result.append(ret)
#             n += 1
#         return result or "没有符合的结果"


# class Solution(object):
#     def twoSum(self, nums, target):
#         """
#         :type nums: List[int]
#         :type target: int
#         :rtype: List[int]
#         """
#         hashmap = {}
#         for index, num in enumerate(nums):
#             to_find = target - num
#             if to_find in hashmap:
#                 return [index, hashmap[to_find]]
#             hashmap[num] = index
#         return None


# class Solution(object):
#     def reverse(self, x):
#         """
#         :type x: int
#         :rtype: int
#         """
#         result = 0
#         if x*(-1) > x:
#             result += int(str(x)[1:][::-1])*(-1)
#         else:
#             result += int(str(x)[::-1])
#
#         if result > (-2)**31 and result < (2**31 - 1):
#             return result
#         return 0
#
#
# obj = Solution()
# print(obj.reverse(1534236469))


# class Solution:
#     def isPalindrome(self, x):
#         """
#         :type x: int
#         :rtype: bool
#         """
#         if x < 0 or (x != 0 and x % 10 == 0):
#             return False
#
#         half = 0
#         while half < x:
#             half = half*10 + x % 10
#             x //= 10
#         return x == half or x == half//10
#
#
# obj = Solution()
# print(obj.isPalindrome(1211121))


# 1 1 2 3 4 7 11 18 29
# @outer
# def fib(n):
#     f1 = f2 = 1
#     for i in range(2, n):
#         f1, f2 = f2, (f2 + f1)
#     return f2
#
#
# def fib_n(n):
#     if n <= 2:
#         return 1
#     return fib_n(n-1) + fib_n(n-2)
#
#
# print(fib(37))
# print(fib_n(37))
@outer
def test1(n):
    lst = []
    for i in range(10000*n):
        lst = lst + [i]
    return lst


@outer
def test2(n):
    lst = []
    for i in range(10000*n):
        lst.append(i)
    return lst


@outer
def test3(n):
    return [i for i in range(10000*n)]


@outer
def test4(n):
    return list(range(10000*n))


# test1(10)
# test2(1000)
# test3(1000)
# test4(1000)
