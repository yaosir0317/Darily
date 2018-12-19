from django.test import TestCase

# Create your tests here.
# with open("models.py", "rb") as e:
#     for i in iter(lambda: e.read(1024), b"0.0.0"):
#         print(i)


lst = [1, 1, 2, 2, 3, 3]
ret = set(i for i in lst)
print(list(ret))
