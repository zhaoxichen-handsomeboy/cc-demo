# CLAUDE.md

本文件为 Claude Code（claude.ai/code）在此仓库中工作时提供指引。

## 项目概述

数据分析与可视化 Web 应用 — 支持 CSV/Excel 数据导入、数据清洗和交互式图表（柱状图/折线图/饼图）的 SPA。Phase 1 使用内存状态（无持久化）。

## 开发命令

```bash
# 后端
cd backend && pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
# API 文档：http://localhost:8000/docs

# 前端
cd frontend && npm install
npm run dev     # 开发服务器 http://localhost:5173
npm run build   # 类型检查 (vue-tsc) + 生产构建
npm run preview # 预览生产构建
```

## 架构

```
backend/                          frontend/
  main.py           FastAPI 入口     src/
  config.py         配置               main.ts         Vue 应用启动
  routers/          API 路由层           views/          页面级组件
    datasets.py     上传/列表/导出        WorkspaceList.vue
    analysis.py     数据清洗               VisualAnalysis.vue
    charts.py       图表聚合               (DatasetManager.vue)
  services/         业务逻辑层           components/     可复用组件
    file_parser.py    CSV/Excel 解析     FileUploader.vue
    data_summary.py   统计与预览          DataPreviewTable.vue
    data_cleaning.py  删除空值/填充等     DataCleaningPanel.vue
    chart_data.py     groupby + 聚合     ChartRenderer.vue
  models/schemas.py Pydantic 模型        ChartConfigPanel.vue
  utils/                               ExportButtons.vue
    file_storage.py  临时文件管理        stores/         Pinia 状态管理
                                          workspace.ts
                                          dataset.ts
                                        api/index.ts    Axios 客户端
                                        types/index.ts  TS 类型定义
```

### 数据流

1. 用户上传 CSV/Excel → `POST /api/datasets/upload` → 文件保存至 `uploads/{workspace_id}/{dataset_id}/data.{ext}` → 元数据缓存至 `config.datasets_meta` 字典
2. 预览/统计信息通过 `parse_file()` 从缓存的 DataFrame 提供
3. 清洗操作（`POST /api/analysis/{id}/clean`）修改缓存的 DataFrame 并覆盖磁盘文件
4. 图表数据（`POST /api/charts/{id}/data`）执行 pandas groupby + 聚合，返回 `{categories, series}` 给 ECharts

### 关键约束

- **无测试** — 两端均未配置测试框架
- **无 Lint** — 无 ESLint、Ruff 等
- **内存元数据** — `config.datasets_meta` 和 `config.workspaces_meta` 为普通字典，服务重启后丢失；`uploads/` 中已上传的文件仍在但成为孤立文件
- **Phase 1 范围** — 单用户、无认证、无数据库；`requirements.txt` 包含 Phase 2 依赖（SQLAlchemy、pdfplumber 等）但尚未使用
- **前端代理** — Vite 开发服务器将 `/api` 代理到 `http://localhost:8000`
- **CSV 编码** — 通过 chardet 自动检测编码；分隔符从首行自动检测
