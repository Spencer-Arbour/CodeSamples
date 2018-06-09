from time import sleep
from termcolor import cprint


class ProgressBar:

    def __init__(self, total: int, decimals: int=1, length: int=50, fill: str="█"):
        self._total = total - 1
        self._decimals = decimals
        self._length = length
        self._fill = fill

        self._current_completion = 0
        self._percent = 0
        self._finished_section = 0
        self._unfinished_section = 0

        self.calculate_progress()

    def calculate_progress(self, current_progress: int = 0) -> "ProgressBar":
        self._percent = ("{0:." + str(self._decimals) + "f}").format(
            100 * (current_progress / float(self._total))
        )
        filled_length = int(self._length * current_progress // self._total)
        self._finished_section = filled_length * self._fill
        self._unfinished_section = "-" * (self._length - filled_length)

        return self

    def print_progress(self) -> "ProgressBar":
        cprint("\rProgress: [", color="white", end="", flush=True)
        cprint("{0}".format(self._finished_section), color="green", end="", flush=True)
        cprint("{0}] {1}% Completed".format(
            self._unfinished_section,
            self._percent
        ), color="white", end="", flush=True)

        return self


if __name__ == "__main__":
    items = list(range(0, 57))
    length = len(items)

    # Initial call to print 0% progress
    p = ProgressBar(length, length=50).print_progress()
    for i, item in enumerate(items):
        sleep(0.3)
        p.calculate_progress(i).print_progress()
