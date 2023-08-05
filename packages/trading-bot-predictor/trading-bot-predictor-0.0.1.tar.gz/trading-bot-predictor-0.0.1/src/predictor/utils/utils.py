import os
import sys


class Utils:

    @staticmethod
    def create_dir(path: str) -> None:
        if not os.path.isdir(path):
            os.mkdir(path)

    @staticmethod
    def is_test() -> bool:
        return len(sys.argv) > 0 and 'test' in sys.argv[0]
