# GoCooking 3

这是一个面向烹饪新手的厨房应用，主要功能包括记录菜品的原材料、切配时间、烹饪方法等。

## 技术架构

- 后端: Python + FastAPI
- 前端: Vue 3 + Element Plus
- 数据库: PostgreSQL
- 部署: 前后端分别部署

## 项目结构

```
backend/
├── main.py             # FastAPI应用入口
├── models.py           # 数据库模型
├── schemas.py          # Pydantic数据模型
├── crud.py             # 数据库操作函数
├── database.py         # 数据库配置
├── routes/             # API路由
│   └── dish_routes.py
├── alembic/            # 数据库迁移
├── init_db.py          # 数据库初始化脚本
└── requirements.txt    # Python依赖

frontend/
├── src/
│   ├── main.js         # Vue应用入口
│   ├── App.vue         # 根组件
│   ├── router/         # 路由配置
│   ├── views/          # 页面组件
│   │   ├── Home.vue
│   │   └── DishDetail.vue
│   └── utils/
│       └── api.js      # API工具
├── package.json        # 前端依赖
├── vite.config.js      # Vite配置
└── index.html          # HTML模板
```

## 快速开始（后端）

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置数据库连接
   - 复制 `.env.example` 文件为 `.env`
   - 修改 `.env` 文件中的数据库连接配置
   - 默认连接字符串: `postgresql://username:password@localhost:5432/gocooking3`
   - 需要确保 PostgreSQL 数据库服务已启动

3. 初始化数据库：
```bash
python backend/init_db.py
```

或者使用Alembic迁移：
```bash
alembic upgrade head
```

4. 启动应用：
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## SQLModel 集成说明

本项目已成功集成 SQLModel，它结合了 SQLAlchemy 的强大 ORM 功能和 Pydantic 的数据验证能力：

- 模型定义使用 SQLModel 基类，支持 SQL 操作和数据验证
- 所有数据库操作通过 SQLModel 兼容的查询方式进行
- 模型间的关系通过 SQLModel 的 Relationship 进行定义
- 使用 SQLModel 的 create_engine 和 metadata 进行数据库初始化

## 自动表创建说明

本项目已实现基于实体关系的自动表创建功能：

- 所有模型类继承自 SQLModel 并设置 `table=True`
- 数据库初始化时使用 `SQLModel.metadata.create_all(engine)` 自动创建所有相关表
- 实体间的关系（一对多、多对多）会自动创建相应的外键和关联表
- 包括：dish 表、ingredient 表、dish_step 表和关联表 dish_ingredients
- 通过运行 `python backend/init_db.py` 即可自动创建所有必要的数据库表

## 环境变量配置

本项目支持通过环境变量配置数据库连接：

- 创建 `.env` 文件来存储数据库配置
- 使用 `DATABASE_URL` 环境变量指定数据库连接字符串
- 系统会自动从 `.env` 文件加载环境变量
- 参考 `.env.example` 文件了解配置格式
- 更多详细配置信息请查看 `docs/database_configuration.md`

## Mock 数据生成

本项目包含一个强大的 Mock 数据生成器，用于测试和开发：

- 位于 `backend/mock_data_generator.py`
- 可以生成完整的菜品数据（包括名称、难度等级）
- 自动生成相关食材和烹饪步骤
- 支持批量生成多个菜品数据
- 所有数据都会被正确插入到数据库中
- 通过运行 `python backend/mock_data_generator.py` 来生成单个菜品
- 通过运行 `python test_mock_generator.py` 来测试生成多个菜品

## 数据库列映射修复

已修复 "Could not locate column in row for column" 错误：

- 通过在模型定义中明确指定 SQL 列映射
- 确保所有字段（如 difficult、type 等）都有正确的数据库列映射
- 使用适当的 SQLModel 查询方法
- 通过测试验证列映射的正确性

## 快速开始（前端）

1. 安装依赖：
```bash
cd frontend
npm install
```

2. 启动开发服务器：
```bash
npm run dev
```

## API接口

### 菜品相关

#### 查询菜品（分页）
- 接口：`POST /cooking/ver3/dish/select`
- 入参：
```json
{
  "page": 0,
  "size": 10,
  "dishName": ""
}
```
- 出参：
```json
{
  "code": 0,
  "data": [
    {
      "id": 1,
      "dish_name": "菜品名",
      "difficult": 1,
      "tags": ["简单"]
    }
  ]
}
```

#### 菜品详情
- 接口：`GET /cooking/ver3/dish/detail/{id}`
- 出参：
```json
{
  "code": 0,
  "data": {
    "id": 1,
    "dish_name": "菜品名",
    "difficult": 1,
    "ingredients": [...],
    "steps": [...],
    "create_time": "...",
    "modify_time": "..."
  }
}
```

## 数据库表结构

### dish（菜品表）
- id: 主键
- dish_name: 菜品名称 (text, 默认 "")
- difficult: 难度 (smallint, 1简单 2中等 3复杂, 默认 1)
- create_time: 创建时间 (timestamp, 默认当前时间)
- modify_time: 修改时间 (timestamp, 默认当前时间，随修改更新)

### ingredient（食材表）
- id: 主键
- ingredient_name: 食材名称 (text, 默认 "")
- type: 类型 (smallint, 1辅料 2配料, 默认 1)
- create_time: 创建时间 (timestamp, 默认当前时间)
- modify_time: 修改时间 (timestamp, 默认当前时间，随修改更新)

### dish_step（菜品步骤表）
- id: 主键
- dish_id: 菜品ID (外键)
- step_order: 步骤顺序 (int, 默认 0)
- step_text: 步骤内容 (text, 默认 "")
- create_time: 创建时间 (timestamp, 默认当前时间)
- modify_time: 修改时间 (timestamp, 默认当前时间，随修改更新)

### dish_ingredients（菜品食材关联表）
- dish_id: 菜品ID (外键)
- ingredient_id: 食材ID (外键)