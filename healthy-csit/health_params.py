import random
from datetime import time

def clamp_int(v: int, min: int, max: int) -> int:
    if v > max: return max
    if v < min: return min
    return v

def clamp_float(v: float, min: float, max: float) -> float:
    if v < min: return min
    if v > max: return max
    return v

class Appetite(object):
    @staticmethod
    def get(l: int) -> str:
        if l < 0 or l > 2:
            raise ValueError('appetite value out of range')
        if l == 0: return 'плохой'
        if l == 1: return 'хороший'
        return 'отличный'

class Irritability(object):
    @staticmethod
    def get(l: int) -> str:
        if l < 0 or l > 1:
            raise ValueError('irritability value out of range')
        if l == 0: return 'нормальная'
        return 'повышенная'

class PhyscialExercise(object):
    @staticmethod
    def get(l: int) -> str:
        if l < 0 or l > 7:
            raise ValueError('physical exercise value out of range')
        if l == 0:
            return '30 мин\n(пешая прогулка)'
        if l == 1:
            return '1 ч\n(пешая прогулка)'
        if l == 2:
            return '1,5 ч\n(пешая прогулка)'
        if l == 3:
            return 'нет'
        if l == 4:
            return '30 мин\n(пешая прогулка)'
        if l == 5:
            return '1 ч\n(спортзал)'
        if l == 6:
            return '10 мин\n(пробежка на улице)'
        return '1 ч\n(пешая прогулка)'

class WellBeing(object):
    @staticmethod
    def get(l: int) -> str:
        if l < 0 or l > 2:
            raise ValueError('well-being value out of range')
        if l == 0:
            return 'удовл.'
        if l == 1:
            return 'хорошее'
        return 'отличное'

class Generator(object):
    BAD_DAY_RANGE = 10
    WEIGHT_DELTA = 3.0
    HBR_DELTA = 22
    UPPER_BP_DELTA = 19
    LOWER_BP_DELTA = 13
    MINUTES_DELTA = 160

    @staticmethod
    def is_bad_day() -> bool:
        return random.randint(0, Generator.BAD_DAY_RANGE) == 0

    @staticmethod
    def get_weight(weight: float) -> float:
        return weight - random.random() * Generator.WEIGHT_DELTA + 2.0

    @staticmethod
    def get_hbr(hbr: int) -> int:
        return hbr - random.randint(0, Generator.HBR_DELTA) + Generator.HBR_DELTA // 2

    @staticmethod
    def get_bp(bp: tuple[int, int]) -> tuple[int, int]:
        return (
            bp[0] - random.randint(0, Generator.UPPER_BP_DELTA) + Generator.UPPER_BP_DELTA // 2,
            bp[1] - random.randint(0, Generator.LOWER_BP_DELTA) + Generator.LOWER_BP_DELTA // 2
        )

    @staticmethod
    def get_appetite(appetite: int) -> str:
        return Appetite.get(
            clamp_int(
                appetite - random.randint(0, 2) + 1 + int(random.randint(0, 10) == 0), 0, 2
            )
        )
    
    @staticmethod
    def get_sleep(sleep_start: time, sleep_end: time) -> tuple[str, time, time]:
        minute_delta_s = random.randint(0, Generator.MINUTES_DELTA) - Generator.MINUTES_DELTA // 2
        hour_delta_s = (-1 if minute_delta_s < 0 else 1) * (abs(minute_delta_s) // 60)
        minute_delta_s = (-1 if minute_delta_s < 0 else 1) * (abs(minute_delta_s) % 60)

        minute_delta_e = random.randint(0, Generator.MINUTES_DELTA) - Generator.MINUTES_DELTA // 2
        hour_delta_e = (-1 if minute_delta_e < 0 else 1) * (abs(minute_delta_e) // 60)
        minute_delta_e = (-1 if minute_delta_e < 0 else 1) * (abs(minute_delta_e) % 60)

        new_start = time(
            hour=((sleep_start.hour + hour_delta_s) % 24),
            minute=((sleep_start.minute + minute_delta_s) % 60)
        )

        new_end = time(
            hour=((sleep_end.hour + hour_delta_e) % 24),
            minute=((sleep_end.minute + minute_delta_e) % 60)
        )

        sleep_dur = (
            str((new_end.hour - new_start.hour - (1 if new_end.minute < new_start.minute else 0)) % 24).rjust(2, '0'),
            str((new_end.minute - new_start.minute) % 60).rjust(2, '0')
        )

        return (
            sleep_dur[0] + ':' + sleep_dur[1],
            new_start,
            new_end
        )

    @staticmethod
    def get_pe() -> str:
        return PhyscialExercise.get(random.randint(0, 7))

    @staticmethod
    def get_wb() -> str:
        return WellBeing.get(random.randint(0, 2))

    @staticmethod
    def get_irritability(l: int) -> str:
        return Irritability.get(l)