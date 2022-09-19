# 谱面导入教程

### Step 1：解压文件

新建两个文件夹，分别命名为 `old` 和 `new`，使用 [7-zip](https://www.7-zip.org/) 等工具将 `mcz `/`osz `等文件解压到 `old` 文件夹中。

### Step 2：放置谱面

##### Malody 谱面

将 `old` 文件夹中的  `mc` 文件复制到 `new` 文件夹。

##### 其他谱面

打开 `rmstZ_20220113_modified.html`，点击“选择文件”按钮，选择刚才解压出的 `mcz`/`osz` 文件，待“reading”消失后点击“点击保存”，将得到的 `xxx[key].mc` 放入 `new` 文件夹中。

### Step 3：放置音频

使用 [在线转换器](https://convertio.co/zh/) 将 `old` 文件夹中的歌曲音频文件转为 OGG 格式后放入 `new` 文件夹。（若原本就为 OGG 格式，可直接复制到 `new` 文件夹。）

### Step 4：导入谱面

打开 Omegar-Toolbox，进入“导入 Malody 谱面”功能，选择 `new` 文件夹。

完成以上操作后，`new` 文件夹中将出现 `json` 项目文件，可使用 Omegar-Toolbox 中的其他功能对其进行操作。
