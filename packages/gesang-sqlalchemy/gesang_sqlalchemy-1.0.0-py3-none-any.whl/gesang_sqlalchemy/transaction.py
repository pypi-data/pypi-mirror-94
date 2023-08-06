from contextlib import ContextDecorator
from gesang_sqlalchemy import FlamingoSqlalchemy
from gesang_sqlalchemy import db


def atomic(db_handler, with_exceptions=(Exception,)):
    """
    安全上下文生成器

    :param db_handler: SQLAlchemy对象
    :param with_exceptions: 异常列表，默认只有全局异常
    :return:
    """
    if isinstance(db_handler, FlamingoSqlalchemy) is False:
        raise Exception("db object is not correct, must be instance of SQLAlchemy.")
    return Atomic(db_handler, with_exceptions)


class Atomic(ContextDecorator):

    def __init__(self, db_handler, with_exceptions=()):
        self.db_handler = db_handler
        self.with_exceptions = with_exceptions

    def __enter__(self):
        pass

    def __exit__(self, exc_typ, exc_val, tb):
        if exc_typ and isinstance(exc_val, self.with_exceptions):
            # 当产生异常时，回滚，可以针对指定的异常进行回滚，默认是全部异常
            self.db_handler.session.rollback()
            # 将异常向上返回去
            raise
        else:
            # 其他情况进行提交
            self.db_handler.session.commit()


def safe_transaction_required(with_exceptions=(Exception,)):
    """
    安全事务提交装饰器，使用此装饰器

    说明：

    1. 不允许方法内部使用commit进行提交
    2. 指定异常进行回滚事务，默认是Exception子集异常
    3. 如果没有异常产生自动进行commit提交，无需手动写commit操作
    4. 如果不需要多步提交（事务操作），不需要添加此装饰器

    :param with_exceptions: [tuple] 异常元组
    :return:
    """

    def outer(func):
        def inner(*args, **kwargs):
            with atomic(db_handler=db, with_exceptions=with_exceptions):
                return func(*args, **kwargs)
        return inner
    return outer
