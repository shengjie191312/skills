---
name: wechat-sales-organizer
description: 从 Windows 微信当前打开的聊天窗口或合并转发聊天记录中整理销售明细。用于用户要求运行微信销售整理、从聊天记录生成 Excel、提取包包图片/付款截图/品牌/金额/销售日期、同步腾讯文档智能表，或处理每月微信销售对账自动化时。
---

# 微信销售整理

## 目标

把用户已合并转发到自己小号的微信聊天记录，整理成销售明细 Excel。优先从本机微信数据库定位合并转发记录，并从微信本地原图缓存解密图片；不要把控制微信窗口点击、截图裁切作为主流程。

## 用户前置动作

让用户完成这一步即可：

1. 把当月销售相关聊天记录合并转发给自己的小号。
2. 告诉 Codex 这条合并记录的大概时间，例如“7月6日下午五点半左右”。
3. 如需要辅助确认，再打开 Windows 微信停在这条聊天附近，但正式处理优先走本地数据库和缓存。

不要要求用户手动导出聊天记录、整理图片、复制命令或打开脚本。

## 默认业务规则

- 只有商品图、没有付款截图：算一条销售记录。
- 一张图里有多个明确商品：按商品数量拆成多条销售记录，同一张原图可重复嵌入多行，备注标明商品位置。
- 商品图和付款图：按时间相邻合并，第一版以候选订单草稿为主。
- 销售渠道：默认“包展”。
- 输出字段：序号、商品名称、金额、销售日期、销售渠道、买家姓名/微信、付款截图、包包图片、备注、退货。
- 手写金额常用推测：70=7000，68=6800，13=1300，1.3=1300，1w=10000。
- 不确定信息写入备注，不要编造。

## 核心脚本

当前稳定脚本位于工作目录：

- `C:\Users\乔治\Desktop\聊天记录整理\codex\tools\run_wda_decrypt_core.py`
- `C:\Users\乔治\Desktop\聊天记录整理\codex\tools\list_forwarded_records_by_time.py`
- `C:\Users\乔治\Desktop\聊天记录整理\codex\tools\extract_forward_record_items.py`
- `C:\Users\乔治\Desktop\聊天记录整理\codex\tools\generate_forward_sales_excel.py`

早期窗口采集脚本位于本技能目录：

`scripts/wechat_sales_automation.py`

配置模板：

- `scripts/config.example.json`：默认不启用 AI。
- `scripts/config.local.example.json`：启用 AI 的模板。

运行时优先使用 Codex 内置 Python：

`C:\Users\乔治\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`

如果该路径不存在，调用 `codex_app.load_workspace_dependencies` 获取 Python 路径。

## 推荐工作流

1. 优先解密本机微信数据库：

```powershell
& "<python>" "C:\Users\乔治\Desktop\聊天记录整理\codex\tools\run_wda_decrypt_core.py"
```

2. 按用户给的时间窗口查找合并转发记录。必要时修改脚本里的 `START` / `END`，输出候选后选择目标记录：

```powershell
& "<python>" "C:\Users\乔治\Desktop\聊天记录整理\codex\tools\list_forwarded_records_by_time.py"
```

3. 解析目标合并记录里的源消息，生成 `source_rows.json`：

```powershell
& "<python>" "C:\Users\乔治\Desktop\聊天记录整理\codex\tools\extract_forward_record_items.py"
```

4. 从 `Rec` 原图缓存优先找图、解密图片、生成 Excel 并自检：

```powershell
& "<python>" "C:\Users\乔治\Desktop\聊天记录整理\codex\tools\generate_forward_sales_excel.py" --source-rows "<source_rows.json>" --tag "<时间标签>"
```

如果一张图里有多个商品，源记录或 AI 识别结果可写入 `line_items`。程序会按 `line_items` 拆成多行，并重复嵌入同一张原图：

```json
{
  "line_items": [
    {"brand": "dior", "amount": 3500, "position": "上方紫色包"},
    {"brand": "dior", "amount": 6300, "position": "中间粉色包"},
    {"brand": "dior", "amount": 6300, "position": "下方粉色包"}
  ]
}
```

5. 如果本地数据库和缓存路径都失败，再做窗口预检。预检只截图和输出窗口信息，不滚动、不点击；如果当前窗口不是 `Weixin.exe` 的 Windows 微信窗口，必须停止：

```powershell
& "<python>" "<skill_dir>\scripts\wechat_sales_automation.py" inspect-window
```

6. 预检截图确实是目标聊天记录后，再小规模测试 2 屏：

```powershell
& "<python>" "<skill_dir>\scripts\wechat_sales_automation.py" capture-original --max-screens 2
```

7. 如果窗口预检失败，或者微信 UI 采集不稳定，先走本地缓存备用方案。它会从本机微信文件目录扫描图片候选并生成 Excel 草稿，不读取加密聊天正文：

```powershell
& "<python>" "<skill_dir>\scripts\wechat_sales_automation.py" scan-local --since 2026-07 --limit 300
```

8. 如果用户提供 API Key 或当前环境有 `OPENAI_API_KEY`，用启用 AI 的配置：

```powershell
$env:OPENAI_API_KEY="<只在当前命令临时设置，不写入文件>"
& "<python>" "<skill_dir>\scripts\wechat_sales_automation.py" capture-original --config "<skill_dir>\scripts\config.local.example.json" --max-screens 2
```

9. 检查输出日志里的：

- `微信复制图片`
- `订单草稿`
- `Excel`

10. 测试正常后再正式跑 40 屏：

```powershell
& "<python>" "<skill_dir>\scripts\wechat_sales_automation.py" capture-original --config "<config>" --max-screens 40
```

## 输出位置

脚本从当前工作目录生成：

- `runs/<时间>/wechat_images/`：从微信图片查看器右键复制得到的原图。
- `runs/<时间>/local_images/`：从本地微信缓存复制或解密得到的图片候选。
- `runs/<时间>/orders.json`：订单草稿。
- `outputs/销售明细_<时间>.xlsx`：本地 Excel。
- `outputs/wechat_<时间>_images_contact_sheet.jpg`：图片总览。
- `outputs/wechat_<时间>_manifest.json`：源记录、图片路径、备注和自检依据。

最终回复用户时，直接给 Excel 的绝对路径链接，并用简短中文说明采集数量、订单数量、是否启用 AI。

## Key 和隐私规则

- 不要把用户给的 API Key 写进脚本、配置、README 或技能文件。
- 只在当前 shell 命令里临时设置 `$env:OPENAI_API_KEY`。
- 不要在回复中回显完整 Key。
- 如果 Key 已经出现在聊天里，提醒用户后续轮换正式 Key。

## 腾讯文档同步

脚本已预留 `sync-tencent`，但除非已有可用的 `upload_image` / `add_records` 接口参数，否则先不要声称腾讯文档同步已完成。

需要补充的信息：

- `upload_image` 调用地址、鉴权方式、返回字段。
- `add_records` 调用地址、鉴权方式。
- 智能表字段 ID 映射。
- 表格 ID、视图 ID 或 sheet URL。

## 故障处理

- 找不到或拿错窗口：不要继续点击。先让用户点一下真正的 Windows 微信聊天窗口，再跑 `inspect-window`。脚本现在会拒绝操作 Chrome、Codex、文件资源管理器等非 `Weixin.exe` 窗口。
- `微信复制图片：0`：微信图片查看器复制路径可能失效，先用 2 屏测试并保留定位截图排查。
- UI 采集走不通：改跑 `scan-local`，先生成本地缓存候选 Excel；后续再接数据库解密/消息时间还原。
- AI 报缺少 Key：关闭 AI 跑基础采集，或让用户提供可用 Key。
- 结果里有残片/重复图：先给用户 Excel 草稿，再根据 `runs` 里的原图和 `orders.json` 调整规则。
