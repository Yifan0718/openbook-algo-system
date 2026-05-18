# SIGN-CS-01 计算机常识、编码、文件和网络

模块编号：SIGN-CS-01

模块名称：计算机基础常识：存储单位、编码、文件大小、网络和格式

标签：签到题、计算机常识、bit、byte、ASCII、UTF-8、BMP、音频、视频、网络、C++17

一句话用途：遇到文件大小、图片音视频、进制编码、IP、带宽、ASCII/UTF-8 等题时，用本模块先统一单位再计算。

题面触发词：bit、byte、KB、KiB、BMP、RGB、RGBA、采样率、码率、ASCII、UTF-8、IPv4、CIDR、Base64、URL 编码。

什么时候用：

- 题目问内存、文件大小、传输时间、编码转换。
- 输入是图片/音频/视频参数，要求估算容量。
- 题目考二进制、十六进制、补码、校验和。

不要什么时候用：

- 复杂文件格式解析，优先 `SIM-04`。
- 真正图像算法如卷积、滤波，优先按矩阵/模拟题处理。
- 网络协议细节题若题面另给规则，以题面为准。

复杂度：

- 单个换算 `O(1)`。
- 字符串编码扫描 `O(len)`。
- IP/CIDR 解析 `O(len)`。

依赖的标准容器：`string`、`vector<int>`、`sstream`、`iomanip`。

输入如何整理：

```text
先看单位：bit 还是 byte，KB 还是 KiB，bps 还是 B/s。
图片先看每像素位数和行对齐。
网络传输先把带宽转成 byte/s。
```

接口：

```text
bmp_size(width,height,bits) -> BMP 像素数据字节数，按 4 字节行对齐。
ipv4_to_int(s) -> IPv4 转 32 位整数。
base_convert(s,base) -> 小范围进制转十进制。
```

常见坑：

- 1 byte = 8 bit。
- `Mbps` 是百万 bit/s，不是 MB/s。
- BMP 24 位图每像素 3 byte，但每行要补到 4 的倍数。
- UTF-8 中文通常占 3 byte，不等于字符个数。
- 十六进制字符 `A-F` 可大小写。

暴力/部分分替代：

- 编码规则复杂时，先处理 ASCII 和题面出现的字符。
- BMP 若忘记行对齐，先交 `w*h*bytes` 可能拿部分分。
- IP/CIDR 不熟时，小范围直接字符串分段比较。

## 1. 单位表

| 单位 | 含义 |
|---|---|
| bit | 位 |
| byte / B | 字节，`1B=8bit` |
| KB | 常见十进制 `1000B`，看题面 |
| KiB | `1024B` |
| MB | `1000^2B`，看题面 |
| MiB | `1024^2B` |
| bps | bit per second |
| B/s | byte per second |

下载时间：

```text
seconds = file_bytes * 8 / bandwidth_bps
```

## 2. BMP 和媒体大小

```cpp
long long bmp_pixel_bytes(long long width, long long height, int bits_per_pixel) {
    long long row_bits = width * bits_per_pixel;
    long long row_bytes = ((row_bits + 31) / 32) * 4; // BMP 行 4 字节对齐
    return row_bytes * height;
}

long long audio_bytes(long long seconds, long long sample_rate, int bits_per_sample, int channels) {
    return seconds * sample_rate * bits_per_sample / 8 * channels;
}

long long video_bytes_by_bitrate(long long seconds, long long bitrate_bps) {
    return seconds * bitrate_bps / 8;
}
```

常见图像：

| 格式 | 每像素 |
|---|---|
| 灰度 8 bit | 1 byte |
| RGB 24 bit | 3 byte |
| RGBA 32 bit | 4 byte |
| BMP 24 bit | 3 byte + 行对齐 |

## 3. 编码和进制

```cpp
int hex_value(char c) {
    if ('0' <= c && c <= '9') return c - '0';
    if ('a' <= c && c <= 'f') return c - 'a' + 10;
    if ('A' <= c && c <= 'F') return c - 'A' + 10;
    return -1;
}

long long to_decimal(const string &s, int base) {
    long long ans = 0;
    for (char c : s) ans = ans * base + hex_value(c);
    return ans;
}

int utf8_byte_count(unsigned char c) {
    if ((c & 0x80) == 0) return 1;
    if ((c & 0xE0) == 0xC0) return 2;
    if ((c & 0xF0) == 0xE0) return 3;
    if ((c & 0xF8) == 0xF0) return 4;
    return 1;
}
```

## 4. IPv4 / CIDR

```cpp
unsigned int ipv4_to_uint(const string &s) {
    unsigned int ans = 0, cur = 0;
    for (char c : s) {
        if (c == '.') {
            ans = (ans << 8) | cur;
            cur = 0;
        } else {
            cur = cur * 10 + (c - '0');
        }
    }
    return (ans << 8) | cur;
}

bool same_cidr(const string &a, const string &b, int prefix) {
    unsigned int x = ipv4_to_uint(a), y = ipv4_to_uint(b);
    if (prefix == 0) return true;
    unsigned int mask = 0xffffffffu << (32 - prefix);
    return (x & mask) == (y & mask);
}
```

