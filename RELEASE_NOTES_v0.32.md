# Release Notes v0.32

v0.32 is a focused release on top of v0.31. It adds a new exam-specific companion volume:

- `第12卷 中关村机试往年题专项与现场拼装卡片`
- Source: `04_generated_drafts/12_zhongguancun_machine_exam_companion.md`
- PDF: `12_zhongguancun_machine_exam_companion.pdf`

## Highlights

- Adds official machine-exam rule cards for the 3-hour, 3-problem, paper-open-book setting.
- Adds a 3-hour rhythm card, 32-submission strategy card, complexity routing card, and final 30-minute rescue card.
- Covers 12 collected Zhongguancun past machine-exam problems from 2025 spring/summer/autumn and 2026 winter.
- Each past problem includes signals, first reaction, partial-score route, upgrade route, key state/data structure, pitfalls, and module assembly checklist.
- Each past problem now also embeds complete runnable C++17 code cards inside the problem explanation, covering partial-score versions and main/answer versions.
- Adds explicit `现场迭代路线` sections so the paper version explains why to write the first version, when to submit it, and how to upgrade under exam pressure.
- Adds focused cards for fractional programming, arbitrage log graphs, circular segment trees, character injection mapping, mixed input parsing, floating-point comparison, overflow, and statement contradictions.
- Final signoff rechecked beginner-friendly routing fields for all 12 past-problem cards and reran the standalone C++ regression suite with zero compile/runtime failures.
- Updates the chapter index and release package to include Volume 12 as a must-bring Zhongguancun machine-exam companion.

## Release Intent

This release intentionally avoids a broad rewrite of existing v0.31 volumes. The main change is the new Volume 12 and the related index/release wiring.
