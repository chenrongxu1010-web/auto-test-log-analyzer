# 项目验收记录

## 验收信息

| 项目 | 内容 |
|---|---|
| 验收日期 | 2026-06-15 |
| Windows 环境 | Windows 11、Python 3.14 |
| Linux 环境 | WSL、Bash |
| 验收范围 | Shell 执行、日志生成、Python 分析、报告输出、自动化测试 |

## 实际执行命令

```bash
bash run_tests.sh
python3 analyze_log.py
python3 -m unittest discover -s tests -v
```

## 验收结果

| 检查项 | 实际结果 | 状态 |
|---|---|---|
| Shell 批量执行 | 输出 8 条模拟测试结果并生成时间戳日志 | 通过 |
| Python 默认分析 | 自动选择修改时间最新的日志 | 通过 |
| 日志统计 | Total=8、Pass=4、Fail=1、Warning=2、Error=1 | 通过 |
| 异常提取 | 提取 4 条 Fail、Warning、Error 日志 | 通过 |
| CSV 报告 | 正常生成，包含统计、通过率和结论 | 通过 |
| Markdown 报告 | 正常生成，包含统计表和异常明细 | 通过 |
| 自动化测试 | 7 个测试全部通过 | 通过 |
| 不存在日志 | 显示友好错误并返回退出码 1 | 通过 |
| 重复执行 | 间隔执行后生成两个不同时间戳日志 | 通过 |
| 输出目录自动创建 | 临时空目录中自动创建 `logs/`；测试中自动创建 `reports/` | 通过 |

## 自动化测试结果摘要

```text
Ran 7 tests
OK
```

## 已知限制

- Shell 模块需要 Linux、WSL 或 Git Bash；Windows PowerShell 可直接运行 Python 模块。
- Shell 中的任务是用于演示日志分析流程的模拟任务，不是真实业务系统测试。
- `reports/report.csv` 和 `reports/report.md` 每次分析时会被最新结果覆盖。
- 仓库保留不包含本机绝对路径的示例日志与报告截图。
