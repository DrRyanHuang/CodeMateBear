<!-- English | [简体中文](./README_cn.md) -->

<div align="center">
<!-- 标题 -->

<h1 align="center">
  - CodeMate Bear - 
</h1>

<!-- star数, fork数, pulls数, issues数, contributors数, 开源协议 -->

<a href="https://github.com/DrRyanHuang/CodeMateBear/stargazers"><img src="https://img.shields.io/github/stars/DrRyanHuang/CodeMateBear" alt="Stars Badge"/></a>
<a href="https://github.com/DrRyanHuang/CodeMateBear/network/members"><img src="https://img.shields.io/github/forks/DrRyanHuang/CodeMateBear" alt="Forks Badge"/></a>
<br/>
<a href="https://github.com/DrRyanHuang/CodeMateBear/pulls"><img src="https://img.shields.io/github/issues-pr/DrRyanHuang/CodeMateBear" alt="Pull Requests Badge"/></a>
<a href="https://github.com/DrRyanHuang/CodeMateBear/issues"><img src="https://img.shields.io/github/issues/DrRyanHuang/CodeMateBear" alt="Issues Badge"/></a>
<a href="https://github.com/DrRyanHuang/CodeMateBear/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/DrRyanHuang/CodeMateBear?color=2b9348"></a>
<a href="https://github.com/DrRyanHuang/CodeMateBear/blob/master/LICENSE"><img src="https://img.shields.io/github/license/DrRyanHuang/CodeMateBear?color=2b9348" alt="License Badge"/></a>

<!-- logo -->

<img alt="LOGO" src="logo/bear.png" width="30%"> </img>
<br/>
<i>Loved the project? Please consider forking the project to help it improve!</i>🌟

</div>



This project leverages the ERNIE Bot to implement a recommendation system. It crawls Github user and repository information, feeds it into the large model, and allows the model to extract keywords. Based on these keywords, it searches for projects on Github and recommends them to users in the order of the most stars, most forks, and best matches.


### Demo Showcase 🎥🌟

<div align="center">
  <img alt="LOGO" src="imgs/1.png" width="18%"> </img>
  <img alt="LOGO" src="imgs/3.png" width="18%"> </img>
  <img alt="LOGO" src="imgs/2.png" width="18%"> </img>
  <img alt="LOGO" src="imgs/4.png" width="18%"> </img>
</div>



### How to run 🚀

```
python3 -mpip install -r requirements.txt
python3 main.py
```

- `utils.py` contains a collection of small utility functions.
- `github_api.py` contains classes and functions for scraping Github information.
- `test_agently.py` 和 `test_github_api.py` are test scripts, with the former testing Agently and the latter verifying the accuracy of Github information scraping