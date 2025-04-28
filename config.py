import os

class Config:
    """Base configuration class."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SESSION_SECRET", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///library.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test_library.db"

class ProductionConfig(Config):
    """Production configuration."""
    # Production-specific settings
    pass

# Dictionary with different configuration environments
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
