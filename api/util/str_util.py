import random
import string

def generate_random_code():
    # 定义可用字符集：大写字母和数字
    characters = string.ascii_uppercase + string.digits
    # 随机选择四个字符
    random_code = ''.join(random.choice(characters) for _ in range(4))
    return random_code

if __name__ == '__main__':
    for _ in range(10):
        print(generate_random_code())
