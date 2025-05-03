from django.test import TestCase

# Create your tests here.


import random
import string


# characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
# length = 10
# random_string = ''.join(random.choice(characters) for _ in range(length))
# print(random_string)  # 应该打印出一个长度为10的随机字符串


characters = string.ascii_letters + string.digits
print(characters)
lists = (random.choice(characters) for _ in range(4))
print(lists)
captcha_text = ''.join(lists)
print(captcha_text)