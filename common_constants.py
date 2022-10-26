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
INSTR_NAME = {
    0x01: '添加 note',
    0x02: 'note 位置',
    0x03: 'note 轨道',
    0x04: '激活 note',
    0x10: '判定线位置'
}
