"""
系統配置檔案
集中管理系統的各項配置參數
"""

import os
from pathlib import Path


class Config:
    """基礎配置"""

    # 專案根目錄
    BASE_DIR = Path(__file__).parent.parent

    # 密鑰
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_very_secret_key_change_in_production')

    # 資料目錄
    DATA_DIR = BASE_DIR / 'data'
    UPLOAD_FOLDER = DATA_DIR / 'uploads'
    PROCESSED_DATA_FOLDER = DATA_DIR / 'processed_data'

    # 模型目錄
    MODELS_DIR = BASE_DIR / 'models'
    SAVED_MODELS_FOLDER = MODELS_DIR / 'saved_models'
    METADATA_FOLDER = MODELS_DIR / 'metadata'

    # 日誌目錄
    LOGS_DIR = BASE_DIR / 'logs'

    # 模型配置
    MIN_PREDICTION_DAYS = 1
    MAX_PREDICTION_DAYS = 30
    DEFAULT_PREDICTION_DAYS = 5

    # 訓練配置
    DEFAULT_LOOK_BACK = 5  # 使用過去 N 天的資料作為輸入
    DEFAULT_TARGET_COLUMN = 'close'  # 預測目標欄位

    # 超參數預設值
    DEFAULT_HYPERPARAMETERS = {
        'learning_rate': 0.001,
        'lstm_units': 64,
        'dropout_rate': 0.3,
        'epochs': 30,
        'batch_size': 32
    }

    # API 配置
    FLASK_HOST = '0.0.0.0'
    FLASK_PORT = 5000
    FLASK_DEBUG = True

    # Dash 配置
    DASH_HOST = '0.0.0.0'
    DASH_PORT = 8050
    DASH_DEBUG = True

    # 效能目標
    PERFORMANCE_TARGETS = {
        'upload_to_prediction_time': 300,  # 5 分鐘（秒）
        'model_switch_time': 3,  # 3 秒
        'auto_tuning_time': 1800  # 30 分鐘（秒）
    }

    @classmethod
    def init_directories(cls):
        """初始化所有必要的目錄"""
        directories = [
            cls.UPLOAD_FOLDER,
            cls.PROCESSED_DATA_FOLDER,
            cls.SAVED_MODELS_FOLDER,
            cls.METADATA_FOLDER,
            cls.LOGS_DIR
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)


class DevelopmentConfig(Config):
    """開發環境配置"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """生產環境配置"""
    DEBUG = False
    TESTING = False
    FLASK_DEBUG = False
    DASH_DEBUG = False

    # 生產環境應從環境變數讀取密鑰
    SECRET_KEY = os.environ.get('SECRET_KEY')

    if not SECRET_KEY:
        raise ValueError("生產環境必須設定 SECRET_KEY 環境變數")


class TestingConfig(Config):
    """測試環境配置"""
    DEBUG = True
    TESTING = True

    # 使用測試專用的目錄
    BASE_DIR = Path(__file__).parent.parent / 'test_data'
    DATA_DIR = BASE_DIR / 'data'
    MODELS_DIR = BASE_DIR / 'models'


# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(config_name='default'):
    """
    取得指定的配置類別
    :param config_name: 配置名稱 ('development', 'production', 'testing', 'default')
    :return: 配置類別
    """
    return config.get(config_name, DevelopmentConfig)
