# 画面高度
FRAME_HEIGHT = 1000

# 在 note 出现前提前几秒将其激活
PREACTIVATING_TIME = 0.1

# 指令列表
ADD_NOTE = 0x01
CHANGE_NOTE_POS = 0x02
CHANGE_NOTE_TRACK = 0x03
ACTIVATE_NOTE = 0x04
CHANGE_LINE_POS = 0x10
INSTR_NAME = {
    0x01: '添加 note',
    0x02: 'note 位置',
    0x03: 'note 轨道',
    0x04: '激活 note',
    0x10: '判定线位置'
}

# note 属性
NOTE_PROPERTIES = ['property_1', 'property_2', 'property_3']

# 缓动类型
LINEAR_SLOW_MOVING = 0x01
SIN_SLOW_MOVING = 0x02

# 调试模式
DEBUG_MODE = True
