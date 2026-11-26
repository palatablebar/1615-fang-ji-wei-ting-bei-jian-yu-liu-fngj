# 业务模块与回归证据

AI/ML / 传统ML · 中型

## 功能模块

| 编号 | 业务模块 | 交付内容 | 核心文件 | 测试文件 |
| --- | --- | --- | --- | --- |
| M1 | `loom_checklists` | 验签、换版与隔离 | `src/loomreserve/loom_checklists/contracts.py` `src/loomreserve/loom_checklists/parsing.py` `src/loomreserve/loom_checklists/service.py` | `tests/test_loom_checklists.py` |
| M2 | `repair_followups` | 按可见时点冻结样本和结果 | `src/loomreserve/repair_followups/contracts.py` `src/loomreserve/repair_followups/revisions.py` `src/loomreserve/repair_followups/service.py` | `tests/test_repair_followups.py` |
| M3 | `weft_indicators` | 形成训练与当班共用的领域特征 | `src/loomreserve/weft_indicators/contracts.py` `src/loomreserve/weft_indicators/indicators.py` `src/loomreserve/weft_indicators/service.py` | `tests/test_weft_indicators.py` |
| M4 | `failure_bayes` | 估计业务结果并输出本地归因 | `src/loomreserve/failure_bayes/contracts.py` `src/loomreserve/failure_bayes/estimator.py` `src/loomreserve/failure_bayes/service.py` | `tests/test_failure_bayes.py` |
| M5 | `shift_precision` | 逐窗校准并与历史基线比较 | `src/loomreserve/shift_precision/contracts.py` `src/loomreserve/shift_precision/calibration.py` `src/loomreserve/shift_precision/service.py` | `tests/test_shift_precision.py` |
| M6 | `loom_mix` | 识别缺测、未建档与分布变动 | `src/loomreserve/loom_mix/contracts.py` `src/loomreserve/loom_mix/distribution.py` `src/loomreserve/loom_mix/service.py` | `tests/test_loom_mix.py` |
| M7 | `spare_compatibility` | 按业务规则锁定和分派资源 | `src/loomreserve/spare_compatibility/contracts.py` `src/loomreserve/spare_compatibility/domain.py` `src/loomreserve/spare_compatibility/service.py` | `tests/test_spare_compatibility.py` |
| M8 | `stores_receipts` | 按版本发布、导出、回查与对账 | `src/loomreserve/stores_receipts/contracts.py` `src/loomreserve/stores_receipts/storage.py` `src/loomreserve/stores_receipts/service.py` | `tests/test_stores_receipts.py` |

## 高风险边界

| 编号 | 可观察后果 | 处理位置 | 回归用例 |
| --- | --- | --- | --- |
| TRAP-14 | 同版互斥读数隔离后继续处理其他单据 | `src/loomreserve/repair_followups/service.py` | `tests/test_repair_followups.py::test_exact_resends_and_conflicts` |
| TRAP-19 | 单据锁定优先于排队和默认动作 | `src/loomreserve/spare_compatibility/service.py` | `tests/test_spare_compatibility.py::test_locked_cannot_book` |
| TRAP-23 | 可见日等于截止的单据属于下一个窗口 | `src/loomreserve/repair_followups/service.py` | `tests/test_repair_followups.py::test_at_cut_is_future` |
| TRAP-26 | 陈旧发布请求保留已生效的派工版 | `src/loomreserve/stores_receipts/service.py` | `tests/test_stores_receipts.py::test_stale_leaves_head` |
| TRAP-32 | 恒定训练轴避免除零和新偏移误放 | `src/loomreserve/weft_indicators/service.py` | `tests/test_weft_indicators.py::test_constant_axis` |
| TRAP-42 | 未来修订绝不替换前序训练证据 | `src/loomreserve/repair_followups/service.py` | `tests/test_repair_followups.py::test_late_revision_cannot_revise_past` |
| TRAP-43 | 回放没有正例时说明指标不可定义 | `src/loomreserve/shift_precision/service.py` | `tests/test_shift_precision.py::test_no_positive_average_precision` |
| TRAP-44 | 未建档片区会拒识，异常流量高时禁止发布 | `src/loomreserve/loom_mix/service.py` | `tests/test_loom_mix.py::test_unseen_blocks_when_majority` |
| TRAP-53 | 批中相邻样本不改变单条评分 | `src/loomreserve/failure_bayes/service.py` | `tests/test_failure_bayes.py::test_point_invariance` |
| TRAP-54 | 账簿参数变化会改变模型摘要并重算 | `src/loomreserve/failure_bayes/service.py` | `tests/test_failure_bayes.py::test_fitted_signature_tracks_source` |
