# json 工程文件

*Version 5，2022/11/11*

- `project_name`：工程名称
- `illustration_file`：曲绘文件名称
- `music_file`：音频文件名称
- `music_offset`：第 0 拍对应音乐第几秒
- `bpm_list`：BPM 列表，每一项形如 `[[a, b, c], v]`，表示从第 `a+b/c` 拍时 BPM 变为 `v`
- `line_list`：判定线列表，每一项如下：

  - `initial_position`：初始位置（若未指定，则等于默认值）
  - `initial_alpha`：初始透明度（若未指定，则等于默认值）
  - `motions`：移动事件列表（若未指定，则为空）
    - `start`：起始节拍
    - `end`：终止节拍（若未指定，则等于 `start`）
    - `target`：目标位置
    - `type`：缓动类型
      - `linear` 表示线性缓动
      - `sine` 表示正弦缓动
  - `speed_changes`：音符流速列表，每一项形如 `[[a, b, c], v]`，表示第 `a+b/c` 拍时流速变为 `v`
  - `alpha_changes`：透明度变化事件列表，格式与 `motions` 相同（若未指定，则为空）
  - `note_list`：音符列表
    - `start`：起始节拍
    - `end`：终止节拍（若未指定，则等于 `start`）
    - `judging_track`：判定轨道
    - `initial_showing_track`：初始显示轨道（若未指定，则等于 `judging_track`）
    - `showing_track_changes`：变轨事件列表，格式与 `motions` 相同（若未指定，则为空）
    - `properties`：属性（`value` 的类型均为 `bool`，若未指定，则等于默认值）
- 
- `music_path`：音频文件路径

---

# omgc 谱面文件

*Version 5，2022/11/9*

omgc 文件中无符号整型（uint）和浮点型（float）均为 4 字节小端型数据。

omgc 文件中时间单位为秒。

omgc 文件开头 4 字节为“omgc”四个小写字母的 ASCII 码，即 `6F 6D 67 63`。

omgc 文件主体分为四部分：meta 区，line 区，note 区，cmd 区。

## meta 区

meta 区由以下 4 个数据组成：

- omgc 版本（uint）
- 判定线数量（uint）
- 音符数量（uint）
- 指令数量（uint）

## line 区

line 区中每条判定线的格式如下：

- 初始位置（float）
- 初始透明度（float）
- 初始音符流速（float，即代表播放位置函数为 $val=kx$）

## note 区

note 区中每个音符的格式如下：

- 起始时间（float）
- 终止时间（float）
- 判定轨道（uint）
- 初始显示轨道（float）
- 显示位置偏移（float）
- 显示长度（float）
- note 对应的判定线 ID（uint）
- note 的属性（uint，每个二进制位表示一个属性）
- 初始是否激活（uint）

## cmd 区

cmd 区中每条指令的格式如下：

时间（float） + 类型（uint） + 参数数量 （uint）+ 参数。

指令类型列表如下：

### `0x00` 播放音乐

- 参数 1：起始时间（float）

### `0x01` 激活 note

- 参数 1：note 的 ID（uint）

注：激活 note 即将 note 添加到活动 note 列表。绘制 note 和进行打击判定时，只遍历活动 note 列表中的 note。

### `0x02` 将 note 轨道函数改为 $val=kt+b$

- 参数 1：note 的 ID（uint）
- 参数 2：$k$ 的值（float）
- 参数 3：$b$ 的值（float）

### `0x03` 将 note 轨道函数改为 $val=Asin(\omega x+\varphi)+b$

- 参数 1：note 的 ID（uint）
- 参数 2：$A$ 的值（float）
- 参数 3：$\omega$ 的值（float）
- 参数 4：$\varphi$ 的值（float）
- 参数 5：$b$ 的值（float）

### `0x11` 将 line 透明度函数改为 $val=kt+b$

- 参数 1：line 的 ID（uint）
- 参数 2：$k$ 的值（float）
- 参数 3：$b$ 的值（float）

### `0x12` 将 line 透明度函数改为 $val=Asin(\omega x+\varphi)+b$

- 参数 1：line 的 ID（uint）
- 参数 2：$A$ 的值（float）
- 参数 3：$\omega$ 的值（float）
- 参数 4：$\varphi$ 的值（float）
- 参数 5：$b$ 的值（float）

### `0x13` 将 line 位置函数改为 $val=kt+b$

- 参数 1：line 的 ID（uint）
- 参数 2：$k$ 的值（float）
- 参数 3：$b$ 的值（float）

### `0x14` 将 line 位置函数改为 $val=Asin(\omega x+\varphi)+b$

- 参数 1：line 的 ID（uint）
- 参数 2：$A$ 的值（float）
- 参数 3：$\omega$ 的值（float）
- 参数 4：$\varphi$ 的值（float）
- 参数 5：$b$ 的值（float）

### `0x15` 将 line 播放位置函数改为 $val=kx+b$

- 参数 1：line 的 ID（uint）
- 参数 2：$k$ 的值（float）
- 参数 3：$b$ 的值（float）

---

# json 歌曲信息文件

*Version 2，2022/11/11*

- `title`：曲名
- `composer`：曲师
- `illustrator`：画师
- `music_file`：歌曲音频文件名称
- `illustration_file`：曲绘文件名称
- `charts`：谱面列表
  - `difficulty`：难度
  - `number`：定数
  - `writer`：谱师
  - `md5`：omgc 的 MD5 字符串

---

# omgz 歌曲压缩包

*Version 2，2022/11/11*

- 歌曲信息文件：`info.json`
- 歌曲音频：`music.mp3` 或 `music.ogg`
- 曲绘：`illustration.png` 或 `illustration.jpg`
- 谱面文件： `(等级名称).omgc`
