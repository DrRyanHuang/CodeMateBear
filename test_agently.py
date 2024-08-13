import json
import Agently

"""
ERNIE SDK提供便捷易用的接口, 可以调用文心大模型的能力, 包含文本创作、通用对话、语义向量、AI作图等。
项目地址：https://github.com/PaddlePaddle/ERNIE-SDK/tree/develop/erniebot
在实际开发中, Agently框架已经对ERNIE SDK进行了封装, 开发者只需要从下面的模型列表中选择适用的模型即可

| 模型名称 | 说明 | 功能| 支持该模型的后端| 输入token数量上限| 输出token数量上限 |
|--|--|--|--|--|--|
| ernie-3.5 | 文心大模型3.5版本。具备优秀的知识增强和内容生成能力, 在文本创作、问答、推理和代码生成等方面表现出色。 | 对话补全, 函数调用 | qianfan, aistudio| message中的content总长度、functions和system字段总内容不能超过20000个字符, 且不能超过5120 tokens | 2048 |
| ernie-lite（免费）| ERNIE Lite是百度自研的轻量级大语言模型, 兼顾优异的模型效果与推理性能, 适合低算力AI加速卡推理使用。 | 对话补全 | qianfan, aistudio| message中的content总长度和system字段总内容不能超过11200个字符, 且不能超过7168 tokens | 1024 |
| ernie-4.0 | 文心大模型4.0版本, 具备目前系列模型中最优的理解和生成能力。 | 对话补全, 函数调用 | qianfan, aistudio| message中的content总长度和system字段总内容不能超过20000个字符, 且不能超过5120 tokens | 2048 |
| ernie-3.5-8k | 文心大模型。在ernie-3.5模型的基础上增强了对长对话上下文的支持, 输入token数量上限为7000。 | 对话补全, 函数调用 | qianfan, aistudio| message中的content总长度、functions和system字段总内容不能超过20000个字符, 且不能超过5120 tokens | 2048 |
| ernie-speed（免费） | ERNIE Speed是百度自研高性能大语言模型, 通用能力优异, 适合作为基座模型进行精调, 更好地处理特定场景问题, 同时具备极佳的推理性能。 | 对话补全 | qianfan, aistudio| message中的content总长度和system字段总内容不能超过24000个字符, 且不能超过6144 tokens | 2048 |
| ernie-speed-128k| ERNIE Speed是百度自研高性能大语言模型, 通用能力优异, 适合作为基座模型进行精调, 更好地处理特定场景问题, 同时具备极佳的推理性能。 | 对话补全 | qianfan, aistudio| message中的content总长度和system字段总内容不能超过516096个字符, 且不能超过126976 tokens | 4096 |
| ernie-tiny-8k| ERNIE Tiny是百度自研的超高性能大语言模型, 部署与精调成本在文心系列模型中最低。 | 对话补全 | qianfan, aistudio| message中的content总长度和system字段总内容不能超过24000个字符, 且不能超过6144 tokens | 2048 |
| ernie-char-8k| 百度自研的垂直场景大语言模型, 适合游戏NPC、客服对话、对话角色扮演等应用场景, 人设风格更为鲜明、一致, 指令遵循能力更强, 推理性能更优。 | 对话补全 | qianfan, aistudio| message中的content总长度和system字段总内容不能超过24000个字符, 且不能超过6144 tokens | 2048 |
| ernie-text-embedding | 文心百中语义模型。支持计算最多384个token的文本的向量表示。 | 语义向量 | qianfan, aistudio| 384*16| |
| ernie-vilg-v2| 文心一格模型。 | 文生图 | yinian | 200 | |
"""

# 测试下 Agently 安装成功否
def test_Agently():

    # 读取 token
    with open("token.txt") as f:
        token = f.read().strip()
    # print(token)

    # 全局配置
    agent_factory = (
        Agently.AgentFactory()
        .set_settings("current_model", "ERNIE")
        .set_settings("model.ERNIE.auth", {"aistudio": token})
        # <---- 修改模型
        .set_settings("model.ERNIE.options", {"model": "ernie-lite"})
    )
    agent = agent_factory.create_agent()
    result = agent.input("你好, 你是谁?").start()
    print(result)

    # 构建 Agent
    agent = agent_factory.create_agent()
    agent.set_agent_prompt("role", [
        {"姓名": "大司马"},
        {"年龄": "35"},
        {"性别": "男"},
        {"身份": "你是LOL游戏主播, 你玩游戏非常下饭"},
    ])
    agent.set_request_prompt("input", "你是谁?")
    result = agent.start()
    print(result)

    # 真的记住了吗？
    agent.set_request_prompt("output", "你的身份")
    result = agent.start()
    print(result)


if __name__ == '__main__':
    test_Agently()