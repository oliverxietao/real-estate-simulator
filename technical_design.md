# Real Estate Investment Return Simulator - 技术设计文档

## 1. 技术栈选择

### 1.1 前端技术栈
- **主框架**: Streamlit
  - 选择理由：快速开发、Python原生支持、内置数据可视化
  - 版本：最新稳定版
  - 优势：无需复杂前端开发，专注于业务逻辑

- **UI组件**:
  - Streamlit原生组件
  - Plotly用于交互式图表
  - 自定义CSS美化界面

### 1.2 后端技术栈
- **核心语言**: Python 3.9+
- **数据处理**:
  - Pandas: 数据处理和分析
  - NumPy: 数值计算
- **计算引擎**:
  - 自定义Python类处理投资计算
  - 使用numpy进行财务计算

### 1.3 数据存储
- **本地存储**:
  - SQLite: 用户数据和场景保存
  - JSON: 配置文件
- **文件存储**:
  - PDF生成: ReportLab
  - Excel导出: openpyxl

## 2. 系统架构

### 2.1 核心模块设计

#### A. 数据输入模块 (input_handler.py)
```python
class InputHandler:
    def __init__(self):
        self.required_fields = {
            'basic_info': ['income', 'retirement_age', 'target_income'],
            'property_info': ['purchase_price', 'down_payment', 'mortgage_rate'],
            'investment_info': ['expected_appreciation', 'rental_income']
        }
    
    def validate_input(self, data):
        # 输入验证逻辑
        pass
    
    def process_input(self, data):
        # 数据处理逻辑
        pass
```

#### B. 计算引擎模块 (calculator.py)
```python
class InvestmentCalculator:
    def __init__(self):
        self.mortgage_calculator = MortgageCalculator()
        self.roi_calculator = ROICalculator()
        self.cash_flow_calculator = CashFlowCalculator()
    
    def calculate_mortgage(self, principal, rate, years):
        # 贷款计算逻辑
        pass
    
    def calculate_roi(self, investment_data):
        # ROI计算逻辑
        pass
    
    def calculate_cash_flow(self, property_data):
        # 现金流计算逻辑
        pass
```

#### C. 可视化模块 (visualizer.py)
```python
class DataVisualizer:
    def __init__(self):
        self.chart_types = {
            'property_value': 'line',
            'cash_flow': 'bar',
            'roi_comparison': 'scatter'
        }
    
    def create_property_value_chart(self, data):
        # 房产价值趋势图
        pass
    
    def create_cash_flow_chart(self, data):
        # 现金流图表
        pass
```

#### D. 报告生成模块 (report_generator.py)
```python
class ReportGenerator:
    def __init__(self):
        self.template_loader = TemplateLoader()
        self.pdf_generator = PDFGenerator()
    
    def generate_report(self, data):
        # 报告生成逻辑
        pass
```

### 2.2 数据流设计

1. 用户输入流程：
   ```
   用户输入 -> InputHandler验证 -> 数据预处理 -> 存储到临时对象
   ```

2. 计算流程：
   ```
   预处理数据 -> InvestmentCalculator计算 -> 结果存储 -> 可视化准备
   ```

3. 展示流程：
   ```
   计算结果 -> DataVisualizer处理 -> Streamlit展示 -> 用户交互
   ```

## 3. 数据库设计

### 3.1 SQLite表结构

#### users表
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    created_at TIMESTAMP,
    email TEXT UNIQUE,
    name TEXT
);
```

#### scenarios表
```sql
CREATE TABLE scenarios (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    name TEXT,
    created_at TIMESTAMP,
    data JSON,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

#### properties表
```sql
CREATE TABLE properties (
    id INTEGER PRIMARY KEY,
    scenario_id INTEGER,
    property_type TEXT,
    purchase_price REAL,
    down_payment REAL,
    mortgage_rate REAL,
    created_at TIMESTAMP,
    FOREIGN KEY (scenario_id) REFERENCES scenarios(id)
);
```

## 4. API设计

### 4.1 内部API

#### 计算API
```python
class CalculationAPI:
    def calculate_mortgage(self, principal, rate, years):
        """计算月供和还款计划"""
        pass
    
    def calculate_roi(self, investment_data):
        """计算投资回报率"""
        pass
    
    def calculate_cash_flow(self, property_data):
        """计算现金流"""
        pass
```

#### 数据API
```python
class DataAPI:
    def save_scenario(self, user_id, scenario_data):
        """保存投资场景"""
        pass
    
    def load_scenario(self, scenario_id):
        """加载投资场景"""
        pass
    
    def export_report(self, scenario_id):
        """导出报告"""
        pass
```

## 5. 部署方案

### 5.1 开发环境
- Python 3.9+
- 虚拟环境: venv
- 依赖管理: requirements.txt

### 5.2 生产环境
- 容器化: Docker
- 部署平台: Streamlit Cloud
- 监控: 基础日志记录

## 6. 开发计划

### 6.1 MVP阶段（4周）

#### 第1周：基础架构
- 项目初始化
- 数据库设计
- 基础类实现

#### 第2周：核心功能
- 输入模块
- 计算引擎
- 基础可视化

#### 第3周：用户界面
- Streamlit界面开发
- 交互功能实现
- 数据验证

#### 第4周：测试和优化
- 单元测试
- 集成测试
- 性能优化

### 6.2 技术债务管理
- 代码审查
- 文档更新
- 性能监控

## 7. 安全考虑

### 7.1 数据安全
- 输入验证
- SQL注入防护
- 数据加密

### 7.2 访问控制
- 用户认证
- 权限管理
- 会话控制

## 8. 性能优化

### 8.1 计算优化
- 缓存机制
- 并行计算
- 数据预处理

### 8.2 响应优化
- 懒加载
- 数据分页
- 异步处理 