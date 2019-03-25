class BaseConfig(object):
    '''
    Base config class
    '''
    DEBUG = True
    TESTING = False

class ProductionConfig(BaseConfig):
    """
    Production specific config
    """
    DEBUG = False

class DevelopmentConfig(BaseConfig):
    """
    Development environment specific configuration
    """
    DEBUG = True
    TESTING = True

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}