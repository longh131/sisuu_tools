# 09-SEO规范.md

# SEO Specification

Version：V1.0

---

# 一、SEO目标

整个网站围绕 Google SEO 开发。

所有页面必须符合 Google 官方最佳实践。

SEO 优先级高于页面效果。

---

# 二、URL

统一：

```text
/tools/amazon-fee-calculator
/tools/fba-profit-calculator
/blog/how-to-calculate-fba-fees
```

禁止：

```text
?id=1
&page=2
```

---

# 三、Title

每个页面唯一。

长度：

50~60字符。

必须包含核心关键词。

---

# 四、Description

每个页面唯一。

长度：

120~160字符。

自然描述。

禁止关键词堆积。

---

# 五、H标签

每页：

仅一个 H1。

合理使用：

H2

H3

H4

不得跳级。

---

# 六、图片SEO

所有图片：

alt

title

width

height

lazy loading

全部必须。

---

# 七、内部链接

每个工具页面：

推荐：

4~6个相关工具。

每篇文章：

推荐：

3~5篇相关文章。

形成完整内链。

---

# 八、Schema

首页：

Organization

Website

SearchAction

工具：

SoftwareApplication

FAQPage

BreadcrumbList

文章：

Article

全部自动生成。

---

# 九、robots

必须允许：

Google

Bing

禁止：

后台

缓存

临时目录

日志目录

---

# 十、Sitemap

自动生成：

sitemap.xml

包含：

首页

工具

分类

文章

静态页面

提交：

Google Search Console。

---

# 十一、Canonical

所有页面：

必须唯一。

防止重复收录。

---

# 十二、Open Graph

自动生成：

title

description

image

url

type

支持：

Facebook

LinkedIn

X

---

# 十三、PageSpeed

目标：

Performance ≥90

SEO ≥95

Accessibility ≥90

Best Practices ≥90

---

# 十四、Core Web Vitals

LCP ≤2秒

CLS ≤0.1

INP ≤200ms

全部达标。

---

# 十五、文章规范

每篇：

1200+

英文单词。

原创。

解决问题。

禁止 AI 灌水。

所有文章必须链接工具页面。

---

# 十六、工具规范

每个工具：

独立URL

独立SEO

独立FAQ

独立Schema

独立Title

形成独立Google入口。

---

# 十七、收录

上线完成：

robots

sitemap

Google Search Console

Bing Webmaster

全部提交。

---

# 十八、SEO原则

以后所有开发：

必须优先考虑：

Google收录

Google排名

Google速度

Google体验

SEO 不得因任何功能受到影响。
