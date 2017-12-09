
- [x] 尝试解析XML
    +  使用Python的lxml.etree
    + 转义字符解决: 使用dtd文件验证
    + 有些论文的作者未知
- [ ] 存入数据库
    + 使用navicat可以很方便的把xml文件导入sql类数据库,注意一些字段的约束
    + 把mysql中的数据存入neo4j
        + sqlalchemy 操作已存在的数据库不需要再次定义表结构,参考[此处](https://stackoverflow.com/questions/11900553/sqlalchemy-table-already-exists)
        + 设计neo4j中的模型

            Node
            ----
            + author(name)
            + article(title,key,ee,url)
            + journal(name)

            Relationship
            ----
            + author -[ modify {mdate,institution} ]-> article
            + article -[ refer ] -> article
            + author -[ work_in ] -> institution
            + article -[ published_in {pages,volume} ]-> journal

- [ ] 提取reference
    + 如何获取: 爬虫爬取
        + <del>使用Article.ee<del>
        + 使用 google scholar
             + 需要使用代理,requests.session参考[此处](https://doomzhou.github.io/coder/2015/03/09/Python-Requests-socks-proxy.html)
             + 无对外api,故使用 [scholarly](https://pypi.python.org/pypi/scholarly) 来避免手动解析
             + 可能遇到anti-robot问题(暂时未遇到)
    + 如何保存这种关系: 非关系型数据库(neo4j)

- [ ] 目标功能 :知识图谱的构建
    + 学习知识
        + 搜索"决策树":
        + 理论的创建者
        + 当前的热点人物
    + 推荐
        + 文章推荐
        + 作者推荐
        + 热点文章(引用次数,发表时间)
    + 知识树展示
        + 发展过程
        + 知识点热度展示