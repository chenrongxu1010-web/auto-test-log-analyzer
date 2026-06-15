# 测试用例与执行记录

## 执行说明

- 执行日期：2026-06-15
- 实际环境：Windows 11、WSL、Bash、Python 3.14
- 自动化测试命令：`python -m unittest discover -s tests -v`
- 完整流程命令：`bash run_all.sh`
- 状态说明：自动化通过表示有代码测试证据；手工通过表示已实际操作验证；待验证表示当前环境未完成验证。

## 测试用例

| 用例编号 | 测试场景 | 前置条件 | 操作步骤 | 预期结果 | 执行方式 | 实际结果 | 状态 |
|---|---|---|---|---|---|---|---|
| FUNC-001 | 正常执行测试任务 | Bash 可用 | 执行 `bash run_tests.sh` | 8 条模拟任务被执行，显示完成提示 | 手工 | WSL 执行成功 | 通过 |
| FUNC-002 | 执行结果为 Pass | 已运行 Shell 脚本 | 查看生成日志中的 `[PASS]` 行 | 存在 4 条 Pass 日志 | 手工 | 实际为 4 条 | 通过 |
| FUNC-003 | 执行结果为 Fail | 已运行 Shell 脚本 | 查看生成日志中的 `[FAIL]` 行 | 存在 1 条 Fail 日志和原因 | 手工 | 实际为 1 条 | 通过 |
| FUNC-004 | 执行结果包含 Warning | 已运行 Shell 脚本 | 查看 `[WARNING]` 行 | 存在 2 条 Warning 日志 | 手工 | 实际为 2 条 | 通过 |
| FUNC-005 | 执行结果包含 Error | 已运行 Shell 脚本 | 查看 `[ERROR]` 行 | 存在 1 条 Error 日志 | 手工 | 实际为 1 条 | 通过 |
| FUNC-006 | 日志文件正常生成 | `logs/` 可写 | 执行 Shell 脚本 | 生成时间戳日志 | 手工 | 已生成时间戳日志 | 通过 |
| FUNC-007 | 日志文件为空 | 创建空日志 | 指定空日志执行分析 | 所有统计为 0，报告正常生成 | 自动化 | `test_analyze_empty_log_returns_zero_counts` 通过 | 通过 |
| FUNC-008 | 日志文件不存在 | 指定不存在路径 | 执行分析命令 | 显示友好错误并返回退出码 1 | 手工 | 友好提示，退出码为 1 | 通过 |
| FUNC-009 | 指定日志路径分析 | `logs/sample.log` 存在 | 使用 `--log` 参数分析 | 分析指定日志 | 手工 | 统计结果符合样例 | 通过 |
| FUNC-010 | 默认分析最新日志 | `logs/` 中存在多个日志 | 不指定 `--log` 执行分析 | 按修改时间选择最新日志 | 自动化 | `test_find_latest_log_returns_newest_file` 通过 | 通过 |
| FUNC-011 | CSV 报告正常生成 | 日志有效 | 执行分析并打开 CSV | 包含统计、通过率和结论 | 自动化 | `test_write_reports_creates_csv_and_markdown` 通过 | 通过 |
| FUNC-012 | Markdown 报告正常生成 | 日志有效 | 执行分析并打开 Markdown | 包含统计表和异常明细 | 自动化 | `test_write_reports_creates_csv_and_markdown` 通过 | 通过 |
| FUNC-013 | 重复执行脚本 | Bash 可用 | 间隔 1 秒运行两次脚本 | 生成两个不同日志文件 | 手工 | 已生成两个不同时间戳日志 | 通过 |
| FUNC-014 | 异常关键词提取 | 日志包含异常关键词 | 执行日志分析 | 提取 Fail、Warning、Error 行 | 自动化 | `test_analyze_log_extracts_abnormal_lines` 通过 | 通过 |
| FUNC-015 | 输出目录不存在时自动创建 | 删除输出目录 | 依次执行脚本和分析器 | 自动创建目录并输出文件 | 自动化/手工 | 临时空目录验证日志目录；自动化测试验证报告目录 | 通过 |
| FUNC-016 | 统计结果准确 | 使用示例日志 | 执行分析并核对结果 | Total=8、Pass=4、Fail=1、Warning=2、Error=1 | 自动化/手工 | 自动化统计与终端结果一致 | 通过 |
| FUNC-017 | Windows Python 兼容运行 | Windows 安装 Python 3 | 执行 Windows 分析命令 | 成功生成报告 | 手工 | Windows PowerShell 执行成功 | 通过 |

## 执行结论

- 已通过：17 条
- 部分通过：0 条
- 待验证：0 条
- 已知未关闭缺陷：无
- 后续验证重点：接入真实接口或网页测试后补充业务场景
