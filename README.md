# Crawler-For-Literature
Crawler-For-Literature 是一个用于自动化获取学术文献和相关信息的爬虫工具，旨在帮助研究人员高效地收集和管理学术资源。本项目着重关注化学、材料领域的中文文献。

该项目正在持续更新支持对多个学术文献网站的信息爬取，目前包含cnki、化学进展、中文维基百科。

项目目前处于开发阶段，功能正在进一步完善中。

## 安装与使用

### 安装依赖库
```bash
pip install -r requirements.txt
```

### 运行爬虫
每个部分是分开运行的，以下是运行cnki部分的示例
```bash
cd crawler_for_cnki
python main.py
```