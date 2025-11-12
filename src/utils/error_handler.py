"""
錯誤處理模組
提供統一的錯誤處理和異常管理
"""

from functools import wraps
from src.utils.logger import get_default_logger

logger = get_default_logger('error_handler')


class DataNotFoundError(Exception):
    """資料未找到錯誤"""
    pass


class ModelNotFoundError(Exception):
    """模型未找到錯誤"""
    pass


class InvalidDataFormatError(Exception):
    """無效的資料格式錯誤"""
    pass


class TrainingError(Exception):
    """模型訓練錯誤"""
    pass


class PredictionError(Exception):
    """預測錯誤"""
    pass


def handle_exceptions(func):
    """
    錯誤處理裝飾器
    自動捕獲並記錄函數執行中的異常
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DataNotFoundError as e:
            logger.error(f"資料未找到: {str(e)} in {func.__name__}")
            raise
        except ModelNotFoundError as e:
            logger.error(f"模型未找到: {str(e)} in {func.__name__}")
            raise
        except InvalidDataFormatError as e:
            logger.error(f"無效的資料格式: {str(e)} in {func.__name__}")
            raise
        except TrainingError as e:
            logger.error(f"模型訓練失敗: {str(e)} in {func.__name__}")
            raise
        except PredictionError as e:
            logger.error(f"預測失敗: {str(e)} in {func.__name__}")
            raise
        except Exception as e:
            logger.error(f"未預期的錯誤: {str(e)} in {func.__name__}", exc_info=True)
            raise

    return wrapper


def validate_input(data: any, expected_type: type, field_name: str = "input") -> None:
    """
    驗證輸入資料類型
    :param data: 要驗證的資料
    :param expected_type: 期望的類型
    :param field_name: 欄位名稱
    :raises InvalidDataFormatError: 當資料類型不符時
    """
    if not isinstance(data, expected_type):
        raise InvalidDataFormatError(
            f"{field_name} 必須是 {expected_type.__name__} 類型，但收到 {type(data).__name__}"
        )


def validate_required_fields(data: dict, required_fields: list) -> None:
    """
    驗證必要欄位是否存在
    :param data: 資料字典
    :param required_fields: 必要欄位列表
    :raises InvalidDataFormatError: 當缺少必要欄位時
    """
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        raise InvalidDataFormatError(
            f"缺少必要欄位: {', '.join(missing_fields)}"
        )


def validate_range(value: int or float, min_val: int or float,
                   max_val: int or float, field_name: str = "value") -> None:
    """
    驗證數值是否在指定範圍內
    :param value: 要驗證的值
    :param min_val: 最小值
    :param max_val: 最大值
    :param field_name: 欄位名稱
    :raises InvalidDataFormatError: 當值超出範圍時
    """
    if not (min_val <= value <= max_val):
        raise InvalidDataFormatError(
            f"{field_name} 必須在 {min_val} 到 {max_val} 之間，但收到 {value}"
        )
