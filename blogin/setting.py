"""
# coding:utf-8
@Time    : 2020/9/21
@Author  : charles feng
@File    : setting
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv('.env')

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class Operators:
    def __init__(self):
        pass

    CONFIRM = 'confirm'
    RESET_PASSWORD = 'reset-password'


class BaseConfig:
    BLOG_THEMES = {'light': 'light', 'dark': 'dark'}
    # Paginate configure
    BLOGIN_BLOG_PER_PAGE = 8
    BLOGIN_COMMENT_PER_PAGE = 10
    BLOGIN_PHOTO_PER_PAGE = 12
    LOGIN_LOG_PER_PAGE = 20
    SECRET_KEY = os.getenv('SECRET_KEY')
    JSON_AS_ASCII = False
    BLOGIN_MAIL_SUBJECT_PRE = '[Blogin]'

    # CKEditor configure
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_ENABLE_CODESNIPPET = True
    CKEDITOR_HEIGHT = 500
    CKEDITOR_CODE_THEME = 'docco'
    CKEDITOR_FILE_UPLOADER = 'be_blog_bp.upload'

    BLOGIN_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    CLOUDFRONT_URL = 'https://d28cl0j4ueg9il.cloudfront.net'

    # SQL configure
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    DATABASE_USER = os.getenv('DATABASE_USER', 'root')
    DATABASE_PWD = os.getenv('DATABASE_PWD')

    # DEFAULT AVATAR CONFIGURE
    AVATARS_SAVE_PATH = BLOGIN_UPLOAD_PATH + '/avatars/'

    # Mail configure
    BLOGIN_EMAIL_PRE = '[Blogin.] '
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('Blogin Admin', MAIL_USERNAME)

    # WHOOSHEE configure
    WHOOSHEE_MIN_STRING_LEN = 1

    # Redis Configure
    EXPIRE_TIME = 60 * 10

    # Photo Configure
    PHOTO_NEED_RESIZE = 1024 * 1024

    # BAIDU Trans appid
    BAIDU_TRANS_APPID = os.getenv('BAIDU_TRANS_APPID')
    BAIDU_TRANS_KEY = os.getenv('BAIDU_TRANS_KEY')

    # APScheduler config
    SCHEDULER_API_ENABLED = True

    # Babel config
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC+10'
    BABEL_TRANSLATION_DIRECTORIES = basedir + '/translations'


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@127.0.0.1:3307/blog?charset=utf8mb4'.format(BaseConfig.DATABASE_USER,
                                                                                            BaseConfig.DATABASE_PWD)
    REDIS_URL = "redis://localhost"


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@localhost:3307/blog?charset=utf8mb4'.format(BaseConfig.DATABASE_USER,
                                                                                            BaseConfig.DATABASE_PWD)
    REDIS_URL = "redis://localhost"


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
