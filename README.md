# Omegar-Toolbox：Omega 制谱工具箱

## 运行方式

### 源代码运行（各系统均可）

```shell
git clone https://github.com/OmegaRhythmLab/Omegar-Toolbox
cd Omegar-Toolbox
pip install easygui
python Omegar-Toolbox.py
```

若以上命令无法运行，请检查 `git` 是否安装、`pip` 和 `python` 版本是否为 Python 3、Linux 下是否已安装 `python3-tk`。

### 编译运行（Windows+WSL）

#### 初始化虚拟环境（只需执行一次）

- Windows 所用的 Python 版本为 3.8，WSL 所用的 Python 版本为 3.10。
- 直接 `wsl pipenv` 会因 `pipenv` 可执行文件不在 `$PATH` 中而提示“未找到命令”，需借助 `python -m` 运行。

```shell
pip install -U pipenv
wsl pip install -U pipenv

pipenv --python 3.8
wsl python -m pipenv --python 3.10

pipenv run pip install easygui pygame pyinstaller
wsl python -m pipenv run pip install easygui pygame pyinstaller
```

#### 编译

运行 `build.bat`，可执行文件将在 `building/{系统名称}` 目录下生成。
