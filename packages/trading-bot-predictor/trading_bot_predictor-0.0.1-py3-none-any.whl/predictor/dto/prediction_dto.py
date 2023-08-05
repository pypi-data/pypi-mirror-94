from typing import NoReturn


class PredictionDTO:

    def __init__(self, delta: float) -> NoReturn:
        self.delta: float = delta
