"""
日誌記錄模組
提供統一的日誌記錄功能
"""

import logging
import os
from datetime import datetime


def setup_logger(name: str, log_file: str = None, level=logging.INFO) -> logging.Logger:
    """
    設定並返回一個 logger 實例
    :param name: logger 名稱
    :param log_file: 日誌檔案路徑（可選）
    :param level: 日誌級別
    :return: Logger 實例
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 避免重複添加 handler
    if logger.handlers:
        return logger

    # 建立格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 控制台 handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 檔案 handler（如果指定了檔案路徑）
    if log_file:
        # 確保日誌目錄存在
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_default_logger(name: str = 'stock_prediction') -> logging.Logger:
    """
    取得預設的 logger
    :param name: logger 名稱
    :return: Logger 實例
    """
    log_dir = os.path.join(os.getcwd(), 'logs')
    log_file = os.path.join(log_dir, f'{name}_{datetime.now().strftime("%Y%m%d")}.log')

    return setup_logger(name, log_file)
