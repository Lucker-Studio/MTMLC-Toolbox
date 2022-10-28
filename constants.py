# 对话框标题
TITLE = 'Omegar Toolbox v0.2.221028'

# 调试模式
DEBUG_MODE = True

# note 属性
NOTE_PROPERTIES = [
    'is_fake'
]
DEFAULT_PROPERTIES = {
    'is_fake': False
}

# 写入的 omgc 版本及支持读取的 omgc 版本
WRITING_OMGC_VERSION = 3
SUPPORTED_OMGC_VERSIONS = {3}

# omgc 数据存储格式
STRUCT_FORMAT = {int: '<I', float: '<f'}

# 指令代码
PLAY_MUSIC = 0x0000
ACTIVATE_NOTE = 0x0100
REMOVE_NOTE = 0x0101
NOTE_POS = 0x0110
NOTE_TRACK_LINEAR = 0x0120
NOTE_TRACK_SINE = 0x0121
LINE_ALPHA_LINEAR = 0x0200
LINE_ALPHA_SINE = 0x0201
LINE_POS_LINEAR = 0x0210
LINE_POS_SINE = 0x0211

# 指令名称
CMD_NAME = {
    PLAY_MUSIC: '播放音乐',
    ACTIVATE_NOTE: '激活 note',
    REMOVE_NOTE: '移除 note',
    NOTE_POS: 'note 位置',
    NOTE_TRACK_LINEAR: 'note 轨道-线性',
    NOTE_TRACK_SINE: 'note 轨道-正弦',
    LINE_ALPHA_LINEAR: 'line 透明度-线性',
    LINE_ALPHA_SINE: 'line 透明度-正弦',
    LINE_POS_LINEAR: 'line 位置-线性',
    LINE_POS_SINE: 'line 位置-正弦'
}

# 指令参数类型
CMD_PARAM_TYPE = {
    PLAY_MUSIC: (),
    ACTIVATE_NOTE: (int,),
    REMOVE_NOTE: (int,),
    NOTE_POS: (int, float, float, float),
    NOTE_TRACK_LINEAR: (int, float, float),
    NOTE_TRACK_SINE: (int, float, float, float, float),
    LINE_ALPHA_LINEAR: (int, float, float),
    LINE_ALPHA_SINE: (int, float, float, float, float),
    LINE_POS_LINEAR: (int, float, float),
    LINE_POS_SINE: (int, float, float, float, float)
}

# 画面宽高
FRAME_WIDTH = 1600
FRAME_HEIGHT = 900

# 默认判定线初始位置
LINE_INITIAL_POSITION = 800

# 缓冲时间（提前激活与推迟消失）
BUFFER_TIME = 0.5

# 缓动类型
LINEAR_SLOW_MOVING = 'linear'
SINE_SLOW_MOVING = 'sine'
