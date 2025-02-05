import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 기본 설정
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'documents/company_docs')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 최대 파일 크기 16MB
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'xlsx', 'xls'}

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 