# Real Estate Investment Return Simulator

## 部署步骤

### 1. 环境准备
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 本地运行
```bash
# 启动应用
streamlit run app.py
```

### 3. 部署到 Streamlit Cloud
1. 访问 [Streamlit Cloud](https://streamlit.io/cloud)
2. 使用 GitHub 账号登录
3. 点击 "New app"
4. 选择您的 GitHub 仓库
5. 选择主分支 (main)
6. 设置主文件路径为 `app.py`
7. 点击 "Deploy"

### 4. 数据目录设置
- 确保 `data/` 目录存在
- 首次运行时会自动创建必要的数据库文件

## 主要依赖
- streamlit==1.32.0
- numpy
- pandas
- plotly
- numpy-financial
- sqlalchemy
- reportlab==4.1.0
- openpyxl==3.1.2
- pytest==8.0.0
- python-dotenv==1.0.1

## 项目结构
```
real_estate_simulator/
├── app.py              # 主应用程序
├── requirements.txt    # 项目依赖
├── src/               # 源代码目录
│   ├── calculator.py  # 投资计算器
│   ├── visualizer.py  # 数据可视化
│   ├── input_handler.py # 输入处理
│   ├── report_generator.py # 报告生成
│   └── db.py         # 数据库操作
├── data/             # 数据目录
└── tests/            # 测试目录
```

## 开发说明
1. 所有代码更改应通过 GitHub 进行版本控制
2. 使用 GitHub Desktop 进行代码管理
3. 定期同步远程仓库
4. 新功能开发应在独立分支进行 