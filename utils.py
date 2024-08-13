import os


def get_token():
    if not os.path.exists("token.txt"):
        raise FileNotFoundError("请先在本目录下创建token.txt文件, 并将token写入其中")
    # 读取token
    with open("token.txt") as f:
        token = f.read().strip()
    # print(token)
    print("token读取成功")
    return token


if __name__ == "__main__":
    get_token()
