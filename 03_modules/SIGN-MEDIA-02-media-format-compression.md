# SIGN-MEDIA-02 多媒体、文件格式与压缩估算

模块编号：SIGN-MEDIA-02

模块名称：图片、音频、视频、文件格式和压缩估算

标签：签到题、多媒体、图片、音频、视频、BMP、颜色、压缩、文件大小、C++17

一句话用途：遇到图片大小、采样率、码率、颜色编码、压缩率和文件格式估算时，用本模块查公式。

题面触发词：BMP、像素、分辨率、DPI、RGB、RGBA、灰度、采样率、声道、帧率、码率、压缩率。

什么时候用：

- 题目给宽高、位深、采样率、帧率，要求文件大小。
- 题目问 RGB/HSV、alpha、颜色十六进制。
- 题目问压缩前后比例或传输时间。

不要什么时候用：

- 真正图像处理算法，如卷积、边缘检测，按矩阵模拟。
- 复杂文件格式头部结构，以题面给出的字段为准。
- 历史编码和字体渲染细节不在本卷范围内。

复杂度：公式估算 `O(1)`；像素逐个处理 `O(width*height)`。

依赖的标准容器：`string`、`vector<int>`、`iomanip`。

输入如何整理：

```text
图像：宽、高、每像素 bit、是否行对齐。
音频：秒数、采样率、每样本 bit、声道数。
视频：秒数、帧率、每帧大小或码率。
```

接口：

```text
image_raw_bytes = width * height * bits_per_pixel / 8。
BMP bytes = row_aligned_bytes * height。
audio bytes = seconds * sample_rate * bits_per_sample/8 * channels。
video bytes = seconds * bitrate_bps / 8。
```

常见坑：

- BMP 像素数据每行 4 字节对齐。
- 24 位 RGB 是 3 字节，不含 alpha。
- 32 位 RGBA 是 4 字节。
- DPI 是打印密度，不直接改变像素总数，除非题目用英寸换算像素。
- 码率通常已经包含压缩后每秒 bit 数。

暴力/部分分替代：

- 不知道头部大小时，先算像素数据大小。
- 不知道压缩格式时，按题面给的压缩率。
- RGB 转换复杂时，先处理十六进制拆分。

## 1. 图片大小

| 图像类型 | 每像素 |
|---|---|
| 黑白 1 bit | `1/8` byte |
| 灰度 8 bit | 1 byte |
| RGB 24 bit | 3 byte |
| RGBA 32 bit | 4 byte |
| 16 bit 色 | 2 byte |

BMP 行对齐：

```text
row_bytes = ceil(width * bits_per_pixel / 32) * 4
total_pixel_bytes = row_bytes * height
```

## 2. 颜色

| 表示 | 含义 |
|---|---|
| `#RRGGBB` | 红绿蓝各 8 bit |
| `#AARRGGBB` | alpha + RGB |
| RGB | 红绿蓝 |
| BGR | BMP 等格式常见存储顺序 |
| Alpha | 透明度 |
| HSV | 色相、饱和度、明度 |

十六进制颜色拆分：

```cpp
int hex2(char a, char b) {
    auto val = [](char c) {
        if ('0' <= c && c <= '9') return c - '0';
        if ('a' <= c && c <= 'f') return c - 'a' + 10;
        return c - 'A' + 10;
    };
    return val(a) * 16 + val(b);
}
```

## 3. 音频大小

```text
bytes = seconds * sample_rate * bits_per_sample / 8 * channels
```

例子：

```text
60 秒，44100 Hz，16 bit，双声道：
60 * 44100 * 16/8 * 2 = 10584000 byte
```

## 4. 视频大小

两种常见题面：

```text
未压缩：width * height * bytes_per_pixel * fps * seconds
有码率：bitrate_bps * seconds / 8
```

## 5. 压缩率

| 问法 | 公式 |
|---|---|
| 压缩后大小 | `original * ratio` |
| 压缩节省 | `original - compressed` |
| 节省百分比 | `(original-compressed)/original` |
| 码率估算 | `file_bits / seconds` |

