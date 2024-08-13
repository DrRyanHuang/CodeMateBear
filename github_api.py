"""
没想到 Github 的个人主页是静态网站, 本项目主要用 xpath 来解析, 这一版目前先将 xpath 硬编码在代码中
不处理私有仓库
# https://pip.baidu.com/pypi/simple
"""

import requests as r
from bs4 import BeautifulSoup
from lxml import etree
from datetime import datetime


class GithubUser:

    BASE_URL = "https://github.com"
    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0",
    }
    GITHUB_USER_URL = "https://api.github.com/users/%s"

    def __init__(self, username, headers=None):

        self.username = username
        self.base_url = f"{self.BASE_URL}/{username}"
        self.page_repo_url = f"{self.BASE_URL}/{username}?page=%s&tab=repositories"

        if headers is None:
            self.headers = self.DEFAULT_HEADERS
        else:
            self.headers = dict(self.DEFAULT_HEADERS, **headers)
        self.resp = r.get(self.base_url, self.headers)
        self.soup, self.xml_tree = self._preprocessing(self.resp)

        self.repositories_num = self.get_repositories_num()
        self.stars_num = self.get_stars_num()
        self.followers_num = self.get_followers_num()
        self.following_num = self.get_following_num()
        self.bio = self.get_Bio()

        self.repos = self._get_all_public_repos()
        # print("仓库数量: {} | star数: {} | follower数: {} | following数: {}".format(
        #     self.repositories_num,
        #     self.stars_num,
        #     self.followers_num,
        #     self.following_num)
        #     )

    def _preprocessing(self, response):
        assert response.status_code == 200, "Invalid response"
        # assert response.apparent_encoding == "utf-8", "Invalid encoding"
        response.encoding = "utf-8"

        # 解析HTML内容
        tree = etree.HTML(response.text)
        return BeautifulSoup(response.text, "html.parser"), tree

    def _get_num_by_xpath(self, xpath_expression):
        try:
            element = self.xml_tree.xpath(xpath_expression)[0]
            num = element.text
            if num.endswith("k"):
                # 3.8k
                return num
            return int(num)
        except:
            return -1

    def _get_str_by_xpath(self, xpath_expression):
        try:
            element = self.xml_tree.xpath(xpath_expression)[0]
            return element.text
        except IndexError:
            return ""
        except:
            return ""

    def get_repositories_num(self):
        try:
            # 通常来说第一个是repo数量
            span_text = self.soup.find("span", class_="Counter").text
            return int(span_text)
        except:
            return -1

    def get_stars_num(self):
        # 使用XPath表达式定位元素
        xpath_expression = (
            "/html/body/div[1]/div[4]/main/div[1]/div/div/div[2]/div/nav/a[5]/span"
        )
        return self._get_num_by_xpath(xpath_expression)

    def get_followers_num(self):
        # 使用XPath表达式定位元素
        # xpath_expression = "/html/body/div[1]/div[4]/main/div[2]/div/div[1]/div/div[2]/div[2]/div[2]/div[2]/div/a[1]/span"
        # return self._get_num_by_xpath(xpath_expression)
        # <span class="text-bold color-fg-default">12.6k</span>
        followers_following = self.soup.find_all(
            "span", class_="text-bold color-fg-default"
        )
        if not followers_following:  # 要有都有, 俩个都有
            return -1
        followers = followers_following[0].text
        if followers.endswith("k"):
            return followers
        return int(followers)

    def get_following_num(self):
        # 使用XPath表达式定位元素
        # xpath_expression = "/html/body/div[1]/div[4]/main/div[2]/div/div[1]/div/div[2]/div[3]/div[2]/div[2]/div/a[2]/span"
        # return self._get_num_by_xpath(xpath_expression)
        # followers_following = self.soup.find_all('span', class_='text-bold color-fg-default')
        # return int(followers_following[1].text)
        followers_following = self.soup.find_all(
            "span", class_="text-bold color-fg-default"
        )
        if not followers_following:  # 要有都有, 俩个都有
            return -1
        following = followers_following[1].text
        if following.endswith("k"):
            return following
        return int(following)

    def get_Bio(self):
        xpath_expression = "/html/body/div[1]/div[4]/main/div[2]/div/div[1]/div/div[2]/div[3]/div[2]/div[1]/div"
        return self._get_str_by_xpath(xpath_expression)

    def _get_all_public_repos(self):
        page_id = 1
        repos_num = 0
        repos_list = []
        while True:
            repos_list += self._get_1page_public_repos(page_id)
            repos_num = len(repos_list)
            page_id += 1
            if repos_num >= self.repositories_num:
                break

        repos_list.sort(key=lambda x: x["last_update"], reverse=True)
        return repos_list

    def _get_1page_public_repos(self, page):

        current_page_url = self.page_repo_url % page
        page_resp = r.get(current_page_url, self.headers)

        if 200 != page_resp.status_code:
            return []

        page_resp.encoding = "utf-8"
        page_soup = BeautifulSoup(page_resp.text, "html.parser")

        repo_ul = page_soup.find_all(
            "ul",
            attrs={
                "data-filterable-for": "your-repos-filter",
                "data-filterable-type": "substring",
            },
        )
        repo_info_1page = []
        if len(repo_ul):
            repo_ul = repo_ul[0]
            repos_li = repo_ul.find_all("li")

            for li in repos_li:
                repo_info = self._get_repo_info_from_li(li)
                repo_info_1page.append(repo_info)

        return repo_info_1page

    def _get_repo_info_from_li(self, li):

        name = li.a.text.strip()
        href = li.a["href"]
        forked = li.find("span", class_="f6 color-fg-muted mb-1")
        description = li.find_all("p")[0].text.strip() if li.p else ""
        language = ""
        _license = ""
        last_update = (
            li.find("relative-time").text.strip() if li.find("relative-time") else ""
        )
        last_update = datetime.strptime(last_update, "%b %d, %Y")

        repo_info = {
            "name": name,
            "href": href,
            "forked": forked,
            "description": description,
            "language": language,
            "license": _license,
            "last_update": last_update,
        }
        return repo_info


if __name__ == "__main__":
    USERNAME = "SigureMo"
    GithubUser(USERNAME, {})


class GithubRepo:
    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0",
    }

    def __init__(self, href, headers=None):
        self.url = f"{GithubUser.BASE_URL}/{href}"

        if headers is None:
            self.headers = self.DEFAULT_HEADERS
        else:
            self.headers = dict(self.DEFAULT_HEADERS, **headers)

        self.repo_info = {}
        # self.soup = self._get_response_soup(self.url)
        # self._get_repo_all_info(self.soup)
        # print(self.repo_info)

    def _get_response_soup(self, url):
        resp = r.get(url, headers=self.headers)
        if resp.status_code != 200:
            # raise Exception(f"Request failed with status code {resp.status_code}")
            return []
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")
        return soup

    def _get_repo_s_w_f(self, soup):
        # stars, watching, forks
        _repo_info = soup.find(class_="hide-sm hide-md")
        _repo_info = _repo_info.find_all("div", class_="mt-2")

        return_info = {}

        for div in _repo_info:
            key = div.text.strip().lower()
            if "stars" in key:
                stars = key.split("\n      ")[0]
                return_info["stars"] = int(stars)
            elif "watching" in key:
                watching = key.split("\n      ")[0]
                return_info["watching"] = int(watching)
            elif "forks" in key:
                forks = key.split("\n      ")[0]
                return_info["forks"] = int(forks)

        return return_info

    def _get_repo_about(self, soup):
        about = soup.find_all(class_="f4 my-3")
        if len(about):
            about = about[0]
            return about.text.strip()
        return ""

    def _get_repo_readme(self, soup):
        readme = soup.find_all(
            "article",
            class_="markdown-body entry-content container-lg",
            itemprop="text",
        )

        if len(readme):
            readme = readme[0]
            return readme.text.strip()
        return ""

    def _get_repo_all_info(self, soup):

        self.repo_info = self._get_repo_s_w_f(soup)

        about = self._get_repo_about(soup)
        self.repo_info["about"] = about

        readme = self._get_repo_readme(soup)
        self.repo_info["readme"] = readme

    def run(self):
        self.soup = self._get_response_soup(self.url)
        self._get_repo_all_info(self.soup)


if __name__ == "__main__":
    REPO_HREF = "DrRyanHuang/bangumi-anime"
    print(GithubRepo(REPO_HREF))


class GithubSearch:
    BASE_URL = "https://github.com/search?q={}&type={}&s={}&p=%s"
    DEFAULT_TYPE = "repositories"
    SORT_BY_BEST_MATCH = ""
    SORT_BY_MOST_STARRED = "stars"
    SORT_BY_MOST_FORKS = "forks"

    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0",
    }

    def __init__(self, query, _type=None, headers={}):
        self.query = query
        if _type is None:
            self._type = self.DEFAULT_TYPE
        else:
            self._type = _type.lower()

        self.url = self.BASE_URL.format(query, self._type, self.SORT_BY_BEST_MATCH)

        if headers is None:
            self.headers = self.DEFAULT_HEADERS
        else:
            self.headers = dict(self.DEFAULT_HEADERS, **headers)

        self.search_res_1page = self._get_response_soup(self.url, page=1)

    def _parse_response_json(self, resp_json):
        if "payload" in resp_json:
            payload = resp_json["payload"]
            if "csrf_tokens" in payload:
                csrf_tokens = payload["csrf_tokens"]
                _repo_href = list(csrf_tokens.keys())[:-1:2]
                _repo_href = [repo[:-5] for repo in _repo_href]
                return _repo_href
            else:
                return []
        else:
            return []

    def _get_response_soup(self, url, page=1):
        resp = r.get(url % page, headers=self.headers)
        if resp.status_code != 200:
            # raise Exception(f"Request failed with status code {resp.status_code}")
            return []
        resp.encoding = "utf-8"
        # WTF 竟然不需要解析, 直接返回一个 json 对象?
        # soup = BeautifulSoup(resp.text, "html.parser")
        repos_href = self._parse_response_json(resp.json())
        return repos_href

    def get_n_repos(self, n):
        return self.search_res_1page[:n]


if __name__ == "__main__":
    # REPO_HREF = "SigureMo/nyakku.moe"
    # print(GithubRepo(REPO_HREF).href)
    print(GithubSearch("paddlepaddle").get_n_repos(4))
