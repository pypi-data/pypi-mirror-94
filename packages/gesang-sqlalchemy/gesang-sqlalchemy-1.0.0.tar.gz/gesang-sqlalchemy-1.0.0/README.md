# flamingo-sqlalchemy

#### 介绍
基于flamingo-core的Sqlalchemy的插件

#### 软件架构
软件架构说明

#### 安装教程

```shell
$ pip install gesang-sqlalchemy
```

#### 使用说明

1.  配置在项目的PLUGINS中
    
    ```python
    PLUGINS = [
        "gesang_sqlalchemy:db"
    ]
    ```
    
2.  代码中ORM
    ```python
    from gesang_sqlalchemy import db
    from sqlalchemy import Column, BigInteger, String, Boolean, DateTime
    from datetime import datetime
    
    
    class User(db.Model):
        __tablename__ = "user"
        __bind_key__ = "default"
    
        id = Column(BigInteger, primary_key=True)
        username = Column(String(200), nullable=True, unique=True)
        password = Column(String(200), nullable=False)
        valid = Column(Boolean, nullable=True, default=1)
        create_time = Column(DateTime, default=datetime.now)
        update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    ```
3. 查询使用
   ```python
   from gesang_sqlalchemy import db
   from test.models import User
   
   db.session.query(User).filter(User.valid == 1).all()
   ```
其他SQL详情请见[SQLAlchemy](https://www.osgeo.cn/sqlalchemy/) ，
项目请见[Github地址](https://github.com/sqlalchemy/sqlalchemy)

#### 感谢

- Flask-Sqlalchemy 感谢此插件的共享提供灵感，项目地址[Github地址](https://github.com/pallets/flask-sqlalchemy) 

#### ChangeLog
- 2021-02-09 重命名为gesang-sqlalchemy
- 2021-02-08 初始版本
#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
