# 秩野Vibe爆款选题雷达

面向「秩野Vibe」账号的证据驱动型小红书选题 Skill。它会结合账号历史数据、近期公开信号和可持续内容矩阵，生成、去重、评分并排序下一批爆款候选选题。

## 核心能力

- 读取最新数据复盘、选题规划、发布信息和草稿标题；
- 区分已发布、制作中和已规划内容，降低重复；
- 使用「母题 × 人群 × 场景 × 限制 × 结果 × 形式 × 时间」扩展选题；
- 搜索公开趋势并区分事实、推断和创意；
- 从账号适配、需求、证据、点击、收藏和系列价值等维度评分；
- 将确认后的选题交接给图文制作流程，不自动发布。

## 安装

将本仓库克隆到 Codex skills 目录：

```powershell
git clone https://github.com/PD-XuHui/Topic-Search-Expert-ZY.git "$env:CODEX_HOME\skills\vibe-topic-radar"
```

如果没有设置 `CODEX_HOME`，可放入用户目录下的 `.codex/skills/vibe-topic-radar`。

## 使用示例

```text
使用 $vibe-topic-radar，结合秩野Vibe历史数据和近30天趋势，推荐下一批10个选题。
```

```text
使用 $vibe-topic-radar，围绕“职场新人形象提升”扩展选题，并排除已经发布和正在制作的内容。
```

## 项目结构

```text
.
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── account-strategy.md
│   ├── topic-engine.md
│   └── output-contract.md
└── scripts/score_topics.py
```

## 边界

本项目提供的是优先测试的「爆款候选」，不保证曝光、涨粉或商业结果；不会自动登录、抓取私有数据、绕过平台限制或自动发布内容。
