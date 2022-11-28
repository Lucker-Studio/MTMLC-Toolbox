import os
import sys

from .mtmlc_commands import *


# 资源路径
if '_MEIPASS' in dir(sys):  # Pyinstaller 生成
    RESOURCES_PATH = os.path.join(sys._MEIPASS, 'Resources')
else:
    RESOURCES_PATH = os.path.abspath('Resources')

# note 属性
NOTE_DEFAULT_PROPERTIES = {
    'is_fake': False
}
NOTE_PROPERTIES = NOTE_DEFAULT_PROPERTIES.keys()

# mtmlproj 缓动类型
SLOW_MOVING_LINEAR = 'linear'
SLOW_MOVING_SINE = 'sine'

# mtmlc 画面高度
CHART_FRAME_HEIGHT = 1000

# mtmlc 默认判定线初始位置
DEFAULT_LINE_INITIAL_POSITION = 800

# mtmlc 默认判定线初始透明度
DEFAULT_LINE_INITIAL_ALPHA = 1

# mtmlc 指令参数类型
ID_LINEAR = (int,)+(float,)*2
ID_SINE = (int,)+(float,)*4
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

# mtmlc 数据存储格式
MTMLC_STRUCT_FORMAT = {int: '<I', float: '<f'}

# 支持的音频格式
SUPPORTED_MUSIC_FORMATS = ['*.ogg', '*.mp3']

# 支持的曲绘格式
SUPPORTED_ILLUSTRATION_FORMATS = ['*.jpg', '*.png']
