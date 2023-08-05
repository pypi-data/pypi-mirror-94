import datetime
from csv import DictWriter, DictReader
from datetime import datetime
from decimal import Decimal
from json import dumps, loads
from operator import attrgetter
from typing import Iterable, TextIO
from typing import List, Dict

from pandas import DataFrame

from predictor.common.constants import NAN
from predictor.dto.intraday_dto import IntradayDTO


class IntradayDTOConverter:

    @staticmethod
    def from_json(content: str) -> List[IntradayDTO]:
        result: List[IntradayDTO] = []
        rows: List[Dict[str]] = loads(content)
        for row in rows:
            intraday: IntradayDTO = IntradayDTO(date=datetime.fromisoformat(row['date']),
                                                o=Decimal(row['open']),
                                                high=Decimal(row['high']),
                                                low=Decimal(row['low']),
                                                close=Decimal(row['close']),
                                                volume=Decimal(row['volume']),
                                                symbol=row['symbol'])
            result.append(intraday)
        return result

    @staticmethod
    def to_json(intraday_list: List[IntradayDTO]) -> str:
        json_str: List[Dict[str, str]] = list(map(lambda row: dict(list(map(
            lambda i: (str(i[0]), str(float(i[1])) if isinstance(i[1], Decimal) else str(i[1])), filter(
                lambda e: not e[0].startswith('_'), row.__dict__.items())))), sorted(
            intraday_list, key=attrgetter('symbol'))))
        return dumps(json_str)

    @staticmethod
    def to_dataframe(intraday_list: List[IntradayDTO]) -> DataFrame:
        frame: DataFrame = DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume', 'symbol'])
        for i in range(len(intraday_list)):
            intraday: IntradayDTO = intraday_list[i]
            frame.loc[i] = [intraday.date,
                            float(intraday.open),
                            float(intraday.high),
                            float(intraday.low),
                            float(intraday.close),
                            float(intraday.volume),
                            intraday.symbol]
        return frame.fillna(NAN)

    @staticmethod
    def group_by_symbol(intraday_list: List[IntradayDTO]) -> List[List[IntradayDTO]]:
        return [[e for e in intraday_list if e.symbol == i] for i in set(map(lambda i: i.symbol, intraday_list))]

    @staticmethod
    def from_csv(csv_file: Iterable[str], symbol: str) -> List[IntradayDTO]:
        intraday_list: List[IntradayDTO] = []
        reader: DictReader = DictReader(csv_file)
        for row in reader:
            intraday: IntradayDTO = IntradayDTO(
                datetime.strptime(row['time'], '%Y-%m-%d %H:%M:%S'), Decimal(row['open']), Decimal(row['high']),
                Decimal(row['low']), Decimal(row['close']), Decimal(row['volume']), symbol)
            intraday_list.append(intraday)
        return intraday_list

    @staticmethod
    def to_csv(intraday_list: List[IntradayDTO], csv_file: TextIO) -> None:
        fieldnames: List[str] = ['time', 'open', 'high', 'low', 'close', 'volume']
        writer: DictWriter = DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for intraday in intraday_list:
            writer.writerow(
                {'time': intraday.date,
                 'open': intraday.open,
                 'high': intraday.high,
                 'low': intraday.low,
                 'close': intraday.close,
                 'volume': intraday.volume})
