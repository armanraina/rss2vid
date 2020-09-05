from typing import Callable


class ProgressUpdater:
    def __init__(self, update_func: Callable[[int, int], None]):
        self.update_func = update_func

    def update_progress(self, progress: int, total: int):
        self.update_func(progress, total)
