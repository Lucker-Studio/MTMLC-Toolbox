# Omegar-Toolbox：Omega 制谱工具箱

## 运行方式

### 源代码运行

```shell
git clone https://github.com/OmegaRhythmLab/Omegar-Toolbox
cd Omegar-Toolbox
pip install easygui
python Omegar-Toolbox.py
```

若无法正常运行，请检查：

- `python` 版本是否为 Python 3
- 所需的第三方 Python 包是否已安装（若未安装请按照错误信息提示使用 `pip` 安装）
- Linux 下是否已安装 `python3-tk`

### 编译运行

#### 初始化虚拟环境（只需执行一次）

```shell
pip install -U pipenv
pipenv --python 3.8
pipenv run pip install -U -i https://mirrors.aliyun.com/pypi/simple/ easygui pillow pygame pyinstaller
```

#### 编译

运行 `build.bat`，可执行文件将在 `building/{系统名称}` 目录下生成。
