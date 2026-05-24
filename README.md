# 数据分析与可视化 Web 应用

前后端分离的数据分析与可视化平台，支持 CSV/Excel 数据接入、数据预览与清洗、交互式图表分析、结果导出。

## 技术栈

- **后端**：Python 3.10+，FastAPI，Uvicorn，pandas，numpy，openpyxl，chardet
- **前端**：Vue 3，Vite，TypeScript，Element Plus，ECharts (vue-echarts)，Pinia，Vue Router，axios

## 项目结构

```
.
├── backend/                # FastAPI 后端
│   ├── main.py             # 入口
│   ├── config.py           # 配置
│   ├── requirements.txt    # Python 依赖
│   ├── routers/            # API 路由
│   │   ├── datasets.py     # 数据集上传/列表/预览/导出
│   │   ├── analysis.py     # 数据清洗/字段信息
│   │   └── charts.py       # 图表数据聚合
│   ├── services/           # 业务逻辑
│   │   ├── file_parser.py  # CSV/Excel 解析
│   │   ├── data_summary.py # 数据预览与统计
│   │   ├── data_cleaning.py# 清洗操作
│   │   └── chart_data.py   # 图表数据生成
│   ├── models/
│   │   └── schemas.py      # Pydantic 模型
│   └── utils/
│       └── file_storage.py # 临时文件管理
├── frontend/               # Vue 3 前端
│   ├── src/
│   │   ├── views/          # 页面
│   │   ├── components/     # 组件
│   │   ├── stores/         # Pinia 状态
│   │   ├── router/         # 路由
│   │   ├── api/            # axios 封装
│   │   └── types/          # TS 类型
│   └── ...
└── README.md
```

## 环境要求

- Python 3.10+
- Node.js 18+
- npm 或 yarn

## 快速启动

### 1. 启动后端

```bash
cd backend

# 创建虚拟环境（推荐）
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

启动后访问：
- API 文档：http://localhost:8000/docs
- Health：http://localhost:8000/health

### 2. 启动前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

启动后访问：http://localhost:5173

前端已配置代理，API 请求会自动转发到 `http://localhost:8000`。

## 使用指南

### 工作区管理
1. 打开首页，可看到默认工作区。
2. 点击"新建工作区"创建新的分析空间。
3. 点击"进入工作区"开始分析。

### 数据集管理
1. 在左侧菜单选择"数据集管理"。
2. 拖拽或点击上传 CSV/Excel 文件。
3. 点击数据集名称查看预览、字段信息和缺失值统计。
4. 在"数据清洗"面板添加操作（删除空值、填充空值、删除重复行、修改字段类型），点击"应用操作"。
5. 点击"导出 CSV"或"导出 Excel"下载清洗后的数据。

### 可视化分析
1. 在左侧菜单选择"可视化分析"。
2. 选择要分析的数据集。
3. 配置图表类型（柱状图/折线图/饼图）、X 轴字段、Y 轴字段、聚合方式。
4. 可选设置分组字段，生成多系列图表。
5. 点击"生成图表"实时渲染。
6. 点击"导出 PNG"下载图表图片。

## Phase 1 功能范围

- [x] 工作区管理（内存状态，无持久化）
- [x] CSV/Excel 文件上传与解析
- [x] 数据预览（前 100 行）
- [x] 字段类型推断、缺失值统计
- [x] 数据清洗：删除空值、填充空值、删除重复行、修改字段类型
- [x] 柱状图、折线图、饼图
- [x] 数值聚合：求和、平均、计数、最大值、最小值
- [x] 按分类字段分组
- [x] 图表导出 PNG
- [x] 数据导出 CSV/Excel

## 后续计划

- **Phase 2**：PDF/Word 表格提取、数据库连接、散点图/箱线图/热力图、词云
- **Phase 3**：PDF 报告合成、后端数据持久化、用户认证

## 注意事项

- 文件上传后保存在 `uploads/` 目录，项目重启后数据集元数据会丢失（Phase 1 设计）。
- 数据库连接信息在 Phase 1 中未实现，仅在 Phase 2 提供。
- 建议在生产环境使用时添加用户认证和持久化存储。
