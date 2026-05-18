# v0.32 Signoff Report

## Scope

v0.32 is a focused update on top of v0.31. The release adds Volume 12:

- Source: `04_generated_drafts/12_zhongguancun_machine_exam_companion.md`
- PDF: `12_zhongguancun_machine_exam_companion.pdf`

## Content Checks

- Covers the official machine-exam rule summary.
- Covers the 3-hour / 3-problem strategy and 32-submission policy.
- Covers all 12 collected Zhongguancun past machine-exam problems.
- Each problem card includes routing, partial-score strategy, upgrade path, key state/data structure, pitfalls, assembly guidance, and exam writing advice.
- Each past-problem card now includes a `现场迭代路线` section explaining the real exam motivation: first submission, why it is insufficient, and how to upgrade.
- Each past-problem card now embeds complete runnable code inside the problem explanation instead of relying on a detached code library at the end.
- Volume 12 currently contains 30 complete C++17 programs across the 12 past-problem cards.
- Includes D1-D14 exam cards for rules, rhythm, submissions, complexity, fractional programming, arbitrage log graph, circular segment tree, character mapping, mixed input parsing, floating point, overflow, statement contradictions, partial-score priority, and final checks.

## Verification

- Markdown structure check: 12 C problem cards, 12 `现场迭代路线` sections, 30 `代码卡片`, 30 complete C++17 programs, no old `## Gx` detached code headings.
- Markdown parse check: `pandoc -t native` succeeds.
- Code check: all 30 complete C++17 programs compile with WSL `g++ -std=c++17 -O2 -pipe -Wall -Wextra`.
- Runtime check: all 30 programs pass selected small or boundary sample tests.
- PDF build check: `12_zhongguancun_machine_exam_companion.pdf` rebuilt successfully as 51 pages.
- PDF visual spot check: title/TOC page, code pages, and final code-index pages render with readable Chinese text and non-clipped code.
- Release check: v0.32 manifest and zip were regenerated after the final Volume 12 source update.

## Focused Review Notes

- The v0.31 example restoration work remains preserved.
- The v0.32 change intentionally avoids a broad rewrite of existing volumes.
- Review found and the main thread fixed the most important Volume 12 issues: detached code organization, missing partial-score programs, C8 code-index mismatch, floating-point epsilon wording, card numbering, module IDs, router ambiguity, and final-rescue wording.
