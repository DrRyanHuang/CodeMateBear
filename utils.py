import re
import os


def run_once(func):
    """一个装饰器，使函数只运行一次，之后返回第一次的结果"""
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.result = func(*args, **kwargs)
            wrapper.has_run = True
        return wrapper.result
    wrapper.has_run = False
    wrapper.result = None
    return wrapper


@run_once
def get_token():
    if not os.path.exists("token.txt"):
        raise FileNotFoundError("请先在本目录下创建token.txt文件, 并将token写入其中")
    # 读取token
    with open("token.txt") as f:
        token = f.read().strip()
    # print(token)
    print("token读取成功")
    return token


@run_once
def get_qianfan_token():
    if not os.path.exists("qianfan_token.txt"):
        raise FileNotFoundError("请先在本目录下创建 qianfan_token 文件, 并将token写入其中")
    # 读取token
    with open("qianfan_token.txt") as f:
        token = f.read().strip()
    # print(token)
    print("token读取成功")
    return token.split("\n")


def remove_emoji(text):
    # 定义emoji的Unicode范围
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # regional indicators
                               u"\U00002700-\U000027BF"  # dingbats
                               u"\U0000FE00-\U0000FE0F"  # variation selectors
                               u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                               u"\U0001FA70-\U0001FAFF"  # Symbols for Legacy Computing
                               "]+", flags=re.UNICODE)

    # 使用正则表达式替换emoji为空字符串
    return emoji_pattern.sub(r'', text)


def filter_n(text_list, n):
    return [text for text in text_list if len(text) <= n]


if __name__ == "__main__":
    get_token()

    # 示例使用
    text_with_emoji = "Hello, World! 😊 This is a test 😀!!!!"
    print(text_with_emoji)
    text_without_emoji = remove_emoji(text_with_emoji)
    print(text_without_emoji)  # 输出: Hello, World!  This is a test

    get_qianfan_token()
