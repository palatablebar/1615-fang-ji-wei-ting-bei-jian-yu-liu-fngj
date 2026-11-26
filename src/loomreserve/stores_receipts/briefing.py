from collections import defaultdict
from math import isfinite, sqrt

from ..settings import EXPOSURE_UNIT, FIELDS


def reading(key: str, label: str, value: float, unit: str, trigger: float, direction: str) -> dict:
    number = float(value)
    boundary = float(trigger)
    if not isfinite(number) or not isfinite(boundary):
        raise ValueError(f'{label} 指标不是有限量')
    if direction not in ('high','low'):
        raise ValueError('证据边界方向不明')
    crossed = number > boundary if direction=='high' else number < boundary
    return {'field':key,'label':label,'value':round(number,3),'unit':unit,'trigger':round(boundary,3),
            'direction':direction,'exceeded':crossed}


def summarize(record: dict) -> dict:
    fields = record['raw']
    if any(fields[item.key] is None for item in FIELDS):
        return {'checks':[],'work':None,'exposure':None, 'work_label':None, 'status':'读数不全'}
    values = tuple(fields[item.key] for item in FIELDS)
    window = record['window']
    prediction = record.get('estimate')
    rpm,stops,hours,oil,humidity,lots = values
    loading=stops/max(1,rpm/600)
    consumable=max(0,oil-28)+max(0,9-oil)*1.8
    findings=[
        reading('age_hours','维保间隔',hours,'小时',525,'high'),
        reading('recoverable_signal','折算纬停',loading,'次',17,'high'),
        reading('lubrication_gap','润滑压差偏移',consumable,'kPa',16,'high'),
        reading('turns_window','挂牌窗口余量',window-22,'分钟',15,'low')]
    work=record['units']
    outcome='确认的兼容备件数'
    exposure=loading*max(0,record['requested']-record['units'])
    return {'checks':findings,'work':round(work,3),'work_label':outcome,'exposure':round(exposure,3),'status':'可核算'}


def tally(rows: list[dict]) -> dict:
    by_region = defaultdict(lambda: {'measured':0,'missing':0,'work':0.,'exposure':0.,'outside':0})
    for row in rows:
        area = by_region[row['region']]
        note = row['business_evidence']
        if note['work'] is None:
            area['missing'] += 1
        else:
            area['measured'] += 1
            area['work'] += note['work']
            area['exposure'] += note['exposure']
            area['outside'] += sum(check['exceeded'] for check in note['checks'])
    aggregates = {'work':0.,'exposure':0.,'source_missing':0,'outside_count':0}
    for area in by_region.values():
        aggregates['work'] += area['work']
        aggregates['exposure'] += area['exposure']
        aggregates['source_missing'] += area['missing']
        aggregates['outside_count'] += area['outside']
    aggregates['work'] = round(aggregates['work'],3)
    aggregates['exposure'] = round(aggregates['exposure'],3)
    return {**aggregates,'exposure_unit':EXPOSURE_UNIT,'regions':dict(sorted(by_region.items()))}
