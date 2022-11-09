# json 工程文件

*Version 4，2022/11/9*

- `project_name`：工程名称。
- `music_path`：音频文件路径。
- `music_offset`：第 $0$ 拍对应音乐第几秒。
- `bpm_list`：BPM 列表，每一项形如 `[[a, b, c], v]`，表示从第 `a+b/c` 拍时 BPM 变为 `v`。
- `line_list`：判定线列表，每一项如下：
  - `initial_position`：初始位置。
  - `initial_alpha`：初始透明度。
  - `motions`：移动事件列表。

    - `start`：起始节拍。
    - `end`：终止节拍。
    - `target`：目标位置。
    - `type`：缓动类型（`linear` 表示线性缓动，`sine` 表示正弦缓动）。
  - `global_speed_changes`：全局流速列表，每一项形如 `[[a, b, c], v]`，表示第 `a+b/c` 拍时流速变为 `v`。
  - `alpha_changes`：透明度变化事件列表，格式与 `motions` 相同。
  - `note_list`：音符列表。

    - `start`：判定节拍。
    - `end`：结束节拍。
    - `judging_track`：判定轨道。
    - `initial_showing_track`：初始显示轨道。
    - `showing_track_changes`：变轨事件列表，格式与 `motions` 相同。
    - `speed_changes`：流速列表，格式与 `global_speed_changes` 相同，若为空则使用全局流速。
    - `properties`：属性（`value` 的类型均为 `bool`）。

---

# omgc 谱面文件

*Version 4，2022/11/9*

omgc 文件中无符号整型（uint）和浮点型（float）均占 4 字节，采用小端型存储。

omgc 文件中“一个数据”的定义为 4 字节组成的整体。

omgc 文件中时间单位为秒（s）。

omgc 文件分为四部分：meta 区，line 区，note 区，cmd 区。

## meta 区

meta 区由以下 8 个数据组成：

- omgc 四个小写字母的 ASCII 码（6F 6D 67 63）
- omgc 版本（uint）
- line 区数据数量（uint）
- 判定线数量（uint）
- note 区数据数量（uint）
- 音符数量（uint）
- cmd 区数据数量（uint）
- 指令数量（uint）

## line 区

line 区中每条判定线的格式如下：

- 初始位置（float）
- 初始透明度（float）

## note 区

note 区中每个音符的格式如下：

- note 的属性（uint，每个二进制位表示一个属性）
- note 对应的判定线 ID（uint）
- 初始位置函数 $k$ 的值（float）
- 初始位置函数 $b$ 的值（float）
- 初始显示轨道（float）
- 实际判定轨道（uint）
- 判定时间（float）
- 结束时间（float）
- 显示长度（float，倒打 note 为负）

## cmd 区

cmd 区中每条指令的格式如下：

时间（float） + 类型（uint） + 参数数量 （uint）+ 参数。

指令类型列表如下：

### `0x0100` 激活 note

- 参数 1：note 的 ID（uint）。

注：激活 note 即将 note 添加到活动 note 列表。绘制 note 和进行打击判定时，只遍历活动 note 列表中的 note。

### `0x0101` 移除 note

- 参数 1：note 的 ID（uint）。

### `0x0111` 将 note 位置函数改为 $val=kt+b$

- 参数 1：note 的 ID（uint）。
- 参数 2：$k$ 的值（float）。
- 参数 3：$b$ 的值（float）。

注：omgc v3 中 `0x0110` 命令为将 note 位置函数改为 $val=ax^2+bx+c$，为兼容 omgc v3，暂不占用该指令，但该指令在新版本“谱面预览”功能中会被忽略。

### `0x0120` 将 note 轨道函数改为 $val=kt+b$

- 参数 1：note 的 ID（uint）。
- 参数 2：$k$ 的值（float）。
- 参数 3：$b$ 的值（float）。

### `0x0121` 将 note 轨道函数改为 $val=Asin(\omega x+\varphi)+b$

- 参数 1：note 的 ID（uint）。
- 参数 2：$A$ 的值（float）。
- 参数 3：$\omega$ 的值（float）。
- 参数 4：$\varphi$ 的值（float）。
- 参数 5：$b$ 的值（float）。

### `0x0200` 将 line 透明度函数改为 $val=kt+b$

- 参数 1：line 的 ID（uint）。
- 参数 2：$k$ 的值（float）。
- 参数 3：$b$ 的值（float）。

### `0x0201` 将 line 透明度函数改为 $val=Asin(\omega x+\varphi)+b$

- 参数 1：line 的 ID（uint）。
- 参数 2：$A$ 的值（float）。
- 参数 3：$\omega$ 的值（float）。
- 参数 4：$\varphi$ 的值（float）。
- 参数 5：$b$ 的值（float）。

### `0x0210` 将 line 位置函数改为 $val=kt+b$

- 参数 1：line 的 ID（uint）。
- 参数 2：$k$ 的值（float）。
- 参数 3：$b$ 的值（float）。

### `0x0211` 将 line 位置函数改为 $val=Asin(\omega x+\varphi)+b$

- 参数 1：line 的 ID（uint）。
- 参数 2：$A$ 的值（float）。
- 参数 3：$\omega$ 的值（float）。
- 参数 4：$\varphi$ 的值（float）。
- 参数 5：$b$ 的值（float）。

---

# txt 歌曲信息文件

*Version 1，2022/9/23*

- 前 3 行：3 个字符串，分别表示曲名、曲师、画师。
- 第 4 行：一个整数 $n$，表示谱面数量。
- 第 5 行起：$n$ 组谱面信息（每组谱面信息有 4 行，分别表示难度、定数、谱师、谱面文件 MD5 值）。

---

# zip 歌曲压缩包

*Version 1，2022/9/23*

- 歌曲信息文件：`info.txt`
- 歌曲音频：`music.mp3`
- 曲绘：`illustration.png`
- 谱面文件： `charts/(等级名称).omgc`
