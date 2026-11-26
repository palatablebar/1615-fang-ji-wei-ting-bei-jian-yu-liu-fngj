from math import log1p, sqrt


def derive(values: tuple[float, ...]) -> tuple[float, ...]:
    """从织机巡检单原始读数生成五个模型轴。"""
    rpm, stops, hours, oil, humidity, lots = values
    speed_factor = rpm / 600
    stops_per_shift_turns = stops / speed_factor
    running_hours = log1p(hours * speed_factor)
    lubricant_excursion = max(0.0, oil - 28) + max(0.0, 9 - oil) * 1.8
    humidity_load = abs(64.0 - humidity) * speed_factor
    switch_rate = lots / (1 + sqrt(speed_factor))
    return stops_per_shift_turns, running_hours, lubricant_excursion, humidity_load, switch_rate
