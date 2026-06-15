"""从命令行启动 analyze_log.py，验证用户实际运行路径。"""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class CommandLineTests(unittest.TestCase):
    """验证成功分析和错误提示两个命令行场景。"""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_dir = Path(self.temp_dir.name)
        (self.project_dir / "logs").mkdir()
        shutil.copy2(PROJECT_ROOT / "analyze_log.py", self.project_dir)
        shutil.copy2(PROJECT_ROOT / "logs" / "sample.log", self.project_dir / "logs")

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_analyzer(self, *args: str) -> subprocess.CompletedProcess:
        """在临时项目目录中真实启动分析脚本。"""
        return subprocess.run(
            [sys.executable, "analyze_log.py", *args],
            cwd=self.project_dir,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

    def test_cli_analyzes_specified_log_and_creates_reports(self):
        result = self.run_analyzer("--log", "logs/sample.log")

        self.assertEqual(result.returncode, 0)
        self.assertIn("总数：8", result.stdout)
        self.assertTrue((self.project_dir / "reports" / "report.csv").is_file())
        self.assertTrue((self.project_dir / "reports" / "report.md").is_file())
        markdown = (self.project_dir / "reports" / "report.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("`logs/sample.log`", markdown)

    def test_cli_returns_friendly_error_for_missing_log(self):
        result = self.run_analyzer("--log", "logs/not_found.log")

        self.assertEqual(result.returncode, 1)
        self.assertIn("[ERROR] 分析失败：日志文件不存在", result.stderr)


if __name__ == "__main__":
    unittest.main()
