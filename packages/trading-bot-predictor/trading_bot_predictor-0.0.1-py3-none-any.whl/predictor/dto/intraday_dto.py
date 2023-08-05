from datetime import datetime
from decimal import Decimal
from typing import NoReturn


class IntradayDTO:

    def __init__(self, date: datetime, o: Decimal, high: Decimal, low: Decimal, close: Decimal, volume: Decimal,
                 symbol: str) -> NoReturn:
        self.date: datetime = date
        self.open: Decimal = o
        self.high: Decimal = high
        self.low: Decimal = low
        self.close: Decimal = close
        self.volume: Decimal = volume
        self.symbol: str = symbol
