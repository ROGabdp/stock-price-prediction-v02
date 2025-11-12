from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import sys
import os

# 將專案根目錄加入 Python 路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.ui.components.chart_generator import ChartGenerator
from src.ui.components.data_selector import DataSelector
from src.ui.components.model_selector import ModelSelector
import pandas as pd
import requests
import base64
import io

def create_dashboard(flask_api_url='http://localhost:5000'):
    """
    建立 Dash 儀表板應用程式
    :param flask_api_url: Flask 後端 API 的基礎 URL
    """
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    chart_gen = ChartGenerator()
    data_selector = DataSelector()
    model_selector = ModelSelector()

    app.layout = html.Div([
        html.H1("股價漲跌機率預測系統", className="text-center my-4"),

        dbc.Container([
            dbc.Row([
                dbc.Col(html.H2("資料選擇與模型訓練", className="text-primary"), width=12),
            ]),
            dbc.Row([
                dbc.Col(dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        '拖曳或 ',
                        html.A('選擇檔案')
                    ]),
                    style={
                        'width': '100%', 'height': '60px', 'lineHeight': '60px',
                        'borderWidth': '1px', 'borderStyle': 'dashed',
                        'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'
                    },
                    multiple=False
                ), width=6),
                dbc.Col(dcc.Dropdown(
                    id='dataset-selector',
                    options=[],
                    placeholder="選擇資料集",
                ), width=6),
            ]),
            dbc.Row([
                dbc.Col(dcc.Input(
                    id='n-days-input',
                    type='number',
                    value=5,
                    min=1,
                    max=30,
                    placeholder="預測天數 (N)",
                ), width=6),
                dbc.Col(dbc.Button("開始訓練模型", id='train-button', color="primary", className="me-1"), width=6),
            ]),
            html.Div(id='output-data-upload'),
            html.Div(id='training-status'),
        ], className="mb-4"),

        dbc.Container([
            dbc.Row([
                dbc.Col(html.H2("模型選擇與預測結果", className="text-primary"), width=12),
            ]),
            dbc.Row([
                dbc.Col(dcc.Dropdown(
                    id='model-selector',
                    options=[],
                    placeholder="選擇模型",
                ), width=6),
                dbc.Col(dbc.Button("顯示預測", id='predict-button', color="success", className="me-1"), width=6),
            ]),
            html.Div(id='prediction-output'),
            dcc.Graph(id='historical-chart'),
            dcc.Graph(id='combined-chart'),
            dcc.Graph(id='prediction-chart'),
        ]),

        # 儲存 API URL
        dcc.Store(id='api-url', data=flask_api_url)
    ])

    # Callback: 更新資料集選擇器選項
    @app.callback(
        Output('dataset-selector', 'options'),
        Input('api-url', 'data')
    )
    def update_dataset_options(api_url):
        """取得可用資料集列表"""
        return data_selector.get_dropdown_options()

    # Callback: 更新模型選擇器選項
    @app.callback(
        Output('model-selector', 'options'),
        Input('api-url', 'data')
    )
    def update_model_options(api_url):
        """從 API 取得已訓練模型列表"""
        return model_selector.get_dropdown_options()

    # Callback: 處理資料上傳
    @app.callback(
        Output('output-data-upload', 'children'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
        State('api-url', 'data')
    )
    def handle_data_upload(contents, filename, api_url):
        """處理資料上傳"""
        if contents is None:
            return ""

        try:
            # 解析上傳的檔案
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)

            # 使用檔名作為資料集名稱
            dataset_name = filename

            # 發送到 Flask API
            files = {'file': (filename, io.BytesIO(decoded), 'text/csv')}
            data = {'dataset_name': dataset_name}

            response = requests.post(f'{api_url}/api/data/upload', files=files, data=data)

            if response.status_code == 200:
                return dbc.Alert(f"資料集 {dataset_name} 上傳成功！", color="success")
            else:
                error = response.json().get('error', '未知錯誤')
                return dbc.Alert(f"上傳失敗: {error}", color="danger")

        except Exception as e:
            return dbc.Alert(f"上傳時發生錯誤: {str(e)}", color="danger")

    # Callback: 處理訓練按鈕
    @app.callback(
        Output('training-status', 'children'),
        Input('train-button', 'n_clicks'),
        [State('dataset-selector', 'value'),
         State('n-days-input', 'value'),
         State('api-url', 'data')],
        prevent_initial_call=True
    )
    def handle_train(n_clicks, dataset_name, n_days, api_url):
        """處理模型訓練請求"""
        if not n_clicks:
            return ""

        if not dataset_name:
            return dbc.Alert("請先選擇資料集！", color="warning")

        if not n_days:
            return dbc.Alert("請輸入預測天數！", color="warning")

        try:
            # 發送訓練請求
            payload = {
                'dataset_name': dataset_name,
                'n_days': int(n_days)
            }

            response = requests.post(f'{api_url}/api/model/train', json=payload)

            if response.status_code == 202:
                result = response.json()
                task_id = result.get('task_id', 'unknown')
                return dbc.Alert([
                    html.H5("✅ 訓練已開始！", className="alert-heading"),
                    html.P(f"任務 ID: {task_id}"),
                    html.P(f"資料集: {dataset_name}"),
                    html.P(f"預測天數: {n_days} 天"),
                    html.Hr(),
                    html.P([
                        "訓練可能需要幾分鐘時間，請耐心等待。",
                        html.Br(),
                        "您可以在終端查看訓練進度。",
                        html.Br(),
                        "完成後，模型將自動出現在模型選擇器中。"
                    ], className="mb-0")
                ], color="success")
            else:
                error = response.json().get('error', '未知錯誤')
                return dbc.Alert(f"訓練失敗: {error}", color="danger")

        except Exception as e:
            return dbc.Alert(f"發生錯誤: {str(e)}", color="danger")

    # Callback: 顯示歷史圖表和預測結果
    @app.callback(
        [Output('historical-chart', 'figure'),
         Output('combined-chart', 'figure'),
         Output('prediction-chart', 'figure'),
         Output('prediction-output', 'children')],
        [Input('predict-button', 'n_clicks')],
        [State('model-selector', 'value'),
         State('dataset-selector', 'value'),
         State('n-days-input', 'value'),
         State('api-url', 'data')]
    )
    def display_charts(n_clicks, model_id, dataset_name, n_days, api_url):
        """顯示歷史和預測圖表"""
        if not n_clicks or not model_id or not dataset_name:
            # 返回空圖表
            empty_fig = {}
            return empty_fig, empty_fig, empty_fig, "請選擇模型和資料集"

        try:
            # 取得歷史資料
            hist_response = requests.get(f'{api_url}/api/data/history', params={'dataset_name': dataset_name})
            if hist_response.status_code != 200:
                return {}, {}, {}, f"無法載入歷史資料: {hist_response.json().get('error', '未知錯誤')}"

            historical_data = pd.DataFrame(hist_response.json())
            historical_data['date'] = pd.to_datetime(historical_data['date'])

            # 取得預測結果
            pred_response = requests.get(f'{api_url}/api/model/predict',
                                        params={'model_id': model_id, 'n_days': n_days})
            if pred_response.status_code != 200:
                return {}, {}, {}, f"無法取得預測結果: {pred_response.json().get('error', '未知錯誤')}"

            prediction_data = pd.DataFrame(pred_response.json())
            prediction_data['target_date'] = pd.to_datetime(prediction_data['target_date'])

            # 生成圖表
            hist_fig = chart_gen.generate_historical_chart(historical_data)
            combined_fig = chart_gen.generate_combined_chart(historical_data, prediction_data)
            pred_fig = chart_gen.generate_prediction_chart(prediction_data)

            output_msg = dbc.Alert(f"已成功載入模型 {model_id} 的預測結果", color="success")

            return hist_fig, combined_fig, pred_fig, output_msg

        except Exception as e:
            error_msg = dbc.Alert(f"發生錯誤: {str(e)}", color="danger")
            return {}, {}, {}, error_msg

    return app

if __name__ == '__main__':
    app = create_dashboard()
    app.run(debug=True, port=8050)
