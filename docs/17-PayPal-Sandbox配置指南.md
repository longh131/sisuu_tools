# 17-PayPal-Sandbox配置指南.md

# PayPal Sandbox 逐步配置指南（截图式说明）

Version：V1.1  
站点：https://sisuu.com/  
代码路径：`/opt/sisuu_tools`（生产）  
预计耗时：**1~2 小时**（首次）

> 本文按「你打开页面 → 看到什么 → 点哪里 → 复制什么」编写，相当于逐步截图说明。  
> 支付宝按约定 **未来再加**，本文不涉及。

---

# 零、先搞清楚：Sandbox  vs  Live

| 模式 | 含义 | 能否收真钱 |
|------|------|------------|
| **Sandbox** | 测试环境，假账户假钱 | ❌ 不能 |
| **Live** | 正式环境 | ✅ 可以 |

**流程：** 先在 Sandbox 跑通全流程 → 再切 Live → 才算「支付正式运营」。

---

# 一、注册与登录 Developer

## 步骤 1.1 打开 Developer 控制台

1. 浏览器访问：**https://developer.paypal.com/**
2. 右上角点击 **Log in to Dashboard**
3. 用你的 **PayPal 个人账户或商业账户** 登录（没有就先注册 PayPal）

## 步骤 1.2 进入 Dashboard

登录后你会看到：

```text
┌─────────────────────────────────────────────┐
│  PayPal Developer    [Sandbox ▼]  [Live ▼]  │
├─────────────────────────────────────────────┤
│  My Apps & Credentials                      │
│  Testing Tools → Sandbox accounts           │
│  ...                                        │
└─────────────────────────────────────────────┘
```

**关键：** 左上角或顶部确保选的是 **Sandbox**（测试），不是 Live。

---

# 二、准备 Sandbox 测试账户

## 步骤 2.1 查看沙盒账户

1. 左侧菜单：**Testing Tools** → **Sandbox Accounts**
2. 页面会列出 PayPal 自动创建的测试账户，例如：

```text
┌──────────────────┬─────────────────────────────┬──────────┐
│ Type             │ Email                       │ Password │
├──────────────────┼─────────────────────────────┼──────────┤
│ Business         │ sb-business-xxxxx@...       │ ******** │  ← 商家（收款方）
│ Personal         │ sb-buyer-xxxxx@...          │ ******** │  ← 买家（付款测试用）
└──────────────────┴─────────────────────────────┴──────────┘
```

3. 点击 Business 账户右侧 **⋯** → **View/Edit Account**
4. **记下：**
   - Business 邮箱（代表你的「商户」）
   - Password（点击 Show 可见，或 Reset password）

> 测试付款时，用 **Personal（买家）** 账户登录 PayPal 确认订阅。

---

# 三、创建 REST API 应用（拿 Client ID / Secret）

## 步骤 3.1 进入 Apps

1. 左侧：**Apps & Credentials**（或 Dashboard 首页 **My Apps & Credentials**）
2. 确认顶部 Tab 为 **Sandbox**（不是 Live）

## 步骤 3.2 创建 App

1. 点击 **Create App**（蓝色按钮）
2. 填写：

| 字段 | 填什么 |
|------|--------|
| App Name | `Seller Toolkit` 或 `sisuu-tools` |
| App Type | 选 **Merchant**（商户） |

3. 点击 **Create App**

## 步骤 3.3 复制密钥

创建成功后页面类似：

```text
┌─────────────────────────────────────────────┐
│  App: Seller Toolkit                        │
│  Client ID:  Axxxxxxxxxxxxxxxxxxxxxxxxxxx   │  ← 复制
│  Secret:     [Show] ●●●●●●●●●●●●●●●●●●●●   │  ← 点 Show 后复制
└─────────────────────────────────────────────┘
```

**保存到记事本：**

```env
PAYPAL_CLIENT_ID=粘贴ClientID
PAYPAL_CLIENT_SECRET=粘贴Secret
PAYPAL_MODE=sandbox
```

⚠️ Secret 只显示一次，务必立刻保存。

---

# 四、创建订阅 Plan（Pro $19 / Business $49）

PayPal 订阅需要先建 **Product（产品）**，再建 **Plan（计划）**。

## 步骤 4.1 打开订阅管理

**方式 A（推荐，界面直观）：**

1. 登录 **https://www.sandbox.paypal.com/**（Sandbox 商家账户）
2. 进入 **Pay & Get Paid** → **Subscriptions** → **Plans**

**方式 B（Developer API 文档侧）：**

1. Developer Dashboard → **Sandbox** → 使用 API 或 PayPal 商户后台创建

> PayPal 界面会更新，若菜单名略有不同，找 **Subscriptions / Plans / Billing Plans** 即可。

## 步骤 4.2 创建 Pro 计划（$19/月）

1. 点击 **Create Plan** 或 **Create Subscription Plan**
2. 按向导填写：

| 步骤 | 填写内容 |
|------|----------|
| Product name | `Seller Toolkit Pro` |
| Product description | `Pro plan - 100 AI uses per day` |
| Billing cycle | **Monthly（每月）** |
| Price | **19.00 USD** |
| Setup fee | 0（无） |
| Auto-renew | Yes（自动续费） |

3. 保存后得到 **Plan ID**，格式类似：

```text
P-5ML427124445436WXNWU5NQ
```

4. 复制到：

```env
PAYPAL_PLAN_PRO=P-xxxxxxxx
```

## 步骤 4.3 创建 Business 计划（$49/月）

重复步骤 4.2：

| 字段 | 值 |
|------|-----|
| Product name | `Seller Toolkit Business` |
| Price | **49.00 USD** |
| Billing cycle | Monthly |

得到第二个 Plan ID：

```env
PAYPAL_PLAN_BUSINESS=P-yyyyyyyy
```

## 步骤 4.4 核对

最终应有 **2 个 Plan ID**，分别对应 Pro 和 Business，不要搞反。

---

# 五、配置 Webhook（订阅激活 / 取消通知）

Webhook 让 PayPal 在用户付款成功后 **自动** 把用户 tier 升级为 pro/business。

## 步骤 5.1 创建 Webhook

1. Developer Dashboard → **Apps & Credentials** → 点进你刚建的 App
2. 向下滚动到 **Webhooks** 区域
3. 点击 **Add Webhook**

## 步骤 5.2 填写 Webhook URL

| 字段 | 值 |
|------|-----|
| Webhook URL | `https://sisuu.com/api/billing/webhook` |
| Event types | 勾选下面两个 |

**必勾选事件：**

- `BILLING.SUBSCRIPTION.ACTIVATED` — 订阅生效 → 升级 tier
- `BILLING.SUBSCRIPTION.CANCELLED` — 订阅取消 → 降级 tier

4. 点击 **Save**

## 步骤 5.3 复制 Webhook ID

保存后列表里会显示：

```text
Webhook ID:  8XXXXXXXYyyyyyyyyyyyy
URL:         https://sisuu.com/api/billing/webhook
```

复制 Webhook ID：

```env
PAYPAL_WEBHOOK_ID=8XXXXXXXYyyyyyyyyyyyy
```

---

# 六、服务器配置 `.env`

## 步骤 6.1 SSH 登录服务器

```bash
ssh your-user@your-server
cd /opt/sisuu_tools
nano .env    # 或 vim .env
```

## 步骤 6.2 追加 / 修改以下项

```env
# 支付 — Sandbox 测试阶段
PAYMENT_PROVIDER=paypal
PAYPAL_CLIENT_ID=你的Sandbox_ClientID
PAYPAL_CLIENT_SECRET=你的Sandbox_Secret
PAYPAL_MODE=sandbox
PAYPAL_PLAN_PRO=P-你的Pro计划ID
PAYPAL_PLAN_BUSINESS=P-你的Business计划ID
PAYPAL_WEBHOOK_ID=你的WebhookID
```

## 步骤 6.3 部署 V1.1 代码并重启

若服务器还是 V1.0 代码，需先拉 V1.1：

```bash
git pull
pip install -r requirements.txt
alembic upgrade head
python scripts/seed_db.py          # 仅数据库为空时执行
docker compose -f docker-compose.prod.yml up -d --build
```

---

# 七、Sandbox 端到端测试（必做）

按顺序测，全部通过再考虑 Live。

## 测试 1：后台显示支付已启用

1. 打开 **https://sisuu.com/admin/**
2. 进入 **支付 / 订阅**
3. 顶部应显示：`当前支付：paypal — 已配置，Pricing 页可真实付款`（绿色）

若仍是黄色「未配置」，检查 `.env` 是否填全、是否重启 Docker。

## 测试 2：注册并登录前台账户

1. 打开 **https://sisuu.com/register**
2. 注册测试邮箱 + 密码（≥8 位）
3. 登录后导航栏应出现 **Account**

## 测试 3：Pricing 页发起订阅

1. 打开 **https://sisuu.com/pricing**
2. Pro 卡片应 **没有**「Coming Soon」，按钮为 **Upgrade Now**
3. 点击 Upgrade → 应跳转到 **PayPal Sandbox** 登录/确认页（域名含 `sandbox.paypal.com`）

## 测试 4：Sandbox 买家付款

1. 在 PayPal 页用 **步骤 2.1 的 Personal（买家）** 账户登录
2. 同意订阅 → 完成
3. 应跳回 **https://sisuu.com/billing/success**

## 测试 5：验证 tier 升级

**方式 A — Webhook 自动（推荐）**

1. 等 10~30 秒
2. 打开 **https://sisuu.com/account**
3. Plan 应显示 **Pro**（或 Business）
4. 后台 **/admin/users** → 该用户 tier 应为 pro

**方式 B — Webhook 未及时触发**

1. 后台 **/admin/users** → 编辑用户 → 手动改 tier（仅测试兜底）
2. 检查 PayPal Developer → Webhooks → 该 URL 的 **Event logs** 是否有失败

## 测试 6：后台流水

1. **/admin/payments** → 应有一条 pending/completed 记录
2. 订阅列表有对应 plan_id

---

# 八、从 Sandbox 切换到 Live（收真钱）

Sandbox 测通后，**重复第三~六步**，但全部在 **Live** 环境下操作：

| 项目 | Sandbox | Live |
|------|---------|------|
| Developer Tab | Sandbox | **Live** |
| Client ID / Secret | Sandbox 密钥 | **Live 密钥** |
| Plan ID | Sandbox Plan | **Live Plan（重新创建）** |
| Webhook | Sandbox Webhook | **Live Webhook（同 URL）** |
| `.env` | `PAYPAL_MODE=sandbox` | **`PAYPAL_MODE=live`** |

⚠️ Live 需要 **PayPal 商业账户** 完成审核，且 Plan 要在 Live 商户后台创建。

---

# 九、配置好 PayPal 后，网站能正式运营吗？

## 简短回答

| 阶段 | 状态 |
|------|------|
| **现在（V1.0 已上线）** | ✅ 已经在运营（工具、SEO、Email 收集） |
| **PayPal Sandbox 配好** | ✅ 支付流程可测通，但 **不收真钱** |
| **PayPal Live + 下面清单** | ✅ 可 **正式商业化运营**（真钱订阅） |

**所以：** Sandbox 配好 = 支付链路验证完成，还不是「正式收款运营」；切 Live 并做完运营清单 = 完整正式运营。

---

## 正式商业化运营清单

在 PayPal Live 之外，建议确认：

### 必须（安全 / 稳定）

- [ ] 生产 `DEBUG=false`
- [ ] `SECRET_KEY`、`ADMIN_PASSWORD` 已改强密码
- [ ] V1.1 代码已部署（用户系统、PayPal、后台 CRUD）
- [ ] `alembic upgrade head` 已执行
- [ ] PayPal **Live** 模式 + Live Plan + Live Webhook
- [ ] 走通一次 **Live 小额真实订阅**（可先订 Pro 再取消）

### 强烈建议（运营数据）

- [ ] `GA_MEASUREMENT_ID` 已配置（看流量）
- [ ] Google Search Console sitemap 正常（你已完成）
- [ ] Bing Webmaster 提交 sitemap（可选）
- [ ] 数据库备份 cron 已配置

### 可后续迭代

- [ ] 支付宝（国内流量上来再加）
- [ ] 发票 / 税务说明页（跨境 SaaS 视地区而定）
- [ ] 用户自助取消订阅入口（目前依赖 PayPal 账户管理 + Webhook 降级）

---

# 十、常见问题

## Q1：Pricing 仍显示 Coming Soon？

- 检查 `PAYMENT_PROVIDER=paypal`
- 五个 PayPal 变量是否都有值
- Docker 是否重启
- 后台 `/admin/payments` 是否显示「已配置」

## Q2：点 Upgrade 提示请先登录？

- 设计如此：订阅必须绑定注册用户
- 先 `/register` 再回 Pricing

## Q3：付款成功但 tier 没变？

1. 查 PayPal Webhook Event logs 是否 4xx/5xx
2. 确认 Webhook URL 是 `https://sisuu.com/api/billing/webhook`（HTTPS）
3. 临时：后台 `/admin/users` 手动改 tier

## Q4：Sandbox 和 Live 的 Plan ID 能混用吗？

**不能。** Sandbox Plan 只能用于 `PAYPAL_MODE=sandbox`，Live 必须重新创建 Plan。

## Q5：没有 PayPal 商业账户可以先测吗？

可以。Developer 注册后自带 Sandbox Business 账户，足够完成 Sandbox 全流程测试。

---

# 十一、配置项速查表

```env
PAYMENT_PROVIDER=paypal
PAYPAL_CLIENT_ID=
PAYPAL_CLIENT_SECRET=
PAYPAL_MODE=sandbox          # 正式收款改 live
PAYPAL_PLAN_PRO=
PAYPAL_PLAN_BUSINESS=
PAYPAL_WEBHOOK_ID=
```

| 变量 | 从哪里复制 |
|------|------------|
| CLIENT_ID / SECRET | Developer → Apps → 你的 App |
| PLAN_PRO / PLAN_BUSINESS | Sandbox 商户后台 → Subscriptions → Plans |
| WEBHOOK_ID | Developer → App → Webhooks |
| Webhook URL | 固定 `https://sisuu.com/api/billing/webhook` |

---

# 十二、相关文档

- 支付方案总览：`docs/15-支付方案.md`
- 运营配置（GA4/Bing/安全）：`docs/16-运营配置指南.md`
- V1.1 开发计划：`docs/14-V1.1开发计划.md`

---

*Sandbox 测通 → Live 上线 → 清单打勾 = Seller Toolkit 正式商业化运营。*
