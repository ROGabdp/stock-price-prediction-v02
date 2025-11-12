import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

class DataPreprocessor:
    def __init__(self):
        self.scaler = None

    def feature_engineering(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        對原始數據進行特徵工程。
        :param df: 原始 DataFrame，包含 'Open', 'High', 'Low', 'Close', 'Volume' 等。
        :return: 包含新特徵的 DataFrame。
        """
        # 刪除全是 NaN 的欄位和 Unnamed 欄位
        df = df.dropna(axis=1, how='all')  # 刪除全是 NaN 的欄位
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]  # 刪除 Unnamed 欄位

        # 刪除包含亂碼的欄位（非 ASCII 字元）
        ascii_cols = [col for col in df.columns if col.isascii()]
        df = df[ascii_cols]

        # 移除 'date' 欄位，因為它不應該作為數值特徵
        if 'date' in df.columns:
            df = df.drop(columns=['date'])
        elif 'Date' in df.columns:
            df = df.drop(columns=['Date'])

        # 確定收盤價欄位名稱（支援大小寫）
        close_col = 'close' if 'close' in df.columns else 'Close'

        # 計算每日收益
        df['Daily_Return'] = df[close_col].pct_change()

        # 計算波動率 (例如，使用 7 天移動標準差)
        df['Volatility'] = df['Daily_Return'].rolling(window=7).std()

        # 添加更多技術指標 (如果原始數據中沒有，可以根據需要計算)
        # 例如：簡單移動平均線 (SMA)
        df['SMA_7'] = df[close_col].rolling(window=7).mean()
        df['SMA_30'] = df[close_col].rolling(window=30).mean()

        # 例如：指數移動平均線 (EMA)
        df['EMA_7'] = df[close_col].ewm(span=7, adjust=False).mean()

        # 例如：相對強弱指數 (RSI) - 這裡只是一個簡化範例，實際計算較複雜
        # delta = df[close_col].diff()
        # gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        # loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        # rs = gain / loss
        # df['RSI'] = 100 - (100 / (1 + rs))

        # 刪除包含 NaN 的行，這些 NaN 是由於計算移動平均或 pct_change 造成的
        df.dropna(inplace=True)

        return df

    def normalize_data(self, df: pd.DataFrame) -> tuple[pd.DataFrame, MinMaxScaler]:
        """
        使用 MinMaxScaler 對數據進行正規化。
        :param df: 包含特徵的 DataFrame。
        :return: 正規化後的 DataFrame 和 MinMaxScaler 實例。
        """
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        normalized_data = self.scaler.fit_transform(df)
        normalized_df = pd.DataFrame(normalized_data, columns=df.columns, index=df.index)
        return normalized_df, self.scaler

    def create_sequences(self, data: pd.DataFrame, look_back: int, forecast_horizon: int, target_column: str):
        """
        從時間序列數據創建輸入序列 (X) 和目標值 (y)。
        :param data: 包含所有特徵的 DataFrame (已正規化)。
        :param look_back: 用於預測的歷史時間步長。
        :param forecast_horizon: 預測未來的天數。
        :param target_column: 目標欄位名稱 (例如 'Close')。
        :return: (X, y) - X 是輸入序列，y 是目標值。
        """
        X, y = [], []
        # 找到目標欄位的索引
        target_idx = data.columns.get_loc(target_column)

        for i in range(len(data) - look_back - forecast_horizon + 1):
            # 輸入序列 (X) 是從當前位置開始的 look_back 個時間步
            X.append(data.iloc[i:(i + look_back)].values)
            # 目標值 (y) 是從 look_back 之後的 forecast_horizon 個時間步的目標欄位值
            # 這裡假設我們預測的是目標欄位的未來值
            y.append(data.iloc[(i + look_back):(i + look_back + forecast_horizon), target_idx].values)

        return np.array(X), np.array(y)

    def preprocess(self, df: pd.DataFrame, look_back: int, forecast_horizon: int, target_column: str):
        """
        執行完整的預處理流程：特徵工程 -> 正規化 -> 序列創建。
        :param df: 原始 DataFrame。
        :param look_back: 用於預測的歷史時間步長。
        :param forecast_horizon: 預測未來的天數。
        :param target_column: 目標欄位名稱（支援大小寫，如 'close' 或 'Close'）。
        :return: (X, y, scaler) - X 是輸入序列，y 是目標值，scaler 是用於正規化的 MinMaxScaler 實例。
        """
        df_features = self.feature_engineering(df.copy())
        normalized_df, self.scaler = self.normalize_data(df_features)

        # 自動偵測目標欄位名稱（不區分大小寫）
        actual_target_col = None
        for col in normalized_df.columns:
            if col.lower() == target_column.lower():
                actual_target_col = col
                break

        if actual_target_col is None:
            raise ValueError(f"找不到目標欄位 '{target_column}'。可用欄位: {list(normalized_df.columns)}")

        X, y = self.create_sequences(normalized_df, look_back, forecast_horizon, actual_target_col)
        return X, y, self.scaler

    def inverse_transform_target(self, scaled_target: np.ndarray, target_column: str) -> np.ndarray:
        """
        將正規化後的目標值反向轉換回原始尺度。
        :param scaled_target: 正規化後的目標值。
        :param target_column: 目標欄位名稱。
        :return: 原始尺度的目標值。
        """
        if self.scaler is None:
            raise ValueError("Scaler 尚未初始化。請先執行 preprocess 方法。")

        # 創建一個與原始數據列數相同的零矩陣
        # 假設原始數據的列數可以從 scaler 的 feature_range_in_ 屬性中獲取
        # 或者從訓練時的 DataFrame 列數中獲取
        # 這裡需要一個更穩健的方法來獲取原始列數，暫時假設一個足夠大的數
        # 更好的方法是儲存原始 DataFrame 的列名和順序
        
        # 為了能夠反向轉換單一目標列，我們需要知道該列在原始數據中的位置
        # 並創建一個全零的陣列，將 scaled_target 放入正確的位置
        # 這裡假設我們在 preprocess 階段儲存了原始數據的列名
        # 為了簡化，我們假設 target_column 是原始數據中的一列，並且 scaler 知道所有列
        
        # 這裡需要一個更精確的方法來處理，目前先用一個簡化的方法
        # 假設 scaler 是針對所有特徵進行 fit 的
        dummy_array = np.zeros((scaled_target.shape[0], self.scaler.n_features_in_))
        target_idx = self.scaler.feature_names_in_.tolist().index(target_column) if hasattr(self.scaler, 'feature_names_in_') else None
        
        if target_idx is None:
            # 如果沒有 feature_names_in_，則需要手動指定目標列的索引
            # 這裡假設 target_column 是最後一列，或者需要一個映射
            # 為了測試，我們假設 target_column 是原始數據中的某一列，並且我們知道它的索引
            # 這裡需要一個更通用的方法來處理
            raise ValueError("無法確定目標欄位在 scaler 中的索引。")

        dummy_array[:, target_idx] = scaled_target.flatten()
        inverted_data = self.scaler.inverse_transform(dummy_array)
        return inverted_data[:, target_idx]
