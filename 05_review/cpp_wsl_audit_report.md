# WSL g++ C++ 代码块审计

- 模块文件：143
- C++ 代码块：636
- 编译尝试：285（standalone + snippet 包壳）
- standalone 编译失败：0
- snippet 需要上下文：79（不代表完整程序错误，只作为人工审计线索）

| 文件 | 块 | 行 | 分类 | 状态 | 摘要 |
|---|---:|---:|---|---|---|
| `03_modules\AI-00-ai-topic-routing.md` | 2 | 115 | standalone | OK |  |
| `03_modules\AI-01-search-planning-game-ai.md` | 2 | 67 | standalone | OK |  |
| `03_modules\AI-01-search-planning-game-ai.md` | 3 | 175 | snippet | OK |  |
| `03_modules\AI-02-lightweight-ml-classification.md` | 1 | 50 | snippet | OK |  |
| `03_modules\AI-02-lightweight-ml-classification.md` | 2 | 66 | standalone | OK |  |
| `03_modules\AI-02-lightweight-ml-classification.md` | 3 | 166 | snippet | OK |  |
| `03_modules\AI-03-similarity-recommendation-text.md` | 2 | 66 | standalone | OK |  |
| `03_modules\AI-03-similarity-recommendation-text.md` | 3 | 185 | snippet | OK |  |
| `03_modules\AI-04-ai-basics-formula-cheatsheet.md` | 2 | 106 | snippet | OK |  |
| `03_modules\AI-04-ai-basics-formula-cheatsheet.md` | 3 | 134 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_15.cpp:8:24: error: ‘w’ was not declared in this scope<br>    8 \| double z = dot_product(w, x, d) + b;<br>      \|                        ^<br><repo>/05_review/tmpdu19mmj0/block_15.cpp:8:27: error: ‘x’ was not declared in this scope<br>    8 \| double z = dot_product(w, x, d) + b; |
| `03_modules\AI-05-text-tfidf-tokenizer.md` | 2 | 65 | standalone | OK |  |
| `03_modules\AI-05-text-tfidf-tokenizer.md` | 3 | 154 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_18.cpp:8:24: error: ‘tokenize’ was not declared in this scope<br>    8 \| vector<string> words = tokenize("Apple, banana! apple");<br>      \|                        ^~~~~~~~<br><repo>/05_review/tmpdu19mmj0/block_18.cpp:9:12: error: ‘count_words’ was not declared in this scope<br>    9 \| auto cnt = count_words(words); |
| `03_modules\AI-06-clustering-regression.md` | 2 | 58 | standalone | OK |  |
| `03_modules\AI-07-markov-viterbi.md` | 2 | 60 | standalone | OK |  |
| `03_modules\AI-07-markov-viterbi.md` | 3 | 147 | snippet | OK |  |
| `03_modules\AI-08-neural-forward-softmax.md` | 2 | 60 | standalone | OK |  |
| `03_modules\AI-08-neural-forward-softmax.md` | 3 | 137 | snippet | OK |  |
| `03_modules\AI-09-reinforcement-learning-mdp.md` | 2 | 60 | standalone | OK |  |
| `03_modules\AI-09-reinforcement-learning-mdp.md` | 3 | 115 | snippet | OK |  |
| `03_modules\AI-10-special-judge-model-strategy.md` | 2 | 64 | standalone | OK |  |
| `03_modules\AI-11-linear-svm.md` | 2 | 64 | standalone | OK |  |
| `03_modules\AI-11-linear-svm.md` | 3 | 128 | snippet | OK |  |
| `03_modules\AI-12-dnn-multilayer-forward.md` | 2 | 62 | standalone | OK |  |
| `03_modules\AI-12-dnn-multilayer-forward.md` | 3 | 148 | snippet | OK |  |
| `03_modules\AI-13-linear-regression-gd.md` | 2 | 60 | standalone | OK |  |
| `03_modules\AI-14-backpropagation.md` | 2 | 101 | standalone | OK |  |
| `03_modules\AI-14-backpropagation.md` | 3 | 200 | snippet | OK |  |
| `03_modules\AI-15-reverse-mode-autodiff.md` | 2 | 85 | standalone | OK |  |
| `03_modules\AI-15-reverse-mode-autodiff.md` | 3 | 198 | snippet | OK |  |
| `03_modules\BASIC-00-control-flow.md` | 2 | 116 | standalone | OK |  |
| `03_modules\BRUTE-00-partial-score-strategy.md` | 1 | 74 | snippet | OK |  |
| `03_modules\BRUTE-00-partial-score-strategy.md` | 2 | 108 | standalone | OK |  |
| `03_modules\BRUTE-01-complexity-cheatsheet.md` | 2 | 104 | standalone | OK |  |
| `03_modules\BRUTE-02-legal-fallback-output.md` | 1 | 59 | snippet | OK |  |
| `03_modules\BRUTE-02-legal-fallback-output.md` | 2 | 82 | standalone | OK |  |
| `03_modules\BRUTE-03-permutation-enumeration.md` | 1 | 60 | snippet | OK |  |
| `03_modules\BRUTE-03-permutation-enumeration.md` | 2 | 83 | standalone | OK |  |
| `03_modules\BRUTE-04-combination-dfs.md` | 1 | 62 | snippet | OK |  |
| `03_modules\BRUTE-04-combination-dfs.md` | 2 | 87 | standalone | OK |  |
| `03_modules\BRUTE-05-subset-enumeration.md` | 2 | 88 | standalone | OK |  |
| `03_modules\BRUTE-06-backtracking-pruning.md` | 1 | 62 | snippet | OK |  |
| `03_modules\BRUTE-06-backtracking-pruning.md` | 2 | 86 | standalone | OK |  |
| `03_modules\BRUTE-07-memoized-search-overview.md` | 1 | 70 | snippet | OK |  |
| `03_modules\BRUTE-07-memoized-search-overview.md` | 2 | 100 | standalone | OK |  |
| `03_modules\BRUTE-07-memoized-search-overview.md` | 4 | 194 | snippet | OK |  |
| `03_modules\BRUTE-08-vector-memo.md` | 1 | 62 | snippet | OK |  |
| `03_modules\BRUTE-08-vector-memo.md` | 2 | 86 | standalone | OK |  |
| `03_modules\BRUTE-09-map-tuple-memo.md` | 1 | 64 | snippet | OK |  |
| `03_modules\BRUTE-09-map-tuple-memo.md` | 2 | 86 | standalone | OK |  |
| `03_modules\BRUTE-10-unordered-map-encoded-memo.md` | 2 | 85 | standalone | OK |  |
| `03_modules\BRUTE-11-bfs-state-search.md` | 1 | 67 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_83.cpp:8:9: error: ‘State’ was not declared in this scope; did you mean ‘_xstate’?<br>    8 \| int bfs(State start, State target);<br>      \|         ^~~~~<br>      \|         _xstate<br><repo>/05_review/tmpdu19mmj0/block_83.cpp:8:22: error: ‘State’ was not declared in this scope; did you mean ‘_xstate’? |
| `03_modules\BRUTE-11-bfs-state-search.md` | 2 | 92 | standalone | OK |  |
| `03_modules\BRUTE-11-bfs-state-search.md` | 4 | 170 | standalone | OK |  |
| `03_modules\BRUTE-12-meet-in-the-middle.md` | 1 | 63 | snippet | OK |  |
| `03_modules\BRUTE-12-meet-in-the-middle.md` | 2 | 87 | standalone | OK |  |
| `03_modules\BRUTE-13-small-exact-large-special.md` | 1 | 61 | snippet | OK |  |
| `03_modules\BRUTE-13-small-exact-large-special.md` | 2 | 87 | standalone | OK |  |
| `03_modules\BRUTE-14-submission-version-route.md` | 1 | 63 | snippet | OK |  |
| `03_modules\BRUTE-14-submission-version-route.md` | 2 | 87 | standalone | OK |  |
| `03_modules\CPP-001-main-io.md` | 1 | 42 | snippet | OK |  |
| `03_modules\CPP-001-main-io.md` | 2 | 48 | snippet | OK |  |
| `03_modules\CPP-001-main-io.md` | 3 | 107 | standalone | OK |  |
| `03_modules\CPP-002-basic-containers.md` | 1 | 48 | standalone | OK |  |
| `03_modules\CPP-003-sort-bounds.md` | 1 | 42 | standalone | OK |  |
| `03_modules\CPP-003-sort-bounds.md` | 2 | 93 | snippet | OK |  |
| `03_modules\CPP-004-queues-stacks-heaps.md` | 1 | 42 | standalone | OK |  |
| `03_modules\CPP-005-associative-containers.md` | 1 | 43 | standalone | OK |  |
| `03_modules\CPP-006-bitset-bit-operations.md` | 1 | 44 | standalone | OK |  |
| `03_modules\CPP-007-coordinate-compression.md` | 1 | 43 | standalone | OK |  |
| `03_modules\CPP-008-integers-overflow.md` | 1 | 42 | standalone | OK |  |
| `03_modules\CPP-009-common-re-wa-pitfalls.md` | 1 | 42 | standalone | OK |  |
| `03_modules\CPP-011-string-reference.md` | 5 | 143 | snippet | OK |  |
| `03_modules\CPP-011-string-reference.md` | 8 | 181 | snippet | OK |  |
| `03_modules\CPP-011-string-reference.md` | 9 | 196 | snippet | OK |  |
| `03_modules\CPP-011-string-reference.md` | 13 | 246 | standalone | OK |  |
| `03_modules\CPP-011-string-reference.md` | 16 | 284 | snippet | OK |  |
| `03_modules\CPP-011-string-reference.md` | 17 | 297 | snippet | OK |  |
| `03_modules\CPP-011-string-reference.md` | 19 | 351 | snippet | OK |  |
| `03_modules\CPP-011-string-reference.md` | 20 | 362 | snippet | OK |  |
| `03_modules\CPP-011-string-reference.md` | 22 | 393 | snippet | OK |  |
| `03_modules\CPP-011-string-reference.md` | 23 | 405 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_140.cpp: In function ‘bool same_lower_multiset(const std::string&, const std::string&)’:<br><repo>/05_review/tmpdu19mmj0/block_140.cpp:9:12: error: ‘count_lower’ was not declared in this scope<br>    9 \|     return count_lower(a) == count_lower(b);<br>      \|            ^~~~~~~~~~~ |
| `03_modules\CPP-011-string-reference.md` | 24 | 415 | snippet | OK |  |
| `03_modules\CPP-011-string-reference.md` | 25 | 429 | snippet | OK |  |
| `03_modules\CPP-011-string-reference.md` | 26 | 448 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_143.cpp:9:24: error: ‘split_by_char’ was not declared in this scope<br>    9 \| vector<string> parts = split_by_char(line, ',');<br>      \|                        ^~~~~~~~~~~~~ |
| `03_modules\CPP-011-string-reference.md` | 27 | 456 | standalone | OK |  |
| `03_modules\CPP-012-stl-algorithms-reference.md` | 1 | 51 | snippet | OK |  |
| `03_modules\CPP-012-stl-algorithms-reference.md` | 8 | 157 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_152.cpp:8:11: error: ‘r’ was not declared in this scope<br>    8 \| int len = r - l;<br>      \|           ^<br><repo>/05_review/tmpdu19mmj0/block_152.cpp:8:15: error: ‘l’ was not declared in this scope; did you mean ‘ll’?<br>    8 \| int len = r - l; |
| `03_modules\CPP-012-stl-algorithms-reference.md` | 9 | 163 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_153.cpp:8:29: error: ‘v’ was not declared in this scope<br>    8 \| int pos = (int)(lower_bound(v.begin(), v.end(), x) - v.begin());<br>      \|                             ^<br><repo>/05_review/tmpdu19mmj0/block_153.cpp:8:40: error: ‘v’ was not declared in this scope<br>    8 \| int pos = (int)(lower_bound(v.begin(), v.end(), x) - v.begin()); |
| `03_modules\CPP-012-stl-algorithms-reference.md` | 16 | 224 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_160.cpp:8:26: error: ‘v’ was not declared in this scope<br>    8 \| auto range = equal_range(v.begin(), v.end(), x);<br>      \|                          ^<br><repo>/05_review/tmpdu19mmj0/block_160.cpp:8:37: error: ‘v’ was not declared in this scope<br>    8 \| auto range = equal_range(v.begin(), v.end(), x); |
| `03_modules\CPP-012-stl-algorithms-reference.md` | 19 | 252 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_163.cpp:8:14: error: ‘a’ was not declared in this scope<br>    8 \| int lo = min(a, b);<br>      \|              ^<br><repo>/05_review/tmpdu19mmj0/block_163.cpp:8:17: error: ‘b’ was not declared in this scope<br>    8 \| int lo = min(a, b); |
| `03_modules\CPP-012-stl-algorithms-reference.md` | 31 | 353 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_175.cpp:8:21: error: ‘v’ was not declared in this scope<br>    8 \| ll sum = accumulate(v.begin(), v.end(), 0LL);<br>      \|                     ^<br><repo>/05_review/tmpdu19mmj0/block_175.cpp:8:32: error: ‘v’ was not declared in this scope<br>    8 \| ll sum = accumulate(v.begin(), v.end(), 0LL); |
| `03_modules\CPP-012-stl-algorithms-reference.md` | 34 | 376 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_178.cpp:8:27: error: ‘v’ was not declared in this scope<br>    8 \| ll total_abs = accumulate(v.begin(), v.end(), 0LL, [](ll s, int x) {<br>      \|                           ^<br><repo>/05_review/tmpdu19mmj0/block_178.cpp:8:38: error: ‘v’ was not declared in this scope<br>    8 \| ll total_abs = accumulate(v.begin(), v.end(), 0LL, [](ll s, int x) { |
| `03_modules\CPP-012-stl-algorithms-reference.md` | 35 | 386 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_179.cpp:8:12: error: ‘a’ was not declared in this scope<br>    8 \| ll g = gcd(a, b);<br>      \|            ^<br><repo>/05_review/tmpdu19mmj0/block_179.cpp:8:15: error: ‘b’ was not declared in this scope<br>    8 \| ll g = gcd(a, b); |
| `03_modules\CPP-012-stl-algorithms-reference.md` | 36 | 393 | snippet | OK |  |
| `03_modules\CPP-012-stl-algorithms-reference.md` | 38 | 424 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_182.cpp:8:20: error: ‘v’ was not declared in this scope<br>    8 \| int c = (int)count(v.begin(), v.end(), x);<br>      \|                    ^<br><repo>/05_review/tmpdu19mmj0/block_182.cpp:8:31: error: ‘v’ was not declared in this scope<br>    8 \| int c = (int)count(v.begin(), v.end(), x); |
| `03_modules\CPP-012-stl-algorithms-reference.md` | 40 | 446 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_184.cpp:8:23: error: ‘v’ was not declared in this scope<br>    8 \| bool all_pos = all_of(v.begin(), v.end(), [](int x) {<br>      \|                       ^<br><repo>/05_review/tmpdu19mmj0/block_184.cpp:8:34: error: ‘v’ was not declared in this scope<br>    8 \| bool all_pos = all_of(v.begin(), v.end(), [](int x) { |
| `03_modules\CPP-012-stl-algorithms-reference.md` | 41 | 454 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_185.cpp:8:24: error: ‘v’ was not declared in this scope<br>    8 \| bool has_even = any_of(v.begin(), v.end(), [](int x) {<br>      \|                        ^<br><repo>/05_review/tmpdu19mmj0/block_185.cpp:8:35: error: ‘v’ was not declared in this scope<br>    8 \| bool has_even = any_of(v.begin(), v.end(), [](int x) { |
| `03_modules\CPP-012-stl-algorithms-reference.md` | 42 | 472 | standalone | OK |  |
| `03_modules\CPP-013-stl-containers-reference.md` | 1 | 77 | standalone | OK |  |
| `03_modules\CPP-013-stl-containers-reference.md` | 11 | 351 | standalone | OK |  |
| `03_modules\CPP-10-io-formatting.md` | 3 | 164 | standalone | OK |  |
| `03_modules\CPP-10-io-formatting.md` | 8 | 239 | standalone | OK |  |
| `03_modules\CPP-10-io-formatting.md` | 12 | 321 | standalone | OK |  |
| `03_modules\CPP-10-io-formatting.md` | 16 | 389 | standalone | OK |  |
| `03_modules\CPP-10-io-formatting.md` | 26 | 549 | snippet | OK |  |
| `03_modules\DIVIDE-00-divide-and-conquer.md` | 2 | 88 | snippet | OK |  |
| `03_modules\DIVIDE-00-divide-and-conquer.md` | 3 | 105 | standalone | OK |  |
| `03_modules\DIVIDE-00-divide-and-conquer.md` | 4 | 151 | standalone | OK |  |
| `03_modules\DP-00-total-flow.md` | 1 | 62 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_240.cpp:9:10: error: redefinition of ‘const ll LINF’<br>    9 \| const ll LINF = 4'000'000'000'000'000'000LL; // 与主骨架统一，作为 long long 无穷大哨兵<br>      \|          ^~~~<br><repo>/05_review/tmpdu19mmj0/block_240.cpp:5:10: note: ‘const ll LINF’ previously defined here<br>    5 \| const ll LINF = 4'000'000'000'000'000'000LL; |
| `03_modules\DP-03-dfs-memo-table-upgrade.md` | 1 | 55 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_242.cpp:8:8: error: ‘State’ was not declared in this scope; did you mean ‘_xstate’?<br>    8 \| ll dfs(State s);<br>      \|        ^~~~~<br>      \|        _xstate |
| `03_modules\DP-03-dfs-memo-table-upgrade.md` | 2 | 115 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_243.cpp: In function ‘ll dfs(int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_243.cpp:10:14: error: ‘n’ was not declared in this scope<br>   10 \|     if (i == n + 1) return 0;<br>      \|              ^<br><repo>/05_review/tmpdu19mmj0/block_243.cpp:14:20: error: ‘val’ was not declared in this scope |
| `03_modules\DP-03-dfs-memo-table-upgrade.md` | 3 | 129 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_244.cpp: In function ‘ll dfs(int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_244.cpp:13:14: error: ‘n’ was not declared in this scope<br>   13 \|     if (i == n + 1) return 0;<br>      \|              ^<br><repo>/05_review/tmpdu19mmj0/block_244.cpp:19:20: error: ‘val’ was not declared in this scope |
| `03_modules\DP-03-dfs-memo-table-upgrade.md` | 5 | 177 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_246.cpp: In function ‘ll dfs(int, int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_246.cpp:12:14: error: ‘n’ was not declared in this scope<br>   12 \|     if (i == n + 1) return 0;<br>      \|              ^ |
| `03_modules\DP-03B-state-dimension-router.md` | 1 | 153 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_247.cpp: In function ‘ll dfs(int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_247.cpp:9:16: error: ‘n’ was not declared in this scope; did you mean ‘yn’?<br>    9 \|     if (pos == n) return 1;<br>      \|                ^<br>      \|                yn |
| `03_modules\DP-03B-state-dimension-router.md` | 5 | 321 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_251.cpp:8:17: error: ‘leading’ was not declared in this scope; did you mean ‘nleading’?<br>    8 \| bool nleading = leading && (d == 0);<br>      \|                 ^~~~~~~<br>      \|                 nleading<br><repo>/05_review/tmpdu19mmj0/block_251.cpp:8:29: error: ‘d’ was not declared in this scope |
| `03_modules\DP-03B-state-dimension-router.md` | 8 | 442 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_254.cpp: In function ‘void dfs(int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_254.cpp:9:18: error: ‘g’ was not declared in this scope<br>    9 \|     for (int v : g[u]) {<br>      \|                  ^ |
| `03_modules\DP-03B-state-dimension-router.md` | 10 | 496 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_256.cpp: In function ‘ll dfs(int, int, int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_256.cpp:12:14: error: ‘n’ was not declared in this scope<br>   12 \|     if (i == n + 1) return (rem == 0 ? 0 : -LINF);<br>      \|              ^ |
| `03_modules\DP-04-linear-dp.md` | 1 | 55 | snippet | OK |  |
| `03_modules\DP-04-linear-dp.md` | 4 | 123 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_260.cpp: In function ‘ll dfs(int)’:<br><repo>/05_review/tmpdu19mmj0/block_260.cpp:9:13: error: ‘n’ was not declared in this scope<br>    9 \|     if (i > n) return 0;<br>      \|             ^<br><repo>/05_review/tmpdu19mmj0/block_260.cpp:11:20: error: ‘a’ was not declared in this scope |
| `03_modules\DP-04-linear-dp.md` | 5 | 134 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_261.cpp: In function ‘ll dfs(int)’:<br><repo>/05_review/tmpdu19mmj0/block_261.cpp:12:13: error: ‘n’ was not declared in this scope<br>   12 \|     if (i > n) return 0;<br>      \|             ^<br><repo>/05_review/tmpdu19mmj0/block_261.cpp:16:20: error: ‘a’ was not declared in this scope |
| `03_modules\DP-05-choose-or-skip-dp.md` | 1 | 56 | snippet | OK |  |
| `03_modules\DP-05-choose-or-skip-dp.md` | 3 | 119 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_265.cpp: In function ‘ll dfs(int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_265.cpp:10:14: error: ‘n’ was not declared in this scope<br>   10 \|     if (i == n + 1) return 0;<br>      \|              ^<br><repo>/05_review/tmpdu19mmj0/block_265.cpp:12:20: error: ‘val’ was not declared in this scope |
| `03_modules\DP-05-choose-or-skip-dp.md` | 4 | 131 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_266.cpp: In function ‘ll dfs(int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_266.cpp:13:14: error: ‘n’ was not declared in this scope<br>   13 \|     if (i == n + 1) return 0;<br>      \|              ^<br><repo>/05_review/tmpdu19mmj0/block_266.cpp:17:20: error: ‘val’ was not declared in this scope |
| `03_modules\DP-06-01-knapsack.md` | 1 | 55 | snippet | OK |  |
| `03_modules\DP-06-01-knapsack.md` | 3 | 121 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_270.cpp: In function ‘ll dfs(int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_270.cpp:10:14: error: ‘n’ was not declared in this scope<br>   10 \|     if (i == n + 1) return 0;<br>      \|              ^<br><repo>/05_review/tmpdu19mmj0/block_270.cpp:12:16: error: ‘v’ was not declared in this scope |
| `03_modules\DP-06-01-knapsack.md` | 4 | 132 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_271.cpp: In function ‘ll dfs(int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_271.cpp:13:14: error: ‘n’ was not declared in this scope<br>   13 \|     if (i == n + 1) return 0;<br>      \|              ^<br><repo>/05_review/tmpdu19mmj0/block_271.cpp:17:18: error: ‘v’ was not declared in this scope |
| `03_modules\DP-07-complete-knapsack.md` | 1 | 53 | snippet | OK |  |
| `03_modules\DP-07-complete-knapsack.md` | 3 | 114 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_276.cpp: In function ‘ll dfs(int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_276.cpp:10:14: error: ‘n’ was not declared in this scope<br>   10 \|     if (i == n + 1) return 0;<br>      \|              ^<br><repo>/05_review/tmpdu19mmj0/block_276.cpp:12:17: error: ‘w’ was not declared in this scope |
| `03_modules\DP-07-complete-knapsack.md` | 4 | 126 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_277.cpp: In function ‘ll dfs(int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_277.cpp:13:14: error: ‘n’ was not declared in this scope<br>   13 \|     if (i == n + 1) return 0;<br>      \|              ^<br><repo>/05_review/tmpdu19mmj0/block_277.cpp:17:17: error: ‘w’ was not declared in this scope |
| `03_modules\DP-08-group-knapsack.md` | 1 | 53 | snippet | OK |  |
| `03_modules\DP-08-group-knapsack.md` | 3 | 115 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_283.cpp: In function ‘ll dfs(int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_283.cpp:10:14: error: ‘G’ was not declared in this scope<br>   10 \|     if (g == G + 1) return 0;<br>      \|              ^<br><repo>/05_review/tmpdu19mmj0/block_283.cpp:12:24: error: ‘groups’ was not declared in this scope |
| `03_modules\DP-08-group-knapsack.md` | 4 | 129 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_284.cpp: In function ‘ll dfs(int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_284.cpp:13:14: error: ‘G’ was not declared in this scope<br>   13 \|     if (g == G + 1) return 0;<br>      \|              ^<br><repo>/05_review/tmpdu19mmj0/block_284.cpp:17:24: error: ‘groups’ was not declared in this scope |
| `03_modules\DP-09-lcs.md` | 1 | 53 | snippet | OK |  |
| `03_modules\DP-09-lcs.md` | 3 | 105 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_288.cpp: In function ‘int dfs(int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_288.cpp:9:14: error: ‘n’ was not declared in this scope<br>    9 \|     if (i == n \|\| j == m) return 0;<br>      \|              ^<br><repo>/05_review/tmpdu19mmj0/block_288.cpp:9:24: error: ‘m’ was not declared in this scope |
| `03_modules\DP-09-lcs.md` | 4 | 116 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_289.cpp: In function ‘int dfs(int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_289.cpp:11:14: error: ‘n’ was not declared in this scope<br>   11 \|     if (i == n \|\| j == m) return 0;<br>      \|              ^<br><repo>/05_review/tmpdu19mmj0/block_289.cpp:11:24: error: ‘m’ was not declared in this scope |
| `03_modules\DP-10-edit-distance.md` | 1 | 53 | snippet | OK |  |
| `03_modules\DP-10-edit-distance.md` | 3 | 111 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_294.cpp: In function ‘int dfs(int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_294.cpp:9:14: error: ‘n’ was not declared in this scope<br>    9 \|     if (i == n) return m - j; // 只能插入剩余字符<br>      \|              ^<br><repo>/05_review/tmpdu19mmj0/block_294.cpp:9:24: error: ‘m’ was not declared in this scope |
| `03_modules\DP-10-edit-distance.md` | 4 | 125 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_295.cpp: In function ‘int dfs(int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_295.cpp:11:14: error: ‘n’ was not declared in this scope<br>   11 \|     if (i == n) return m - j;<br>      \|              ^<br><repo>/05_review/tmpdu19mmj0/block_295.cpp:11:24: error: ‘m’ was not declared in this scope |
| `03_modules\DP-11-lis.md` | 1 | 53 | snippet | OK |  |
| `03_modules\DP-11-lis.md` | 3 | 104 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_299.cpp:8:23: error: ‘d’ was not declared in this scope<br>    8 \| auto it = lower_bound(d.begin(), d.end(), a[i]); // 严格递增<br>      \|                       ^<br><repo>/05_review/tmpdu19mmj0/block_299.cpp:8:34: error: ‘d’ was not declared in this scope<br>    8 \| auto it = lower_bound(d.begin(), d.end(), a[i]); // 严格递增 |
| `03_modules\DP-11-lis.md` | 4 | 120 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_300.cpp: In function ‘int dfs(int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_300.cpp:9:14: error: ‘n’ was not declared in this scope<br>    9 \|     if (i == n + 1) return 0;<br>      \|              ^<br><repo>/05_review/tmpdu19mmj0/block_300.cpp:11:22: error: ‘a’ was not declared in this scope |
| `03_modules\DP-11-lis.md` | 5 | 133 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_301.cpp: In function ‘int dfs(int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_301.cpp:11:14: error: ‘n’ was not declared in this scope<br>   11 \|     if (i == n + 1) return 0;<br>      \|              ^<br><repo>/05_review/tmpdu19mmj0/block_301.cpp:15:22: error: ‘a’ was not declared in this scope |
| `03_modules\DP-12-grid-dp.md` | 1 | 53 | snippet | OK |  |
| `03_modules\DP-12-grid-dp.md` | 4 | 113 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_307.cpp: In function ‘ll dfs(int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_307.cpp:9:13: error: ‘n’ was not declared in this scope<br>    9 \|     if (i > n \|\| j > m \|\| blocked[i][j]) return 0;<br>      \|             ^<br><repo>/05_review/tmpdu19mmj0/block_307.cpp:9:22: error: ‘m’ was not declared in this scope |
| `03_modules\DP-12-grid-dp.md` | 5 | 123 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_308.cpp: In function ‘ll dfs(int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_308.cpp:15:13: error: ‘n’ was not declared in this scope<br>   15 \|     if (i > n \|\| j > m \|\| blocked[i][j]) return 0;<br>      \|             ^<br><repo>/05_review/tmpdu19mmj0/block_308.cpp:15:22: error: ‘m’ was not declared in this scope |
| `03_modules\DP-13-interval-dp.md` | 1 | 55 | snippet | OK |  |
| `03_modules\DP-13-interval-dp.md` | 4 | 117 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_314.cpp: In function ‘ll dfs(int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_314.cpp:12:52: error: ‘sum’ was not declared in this scope<br>   12 \|         ans = min(ans, dfs(l, k) + dfs(k + 1, r) + sum(l, r));<br>      \|                                                    ^~~ |
| `03_modules\DP-13-interval-dp.md` | 5 | 130 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_315.cpp: In function ‘ll dfs(int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_315.cpp:17:52: error: ‘sum’ was not declared in this scope<br>   17 \|         ans = min(ans, dfs(l, k) + dfs(k + 1, r) + sum(l, r));<br>      \|                                                    ^~~ |
| `03_modules\DP-14-tree-dp.md` | 1 | 56 | snippet | OK |  |
| `03_modules\DP-14-tree-dp.md` | 5 | 137 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_321.cpp: In function ‘ll brute(int, int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_321.cpp:10:18: error: ‘g’ was not declared in this scope<br>   10 \|     for (int v : g[u]) if (v != p) ans0 += brute(v, u, 0);<br>      \|                  ^<br><repo>/05_review/tmpdu19mmj0/block_321.cpp:14:16: error: ‘w’ was not declared in this scope |
| `03_modules\DP-14-tree-dp.md` | 6 | 155 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_322.cpp: In function ‘ll dfs_memo(int, int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_322.cpp:16:18: error: ‘g’ was not declared in this scope<br>   16 \|     for (int v : g[u]) if (v != p) ans0 += dfs_memo(v, u, 0);<br>      \|                  ^<br><repo>/05_review/tmpdu19mmj0/block_322.cpp:20:16: error: ‘w’ was not declared in this scope |
| `03_modules\DP-15-dag-dp.md` | 1 | 58 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_324.cpp:8:29: error: ‘Graph’ does not name a type<br>    8 \| vector<int> topo_sort(const Graph& G);<br>      \|                             ^~~~~ |
| `03_modules\DP-15-dag-dp.md` | 5 | 138 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_328.cpp: In function ‘ll dfs(int)’:<br><repo>/05_review/tmpdu19mmj0/block_328.cpp:9:14: error: ‘t’ was not declared in this scope<br>    9 \|     if (u == t) return 0;<br>      \|              ^<br><repo>/05_review/tmpdu19mmj0/block_328.cpp:11:24: error: ‘g’ was not declared in this scope |
| `03_modules\DP-15-dag-dp.md` | 6 | 152 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_329.cpp: In function ‘ll dfs(int)’:<br><repo>/05_review/tmpdu19mmj0/block_329.cpp:12:14: error: ‘t’ was not declared in this scope<br>   12 \|     if (u == t) return 0;<br>      \|              ^<br><repo>/05_review/tmpdu19mmj0/block_329.cpp:16:24: error: ‘g’ was not declared in this scope |
| `03_modules\DP-16-bitmask-dp.md` | 2 | 77 | snippet | OK |  |
| `03_modules\DP-16-bitmask-dp.md` | 4 | 135 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_334.cpp: In function ‘ll dfs(int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_334.cpp:9:17: error: ‘full’ was not declared in this scope; did you mean ‘fmull’?<br>    9 \|     if (mask == full) return 0;<br>      \|                 ^~~~<br>      \|                 fmull |
| `03_modules\DP-16-bitmask-dp.md` | 5 | 151 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_335.cpp:8:9: error: ‘SMAX’ was not declared in this scope<br>    8 \| ll memo[SMAX][KMAX + 1];<br>      \|         ^~~~<br><repo>/05_review/tmpdu19mmj0/block_335.cpp:8:15: error: ‘KMAX’ was not declared in this scope<br>    8 \| ll memo[SMAX][KMAX + 1]; |
| `03_modules\DP-17-digit-dp.md` | 1 | 53 | snippet | OK |  |
| `03_modules\DP-17-digit-dp.md` | 3 | 108 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_339.cpp: In function ‘ll dfs_plain(int, bool, bool, int)’:<br><repo>/05_review/tmpdu19mmj0/block_339.cpp:10:16: error: ‘len’ was not declared in this scope<br>   10 \|     if (pos == len) return ((!leading \|\| count_zero) && sum % K == 0) ? 1 : 0;<br>      \|                ^~~<br><repo>/05_review/tmpdu19mmj0/block_339.cpp:10:63: error: ‘K’ was not declared in this scope |
| `03_modules\DP-17-digit-dp.md` | 4 | 126 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_340.cpp: In function ‘ll dfs(int, bool, bool, int)’:<br><repo>/05_review/tmpdu19mmj0/block_340.cpp:15:16: error: ‘len’ was not declared in this scope<br>   15 \|     if (pos == len) return ((!leading \|\| count_zero) && sum % K == 0) ? 1 : 0;<br>      \|                ^~~<br><repo>/05_review/tmpdu19mmj0/block_340.cpp:15:63: error: ‘K’ was not declared in this scope |
| `03_modules\DP-17-digit-dp.md` | 5 | 168 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_341.cpp: In function ‘ll solve_string(const std::string&)’:<br><repo>/05_review/tmpdu19mmj0/block_341.cpp:9:5: error: ‘digits’ was not declared in this scope<br>    9 \|     digits.clear();<br>      \|     ^~~~~~<br><repo>/05_review/tmpdu19mmj0/block_341.cpp:11:5: error: ‘len’ was not declared in this scope |
| `03_modules\DP-18-dp-with-data-structure-optimization.md` | 4 | 154 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_346.cpp: In function ‘ll dfs(int)’:<br><repo>/05_review/tmpdu19mmj0/block_346.cpp:9:9: error: ‘vis’ was not declared in this scope<br>    9 \|     if (vis[i]) return memo[i];<br>      \|         ^~~<br><repo>/05_review/tmpdu19mmj0/block_346.cpp:9:24: error: ‘memo’ was not declared in this scope |
| `03_modules\DP-18-dp-with-data-structure-optimization.md` | 5 | 168 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_347.cpp:8:17: error: ‘n’ was not declared in this scope; did you mean ‘yn’?<br>    8 \| vector<ll> memo(n + 1);<br>      \|                 ^<br>      \|                 yn<br><repo>/05_review/tmpdu19mmj0/block_347.cpp:9:17: error: ‘n’ was not declared in this scope; did you mean ‘yn’? |
| `03_modules\DP-19-model-composition-recipes.md` | 2 | 190 | snippet | OK |  |
| `03_modules\DP-19-model-composition-recipes.md` | 10 | 557 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_359.cpp: In function ‘ll dfs(int, bool, bool, int)’:<br><repo>/05_review/tmpdu19mmj0/block_359.cpp:9:16: error: ‘len’ was not declared in this scope<br>    9 \|     if (pos == len) {<br>      \|                ^~~<br><repo>/05_review/tmpdu19mmj0/block_359.cpp:14:19: error: ‘vis’ was not declared in this scope |
| `03_modules\DP-20-count-feasibility-dp.md` | 1 | 61 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_361.cpp:8:10: error: conflicting declaration ‘const ll MOD’<br>    8 \| const ll MOD = 1000000007LL;<br>      \|          ^~~<br><repo>/05_review/tmpdu19mmj0/block_361.cpp:6:11: note: previous declaration as ‘const int MOD’<br>    6 \| const int MOD = 1000000007; |
| `03_modules\DP-20-count-feasibility-dp.md` | 2 | 124 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_362.cpp:9:10: error: conflicting declaration ‘const ll MOD’<br>    9 \| const ll MOD = 1000000007LL;<br>      \|          ^~~<br><repo>/05_review/tmpdu19mmj0/block_362.cpp:6:11: note: previous declaration as ‘const int MOD’<br>    6 \| const int MOD = 1000000007; |
| `03_modules\DP-21-p1874-modeling-example.md` | 3 | 232 | standalone | OK |  |
| `03_modules\DP-21-p1874-modeling-example.md` | 5 | 306 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_384.cpp:11:11: error: redefinition of ‘const int INF’<br>   11 \| const int INF = 1000000000;<br>      \|           ^~~<br><repo>/05_review/tmpdu19mmj0/block_384.cpp:4:11: note: ‘const int INF’ previously defined here<br>    4 \| const int INF = 1000000000; |
| `03_modules\DP-22-edit-distance-modeling-example.md` | 4 | 238 | standalone | OK |  |
| `03_modules\DP-22-edit-distance-modeling-example.md` | 6 | 323 | snippet | OK |  |
| `03_modules\DP-23-lis-lcs-variants.md` | 1 | 65 | snippet | OK |  |
| `03_modules\DP-23-lis-lcs-variants.md` | 2 | 134 | snippet | OK |  |
| `03_modules\DP-23-lis-lcs-variants.md` | 3 | 160 | snippet | OK |  |
| `03_modules\DP-23-lis-lcs-variants.md` | 4 | 194 | snippet | OK |  |
| `03_modules\DP-23-lis-lcs-variants.md` | 5 | 218 | snippet | OK |  |
| `03_modules\DP-23-lis-lcs-variants.md` | 6 | 252 | snippet | OK |  |
| `03_modules\DP-23-lis-lcs-variants.md` | 7 | 291 | snippet | OK |  |
| `03_modules\DP-23-lis-lcs-variants.md` | 8 | 315 | snippet | OK |  |
| `03_modules\DP-23-lis-lcs-variants.md` | 9 | 346 | snippet | OK |  |
| `03_modules\DP-23-lis-lcs-variants.md` | 10 | 379 | snippet | OK |  |
| `03_modules\DP-24-knapsack-variants.md` | 1 | 64 | snippet | OK |  |
| `03_modules\DP-24-knapsack-variants.md` | 2 | 134 | snippet | OK |  |
| `03_modules\DP-24-knapsack-variants.md` | 4 | 186 | snippet | OK |  |
| `03_modules\DP-24-knapsack-variants.md` | 8 | 258 | snippet | OK |  |
| `03_modules\DP-24-knapsack-variants.md` | 9 | 283 | snippet | OK |  |
| `03_modules\DP-25-dfs-memo-case-strategy.md` | 1 | 124 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_410.cpp:8:12: error: ‘pos’ was not declared in this scope; did you mean ‘pow’?<br>    8 \| int add = (pos == 0 ? 0 : 1);<br>      \|            ^~~<br>      \|            pow |
| `03_modules\DP-25-dfs-memo-case-strategy.md` | 2 | 130 | standalone | OK |  |
| `03_modules\DP-25-dfs-memo-case-strategy.md` | 3 | 223 | standalone | OK |  |
| `03_modules\DP-25-dfs-memo-case-strategy.md` | 4 | 324 | snippet | OK |  |
| `03_modules\DP-26-aftereffect-state-augmentation.md` | 1 | 155 | standalone | OK |  |
| `03_modules\DP-26-aftereffect-state-augmentation.md` | 2 | 257 | standalone | OK |  |
| `03_modules\DP-26-aftereffect-state-augmentation.md` | 3 | 335 | standalone | OK |  |
| `03_modules\DP-26-aftereffect-state-augmentation.md` | 4 | 409 | standalone | OK |  |
| `03_modules\DP-26-aftereffect-state-augmentation.md` | 5 | 510 | standalone | OK |  |
| `03_modules\DS-00-data-structure-routing.md` | 2 | 120 | snippet | OK |  |
| `03_modules\DS-01-prefix-difference.md` | 2 | 77 | snippet | OK |  |
| `03_modules\DS-02-tree-array-compressor.md` | 2 | 90 | snippet | OK |  |
| `03_modules\DS-03-segtree-sparse.md` | 2 | 84 | snippet | OK |  |
| `03_modules\DS-04-monotonic-dsu.md` | 2 | 84 | snippet | OK |  |
| `03_modules\DS-05-advanced-segtree.md` | 2 | 95 | snippet | OK |  |
| `03_modules\DS-05-advanced-segtree.md` | 3 | 189 | standalone | OK |  |
| `03_modules\DS-05-advanced-segtree.md` | 4 | 281 | snippet | OK |  |
| `03_modules\DS-06-two-pointers-sliding-window.md` | 3 | 110 | snippet | OK |  |
| `03_modules\DS-06-two-pointers-sliding-window.md` | 5 | 140 | snippet | OK |  |
| `03_modules\DS-06-two-pointers-sliding-window.md` | 6 | 163 | snippet | OK |  |
| `03_modules\DS-06-two-pointers-sliding-window.md` | 8 | 191 | snippet | OK |  |
| `03_modules\DS-06-two-pointers-sliding-window.md` | 10 | 216 | snippet | OK |  |
| `03_modules\DS-06-two-pointers-sliding-window.md` | 11 | 240 | snippet | OK |  |
| `03_modules\DS-07-stl-first-data-structures.md` | 2 | 106 | standalone | OK |  |
| `03_modules\GRAPH-00-standard-graph.md` | 2 | 95 | snippet | OK |  |
| `03_modules\GRAPH-01-dfs-bfs-connectivity.md` | 2 | 87 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_458.cpp:8:29: error: ‘Graph’ does not name a type<br>    8 \| vector<int> bfs_order(const Graph &G, int s) {<br>      \|                             ^~~~~<br><repo>/05_review/tmpdu19mmj0/block_458.cpp: In function ‘std::vector<int> bfs_order(const int&, int)’:<br><repo>/05_review/tmpdu19mmj0/block_458.cpp:9:23: error: request for member ‘n’ in ‘G’, which is of non-class type ‘const int’ |
| `03_modules\GRAPH-05-topo-dag-dp.md` | 2 | 91 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_470.cpp:8:29: error: ‘Graph’ does not name a type<br>    8 \| vector<int> topo_sort(const Graph &G) {<br>      \|                             ^~~~~<br><repo>/05_review/tmpdu19mmj0/block_470.cpp: In function ‘std::vector<int> topo_sort(const int&)’:<br><repo>/05_review/tmpdu19mmj0/block_470.cpp:9:21: error: request for member ‘edges’ in ‘G’, which is of non-class type ‘const int’ |
| `03_modules\GRAPH-09-tree-dfs-lca.md` | 2 | 93 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_482.cpp:15:22: error: ‘Graph’ does not name a type<br>   15 \|     void build(const Graph &G, int root_ = 1) {<br>      \|                      ^~~~~<br><repo>/05_review/tmpdu19mmj0/block_482.cpp: In member function ‘void LCA::build(const int&, int)’:<br><repo>/05_review/tmpdu19mmj0/block_482.cpp:17:15: error: request for member ‘n’ in ‘G’, which is of non-class type ‘const int’ |
| `03_modules\GRAPH-10-dinic-low-priority.md` | 2 | 84 | snippet | OK |  |
| `03_modules\GRAPH-11-graph-tree-partial-score-playbook.md` | 2 | 129 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_488.cpp:11:24: error: ‘Graph’ does not name a type<br>   11 \| void floyd_small(const Graph& G) {<br>      \|                        ^~~~~<br><repo>/05_review/tmpdu19mmj0/block_488.cpp: In function ‘void floyd_small(const int&)’:<br><repo>/05_review/tmpdu19mmj0/block_488.cpp:12:15: error: request for member ‘n’ in ‘G’, which is of non-class type ‘const int’ |
| `03_modules\GRAPH-11-graph-tree-partial-score-playbook.md` | 3 | 159 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_489.cpp:8:25: error: ‘Graph’ does not name a type<br>    8 \| int bfs_one_query(const Graph& G, int s, int t) {<br>      \|                         ^~~~~<br><repo>/05_review/tmpdu19mmj0/block_489.cpp: In function ‘int bfs_one_query(const int&, int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_489.cpp:9:24: error: request for member ‘n’ in ‘G’, which is of non-class type ‘const int’ |
| `03_modules\GRAPH-11-graph-tree-partial-score-playbook.md` | 4 | 190 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_490.cpp:8:34: error: ‘FullEdge’ was not declared in this scope<br>    8 \| ll brute_mst_edges(int n, vector<FullEdge>& edges) {<br>      \|                                  ^~~~~~~~<br><repo>/05_review/tmpdu19mmj0/block_490.cpp:8:42: error: template argument 1 is invalid<br>    8 \| ll brute_mst_edges(int n, vector<FullEdge>& edges) { |
| `03_modules\GRAPH-11-graph-tree-partial-score-playbook.md` | 5 | 220 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_491.cpp:8:30: error: ‘Graph’ does not name a type<br>    8 \| bool dfs_path_distance(const Graph& T, int u, int p, int target, ll cur, ll& ans) {<br>      \|                              ^~~~~<br><repo>/05_review/tmpdu19mmj0/block_491.cpp: In function ‘bool dfs_path_distance(const int&, int, int, int, ll, ll&)’:<br><repo>/05_review/tmpdu19mmj0/block_491.cpp:13:21: error: request for member ‘g’ in ‘T’, which is of non-class type ‘const int’ |
| `03_modules\GRAPH-11-graph-tree-partial-score-playbook.md` | 6 | 243 | snippet | OK |  |
| `03_modules\GRAPH-12-01bfs-layered-shortest.md` | 2 | 64 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_494.cpp:8:31: error: ‘Graph’ does not name a type<br>    8 \| vector<ll> zero_one_bfs(const Graph& G, int s);<br>      \|                               ^~~~~<br><repo>/05_review/tmpdu19mmj0/block_494.cpp:9:38: error: ‘Graph’ does not name a type<br>    9 \| bool shortest_with_free_passes(const Graph& G, int s, int k); |
| `03_modules\GRAPH-12-01bfs-layered-shortest.md` | 3 | 89 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_495.cpp:8:31: error: ‘Graph’ does not name a type<br>    8 \| vector<ll> zero_one_bfs(const Graph &G, int s) {<br>      \|                               ^~~~~<br><repo>/05_review/tmpdu19mmj0/block_495.cpp: In function ‘std::vector<long long int> zero_one_bfs(const int&, int)’:<br><repo>/05_review/tmpdu19mmj0/block_495.cpp:9:23: error: request for member ‘n’ in ‘G’, which is of non-class type ‘const int’ |
| `03_modules\GREEDY-00-routing.md` | 2 | 115 | standalone | OK |  |
| `03_modules\GREEDY-01-greedy-vs-dp.md` | 1 | 191 | snippet | OK |  |
| `03_modules\GREEDY-02-common-models.md` | 1 | 90 | snippet | OK |  |
| `03_modules\GREEDY-02-common-models.md` | 2 | 131 | snippet | OK |  |
| `03_modules\GREEDY-02-common-models.md` | 3 | 157 | snippet | OK |  |
| `03_modules\GREEDY-02-common-models.md` | 4 | 187 | snippet | OK |  |
| `03_modules\GREEDY-02-common-models.md` | 5 | 246 | snippet | OK |  |
| `03_modules\MATH-01-gcd-lcm.md` | 2 | 96 | snippet | OK |  |
| `03_modules\MATH-02-fast-power-mod-arithmetic.md` | 2 | 93 | snippet | OK |  |
| `03_modules\MATH-03-inverse-combination.md` | 2 | 107 | snippet | OK |  |
| `03_modules\MATH-04-sieve-factorization.md` | 2 | 98 | snippet | OK |  |
| `03_modules\MATH-05-matrix-fast-power.md` | 3 | 160 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_524.cpp: In function ‘ll fib(ll, ll)’:<br><repo>/05_review/tmpdu19mmj0/block_524.cpp:12:5: error: ‘Matrix’ was not declared in this scope<br>   12 \|     Matrix T(2, mod);<br>      \|     ^~~~~~<br><repo>/05_review/tmpdu19mmj0/block_524.cpp:13:5: error: ‘T’ was not declared in this scope |
| `03_modules\MATH-06-inclusion-exclusion.md` | 2 | 97 | snippet | OK |  |
| `03_modules\MATH-LA-00-linear-algebra.md` | 3 | 133 | snippet | OK |  |
| `03_modules\MATH-LA-00-linear-algebra.md` | 4 | 193 | snippet | OK |  |
| `03_modules\MATH-LA-00-linear-algebra.md` | 5 | 278 | snippet | OK |  |
| `03_modules\MATHREF-01-divisibility-congruence.md` | 1 | 54 | snippet | OK |  |
| `03_modules\MATHREF-01-divisibility-congruence.md` | 2 | 135 | snippet | OK |  |
| `03_modules\MATHREF-02-egcd-inverse-crt.md` | 1 | 56 | snippet | OK |  |
| `03_modules\MATHREF-02-egcd-inverse-crt.md` | 2 | 142 | snippet | OK |  |
| `03_modules\MATHREF-02-egcd-inverse-crt.md` | 3 | 261 | snippet | OK |  |
| `03_modules\MATHREF-03-prime-factor-euler-mobius.md` | 1 | 49 | snippet | OK |  |
| `03_modules\MATHREF-03-prime-factor-euler-mobius.md` | 2 | 143 | snippet | OK |  |
| `03_modules\MATHREF-03-prime-factor-euler-mobius.md` | 3 | 234 | snippet | OK |  |
| `03_modules\MATHREF-04-combinatorics-counting.md` | 1 | 56 | snippet | OK |  |
| `03_modules\MATHREF-04-combinatorics-counting.md` | 2 | 121 | snippet | OK |  |
| `03_modules\MATHREF-04-combinatorics-counting.md` | 3 | 218 | snippet | OK |  |
| `03_modules\MATHREF-04-combinatorics-counting.md` | 4 | 283 | snippet | OK |  |
| `03_modules\MATHREF-04-combinatorics-counting.md` | 5 | 352 | snippet | OK |  |
| `03_modules\MATHREF-05-recurrence-probability-game.md` | 2 | 142 | snippet | OK |  |
| `03_modules\MATHREF-05-recurrence-probability-game.md` | 3 | 161 | snippet | OK |  |
| `03_modules\MATHREF-05-recurrence-probability-game.md` | 4 | 233 | snippet | OK |  |
| `03_modules\MATHREF-06-geometry-numeric-modeling.md` | 2 | 148 | snippet | OK |  |
| `03_modules\OPS-00-unified-protocols.md` | 1 | 63 | standalone | OK |  |
| `03_modules\OPS-00-unified-protocols.md` | 2 | 139 | snippet | OK |  |
| `03_modules\OPS-00-unified-protocols.md` | 3 | 164 | snippet | OK |  |
| `03_modules\OPS-00-unified-protocols.md` | 7 | 273 | snippet | OK |  |
| `03_modules\OPS-00-unified-protocols.md` | 8 | 299 | snippet | OK |  |
| `03_modules\OPS-00-unified-protocols.md` | 10 | 351 | snippet | OK |  |
| `03_modules\OPS-00-unified-protocols.md` | 12 | 385 | snippet | OK |  |
| `03_modules\OPS-00-unified-protocols.md` | 14 | 455 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_566.cpp: In function ‘ll dfs(int, int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_566.cpp:11:14: error: ‘n’ was not declared in this scope<br>   11 \|     if (i == n + 1) return 0; // base case 按题意替换<br>      \|              ^ |
| `03_modules\OPS-01-exam-operations.md` | 1 | 149 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_568.cpp: In function ‘void solve()’:<br><repo>/05_review/tmpdu19mmj0/block_568.cpp:9:5: error: ‘read_input’ was not declared in this scope; did you mean ‘readlinkat’?<br>    9 \|     read_input();<br>      \|     ^~~~~~~~~~<br>      \|     readlinkat |
| `03_modules\ROUTE-01-assembly-recipes.md` | 3 | 193 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_571.cpp: In function ‘void range_add(int, int, ll)’:<br><repo>/05_review/tmpdu19mmj0/block_571.cpp:9:5: error: ‘fw’ was not declared in this scope<br>    9 \|     fw.add(l, x);<br>      \|     ^~<br><repo>/05_review/tmpdu19mmj0/block_571.cpp:10:18: error: ‘n’ was not declared in this scope |
| `03_modules\ROUTE-01-assembly-recipes.md` | 15 | 724 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_583.cpp: In function ‘ll dfs(int, int, int)’:<br><repo>/05_review/tmpdu19mmj0/block_583.cpp:11:9: error: ‘memo’ was not declared in this scope<br>   11 \|     if (memo.count(key)) return memo[key];<br>      \|         ^~~~<br><repo>/05_review/tmpdu19mmj0/block_583.cpp:12:14: error: ‘n’ was not declared in this scope |
| `03_modules\SIM-01-high-precision.md` | 2 | 105 | standalone | OK |  |
| `03_modules\SIM-02-big-integer-class.md` | 2 | 123 | standalone | OK |  |
| `03_modules\SIM-03-expression-ast.md` | 2 | 116 | standalone | OK |  |
| `03_modules\SIM-04-json-csv-ini-parsers.md` | 2 | 94 | standalone | OK |  |
| `03_modules\SIM-05-mini-interpreter.md` | 1 | 56 | snippet | OK |  |
| `03_modules\SIM-05-mini-interpreter.md` | 2 | 98 | standalone | OK |  |
| `03_modules\STR-02-kmp-z.md` | 2 | 97 | snippet | OK |  |
| `03_modules\STR-03-trie-rolling-hash.md` | 2 | 110 | snippet | OK |  |
| `03_modules\STR-04-ac-automaton-low-priority.md` | 2 | 88 | snippet | OK |  |
| `03_modules\STR-04-ac-automaton-low-priority.md` | 3 | 190 | standalone | OK |  |
| `03_modules\STR-05-manacher.md` | 2 | 84 | snippet | OK |  |
| `03_modules\STR-05-manacher.md` | 3 | 158 | standalone | OK |  |
| `03_modules\STR-05-manacher.md` | 4 | 219 | standalone | OK |  |
| `03_modules\STR-05-manacher.md` | 6 | 309 | snippet | OK |  |
| `03_modules\TREE-00-binary-tree.md` | 2 | 92 | standalone | OK |  |
| `03_modules\TREE-00-binary-tree.md` | 3 | 252 | standalone | OK |  |
| `03_modules\TREE-02-diameter-reroot-diff.md` | 2 | 64 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_633.cpp:8:35: error: ‘Graph’ does not name a type<br>    8 \| pair<int, ll> farthest_from(const Graph& T, int s);<br>      \|                                   ^~~~~<br><repo>/05_review/tmpdu19mmj0/block_633.cpp:9:31: error: ‘Graph’ does not name a type<br>    9 \| ll tree_diameter_length(const Graph& T); |
| `03_modules\TREE-02-diameter-reroot-diff.md` | 3 | 93 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_634.cpp:8:35: error: ‘Graph’ does not name a type<br>    8 \| pair<int, ll> farthest_from(const Graph &T, int s) {<br>      \|                                   ^~~~~<br><repo>/05_review/tmpdu19mmj0/block_634.cpp: In function ‘std::pair<int, long long int> farthest_from(const int&, int)’:<br><repo>/05_review/tmpdu19mmj0/block_634.cpp:9:23: error: request for member ‘n’ in ‘T’, which is of non-class type ‘const int’ |
| `03_modules\TREE-02-diameter-reroot-diff.md` | 4 | 169 | snippet | CONTEXT | <repo>/05_review/tmpdu19mmj0/block_635.cpp:8:37: error: ‘Graph’ does not name a type<br>    8 \| vector<ll> vertex_path_counts(const Graph &T, const vector<pair<int, int>> &queries, const LCA &lca) {<br>      \|                                     ^~~~~<br><repo>/05_review/tmpdu19mmj0/block_635.cpp:8:92: error: ‘LCA’ does not name a type<br>    8 \| vector<ll> vertex_path_counts(const Graph &T, const vector<pair<int, int>> &queries, const LCA &lca) { |
