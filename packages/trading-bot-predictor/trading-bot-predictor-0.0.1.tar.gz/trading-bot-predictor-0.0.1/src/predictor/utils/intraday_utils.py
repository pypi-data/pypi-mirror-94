import csv
import os
from decimal import Decimal
from random import random, seed
from time import sleep
from typing import List, Final, IO, Optional

from alpha_vantage.timeseries import TimeSeries
from pandas import date_range, DatetimeIndex

from predictor.converter.intraday_dto_converter import IntradayDTOConverter
from predictor.dto.intraday_dto import IntradayDTO
from predictor.utils.predictor_utils import PredictorUtils
from predictor.utils.utils import Utils


class IntradayUtils:
    YEAR_RANGE: Final[int] = 2
    MONTH_RANGE: Final[int] = 12
    CSV_PATH: Final[str] = os.path.join('..', '..', 'data', 'symbol{}_year{}_month{}.csv')
    JSON_PATH: Final[str] = os.path.join('..', '..', 'data', 'test_data.json')

    @classmethod
    def generate_test_data(cls, write_file: bool = False) -> Optional[List[IntradayDTO]]:
        intraday_list: List[IntradayDTO] = []
        dates: DatetimeIndex = date_range(
            end='2020-12-01', periods=PredictorUtils.SUFFICIENT_DATA).to_pydatetime().tolist()
        for i, date in enumerate(dates):
            decimal: List[Decimal] = []
            for j in range(5):
                seed(i * j)
                decimal.append(Decimal(random()))
            intraday: IntradayDTO = IntradayDTO(date, decimal[0], decimal[1], decimal[2], decimal[3], decimal[4], 'AAA')
            intraday_list.append(intraday)
        if write_file:
            file: IO = open(cls.JSON_PATH, 'a')
            file.write(IntradayDTOConverter.to_json(intraday_list))
            file.close()
        else:
            return intraday_list

    @classmethod
    def write_time_series_intraday_extended(cls, symbol: str = 'IBM') -> None:
        Utils.create_dir(os.path.join('..', '..', '..', 'data'))
        time_series = TimeSeries(output_format='csv')
        for year in range(cls.YEAR_RANGE):
            for month in range(cls.MONTH_RANGE):
                path: str = cls.CSV_PATH.format(symbol, year + 1, month + 1)
                if not os.path.isfile(path):
                    s: str = 'year{}month{}'.format(year + 1, month + 1)
                    csv_reader, _ = time_series.get_intraday_extended(symbol, slice=s)
                    csv_file: IO = open(path, 'a')
                    writer = csv.writer(csv_file)
                    writer.writerows(csv_reader)
                    if not Utils.is_test():
                        sleep(25)

    @classmethod
    def read_time_series_intraday_extended(cls, symbol: str = 'IBM') -> List[IntradayDTO]:
        intraday_list: List[IntradayDTO] = []
        for year in range(cls.YEAR_RANGE):
            for month in range(cls.MONTH_RANGE):
                path: str = cls.CSV_PATH.format(symbol, year + 1, month + 1)
                intraday_list.extend(IntradayDTOConverter.from_csv(open(path, 'r'), symbol))
        return intraday_list


if __name__ == '__main__':
    IntradayUtils.write_time_series_intraday_extended()
    print(IntradayUtils.read_time_series_intraday_extended())
