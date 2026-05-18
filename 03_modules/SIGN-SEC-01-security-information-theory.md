# SIGN-SEC-01 信息安全、校验、压缩与信息论常识

模块编号：SIGN-SEC-01

模块名称：信息安全、哈希、校验、压缩和信息论基础

标签：签到题、信息安全、哈希、校验和、压缩、熵、编码、CRC、C++17

一句话用途：遇到校验码、哈希、加密、压缩率、熵、错误检测等常识题时，用本模块快速查概念和小公式。

题面触发词：校验和、奇偶校验、CRC、哈希、MD5、SHA、加密、压缩率、熵、Huffman、错误检测。

什么时候用：

- 题目考概念判断：哈希 vs 加密，压缩 vs 编码。
- 题目要求计算简单校验和、奇偶校验、压缩率。
- 题目给频率，要求估算信息熵或 Huffman 直觉。

不要什么时候用：

- 不要自己实现真实密码算法，考试一般不会要求。
- 如果题目给了具体编码树，按题面模拟，不要套概念。
- 大规模字符串哈希算法题翻字符串卷。

复杂度：

- 简单校验：`O(n)`。
- 频率统计：`O(n)`。
- Huffman 建树：`O(k log k)`。

依赖的标准容器：`string`、`vector<int>`、`priority_queue`、`map`。

输入如何整理：

```text
先确认处理单位是 bit、byte 还是字符。
压缩率常见写法：
compressed / original 或 (original-compressed)/original，按题面。
```

接口：

```text
xor_checksum(s) -> 异或校验。
parity(x) -> 二进制 1 的个数奇偶。
entropy(freq) -> 信息熵。
```

常见坑：

- 哈希不是加密；哈希通常不可逆，加密应可用密钥解密。
- 编码不是压缩；Base64 反而会变大。
- 压缩后大小可能因为头部信息而变大。
- 奇偶校验只能检测奇数个位错误，不一定能纠错。

暴力/部分分替代：

- 复杂 CRC 不会时，先按题面给的小规则逐位模拟。
- Huffman 不会时，小数据可以枚举树形很难，优先掌握优先队列贪心。

## 1. 概念区分

| 概念 | 目的 | 是否可逆 |
|---|---|---|
| 编码 | 表示数据 | 通常可逆 |
| 压缩 | 减少大小 | 无损可逆，有损不可完全恢复 |
| 哈希 | 摘要/查找/完整性 | 通常不可逆 |
| 加密 | 保密 | 有密钥可逆 |
| 签名 | 证明身份和完整性 | 验证可行，不是解密 |
| 校验 | 检测错误 | 通常不能恢复 |

## 2. 校验短代码

```cpp
int parity_ones(unsigned int x) {
    return __builtin_popcount(x) & 1;
}

unsigned char xor_checksum(const string &s) {
    unsigned char ans = 0;
    for (unsigned char c : s) ans ^= c;
    return ans;
}

int digit_sum_mod10(const string &s) {
    int sum = 0;
    for (char c : s) if (isdigit((unsigned char)c)) sum = (sum + c - '0') % 10;
    return sum;
}
```

## 3. 压缩和熵

信息熵：

```text
H = -sum p_i * log2(p_i)
```

直觉：

- 越均匀，熵越大。
- 越集中，越容易压缩。
- Huffman 编码给高频字符更短码。

```cpp
double entropy_from_counts(const vector<int> &cnt) {
    double total = 0;
    for (int x : cnt) total += x;
    double h = 0;
    for (int x : cnt) {
        if (x == 0) continue;
        double p = x / total;
        h -= p * log2(p);
    }
    return h;
}
```

## 4. 常见压缩率

| 问法 | 公式 |
|---|---|
| 压缩后占原来的比例 | `compressed/original` |
| 压缩率减少了多少 | `(original-compressed)/original` |
| 压缩倍数 | `original/compressed` |
| Base64 大小 | 约 `ceil(n/3)*4` byte |

