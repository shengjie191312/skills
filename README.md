# 我的 Codex Skills 仓库

这是我用来管理个人 Codex skills 的仓库。

简单说：这里不是某一个工具的项目，而是我的“AI 自动化能力库”。以后电脑重装、换电脑、误删 skill，或者想把某个好用的能力同步到 GitHub，都放在这里统一管理。

## 当前已上传的 skills

| Skill | 作用 | 适合什么时候用 |
|---|---|---|
| `wechat-sales-organizer` | 微信销售聊天记录整理工具。把 Windows 微信里的销售聊天记录、合并转发记录整理成 Excel，支持商品图、付款图、品牌、金额、销售日期等字段。 | 每月销售对账、从微信聊天记录生成销售明细、整理包包图片到 Excel、后续同步腾讯文档智能表。 |
| `product-design` | 产品设计工作流入口。从 Codex 自带 Product Design 插件备份而来，包含产品体验分析、页面审查、UI 设计、原型设计、截图/Figma/网页到代码等子能力。 | 做产品方案、页面改版、UI/UX 分析、原型设计、把截图或 Figma 做成可运行页面。 |
| `figma` | Figma MCP 使用规则。用于从 Figma 获取设计上下文、截图、变量和素材，并指导把 Figma 节点还原成项目代码。 | 有 Figma 链接、节点 ID、设计稿转代码、Figma MCP 配置或排查问题时。 |
| `ui-ux-pro-max` | UI/UX 设计增强库。包含大量风格、配色、字体、产品类型、UX 指南和图表建议，辅助做界面设计、优化和走查。 | 做网页、后台、SaaS、移动端、表单、表格、图表、导航、视觉改版、体验优化时。 |
| `pm-hub` | 产品经理统一工作台。覆盖数据分析、竞品研究、用户反馈、市场分析、会议纪要、Jira 拆解、A/B 测试、SQL、UI 走查等 PM 工作。 | 遇到指标异常、竞品分析、用户研究、需求拆解、会议纪要、数据查询和产品规划时。 |
| `prd-template` | PRD 文档模板。用于生成或完善标准产品需求文档，包含背景、目标、流程、异常、埋点、验收和 Mermaid 流程图。 | 要写 PRD、补全需求文档、检查异常流程、整理产品方案时。 |
| `prototype-demo-wizard` | 产品经理原型 Demo 向导。先生成可点击配置器，让用户选择场景、对象、风格、布局、数据和交互，再生成单文件 HTML 原型。 | 需求还比较模糊，但想快速做一个可看的产品 Demo 或交互原型。 |
| `requesting-code-review` | 代码评审请求模板。用于在完成重要功能、合并前或复杂修改后，让代码评审子任务检查风险。 | 做完代码改动、准备合并、想提前发现 bug 或回归风险时。 |
| `drawio-generator` | draw.io / diagrams.net 图表生成器。根据业务流程、系统架构、状态机等内容生成可导入、可继续编辑的 `.drawio` XML。 | 画流程图、架构图、状态机、数据流图、组织结构图。 |
| `ima-skill` | IMA OpenAPI 技能。支持笔记管理、知识库操作、文件上传到知识库、网页收藏、知识库搜索等。 | 想把资料、网页、文件、笔记放进 IMA 知识库，或从知识库里搜索内容。 |
| `find-skills` | skill 查找和安装辅助工具。帮助发现开放 skill 生态里是否有现成能力，并指导安装。 | 想问“有没有某类 skill”“能不能找一个做某事的 skill”“我想扩展 Codex 能力”。 |
| `hatch-pet` | Codex 动态宠物制作工具。根据角色设定、品牌线索、图片参考生成 Codex 可用的宠物素材包、动画精灵图和配置。 | 想做 Codex 小宠物、品牌吉祥物、动画 sprite sheet。 |
| `remotion` | Remotion 视频开发最佳实践。提供 React 视频生成、动画、Composition、渲染等相关指导。 | 写 Remotion 视频项目、做 React 动画视频、生成程序化视频。 |

## 来源说明

这份仓库现在主要同步两个来源：

- `C:\Users\乔治\.skills`：我本机正在使用的个人 skills。
- 之前已经备份到 Git 的少量额外 skills：例如 `drawio-generator`、`hatch-pet`、`ima-skill`。

以后以 `C:\Users\乔治\.skills` 为主，只要这里新增了 skill，就应该同步到本仓库和 GitHub。

## 重点 skill 说明

### `wechat-sales-organizer`

这是目前最重要、最贴合我业务的 skill。

用途：

- 从 Windows 微信聊天记录中整理销售明细
- 支持合并转发聊天记录
- 支持商品实拍图写入 Excel
- 支持付款截图、品牌、金额、销售日期识别
- 支持一张图片里多个商品时拆成多条记录
- 默认销售渠道写“包展”

稳定使用方式：

1. 把真实销售聊天记录合并转发给自己的微信小号。
2. 告诉 Codex 这条记录的大概时间，例如“7月6日下午五点半左右”。
3. 让 Codex 使用 `wechat-sales-organizer` 整理成 Excel。

当前稳定方案不是让程序乱点微信窗口，也不是截图裁切，而是优先从本机微信数据库和图片缓存中找源记录、源图片，再生成 Excel。

### `product-design`

这是从 Codex 自带 Product Design 插件备份出来的一整套产品设计能力。

它不是单个文件，而是一组子 skill：

- `get-context`：先澄清产品背景和设计目标
- `ideate`：生成视觉方向和设计方案
- `prototype`：做可运行原型
- `image-to-code`：根据截图、视觉稿、Figma 等还原页面
- `url-to-code`：根据网页做本地原型
- `audit`：做产品体验或页面审查
- `design-qa`：对原型做设计还原检查
- `share`：分享或部署原型
- `user-context`：保存产品设计偏好和上下文

以后要做产品设计、页面改版、原型 Demo，可以优先用这个。

## 每个目录怎么看

每个 skill 目录里通常会有：

```text
SKILL.md
```

这个文件就是给 Codex 看的说明书，里面写了：

- 这个 skill 是干什么的
- 什么时候应该使用
- 需要调用哪些脚本
- 有哪些边界和注意事项

如果目录里还有：

```text
scripts/
templates/
references/
assets/
```

一般含义是：

- `scripts/`：配套脚本
- `templates/`：模板文件
- `references/`：补充规则或参考文档
- `assets/`：图片、图标等资源

## 如何安装到本机

本机个人 skills 目录是：

```text
C:\Users\乔治\.skills
```

把某个 skill 目录放到这里，Codex 就可以在后续会话里识别和使用。

比如：

```text
C:\Users\乔治\.skills\wechat-sales-organizer
C:\Users\乔治\.skills\product-design
```

## 如何更新这个仓库

如果本机 skill 改了，可以让 Codex 帮我同步，也可以手动执行：

```powershell
git status
git add .
git commit -m "update skills"
git push
```

我不需要自己记这些命令。以后直接跟 Codex 说“把我的 skills 更新到 GitHub”，让 Codex 做即可。

## 不要上传的东西

为了安全，下面这些东西不要放进这个仓库：

- API Key
- token
- 账号密码
- 微信数据库原始文件
- 客户隐私数据
- 临时输出 Excel
- 图片缓存
- 解密过程文件
- 本地运行日志

这个仓库的 `.gitignore` 已经尽量排除这些内容，但每次上传前仍建议让 Codex 做一次敏感信息检查。

## 当前仓库定位

这个仓库的目标不是写代码给别人用，而是方便我长期管理自己的 AI 自动化能力。

重点标准：

- 我自己能看懂
- 换电脑能恢复
- 好用的 skill 能沉淀
- 不上传隐私和密钥
- 每个 skill 都能说清楚“解决什么问题”
