import sys

# 版本号
VERSION = 'v0.4.221109'

# 调试模式
if '_MEIPASS' in dir(sys):  # Pyinstaller 生成
    DEBUG_MODE = False
else:
    DEBUG_MODE = True

# 对话框标题
DIALOG_TITLE = 'Omegar Toolbox '+VERSION+' [Debug Mode]'*DEBUG_MODE


"""
json 写入
"""

# note 属性
NOTE_PROPERTIES = [
    'is_fake'
]

# note 默认属性
DEFAULT_PROPERTIES = {
    'is_fake': False
}


"""
omgc 转换
"""

# 画面高度
CHART_FRAME_HEIGHT = 1000

# 默认判定线初始位置
CHART_LINE_INITIAL_POSITION = 800

# 缓冲时间（单位：秒，适用于提前激活、推迟消失、游戏提前开始）
BUFFER_TIME = 1

# 线性缓动
SLOW_MOVING_LINEAR = 'linear'

# 正弦缓动
SLOW_MOVING_SINE = 'sine'


"""
omgc 指令
"""

# 指令代码
CMD_PLAY_MUSIC = 0x0000
CMD_ACTIVATE_NOTE = 0x0100
CMD_REMOVE_NOTE = 0x0101
CMD_NOTE_POS = 0x0110
CMD_NOTE_TRACK_LINEAR = 0x0120
CMD_NOTE_TRACK_SINE = 0x0121
CMD_LINE_ALPHA_LINEAR = 0x0200
CMD_LINE_ALPHA_SINE = 0x0201
CMD_LINE_POS_LINEAR = 0x0210
CMD_LINE_POS_SINE = 0x0211

# 指令名称
COMMAND_NAME = {
    CMD_PLAY_MUSIC: '播放音乐',
    CMD_ACTIVATE_NOTE: '激活 note',
    CMD_REMOVE_NOTE: '移除 note',
    CMD_NOTE_POS: 'note 位置',
    CMD_NOTE_TRACK_LINEAR: 'note 轨道-线性',
    CMD_NOTE_TRACK_SINE: 'note 轨道-正弦',
    CMD_LINE_ALPHA_LINEAR: 'line 透明度-线性',
    CMD_LINE_ALPHA_SINE: 'line 透明度-正弦',
    CMD_LINE_POS_LINEAR: 'line 位置-线性',
    CMD_LINE_POS_SINE: 'line 位置-正弦'
}

# 指令参数类型
COMMAND_PARAM_TYPE = {
    CMD_PLAY_MUSIC: (),
    CMD_ACTIVATE_NOTE: (int,),
    CMD_REMOVE_NOTE: (int,),
    CMD_NOTE_POS: (int, float, float, float),
    CMD_NOTE_TRACK_LINEAR: (int, float, float),
    CMD_NOTE_TRACK_SINE: (int, float, float, float, float),
    CMD_LINE_ALPHA_LINEAR: (int, float, float),
    CMD_LINE_ALPHA_SINE: (int, float, float, float, float),
    CMD_LINE_POS_LINEAR: (int, float, float),
    CMD_LINE_POS_SINE: (int, float, float, float, float)
}


"""
omgc 写入
"""

# 写入的 omgc 版本
OMGC_WRITING_VERSION = 3

# 支持读取的 omgc 版本
OMGC_SUPPORTED_VERSIONS = {3}

# omgc 数据存储格式
OMGC_STRUCT_FORMAT = {int: '<I', float: '<f'}


"""
谱面预览
"""

# 窗口高度
PREVIEW_WINDOW_HEIGHT = 600

# 背景亮度
PREVIEW_BACKGROUND_BRIGHTNESS = 0.5

# 背景模糊度
PREVIEW_BACKGROUND_BLUR = 10

# 键位映射
PREVIEW_KEY_MAP = 'dfjk'

# 轨道数量
PREVIEW_TRACK_NUMBER = len(PREVIEW_KEY_MAP)

# 轨道宽度
PREVIEW_TRACK_WIDTH = 100

# 分隔线宽度
PREVIEW_SPLIT_WIDTH = 3

# 分隔线颜色
PREVIEW_SPLIT_COLOR = (200, 200, 200)

# 判定线宽度
PREVIEW_LINE_WIDTH = 5

# 判定线颜色
PREVIEW_LINE_COLOR = (100, 255, 100)

# 音符宽度
PREVIEW_NOTE_WIDTH = 90

# 音符高度
PREVIEW_NOTE_HEIGHT = 15

# 音符圆角大小
PREVIEW_NOTE_BORDER_RADIUS = 10

# 音符颜色
PREVIEW_NOTE_COLOR = (200, 200, 255)

# 字体大小
PREVIEW_FONT_SIZE = 30

# 字体颜色
PREVIEW_FONT_COLOR = (255, 100, 100)

# 默认音符流速倍率
PREVIEW_DEFAULT_NOTE_SPEED_RATE = 8

# 默认音乐音量
PREVIEW_DEFAULT_MUSIC_VOLUME = 0.5
