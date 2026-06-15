"""analyze_log.py 的自动化测试。"""

import csv
import os
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from analyze_log import analyze_log, find_latest_log, write_reports


class AnalyzeLogTests(unittest.TestCase):
    """验证日志分析和报告输出的核心行为。"""

    def test_analyze_log_counts_each_result(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            log_path = Path(temp_dir) / "test.log"
            log_path.write_text(
                "[2026-06-15 10:00:00] [PASS] Login test passed\n"
                "[2026-06-15 10:00:01] [FAIL] Search test failed\n"
                "[2026-06-15 10:00:02] [WARNING] Slow response\n"
                "[2026-06-15 10:00:03] [ERROR] Database unavailable\n",
                encoding="utf-8",
            )

            result = analyze_log(log_path)

            self.assertEqual(result["total"], 4)
            self.assertEqual(result["pass"], 1)
            self.assertEqual(result["fail"], 1)
            self.assertEqual(result["warning"], 1)
            self.assertEqual(result["error"], 1)

    def test_analyze_log_extracts_abnormal_lines(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            log_path = Path(temp_dir) / "test.log"
            log_path.write_text(
                "[PASS] Normal task passed\n"
                "[FAIL] Payment failed\n"
                "[WARNING] Response is slow\n"
                "[ERROR] Service stopped\n",
                encoding="utf-8",
            )

            result = analyze_log(log_path)

            self.assertEqual(len(result["abnormal_lines"]), 3)

    def test_analyze_empty_log_returns_zero_counts(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            log_path = Path(temp_dir) / "empty.log"
            log_path.write_text("", encoding="utf-8")

            result = analyze_log(log_path)

            self.assertEqual(result["total"], 0)
            self.assertEqual(result["abnormal_lines"], [])

    def test_find_latest_log_returns_newest_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            logs_dir = Path(temp_dir)
            old_log = logs_dir / "z_old.log"
            new_log = logs_dir / "a_new.log"
            old_log.write_text("old", encoding="utf-8")
            new_log.write_text("new", encoding="utf-8")
            os.utime(old_log, (1, 1))
            os.utime(new_log, (2, 2))

            latest = find_latest_log(logs_dir)

            self.assertEqual(latest, new_log)

    def test_write_reports_creates_csv_and_markdown(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            reports_dir = Path(temp_dir) / "reports"
            result = {
                "log_file": "sample.log",
                "total": 4,
                "pass": 1,
                "fail": 1,
                "warning": 1,
                "error": 1,
                "abnormal_lines": ["[FAIL] Search failed"],
            }

            csv_path, md_path = write_reports(result, reports_dir)

            self.assertTrue(csv_path.exists())
            self.assertTrue(md_path.exists())
            with csv_path.open(encoding="utf-8-sig", newline="") as csv_file:
                rows = list(csv.DictReader(csv_file))
            self.assertEqual(rows[0]["Total"], "4")
            self.assertEqual(rows[0]["Pass Rate"], "25.0%")
            self.assertEqual(rows[0]["Conclusion"], "存在失败或错误")
            markdown = md_path.read_text(encoding="utf-8")
            self.assertIn("异常日志明细", markdown)
            self.assertIn("| 通过率 | 25.0% |", markdown)
            self.assertIn("| 测试结论 | 存在失败或错误 |", markdown)


if __name__ == "__main__":
    unittest.main()
