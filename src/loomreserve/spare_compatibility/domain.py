from ..weft_indicators.contracts import Prepared
from .contracts import Disposition, Draft


def interpret(resolved: Prepared, value: float, uncertainty: float) -> Draft:
    probe = resolved.record

    def block(reason: str) -> Draft:
        return Draft(resolved,Disposition.MANUAL,0,0,1,0,0,reason,'')

    def normal(reason: str) -> Draft:
        return Draft(resolved,Disposition.NORMAL,0,0,1,0,0,reason,'')

    def proposal(qty: int, priority: float, minutes: int, reason: str, resource: str,
                 *, minimum: int | None = None, unit: int = 1) -> Draft:
        return Draft(resolved,Disposition.BOOKED,qty,qty if minimum is None else minimum,
                     unit,priority,minutes,reason,resource)

    rpm, stops, hours, oil, humidity, lots = resolved.raw
    if oil >= 53 and probe.window < 26:
        return block('润滑压差越限且缺停台挂牌时段')
    high_wear = hours > 525 and stops / max(1, rpm/600) > 17
    if value < 0.48 and not high_wear:
        return normal('保留安全库存，继续班间观测')
    family = '共用密封组' if oil >= 38 else '纬停检测组'
    if probe.pool.endswith('2'):
        family = family + 'B'
    need = 2 if lots >= 8 and high_wear else 1
    confidence = value * 91 + (15 if high_wear else 0) + stops / 8
    return proposal(need, confidence, 22, f'按实际机型扣{family}，安全库存另计', family)
