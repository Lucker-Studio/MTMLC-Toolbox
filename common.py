import hashlib
import json
import os
import shutil
import sys
import zipfile


# 版本号
VERSION = 'v1.0.221127'

# 调试模式
if '_MEIPASS' in dir(sys):  # Pyinstaller 生成
    DEBUG_MODE = False
    RESOURCES_DIR = os.path.join(sys._MEIPASS, 'Resources')
else:
    DEBUG_MODE = True
    RESOURCES_DIR = os.path.abspath('Resources')

# 对话框标题
DIALOG_TITLE = 'MTMLC-Toolbox '+VERSION+' [Debug Mode]'*DEBUG_MODE


"""
note 属性
"""

# 属性列表
NOTE_PROPERTIES = [
    'is_fake'
]

# 默认属性
DEFAULT_PROPERTIES = {
    'is_fake': False
}


"""
mc 转 mtmlproj
"""

# 流速倍率
MC_SPEED_RATE = 3


"""
mtmlproj 转 mtmlc
"""

# 画面高度
CHART_FRAME_HEIGHT = 1000

# 默认判定线初始位置
DEFAULT_LINE_INITIAL_POSITION = 800

# 默认判定线透明度
DEFAULT_LINE_INITIAL_ALPHA = 1

# 线性缓动
SLOW_MOVING_LINEAR = 'linear'

# 正弦缓动
SLOW_MOVING_SINE = 'sine'


"""
mtmlc 指令
"""

# 指令代码
CMD_PLAY_MUSIC = 0x00
CMD_ACTIVATE_NOTE = 0x01
CMD_NOTE_TRACK_LINEAR = 0x02
CMD_NOTE_TRACK_SINE = 0x03
CMD_LINE_ALPHA_LINEAR = 0x11
CMD_LINE_ALPHA_SINE = 0x12
CMD_LINE_POS_LINEAR = 0x13
CMD_LINE_POS_SINE = 0x14
CMD_LINE_PLAY_POS = 0x15

# 指令名称
COMMAND_NAME = {
    CMD_PLAY_MUSIC: '播放音乐',
    CMD_ACTIVATE_NOTE: '激活 note',
    CMD_NOTE_TRACK_LINEAR: 'note 轨道-线性',
    CMD_NOTE_TRACK_SINE: 'note 轨道-正弦',
    CMD_LINE_ALPHA_LINEAR: 'line 透明度-线性',
    CMD_LINE_ALPHA_SINE: 'line 透明度-正弦',
    CMD_LINE_POS_LINEAR: 'line 位置-线性',
    CMD_LINE_POS_SINE: 'line 位置-正弦',
    CMD_LINE_PLAY_POS: 'line 播放位置'
}

# 指令参数类型模板
ID_LINEAR = (int,)+(float,)*2
ID_SINE = (int,)+(float,)*4

# 指令参数类型
COMMAND_PARAM_TYPE = {
    CMD_PLAY_MUSIC: (float,),
    CMD_ACTIVATE_NOTE: (int,),
    CMD_NOTE_TRACK_LINEAR: ID_LINEAR,
    CMD_NOTE_TRACK_SINE: ID_SINE,
    CMD_LINE_ALPHA_LINEAR: ID_LINEAR,
    CMD_LINE_ALPHA_SINE: ID_SINE,
    CMD_LINE_POS_LINEAR: ID_LINEAR,
    CMD_LINE_POS_SINE: ID_SINE,
    CMD_LINE_PLAY_POS: ID_LINEAR
}


"""
mtmlc 写入
"""

# mtmlc 数据存储格式
MTMLC_STRUCT_FORMAT = {int: '<I', float: '<f'}


"""
mtmlz 打包
"""

# 支持的音频格式
MTMLZ_SUPPORTED_MUSIC_FORMATS = ['*.ogg', '*.mp3']

# 支持的曲绘格式
MTMLZ_SUPPORTED_ILLUSTRATION_FORMATS = ['*.jpg', '*.png']


"""
预览谱面
"""

# 窗口高度
PREVIEW_WINDOW_HEIGHT = 600

# 背景亮度
PREVIEW_BACKGROUND_BRIGHTNESS = 0.5

# 背景模糊度
PREVIEW_BACKGROUND_BLUR = 10

# 轨道宽度
PREVIEW_TRACK_WIDTH = 120

# 分隔线宽度
PREVIEW_SPLIT_WIDTH = 3

# 分隔线颜色
PREVIEW_SPLIT_COLOR = (200, 200, 200)

# 进度条宽度
PREVIEW_PROGRESS_WIDTH = 3

# 进度条颜色
PREVIEW_PROGRESS_COLOR = (255, 255, 100)

# 判定线宽度
PREVIEW_LINE_WIDTH = 5

# 判定线颜色
PREVIEW_LINE_COLOR = (100, 255, 100)

# 音符宽度
PREVIEW_NOTE_WIDTH = 100

# 音符高度
PREVIEW_NOTE_HEIGHT = 15

# 音符圆角大小
PREVIEW_NOTE_BORDER_RADIUS = 5

# 音符颜色
PREVIEW_NOTE_COLOR = (200, 200, 255)

# 音符边框宽度
PREVIEW_NOTE_BORDER_WIDTH = 2

# 音符边框颜色
PREVIEW_NOTE_BORDER_COLOR = (255, 255, 100)

# 字体大小
PREVIEW_FONT_SIZE = 30

# 字体颜色
PREVIEW_FONT_COLOR = (255, 100, 100)

# FPS 更新时间
PREVIEW_FPS_UPDATE_TIME = 0.5

# 开始前等待时间
PREVIEW_WAIT_TIME = 1

# MISS 判定时间
PREVIEW_MISS_TIME = 0.2

# 默认音符流速倍率
PREVIEW_DEFAULT_NOTE_SPEED_RATE = 2.5

# 默认音乐音量
PREVIEW_DEFAULT_MUSIC_VOLUME = 0.5


"""
文件操作
"""


def read_json(json_path: str) -> dict:
    """
    读取 json 文件
    """
    return json.load(open(json_path, encoding='utf-8'))


def write_json(data: dict, json_path: str) -> None:
    """
    写入 json 文件
    """
    json.dump(data, open(json_path, 'w', encoding='utf-8'))


def unpack_zip(zip_path: str, target_path: str) -> None:
    """
    解包 zip 文件
    """
    if not os.path.isdir(target_path):
        os.makedirs(target_path)
    zipfile.ZipFile(zip_path).extractall(target_path)
    for dirpath, dirnames, filenames in os.walk(target_path):
        for name in dirnames+filenames:
            try:
                newname = name.encode('cp437').decode('utf-8')
                os.rename(os.path.join(target_path, dirpath, name), os.path.join(target_path, dirpath, newname))
            except UnicodeError:
                pass


def pack_zip(files: dict, zip_path: str) -> None:
    """
    打包到 zip 文件
    """

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as f:
        for inside_path, outside_path in files.items():
            f.write(outside_path, inside_path)


def pack_dir(files: dict, dir_path: str) -> None:
    """
    打包到文件夹
    """

    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    for inside_path, outside_path in files.items():
        shutil.copy(outside_path, os.path.join(dir_path, inside_path))


def get_md5(file_path: str) -> str:
    """
    获取文件 MD5 字符串
    """

    return hashlib.md5(open(file_path, 'rb').read()).hexdigest()
