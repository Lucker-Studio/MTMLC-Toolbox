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

- Windows 的 Python 版本为 3.8+3.10（Windows 7 仅支持 3.8），WSL 的 Python 版本为 3.10。
- 必须先在 WSL 中创建虚拟环境，否则会因要求的 Python 版本与 `Pipfile` 中的不同而报错。
- 直接 `wsl pipenv` 会因 `pipenv` 可执行文件不在 `$PATH` 中而提示“未找到命令”，需借助 `python -m` 运行。

```shell
wsl pip install -U pipenv
pip install -U pipenv

wsl python -m pipenv --python 3.10
pipenv --python 3.8

wsl python -m pipenv run pip install easygui pyinstaller
pipenv run pip install easygui pyinstaller
```

#### 编译

运行 `build.bat`，可执行文件将在 `building/{系统名称}` 目录下生成。

## 二、文件格式说明

### 1. 歌曲压缩包（`.omgz`，zip 格式）

- 歌曲信息文件：`info.txt`
- 歌曲音频：`music.ogg`
- 曲绘：`illustration.png`
- 谱面文件： `charts/(等级名称).omgc`

### 2. 歌曲信息文件（`.txt`，文本格式）

- 前 3 行：3 个字符串，分别表示曲名、曲师、画师。
- 第 4 行：一个整数 $n$，表示谱面数量。
- 第 5 行起：$n$ 组谱面信息（每组谱面信息有 4 行，分别表示难度、定数、谱师、谱面文件 MD5 值）。

### 3. 谱面文件（`.omgc`，二进制格式）

该文件由一个整数 $n$ 和 $n$ 个指令构成。

指令格式：时间（单位为 s，类型为 float，若为负数则表示游戏开始前执行） + 类型 + 参数。

指令列表如下：

#### `0x01` 添加 note

- 参数 1：note 的 ID（int）。
- 参数 2：note 的属性（int）。
  - `0b1` （属性 1）
  - `0b10` （属性 2）
  - `0b100` （属性 3）
  - `0b1000` （属性 4）
- 参数 3~5：初始位置函数（float）。
- 参数 6：初始显示轨道（int）。
- 参数 7：实际判定轨道（int）。
- 参数 8：开始时间（float）。
- 参数 9：结束时间（float）。
- 参数 10：显示长度（float，头-尾）。

#### `0x02` 更改 note 位置函数

- 参数 1：note 的 ID（int）。
- 参数 2：二次项系数（float）。
- 参数 3：一次项系数（float）。
- 参数 4：常数项（float）。

注：note 相对于判定线的位置关于时间的二次函数为 note 相对于判定线的速度关于时间的一次函数的不定积分。制谱器项目文件中存储了 $n$ 个形如 $(t_i,n_i)$ 的关键点，每相邻两点可确定该区间上的速度变化直线，对速度函数做不定积分即可计算出该区间上位置关于时间的二次函数。另外，需要取常数以使各段抛物线首尾顺次相接。

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
