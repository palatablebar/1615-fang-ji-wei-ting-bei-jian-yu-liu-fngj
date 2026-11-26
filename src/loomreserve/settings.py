from .loom_checklists.contracts import Field

EXPOSURE_UNIT = '缺兼容件对应折算纬停次'
TITLE = '纺机纬停备件预留'
ROLE = '织造机修库保管员'
OBJECT = '织机巡检单'
TARGET = '纬停故障确认'
ALGORITHM = '带分区先验的高斯朴素贝叶斯'
MODE = 'classification'
IS_SURVIVAL = False
MODEL_EPOCH = 'loomreserve-1.0'
REGIONS = ('剑杆区', '喷气区', '试样区')
SIGNAL_NAMES = ('stops_per_turn', 'age_under_speed', 'oil_excursion', 'moisture_load', 'yarn_switch_rate')
RAW_EXPLAIN_INDEX = (None, None, None, None, None)
RESOURCE = '可预留备件'
DEFAULT_BUDGET = 9
ACTION = '预留兼容备件'
MANUAL_ACTION = '核实机型铭牌'
NORMAL_ACTION = '继续观测'
WORKFLOW = '依实际可互换系列扣库存，临界机型保留最低安全备件。'
PLACEMENT_MODE = 'stock_family'
POOL_LIMIT = 3
SEPARATE_CONTEXTS = False
HAS_WORKBENCH = False
SAMPLE_NAME = 'loomreserve_register.csv'

FIELDS = (
    Field('rpm', '主轴转速', 'r/min', 320, 1150, False),
    Field('stops', '班内纬停', '次', 0, 48, False),
    Field('hours', '上次检修后', '小时', 14, 920, False),
    Field('oil', '润滑压差', 'kPa', 2, 68, False),
    Field('humidity', '现场湿度', '%', 35, 84, False),
    Field('lots', '当日换纱', '批', 0, 19, True),
)
