# 部署指南

本文件提供將股價漲跌機率預測系統部署到生產環境的指引。

## 部署前準備

### 系統需求

- **作業系統**: Ubuntu 20.04 LTS 或以上（建議）/ Windows Server 2019 或以上
- **Python**: 3.12 或以上
- **記憶體**: 至少 8GB RAM
- **儲存空間**: 至少 10GB 可用空間
- **網路**: 穩定的網路連線

### 安全性檢查清單

- [ ] 更改預設密鑰 (SECRET_KEY)
- [ ] 設定防火牆規則
- [ ] 啟用 HTTPS
- [ ] 設定適當的檔案權限
- [ ] 設定環境變數
- [ ] 配置日誌系統
- [ ] 設定自動備份

## 部署方式

### 方式 1: 直接部署（適合小型應用）

#### 1. 準備伺服器

```bash
# 更新系統
sudo apt update && sudo apt upgrade -y

# 安裝必要套件
sudo apt install python3.12 python3.12-venv python3-pip nginx -y
```

#### 2. 部署應用程式

```bash
# 建立應用程式目錄
sudo mkdir -p /var/www/stock-prediction
cd /var/www/stock-prediction

# Clone 專案
git clone <repository-url> .

# 建立虛擬環境
python3.12 -m venv venv
source venv/bin/activate

# 安裝依賴
pip install -r requirements.txt

# 設定環境變數
sudo nano /etc/environment
# 添加以下內容：
# SECRET_KEY=<your-secret-key>
# FLASK_ENV=production
```

#### 3. 設定系統服務

建立 Flask 後端服務：

```bash
sudo nano /etc/systemd/system/stock-prediction-api.service
```

內容：

```ini
[Unit]
Description=Stock Prediction API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/stock-prediction
Environment="PATH=/var/www/stock-prediction/venv/bin"
ExecStart=/var/www/stock-prediction/venv/bin/python src/app.py

[Install]
WantedBy=multi-user.target
```

建立 Dash 前端服務：

```bash
sudo nano /etc/systemd/system/stock-prediction-dash.service
```

內容：

```ini
[Unit]
Description=Stock Prediction Dashboard
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/stock-prediction
Environment="PATH=/var/www/stock-prediction/venv/bin"
ExecStart=/var/www/stock-prediction/venv/bin/python src/ui/dashboard.py

[Install]
WantedBy=multi-user.target
```

啟動服務：

```bash
sudo systemctl daemon-reload
sudo systemctl start stock-prediction-api
sudo systemctl start stock-prediction-dash
sudo systemctl enable stock-prediction-api
sudo systemctl enable stock-prediction-dash

# 檢查狀態
sudo systemctl status stock-prediction-api
sudo systemctl status stock-prediction-dash
```

#### 4. 設定 Nginx 反向代理

```bash
sudo nano /etc/nginx/sites-available/stock-prediction
```

內容：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # API 端點
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Dashboard
    location / {
        proxy_pass http://localhost:8050;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

啟用站點：

```bash
sudo ln -s /etc/nginx/sites-available/stock-prediction /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 5. 設定 HTTPS（使用 Let's Encrypt）

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### 方式 2: Docker 部署（建議）

#### 1. 建立 Dockerfile

建立 `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 複製需求檔案
COPY requirements.txt .

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式
COPY . .

# 建立必要目錄
RUN mkdir -p data/uploads data/processed_data models/saved_models models/metadata logs

# 設定環境變數
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

EXPOSE 5000 8050

# 預設命令
CMD ["python", "src/app.py"]
```

#### 2. 建立 docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build: .
    container_name: stock-prediction-api
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
      - ./models:/app/models
      - ./logs:/app/logs
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - FLASK_ENV=production
    restart: unless-stopped
    command: python src/app.py

  dashboard:
    build: .
    container_name: stock-prediction-dash
    ports:
      - "8050:8050"
    volumes:
      - ./data:/app/data
      - ./models:/app/models
    environment:
      - FLASK_API_URL=http://api:5000
    depends_on:
      - api
    restart: unless-stopped
    command: python src/ui/dashboard.py

  nginx:
    image: nginx:alpine
    container_name: stock-prediction-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - api
      - dashboard
    restart: unless-stopped
```

#### 3. 部署

```bash
# 建立 .env 檔案
echo "SECRET_KEY=$(openssl rand -hex 32)" > .env

# 啟動服務
docker-compose up -d

# 檢查狀態
docker-compose ps

# 查看日誌
docker-compose logs -f
```

## 效能優化

### 1. 使用 Gunicorn (生產環境 WSGI 伺服器)

```bash
pip install gunicorn
```

更新服務檔案，將 `ExecStart` 改為：

```
ExecStart=/var/www/stock-prediction/venv/bin/gunicorn \
    --workers 4 \
    --bind 0.0.0.0:5000 \
    --timeout 120 \
    src.app:create_app()
```

### 2. 快取設定

在 Nginx 配置中添加快取：

```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=cache:10m max_size=1g;

location /api {
    proxy_cache cache;
    proxy_cache_valid 200 5m;
    proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
}
```

### 3. 資料庫優化

如果未來添加資料庫：

- 使用連線池
- 建立適當的索引
- 定期清理舊資料

## 監控與維護

### 1. 日誌管理

設定 logrotate：

```bash
sudo nano /etc/logrotate.d/stock-prediction
```

內容：

```
/var/www/stock-prediction/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload stock-prediction-api
        systemctl reload stock-prediction-dash
    endscript
}
```

### 2. 監控設定

使用 systemd 監控服務狀態：

```bash
# 檢查服務狀態
systemctl status stock-prediction-api
systemctl status stock-prediction-dash

# 查看日誌
journalctl -u stock-prediction-api -f
```

### 3. 自動備份

建立備份腳本：

```bash
sudo nano /usr/local/bin/backup-stock-prediction.sh
```

內容：

```bash
#!/bin/bash

BACKUP_DIR="/var/backups/stock-prediction"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# 備份模型和資料
tar -czf $BACKUP_DIR/models_$DATE.tar.gz /var/www/stock-prediction/models
tar -czf $BACKUP_DIR/data_$DATE.tar.gz /var/www/stock-prediction/data

# 保留最近 7 天的備份
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

設定 cron job：

```bash
sudo crontab -e

# 每天凌晨 2 點執行備份
0 2 * * * /usr/local/bin/backup-stock-prediction.sh
```

## 疑難排解

### 常見問題

1. **服務無法啟動**
   - 檢查日誌：`journalctl -u stock-prediction-api -n 50`
   - 檢查權限：`ls -la /var/www/stock-prediction`
   - 檢查 Python 路徑：`which python3.12`

2. **記憶體不足**
   - 調整 worker 數量
   - 增加系統記憶體
   - 使用 swap 空間

3. **連線逾時**
   - 增加 Gunicorn timeout 設定
   - 檢查網路防火牆設定
   - 調整 Nginx proxy_read_timeout

## 安全性建議

1. **定期更新**
   ```bash
   sudo apt update && sudo apt upgrade -y
   pip install --upgrade -r requirements.txt
   ```

2. **防火牆設定**
   ```bash
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

3. **限制存取**
   - 使用 API 金鑰或 JWT 驗證
   - 設定 rate limiting
   - 使用 CORS 限制

4. **資料加密**
   - 使用 HTTPS
   - 加密敏感資料
   - 定期更換密鑰

## 擴展性考量

如果需要處理大量請求：

1. **水平擴展**: 使用多個伺服器實例和負載平衡器
2. **資料庫**: 添加 PostgreSQL 或 MongoDB
3. **快取層**: 使用 Redis 快取預測結果
4. **非同步處理**: 使用 Celery 進行模型訓練

## 檢查清單

部署前確認：

- [ ] 環境變數已設定
- [ ] 資料庫已初始化（如適用）
- [ ] 日誌系統正常運作
- [ ] 備份系統已設定
- [ ] 監控系統已啟用
- [ ] HTTPS 已設定
- [ ] 防火牆規則已配置
- [ ] 效能測試已完成
- [ ] 安全性掃描已完成

部署後確認：

- [ ] 所有服務正常運行
- [ ] API 端點可存取
- [ ] 前端介面可存取
- [ ] 日誌正常記錄
- [ ] 備份正常執行
- [ ] 監控系統正常顯示資料

祝您部署順利！
