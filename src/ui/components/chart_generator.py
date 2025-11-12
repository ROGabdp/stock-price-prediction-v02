"""
圖表生成器模組
使用 Plotly 根據歷史和預測數據生成視覺化圖表
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Optional


class ChartGenerator:
    """
    負責生成各種股價相關的圖表
    """

    def __init__(self):
        """初始化圖表生成器"""
        self.default_colors = {
            'historical': '#1f77b4',  # 藍色
            'prediction': '#ff7f0e',  # 橘色
            'up': '#2ca02c',          # 綠色
            'down': '#d62728'         # 紅色
        }

    def generate_historical_chart(self, historical_data: pd.DataFrame) -> go.Figure:
        """
        生成歷史股價圖表
        :param historical_data: 包含 'date' 和 'close' 欄位的 DataFrame
        :return: Plotly Figure 物件
        """
        if historical_data.empty:
            raise ValueError("歷史資料不能為空")

        if 'date' not in historical_data.columns or 'close' not in historical_data.columns:
            raise KeyError("歷史資料必須包含 'date' 和 'close' 欄位")

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=historical_data['date'],
            y=historical_data['close'],
            mode='lines',
            name='歷史收盤價',
            line=dict(color=self.default_colors['historical'], width=2)
        ))

        fig.update_layout(
            title='歷史股價走勢',
            xaxis_title='日期',
            yaxis_title='收盤價',
            hovermode='x unified',
            template='plotly_white'
        )

        return fig

    def generate_prediction_chart(self, prediction_data: pd.DataFrame) -> go.Figure:
        """
        生成預測結果圖表
        :param prediction_data: 包含 'target_date', 'up_down_probability', 'change_magnitude' 的 DataFrame
        :return: Plotly Figure 物件
        """
        if prediction_data.empty:
            raise ValueError("預測資料不能為空")

        # 建立子圖：上方顯示漲跌機率，下方顯示漲跌幅度
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('漲跌機率', '預測漲跌幅度'),
            vertical_spacing=0.15
        )

        # 漲跌機率圖表
        colors = [self.default_colors['up'] if prob >= 0.5 else self.default_colors['down']
                  for prob in prediction_data['up_down_probability']]

        fig.add_trace(
            go.Bar(
                x=prediction_data['target_date'],
                y=prediction_data['up_down_probability'],
                name='漲跌機率',
                marker_color=colors
            ),
            row=1, col=1
        )

        # 漲跌幅度圖表
        magnitude_colors = [self.default_colors['up'] if mag >= 0 else self.default_colors['down']
                           for mag in prediction_data['change_magnitude']]

        fig.add_trace(
            go.Bar(
                x=prediction_data['target_date'],
                y=prediction_data['change_magnitude'],
                name='漲跌幅度',
                marker_color=magnitude_colors
            ),
            row=2, col=1
        )

        fig.update_xaxes(title_text="日期", row=2, col=1)
        fig.update_yaxes(title_text="機率", row=1, col=1)
        fig.update_yaxes(title_text="幅度 (%)", row=2, col=1)

        fig.update_layout(
            title='預測結果',
            hovermode='x unified',
            template='plotly_white',
            showlegend=False,
            height=600
        )

        return fig

    def generate_combined_chart(self,
                                historical_data: pd.DataFrame,
                                prediction_data: pd.DataFrame,
                                last_close_price: Optional[float] = None) -> go.Figure:
        """
        生成結合歷史與預測的綜合圖表
        :param historical_data: 歷史資料 DataFrame
        :param prediction_data: 預測資料 DataFrame
        :param last_close_price: 最後一個收盤價（用於計算預測價格）
        :return: Plotly Figure 物件
        """
        if historical_data.empty:
            raise ValueError("歷史資料不能為空")

        if prediction_data.empty:
            raise ValueError("預測資料不能為空")

        fig = go.Figure()

        # 繪製歷史收盤價
        fig.add_trace(go.Scatter(
            x=historical_data['date'],
            y=historical_data['close'],
            mode='lines',
            name='歷史收盤價',
            line=dict(color=self.default_colors['historical'], width=2)
        ))

        # 計算預測價格
        if last_close_price is None:
            last_close_price = historical_data['close'].iloc[-1]

        predicted_prices = []
        current_price = last_close_price

        for magnitude in prediction_data['change_magnitude']:
            current_price = current_price * (1 + magnitude)
            predicted_prices.append(current_price)

        # 繪製預測價格
        fig.add_trace(go.Scatter(
            x=prediction_data['target_date'],
            y=predicted_prices,
            mode='lines+markers',
            name='預測價格',
            line=dict(color=self.default_colors['prediction'], width=2, dash='dash'),
            marker=dict(size=8)
        ))

        # 添加連接線（從最後歷史點到第一個預測點）
        fig.add_trace(go.Scatter(
            x=[historical_data['date'].iloc[-1], prediction_data['target_date'].iloc[0]],
            y=[last_close_price, predicted_prices[0]],
            mode='lines',
            name='連接線',
            line=dict(color='gray', width=1, dash='dot'),
            showlegend=False
        ))

        fig.update_layout(
            title='歷史股價與預測趨勢',
            xaxis_title='日期',
            yaxis_title='收盤價',
            hovermode='x unified',
            template='plotly_white',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        return fig

    def generate_probability_heatmap(self, prediction_data: pd.DataFrame) -> go.Figure:
        """
        生成漲跌機率熱力圖
        :param prediction_data: 預測資料 DataFrame
        :return: Plotly Figure 物件
        """
        if prediction_data.empty:
            raise ValueError("預測資料不能為空")

        fig = go.Figure(data=go.Heatmap(
            x=prediction_data['target_date'],
            y=['漲跌機率'],
            z=[prediction_data['up_down_probability'].values],
            colorscale='RdYlGn',
            zmid=0.5,
            text=prediction_data['up_down_probability'].values,
            texttemplate='%{text:.2%}',
            textfont={"size": 12},
            colorbar=dict(title="機率")
        ))

        fig.update_layout(
            title='漲跌機率熱力圖',
            xaxis_title='預測日期',
            template='plotly_white',
            height=200
        )

        return fig
