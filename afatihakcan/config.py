class Config:
    DEBUG = True
    USE_RELOADER = True
    HOST = '0.0.0.0'
    PORT = 5000
    
    SECRET_KEY = "super-secret-key"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_USERNAME = "postgres"
    DB_PASSWORD = "postgres"
    DB_NAME = "adventureworks"
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost/{DB_NAME}"
    )
