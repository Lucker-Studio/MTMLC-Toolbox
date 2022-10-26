# Omegar-Toolbox：Omega 制谱工具箱

## 一、工具箱运行方式

### 1. 源代码运行（各系统均可）

```shell
git clone https://github.com/OmegaRhythmLab/Omegar-Toolbox
cd Omegar-Toolbox
pip install easygui
python Omegar-Toolbox.py
```

若以上命令无法运行，请检查 `git` 是否安装、`pip` 和 `python` 版本是否为 Python 3、Linux 下是否已安装 `python3-tk`。

### 2. 编译运行（Windows+WSL）

#### 初始化虚拟环境（只需执行一次）

##### 注意事项

- 所用的 Python 版本为 3.10。
- 直接 `wsl pipenv` 会因 `pipenv` 可执行文件不在 `$PATH` 中而提示“未找到命令”，需借助 `python -m` 运行。

```shell
pip install -U pipenv
wsl pip install -U pipenv

pipenv --python 3.10
wsl python -m pipenv --python 3.10

pipenv run pip install easygui pygame pyinstaller
wsl python -m pipenv run pip install easygui pygame pyinstaller
```

#### 编译

运行 `build.bat`，可执行文件将在 `building/{系统名称}` 目录下生成。

## 二、谱面导入教程

### Step 1：解压文件

使用 7-zip 等工具将 `mcz`/`osz `等文件解压到某个文件夹中。

### Step 2：转换谱面（Malody 谱面可跳过）

打开 `rmstZ_20220113_modified.html`，点击“选择文件”按钮，选择刚才解压出的谱面文件（如 `.osu`），待“reading”消失后点击“点击保存”，将得到的 `xxx[key].mc` 放入文件夹中。

### Step 3：导入谱面

打开 Omegar-Toolbox，进入“导入 Malody 谱面”功能，选择刚才解压的文件夹。

完成以上操作后，文件夹中将出现 `json` 工程文件，可使用 Omegar-Toolbox 中的其他功能对其进行操作。

## 三、文件格式说明

### 1. 工程文件（`.json`，json 格式）

- `project_name`：工程名称。
- `music_path`：音频文件路径。
- `music_offset`：第 $0$ 拍对应音乐第几秒。
- `bpm_list`：BPM 列表，每一项形如 `[[a, b, c], v]`，表示从第 `a+b/c` 拍（从 $0$ 开始）起 BPM **瞬间变为** `v`。
- `global_speed_key_points`：全局流速关键点列表，每一项形如 `[[a, b, c], v]`，表示第 `a+b/c` 拍（从 $0$ 开始）时流速为 `v`（瞬时变速事件需在同一拍记录两个关键点）。
- `note_list`：note 列表。
  - `start`：判定节拍（`[a, b, c]`）。
  - `end`：结束节拍（瞬时 note 的 `start` 与  `end` 相等）。
  - `judging_track`：判定轨道。
  - `initial_showing_track`：初始显示轨道。
  - `showing_track_changes`：变轨事件列表。
    - `start`：起始节拍。
    - `end`：终止节拍（瞬时事件的 `start` 与  `end` 相等）。
    - `target`：目标轨道。
    - `type`：缓动类型（$1$ 为线性缓动，$2$ 为正弦缓动；瞬时事件的缓动类型任意）。
  - `speed_key_points`：流速关键点列表，每一项形如 `[[a, b, c], v]`，表示第 `a+b/c` 拍（从 $0$ 开始）时流速为 `v`（瞬时变速事件需在同一拍记录两个关键点）。
  - `free_from_global_speed`：是否不受全局流速影响（当此项为 `true` 且 `speed_key_points` 不为空时，将两组关键点叠加）。
  - `properties`：属性（`value` 的类型均为 `bool`）。
    - `property_1`：属性 1。
    - `property_2`：属性 2。
    - `property_3`：属性 3。
- `line`：判定线相关。
  - `initial_position`：判定线的初始位置。
  - `motions`：判定线移动事件列表，详见 `note_list` 的 `showing_track_changes`。

### 2. 谱面文件（`.omgc`，二进制格式）

该文件中的数据全部采用小端型存储，无符号整型（int）和浮点型（float）均占 4 字节。

该文件由一个整型数据 $n$ 和 $n$ 个指令构成。

指令格式：时间（单位为 s，浮点型，若为负数则表示游戏开始前执行） + 类型 + 参数数量 + 参数。

指令列表如下：

#### `0x01` 添加 note

- 参数 1：note 的 ID（int）。
- 参数 2：note 的属性（int）。
  - `0b1` （属性 1）
  - `0b10` （属性 2）
  - `0b100` （属性 3）
- 参数 3~5：初始位置函数（float）。
- 参数 6：初始显示轨道（int）。
- 参数 7：实际判定轨道（int）。
- 参数 8：判定时间（float）。
- 参数 9：结束时间（float）。
- 参数 10：显示长度（float，倒打 note 为负）。

#### `0x02` 更改 note 位置函数

- 参数 1：note 的 ID（int）。
- 参数 2：二次项系数（float）。
- 参数 3：一次项系数（float）。
- 参数 4：常数项（float）。

注：note 相对于判定线的位置关于时间的二次函数为 note 相对于判定线的速度关于时间的一次函数的不定积分。制谱器工程文件中存储了 $n$ 个形如 $(t_i,n_i)$ 的关键点，每相邻两点可确定该区间上的速度变化直线，对速度函数做不定积分即可计算出该区间上位置关于时间的二次函数。另外，需要取常数以使各段抛物线首尾顺次相接。

#### `0x03` 更改 note 轨道函数

- 参数 1：note 的 ID（int）。
- 参数 2：函数类型（int）。
  - `0x01` 线性缓动（$val=kt+b$）
    - 参数 3~4：$k$ 和 $b$ 的值（float）。
  - `0x02` 正弦缓动（$val=Asin(\omega x+\varphi)+b$）
    - 参数 3~6：$A、\omega、\varphi、b$ 的值（float）。

#### `0x04` 激活 note

- 参数 1：note 的 ID（int）。

注：激活 note 即将 note 添加到活动 note 列表。绘制 note 和进行打击判定时，只遍历活动 note 列表中的 note。note 被打击或超时后，将 note 从活动 note 列表中移除。

#### `0x10` 更改判定线位置函数

- 参数 1：函数类型（int）。
  - `0x01` 线性缓动（$val=kt+b$）
    - 参数 2~3：$k$ 和 $b$ 的值（float）。
  - `0x02` 正弦缓动（$val=Asin(\omega x+\varphi)+b$）
    - 参数 2~5：$A、\omega、\varphi、b$ 的值（float）。

### 3. 歌曲信息文件（`.txt`，纯文本格式）

- 前 3 行：3 个字符串，分别表示曲名、曲师、画师。
- 第 4 行：一个整数 $n$，表示谱面数量。
- 第 5 行起：$n$ 组谱面信息（每组谱面信息有 4 行，分别表示难度、定数、谱师、谱面文件 MD5 值）。

### 4. 歌曲压缩包（`.omgz`，zip 格式）

- 歌曲信息文件：`info.txt`
- 歌曲音频：`music.mp3`
- 曲绘：`illustration.png`
- 谱面文件： `charts/(等级名称).omgc`
