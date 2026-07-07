# Codex Skills 备份仓库

这是我本机 Codex skills 的备份仓库，主要用来保存自己常用的自动化能力。

你可以把它理解成：

- `wechat-sales-organizer`：微信销售聊天记录整理工具
- 其他目录：一些已经安装过的 Codex skill 备份
- 这个 GitHub 仓库：防止电脑重装、误删、换电脑时找不回来

## 导出范围

- 已排除 `.system` 内置系统 skills。
- 已将原本的软链接 skills 复制成真实目录，方便备份和迁移。
- 已排除运行缓存、输出目录、Python 缓存、本地环境文件和明显敏感配置。

## 当前包含的 skill

- `wechat-sales-organizer`
- `drawio-generator`
- `find-skills`
- `hatch-pet`
- `ima-skill`
- `prototype-demo-wizard`
- `remotion`

## 重点：微信销售整理 skill

路径：

```text
wechat-sales-organizer/
```

用途：

- 从 Windows 微信聊天记录里整理销售明细
- 支持合并转发聊天记录
- 支持商品图写入 Excel
- 支持金额识别、品牌识别、销售日期提取
- 支持一张图多个商品时拆成多条记录
- 默认销售渠道写“包展”

稳定使用方式：

1. 先把真实销售聊天记录合并转发给自己的微信小号。
2. 电脑微信打开和小号的聊天窗口。
3. 在 Codex 里说：使用 `wechat-sales-organizer`，整理某天某个时间附近的聊天记录，输出 Excel。
4. 生成的 Excel 会保存到指定目录。

目前最稳定的思路不是让程序乱点微信窗口，而是从本机微信聊天数据和图片缓存里找源文件，再生成 Excel。这样比截图裁切稳定。

## 每个目录怎么看

每个 skill 目录里通常会有一个：

```text
SKILL.md
```

这个文件就是给 Codex 看的说明书，里面写了这个 skill 什么时候用、怎么用、有哪些脚本和注意事项。

如果目录里有：

```text
scripts/
```

一般表示这个 skill 有配套脚本，Codex 会优先运行这些脚本，不需要你手动打开。

## 后续怎么更新这个仓库

如果本机 skill 改了，可以重新同步后提交：

```powershell
git status
git add .
git commit -m "update skills"
git push
```

如果你不懂这些命令，直接让 Codex 帮你做就行。

## 不要上传的东西

为了安全，下面这些东西不要提交到 GitHub：

- API Key
- token
- 账号密码
- 微信数据库原始文件
- 真实客户隐私数据
- 临时输出 Excel
- 图片缓存和解密过程文件

本仓库已经尽量通过 `.gitignore` 排除了这些内容，但每次推送前仍建议做一次敏感信息检查。
