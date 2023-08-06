from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.session import Session as SessionBase
from gesang.plugin.base import BasePlugin
from gesang_sqlalchemy import exc
from gesang_sqlalchemy import utils


class Session(SessionBase):

    def __init__(self, db, autocommit=False, autoflush=True, **options):
        binds = options.pop("binds", db.get_binds())

        SessionBase.__init__(
            self,
            autocommit=autocommit,
            autoflush=autoflush,
            binds=binds,
            **options,
        )


class GesangSqlalchemy(BasePlugin):
    default_settings = {
        "BINDS": {},
        "OPTIONS": {},
        "SESSION_OPTIONS": {}
    }

    def __init__(self):
        self.__model = utils.make_model()
        self.__session = None
        self.sqlalchemy_binds = {}
        self.sqlalchemy_default_options = {}
        self.session_options = {}
        self.bind_engines = {}

    def setup(self, settings):
        """
        插件初始化方法

        :param settings: 配置信息
        :return:
        """
        if hasattr(settings, "DATABASE_SETTINGS"):
            db_settings = getattr(settings, "DATABASE_SETTINGS")
        else:
            raise exc.FlamingoSqlalchemyError("Cannot find database configure.")
        if isinstance(db_settings, dict):
            self.sqlalchemy_binds = db_settings.get("BINDS", {})
            self.sqlalchemy_default_options = db_settings.get("ENGINE_DEFAULT_OPTIONS", {})
            self.session_options = db_settings.get("SESSION_OPTIONS", {})
            self.__session = self.create_scoped_session()
            self.create_bind_engines()
        else:
            raise exc.FlamingoSqlalchemyError("Database configure not dict.")

    def create_scoped_session(self):
        """
        创建基于asyncio的任务安全session
        :return:
        """
        return scoped_session(
            sessionmaker(class_=Session, db=self, **self.session_options),
            scopefunc=utils.get_indent
        )

    @property
    def Model(self):
        """
        获取属性Model
        :return:
        """
        return self.__model

    @property
    def session(self):
        """
        获取属性session
        :return:
        """
        if self.__session is None:
            raise exc.FlamingoSqlalchemyError("Plugin not register.")
        return self.__session()

    def get_handler(self):
        """
        获取操作句柄，对象本身

        :return:
        """
        return self

    def get_bind_models(self, bind_key):
        """
        获取指定bind_key的模型
        :param bind_key: 绑定key的值
        :return:
        """
        table_cls_list = []
        for table in self.__model.metadata.tables.values():
            if table.info.get("bind_key") == bind_key:
                table_cls_list.append(table)
        return table_cls_list

    def create_bind_engines(self):
        """
        创建绑定的引擎
        :return:
        """
        for key, engine_config in self.sqlalchemy_binds.items():
            engine_options = engine_config.get("options", None) or self.sqlalchemy_default_options
            kw = {
                "host": engine_config.get("HOST", "localhost"),
                "port": engine_config.get("PORT", "3306"),
                "username": engine_config.get("USER"),
                "password": engine_config.get("PASSWD"),
                "charset": engine_config.get("CHARSET", "utf8"),
                "db_name": engine_config.get("NAME", "default"),
                "engine_name": engine_config.get("ENGINE", "mysql"),
                "options": engine_options
            }
            engine = utils.generate_engine(**kw)
            self.bind_engines.update({key: engine})

    def get_binds(self):
        """
        获取绑定键值对
        :param binds: 绑定key和引擎配置关系
        :return:
        """
        bind_sessions = {}
        try:
            for key, engine_config in self.sqlalchemy_binds.items():
                bind_models = self.get_bind_models(bind_key=key)
                bind_sessions.update({bind_model: self.bind_engines.get(key) for bind_model in bind_models})
        except Exception as e:
            raise exc.FlamingoSqlalchemyError(e)
        finally:
            return bind_sessions


sqlalchemy_db = GesangSqlalchemy()
