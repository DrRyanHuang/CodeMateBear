import json
import Agently
from github_api import GithubUser, GithubRepo, GithubSearch
from utils import get_token
import random

TOP_K = 5
FILTER_KEYWORDS_CONTENTS = [
    "过滤无意义的关键词, 如'文档', '社区', '贡献', '课程', '安装'",
    "过滤开源协议相关关键词, 如'MIT', 'Apache",
    "过滤冗余关键词",
    "过滤与技术完全不相关的关键词",
    "过滤无实际意义的文件名称/路径",
    "过滤公司名字，如'谷歌', 'Tencent'"
]

REFINE_KEYWORDS_CONTENTS = [
    "优化技术关键词",
    "保留关键名词",
    "翻译为地道的英文"
]


user = GithubUser("DrRyanHuang")
all_repos_info = []
for repo_brief in user.repos[:TOP_K]:
    repo = GithubRepo(repo_brief["href"])
    repo.run()
    repo.repo_info['name'] = repo_brief["name"]
    all_repos_info.append(repo.repo_info)

agent_factory = (
    Agently.AgentFactory()
    .set_settings("current_model", "ERNIE")
    .set_settings("model.ERNIE.auth", {"aistudio": get_token()})
    # <---- 修改模型
    .set_settings("model.ERNIE.options", {"model": "ernie-4.0"})
)

# 创建一个工作流
workflow = Agently.Workflow()

keyword_writer = (
    agent_factory.create_agent()
    # .set_settings("model.ERNIE.options", { "model": "ernie-4.0" })
    .set_role(
        """你是一个在Github上阅码无数的资深研发工程师, 你需要根据给定的内容, 提炼出技术类关键词, 供后续的项目检索""")
)


@workflow.chunk()
def set_keyword_storage(inputs, storage):
    keywords_list = []
    for i, repo_info in enumerate(all_repos_info):
        print(f"正在处理第{i+1}个仓库...")
        keywords = (
            keyword_writer
            .input({
                "Github仓库名称": repo_info["name"],
                "Github仓库简短描述": repo_info["about"],
                "Github Readme内容": repo_info["readme"],
            })
            .instruct("仓库{Github仓库名称}的简短描述是{Github仓库简短描述}, 其Readme文件的内容为{Github Readme内容}，请从中提取简短有效的技术关键词, 并按照置信度排序")
            .output([("str", )])
            .start()
        )
        keywords_list += list(keywords)
        print(keywords)

    storage.set("keywords_list", keywords_list)


@workflow.chunk()
def filter_keywords(inputs, storage):
    keywords_list = storage.get("keywords_list", ["AGI", "SoRA"])
    keywords_filtered = (
        keyword_writer
        .input({
            "Github搜索关键词": "\t".join(keywords_list),
            "需要过滤的内容": "\t".join(FILTER_KEYWORDS_CONTENTS),
            "需要优化的内容": "\t".join(REFINE_KEYWORDS_CONTENTS),
        })
        .instruct("根据之前Github搜索关键词{Github搜索关键词}, 按照{需要过滤的内容}要求过滤不需要的关键词, 然后再按照{需要优化的内容}优化这些关键词, 使Github用户能够快速找到自己感兴趣的技术, 并按照用户可能的感兴趣程度排序")
        .output([("str", )])
        .start()
    )
    print("过滤后的关键词:")
    print(keywords_filtered)

    storage.set("keywords_filtered", keywords_filtered)
    return keywords_filtered


@workflow.chunk()
def github_search_from_keywords(inputs, storage):
    keywords_filtered = storage.get("keywords_filtered", ["AGI", "SoRA"])
    keywords_filtered = random.shuffle(keywords_filtered)

    search_out = []
    for keyword in keywords_filtered[:2]:
        search_out += GithubSearch(keyword).get_n_repos(1)
    
    print("推荐结果:")
    print(search_out)

(
    workflow
    .connect_to("set_keyword_storage")
    .connect_to("filter_keywords")
    .connect_to("github_search_from_keywords")
    # .if_condition(lambda value, storage: value == "y")
    #     .connect_to("return_background")
    #     .connect_to("end")
    # .else_condition()
    #     .connect_to("input_revision_suggestion")
    #     .connect_to("generate_background")
)

# 运行一下试试
workflow.start()