# 对话框标题
TITLE = 'Omegar Toolbox v0.1.220925'

# 调试模式
DEBUG_MODE = True

# note 属性
NOTE_PROPERTIES = [
    'visible',
    'real',
    '114514'
]
DEFAULT_PROPERTIES = {
    'visible': True,
    'real': True
}

# 指令列表
ADD_NOTE = 0x01
CHANGE_NOTE_POS = 0x02
CHANGE_NOTE_TRACK = 0x03
ACTIVATE_NOTE = 0x04
CHANGE_LINE_POS = 0x10
CMD_NAME = {
    0x01: '添加 note',
    0x02: 'note 位置',
    0x03: 'note 轨道',
    0x04: '激活 note',
    0x10: '判定线位置'
}

# 画面宽高
FRAME_WIDTH = 800
FRAME_HEIGHT = 450

# 默认判定线初始位置
LINE_INITIAL_POSITION = 400

# 在 note 出现前提前几秒将其激活
PREACTIVATING_TIME = 0.1

# 缓动类型
LINEAR_SLOW_MOVING = 0x01
SIN_SLOW_MOVING = 0x02
