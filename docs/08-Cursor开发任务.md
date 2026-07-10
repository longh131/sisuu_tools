# 07-Cursor开发任务.md

# Cursor Master Development Task

## 项目目标

根据 docs 目录下所有文档，从零开始开发 **Seller Toolkit**。

这是一个面向全球跨境电商卖家的英文工具平台。

目标：

* 可直接上线
* 可长期维护
* SEO 优先
* FastAPI 服务端渲染（SSR）
* 后续可扩展到 100+ 工具

开发过程中必须严格遵守 docs 目录全部规范。

---

# 开发要求

必须严格按照以下要求：

* 不允许修改项目架构
* 不允许修改目录结构
* 不允许修改 UI 风格
* 不允许更换技术栈
* 不允许删除已有功能
* 不允许使用复杂框架
* 所有代码必须模块化
* 所有页面必须响应式
* 所有工具必须复用统一模板

任何新增代码都必须符合开发规范。

---

# 技术要求

后端：

* FastAPI
* Jinja2
* Uvicorn

前端：

* HTML5
* Bootstrap 5
* 原生 JavaScript

数据库：

* MySQL 初始化

* Alembic 数据库迁移

AI：

* DeepSeek API

部署：

* Docker
* Docker Compose
* Nginx

配置：

* `.env`

---

# 第一阶段开发内容（MVP）

必须完成：

## 首页

包含：

* Hero
* 搜索框
* Popular Tools
* Tool Categories
* Latest Tools
* FAQ
* Footer

---

## 工具分类

建立：

* AI Tools
* Calculators
* Policy Center
* Seller Resources

---

## 六个工具

AI：

* Negative Review Reply Generator
* Product Description Generator

Calculator：

* Amazon Fee Calculator
* FBA Profit Calculator
* VAT Calculator
* Shipping Calculator

所有工具必须使用统一模板。

---

## 基础页面

* About
* Contact
* Privacy Policy
* Terms of Service
* 404

---

# SEO

自动生成：

* Title
* Description
* Canonical
* Open Graph
* robots.txt
* sitemap.xml
* FAQ Schema
* Breadcrumb Schema

所有页面必须符合 Google SEO 最佳实践。

---

# UI

必须遵循 docs 中 UI 规范。

整体风格参考国际 SaaS 产品：

* 简洁
* 留白
* 专业
* 响应式

禁止复杂动画。

---

# 性能

要求：

* Lighthouse Performance ≥90
* Lighthouse SEO ≥95
* 首页加载 ≤2 秒

图片全部压缩。

CSS、JS 最小化。

---

# 安全

所有 API Key 从 `.env` 读取。

所有输入必须验证。

禁止硬编码。

错误信息不得暴露服务器信息。

---

# 输出要求

一次性生成完整项目，包括：

* 项目目录
* 所有源代码
* Dockerfile
* docker-compose.yml
* requirements.txt
* README.md
* nginx 配置
* MySQL 8 初始化
* 基础数据
* 所有 HTML 模板
* CSS
* JavaScript

项目生成完成后：

自动检查：

* 是否可运行
* 是否可构建 Docker
* 是否存在语法错误
* 是否存在缺失依赖

修复全部错误后再结束。

---

# 最终目标

交付一个可以直接执行以下命令运行的完整项目：

```bash
docker compose up -d --build
```

启动成功后，可直接通过域名访问首页。

整个项目代码必须达到可维护、可扩展、可上线的标准，为后续持续增加工具和 SEO 内容打下稳定基础。
