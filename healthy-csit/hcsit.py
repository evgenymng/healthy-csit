import codecs
import csv
from datetime import datetime, timedelta
from datetime import time
import argparse

from pkg_resources import require

from health_params import *

class PersonParams(object):
    def __init__(self,
                 height: float, # рост
                 weight: float, # вес
                 heart_beat_rate: int, # частота сердечного стука
                 bp: tuple[int, int], # А/Д
                 appetite: int, # аппетит
                 sleep_start: time, # время начала сна
                 sleep_end: time # конец сна
                 ) -> None:
        if height <= 0:
            raise ValueError('person\'s height <= 0')
        self.height = height

        if weight <= 0:
            raise ValueError('person\'s weight <= 0')
        self.weight = weight

        if heart_beat_rate <= 0:
            raise ValueError('person\'s heart beat rate <= 0')
        self.hbr = heart_beat_rate

        if len(bp) != 2 or type(bp[0]) != int or type(bp[1]) != int:
            raise ValueError('invalid blood pressure value format')
        self.bp = bp

        if appetite < 0 or appetite > 2:
            raise ValueError('person\'s average appetite level is out of bounds')
        self.appetite = appetite
        
        self.sleep_start = sleep_start
        self.sleep_end = sleep_end

class DiaryParams(object):
    def __init__(self,
                 date_start: datetime,
                 date_end: datetime
                 ) -> None:

        # Raises a ValueError if something is wrong
        # TODO: implement catch on object construction
        if date_end < date_start:
            raise ValueError('the start date is past the end date')

        self.date_start = date_start
        self.date_end = date_end



def gen_regular_day(person: PersonParams, d: str) -> list:
    row = []

    dur, s_time, e_time = Generator.get_sleep(person.sleep_start, person.sleep_end)
    s_time_str = str(s_time.hour).rjust(2, '0') + ':' + str(s_time.minute).rjust(2, '0')
    e_time_str = str(e_time.hour).rjust(2, '0') + ':' + str(e_time.minute).rjust(2, '0')

    bp = Generator.get_bp(person.bp)

    row = [
        d,
        int(round(person.height)),
        round(Generator.get_weight(person.weight), 1),
        Generator.get_hbr(person.hbr),
        f'{bp[0]}/{bp[1]}',
        Generator.get_appetite(person.appetite),
        f'{dur}\n({s_time_str}–{e_time_str})',
        Generator.get_pe(),
        Generator.get_wb(),
        'нет',
        'нет',
        'нет',
        'нет',
        'нет',
        'нет',
        Generator.get_irritability(0)
    ]

    return row

def gen_bad_day(person: PersonParams, d: str) -> list:
    row = []

    # BUG: если установленный пользователем интервал сна слишком маленький, здесь получатся
    # непредвиденные результаты.
    _, s_time, e_time = Generator.get_sleep(person.sleep_start, person.sleep_end)
    s_time = time(hour=(s_time.hour + 2) % 24, minute=s_time.minute)
    e_time = time(hour=(e_time.hour - 1) % 24, minute=e_time.minute)
    s_time_str = str(s_time.hour).rjust(2, '0') + ':' + str(s_time.minute).rjust(2, '0')
    e_time_str = str(e_time.hour).rjust(2, '0') + ':' + str(e_time.minute).rjust(2, '0')

    _dur = (
        str((e_time.hour - s_time.hour - (1 if e_time.minute < s_time.minute else 0)) % 24).rjust(2, '0'),
        str((e_time.minute - s_time.minute) % 60).rjust(2, '0')
    )

    dur = _dur[0] + ":" + _dur[1]

    bp = Generator.get_bp(person.bp)

    row = [
        d,
        int(round(person.height)),
        round(Generator.get_weight(person.weight), 1),
        Generator.get_hbr(person.hbr),
        f'{bp[0]}/{bp[1]}',
        Generator.get_appetite(person.appetite - 2),
        f'{dur}\n({s_time_str}–{e_time_str})',
        'нет',
        'удовл.',
        'да',
        'да',
        'нет',
        'нет',
        'нет',
        'нет',
        Generator.get_irritability(1)
    ]

    return row

SPREADSHEET_NUMBERING = [''] + [str(i) for i in range(1, 9)] + ['8.'+str(i) for i in range(1, 8)]

SPREADSHEET_LABELS = [
    '',
    'Рост (см)',
    'Вес (кг)',
    'ЧСС (уд/мин) в покое',
    'Давление (А/Д)',
    'Аппетит',
    'Сон',
    'Физическая нагрузка',
    'Самочувствие',
    'Сонливость, усталость',
    'Невозможно сосредоточиться',
    'Головные боли',
    'Боли в желудке',
    'Сухость глаз',
    'Головокружение',
    'Раздражительность'
]

def parse_time(ts: str) -> time:
    spl = ts.split(sep=':')
    if len(spl) == 2 and len(spl[0]) == 2 and len(spl[1]) == 2:
        try:
            hour = int(spl[0])
            minute = int(spl[1])
            if hour >= 0 and hour <= 23 and minute >= 0 and minute <= 59:
                return time(hour=hour, minute=minute)
        except ValueError:
            pass

    raise argparse.ArgumentTypeError('not a valid time format (HH:MM expected)')

def parse_bp(bps: str) -> tuple[int, int]:
    spl = bps.split(sep='/')
    if len(spl) == 2:
        try:
            upper = int(spl[0])
            lower = int(spl[1])
            if upper > 0 and lower > 0:
                return (upper, lower)
        except ValueError:
            pass

    raise argparse.ArgumentTypeError('not a valid arterial blood pressure format (N/M expected)')

def parse_date(ds: str) -> datetime:
    try:
        return datetime.strptime(ds, '%d.%m.%y')
    except ValueError:
        try:
            return datetime.strptime(ds, '%d.%m.%Y')
        except ValueError:
            raise argparse.ArgumentTypeError('not a valid date format (dd.mm.yy or dd.mm.yyyy expected)')

def main():
    parser = argparse.ArgumentParser(description=
        """
        Generate a .csv spreadsheet with RANDOM health parameters, for your
        PE course (see disclaimer below).

        Disclaimer #1!
        The generated values are completely fictional and cannot
        be associated with any person in the world. This application
        RANDOMLY MAKES UP values based on the parameters you've provided.
        The spreadsheet files created by this application or any other
        output of the application must not be treated at face value.
        If you have health problems, please, consult your doctor.\r\n

        Disclaimer #2!
        I provide no guarantee, that your PE prof. or teacher will
        accept the generated data.
        """,
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument('outfile', metavar='path/to/file', type=str, nargs='?',
                        help='an output file path to write the data to', default='healthy-csit.csv')

    parser.add_argument('-ht', '--height', metavar='N cm', type=float, nargs='?',
                        help='a person\'s height in cm', required=True)

    parser.add_argument('-w', '--weight', metavar='N kg', type=float, nargs='?',
                        help='a person\'s weight in kg', required=True)

    parser.add_argument('-hbr', '--heart-beat-rate', metavar='N bpm', type=int, nargs='?',
                        help='a person\'s heart beat rate in beats per minute', required=True)

    parser.add_argument('-bp', '--blood-pressure', metavar='N/M', type=parse_bp, nargs='?',
                        help='a person\'s arterial blood pressure', required=True)

    parser.add_argument('-a', '--appetite', metavar='N', type=int, choices=range(0, 3), default=1, nargs='?',
                        help='a person\'s usual appetite: 0 - bad, 1 - good [default], 2 - great')

    parser.add_argument('-ss', '--sleep-start', metavar='HH:MM', type=parse_time, nargs='?',
                        default=time(hour=22, minute=0),
                        help='a person\'s usual bedtime (in 24-hour format). Defaults to 22:00.')

    parser.add_argument('-se', '--sleep-end', metavar='HH:MM', type=parse_time, nargs='?',
                        default=time(hour=7, minute=0),
                        help='a person\'s usual wake-up time (in 24-hour format). Defaults to 07:00')

    parser.add_argument('-ds', '--date-start', metavar='dd.mm.yy | dd.mm.yyyy', type=parse_date, nargs='?',
                        default=datetime(day=10, month=9, year=2022),
                        help='the start date of the diary. Defaults to 10.09.2022')

    parser.add_argument('-de', '--date-end', metavar='dd.mm.yy | dd.mm.yyyy', type=parse_date, nargs='?',
                        default=datetime(day=10, month=10, year=2022),
                        help='the end date of the diary. Defaults to 10.10.2022')

    args = parser.parse_args()

    person = PersonParams(args.height, args.weight, args.heart_beat_rate, args.blood_pressure, args.appetite, args.sleep_start, args.sleep_end)
    diary = DiaryParams(args.date_start, args.date_end)

    data = [[] for _ in range((diary.date_end - diary.date_start).days + 1)]

    curr_date = diary.date_start

    print('> Begin data generation.')
    # main loop. Data generation
    while curr_date <= diary.date_end:
        i = (curr_date - diary.date_start).days

        date_field = str(curr_date.day).rjust(2, '0') + '.' + str(curr_date.month).rjust(2, '0')
        if diary.date_end.year != diary.date_start.year:
            date_field += '.' + str(curr_date.year)

        if Generator.is_bad_day(): # oops, unlucky. Stats are worse
            data[i] = gen_bad_day(person, date_field)
        else: # a regular day
            data[i] = gen_regular_day(person, date_field)

        curr_date += timedelta(1) # + 1 day

    print('> Finish data generation.')

    print('> Open the output file in binary mode.')

    with open(args.outfile, 'wb') as outfile_bytes:
        print(
f'> File opened\n\
    name: {outfile_bytes.name}'
)
        outfile_bytes.write(codecs.BOM_UTF8)

    print('> Open the output file in text mode.')

    with open(args.outfile, 'a', encoding='utf-8', newline='') as outfile:
        print(
f'> File opened\n\
    name: {outfile.name}\n\
    delimiter: \',\'\n\
    encoding: utf-8 with BOM\n\
    dialect: MS Excel'
)
        wr = csv.writer(outfile, dialect=csv.excel, delimiter=';')
        print('> Write column numbers...')
        wr.writerow(SPREADSHEET_NUMBERING)
        print('> Write column headings...')
        wr.writerow(SPREADSHEET_LABELS)
        print('> Write data...')
        wr.writerows(data)

    print('> All done!')

if __name__ == "__main__":
    main()