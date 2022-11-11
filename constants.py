import sys

# 版本号
VERSION = 'v0.5.221111'

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
CHART_FRAME_HEIGHT = 500

# 默认判定线初始位置
DEFAULT_LINE_INITIAL_POSITION = 400

# 默认判定线透明度
DEFAULT_LINE_INITIAL_ALPHA = 1

# 线性缓动
SLOW_MOVING_LINEAR = 'linear'

# 正弦缓动
SLOW_MOVING_SINE = 'sine'


"""
omgc 指令
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
omgc 写入
"""

# 写入的 omgc 版本
OMGC_WRITING_VERSION = 5

# omgc 数据存储格式
OMGC_STRUCT_FORMAT = {int: '<I', float: '<f'}


"""
omgz 打包
"""

# 支持的音频格式
OMGZ_SUPPORTED_MUSIC_FORMATS = ['*.ogg', '*.mp3']

# 支持的曲绘格式
OMGZ_SUPPORTED_ILLUSTRATION_FORMATS = ['*.jpg', '*.png']


"""
谱面预览
"""

# 支持读取的 omgc 版本
PREVIEW_SUPPORTED_OMGC_VERSIONS = {5}

# 窗口高度
PREVIEW_WINDOW_HEIGHT = 600

# 背景亮度
PREVIEW_BACKGROUND_BRIGHTNESS = 0.5

# 背景模糊度
PREVIEW_BACKGROUND_BLUR = 10

# 轨道数量
PREVIEW_TRACK_NUMBER = 4

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

# 开始前等待时间
PREVIEW_WAIT_TIME = 1

# MISS 判定时间
PREVIEW_MISS_TIME = 0.2

# 默认音符流速倍率
PREVIEW_DEFAULT_NOTE_SPEED_RATE = 5

# 默认音乐音量
PREVIEW_DEFAULT_MUSIC_VOLUME = 0.5
