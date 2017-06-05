import os
import tempfile


class Configuration:

    # Flask
    SECRET_KEY = os.environ.get("NC_USER_SECRET_KEY") or \
        "yabbadabbadoo!"
    JSON_AS_ASCII = False

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    @staticmethod
    def init_app(
            app):
        pass


class DevelopmentConfiguration(Configuration):

    DEBUG = True
    DEBUG_TOOLBAR_ENABLED = True
    FLASK_DEBUG_DISABLE_STRICT = True

    SQLALCHEMY_DATABASE_URI = \
        os.environ.get("NC_USER_DEV_DATABASE_URI") or \
        "sqlite:///" + os.path.join(tempfile.gettempdir(),
            "user-dev.sqlite")


    @staticmethod
    def init_app(
            app):
        Configuration.init_app(app)

        from flask_debug import Debug
        Debug(app)


class TestConfiguration(Configuration):

    SQLALCHEMY_DATABASE_URI = \
        os.environ.get("NC_USER_TEST_DATABASE_URI") or \
        "sqlite:///" + os.path.join(tempfile.gettempdir(),
            "user-test.sqlite")


class ProductionConfiguration(Configuration):

    SQLALCHEMY_DATABASE_URI = \
        os.environ.get("NC_USER_DATABASE_URI") or \
        "sqlite:///" + os.path.join(tempfile.gettempdir(),
            "user.sqlite")


configuration = {
    "development": DevelopmentConfiguration,
    "test": TestConfiguration,
    "acceptance": ProductionConfiguration,
    "production": ProductionConfiguration
}
