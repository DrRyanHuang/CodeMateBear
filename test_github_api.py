# 这是单元测试类
import unittest
from github_api import GithubUser


class TestGithubUserDrRyanHuang(unittest.TestCase):

    def _init(self):
        # 用户状态私有, 只有仓库数量
        self.name = "DrRyanHuang"
        self.repositories_num = 96
        self.stars_num = -1
        self.followers_num = -1
        self.following_num = -1

    def setUp(self):
        self._init()
        self.user = GithubUser(self.name)

    def test_username(self):
        self.assertEqual(self.user.username, self.name)

    def test_repositories_num(self):
        self.assertEqual(self.user.repositories_num, self.repositories_num)

    def test_stars_num(self):
        self.assertEqual(self.user.stars_num, self.stars_num)

    def test_followers_num(self):
        self.assertEqual(self.user.followers_num, self.followers_num)

    def test_following_num(self):
        self.assertEqual(self.user.following_num, self.following_num)


class TestGithubUserRenJoker(TestGithubUserDrRyanHuang):

    def _init(self):

        self.name = "ren-joker"
        self.repositories_num = 0
        self.stars_num = 0
        self.followers_num = 60
        self.following_num = 122


class TestGithubUserLuotao1(TestGithubUserDrRyanHuang):

    def _init(self):
        self.name = "luotao1"
        self.repositories_num = 15
        self.stars_num = 14
        self.followers_num = 172
        self.following_num = 3


class TestGithubUserCharlesChrismann(TestGithubUserDrRyanHuang):

    def _init(self):

        self.name = "Charles-Chrismann"
        self.repositories_num = 35
        self.stars_num = 24
        self.followers_num = "3.9k"
        self.following_num = "97.5k"


class TestGithubUserKaimingHe(TestGithubUserDrRyanHuang):

    def _init(self):

        self.name = "KaimingHe"
        self.repositories_num = 2
        self.stars_num = 20
        self.followers_num = "12.6k"
        self.following_num = 0


class TestGithubUserSigureMo(TestGithubUserDrRyanHuang):

    def _init(self):

        self.name = "SigureMo"
        self.repositories_num = 29
        self.stars_num = 555
        self.followers_num = 376
        self.following_num = 55


if __name__ == "__main__":
    unittest.main()
