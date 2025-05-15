import os


class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = 'c6d0287e0a3b233794fccd236a78eea82eb30428ff3cf98ef84f6ffe20b6faab'
    SECRET_KEY = '9d6ba527e277f1f16b60a646c7794f43e5d0a8b8f05338ec67abd575f9ea11cd'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(Config.BASE_DIR, 'project.db')

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ...