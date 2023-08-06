from asyncio.tasks import current_task
from urllib import parse
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from gesang_sqlalchemy.model import DefaultMeta


def get_indent():
    """
    获取任务ID
    :return:
    """
    return id(current_task())


def make_model(metadata=None):
    """
    创建model
    :param metadata:
    :return:
    """
    model = declarative_base(metadata=metadata, metaclass=DefaultMeta)
    if metadata is not None and model.metadata is not metadata:
        model.metadata = metadata
    return model


def generate_engine(host, port, username, password, charset, db_name, engine_name, options):
    """
    生成引擎

    :param host: 主机地址
    :param port: 端口号
    :param username: 用户名
    :param password: 密码
    :param charset: 字符集
    :param db_name: 数据库名称
    :param engine_name: 引擎名称
    :param options: 选项
    :return:
    """
    db_uri = f"{engine_name}://{username}:{parse.quote(password)}@{host}:{port}/{db_name}?charset={charset}"
    return create_engine(db_uri, **options)
