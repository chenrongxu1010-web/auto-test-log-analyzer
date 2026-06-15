#!/usr/bin/env bash

# 一键完成：生成日志、分析最新日志、运行 Python 自动化测试。
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

echo "=== 1/3 执行模拟测试任务 ==="
bash run_tests.sh

echo
echo "=== 2/3 分析最新日志并生成报告 ==="
python3 analyze_log.py

echo
echo "=== 3/3 运行自动化测试 ==="
python3 -m unittest discover -s tests -v

echo
echo "项目验收完成：日志、报告和自动化测试均已生成或执行。"
