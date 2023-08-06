from sqlalchemy.ext.declarative import DeclarativeMeta


class BindMetaMixin(type):
    def __init__(cls, name, bases, d):
        bind_key = d.pop("__bind_key__", None) or getattr(cls, "__bind_key__", None) or "default"

        super().__init__(name, bases, d)

        if bind_key is not None and getattr(cls, "__table__", None) is not None:
            cls.__table__.info["bind_key"] = bind_key


class DefaultMeta(BindMetaMixin, DeclarativeMeta):
    pass
