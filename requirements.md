# Real Estate Investment Return Simulator
## 需求文档版本：v1.1
## 创建时间：2025-05-26

## 1. 项目概述
### 1.1 项目背景
基于十多年房地产投资经验，开发一款模拟工具，帮助初学者、地产经纪和潜在买家理解并验证房地产投资的回报逻辑。该工具将基于真实投资经验，模拟从自住房开始，通过再融资逐步构建投资组合的完整路径。

### 1.2 项目目标
- 帮助用户模拟从自住房开始，通过再融资逐步构建投资组合的路径
- 根据收入、首付、贷款能力等现实变量评估可行性
- 提供10/20/30年期的资产增值、现金流与回报率演算
- 用直观方式展示投资路径与策略对比
- 可持续迭代，扩展更多投资场景

## 2. 功能需求
### 2.1 用户角色
1. 普通用户（初级投资者）
   - 有稳定收入
   - 拥有或即将购买自住房
   - 希望未来将自住房变为第一套投资房

2. 地产经纪
   - 帮助客户判断投资回报潜力
   - 根据客户不同情况生成个性化模拟报告

3. 高级用户/业主
   - 可输入多个投资物业组合
   - 用于真实资产组合分析、税务模拟与退出策略演算

### 2.2 MVP阶段核心功能
#### A. 前端输入模块
1. 基础信息收集
   - 家庭结构（单人/双人收入）
   - 年收入信息（个人1/个人2）
   - 退休目标（退休年龄、目标被动收入）
   - 净资产目标

2. 房产信息输入
   - 首套房类型（自住/投资）
   - 首付款信息
   - 目标购买价格
   - 交房日期
   - 贷款信息（利率、期限、摊销期）
   - 租金假设
   - 预期增值率
   - 空置率
   - 年度支出预估

3. 其他负债信息
   - 投资贷款
   - 汽车贷款
   - 信用卡债务

4. 再融资规划
   - 再融资次数
   - 再融资年份
   - 再融资策略

#### B. 后端建模模块
1. 贷款计算
   - 月供计算
   - 本金利息分摊
   - 贷款余额追踪
   - 再融资计算

2. 回报率计算
   - 标准ROI
   - 杠杆ROI
   - 税后净现金流回报率

3. 多周期模拟
   - 10年/20年/30年模拟
   - 阶段性模拟（1-5年、6-10年等）

#### C. 可视化展示模块
- 年度房产价值增长趋势图
- 净值增长vs贷款余额曲线图
- 净现金流柱状图
- ROI/杠杆率对比图
- 策略对比图表

#### D. 报告输出模块
- 英文报告输出（PDF格式）
- 详细表格数据
- 标准化页眉页脚

#### D+. 支出追踪模块
- 支出描述
- 支出类型分类
- 金额记录
- 日期记录
- 关联房产
- 年度支出汇总
- 单房产维护成本追踪

### 2.3 未来功能扩展（Phase 2+）
1. 语义提示引擎
   - 自然语言输入识别
   - 情境模拟触发
   - 风险场景分析

2. AI智能建议模块
   - 投资建议生成
   - 退出策略建议
   - 资产配置建议

3. 财务愿景与路径建议推演图
   - 目标达成路径可视化
   - 关键时间节点标注
   - 实际vs计划对比

4. 税务模块
   - CCA计算
   - 租金抵税
   - 资本增值税

5. 其他扩展功能
   - 维修周期模拟
   - 利率波动场景
   - 压力测试
   - 退出策略模拟
   - 多场景保存

## 3. 技术架构
### 3.1 开发环境
- 前端：Tally/Typeform（问答式表单）
- 后端：Python + Pandas + Streamlit
- 图表库：Matplotlib/Plotly
- 托管平台：Replit/Streamlit Cloud

### 3.2 系统架构
- 模块化设计
- 数据流处理
- API接口设计

## 4. 项目规划
### 4.1 开发周期
- MVP阶段：核心功能实现
- Phase 2：功能扩展
- 持续迭代优化

### 4.2 资源需求
- 开发团队
- 服务器资源
- 开发工具

## 5. 风险评估
### 5.1 潜在风险
- 技术实现风险
- 数据准确性风险
- 用户接受度风险

### 5.2 应对策略
- 分阶段开发
- 持续测试验证
- 用户反馈收集

## 6. 验收标准
### 6.1 功能验收
- 核心功能测试
- 性能测试
- 用户体验测试

### 6.2 文档验收
- 技术文档
- 用户手册
- 维护文档

## 7. 附录
### 7.1 术语表
[待补充]

### 7.2 参考文档
[待补充] 