#!/usr/bin/env python3
"""分析自动化测试日志，并生成 CSV 和 Markdown 测试报告。"""

import argparse
import csv
import re
import sys
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_LOGS_DIR = PROJECT_ROOT / "logs"
DEFAULT_REPORTS_DIR = PROJECT_ROOT / "reports"
RESULT_PATTERN = re.compile(r"\[(PASS|FAIL|WARNING|ERROR)\]", re.IGNORECASE)
ABNORMAL_PATTERN = re.compile(r"\b(error|warning|failed|fail)\b", re.IGNORECASE)


def find_latest_log(logs_dir: Path) -> Path:
    """返回 logs 目录中修改时间最新的 .log 文件。"""
    log_files = list(logs_dir.glob("*.log"))
    if not log_files:
        raise FileNotFoundError(f"目录中没有可分析的日志文件：{logs_dir}")
    return max(log_files, key=lambda path: path.stat().st_mtime_ns)


def analyze_log(log_path: Path) -> dict:
    """读取日志并统计测试结果，同时提取异常日志行。"""
    counts = {"pass": 0, "fail": 0, "warning": 0, "error": 0}
    abnormal_lines = []

    with log_path.open("r", encoding="utf-8") as log_file:
        for raw_line in log_file:
            line = raw_line.strip()
            if not line:
                continue

            result_match = RESULT_PATTERN.search(line)
            if result_match:
                level = result_match.group(1).lower()
                counts[level] += 1

            if ABNORMAL_PATTERN.search(line):
                abnormal_lines.append(line)

    return {
        "log_file": str(log_path),
        "total": sum(counts.values()),
        **counts,
        "abnormal_lines": abnormal_lines,
    }


def write_reports(result: dict, reports_dir: Path) -> tuple[Path, Path]:
    """创建 reports 目录，并写入 CSV 与 Markdown 报告。"""
    reports_dir.mkdir(parents=True, exist_ok=True)
    csv_path = reports_dir / "report.csv"
    markdown_path = reports_dir / "report.md"
    pass_rate = result["pass"] / result["total"] * 100 if result["total"] else 0
    pass_rate_text = f"{pass_rate:.1f}%"
    conclusion = (
        "存在失败或错误"
        if result["fail"] > 0 or result["error"] > 0
        else "未发现失败或错误"
    )

    # 使用 utf-8-sig，方便在 Windows Excel 中直接查看中文内容。
    with csv_path.open("w", encoding="utf-8-sig", newline="") as csv_file:
        fieldnames = [
            "Log File",
            "Total",
            "Pass",
            "Fail",
            "Warning",
            "Error",
            "Pass Rate",
            "Conclusion",
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(
            {
                "Log File": result["log_file"],
                "Total": result["total"],
                "Pass": result["pass"],
                "Fail": result["fail"],
                "Warning": result["warning"],
                "Error": result["error"],
                "Pass Rate": pass_rate_text,
                "Conclusion": conclusion,
            }
        )

    abnormal_text = "\n".join(
        f"- `{line}`" for line in result["abnormal_lines"]
    ) or "- 未发现异常日志"
    report_content = f"""# 自动化测试日志分析报告

## 报告信息

- 分析时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- 日志文件：`{result["log_file"]}`

## 统计结果

| 指标 | 数量 |
|---|---:|
| 总测试数 | {result["total"]} |
| Pass | {result["pass"]} |
| Fail | {result["fail"]} |
| Warning | {result["warning"]} |
| Error | {result["error"]} |
| 通过率 | {pass_rate_text} |
| 测试结论 | {conclusion} |

## 异常日志明细

{abnormal_text}
"""
    markdown_path.write_text(report_content, encoding="utf-8")
    return csv_path, markdown_path


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(description="分析自动化测试日志并生成报告")
    parser.add_argument(
        "--log",
        type=Path,
        help="指定要分析的日志文件；不指定时分析 logs/ 中最新的日志",
    )
    return parser.parse_args()


def main() -> int:
    """程序入口：选择日志、执行分析并输出报告。"""
    args = parse_args()

    try:
        log_path = args.log if args.log else find_latest_log(DEFAULT_LOGS_DIR)
        if not log_path.is_absolute():
            log_path = Path.cwd() / log_path
        if not log_path.is_file():
            raise FileNotFoundError(f"日志文件不存在：{log_path}")

        result = analyze_log(log_path)
        # 项目内文件在报告中使用相对路径，避免上传仓库时暴露本机目录。
        try:
            result["log_file"] = log_path.resolve().relative_to(PROJECT_ROOT).as_posix()
        except ValueError:
            pass
        csv_path, markdown_path = write_reports(result, DEFAULT_REPORTS_DIR)
    except (FileNotFoundError, OSError, UnicodeError) as error:
        print(f"[ERROR] 分析失败：{error}", file=sys.stderr)
        return 1

    print("日志分析完成")
    print(f"日志文件：{log_path}")
    print(
        f"总数：{result['total']} | Pass：{result['pass']} | "
        f"Fail：{result['fail']} | Warning：{result['warning']} | "
        f"Error：{result['error']}"
    )
    print(f"异常日志：{len(result['abnormal_lines'])} 条")
    print(f"报告文件：{csv_path}、{markdown_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
