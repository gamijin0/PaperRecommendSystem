
- [x] 尝试解析XML
    +  使用Python的lxml.etree
    + 转义字符解决: 使用dtd文件验证
- [ ] 存入数据库
    + 使用navicat可以很方便的把xml文件导入sql类数据库,注意一些字段的约束
    + 把mysql中的数据存入neo4j
        + sqlalchemy 操作已存在的数据库不需要再次定义表结构,[参考](https://stackoverflow.com/questions/11900553/sqlalchemy-table-already-exists)
        + 设计neo4j中的关系
            + author -[ wrote {date,} ]-> article
            + article -[ refer ] -> article
- [ ] 提取reference
    + 如何获取: 爬虫爬取
    + 如何保存这种关系: 非关系型数据库(neo4j)
- [ ] 目标功能
    + 