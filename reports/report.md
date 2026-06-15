# 自动化测试日志分析报告

## 报告信息

- 日志文件：`logs/sample.log`

## 统计结果

| 指标 | 数量 |
|---|---:|
| 总测试数 | 8 |
| Pass | 4 |
| Fail | 1 |
| Warning | 2 |
| Error | 1 |
| 通过率 | 50.0% |
| 测试结论 | 存在失败或错误 |

## 异常日志明细

- `[2026-06-15 10:00:03] [FAIL] TC003 Checkout test failed: total price mismatch`
- `[2026-06-15 10:00:04] [WARNING] TC004 API response time exceeded 2 seconds`
- `[2026-06-15 10:00:05] [ERROR] TC005 Database connection unavailable`
- `[2026-06-15 10:00:07] [WARNING] TC007 Disk usage reached 85 percent`
