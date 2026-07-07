#!/usr/bin/env python3
"""Generate a prototype configurator from the bundled HTML template."""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = SKILL_DIR / "templates" / "configurator-template.html"

CHART_SMART = "智能按需：无图表场景不强行加入；涉及指标、趋势、对比、分布或看板时优先使用 ECharts 可交互图表"
CHART_NATIVE = "原生轻量图表：使用 HTML/CSS/SVG/Canvas 做简单图形或参数曲线，减少外部依赖"
CHART_ECHARTS = "ECharts 可交互图表：通过 CDN 引入 ECharts，提供 tooltip、legend、筛选/切换和加载失败降级"


SCENARIOS = [
    {
        "name": "activity",
        "pattern": r"活动|落地页|官网|转化|报名|预约|领取|促销|618|双11|营销",
        "label": "官网/活动页",
        "reason": "适合官网、活动、报名、预约、促销和强转化页面。",
        "flow": "从首屏理解价值，浏览核心卖点，完成报名/预约/领取等转化动作",
        "goal": "汇报演示/方案呈现",
        "roles": ["目标用户", "运营/市场", "产品经理"],
        "scope": "首页卖点 + 活动详情 + 转化操作",
        "features": ["内容浏览", "转化按钮", "表单提交", "状态反馈"],
        "gsap": "汇报增强：使用 GSAP 时间轴强化模块入场、流程推进、指标滚动和方案亮点展示",
        "fields": "活动主题、利益点、目标人群、转化按钮、报名状态、优惠信息、时间节点、常见问题、成功反馈",
        "states": "默认、加载、无内容、提交中、提交成功、提交失败、名额已满、活动结束",
        "changes": "首屏要有吸引力，利益点清楚，转化路径短；不要做成后台页面。"
    },
    {
        "name": "education",
        "pattern": r"物理|科普|原理|动画|学习|知识|课程|实验|公式|教学|教育|题库|训练|力学|电磁|光学|热学",
        "label": "C 端内容/社区",
        "reason": "适合科普内容浏览、动画讲解、互动实验和学习路径。",
        "flow": "从首页选择学习主题，进入知识详情，观看动画演示，调节参数并查看结论",
        "goal": "汇报演示/方案呈现",
        "roles": ["学生/学习者", "教师/家长", "科普爱好者"],
        "scope": "首页主题推荐 + 知识详情 + 动画实验页",
        "features": ["主题搜索", "知识详情", "动画演示", "参数调节"],
        "gsap": "趣味演示：使用 GSAP 做滚动叙事、卡片翻转、路径高亮或文字动效，适合概念 Demo",
        "fields": "学习主题、难度、学习时长、核心概念、动画演示步骤、可调参数、公式解释、生活案例、实验结论、推荐下一课",
        "states": "默认、动画播放中、暂停、参数调整后、知识点完成、测验答对、测验答错、加载失败、无搜索结果",
        "changes": "面向普通学习者，避免后台感；重点突出动画演示区、参数调节、公式与生活案例的对应关系。"
    },
    {
        "name": "content",
        "pattern": r"内容|社区|推荐|关注|创作者|帖子|直播|短视频|动态|种草|文章|资讯",
        "label": "C 端内容/社区",
        "reason": "适合内容浏览、推荐流、社区互动、创作者和用户增长。",
        "flow": "从推荐内容进入详情，完成浏览、互动、收藏和继续探索",
        "goal": "流程验证/可用性讨论",
        "roles": ["内容浏览用户", "创作者", "产品经理"],
        "scope": "推荐首页 + 内容详情 + 互动操作",
        "features": ["内容搜索", "详情查看", "点赞收藏", "评论互动"],
        "gsap": "克制动效：使用 GSAP 做页面进入、弹窗、状态反馈、指标计数等轻量微交互",
        "fields": "内容标题、作者、分类、热度、互动数、推荐理由、评论、收藏状态、相关推荐",
        "states": "默认、加载、无搜索结果、已点赞、已收藏、评论成功、评论失败、网络异常",
        "changes": "突出内容浏览节奏和互动反馈，移动端要顺手，避免后台感。"
    },
    {
        "name": "mobile",
        "pattern": r"App|小程序|移动|手机|会员|打卡|下单|支付|消费|用户|个人|生活|健身",
        "label": "C 端 App/小程序",
        "reason": "适合 C 端 App、小程序、移动工具、会员、消费、打卡和下单体验。",
        "flow": "从首页进入核心任务，完成选择、操作、反馈和下一步引导",
        "goal": "流程验证/可用性讨论",
        "roles": ["C 端用户", "产品经理", "设计评审人"],
        "scope": "首页 + 核心任务 + 结果反馈",
        "features": ["快捷入口", "核心操作", "状态反馈", "结果页"],
        "gsap": "克制动效：使用 GSAP 做页面进入、弹窗、状态反馈、指标计数等轻量微交互",
        "fields": "用户昵称、任务名称、进度、状态、权益、操作按钮、反馈文案、推荐内容、下一步动作",
        "states": "默认、加载、空状态、操作成功、操作失败、权限不足、网络异常、已完成",
        "changes": "移动优先，路径短，反馈明确，触控区域足够大。"
    },
    {
        "name": "ai",
        "pattern": r"AI|智能|助手|知识库|研报|对话|Copilot|Agent|自动",
        "label": "AI 工作台型",
        "reason": "适合 AI 助手、智能流程、研报、知识库和任务自动化。",
        "flow": "输入任务目标，AI 生成结果，用户查看依据、调整参数并确认输出",
        "goal": "需求评审/研发对齐",
        "roles": ["业务用户", "产品经理", "研发/测试"],
        "scope": "任务输入 + 生成过程 + 结果确认",
        "features": ["任务输入", "生成状态", "结果编辑", "引用查看"],
        "gsap": "克制动效：使用 GSAP 做页面进入、弹窗、状态反馈、指标计数等轻量微交互",
        "fields": "任务名称、输入内容、生成状态、引用来源、结果摘要、置信度、编辑建议、下一步动作",
        "states": "默认、生成中、生成成功、生成失败、无引用、结果已确认、需要人工复核",
        "changes": "突出任务流、生成结果、引用依据和可控编辑，避免只做聊天窗口。"
    },
    {
        "name": "dashboard",
        "pattern": r"数据|指标|监控|看板|报表|分析|诊断|趋势",
        "label": "数据看板型",
        "reason": "适合指标、监控、经营分析、报表和诊断类需求。",
        "flow": "查看指标总览，定位异常，钻取详情并输出判断",
        "goal": "需求评审/研发对齐",
        "roles": ["业务运营", "数据分析师", "管理者"],
        "scope": "指标总览 + 异常详情 + 诊断建议",
        "features": ["指标筛选", "图表统计", "异常钻取", "导出分享"],
        "gsap": "克制动效：使用 GSAP 做页面进入、弹窗、状态反馈、指标计数等轻量微交互",
        "fields": "指标名称、当前值、环比、同比、趋势、异常原因、影响范围、建议动作",
        "states": "默认、加载、无数据、指标异常、筛选后、导出成功、导出失败",
        "changes": "指标优先，异常突出，图表和结论要能快速被理解。"
    },
    {
        "name": "workbench",
        "pattern": r"工作台|运营台|坐席|审批|工单|任务处理|待办|协作|外勤",
        "label": "B 端工作台型",
        "reason": "适合运营台、审批台、坐席台、工单和多角色协同。",
        "flow": "查看待办任务，进入详情处理，提交结果并同步状态",
        "goal": "需求评审/研发对齐",
        "roles": ["业务运营", "主管/审批人", "研发/测试"],
        "scope": "任务列表 + 详情 + 核心操作",
        "features": ["搜索筛选", "详情查看", "状态流转", "协作审批"],
        "gsap": "不使用 GSAP：保持原生 HTML/CSS/JS，优先保证轻量稳定",
        "fields": "任务名称、优先级、负责人、截止时间、处理状态、协作人、处理记录、下一步动作",
        "states": "默认、加载、空状态、处理中、提交成功、提交失败、权限不足、已完成",
        "changes": "任务聚合清楚，处理路径短，状态流转和异常边界可评审。"
    },
    {
        "name": "b2b",
        "pattern": r"后台|管理|平台|CRM|权限|配置|运营|B端|SaaS|列表",
        "label": "清爽 B 端 SaaS",
        "reason": "适合后台、管理平台、CRM、运营工具和配置类需求。",
        "flow": "从列表进入详情，完成筛选、编辑、提交和状态反馈",
        "goal": "需求评审/研发对齐",
        "roles": ["业务运营", "产品经理", "研发/测试"],
        "scope": "列表 + 详情 + 核心操作",
        "features": ["搜索筛选", "详情查看", "新增/编辑", "状态流转"],
        "gsap": "不使用 GSAP：保持原生 HTML/CSS/JS，优先保证轻量稳定",
        "fields": "名称、状态、负责人、更新时间、类型、数量、转化率、异常原因、下一步动作",
        "states": "默认、加载、空状态、保存成功、保存失败、权限不足、审核中、已完成",
        "changes": "界面简约清爽，不要拥挤；重点保证流程、字段、异常状态和验收边界可评审。"
    },
]


def choose_scenario(prompt: str) -> dict:
    for scenario in SCENARIOS:
      if re.search(scenario["pattern"], prompt, re.I):
          return scenario
    return SCENARIOS[-1]


def js_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)[1:-1]


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "-", value.strip()).strip("-")
    return slug.lower() or "prototype"


def replace_checked(html_text: str, name: str, value: str) -> str:
    html_text = re.sub(
        rf'(<input type="radio" name="{re.escape(name)}"[^>]*?)\s+checked(?=[\s/>])',
        r"\1",
        html_text,
    )
    pattern = rf'(<input type="radio" name="{re.escape(name)}" value="{re.escape(value)}"[^>]*?)(\s*/>)'
    return re.sub(pattern, r"\1 checked\2", html_text, count=1)


def replace_checkboxes(html_text: str, name: str, values: list[str]) -> str:
    html_text = re.sub(
        rf'(<input type="checkbox" name="{re.escape(name)}"[^>]*?)\s+checked(?=[\s/>])',
        r"\1",
        html_text,
    )
    for value in values:
        pattern = rf'(<input type="checkbox" name="{re.escape(name)}" value="{re.escape(value)}"[^>]*?)(\s*/>)'
        html_text = re.sub(pattern, r"\1 checked\2", html_text, count=1)
    return html_text


def apply_scenario_checks(html_text: str, scenario: dict) -> str:
    label = scenario["label"]
    if label == "官网/活动页":
        choices = {
            "scene": "官网/活动/转化页",
            "audience": "C 端个人用户：重视路径短、情绪反馈、视觉吸引、移动触控",
            "style": "官网/活动转化型：首屏吸引、利益点明确、转化路径突出，适合活动和官网",
            "tone": "红色系：活动、提醒、消费、热度，适合促销和强转化",
            "layout": "内容沉浸型：强调首屏内容、卡片流、浏览节奏和互动入口",
        }
        experience = ["强引导", "强反馈", "转化路径"]
    elif label == "C 端 App/小程序":
        choices = {
            "scene": "C 端 App/小程序",
            "audience": "C 端个人用户：重视路径短、情绪反馈、视觉吸引、移动触控",
            "style": "C 端 App/小程序型：触控友好、路径短、反馈清晰，适合移动端体验",
            "tone": "绿色系：健康、增长、稳定，适合打卡、成长和稳健业务",
            "layout": "移动优先型：强调触控、底部导航、路径短和关键反馈",
        }
        experience = ["快速完成", "强引导", "强反馈"]
    elif label == "C 端内容/社区":
        choices = {
            "scene": "C 端内容/社区",
            "audience": "C 端个人用户：重视路径短、情绪反馈、视觉吸引、移动触控",
            "style": "C 端内容/社区型：内容优先、沉浸浏览、互动反馈强，适合社区和增长场景",
            "tone": "蓝色系：可信、效率、科技，适合通用 B 端和企业服务",
            "layout": "内容沉浸型：强调首屏内容、卡片流、浏览节奏和互动入口",
        }
        experience = ["强引导", "强反馈", "内容浏览", "数据洞察"]
    elif label == "AI 工作台型":
        choices = {
            "scene": "AI 助手/智能流程",
            "audience": "混合场景：兼顾管理效率和用户体验",
            "style": "AI 工作台型：对话、任务流和知识结果并重，适合 AI 助手和智能流程",
            "tone": "蓝色系：可信、效率、科技，适合通用 B 端和企业服务",
            "layout": "任务流引导型：强调步骤、待办、进度、下一步动作和结果反馈",
        }
        experience = ["快速完成", "强引导", "强反馈", "数据洞察"]
    elif label == "数据看板型":
        choices = {
            "scene": "数据看板/分析诊断",
            "audience": "B 端组织用户：重视效率、权限、状态、批量操作",
            "style": "数据看板型：指标优先、图表清晰、异常突出，适合分析和监控场景",
            "tone": "蓝色系：可信、效率、科技，适合通用 B 端和企业服务",
            "layout": "数据决策型：强调指标总览、趋势洞察、异常定位和钻取分析",
        }
        experience = ["快速完成", "数据洞察", "异常处理"]
    elif label == "B 端工作台型":
        choices = {
            "scene": "B 端工作台/运营台",
            "audience": "B 端组织用户：重视效率、权限、状态、批量操作",
            "style": "B 端工作台型：任务聚合、待办优先、协作流清晰，适合运营台和审批台",
            "tone": "蓝色系：可信、效率、科技，适合通用 B 端和企业服务",
            "layout": "任务流引导型：强调步骤、待办、进度、下一步动作和结果反馈",
        }
        experience = ["快速完成", "协作审批", "异常处理"]
    else:
        choices = {
            "scene": "B 端 SaaS/管理后台",
            "audience": "B 端组织用户：重视效率、权限、状态、批量操作",
            "style": "清爽 B 端 SaaS：白底、克制、信息层级清晰，适合后台和管理平台",
            "tone": "蓝色系：可信、效率、科技，适合通用 B 端和企业服务",
            "layout": "桌面信息密集型：强调筛选、列表、详情、批量操作和状态管理",
        }
        experience = ["快速完成", "协作审批", "异常处理"]

    chart = CHART_SMART
    if label == "数据看板型":
        chart = CHART_ECHARTS
    elif scenario["name"] == "education":
        chart = CHART_NATIVE

    for name, value in choices.items():
        html_text = replace_checked(html_text, name, value)
    html_text = replace_checked(html_text, "goal", scenario["goal"])
    html_text = replace_checked(html_text, "scope", scenario["scope"])
    html_text = replace_checked(html_text, "gsap", scenario["gsap"])
    html_text = replace_checked(html_text, "chart", chart)
    html_text = replace_checkboxes(html_text, "roles", scenario["roles"])
    html_text = replace_checkboxes(html_text, "features", scenario["features"])
    return replace_checkboxes(html_text, "experience", experience)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    parser.add_argument("--prompt")
    parser.add_argument("--output")
    args = parser.parse_args()

    topic = args.topic.strip()
    prompt = args.prompt or f"做一个{topic}原型"
    scenario = choose_scenario(prompt + " " + topic)
    page_title = f"{topic}原型生成确认页"
    subtitle = "先确认场景、用户、风格、体验和约束，再生成可演示的 HTML 原型。"

    html_text = TEMPLATE_PATH.read_text(encoding="utf-8")
    replacements = {
        "{{PAGE_TITLE}}": html.escape(page_title),
        "{{PAGE_SUBTITLE}}": html.escape(subtitle),
        "{{PROMPT}}": html.escape(prompt),
        "{{TOPIC}}": html.escape(topic),
        "{{FLOW}}": html.escape(scenario["flow"]),
        "{{RECOMMEND_LABEL}}": html.escape(scenario["label"]),
        "{{RECOMMEND_REASON}}": html.escape(scenario["reason"]),
        "{{FIELDS}}": html.escape(scenario["fields"]),
        "{{STATES}}": html.escape(scenario["states"]),
        "{{CHANGES}}": html.escape(scenario["changes"]),
        "{{PROMPT_JS}}": js_string(prompt),
        "{{TOPIC_JS}}": js_string(topic),
        "{{FLOW_JS}}": js_string(scenario["flow"]),
        "{{FIELDS_JS}}": js_string(scenario["fields"]),
        "{{STATES_JS}}": js_string(scenario["states"]),
        "{{CHANGES_JS}}": js_string(scenario["changes"]),
    }
    for key, value in replacements.items():
        html_text = html_text.replace(key, value)
    html_text = apply_scenario_checks(html_text, scenario)

    output = Path(args.output) if args.output else Path.cwd() / f"prototype-configurator-{slugify(topic)}.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html_text, encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
